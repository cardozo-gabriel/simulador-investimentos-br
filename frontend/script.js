// 1. Variáveis globais para controlar as instâncias dos gráficos (Evita sobreposição)
let graficoPizza = null;
let graficoBarras = null;
let graficoLinha = null;

// 2. Evento Único do Botão Simular
document.getElementById('btn-simular').addEventListener('click', async function() {
    
    // Captura os valores dos campos
    const dadosParaEnviar = {
        valor_inicial: document.getElementById('valor_inicial').value,
        aporte_mensal: document.getElementById('aporte_mensal').value,
        prazo: document.getElementById('prazo').value,
        taxa_cdi_cdb: document.getElementById('taxa_cdi_cdb').value,
        taxa_cdi_lci: document.getElementById('taxa_cdi_lci').value,
        taxa_pre_user: document.getElementById('taxa_pre_user').value
    };

    try {
        const resposta = await fetch('http://127.0.0.1:5000/simular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosParaEnviar)
        });

        if (!resposta.ok) throw new Error('Falha na comunicação com o Flask');

        const resultados = await resposta.json();

        // EXECUÇÃO EM ORDEM
        exibirResultados(resultados);      // Primeiro os Cards
        desenharTodosGraficos(resultados); // Depois os Gráficos

    } catch (erro) {
        console.error("Erro no processo:", erro);
        alert("O servidor Flask não respondeu. Verifique se o terminal do Python está rodando!");
    }
});

// 3. Função para desenhar os 3 Gráficos na área de Análise
function desenharTodosGraficos(dados) {
    const canvasBarras = document.getElementById('graficoBarras');
    const canvasLinha = document.getElementById('graficoLinha');

    if (!canvasBarras || !canvasLinha) return;

    // Destruir instâncias anteriores
    if (graficoBarras) graficoBarras.destroy();
    if (graficoLinha) graficoLinha.destroy();

    const chaves = ['cdb', 'lci', 'poupanca', 'tesouro_prefixado', 'tesouro_ipca'];
    const cores = { 
        cdb: '#3498db', 
        lci: '#9b59b6', 
        poupanca: '#f39c12', 
        tesouro_prefixado: '#e74c3c', 
        tesouro_ipca: '#27ae60' 
    };

    // Criar os labels dos meses (Eixo X)
    const mesesLabels = dados.cdb.serie_temporal.map((_, i) => `Mês ${i}`);

    // --- 1. GRÁFICO DE BARRAS AGRUPADAS (Evolução Patrimonial) ---
    graficoBarras = new Chart(canvasBarras, {
        type: 'bar',
        data: {
            labels: mesesLabels, // Meses no eixo X
            datasets: chaves.map(chave => ({
                label: chave.toUpperCase().replace('_', ' '),
                data: dados[chave].serie_temporal, // Evolução mês a mês
                backgroundColor: cores[chave],
                borderRadius: 3,
                barPercentage: 0.9,      // Ajusta a largura da barra
                categoryPercentage: 0.8  // Ajusta o espaçamento entre os grupos de meses
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    mode: 'index', // Ao passar o mouse, mostra todos os investimentos daquele mês
                    intersect: false
                }
            },
            scales: {
                x: {
                    grid: { display: false } // Deixa o visual mais limpo como na imagem
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
                    }
                }
            }
        }
    });

    // --- 2. GRÁFICO DE LINHA (Comparativo de Evolução) ---
    graficoLinha = new Chart(canvasLinha, {
        type: 'line',
        data: {
            labels: mesesLabels,
            datasets: chaves.map(chave => ({
                label: chave.toUpperCase().replace('_', ' '),
                data: dados[chave].serie_temporal,
                borderColor: cores[chave],
                backgroundColor: cores[chave],
                tension: 0.3,
                pointRadius: 0
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

// 4. Função para exibir os Cards de Resultado
function exibirResultados(dados) {
    const container = document.getElementById('container-cards');
    container.innerHTML = ''; 
    const ordem = ['cdb', 'lci', 'poupanca', 'tesouro_prefixado', 'tesouro_ipca'];

    ordem.forEach(chave => {
        if (dados[chave]) {
            const inv = dados[chave];
            const card = document.createElement('div');
            card.className = `resultado-item card-${chave}`;
            
            card.innerHTML = `
                <h3>${chave === 'tesouro_ipca' ? 'TESOURO IPCA+ (Inflação + 6%)' : chave.toUpperCase().replace('_', ' ')}</h3>
                <p>Total Investido: <strong>R$ ${inv.total_investido.toLocaleString('pt-BR')}</strong></p>
                <p>Valor Líquido: <strong>R$ ${inv.valor_liquido.toLocaleString('pt-BR')}</strong></p>
                <p class="lucro">Rendimento: R$ ${inv.rendimento_liquido.toLocaleString('pt-BR')}</p>
            `;
            container.appendChild(card);
        }
    });
}