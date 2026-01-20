def calcular_aliquota_ir(meses):
    if meses <= 6:
        return 0.225 #25%
    elif meses <= 12:
        return 0.2  #20%
    elif meses <= 24:
        return 0.175 #17,5%
    else:
        return 0.15  #15%

def simular_pos_fixado(valor_inicial, aporte_mensal, taxa_anual, meses, isento=False):
    taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
    saldo = valor_inicial
    total_investido = valor_inicial

    evolucao = [round(saldo, 2)]

    for mes in range(meses):
        saldo *= (1 + taxa_mensal)
        saldo += aporte_mensal
        total_investido += aporte_mensal
        evolucao.append(round(saldo,2))

    lucro_bruto = saldo - total_investido
    
    if isento:
        imposto = 0
    else:
        aliquota = calcular_aliquota_ir(meses)
        imposto = lucro_bruto * aliquota

    valor_liquido = saldo - imposto

    return {
        "total_investido": round(total_investido, 2),
        "valor_bruto": round(saldo, 2),
        "valor_liquido": round(valor_liquido, 2),
        "imposto_pago": round(imposto, 2),
        "rendimento_bruto": round(lucro_bruto, 2),
        "rendimento_liquido": round(valor_liquido - total_investido, 2),
        "serie_temporal": evolucao
    }

def simular_poupanca(valor_inicial, aporte_mensal, meses, taxa_selic_atual):
    # Regra da Selic
    if taxa_selic_atual > 0.085:
        taxa_mensal = 0.005 
    else:
        taxa_anual = taxa_selic_atual * 0.7
        taxa_mensal = (1 + taxa_anual) ** (1/12) - 1

    saldo = valor_inicial
    total_investido = valor_inicial

    evolucao = [round(saldo, 2)]

    for mes in range(meses):
        saldo *= (1 + taxa_mensal)
        saldo += aporte_mensal
        total_investido += aporte_mensal
        evolucao.append(round(saldo,2))

    # Poupança é isenta, logo bruto = líquido
    lucro_bruto = saldo - total_investido

    return {
        "total_investido": round(total_investido, 2),
        "valor_bruto": round(saldo, 2),
        "valor_liquido": round(saldo, 2),
        "imposto_pago": 0,
        "rendimento_bruto": round(lucro_bruto, 2),
        "rendimento_liquido": round(lucro_bruto, 2),
        "serie_temporal": evolucao
    }

def simular_tesouro_selic(valor_inicial, aporte_mensal, meses, taxa_selic_anual):
    taxa_mensal = (1 + taxa_selic_anual) ** (1/12) - 1
    taxa_b3_mensal = (1 + 0.002) ** (1/12) - 1 # 0.20% a.a.

    saldo = valor_inicial
    total_investido = valor_inicial

    evolucao = [round(saldo, 2)]

    for _ in range(meses):
        saldo *= (1 + taxa_mensal)
        saldo *= (1 - taxa_b3_mensal)
        saldo += aporte_mensal
        total_investido += aporte_mensal
        evolucao.append(round(saldo,2))

    lucro_bruto = saldo - total_investido
    imposto = lucro_bruto * calcular_aliquota_ir(meses)
    valor_liquido = saldo - imposto

    return {
        "total_investido": round(total_investido, 2),
        "valor_bruto": round(saldo, 2),
        "valor_liquido": round(valor_liquido, 2),
        "imposto_pago": round(imposto, 2),
        "rendimento_bruto": round(lucro_bruto, 2),
        "rendimento_liquido": round(valor_liquido - total_investido, 2),
        "serie_temporal": evolucao
    }

def simular_tesouro_prefixado(valor_inicial, aporte_mensal, meses, taxa_prefixada_anual):
    taxa_mensal = (1 + taxa_prefixada_anual) ** (1/12) - 1
    taxa_b3_mensal = (1 + 0.002) ** (1/12) - 1

    saldo = valor_inicial
    total_investido = valor_inicial

    evolucao = [round(saldo, 2)]

    for _ in range(meses):
        saldo *= (1 + taxa_mensal)
        saldo *= (1 - taxa_b3_mensal)
        saldo += aporte_mensal
        total_investido += aporte_mensal
        evolucao.append(round(saldo,2))

    lucro_bruto = saldo - total_investido
    imposto = lucro_bruto * calcular_aliquota_ir(meses)
    valor_liquido = saldo - imposto

    return {
        "total_investido": round(total_investido, 2),
        "valor_bruto": round(saldo, 2),
        "valor_liquido": round(valor_liquido, 2),
        "imposto_pago": round(imposto, 2),
        "rendimento_bruto": round(lucro_bruto, 2),
        "rendimento_liquido": round(valor_liquido - total_investido, 2),
        "serie_temporal": evolucao

    }

def simular_tesouro_ipca(valor_inicial, aporte_mensal, meses, taxa_ipca_anual, taxa_real_anual):
    # Fórmula correta de juros compostos para taxas híbridas
    taxa_combinada = (1 + taxa_ipca_anual) * (1 + taxa_real_anual) - 1
    taxa_mensal = (1 + taxa_combinada) ** (1/12) - 1
    taxa_b3_mensal = (1 + 0.002) ** (1/12) - 1

    saldo = valor_inicial
    total_investido = valor_inicial

    evolucao = [round(saldo, 2)]

    for _ in range(meses):
        saldo *= (1 + taxa_mensal)
        saldo *= (1 - taxa_b3_mensal)
        saldo += aporte_mensal
        total_investido += aporte_mensal
        evolucao.append(round(saldo,2)) 
        

    lucro_bruto = saldo - total_investido
    imposto = lucro_bruto * calcular_aliquota_ir(meses)
    valor_liquido = saldo - imposto

    return {
        "total_investido": round(total_investido, 2),
        "valor_bruto": round(saldo, 2),
        "valor_liquido": round(valor_liquido, 2),
        "imposto_pago": round(imposto, 2),
        "rendimento_bruto": round(lucro_bruto, 2),
        "rendimento_liquido": round(valor_liquido - total_investido, 2),
        "serie_temporal": evolucao
    }