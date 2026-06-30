<div align="center">

# 💎 PMO Intel Engine

**Diagnostic Analytics & EVM Dashboard para Microsoft Project**

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Engine-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[Proposta de Valor](#-a-proposta-de-valor) • [Features Core](#-features-core-c-level) • [Arquitetura](#-arquitetura-técnica) • [Quickstart](#-quickstart-como-rodar)

</div>

---

## 🎯 A Proposta de Valor

Arquivos nativos do Microsoft Project (`.mpp` ou `.xml`) são robustos, mas oferecem uma péssima experiência de usuário (UX) para diretores e stakeholders. **Eles não querem ver linhas infinitas; eles querem saber onde o projeto está sangrando.**

O **PMO Intel Engine** é uma aplicação SaaS *In-Memory* que minera a estrutura analítica de um cronograma XML e a converte instantaneamente em um **Cockpit Executivo Interativo**. Zero banco de dados. Zero envio de informações para a nuvem. Processamento 100% local com exportação de relatórios HTML portáteis.

---

## ✨ Features Core (C-Level)

### 🚨 1. Matriz de Gravidade (Diagnostic Analytics)
O sistema não diz apenas se a tarefa está "Atrasada". O algoritmo em Python cruza o avanço físico, o tempo decorrido, a linha de base e os gargalos de predecessoras para taguear as anomalias em 3 Filas de Ação:
*   🔴 **Fila de Incêndio:** Marcos Rompidos, Estouro Real e Efeito Dominó.
*   🟠 **Fila de Atenção:** Inércia de Início, Desvio Projetado e Alerta de Ritmo.
*   🟣 **Auditoria:** Cronograma Maquiado ou Absorvido no Crítico.

### 💰 2. Motor EVM (Earned Value Management)
Cálculo automatizado a prova de falhas matemáticas (divisão por zero) para métricas globais de projeto:
*   **Curva S Dinâmica** renderizada em SVG puro (sem pacotes pesados).
*   Índices de Performance de Prazo (**SPI**) e Custo (**CPI**).
*   Variações Financeiras (**SV**, **CV**) e Projeções Finais (**EAC**, **VAC**).

### 📊 3. Gantt Interativo & Tracker
*   **Tracker de Delivery:** Linha do tempo visual no topo do relatório focada apenas nos *Milestones* (Marcos).
*   **WBS Drill-down:** Tabela de Gantt expansível com menu em cascata para isolar e inspecionar apenas tarefas com anomalias de Causa Raiz.

### 📥 4. Exportação "Single-File" HTML
Todo o dashboard (com os modais pop-up, CSS, JavaScript e Dados) é compactado e encodado em um único arquivo `.html`. O gestor baixa o arquivo e o envia via e-mail ou WhatsApp para a diretoria, que o abre interativamente no celular, **totalmente offline**.

---

## 🧠 Arquitetura Técnica

Este projeto foi arquitetado com foco em **Clean Code**, separação de responsabilidades (MVC) e *Tolerância a Falhas*.

| Módulo | Responsabilidade | Stack / Lógica |
| :--- | :--- | :--- |
| `app.py` | Controller & View | Streamlit atuando como Landing Page. CSS injetado para overriding de componentes nativos (Look & Feel SaaS). |
| `data_engine.py` | Model & Business Rules | **Pandas** + `xml.etree`. Onde a mágica matemática acontece. Extrai dependências e processa a Matriz de Gravidade. |
| `html_generator.py` | UI/UX Renderer | Gera a interface Executiva, constrói os SVGs matematicamente e injeta o JavaScript para os filtros e *Drill-down*. |

> **Tech Flex:** Para evitar *warnings* de depreciação visual do Streamlit ao injetar iframes pesados, o HTML gerado pelo backend é encodado em **Base64** e injetado via Data URI (`data:text/html;base64,...`), garantindo uma renderização 100% edge-to-edge na tela.

---

## 📂 Estrutura do Projeto

```text
pmo-intel-engine/
├── .streamlit/
│   └── config.toml           # Oculta menus padrão do Streamlit (UI Premium)
├── app.py                    # Interface de Upload e Controller principal
├── data_engine.py            # Motor de mineração XML, WBS e EVM
├── html_generator.py         # Template HTML5/CSS3/JS e gráficos SVG
├── playbook.html             # Manual de Adoção Corporativa (Embutido no App)
├── requirements.txt          # Dependências
├── sample.xml                # Arquivo de exemplo com custos, baselines e atrasos
└── README.md                 # Esta documentação
```

---

## ⚡ Quickstart (Como Rodar)

**Pré-requisitos:** Python 3.10 ou superior.

1. **Clone o Repositório:**
```bash
git clone https://github.com/seu-usuario/pmo-intel-engine.git
cd pmo-intel-engine
```

2. **Instale as dependências (Apenas Pandas e Streamlit):**
```bash
pip install -r requirements.txt
```

3. **Inicie a Engine Executiva:**
```bash
streamlit run app.py
```

> **Para testar:** Use o arquivo `sample.xml` incluso no repositório. Ele já contém a Linha de Base salva, orçamentos (BAC) e anomalias plantadas para disparar a Matriz de Gravidade.

---

<div align="center">
  <p>Desenvolvido com 💡 e IA como projeto de excelência Analítica e de Automação.</p>
</div>