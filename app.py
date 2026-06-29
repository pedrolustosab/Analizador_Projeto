import streamlit as st
import streamlit.components.v1 as components
import base64

try:
    from data_engine import parse_xml_to_json
    from html_generator import get_html_template
except Exception as e:
    st.error("🛑 Falha Crítica de Inicialização")
    st.stop()

st.set_page_config(page_title="PMO Intelligence Pro", layout="wide", page_icon="🚀", initial_sidebar_state="collapsed")

# CSS para exterminar qualquer resquício do Streamlit
st.markdown("""
    <style>
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3rem !important; max-width: 1400px; }
    
    /* Upload Dropzone SaaS */
    [data-testid="stFileUploadDropzone"] {
        background-color: #ffffff !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 40px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #0284c7 !important;
        background-color: #f0f9ff !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: transform 0.2s !important;
    }
    .stDownloadButton > button:hover { transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["xml"], label_visibility="collapsed")

if not uploaded_file:
    # LANDING PAGE INICIAL
    st.markdown("""
        <div style="text-align: center; margin-top: 4vh; margin-bottom: 40px;">
            <div style="display:inline-flex; align-items:center; gap:8px; background: #ecfdf5; color: #059669; padding: 6px 16px; border-radius: 99px; font-size: 13px; font-weight: 700; margin-bottom: 24px; border: 1px solid #a7f3d0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                PROCESSAMENTO 100% NO NAVEGADOR
            </div>
            <h1 style="color: #0f172a; font-size: 3.5rem; letter-spacing: -1.5px; margin-bottom: 16px;">
                PMO Intel <span style="color: #0284c7;">Engine</span>
            </h1>
            <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                Arraste seu arquivo XML do MS Project acima. A análise de EVM, Gantt e Caminho de Marcos é gerada localmente. Nenhum dado é enviado para servidores externos.
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    # RENDERIZAÇÃO DO DASHBOARD
    with st.spinner("Construindo painel executivo..."):
        try:
            app_data = parse_xml_to_json(uploaded_file.getvalue())
            html_string = get_html_template(app_data)
            
            c1, c2 = st.columns([5, 1.5])
            with c1:
                st.markdown(f"### 📊 Dashboard: **{app_data['proj_name']}**")
            with c2:
                st.download_button("📥 Baixar Relatório HTML", html_string, file_name="PMO_Cockpit.html", mime="text/html")
            
            # Injeção Iframe Base64
            b64_html = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{b64_html}"
            components.iframe(iframe_src, height=1400, scrolling=True)
            
        except Exception as e:
            st.error("Erro na leitura do arquivo.")
            st.exception(e)