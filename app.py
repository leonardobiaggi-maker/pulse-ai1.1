import streamlit as st
import pandas as pd
import plotly.express as px

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

produtos = pd.read_excel(excel_file, sheet_name="produtos")
recorrencia = pd.read_excel(excel_file, sheet_name="recorrencia_futura")
substituicoes = pd.read_excel(excel_file, sheet_name="substituicoes")
alertas = pd.read_excel(excel_file, sheet_name="alertas")

# =========================
# HEADER
# =========================

st.title("📦 Pulse AI")
st.subheader("Agente Inteligente de Prevenção de Ruptura")

st.markdown("---")

# =========================
# KPIs
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Produtos em risco",
    len(produtos[produtos["risco_ruptura"].isin(["Critico", "Alto"])])
)

col2.metric(
    "Impacto Financeiro",
    f"R$ {int(produtos['impacto_financeiro_estimado'].sum()):,}".replace(',', '.')
)

col3.metric(
    "Pedidos Recorrentes",
    len(recorrencia)
)

col4.metric(
    "Alertas Ativos",
    len(alertas)
)

st.markdown("---")

# =========================
# RADAR DE RUPTURA
# =========================

st.header("🚨 Radar de Ruptura")

risco_filter = st.selectbox(
    "Filtrar risco",
    ["Todos", "Critico", "Alto", "Medio", "Baixo"]
)

if risco_filter != "Todos":
    produtos_view = produtos[produtos["risco_ruptura"] == risco_filter]
else:
    produtos_view = produtos

st.dataframe(produtos_view, use_container_width=True)

# =========================
# IMPACTO FINANCEIRO
# =========================

st.header("📊 Impacto Financeiro por Loja")

impacto_loja = (
    produtos
    .groupby("loja")["impacto_financeiro_estimado"]
    .sum()
    .reset_index()
)

fig = px.bar(
    impacto_loja,
    x="loja",
    y="impacto_financeiro_estimado",
    title="Impacto Financeiro por Loja"
)

st.plotly_chart(fig, use_container_width=True)

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

fig2 = px.line(
    recorrencia_group,
    x="data_entrega_prevista",
    y="quantidade_prevista",
    title="Demanda Prevista"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# SUBSTITUIÇÕES
# =========================

st.header("🧠 Substituição Inteligente")

st.dataframe(substituicoes, use_container_width=True)

# =========================
# ALERTAS
# =========================



st.header("💬 Central de Alertas Slack")

st.markdown("### Canal: #pulse-alertas")

for _, row in alertas.iterrows():

    with st.container(border=True):

        if row["risco_ruptura"] == "Critico":
            emoji = "🔴"
        elif row["risco_ruptura"] == "Alto":
            emoji = "🟠"
        else:
            emoji = "🟡"

        st.markdown(f"## {emoji} Pulse AI Alert")

        st.markdown(f"**Produto:** {row['produto']}")
        st.markdown(f"**Loja:** {row['loja']}")
        st.markdown(f"**Risco:** {row['risco_ruptura']}")
        st.markdown(
            f"**Impacto Financeiro:** R$ {int(row['impacto_financeiro_estimado']):,}".replace(',', '.')
        )
        st.markdown(f"**Pedidos Impactados:** {row['pedidos_recorrentes_afetados']}")
        st.markdown(f"**Ação Sugerida:** {row['acao_sugerida']}")

        st.code(row["mensagem_slack"], language="text")

        st.markdown("---")
