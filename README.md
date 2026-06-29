<div align="center">

# 📊 Cockpit Executivo + EVA + Gantt + PERT

**Dashboard executivo inteligente para gestão de projetos com análise avançada de cronograma e custos**

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Funcionalidades](#-funcionalidades-principais) • [Instalação](#-instalação-e-execução) • [Estrutura](#-estrutura-do-projeto) • [Como Usar](#-como-preparar-seu-arquivo-xml)

</div>

---

## 📋 Visão Geral

Este projeto é um **Dashboard Executivo** desenvolvido para transformar dados brutos exportados do Microsoft Project (XML) em um cockpit interativo, offline e de alto impacto visual — ideal para apresentações C-Level.

A solução utiliza **Python**, **Streamlit** e **Engenharia de Dados** para entregar métricas avançadas de gestão de projetos, incluindo:
- ✅ Análise de Valor Agregado (EVM/EVA)
- ✅ Cronograma com Gantt Interativo
- ✅ Análise de Performance (SPI/CPI)
- ✅ Identificação automática de atrasos

---

## 🚀 Funcionalidades Principais

O Dashboard foi modularizado em seções estratégicas para máxima usabilidade:

| 📈 **Resumo do Prazo** | Visão geral da saúde do projeto, data base, tarefas mapeadas e índices de performance (SPI e CPI) |
|---|---|
| **⏱️ Gantt Interativo** | Cronograma visual com Drilldown (WBS). Expanda/recolha fases, compare Baseline vs. Realizado e acesse detalhes modais |
| **⚠️ Painel de Atrasos** | Classificação inteligente com 3 tipos:<br>• **TIPO 1:** Não iniciou<br>• **TIPO 2:** Em andamento com estouro projetado<br>• **TIPO 3:** Deveria estar 100% concluída |
| **💰 Curva S & EVM** | Gráfico cumulativo de Valor Agregado dinâmico com PV (VP), EV (VA) e AC (CR) |
| **📥 Exportação HTML** | Relatório portátil e 100% offline para compartilhamento |

---

## 🛠️ Tecnologias

<div align="center">

| Categoria | Tecnologia |
|:---:|:---|
| **Linguagem** | Python 3.12+ |
| **Framework Web** | Streamlit |
| **Processamento** | Pandas, NumPy |
| **Frontend** | HTML5, CSS3, Tailwind CSS |
| **Gráficos** | SVG nativo via Python (0 deps externas) |

</div>

---

## 📂 Estrutura do Projeto

```
analizador-projeto/
├── app.py                    # Interface Streamlit e renderização
├── data_engine.py            # Motor de processamento WBS e cálculos EVM
├── html_generator.py         # Geração de HTML, Tailwind e SVG
├── requirements.txt          # Dependências Python
├── sample.xml               # Arquivo de exemplo
├── README.md                # Esta documentação
└── .streamlit/              # Configuração Streamlit
```

---

## 📦 Instalação e Execução

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/pedrolustosab/Analizador_Projeto.git
cd Analizador_Projeto
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

---

## 💡 Como Preparar seu Arquivo XML

Para extrair o máximo de informações (EVM, variações e análises), siga estes passos no **Microsoft Project**:

### ✅ Pré-requisitos

1. **Salve uma Linha de Base (Baseline)**
   - Acesse: Projeto → Definir Linha de Base
   - Isso permite comparar Planejado vs. Realizado

2. **Atribua Custos e Recursos**
   - Garanta que as tarefas possuem custos ou recursos
   - Necessário para gerar BAC, PV e AC

3. **Exporte como XML**
   - Arquivo → Salvar Como
   - Selecione formato: **XML do Microsoft Project (*.xml)**

4. **Carregue no Dashboard**
   - Use o menu lateral para fazer upload do arquivo gerado
   - O dashboard processará automaticamente!

### 📊 Resultado Esperado

Após o upload, você terá acesso a:
- Análise de prazo e custos em tempo real
- Gráficos interativos e exportáveis
- Relatório completo em HTML

---

## 🎓 Autor

Desenvolvido por **Pedro Henrique Bezerra** como projeto de excelência para o Bootcamp de AI.

---

<div align="center">

**[⬆ Voltar ao topo](#cockpit-executivo--eva--gantt--pert)**

</div>