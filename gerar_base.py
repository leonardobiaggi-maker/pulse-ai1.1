"""
gerar_base.py
Gera o arquivo Pulse_AI_Base.xlsx com estrutura completa e dados de exemplo.
Execute: python gerar_base.py
"""
import pandas as pd
from datetime import datetime, timedelta

# =========================
# PRODUTOS
# =========================
produtos = pd.DataFrame([
    {
        "produto": "Leite Integral Itambé 1L",
        "loja": "SP-01",
        "risco_ruptura": "Critico",
        "estoque_atual": 12,
        "velocidade_venda": 45,
        "prazo_reposicao": 3,
        "dias_cobertura": round(12 / 45, 1),
        "score_risco": 92,
        "impacto_financeiro_estimado": 14200,
        "pedidos_recorrentes_afetados": 87,
        "criticidade": "Alta",
    },
    {
        "produto": "Frango Inteiro Sadia",
        "loja": "SP-02",
        "risco_ruptura": "Critico",
        "estoque_atual": 8,
        "velocidade_venda": 30,
        "prazo_reposicao": 5,
        "dias_cobertura": round(8 / 30, 1),
        "score_risco": 89,
        "impacto_financeiro_estimado": 12000,
        "pedidos_recorrentes_afetados": 64,
        "criticidade": "Alta",
    },
    {
        "produto": "Arroz Tio João 5kg",
        "loja": "SP-01",
        "risco_ruptura": "Alto",
        "estoque_atual": 69,
        "velocidade_venda": 23,
        "prazo_reposicao": 3,
        "dias_cobertura": round(69 / 23, 1),
        "score_risco": 71,
        "impacto_financeiro_estimado": 8500,
        "pedidos_recorrentes_afetados": 52,
        "criticidade": "Alta",
    },
    {
        "produto": "Feijão Carioca Kicaldo 1kg",
        "loja": "RJ-01",
        "risco_ruptura": "Alto",
        "estoque_atual": 124,
        "velocidade_venda": 22,
        "prazo_reposicao": 4,
        "dias_cobertura": round(124 / 22, 1),
        "score_risco": 66,
        "impacto_financeiro_estimado": 6200,
        "pedidos_recorrentes_afetados": 43,
        "criticidade": "Alta",
    },
    {
        "produto": "Queijo Mussarela Polenghi",
        "loja": "SP-03",
        "risco_ruptura": "Alto",
        "estoque_atual": 57,
        "velocidade_venda": 18,
        "prazo_reposicao": 2,
        "dias_cobertura": round(57 / 18, 1),
        "score_risco": 63,
        "impacto_financeiro_estimado": 5800,
        "pedidos_recorrentes_afetados": 38,
        "criticidade": "Media",
    },
    {
        "produto": "Pão de Forma Wickbold",
        "loja": "SP-02",
        "risco_ruptura": "Medio",
        "estoque_atual": 135,
        "velocidade_venda": 15,
        "prazo_reposicao": 3,
        "dias_cobertura": round(135 / 15, 1),
        "score_risco": 44,
        "impacto_financeiro_estimado": 3500,
        "pedidos_recorrentes_afetados": 29,
        "criticidade": "Media",
    },
    {
        "produto": "Iogurte Grego Danio",
        "loja": "RJ-02",
        "risco_ruptura": "Medio",
        "estoque_atual": 201,
        "velocidade_venda": 12,
        "prazo_reposicao": 4,
        "dias_cobertura": round(201 / 12, 1),
        "score_risco": 38,
        "impacto_financeiro_estimado": 2800,
        "pedidos_recorrentes_afetados": 18,
        "criticidade": "Baixa",
    },
    {
        "produto": "Manteiga Aviação 200g",
        "loja": "SP-03",
        "risco_ruptura": "Baixo",
        "estoque_atual": 440,
        "velocidade_venda": 7,
        "prazo_reposicao": 5,
        "dias_cobertura": round(440 / 7, 1),
        "score_risco": 18,
        "impacto_financeiro_estimado": 1200,
        "pedidos_recorrentes_afetados": 11,
        "criticidade": "Baixa",
    },
])

# =========================
# RECORRÊNCIA FUTURA
# =========================
base_date = datetime.today()
recorrencia = pd.DataFrame([
    {"data_entrega_prevista": base_date + timedelta(days=i), "quantidade_prevista": qty}
    for i, qty in enumerate([210, 198, 234, 267, 289, 312, 298, 321, 308, 345])
])

# =========================
# SUBSTITUIÇÕES
# =========================
substituicoes = pd.DataFrame([
    {
        "produto_original": "Leite Integral Itambé 1L",
        "substituto_sugerido": "Leite Integral Tirol 1L",
        "similaridade": "97%",
        "disponibilidade": "Disponível",
        "score_aceitacao": 94,
        "delta_preco_pct": 0,
        "motivo_recomendacao": "Mesma categoria, gramatura equivalente, preço idêntico",
    },
    {
        "produto_original": "Frango Inteiro Sadia",
        "substituto_sugerido": "Frango Inteiro Aurora",
        "similaridade": "94%",
        "disponibilidade": "Disponível",
        "score_aceitacao": 87,
        "delta_preco_pct": -3,
        "motivo_recomendacao": "Histórico: cliente aceitou marca Aurora 3× nos últimos 60 dias",
    },
    {
        "produto_original": "Arroz Tio João 5kg",
        "substituto_sugerido": "Arroz Camil 5kg",
        "similaridade": "96%",
        "disponibilidade": "Disponível",
        "score_aceitacao": 91,
        "delta_preco_pct": 2,
        "motivo_recomendacao": "Produto similar, leve acréscimo de preço, alta similaridade",
    },
    {
        "produto_original": "Feijão Carioca Kicaldo 1kg",
        "substituto_sugerido": "Feijão Carioca Camil 1kg",
        "similaridade": "93%",
        "disponibilidade": "Limitado",
        "score_aceitacao": 65,
        "delta_preco_pct": -9,
        "motivo_recomendacao": "⚠️ Cliente sensível à marca — risco elevado de rejeição",
    },
])

# =========================
# ALERTAS
# =========================
alertas = pd.DataFrame([
    {
        "produto": "Leite Integral Itambé 1L",
        "loja": "SP-01",
        "risco_ruptura": "Critico",
        "impacto_financeiro_estimado": 14200,
        "pedidos_recorrentes_afetados": 87,
        "acao_sugerida": "Acionar fornecedor emergencial + ativar substituição automática por Tirol",
        "mensagem_slack": (
            "*🔴 PULSE AI ALERT — CRÍTICO*\n"
            "• Produto: Leite Integral Itambé 1L | Loja: SP-01\n"
            "• Cobertura: 0.3 dias | Prazo reposição: 3 dias\n"
            "• Impacto estimado: R$ 14.200 | Pedidos afetados: 87\n"
            "• Ação: Acionar fornecedor emergencial + ativar substituição por Tirol\n"
            "• Score substituto: 94% aceitação"
        ),
    },
    {
        "produto": "Frango Inteiro Sadia",
        "loja": "SP-02",
        "risco_ruptura": "Critico",
        "impacto_financeiro_estimado": 12000,
        "pedidos_recorrentes_afetados": 64,
        "acao_sugerida": "Redistribuir estoque das lojas SP-03 e RJ-01 + ativar substituto Aurora",
        "mensagem_slack": (
            "*🔴 PULSE AI ALERT — CRÍTICO*\n"
            "• Produto: Frango Inteiro Sadia | Loja: SP-02\n"
            "• Cobertura: 0.3 dias | Prazo reposição: 5 dias\n"
            "• Impacto estimado: R$ 12.000 | Pedidos afetados: 64\n"
            "• Ação: Redistribuir estoque de SP-03/RJ-01 + ativar substituto Aurora\n"
            "• Score substituto: 87% aceitação"
        ),
    },
    {
        "produto": "Arroz Tio João 5kg",
        "loja": "SP-01",
        "risco_ruptura": "Alto",
        "impacto_financeiro_estimado": 8500,
        "pedidos_recorrentes_afetados": 52,
        "acao_sugerida": "Criar pedido de reposição com prioridade alta — cobertura de 3 dias",
        "mensagem_slack": (
            "*🟠 PULSE AI ALERT — ALTO*\n"
            "• Produto: Arroz Tio João 5kg | Loja: SP-01\n"
            "• Cobertura: 3.0 dias | Prazo reposição: 3 dias\n"
            "• Impacto estimado: R$ 8.500 | Pedidos afetados: 52\n"
            "• Ação: Criar pedido de reposição com prioridade alta\n"
            "• Score substituto: 91% aceitação (Camil)"
        ),
    },
    {
        "produto": "Feijão Carioca Kicaldo 1kg",
        "loja": "RJ-01",
        "risco_ruptura": "Alto",
        "impacto_financeiro_estimado": 6200,
        "pedidos_recorrentes_afetados": 43,
        "acao_sugerida": "Notificar gestor de loja + avaliar substituto com cautela (cliente sensível à marca)",
        "mensagem_slack": (
            "*🟠 PULSE AI ALERT — ALTO*\n"
            "• Produto: Feijão Carioca Kicaldo 1kg | Loja: RJ-01\n"
            "• Cobertura: 5.6 dias | Prazo reposição: 4 dias\n"
            "• Impacto estimado: R$ 6.200 | Pedidos afetados: 43\n"
            "• Ação: Notificar gestor — cliente sensível à marca, cautela com substituto\n"
            "• ⚠️ Score substituto: 65% aceitação (risco de rejeição)"
        ),
    },
])

# =========================
# SALVAR EXCEL
# =========================
with pd.ExcelWriter("Pulse_AI_Base.xlsx", engine="openpyxl") as writer:
    produtos.to_excel(writer, sheet_name="produtos", index=False)
    recorrencia.to_excel(writer, sheet_name="recorrencia_futura", index=False)
    substituicoes.to_excel(writer, sheet_name="substituicoes", index=False)
    alertas.to_excel(writer, sheet_name="alertas", index=False)

print("✅ Pulse_AI_Base.xlsx gerado com sucesso!")
print(f"   → {len(produtos)} produtos | {len(substituicoes)} substituições | {len(alertas)} alertas")
