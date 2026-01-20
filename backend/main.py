# import das funções
from services.simulador import (
    simular_pos_fixado,
    simular_poupanca,
    simular_tesouro_selic,
    simular_tesouro_prefixado,
    simular_tesouro_ipca
)
# import das taxas
from config.taxas import SELIC_ATUAL, CDI_ATUAL, IPCA_ATUAL

valor = 1000
aporte = 200
prazo = 10

print("--- FINTRACK: COMPARADOR DE INVESTIMENTOS ---")

# Testando CDB
res_cdb = simular_pos_fixado(valor, aporte, CDI_ATUAL, prazo)
print(f"CDB: R$ {res_cdb['valor_liquido']} | Série: {res_cdb['serie_temporal']}")

# Testando Poupança
res_poup = simular_poupanca(valor, aporte, prazo, SELIC_ATUAL)
print(f"Poupança: R$ {res_poup['valor_liquido']} | Série: {res_poup['serie_temporal']}")

# Testando Tesouro IPCA
res_ipca = simular_tesouro_ipca(valor, aporte, prazo, IPCA_ATUAL, 0.06)
print(f"Tesouro IPCA+: R$ {res_ipca['valor_liquido']} | Série: {res_ipca['serie_temporal']}")