"""Aplicación Unificada - Todas las apps en una sola interfaz"""
import streamlit as st
import sys
import base64
from pathlib import Path

def get_image_base64(image_path):
    """Convierte imagen a base64 para uso en HTML"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Configuración de la página
st.set_page_config(
    page_title="Inapsis IA - Sistema Completo",
    page_icon="🧠",
    layout="wide"
)

# Bandera para indicar que estamos en modo unificado
if 'is_unified_app' not in st.session_state:
    st.session_state.is_unified_app = True

# Identificador único de sesión para aislar cada usuario
import uuid
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

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
    
    /* Fondo blanco para el logo en sidebar - centrado y responsive */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0 auto 1rem auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        display: block;
        text-align: center;
    }
    
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        margin: 0 auto;
        display: block;
    }
    
    /* Ocultar botón de fullscreen en imágenes del sidebar */
    [data-testid="stSidebar"] button[title="View fullscreen"] {
        display: none !important;
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
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            width: 140px !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            font-size: 0.9rem;
            padding: 0.6rem 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state para navegación (solo si no existe)
# Esto previene que se reinicialice cuando otro usuario interactúa
if 'pagina_actual' not in st.session_state:
    # Leer parámetro de URL si existe (compatible con Streamlit 1.28.2)
    try:
        # Intentar con la nueva API (Streamlit >= 1.29.0)
        if hasattr(st, 'query_params'):
            query_params = st.query_params
            if 'pagina_actual' in query_params:
                st.session_state.pagina_actual = query_params['pagina_actual']
            else:
                st.session_state.pagina_actual = 'home'
        # Usar API experimental (Streamlit < 1.29.0)
        elif hasattr(st, 'experimental_get_query_params'):
            query_params = st.experimental_get_query_params()
            if 'pagina_actual' in query_params:
                # experimental_get_query_params devuelve una lista
                st.session_state.pagina_actual = query_params['pagina_actual'][0]
            else:
                st.session_state.pagina_actual = 'home'
        else:
            st.session_state.pagina_actual = 'home'
    except:
        st.session_state.pagina_actual = 'home'
else:
    # Si ya existe, verificar si hay un cambio en la URL (solo para navegación directa)
    try:
        if hasattr(st, 'query_params'):
            query_params = st.query_params
            if 'pagina_actual' in query_params and query_params['pagina_actual'] != st.session_state.pagina_actual:
                st.session_state.pagina_actual = query_params['pagina_actual']
        elif hasattr(st, 'experimental_get_query_params'):
            query_params = st.experimental_get_query_params()
            if 'pagina_actual' in query_params and query_params['pagina_actual'][0] != st.session_state.pagina_actual:
                st.session_state.pagina_actual = query_params['pagina_actual'][0]
    except:
        pass  # Mantener el estado actual si hay error

# Sidebar para navegación
with st.sidebar:
    # Logo en el sidebar con fondo blanco y enlace
    logo_path = Path("assets/inapsis_logo.png")
    
    if logo_path.exists():
        try:
            st.markdown(
                f'<div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">'
                f'<a href="https://inapsis.com.ar" target="_blank" style="display: inline-block;">'
                f'<img src="data:image/png;base64,{get_image_base64(str(logo_path))}" style="max-width: 180px; width: 100%; height: auto; cursor: pointer;"></a>'
                f'</div>',
                unsafe_allow_html=True
            )
        except:
            st.markdown("### 🧠 Inapsis IA")
    else:
        st.markdown("### 🧠 Inapsis IA")
    
    st.markdown("---")
    
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.pagina_actual = 'home'
        st.rerun()
    
    if st.button("💼 Diagnóstico Empresarial", use_container_width=True):
        st.session_state.pagina_actual = 'diagnostico'
        st.rerun()
    
    if st.button("🦸 Generador de Superhéroes", use_container_width=True):
        st.session_state.pagina_actual = 'gemelo'
        st.rerun()
    
    if st.button("🍝 Generador de Brainrot Italiano", use_container_width=True):
        st.session_state.pagina_actual = 'brainrot'
        st.rerun()
    
    # JUEGO IA - COMENTADO (juego para niños deshabilitado temporalmente)
    # if st.button("🎮 Juego IA", use_container_width=True):
    #     st.session_state.pagina_actual = 'juego'
    #     st.rerun()
    
    st.markdown("---")
    st.markdown("### 🧠 Inteligencia Natural")
    
    if st.button("🧩 Juego de Lógica", use_container_width=True):
        st.session_state.pagina_actual = 'logica'
        st.rerun()

# Mostrar la página correspondiente
if st.session_state.pagina_actual == 'home':
    # Importar y mostrar el portal principal
    from main_menu import run_main_menu
    run_main_menu()

elif st.session_state.pagina_actual == 'diagnostico':
    # Importar la app de diagnóstico
    from diagnostico.app import run_diagnostico_app
    run_diagnostico_app()

elif st.session_state.pagina_actual == 'gemelo':
    # Importar la app de Generador de Superhéroes
    from gemelo.app import run_gemelo_app
    run_gemelo_app()

# JUEGO IA - COMENTADO (juego para niños deshabilitado temporalmente)
# elif st.session_state.pagina_actual == 'juego':
#     # Importar la app de juego
#     from juego.app import run_juego_app
#     run_juego_app()

elif st.session_state.pagina_actual == 'logica':
    # Importar la app de lógica
    from logica.app import run_logica_app
    run_logica_app()

elif st.session_state.pagina_actual == 'brainrot':
    # Importar la app de brainrot italiano
    from brainrot.app import run_brainrot_app
    run_brainrot_app()

elif st.session_state.pagina_actual == 'estadisticas':
    # Importar la app de estadísticas
    from estadisticas.app import run_estadisticas_app
    run_estadisticas_app()


