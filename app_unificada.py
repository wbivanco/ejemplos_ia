"""Aplicación Unificada - Todas las apps en una sola interfaz"""
import streamlit as st
import sys
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Inapsis IA - Sistema Completo",
    page_icon="🧠",
    layout="wide"
)

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar utilidades
from utils.openai_client import get_openai_client
from utils.db import get_db

# Estilos CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state para navegación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'

# Sidebar para navegación
with st.sidebar:
    st.markdown("### 🧠 Inapsis IA")
    st.markdown("---")
    
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.pagina_actual = 'home'
        st.rerun()
    
    if st.button("💼 Diagnóstico Empresarial", use_container_width=True):
        st.session_state.pagina_actual = 'diagnostico'
        st.rerun()
    
    if st.button("👤 Gemelo IA", use_container_width=True):
        st.session_state.pagina_actual = 'gemelo'
        st.rerun()
    
    if st.button("🎮 Juego IA", use_container_width=True):
        st.session_state.pagina_actual = 'juego'
        st.rerun()

# Mostrar la página correspondiente
if st.session_state.pagina_actual == 'home':
    # Importar y mostrar el portal principal
    exec(open('main_menu.py').read())

elif st.session_state.pagina_actual == 'diagnostico':
    # Importar la app de diagnóstico
    exec(open('diagnostico/app.py').read())

elif st.session_state.pagina_actual == 'gemelo':
    # Importar la app de gemelo
    exec(open('gemelo/app.py').read())

elif st.session_state.pagina_actual == 'juego':
    # Importar la app de juego
    exec(open('juego/app.py').read())


