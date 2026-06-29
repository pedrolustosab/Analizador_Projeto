import streamlit as st
import streamlit.components.v1 as components
import base64

try:
    from data_engine import parse_xml_to_json
    from html_generator import get_html_template
except Exception as e:
    st.error("### 🛑 Falha de Inicialização")
    st.exception(e)
    st.stop()

st.set_page_config(page_title="Executive Command Center", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    /* header {visibility: hidden;}  <-- APAGUE OU COMENTE ESTA LINHA */
    .stApp { background-color: #f1f5f9; }
    .block-container { padding-top: 2rem !important; max-width: 1600px; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🏢 PMO Intelligence")
    st.caption("AI Analytics Engine para MS Project.")
    st.divider()
    uploaded_file = st.file_uploader("📂 Upload do MS Project (.xml)", type=["xml"])

if not uploaded_file:
    st.markdown("<h2 style='text-align:center; margin-top: 100px; color:#475569;'>Faça o upload do seu XML no menu lateral para gerar o Cockpit Premium.</h2>", unsafe_allow_html=True)
else:
    with st.spinner("🔄 Renderizando Curva S e Matriz de Gantt..."):
        try:
            app_data = parse_xml_to_json(uploaded_file.getvalue())
            html_string = get_html_template(app_data)
            
            col1, col2 = st.columns([5, 1])
            with col2:
                st.download_button(label="📥 Exportar HTML", data=html_string, file_name="Cockpit_Premium.html", mime="text/html", use_container_width=True)
            
            # --- SOLUÇÃO PARA O AVISO DE DEPRECIAÇÃO ---
            # Converte o HTML gerado para base64 e injeta usando o método iframe padrão (silencia o aviso)
            b64_html = base64.b64encode(html_string.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{b64_html}"
            
            components.iframe(iframe_src, height=1200, scrolling=True)
            
        except Exception as e:
            st.error("🛑 Erro ao processar arquivo.")
            st.exception(e)