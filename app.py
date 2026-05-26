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
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Page background ── */
    .stApp { background-color: #F4F6F9 !important; }
    .main .block-container {
        background-color: #F4F6F9;
        padding-top: 1.75rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px;
    }

    /* ── Accent bar topo ── */
    .stApp::before {
        content: '';
        display: block;
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00C25A 0%, #00E56A 60%, #A7F3C4 100%);
        z-index: 9999;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    [data-testid="stSidebar"] * { color: #374151 !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.875rem !important;
        padding: 7px 0 !important;
        color: #374151 !important;
        transition: color 0.15s;
    }

    /* ── Header ── */
    .pulse-header {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.75rem;
        border: 1px solid #E9ECF0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    }
    .pulse-header-logo {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .pulse-header-logo img {
        height: 44px;
        object-fit: contain;
        filter: drop-shadow(0 1px 2px rgba(0,0,0,0.08));
    }
    .pulse-header-divider {
        width: 1px;
        height: 40px;
        background: #E5E7EB;
        flex-shrink: 0;
    }
    .pulse-header-left h1 {
        color: #111827 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .pulse-header-left p {
        color: #9CA3AF !important;
        margin: 5px 0 0 !important;
        font-size: 0.78rem !important;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    .pulse-header-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
    }
    .pulse-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: #ECFDF5;
        color: #065F46;
        border: 1px solid #6EE7B7;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .pulse-badge::before {
        content: '';
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #00C25A;
        display: inline-block;
        box-shadow: 0 0 0 2px rgba(0,194,90,0.25);
        animation: pulse-ring 2s ease infinite;
    }
    @keyframes pulse-ring {
        0%   { box-shadow: 0 0 0 0 rgba(0,194,90,0.4); }
        70%  { box-shadow: 0 0 0 6px rgba(0,194,90,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,194,90,0); }
    }
    .pulse-timestamp {
        font-size: 0.7rem;
        color: #9CA3AF;
        font-weight: 400;
    }

    /* ── KPI cards ── */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 1.25rem 1.4rem !important;
        border: 1px solid #E9ECF0 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
        transition: box-shadow 0.2s;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 12px rgba(0,194,90,0.1) !important;
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.7rem !important;
        color: #9CA3AF !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

    /* ── Section titles ── */
    h2, h3 {
        color: #111827 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    h3 { font-size: 1.05rem !important; }

    /* ── Divider ── */
    hr { border-color: #E9ECF0 !important; margin: 1.75rem 0 !important; }

    /* ── Selectbox label ── */
    .stSelectbox label p {
        font-size: 0.72rem !important;
        color: #9CA3AF !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E9ECF0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* ── Container with border ── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E9ECF0 !important;
        border-radius: 12px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    }

    /* ── Section card (wrapper) ── */
    .section-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E9ECF0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.25rem;
    }
    .section-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .section-label::before {
        content: '';
        width: 3px;
        height: 12px;
        background: #00C25A;
        border-radius: 2px;
        display: inline-block;
    }

    /* ── Agent steps ── */
    .agent-step {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 10px;
        border: 1px solid #E9ECF0;
        border-left: 3px solid #00C25A;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.15s;
    }
    .agent-step:hover { box-shadow: 0 3px 10px rgba(0,194,90,0.09); }
    .agent-step-num {
        background: linear-gradient(135deg, #00C25A, #009944);
        color: #FFFFFF;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 800;
        flex-shrink: 0;
        margin-top: 1px;
        box-shadow: 0 2px 6px rgba(0,194,90,0.3);
    }
    .agent-step-content h4 {
        margin: 0 0 4px 0;
        color: #111827;
        font-size: 0.9rem;
        font-weight: 700;
    }
    .agent-step-content p {
        margin: 0;
        color: #6B7280;
        font-size: 0.825rem;
        line-height: 1.6;
    }

    /* ── Impact cards ── */
    .impact-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF8 100%);
        border-radius: 12px;
        padding: 1.5rem 1.25rem;
        text-align: center;
        border: 1px solid #D1FAE5;
        box-shadow: 0 1px 4px rgba(0,194,90,0.08);
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .impact-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,194,90,0.14);
    }
    .impact-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #00963F;
        display: block;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .impact-card .label {
        font-size: 0.75rem;
        color: #6B7280;
        margin-top: 8px;
        display: block;
        font-weight: 500;
        line-height: 1.4;
    }

    /* ── Status cards ── */
    .status-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        border: 1px solid #E9ECF0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .status-card .label {
        color: #9CA3AF;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }
    .status-card .value {
        color: #111827;
        font-size: 1rem;
        font-weight: 700;
        margin: 5px 0 0;
    }
    .status-card.active {
        background: linear-gradient(135deg, #ECFDF5, #F0FDF8);
        border-color: #6EE7B7;
        box-shadow: 0 2px 8px rgba(0,194,90,0.1);
    }
    .status-card.active .label { color: #059669; }
    .status-card.active .value { color: #065F46; }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        display: flex;
        align-items: center;
        padding: 4px 0 12px;
        border-bottom: 1px solid #F3F4F6;
        margin-bottom: 16px;
    }
    .sidebar-logo img {
        height: 36px;
        object-fit: contain;
    }
    .sidebar-product-tag {
        display: inline-block;
        background: #ECFDF5;
        color: #065F46;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 16px;
        border: 1px solid #A7F3C4;
    }

    /* ── Primary button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00C25A, #009944) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.4rem !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 2px 8px rgba(0,194,90,0.3) !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #00D964, #00C25A) !important;
        box-shadow: 0 4px 14px rgba(0,194,90,0.45) !important;
        transform: translateY(-1px) !important;
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
    <span class="sidebar-product-tag">Pulse AI</span>
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

agora_str = datetime.now().strftime("%d/%m/%Y · %H:%M")
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
    <div class="pulse-header-right">
        <span class="pulse-badge">AGENTE ATIVO</span>
        <span class="pulse-timestamp">Última atualização: {agora_str}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# VISÃO GERAL
# =========================
if pagina == "Visão geral":

    # ── Banner situacional ──
    criticos_count = len(produtos[produtos["risco_ruptura"] == "Critico"])
    if criticos_count > 0:
        st.markdown(f"""
        <div style="background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #DC2626;
                    border-radius:10px;padding:1rem 1.4rem;margin-bottom:1.5rem;
                    display:flex;align-items:center;gap:12px;">
            <div style="font-size:1.4rem;">⚠️</div>
            <div>
                <p style="margin:0;font-weight:700;color:#991B1B;font-size:0.95rem;">
                    {criticos_count} produto(s) em ruptura crítica — ação imediata necessária
                </p>
                <p style="margin:4px 0 0;color:#B91C1C;font-size:0.82rem;">
                    Estoque abaixo do prazo de reposição. Sem intervenção, pedidos recorrentes serão impactados ainda hoje.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#ECFDF5;border:1px solid #A7F3C4;border-left:4px solid #00C25A;
                    border-radius:10px;padding:1rem 1.4rem;margin-bottom:1.5rem;
                    display:flex;align-items:center;gap:12px;">
            <div style="font-size:1.4rem;">✅</div>
            <div>
                <p style="margin:0;font-weight:700;color:#065F46;font-size:0.95rem;">Operação estável</p>
                <p style="margin:4px 0 0;color:#047857;font-size:0.82rem;">
                    Nenhum produto em nível crítico no momento.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPIs ──
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(
        "Produtos em risco", em_risco,
        help="Produtos classificados como Crítico ou Alto risco de ruptura agora"
    )
    col2.metric(
        "Impacto financeiro", f"R$ {impacto_total:,.0f}".replace(",", "."),
        help="Receita estimada em risco caso as rupturas não sejam resolvidas"
    )
    col3.metric(
        "Cobertura média", f"{dias_medio}d",
        delta=f"{round(dias_medio - 10, 1)}d vs meta 10d",
        delta_color="normal" if dias_medio >= 10 else "inverse",
        help="Quantos dias, em média, o estoque atual cobre a demanda. Meta: 10 dias."
    )
    col4.metric(
        "Pedidos recorrentes", pedidos_total,
        help="Entregas recorrentes programadas que podem ser afetadas pelas rupturas"
    )
    col5.metric(
        "Alertas disparados", alertas_ativos,
        help="Alertas enviados automaticamente ao Slack pelo agente neste ciclo"
    )

    # ── Top 3 ações urgentes ──
    st.markdown("---")
    st.subheader("Prioridades agora")
    st.caption("O Pulse AI identificou as seguintes ações ordenadas por impacto financeiro.")

    top_alertas = alertas.nlargest(3, "impacto_financeiro_estimado")
    for i, (_, row) in enumerate(top_alertas.iterrows(), 1):
        nivel = row["risco_ruptura"]
        cor_borda = "#DC2626" if nivel == "Critico" else "#D97706"
        cor_bg    = "#FEF2F2" if nivel == "Critico" else "#FFFBEB"
        cor_texto = "#991B1B" if nivel == "Critico" else "#92400E"
        st.markdown(f"""
        <div style="background:{cor_bg};border:1px solid;border-color:{cor_borda}33;
                    border-left:4px solid {cor_borda};border-radius:10px;
                    padding:0.9rem 1.2rem;margin-bottom:8px;display:flex;align-items:flex-start;gap:14px;">
            <div style="font-size:1.1rem;font-weight:800;color:{cor_borda};min-width:22px;">
                {i}
            </div>
            <div style="flex:1;">
                <p style="margin:0;font-weight:700;color:#111827;font-size:0.9rem;">
                    {row['produto']} <span style="font-weight:400;color:#6B7280;">· {row['loja']}</span>
                </p>
                <p style="margin:4px 0 0;color:#374151;font-size:0.82rem;">{row['acao_sugerida']}</p>
            </div>
            <div style="text-align:right;flex-shrink:0;">
                <p style="margin:0;font-weight:700;color:{cor_texto};font-size:0.95rem;">
                    R$ {int(row['impacto_financeiro_estimado']):,}
                </p>
                <p style="margin:2px 0 0;color:#9CA3AF;font-size:0.72rem;">impacto estimado</p>
            </div>
        </div>
        """.replace(",", "."), unsafe_allow_html=True)

    # ── Charts ──
    st.markdown("---")
    col_c1, col_c2 = st.columns([3, 2])

    with col_c1:
        st.subheader("Impacto por loja")
        st.caption("Receita em risco acumulada por filial. Lojas com maior barra exigem atenção prioritária.")
        impacto_loja = (
            produtos.groupby("loja")["impacto_financeiro_estimado"]
            .sum().reset_index()
            .sort_values("impacto_financeiro_estimado", ascending=False)
        )
        fig_loja = px.bar(
            impacto_loja, x="loja", y="impacto_financeiro_estimado",
            color="impacto_financeiro_estimado",
            color_continuous_scale=["#A7F3C4", "#00C25A", "#009944", "#065F46"],
            text_auto=True,
            labels={"loja": "Loja", "impacto_financeiro_estimado": "Impacto (R$)"},
            height=320,
        )
        fig_loja.update_coloraxes(showscale=False)
        fig_loja.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
        fig_loja.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#374151", margin=dict(t=20, b=10),
        )
        st.plotly_chart(fig_loja, use_container_width=True)

    with col_c2:
        st.subheader("Distribuição por risco")
        st.caption("Proporção de produtos por nível de alerta.")
        dist_risco = produtos["risco_ruptura"].value_counts().reset_index()
        dist_risco.columns = ["Risco", "Qtd"]
        fig_pie = px.pie(
            dist_risco, names="Risco", values="Qtd",
            color="Risco",
            color_discrete_map={
                "Critico": "#DC2626", "Alto": "#D97706",
                "Medio": "#2563EB", "Baixo": "#00C25A"
            },
            height=320,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#374151", showlegend=False, margin=dict(t=20, b=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Demanda prevista — próximos 10 dias")
    st.caption(
        "Volume de pedidos recorrentes esperado. Picos de demanda com estoque baixo = risco elevado. "
        "O agente usa essa projeção para antecipar alertas antes que a ruptura aconteça."
    )
    recorrencia_group = (
        recorrencia.groupby("data_entrega_prevista")["quantidade_prevista"]
        .sum().reset_index()
    )
    fig_recor = px.area(
        recorrencia_group, x="data_entrega_prevista", y="quantidade_prevista",
        markers=True, height=260,
        labels={"data_entrega_prevista": "Data", "quantidade_prevista": "Pedidos previstos"},
    )
    fig_recor.update_traces(line_color="#00C25A", fillcolor="rgba(0,194,90,0.10)")
    fig_recor.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#374151", margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_recor, use_container_width=True)

# =========================
# RADAR DE RUPTURA
# =========================
elif pagina == "Radar de ruptura":
    st.subheader("Radar de Ruptura")

    # ── O que é esse radar ──
    st.markdown("""
    <div style="background:#F8FAFC;border:1px solid #E9ECF0;border-radius:10px;
                padding:1rem 1.4rem;margin-bottom:1.25rem;">
        <p style="margin:0;font-weight:600;color:#111827;font-size:0.875rem;">
            O que este radar monitora
        </p>
        <p style="margin:6px 0 0;color:#6B7280;font-size:0.82rem;line-height:1.6;">
            Para cada produto e loja, o agente calcula quantos dias o estoque atual consegue
            atender a demanda (<strong>Dias de cobertura</strong>) e compara com o tempo
            necessário para repor (<strong>Prazo de reposição</strong>).
            Quando a cobertura é menor que o prazo, a ruptura já está acontecendo.
            O <strong>Score de risco</strong> combina esses fatores em um número de 0 a 100.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Legenda de risco ──
    st.markdown("""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:1rem;">
        <span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:5px;
                     font-size:0.75rem;font-weight:600;border:1px solid #FECACA;">
            Crítico — Cobertura &lt; Prazo de reposição. Ruptura iminente.
        </span>
        <span style="background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:5px;
                     font-size:0.75rem;font-weight:600;border:1px solid #FDE68A;">
            Alto — Cobertura abaixo de 7 dias. Monitoramento intenso.
        </span>
        <span style="background:#DBEAFE;color:#1E40AF;padding:3px 10px;border-radius:5px;
                     font-size:0.75rem;font-weight:600;border:1px solid #BFDBFE;">
            Médio — Estoque adequado, mas em tendência de queda.
        </span>
        <span style="background:#DCFCE7;color:#166534;padding:3px 10px;border-radius:5px;
                     font-size:0.75rem;font-weight:600;border:1px solid #BBF7D0;">
            Baixo — Cobertura confortável.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Filtro + resumo ──
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        risco_filter = st.selectbox("Filtrar por nível", ["Todos", "Critico", "Alto", "Medio", "Baixo"])

    produtos_view = produtos if risco_filter == "Todos" else produtos[produtos["risco_ruptura"] == risco_filter]

    total_view = len(produtos_view)
    impacto_view = int(produtos_view["impacto_financeiro_estimado"].sum())
    col_f2.metric("Produtos exibidos", total_view)
    col_f3.metric("Impacto filtrado", f"R$ {impacto_view:,.0f}".replace(",", "."))
    col_f4.metric("Score médio", int(produtos_view["score_risco"].mean()) if "score_risco" in produtos_view.columns else "—")

    # ── Tabela enriquecida ──
    produtos_view = produtos_view.copy()
    if "dias_cobertura" in produtos_view.columns and "prazo_reposicao" in produtos_view.columns:
        produtos_view["status_cobertura"] = produtos_view.apply(
            lambda r: "Ruptura ativa" if r["dias_cobertura"] < r["prazo_reposicao"] else "OK", axis=1
        )

    show_cols = {
        "produto": "Produto", "loja": "Loja", "risco_ruptura": "Risco",
        "estoque_atual": "Estoque atual", "velocidade_venda": "Venda/dia",
        "dias_cobertura": "Dias cobertura", "prazo_reposicao": "Prazo repos. (dias)",
        "status_cobertura": "Status",
        "impacto_financeiro_estimado": "Impacto (R$)", "score_risco": "Score (0–100)",
    }
    available  = {k: v for k, v in show_cols.items() if k in produtos_view.columns}
    df_display = produtos_view[list(available.keys())].rename(columns=available)

    RISCO_BG = {
        "Critico": "background-color:#FEE2E2; color:#991B1B",
        "Alto":    "background-color:#FEF3C7; color:#92400E",
    }

    def highlight(row):
        styles = [""] * len(row)
        cols   = list(df_display.columns)
        ri = cols.index("Risco") if "Risco" in cols else None
        di = cols.index("Dias cobertura") if "Dias cobertura" in cols else None
        si = cols.index("Status") if "Status" in cols else None
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
        if si is not None and row.iloc[si] == "Ruptura ativa":
            styles[si] = "background-color:#DC2626; color:#FFFFFF; font-weight:bold"
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

    st.caption(
        "Dias cobertura = Estoque atual ÷ Venda média por dia. "
        "Quando Dias cobertura < Prazo de reposição, o produto entra em ruptura antes da reposição chegar."
    )

# =========================
# MATRIZ DE RISCO
# =========================
elif pagina == "Matriz de risco":
    st.subheader("Matriz de Risco")

    # ── Como ler ──
    st.markdown("""
    <div style="background:#F8FAFC;border:1px solid #E9ECF0;border-radius:10px;
                padding:1rem 1.4rem;margin-bottom:1.25rem;">
        <p style="margin:0;font-weight:600;color:#111827;font-size:0.875rem;">Como ler esta matriz</p>
        <p style="margin:6px 0 0;color:#6B7280;font-size:0.82rem;line-height:1.65;">
            Cada bolha é um produto. Quanto mais à <strong>esquerda</strong>, menos dias de estoque restam
            — mais urgente. Quanto mais <strong>acima</strong>, maior o impacto financeiro se faltar.
            O <strong>tamanho</strong> da bolha representa quantos pedidos recorrentes de clientes serão afetados.
            <br>Os produtos no quadrante <strong>superior esquerdo</strong> (poucos dias + alto impacto)
            são a prioridade máxima de intervenção.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Quadrantes de ação ──
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.markdown("""
        <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;padding:0.9rem 1rem;">
            <p style="margin:0;font-weight:700;color:#DC2626;font-size:0.8rem;">
                Zona crítica &lt; 3 dias
            </p>
            <p style="margin:5px 0 0;color:#991B1B;font-size:0.78rem;line-height:1.5;">
                Acionar fornecedor emergencial ou ativar substituição automática imediatamente.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_q2:
        st.markdown("""
        <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:0.9rem 1rem;">
            <p style="margin:0;font-weight:700;color:#D97706;font-size:0.8rem;">
                Zona de alerta 3–7 dias
            </p>
            <p style="margin:5px 0 0;color:#92400E;font-size:0.78rem;line-height:1.5;">
                Criar pedido de reposição com prioridade alta. Monitorar demanda diariamente.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_q3:
        st.markdown("""
        <div style="background:#ECFDF5;border:1px solid #A7F3C4;border-radius:8px;padding:0.9rem 1rem;">
            <p style="margin:0;font-weight:700;color:#059669;font-size:0.8rem;">
                Zona segura &gt; 7 dias
            </p>
            <p style="margin:5px 0 0;color:#065F46;font-size:0.78rem;line-height:1.5;">
                Cobertura adequada. Reposição no ciclo normal. Sem ação urgente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Gráfico ──
    fig_matrix = px.scatter(
        produtos,
        x="dias_cobertura", y="impacto_financeiro_estimado",
        size="pedidos_recorrentes_afetados", color="risco_ruptura",
        hover_name="produto",
        hover_data={
            "loja": True, "score_risco": True,
            "dias_cobertura": ":.1f", "pedidos_recorrentes_afetados": True,
            "impacto_financeiro_estimado": ":,.0f",
        },
        color_discrete_map={
            "Critico": "#DC2626", "Alto": "#D97706",
            "Medio": "#2563EB", "Baixo": "#00C25A",
        },
        labels={
            "dias_cobertura": "Dias de cobertura restantes",
            "impacto_financeiro_estimado": "Impacto financeiro (R$)",
            "risco_ruptura": "Nível de risco",
            "pedidos_recorrentes_afetados": "Pedidos afetados",
        },
        size_max=55, height=460,
    )
    fig_matrix.add_vline(
        x=3, line_dash="dash", line_color="#DC2626", line_width=1.5,
        annotation_text="Ruptura iminente", annotation_position="top right",
        annotation_font_color="#DC2626", annotation_font_size=11,
    )
    fig_matrix.add_vline(
        x=7, line_dash="dash", line_color="#D97706", line_width=1.5,
        annotation_text="Zona de alerta", annotation_position="top right",
        annotation_font_color="#D97706", annotation_font_size=11,
    )
    fig_matrix.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#374151",
        legend=dict(
            title="Nível de risco",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E5E7EB",
            borderwidth=1,
        ),
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

    # ── Tabela de prioridade ──
    st.markdown("---")
    st.subheader("Ranking de prioridade de intervenção")
    st.caption("Ordenado por score de risco decrescente. Foque nos primeiros itens da lista.")
    cols_rank = [c for c in ["produto", "loja", "risco_ruptura", "dias_cobertura",
                               "prazo_reposicao", "impacto_financeiro_estimado",
                               "pedidos_recorrentes_afetados", "score_risco"] if c in produtos.columns]
    df_rank = (
        produtos[cols_rank]
        .sort_values("score_risco", ascending=False)
        .rename(columns={
            "produto": "Produto", "loja": "Loja", "risco_ruptura": "Risco",
            "dias_cobertura": "Cobertura (d)", "prazo_reposicao": "Prazo repos.",
            "impacto_financeiro_estimado": "Impacto (R$)",
            "pedidos_recorrentes_afetados": "Pedidos afetados", "score_risco": "Score",
        })
    )
    fmt_rank = {}
    if "Cobertura (d)" in df_rank.columns: fmt_rank["Cobertura (d)"] = "{:.1f}"
    if "Impacto (R$)" in df_rank.columns:  fmt_rank["Impacto (R$)"] = "{:,.0f}"
    st.dataframe(df_rank.style.format(fmt_rank), use_container_width=True, hide_index=True)

# =========================
# SUBSTITUIÇÕES
# =========================
elif pagina == "Substituições":
    st.subheader("Substituição Inteligente")

    # ── Contexto ──
    st.markdown("""
    <div style="background:#F8FAFC;border:1px solid #E9ECF0;border-radius:10px;
                padding:1rem 1.4rem;margin-bottom:1.25rem;">
        <p style="margin:0;font-weight:600;color:#111827;font-size:0.875rem;">
            Por que isso importa
        </p>
        <p style="margin:6px 0 0;color:#6B7280;font-size:0.82rem;line-height:1.65;">
            Quando um produto entra em ruptura, a operação precisa de um substituto.
            Mas trocar um produto sem considerar o perfil do cliente gera <strong>rejeição na entrega</strong>
            — o cliente recusa, o produto volta, e o custo operacional sobe.
            O Pulse AI calcula um <strong>Score de Aceitação</strong> para cada substituição possível,
            cruzando histórico de compras, sensibilidade à marca e variação de preço.
            Substituições abaixo de 70% são <strong>bloqueadas automaticamente</strong> no picking.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Legenda do score ──
    st.markdown("""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:1.25rem;">
        <span style="background:#ECFDF5;color:#065F46;padding:4px 12px;border-radius:6px;
                     font-size:0.75rem;font-weight:600;border:1px solid #6EE7B7;">
            85–100% — Alta aceitação. Substituição aprovada automaticamente.
        </span>
        <span style="background:#FFFBEB;color:#92400E;padding:4px 12px;border-radius:6px;
                     font-size:0.75rem;font-weight:600;border:1px solid #FDE68A;">
            70–84% — Aceitação moderada. Aprovada com aviso ao cliente.
        </span>
        <span style="background:#FEF2F2;color:#991B1B;padding:4px 12px;border-radius:6px;
                     font-size:0.75rem;font-weight:600;border:1px solid #FECACA;">
            &lt;70% — Risco de rejeição. Bloqueada. Requer ação manual.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Cards de substituição ──
    for _, row in substituicoes.iterrows():
        score  = int(row.get("score_aceitacao", 80))
        delta  = row.get("delta_preco_pct", 0)
        motivo = row.get("motivo_recomendacao", "—")

        if score >= 85:
            score_label = "Alta aceitação"
            score_color = "#065F46"
            score_bg    = "#ECFDF5"
            score_border= "#6EE7B7"
            decisao     = "Aprovada automaticamente"
            decisao_cor = "#059669"
        elif score >= 70:
            score_label = "Aceitação moderada"
            score_color = "#92400E"
            score_bg    = "#FFFBEB"
            score_border= "#FDE68A"
            decisao     = "Aprovada com aviso"
            decisao_cor = "#D97706"
        else:
            score_label = "Risco de rejeição"
            score_color = "#991B1B"
            score_bg    = "#FEF2F2"
            score_border= "#FECACA"
            decisao     = "Bloqueada — ação manual"
            decisao_cor = "#DC2626"

        delta_str  = "Mesmo preço" if delta == 0 else (f"+{delta}% mais caro" if delta > 0 else f"{abs(delta)}% mais barato")
        delta_cor  = "#6B7280" if delta == 0 else ("#DC2626" if delta > 0 else "#059669")
        sim_val    = row.get(sim_col, "—") if sim_col else "—"
        disp_val   = row.get(disp_col, "—") if disp_col else "—"

        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 3, 2])
            with col1:
                st.markdown(f"""
                <p style="margin:0;font-weight:700;color:#111827;font-size:0.95rem;">
                    {row[orig_col]}
                </p>
                <p style="margin:3px 0 6px;color:#9CA3AF;font-size:0.8rem;">→ substituto sugerido</p>
                <p style="margin:0;font-weight:600;color:#00963F;font-size:0.9rem;">{row[sub_col]}</p>
                <p style="margin:8px 0 0;color:#6B7280;font-size:0.8rem;line-height:1.5;">
                    {motivo}
                </p>
                """, unsafe_allow_html=True)
                if sim_col:
                    st.caption(f"Similaridade de produto: {sim_val} · Disponibilidade: {disp_val}")

            with col2:
                st.markdown(f"""
                <div style="background:{score_bg};border:1px solid {score_border};
                            border-radius:8px;padding:0.9rem 1rem;text-align:center;">
                    <p style="margin:0;font-size:1.8rem;font-weight:800;color:{score_color};
                               letter-spacing:-0.02em;">{score}%</p>
                    <p style="margin:3px 0 0;font-size:0.75rem;font-weight:600;color:{score_color};">
                        {score_label}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(score / 100)

            with col3:
                st.markdown(f"""
                <p style="margin:0;font-size:0.7rem;font-weight:600;color:#9CA3AF;
                           text-transform:uppercase;letter-spacing:0.06em;">Decisão do agente</p>
                <p style="margin:5px 0 8px;font-weight:700;color:{decisao_cor};font-size:0.85rem;">
                    {decisao}
                </p>
                <p style="margin:0;font-size:0.7rem;font-weight:600;color:#9CA3AF;
                           text-transform:uppercase;letter-spacing:0.06em;">Variação de preço</p>
                <p style="margin:5px 0 0;font-weight:600;color:{delta_cor};font-size:0.85rem;">
                    {delta_str}
                </p>
                """, unsafe_allow_html=True)

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
