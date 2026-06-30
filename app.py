import streamlit as st
import streamlit.components.v1 as components
import base64
import os

try:
    from data_engine import parse_xml_to_json
    from html_generator import get_html_template
except Exception as e:
    st.error("🛑 Falha Crítica de Inicialização")
    st.stop()

st.set_page_config(page_title="PMO Intelligence Pro", layout="wide", page_icon="🚀", initial_sidebar_state="collapsed")

# Função de segurança para carregar o playbook
def load_playbook():
    try:
        with open("playbook.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<html><body><h2>Erro: O arquivo playbook.html não foi encontrado no servidor.</h2></body></html>"

playbook_content = load_playbook()

# CSS SaaS Premium (Forçando 100% de largura de ponta a ponta)
st.markdown("""
    <style>
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* FORÇA A TELA 100% DE PONTA A PONTA */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 100% !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important; 
    }
    
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
    
    /* Botões Premium */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .stDownloadButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["xml"], label_visibility="collapsed")

if not uploaded_file:
    # LANDING PAGE INICIAL
    st.markdown("""
        <div style="text-align: center; margin-top: 4vh; margin-bottom: 24px;">
            <div style="display:inline-flex; align-items:center; gap:8px; background: #ecfdf5; color: #059669; padding: 6px 16px; border-radius: 99px; font-size: 13px; font-weight: 700; margin-bottom: 24px; border: 1px solid #a7f3d0;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                PROCESSAMENTO 100% NO NAVEGADOR
            </div>
            <h1 style="color: #0f172a; font-size: 3.5rem; letter-spacing: -1.5px; margin-top: 24px; margin-bottom: 16px;">
                PMO Intel <span style="color: #0284c7;">Engine</span>
            </h1>
            <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                Arraste seu arquivo XML do MS Project acima. A análise de EVM, Gantt e Caminho de Marcos é gerada localmente. Nenhum dado é enviado para servidores externos.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de Playbook centralizado na tela inicial
    col_space1, col_btn, col_space2 = st.columns([1.5, 2, 1.5])
    with col_btn:
        st.download_button(
            label="📘 Baixar Playbook (Manual de Adoção)", 
            data=playbook_content, 
            file_name="Playbook_PMO_Intel.html", 
            mime="text/html",
            use_container_width=True
        )

else:
    # RENDERIZAÇÃO DO DASHBOARD ATIVO
    with st.spinner("Construindo painel executivo e matriz de causas..."):
        try:
            app_data = parse_xml_to_json(uploaded_file.getvalue())
            html_string = get_html_template(app_data)
            
            # Cabeçalho do App de ponta a ponta
            c1, c2, c3 = st.columns([4, 1.5, 1.5])
            with c1:
                st.markdown(f"### 📊 Dashboard: **{app_data['proj_name']}**")
            with c2:
                st.download_button(
                    label="📘 Baixar Playbook", 
                    data=playbook_content, 
                    file_name="Playbook_PMO_Intel.html", 
                    mime="text/html",
                    use_container_width=True
                )
            with c3:
                st.download_button(
                    label="📥 Exportar Relatório HTML", 
                    data=html_string, 
                    file_name="PMO_Cockpit.html", 
                    mime="text/html",
                    use_container_width=True
                )
            
            st.markdown("<hr style='margin: 8px 0 24px 0; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            # Injeção Iframe Base64 do Dashboard
            b64_html = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{b64_html}"
            components.iframe(iframe_src, height=1400, scrolling=True)
            
        except Exception as e:
            st.error("Erro na leitura do arquivo XML. Verifique se ele foi exportado corretamente do MS Project.")
            st.exception(e)