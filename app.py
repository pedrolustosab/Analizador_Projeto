import streamlit as st
import streamlit.components.v1 as components
import base64
import time

try:
    from data_engine import parse_xml_to_json
    from html_generator import get_html_template
except Exception as e:
    st.error("### 🛑 Falha Crítica de Inicialização")
    st.exception(e)
    st.stop()

# Configuração da Página (Aparência SaaS)
st.set_page_config(page_title="PMO Intelligence Pro", layout="wide", page_icon="💎")

# CSS Avançado para overriding do Streamlit
st.markdown("""
    <style>
    /* Oculta marca d'água e menus do Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Cores e fundo da aplicação */
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem !important; max-width: 1600px; }
    
    /* Estilização da Sidebar */
    [data-testid="stSidebar"] { 
        background-color: #ffffff; 
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    /* Customização do Botão de Upload e Botão Primário */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Cards de feature na tela inicial */
    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
    .feature-title { font-weight: 700; color: #0f172a; margin-bottom: 8px; font-size: 1.1rem; }
    .feature-desc { color: #64748b; font-size: 0.9rem; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR (Menu de Controle Executivo)
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h1 style='color: #0f172a; margin: 0; font-size: 24px; letter-spacing: -0.5px;'>💎 PMO Intel</h1>
            <p style='color: #64748b; margin: 0; font-size: 13px; font-weight: 500;'>C-Level Analytics Engine</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<p style='font-size:14px; font-weight:600; color:#334155; margin-bottom:8px;'>📥 Fonte de Dados (MS Project)</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["xml"], label_visibility="collapsed")
    
    st.divider()
    
    # Selos de Governança e Segurança
    st.markdown("""
        <div style='background: #f1f5f9; padding: 16px; border-radius: 8px; font-size: 12px; color: #475569;'>
            <div style='display:flex; align-items:center; gap:8px; margin-bottom:8px;'>
                <span style='font-size:16px;'>⚡</span> <b>Motor In-Memory</b> (Sem DB)
            </div>
            <div style='display:flex; align-items:center; gap:8px; margin-bottom:8px;'>
                <span style='font-size:16px;'>🛡️</span> <b>Governança:</b> Processamento Local
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span style='font-size:16px;'>📈</span> <b>Framework:</b> PMI / EVM Standard
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# ÁREA PRINCIPAL
# ==========================================
if not uploaded_file:
    # --- ESTADO VAZIO: LANDING PAGE CORPORATIVA ---
    st.markdown("""
        <div style="text-align: center; margin-top: 8vh; margin-bottom: 60px;">
            <span style="background: #e0f2fe; color: #0284c7; padding: 6px 16px; border-radius: 99px; font-size: 13px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">
                Engine de Dados Ativada
            </span>
            <h1 style="color: #0f172a; font-size: 3.5rem; letter-spacing: -1.5px; margin-top: 24px; margin-bottom: 16px;">
                Transforme Projetos em <span style="color: #0284c7;">Inteligência</span>.
            </h1>
            <p style="color: #64748b; font-size: 1.2rem; max-width: 650px; margin: 0 auto; line-height: 1.6;">
                Faça o upload do arquivo XML do seu Microsoft Project no menu lateral e gere instantaneamente um Cockpit Executivo preditivo.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Análise EVM (Curva S)</div>
            <div class="feature-desc">Cálculo automático de Valor Agregado, SPI e CPI identificando a saúde financeira.</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🕸️</div>
            <div class="feature-title">Topologia PERT / CPM</div>
            <div class="feature-desc">Mapeamento dinâmico de rede sinalizando o Caminho Crítico e nós de alto risco.</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Gantt Drill-down</div>
            <div class="feature-desc">Visão hierárquica completa da Estrutura Analítica (WBS) com navegação fluida.</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # --- ESTADO PREENCHIDO: PROCESSAMENTO E RENDERIZAÇÃO ---
    st.toast('Arquivo XML validado com sucesso!', icon='✅')
    
    with st.spinner("⚡ Processando motor de regras e algoritmos CPM..."):
        time.sleep(0.5) # Leve delay apenas para UX (mostrar que está processando)
        try:
            # 1. Extração e Engenharia
            app_data = parse_xml_to_json(uploaded_file.getvalue())
            
            # 2. Geração do HTML (Frontend Final)
            html_string = get_html_template(app_data)
            
            # 3. Cabeçalho de Sucesso e Botão de Exportação
            col_text, col_btn = st.columns([5, 1])
            with col_text:
                st.markdown(f"### 📑 Relatório Gerado: **{app_data['proj_name']}**")
                st.caption(f"Data Base: {app_data['status_date']} | Motor Executado com Sucesso")
                
            with col_btn:
                st.download_button(
                    label="📥 Exportar HTML Offline", 
                    data=html_string, 
                    file_name="Cockpit_Executivo_PMO.html", 
                    mime="text/html", 
                    use_container_width=True
                )
            
            # 4. Injeção do HTML via iframe Base64 (Evita warnings do Streamlit)
            st.markdown("<hr style='margin-top: 0; margin-bottom: 24px; border-color: #e2e8f0;'>", unsafe_allow_html=True)
            
            b64_html = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{b64_html}"
            
            components.iframe(iframe_src, height=1400, scrolling=True)
            
        except Exception as e:
            st.error("### 🛑 Falha na Ingestão de Dados")
            st.markdown("Ocorreu um erro ao tentar processar o arquivo XML. Verifique se ele é um arquivo válido exportado pelo MS Project.")
            st.exception(e)