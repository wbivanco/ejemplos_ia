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

# Bandera para indicar que estamos en modo unificado
if 'is_unified_app' not in st.session_state:
    st.session_state.is_unified_app = True

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar utilidades
from utils.openai_client import get_openai_client
from utils.db import get_db

# Estilos CSS con paleta Inapsis
st.markdown("""
    <style>
    /* Sidebar con gradiente Inapsis */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #8B7BC8 0%, #FF6B5A 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700;
    }
    
    /* Botones del sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: white;
        transform: translateX(5px);
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state para navegación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'home'

# Sidebar para navegación
with st.sidebar:
    # Logo en el sidebar
    logo_path = Path("assets/inapsis_logo.png")
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
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


