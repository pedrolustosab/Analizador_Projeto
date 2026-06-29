# 📊 Cockpit Executivo + EVA + Gantt + PERT
> Acompanhamento automatizado de cronograma e matriz de custos (EVA/EVM).

Este projeto é um Dashboard Executivo desenvolvido para um **Bootcamp de AI**. Ele transforma dados brutos exportados do Microsoft Project (XML) em um cockpit interativo, offline e de alto impacto visual, ideal para apresentações C-Level. A solução utiliza **Python**, **Streamlit** e **Engenharia de Dados** para entregar métricas avançadas de gestão de projetos.

---

## 🚀 Funcionalidades Principais

O Dashboard foi modularizado em seções estratégicas de navegação:

- **📈 Resumo do Prazo:** Visão geral da saúde do projeto, data base, tarefas mapeadas e índices de performance (SPI e CPI).
- **⏱️ Gantt Interativo:** Cronograma visual com suporte a Drilldown (WBS). Permite expandir/recolher fases, visualizar a Linha de Base (Baseline) vs. Realizado e acessar detalhes modais de cada tarefa.
- **⚠️ Painel de Atrasos:** Classificação inteligente de tarefas atrasadas:
  - **TIPO 1:** Era para iniciar, mas não iniciou.
  - **TIPO 2:** Em andamento, mas projetando estouro futuro.
  - **TIPO 3:** Deveria estar 100% concluída.
- **💰 Curva S & EVM:** Gráfico cumulativo de Valor Agregado gerado dinamicamente e sem bibliotecas externas pesadas, detalhando PV (VP), EV (VA) e AC (CR).
- **📥 Exportação HTML:** Geração de um relatório portátil e 100% offline para fácil compartilhamento.

---

## 📂 Estrutura do Projeto

```text
/
├── app.py                  # Interface Streamlit e injeção do Iframe/HTML
├── data_engine.py          # Motor de processamento WBS e cálculos financeiros (EVM)
├── requirements.txt        # Dependências do ambiente Python
├── README.md               # Documentação
└── components/
    ├── __init__.py         
    └── html_generator.py   # Motor de geração do HTML, Tailwind e SVG Nativo
🛠️ Tecnologias Utilizadas
Linguagem: Python 3.12+
Framework Web: Streamlit
Processamento de Dados: Pandas
Design & UI: HTML5, CSS3, e Tailwind CSS
Gráficos: Renderização SVG 100% nativa via Python (Zero dependência de bibliotecas JS lentas).
📦 Como Instalar e Executar
1. Clonar o Repositório
code
Bash
git clone https://github.com/seu-usuario/analizador-projeto.git
cd analizador-projeto
2. Instalar Dependências
code
Bash
pip install -r requirements.txt
3. Rodar a Aplicação
code
Bash
streamlit run app.py
💡 Como preparar seu arquivo XML
Para que o Cockpit extraia o máximo de informações (incluindo o EVM e Variações), exporte seu cronograma do Microsoft Project da seguinte forma:
Certifique-se de salvar uma Linha de Base (Baseline) no MS Project (Guia Projeto > Definir Linha de Base).
Valide se as tarefas possuem Custos ou recursos atribuídos (Para gerar o BAC, PV, AC).
Vá em Arquivo > Salvar Como.
Selecione o formato XML do Microsoft Project (*.xml).
Faça o upload do arquivo gerado diretamente no menu lateral do Dashboard.
🎓 Autor
Desenvolvido por Pedro Henrique Bezerra como projeto de excelência para o Bootcamp de AI.