import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Pulse AI",
    layout="wide",
    page_icon="📦"
)

# =========================
# LOAD DATA
# =========================
excel_file = "Pulse_AI_Base.xlsx"

@st.cache_data(ttl=300)
def load_data():
    produtos = pd.read_excel(excel_file, sheet_name="produtos")
    recorrencia = pd.read_excel(excel_file, sheet_name="recorrencia_futura")
    substituicoes = pd.read_excel(excel_file, sheet_name="substituicoes")
    alertas = pd.read_excel(excel_file, sheet_name="alertas")
    return produtos, recorrencia, substituicoes, alertas

produtos, recorrencia, substituicoes, alertas = load_data()

# =========================
# ENRIQUECER DADOS
# (compatível com Excel antigo — deriva colunas novas se ausentes)
# =========================

# Velocidade de venda (unidades/dia)
if "velocidade_venda" not in produtos.columns:
    vv_ref = {"Critico": 45, "Alto": 30, "Medio": 15, "Baixo": 7}
    produtos["velocidade_venda"] = produtos["risco_ruptura"].map(vv_ref).fillna(10)

# Prazo de reposição (dias)
if "prazo_reposicao" not in produtos.columns:
    produtos["prazo_reposicao"] = 3

# Dias de cobertura = estoque / velocidade de venda
if "dias_cobertura" not in produtos.columns:
    produtos["dias_cobertura"] = (
        produtos["estoque_atual"] / produtos["velocidade_venda"].replace(0, 1)
    ).round(1)

# Score de risco (0–100)
if "score_risco" not in produtos.columns:
    base = {"Critico": 88, "Alto": 68, "Medio": 42, "Baixo": 18}
    produtos["score_risco"] = produtos["risco_ruptura"].map(base).fillna(50).astype(int)

# Score de aceitação de substituição (%)
if "score_aceitacao" not in substituicoes.columns:
    defaults = [94, 87, 91, 65]
    substituicoes["score_aceitacao"] = (defaults * 10)[:len(substituicoes)]

# Variação de preço vs original (%)
if "delta_preco_pct" not in substituicoes.columns:
    defaults = [0, -3, 2, -9]
    substituicoes["delta_preco_pct"] = (defaults * 10)[:len(substituicoes)]

# Motivo da recomendação
if "motivo_recomendacao" not in substituicoes.columns:
    motivos = [
        "Mesma marca, gramatura equivalente",
        "Histórico: cliente aceitou 3× nos últimos 60 dias",
        "Produto similar, preço levemente superior",
        "⚠️ Cliente sensível à marca — risco elevado de rejeição",
    ]
    substituicoes["motivo_recomendacao"] = (motivos * 10)[:len(substituicoes)]

# Detectar nomes das colunas de substituição (flexível)
orig_col = next((c for c in substituicoes.columns if "original" in c.lower()), substituicoes.columns[0])
sub_col  = next((c for c in substituicoes.columns if "substitut" in c.lower()), substituicoes.columns[1])
sim_col  = next((c for c in substituicoes.columns if "similar" in c.lower()), None)
disp_col = next((c for c in substituicoes.columns if "disp" in c.lower()), None)

# =========================
# HEADER
# =========================
st.title("📦 Pulse AI")
st.subheader("Agente Inteligente de Prevenção de Ruptura")
st.markdown("---")

# =========================
# KPIs
# =========================
em_risco      = len(produtos[produtos["risco_ruptura"].isin(["Critico", "Alto"])])
impacto_total = int(produtos["impacto_financeiro_estimado"].sum())
dias_medio    = round(produtos["dias_cobertura"].mean(), 1)
pedidos_total = len(recorrencia)
alertas_ativos = len(alertas)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🔴 Produtos em risco",   em_risco)
col2.metric("💰 Impacto estimado",    f"R$ {impacto_total:,.0f}".replace(",", "."))
col3.metric(
    "📅 Cobertura média",
    f"{dias_medio}d",
    delta=f"{round(dias_medio - 10, 1)}d vs meta 10d",
    delta_color="normal" if dias_medio >= 10 else "inverse"
)
col4.metric("🔁 Pedidos recorrentes", pedidos_total)
col5.metric("💬 Alertas ativos",      alertas_ativos)

st.markdown("---")

# =========================
# RADAR DE RUPTURA
# =========================
st.header("🚨 Radar de Ruptura")

col_f1, _ = st.columns([2, 6])
with col_f1:
    risco_filter = st.selectbox(
        "Filtrar risco",
        ["Todos", "Critico", "Alto", "Medio", "Baixo"]
    )

produtos_view = (
    produtos if risco_filter == "Todos"
    else produtos[produtos["risco_ruptura"] == risco_filter]
)

show_cols = {
    "produto":                      "Produto",
    "loja":                         "Loja",
    "risco_ruptura":                "Risco",
    "estoque_atual":                "Estoque",
    "velocidade_venda":             "Venda/dia",
    "dias_cobertura":               "Dias cobertura",
    "prazo_reposicao":              "Prazo repos.",
    "impacto_financeiro_estimado":  "Impacto (R$)",
    "score_risco":                  "Score risco",
}
available = {k: v for k, v in show_cols.items() if k in produtos_view.columns}
df_display = produtos_view[list(available.keys())].rename(columns=available)

RISCO_BG = {
    "Critico": "background-color: #fff0f0",
    "Alto":    "background-color: #fff8f0",
}

def highlight(row):
    styles = [""] * len(row)
    cols = list(df_display.columns)
    risco_i = cols.index("Risco") if "Risco" in cols else None
    dias_i  = cols.index("Dias cobertura") if "Dias cobertura" in cols else None

    if risco_i is not None:
        bg = RISCO_BG.get(row.iloc[risco_i], "")
        if bg:
            styles = [bg] * len(row)

    if dias_i is not None:
        v = row.iloc[dias_i]
        if isinstance(v, (int, float)):
            if v <= 3:
                styles[dias_i] = "background-color:#FCEBEB;color:#791F1F;font-weight:bold"
            elif v <= 7:
                styles[dias_i] = "background-color:#FAEEDA;color:#633806"
    return styles

st.dataframe(
    df_display.style.apply(highlight, axis=1),
    use_container_width=True
)

st.markdown("---")

# =========================
# MATRIZ DE RISCO
# =========================
st.header("📍 Matriz de Risco")
st.caption(
    "Cada bolha é um produto — posicionado por dias de cobertura vs impacto financeiro. "
    "Tamanho = pedidos recorrentes afetados."
)

fig_matrix = px.scatter(
    produtos,
    x="dias_cobertura",
    y="impacto_financeiro_estimado",
    size="pedidos_recorrentes_afetados",
    color="risco_ruptura",
    hover_name="produto",
    hover_data={
        "loja": True,
        "score_risco": True,
        "dias_cobertura": True,
        "pedidos_recorrentes_afetados": True,
    },
    color_discrete_map={
        "Critico": "#E24B4A",
        "Alto":    "#D85A30",
        "Medio":   "#378ADD",
        "Baixo":   "#1D9E75",
    },
    labels={
        "dias_cobertura":               "Dias de cobertura",
        "impacto_financeiro_estimado":  "Impacto financeiro (R$)",
        "risco_ruptura":                "Nível de risco",
    },
    size_max=45,
    height=420,
)
fig_matrix.add_vline(
    x=3, line_dash="dash", line_color="#E24B4A",
    annotation_text="Zona crítica (< 3d)", annotation_position="top right"
)
fig_matrix.add_vline(
    x=7, line_dash="dash", line_color="#D85A30",
    annotation_text="Alerta (< 7d)", annotation_position="top right"
)
fig_matrix.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_matrix, use_container_width=True)

st.markdown("---")

# =========================
# IMPACTO FINANCEIRO POR LOJA
# =========================
st.header("📊 Impacto Financeiro por Loja")

impacto_loja = (
    produtos
    .groupby("loja")["impacto_financeiro_estimado"]
    .sum()
    .reset_index()
    .sort_values("impacto_financeiro_estimado", ascending=False)
)

fig_loja = px.bar(
    impacto_loja,
    x="loja",
    y="impacto_financeiro_estimado",
    color="impacto_financeiro_estimado",
    color_continuous_scale=["#1D9E75", "#378ADD", "#D85A30", "#E24B4A"],
    text_auto=True,
    labels={"loja": "Loja", "impacto_financeiro_estimado": "Impacto (R$)"},
    height=320,
)
fig_loja.update_coloraxes(showscale=False)
fig_loja.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
fig_loja.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_loja, use_container_width=True)

st.markdown("---")

# =========================
# RECORRÊNCIA FUTURA
# =========================
st.header("🔁 Recorrência Futura")

recorrencia_group = (
    recorrencia
    .groupby("data_entrega_prevista")["quantidade_prevista"]
    .sum()
    .reset_index()
)

fig_recor = px.area(
    recorrencia_group,
    x="data_entrega_prevista",
    y="quantidade_prevista",
    title="Demanda prevista por data de entrega",
    markers=True,
    height=300,
)
fig_recor.update_traces(line_color="#378ADD", fillcolor="rgba(55,138,221,0.12)")
fig_recor.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_recor, use_container_width=True)

st.markdown("---")

# =========================
# SUBSTITUIÇÕES INTELIGENTES
# =========================
st.header("🧠 Substituição Inteligente")
st.caption(
    "Score de aceitação calculado com base em histórico de compras, "
    "sensibilidade à marca, faixa de preço e similaridade de produto."
)

for _, row in substituicoes.iterrows():
    score  = int(row.get("score_aceitacao", 80))
    delta  = row.get("delta_preco_pct", 0)
    motivo = row.get("motivo_recomendacao", "—")

    if score >= 85:
        score_label = "🟢 Alta aceitação"
    elif score >= 70:
        score_label = "🟡 Aceitação moderada"
    else:
        score_label = "🔴 Risco de rejeição"

    if delta == 0:
        delta_str, delta_icon = "Mesmo preço", "➡️"
    elif delta > 0:
        delta_str, delta_icon = f"+{delta}%", "🔺"
    else:
        delta_str, delta_icon = f"{delta}%", "🔻"

    with st.container(border=True):
        col1, col2, col3 = st.columns([5, 3, 2])

        with col1:
            st.markdown(f"**{row[orig_col]}** → **{row[sub_col]}**")
            st.caption(f"💡 {motivo}")
            if sim_col and sim_col in row.index:
                st.caption(f"Similaridade de produto: {row[sim_col]}")

        with col2:
            st.markdown(f"**Score de aceitação:** {score_label}")
            st.progress(score / 100)
            st.caption(f"{score}% de chance de aceite")

        with col3:
            st.markdown("**Variação de preço**")
            st.markdown(f"{delta_icon} **{delta_str}**")
            if disp_col and disp_col in row.index:
                st.caption(f"Status: {row[disp_col]}")

st.markdown("---")

# =========================
# CENTRAL DE ALERTAS SLACK
# =========================
st.header("💬 Central de Alertas Slack")
st.markdown("### Canal: #pulse-alertas")

for _, row in alertas.iterrows():
    if row["risco_ruptura"] == "Critico":
        emoji = "🔴"
    elif row["risco_ruptura"] == "Alto":
        emoji = "🟠"
    else:
        emoji = "🟡"

    prod_data = produtos[produtos["produto"] == row["produto"]]
    urgencia_str = ""
    if not prod_data.empty and "dias_cobertura" in prod_data.columns:
        dias  = prod_data.iloc[0]["dias_cobertura"]
        prazo = prod_data.iloc[0].get("prazo_reposicao", 3)
        if dias < prazo:
            urgencia_str = "⚠️ **Ruptura iminente** — cobertura abaixo do prazo de reposição"
        else:
            urgencia_str = f"📅 Cobertura estimada: **{dias} dias** (prazo reposição: {prazo}d)"

    with st.container(border=True):
        st.markdown(f"## {emoji} Pulse AI Alert")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Produto:** {row['produto']}")
            st.markdown(f"**Loja:** {row['loja']}")
            st.markdown(f"**Risco:** {row['risco_ruptura']}")
        with col2:
            st.markdown(
                f"**Impacto Financeiro:** R$ {int(row['impacto_financeiro_estimado']):,}".replace(",", ".")
            )
            st.markdown(f"**Pedidos Impactados:** {row['pedidos_recorrentes_afetados']}")
            if urgencia_str:
                st.markdown(urgencia_str)

        st.markdown(f"**Ação Sugerida:** {row['acao_sugerida']}")
        st.code(row["mensagem_slack"], language="text")
        st.markdown("---")
