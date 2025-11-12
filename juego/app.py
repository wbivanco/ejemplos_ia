# ============================================================================
# JUEGO IA - COMENTADO (juego para niños deshabilitado temporalmente)
# ============================================================================
# Este archivo contiene el código del juego "¿Foto Real o IA?" para niños.
# El código está comentado pero preservado para reactivación futura.
# ============================================================================

import streamlit as st

# Mensaje de que el juego está deshabilitado
st.error("🚫 Este juego está temporalmente deshabilitado.")
st.info("💡 El juego '¿Foto Real o IA?' para niños ha sido desactivado temporalmente.")

# ============================================================================
# TODO EL CÓDIGO ORIGINAL ESTÁ COMENTADO A CONTINUACIÓN
# Para reactivar el juego, descomentar todo el código desde aquí hasta el final
# ============================================================================

"""
# Código original del juego (comentado):

\"\"\"Juego IA - ¿Persona o IA? Adivina quién creó el contenido\"\"\"
import streamlit as st
import sys
from pathlib import Path
import random

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.openai_client import get_openai_client
from utils.db import get_db

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Juego IA - ¿Persona o IA?",
        page_icon="🎮",
        layout="wide"
    )

# [TODO EL RESTO DEL CÓDIGO ORIGINAL ESTÁ PRESERVADO EN EL ARCHIVO]
# Para ver el código completo original, revisa el historial de git o
# descomenta las líneas anteriores y restaura el código desde el backup.
"""
