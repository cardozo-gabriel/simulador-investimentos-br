from flask import Flask, request, jsonify
from flask_cors import CORS
from services.simulador import (
    simular_pos_fixado, 
    simular_poupanca, 
    simular_tesouro_selic,
    simular_tesouro_prefixado,
    simular_tesouro_ipca
)
from config.taxas import CDI_ATUAL, SELIC_ATUAL, IPCA_ATUAL

app = Flask(__name__)
CORS(app) 

@app.route('/simular', methods=['POST'])
def simular():
    try:
        dados = request.json
        
        # 1. Pegar dados básicos (Garantindo nomes consistentes)
        valor_ini = float(dados.get('valor_inicial', 1000))
        aporte = float(dados.get('aporte_mensal', 0))
        prazo = int(dados.get('prazo', 12))

        # 2. Pegar as taxas customizadas enviadas pelo JS
        # Usamos o valor dividido por 100 para transformar % em decimal
        perc_cdb = float(dados.get('taxa_cdi_cdb', 100)) / 100
        perc_lci = float(dados.get('taxa_cdi_lci', 90)) / 100
        taxa_pre = float(dados.get('taxa_pre_user', 12)) / 100

        # 3. Executar os cálculos usando as variáveis corretas
        res_cdb = simular_pos_fixado(valor_ini, aporte, CDI_ATUAL * perc_cdb, prazo)
        res_lci = simular_pos_fixado(valor_ini, aporte, CDI_ATUAL * perc_lci, prazo, isento=True)
        res_pre = simular_tesouro_prefixado(valor_ini, aporte, prazo, taxa_pre)
        res_poup = simular_poupanca(valor_ini, aporte, prazo, SELIC_ATUAL)
        
        # IPCA usa a constante do sistema (IPCA_ATUAL) + taxa real de 6%
        res_ipca = simular_tesouro_ipca(valor_ini, aporte, prazo, IPCA_ATUAL, 0.06)

        return jsonify({
            "cdb": res_cdb,
            "lci": res_lci,
            "poupanca": res_poup,
            "tesouro_prefixado": res_pre,
            "tesouro_ipca": res_ipca
        })

    except Exception as e:
        print(f"Erro no servidor: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)