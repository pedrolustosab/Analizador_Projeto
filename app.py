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

# Configuração da Página
st.set_page_config(page_title="PMO Intelligence Pro", layout="wide", page_icon="💎")

# CSS para fixar a visibilidade e estilizar o Dropzone
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Estilização do Campo de Upload para parecer um Dropzone Premium */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #0284c7 !important;
        background: #f0f9ff !important;
        border-radius: 12px !important;
        padding: 40px !important;
    }

    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }

    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Variável para controlar o upload
uploaded_file = None

# --- SIDEBAR (Sempre visível para controle) ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #0f172a; margin: 0; font-size: 24px;'>💎 PMO Intel</h1>
            <p style='color: #64748b; font-size: 12px;'>Enterprise Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    # Upload secundário na lateral
    st.markdown("### 📥 Novo Projeto")
    sidebar_upload = st.file_uploader("Trocar arquivo XML", type=["xml"], key="sidebar_up")
    if sidebar_upload:
        uploaded_file = sidebar_upload

    st.divider()
    st.info("O processamento é realizado 100% no seu navegador, garantindo a privacidade dos dados do cronograma.")

# --- ÁREA PRINCIPAL ---
if not uploaded_file:
    # Se não houver arquivo, mostra a Landing Page com o upload no MEIO
    st.markdown("""
        <div style="text-align: center; margin-top: 5vh;">
            <span style="background: #e0f2fe; color: #0284c7; padding: 6px 16px; border-radius: 99px; font-size: 13px; font-weight: 700; text-transform: uppercase;">
                Engine de Inteligência de Projetos
            </span>
            <h1 style="color: #0f172a; font-size: 3rem; letter-spacing: -1.5px; margin-top: 20px;">
                Seu cronograma, nível <span style="color: #0284c7;">Executivo</span>.
            </h1>
            <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto 40px auto;">
                Arraste seu arquivo XML do MS Project para a área abaixo para processar métricas de EVM e Caminho Crítico.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Upload Central
    main_upload = st.file_uploader("", type=["xml"], key="main_up")
    if main_upload:
        uploaded_file = main_upload
        st.rerun() # Força a atualização para renderizar o dashboard

    # Cards informativos abaixo do upload
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><h3>🎯 EVM</h3><p>Cálculo de SPI, CPI e Curva S integrados.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><h3>🕸️ PERT</h3><p>Caminho crítico visual (CPM) dinâmico.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><h3>📊 Gantt</h3><p>Drill-down hierárquico profissional.</p></div>', unsafe_allow_html=True)

else:
    # --- DASHBOARD ATIVO ---
    st.toast('Arquivo carregado com sucesso!', icon='🚀')
    
    try:
        app_data = parse_xml_to_json(uploaded_file.getvalue())
        html_string = get_html_template(app_data)
        
        col_text, col_btn = st.columns([5, 1.5])
        with col_text:
            st.markdown(f"### 📑 Dashboard Ativo: **{app_data['proj_name']}**")
            st.caption(f"Data Base do Relatório: {app_data['status_date']}")
            
        with col_btn:
            st.download_button(
                label="📥 Exportar Cockpit (HTML)", 
                data=html_string, 
                file_name=f"Cockpit_{app_data['proj_name']}.html", 
                mime="text/html"
            )
        
        st.divider()
        
        # Renderização do Dashboard
        b64_html = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
        iframe_src = f"data:text/html;base64,{b64_html}"
        components.iframe(iframe_src, height=1400, scrolling=True)
        
    except Exception as e:
        st.error("### 🛑 Erro no processamento")
        st.markdown("O XML fornecido não possui o formato esperado pelo MS Project.")
        st.exception(e)