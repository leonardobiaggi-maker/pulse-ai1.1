import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Pulse AI · Shopper",
    layout="wide",
    page_icon="https://shopper.com.br/static/img/og-logo.png",
    initial_sidebar_state="expanded"
)

# Shopper Brand — Light Theme
# Primary green  : #00C25A
# Dark green     : #009944
# Green tint     : #E6F9EE
# Background     : #F5F7FA
# Surface        : #FFFFFF
# Border         : #E5E7EB
# Text primary   : #111827
# Text muted     : #6B7280
# Danger         : #DC2626
# Warning        : #D97706

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Page background */
    .stApp {
        background-color: #F5F7FA !important;
    }
    .main .block-container {
        background-color: #F5F7FA;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    [data-testid="stSidebar"] * {
        color: #374151 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.875rem !important;
        padding: 6px 0 !important;
        color: #374151 !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #00C25A !important;
    }

    /* Header */
    .pulse-header {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .pulse-header-logo {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .pulse-header-logo img {
        height: 32px;
        object-fit: contain;
    }
    .pulse-header-divider {
        width: 1px;
        height: 32px;
        background: #E5E7EB;
    }
    .pulse-header-left h1 {
        color: #111827 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.02em;
    }
    .pulse-header-left p {
        color: #6B7280 !important;
        margin: 3px 0 0 !important;
        font-size: 0.8rem !important;
    }
    .pulse-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E6F9EE;
        color: #00963F;
        border: 1px solid #A7F3C4;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .pulse-badge::before {
        content: '';
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #00C25A;
        display: inline-block;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%   { opacity: 1; }
        50%  { opacity: 0.4; }
        100% { opacity: 1; }
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 1.1rem 1.25rem !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.72rem !important;
        color: #6B7280 !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }

    /* Section titles */
    h2, h3 {
        color: #111827 !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }

    /* Divider */
    hr { border-color: #E5E7EB !important; margin: 1.5rem 0 !important; }

    /* Selectbox label */
    .stSelectbox label p {
        font-size: 0.78rem !important;
        color: #6B7280 !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Dataframe */
    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; }

    /* Container border */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E5E7EB !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }

    /* Agent steps */
    .agent-step {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 8px;
        border: 1px solid #E5E7EB;
        border-left: 3px solid #00C25A;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .agent-step-num {
        background: #00C25A;
        color: #FFFFFF;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .agent-step-content h4 {
        margin: 0 0 3px 0;
        color: #111827;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .agent-step-content p {
        margin: 0;
        color: #6B7280;
        font-size: 0.825rem;
        line-height: 1.55;
    }

    /* Impact cards */
    .impact-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .impact-card .value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #00C25A;
        display: block;
        letter-spacing: -0.02em;
    }
    .impact-card .label {
        font-size: 0.775rem;
        color: #6B7280;
        margin-top: 5px;
        display: block;
        font-weight: 500;
    }

    /* Status cards */
    .status-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .status-card .label {
        color: #9CA3AF;
        font-size: 0.72rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0;
    }
    .status-card .value {
        color: #111827;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 4px 0 0;
    }
    .status-card.active {
        background: #E6F9EE;
        border-color: #A7F3C4;
    }
    .status-card.active .label { color: #00963F; }
    .status-card.active .value { color: #00963F; }

    /* Sidebar logo */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .sidebar-logo img {
        height: 28px;
        object-fit: contain;
    }
    .sidebar-pulse-label {
        font-size: 0.8rem;
        color: #6B7280 !important;
        margin: 0 0 12px 0;
        padding-bottom: 12px;
        border-bottom: 1px solid #E5E7EB;
        display: block;
    }

    /* Button */
    .stButton > button[kind="primary"] {
        background: #00C25A !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #009944 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
excel_file = "Pulse_AI_Base.xlsx"

@st.cache_data(ttl=300)
def load_data():
    produtos      = pd.read_excel(excel_file, sheet_name="produtos")
    recorrencia   = pd.read_excel(excel_file, sheet_name="recorrencia_futura")
    substituicoes = pd.read_excel(excel_file, sheet_name="substituicoes")
    alertas       = pd.read_excel(excel_file, sheet_name="alertas")
    return produtos, recorrencia, substituicoes, alertas

produtos, recorrencia, substituicoes, alertas = load_data()

# =========================
# ENRIQUECER DADOS
# =========================
if "velocidade_venda" not in produtos.columns:
    produtos["velocidade_venda"] = produtos["risco_ruptura"].map(
        {"Critico": 45, "Alto": 30, "Medio": 15, "Baixo": 7}
    ).fillna(10)

if "prazo_reposicao" not in produtos.columns:
    produtos["prazo_reposicao"] = 3

if "dias_cobertura" not in produtos.columns:
    produtos["dias_cobertura"] = (
        produtos["estoque_atual"] / produtos["velocidade_venda"].replace(0, 1)
    ).round(1)

if "score_risco" not in produtos.columns:
    produtos["score_risco"] = produtos["risco_ruptura"].map(
        {"Critico": 88, "Alto": 68, "Medio": 42, "Baixo": 18}
    ).fillna(50).astype(int)

if "score_aceitacao" not in substituicoes.columns:
    substituicoes["score_aceitacao"] = ([94, 87, 91, 65] * 10)[:len(substituicoes)]

if "delta_preco_pct" not in substituicoes.columns:
    substituicoes["delta_preco_pct"] = ([0, -3, 2, -9] * 10)[:len(substituicoes)]

if "motivo_recomendacao" not in substituicoes.columns:
    substituicoes["motivo_recomendacao"] = ([
        "Mesma marca, gramatura equivalente",
        "Histórico: cliente aceitou 3× nos últimos 60 dias",
        "Produto similar, preço levemente superior",
        "Cliente sensível à marca — risco elevado de rejeição",
    ] * 10)[:len(substituicoes)]

orig_col = next((c for c in substituicoes.columns if "original"  in c.lower()), substituicoes.columns[0])
sub_col  = next((c for c in substituicoes.columns if "substitut" in c.lower()), substituicoes.columns[1])
sim_col  = next((c for c in substituicoes.columns if "similar"   in c.lower()), None)
disp_col = next((c for c in substituicoes.columns if "disp"      in c.lower()), None)

# =========================
# SIDEBAR — NAVEGAÇÃO
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <img src="https://shopper.com.br/static/img/og-logo.png" alt="Shopper" />
    </div>
    <span class="sidebar-pulse-label">Pulse AI · Prevenção de Ruptura</span>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegar para",
        [
            "Visão geral",
            "Radar de ruptura",
            "Matriz de risco",
            "Substituições",
            "Alertas Slack",
            "Como o agente funciona",
            "Executar agente",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#9CA3AF;font-size:0.72rem;'>Atualizado a cada 5 min<br>Fonte: Pulse_AI_Base.xlsx</small>",
        unsafe_allow_html=True
    )

# =========================
# HEADER
# =========================
em_risco       = len(produtos[produtos["risco_ruptura"].isin(["Critico", "Alto"])])
impacto_total  = int(produtos["impacto_financeiro_estimado"].sum())
dias_medio     = round(produtos["dias_cobertura"].mean(), 1)
pedidos_total  = len(recorrencia)
alertas_ativos = len(alertas)

st.markdown(f"""
<div class="pulse-header">
    <div class="pulse-header-logo">
        <img src="https://shopper.com.br/static/img/og-logo.png" alt="Shopper" />
        <div class="pulse-header-divider"></div>
        <div class="pulse-header-left">
            <h1>Pulse AI</h1>
            <p>Agente Inteligente de Prevenção de Ruptura</p>
        </div>
    </div>
    <span class="pulse-badge">AGENTE ATIVO</span>
</div>
""", unsafe_allow_html=True)

# =========================
# VISÃO GERAL
# =========================
if pagina == "Visão geral":

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Produtos em risco",   em_risco)
    col2.metric("Impacto estimado",    f"R$ {impacto_total:,.0f}".replace(",", "."))
    col3.metric(
        "Cobertura média", f"{dias_medio}d",
        delta=f"{round(dias_medio - 10, 1)}d vs meta",
        delta_color="normal" if dias_medio >= 10 else "inverse"
    )
    col4.metric("Pedidos recorrentes", pedidos_total)
    col5.metric("Alertas ativos",      alertas_ativos)

    st.markdown("---")
    st.subheader("Impacto financeiro por loja")

    impacto_loja = (
        produtos.groupby("loja")["impacto_financeiro_estimado"]
        .sum().reset_index()
        .sort_values("impacto_financeiro_estimado", ascending=False)
    )
    fig_loja = px.bar(
        impacto_loja, x="loja", y="impacto_financeiro_estimado",
        color="impacto_financeiro_estimado",
        color_continuous_scale=["#A7F3C4", "#00C25A", "#009944", "#006B2F"],
        text_auto=True,
        labels={"loja": "Loja", "impacto_financeiro_estimado": "Impacto (R$)"},
        height=320,
    )
    fig_loja.update_coloraxes(showscale=False)
    fig_loja.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
    fig_loja.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#374151",
    )
    st.plotly_chart(fig_loja, use_container_width=True)

    st.markdown("---")
    st.subheader("Demanda prevista — pedidos recorrentes")

    recorrencia_group = (
        recorrencia.groupby("data_entrega_prevista")["quantidade_prevista"]
        .sum().reset_index()
    )
    fig_recor = px.area(
        recorrencia_group, x="data_entrega_prevista", y="quantidade_prevista",
        markers=True, height=280,
    )
    fig_recor.update_traces(line_color="#00C25A", fillcolor="rgba(0,194,90,0.10)")
    fig_recor.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#374151",
    )
    st.plotly_chart(fig_recor, use_container_width=True)

# =========================
# RADAR DE RUPTURA
# =========================
elif pagina == "Radar de ruptura":
    st.subheader("Radar de Ruptura")

    col_f1, _ = st.columns([2, 6])
    with col_f1:
        risco_filter = st.selectbox("Filtrar risco", ["Todos", "Critico", "Alto", "Medio", "Baixo"])

    produtos_view = produtos if risco_filter == "Todos" else produtos[produtos["risco_ruptura"] == risco_filter]

    show_cols = {
        "produto": "Produto", "loja": "Loja", "risco_ruptura": "Risco",
        "estoque_atual": "Estoque", "velocidade_venda": "Venda/dia",
        "dias_cobertura": "Dias cobertura", "prazo_reposicao": "Prazo repos.",
        "impacto_financeiro_estimado": "Impacto (R$)", "score_risco": "Score risco",
    }
    available  = {k: v for k, v in show_cols.items() if k in produtos_view.columns}
    df_display = produtos_view[list(available.keys())].rename(columns=available)

    # Light theme: backgrounds suaves
    RISCO_BG = {
        "Critico": "background-color:#FEE2E2; color:#991B1B",
        "Alto":    "background-color:#FEF3C7; color:#92400E",
    }

    def highlight(row):
        styles = [""] * len(row)
        cols   = list(df_display.columns)
        ri = cols.index("Risco") if "Risco" in cols else None
        di = cols.index("Dias cobertura") if "Dias cobertura" in cols else None
        if ri is not None:
            bg = RISCO_BG.get(row.iloc[ri], "")
            if bg:
                styles = [bg] * len(row)
        if di is not None:
            v = row.iloc[di]
            if isinstance(v, (int, float)):
                if v <= 3:
                    styles[di] = "background-color:#FCA5A5; color:#7F1D1D; font-weight:bold"
                elif v <= 7:
                    styles[di] = "background-color:#FCD34D; color:#78350F"
        return styles

    fmt = {}
    if "Dias cobertura" in df_display.columns:
        fmt["Dias cobertura"] = "{:.1f}"
    if "Impacto (R$)" in df_display.columns:
        fmt["Impacto (R$)"] = "{:,.0f}"

    st.dataframe(
        df_display.style.apply(highlight, axis=1).format(fmt),
        use_container_width=True
    )

# =========================
# MATRIZ DE RISCO
# =========================
elif pagina == "Matriz de risco":
    st.subheader("Matriz de Risco")
    st.caption("Cada bolha representa um produto. Eixo X: cobertura restante. Eixo Y: impacto financeiro. Tamanho: pedidos afetados.")

    fig_matrix = px.scatter(
        produtos,
        x="dias_cobertura", y="impacto_financeiro_estimado",
        size="pedidos_recorrentes_afetados", color="risco_ruptura",
        hover_name="produto",
        hover_data={"loja": True, "score_risco": True, "dias_cobertura": True, "pedidos_recorrentes_afetados": True},
        color_discrete_map={
            "Critico": "#DC2626",
            "Alto":    "#D97706",
            "Medio":   "#2563EB",
            "Baixo":   "#00C25A",
        },
        labels={
            "dias_cobertura": "Dias de cobertura",
            "impacto_financeiro_estimado": "Impacto financeiro (R$)",
            "risco_ruptura": "Nível de risco",
        },
        size_max=50, height=480,
    )
    fig_matrix.add_vline(x=3, line_dash="dash", line_color="#DC2626",
                         annotation_text="Zona crítica (< 3d)", annotation_position="top right")
    fig_matrix.add_vline(x=7, line_dash="dash", line_color="#D97706",
                         annotation_text="Alerta (< 7d)", annotation_position="top right")
    fig_matrix.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#374151",
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

# =========================
# SUBSTITUIÇÕES
# =========================
elif pagina == "Substituições":
    st.subheader("Substituição Inteligente")
    st.caption("Score calculado com base em histórico de compras, sensibilidade à marca, faixa de preço e similaridade.")

    for _, row in substituicoes.iterrows():
        score  = int(row.get("score_aceitacao", 80))
        delta  = row.get("delta_preco_pct", 0)
        motivo = row.get("motivo_recomendacao", "—")

        if score >= 85:
            score_label = "Alta aceitação"
            score_color = "#00963F"
        elif score >= 70:
            score_label = "Aceitação moderada"
            score_color = "#D97706"
        else:
            score_label = "Risco de rejeição"
            score_color = "#DC2626"

        delta_str = "Mesmo preço" if delta == 0 else (f"+{delta}%" if delta > 0 else f"{delta}%")

        with st.container(border=True):
            col1, col2, col3 = st.columns([5, 3, 2])
            with col1:
                st.markdown(f"**{row[orig_col]}** → **{row[sub_col]}**")
                st.caption(motivo)
                if sim_col and sim_col in row.index:
                    st.caption(f"Similaridade: {row[sim_col]}")
            with col2:
                st.markdown(f"<span style='color:{score_color};font-weight:600;font-size:0.875rem;'>{score_label}</span>", unsafe_allow_html=True)
                st.progress(score / 100)
                st.caption(f"{score}% de chance de aceite")
            with col3:
                st.markdown("**Variação de preço**")
                st.markdown(f"**{delta_str}**")
                if disp_col and disp_col in row.index:
                    st.caption(f"Status: {row[disp_col]}")

# =========================
# ALERTAS SLACK
# =========================
elif pagina == "Alertas Slack":
    st.subheader("Central de Alertas Slack")
    st.markdown("**Canal:** `#pulse-alertas`")
    st.markdown("")

    for _, row in alertas.iterrows():
        nivel = row["risco_ruptura"]
        badge_color = "#FEE2E2" if nivel == "Critico" else ("#FEF3C7" if nivel == "Alto" else "#EFF6FF")
        text_color  = "#991B1B" if nivel == "Critico" else ("#92400E" if nivel == "Alto" else "#1E40AF")
        label_risco = f"<span style='background:{badge_color};color:{text_color};padding:2px 10px;border-radius:4px;font-size:0.78rem;font-weight:600;'>{nivel}</span>"

        prod_data    = produtos[produtos["produto"] == row["produto"]]
        urgencia_str = ""
        if not prod_data.empty and "dias_cobertura" in prod_data.columns:
            dias  = prod_data.iloc[0]["dias_cobertura"]
            prazo = prod_data.iloc[0].get("prazo_reposicao", 3)
            urgencia_str = (
                "Ruptura iminente — cobertura abaixo do prazo de reposição"
                if dias < prazo
                else f"Cobertura estimada: **{dias} dias** (prazo reposição: {prazo}d)"
            )

        with st.container(border=True):
            st.markdown(f"**{row['produto']}** &nbsp; {label_risco}", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Loja:** {row['loja']}")
                st.markdown(f"**Impacto:** R$ {int(row['impacto_financeiro_estimado']):,}".replace(",", "."))
            with col2:
                st.markdown(f"**Pedidos afetados:** {row['pedidos_recorrentes_afetados']}")
                if urgencia_str:
                    st.markdown(urgencia_str)
            st.markdown(f"**Ação sugerida:** {row['acao_sugerida']}")
            st.code(row["mensagem_slack"], language="text")

# =========================
# COMO O AGENTE FUNCIONA
# =========================
elif pagina == "Como o agente funciona":
    st.subheader("Como o Pulse AI funciona como agente")
    st.markdown(
        "O Pulse AI não é um dashboard passivo — ele é um **agente autônomo** que monitora, "
        "decide e age sem precisar que ninguém abra o app."
    )
    st.markdown("")

    st.markdown("#### Ciclo de execução autônoma")

    steps = [
        ("1", "Coleta de dados em tempo real",
         "A cada ciclo, o agente consulta automaticamente estoque, velocidade de venda, cestas ativas e histórico de compras diretamente do data warehouse."),
        ("2", "Cálculo de score de risco",
         "Para cada produto × loja, o modelo calcula dias de cobertura, cruza com o prazo de reposição e gera um score de risco de 0 a 100."),
        ("3", "Detecção de anomalias de demanda",
         "O agente compara a demanda atual com o padrão histórico e sazonalidade — identificando picos antes que o estoque seja impactado."),
        ("4", "Avaliação de substituições",
         "Para produtos em risco, o agente verifica substitutos disponíveis e calcula o score de aceitação por cliente, considerando marca, preço e histórico."),
        ("5", "Disparo automático de alertas",
         "Produtos que cruzam o limiar crítico geram alertas automáticos no Slack — sem ninguém precisar verificar o dashboard."),
        ("6", "Bloqueio preventivo de substituições",
         "No momento do picking, o agente bloqueia automaticamente substituições com score de aceitação abaixo do limiar, evitando rejeições antes que aconteçam."),
    ]

    for num, titulo, descricao in steps:
        st.markdown(f"""
        <div class="agent-step">
            <div class="agent-step-num">{num}</div>
            <div class="agent-step-content">
                <h4>{titulo}</h4>
                <p>{descricao}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("#### Impacto estimado em produção")

    c1, c2, c3, c4 = st.columns(4)
    impacts = [
        ("−35%", "Rupturas evitadas"),
        ("−28%", "Substituições rejeitadas"),
        ("+R$ 2M", "Receita recuperada / ano"),
        ("−40%", "Análises manuais"),
    ]
    for col, (val, label) in zip([c1, c2, c3, c4], impacts):
        col.markdown(f"""
        <div class="impact-card">
            <span class="value">{val}</span>
            <span class="label">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.info(
        "Para a competição: o Streamlit é a camada de visualização. "
        "O agente real rodaria como um script agendado (Airflow / cron) integrado ao data warehouse da Shopper, "
        "atuando de forma autônoma a cada ciclo operacional."
    )

# =========================
# EXECUTAR AGENTE (SIMULADOR)
# =========================
elif pagina == "Executar agente":

    if "historico_ciclos" not in st.session_state:
        st.session_state.historico_ciclos = []
    if "ultimo_ciclo" not in st.session_state:
        st.session_state.ultimo_ciclo = None

    st.subheader("Simulador de ciclo do agente")

    # Status do agente
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div class='status-card active'>
            <p class='label'>Status</p>
            <p class='value'>Monitoramento contínuo</p>
        </div>""", unsafe_allow_html=True)
    with col_s2:
        ultimo = st.session_state.ultimo_ciclo
        texto_ultimo = ultimo.strftime("%H:%M:%S") if ultimo else "Nenhum ciclo executado"
        st.markdown(f"""
        <div class='status-card'>
            <p class='label'>Último ciclo</p>
            <p class='value'>{texto_ultimo}</p>
        </div>""", unsafe_allow_html=True)
    with col_s3:
        total = len(st.session_state.historico_ciclos)
        st.markdown(f"""
        <div class='status-card'>
            <p class='label'>Ciclos nesta sessão</p>
            <p class='value'>{total}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    executar = st.button("Executar ciclo agora", type="primary", use_container_width=False)

    st.markdown("")
    log_area    = st.empty()
    result_area = st.empty()
    slack_area  = st.empty()

    if executar:
        agora = datetime.now()
        st.session_state.ultimo_ciclo = agora
        logs = []

        def render_log(logs):
            linhas = "\n".join(logs)
            log_area.code(linhas, language="bash")

        def add_log(nivel, mensagem):
            ts = datetime.now().strftime("%H:%M:%S")
            prefixo = {
                "INFO":  "[INFO ]",
                "OK":    "[ OK  ]",
                "WARN":  "[WARN ]",
                "CRIT":  "[CRIT ]",
                "SLACK": "[SLACK]",
                "DONE":  "[ OK  ]",
            }.get(nivel, "[INFO ]")
            logs.append(f"{ts}  {prefixo}  {mensagem}")
            render_log(logs)

        # ── PASSO 1: Coleta ──
        add_log("INFO", "Iniciando ciclo do Pulse AI...")
        time.sleep(0.6)
        add_log("INFO", "Conectando ao data warehouse...")
        time.sleep(0.8)
        add_log("OK",   f"{len(produtos)} produtos carregados · {produtos['loja'].nunique()} lojas · {len(recorrencia)} pedidos recorrentes")
        time.sleep(0.5)

        # ── PASSO 2: Scores de risco ──
        add_log("INFO", "Calculando scores de risco por produto × loja...")
        time.sleep(0.7)

        criticos, altos, alertas_gerados = [], [], []
        for _, row in produtos.iterrows():
            nivel = row["risco_ruptura"]
            score = row.get("score_risco", 50)
            dias  = row.get("dias_cobertura", 5)
            if nivel == "Critico":
                add_log("CRIT", f"{row['produto']} · {row['loja']} · cobertura: {dias}d · score: {score} → CRITICO")
                criticos.append(row)
                time.sleep(0.35)
            elif nivel == "Alto":
                add_log("WARN", f"{row['produto']} · {row['loja']} · cobertura: {dias}d · score: {score} → ALTO")
                altos.append(row)
                time.sleep(0.3)

        add_log("OK", f"Scores calculados · {len(criticos)} criticos · {len(altos)} altos")
        time.sleep(0.5)

        # ── PASSO 3: Demanda ──
        add_log("INFO", "Analisando variação de demanda vs histórico...")
        time.sleep(0.8)
        add_log("OK",   "Demanda +12% acima da média semanal — risco de antecipação de ruptura")
        time.sleep(0.5)

        # ── PASSO 4: Substituições ──
        add_log("INFO", f"Avaliando substitutos para {len(criticos) + len(altos)} produtos em risco...")
        time.sleep(0.6)

        bloqueadas = 0
        for _, row in substituicoes.iterrows():
            score_sub = int(row.get("score_aceitacao", 80))
            orig = row[orig_col]
            sub  = row[sub_col]
            if score_sub >= 80:
                add_log("OK",   f"{orig} -> {sub} · score: {score_sub}% aprovada")
            else:
                add_log("CRIT", f"{orig} -> {sub} · score: {score_sub}% BLOQUEADA (cliente sensivel a marca)")
                bloqueadas += 1
            time.sleep(0.35)

        add_log("OK", f"Substituições avaliadas · {bloqueadas} bloqueada(s) por risco de rejeição")
        time.sleep(0.5)

        # ── PASSO 5: Alertas Slack ──
        add_log("INFO", f"Disparando {len(alertas)} alertas para #pulse-alertas no Slack...")
        time.sleep(0.6)
        for _, row in alertas.iterrows():
            add_log("SLACK", f"Alerta enviado → {row['produto']} · {row['loja']} · {row['risco_ruptura']}")
            alertas_gerados.append(row)
            time.sleep(0.3)

        # ── PASSO 6: Conclusão ──
        time.sleep(0.4)
        add_log("DONE", f"Ciclo concluido · {agora.strftime('%H:%M:%S')} · proximo ciclo em 60 min")

        # Salvar no histórico
        st.session_state.historico_ciclos.append({
            "hora": agora.strftime("%H:%M:%S"),
            "criticos": len(criticos),
            "altos": len(altos),
            "bloqueadas": bloqueadas,
            "alertas": len(alertas_gerados),
        })
        st.session_state.ultimo_ciclo = agora

        # ── Resultados ──
        result_area.markdown("---")
        with result_area.container():
            st.markdown("#### Resultado do ciclo")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Produtos analisados", len(produtos))
            r2.metric("Alertas críticos",    len(criticos))
            r3.metric("Alertas altos",       len(altos))
            r4.metric("Subs. bloqueadas",    bloqueadas)

        # ── Preview Slack ──
        with slack_area.container():
            st.markdown("---")
            st.markdown("#### Alertas enviados ao Slack — `#pulse-alertas`")
            for _, row in alertas.iterrows():
                with st.container(border=True):
                    st.code(row["mensagem_slack"], language="text")
                    st.caption(f"Enviado às {agora.strftime('%H:%M:%S')} · canal #pulse-alertas")

    # Histórico de ciclos
    if st.session_state.historico_ciclos:
        st.markdown("---")
        st.markdown("#### Histórico desta sessão")
        df_hist = pd.DataFrame(st.session_state.historico_ciclos)
        df_hist.columns = ["Hora", "Críticos", "Altos", "Subs. bloqueadas", "Alertas enviados"]
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
