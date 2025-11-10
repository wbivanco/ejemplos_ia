"""Portal Principal - Sistema de Aplicaciones IA Inapsis"""
import streamlit as st
import subprocess
import os
import base64
from pathlib import Path

def get_image_base64(image_path):
    """Convierte imagen a base64 para uso en HTML"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Inapsis IA - Portal de Eventos",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# Estilos personalizados con paleta Inapsis
st.markdown("""
    <style>
    .logo-container {
        text-align: center;
        padding: 1.5rem 0;
    }
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .app-card {
        padding: 2rem;
        border-radius: 12px;
        background: white;
        border-left: 5px solid #FF6B5A;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .app-card:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(139, 123, 200, 0.2);
        border-left-color: #8B7BC8;
    }
    .app-card h3 {
        color: #8B7BC8;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: #666;
        margin-top: 4rem;
        border-top: 2px solid #f8f9fa;
    }
    .footer .brand {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .info-box {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #8B7BC8;
    }
    /* Ocultar botón de fullscreen y controles de imágenes */
    button[title="View fullscreen"],
    button[kind="header"],
    [data-testid="StyledFullScreenButton"],
    .fullScreenFrame button {
        display: none !important;
        visibility: hidden !important;
    }
    /* Centrar imágenes del header */
    .main img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    /* Ocultar overlay de imágenes */
    [data-testid="stImage"] button {
        display: none !important;
    }
    /* Ocultar anclas de headers */
    .css-10trblm,
    [data-testid="stHeaderActionElements"],
    h1 a, h2 a, h3 a {
        display: none !important;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .app-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .app-card h3 {
            font-size: 1.3rem;
        }
        .main-header h1 {
            font-size: 2rem !important;
        }
        .footer {
            padding: 2rem 0 1rem 0;
        }
        .footer .brand {
            font-size: 1.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Header principal - compacto sin scroll automático
# Logo centrado con columnas y enlace
logo_path = Path("assets/inapsis_logo.png")
if logo_path.exists():
    try:
        col_l1, col_l2, col_l3 = st.columns([2, 1, 2])
        with col_l2:
            st.markdown(
                f'<a href="https://inapsis.com.ar" target="_blank" style="display: block; text-align: center;">'
                f'<img src="data:image/png;base64,{get_image_base64(str(logo_path))}" style="max-width: 200px; width: 100%; height: auto; cursor: pointer;"></a>',
                unsafe_allow_html=True
            )
    except:
        pass

# Subtítulo centrado debajo del logo
st.markdown("""
    <div style="text-align: center; margin-top: -0.8rem; margin-bottom: 0.8rem;">
        <p style="font-size: 1.1rem; color: #666; margin: 0;">
            Experimenta el Futuro de la Inteligencia Artificial
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Verificar API Key
env_file = Path(".env")
if not env_file.exists():
    st.error("⚠️ No se encontró el archivo .env. Por favor, copia .env.example a .env y configura tu OPENAI_API_KEY")
    st.stop()

# Introducción
st.markdown("""
### Bienvenido al Demo Interactivo de IA

Explora tres experiencias diferentes diseñadas para mostrar el poder de la inteligencia artificial 
aplicada a distintos contextos:
""")

# Columnas para las aplicaciones
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="app-card">
            <h3>💼 Diagnóstico Empresarial</h3>
            <p>Analiza tu negocio y descubre oportunidades de automatización personalizadas para tu empresa.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Iniciar Diagnóstico", use_container_width=True, type="primary"):
        if 'is_unified_app' in st.session_state:
            # Modo unificado: navegar a la app
            st.session_state.pagina_actual = 'diagnostico'
            st.rerun()
        else:
            # Modo standalone: mostrar instrucciones
            st.info("📱 Abriendo aplicación de Diagnóstico Empresarial...")
            st.markdown("**Instrucciones:**")
            st.code("streamlit run diagnostico/app.py --server.port 8502", language="bash")
            st.markdown("O ejecuta en tu terminal el comando de arriba")

with col2:
    st.markdown("""
        <div class="app-card">
            <h3>🦸 Generador de Superhéroes</h3>
            <p>¡Conviértete en superhéroe! Con poderes, origen épico e imagen generada por IA. 100% Gratis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ ¡Ser Superhéroe!", use_container_width=True, type="primary"):
        if 'is_unified_app' in st.session_state:
            # Modo unificado: navegar a la app
            st.session_state.pagina_actual = 'gemelo'
            st.rerun()
        else:
            # Modo standalone: mostrar instrucciones
            st.info("📱 Abriendo Generador de Superhéroes...")
            st.markdown("**Instrucciones:**")
            st.code("streamlit run gemelo/app.py --server.port 8503", language="bash")
            st.markdown("O ejecuta en tu terminal el comando de arriba")

with col3:
    st.markdown("""
        <div class="app-card">
            <h3>🎮 Juego Visual IA</h3>
            <p>¿Foto Real o IA? ¡Adivina qué imágenes son reales y cuáles hizo la computadora! Perfecto para niños.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Jugar Ahora", use_container_width=True, type="primary"):
        if 'is_unified_app' in st.session_state:
            # Modo unificado: navegar a la app
            st.session_state.pagina_actual = 'juego'
            st.rerun()
        else:
            # Modo standalone: mostrar instrucciones
            st.info("📱 Abriendo Juego IA...")
            st.markdown("**Instrucciones:**")
            st.code("streamlit run juego/app.py --server.port 8504", language="bash")
            st.markdown("O ejecuta en tu terminal el comando de arriba")

# Nueva sección: Inteligencia Natural
st.markdown("---")
st.markdown("### 🧠 Inteligencia Natural vs Artificial")

col4, col5, col6 = st.columns([1, 1, 1])

with col5:
    st.markdown("""
        <div class="app-card">
            <h3>🧩 Juego de Lógica</h3>
            <p>Demuestra tu inteligencia natural. Sin IA, solo tu mente resolviendo desafíos de lógica, patrones y matemáticas.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧠 ¡Demostrar Inteligencia!", use_container_width=True, type="primary"):
        if 'is_unified_app' in st.session_state:
            # Modo unificado: navegar a la app
            st.session_state.pagina_actual = 'logica'
            st.rerun()
        else:
            # Modo standalone: mostrar instrucciones
            st.info("📱 Abriendo Juego de Lógica...")
            st.markdown("**Instrucciones:**")
            st.code("streamlit run logica/app.py --server.port 8505", language="bash")
            st.markdown("O ejecuta en tu terminal el comando de arriba")

# Información adicional
st.markdown("---")

col_info1, col_info2 = st.columns(2)

with col_info1:
    if 'is_unified_app' in st.session_state:
        # Modo unificado (Azure/Cloud)
        st.markdown("""
        ### 📊 Acerca de este Demo
        
        Este sistema está diseñado para funcionar online, conectándose únicamente 
        a la API de OpenAI para las inferencias. 
        
        **Ventajas:**
        - ✅ Bajo costo operativo
        - ✅ Control total de los datos
        - ✅ Ideal para eventos presenciales
        """)
    else:
        # Modo standalone (Local)
        st.markdown("""
        ### 📊 Acerca de este Demo
        
        Este sistema está diseñado para funcionar 100% localmente, conectándose únicamente 
        a la API de OpenAI para las inferencias. 
        
        **Ventajas:**
        - ✅ Bajo costo operativo
        - ✅ Control total de los datos
        - ✅ Sin dependencia de infraestructura cloud
        - ✅ Ideal para eventos presenciales
        """)

with col_info2:
    if 'is_unified_app' in st.session_state:
        # Modo unificado (Azure/Cloud) - Mostrar QR
        st.markdown("""
        ### 🌐 Acceso desde Otros Dispositivos
        
        Para permitir que otros usuarios accedan desde sus dispositivos:
        
        **Escanea el QR code con tu dispositivo móvil:** `aquí va el QR code`
        """)
    else:
        # Modo standalone (Local) - Instrucciones de IP
        st.markdown("""
        ### 🌐 Acceso desde Otros Dispositivos
        
        Para permitir que otros usuarios accedan desde sus dispositivos:
        
        1. Encuentra tu IP local: `ifconfig` (Mac/Linux) o `ipconfig` (Windows)
        2. Ejecuta con: `streamlit run main_menu.py --server.address 0.0.0.0`
        3. Comparte la URL: `http://TU_IP:8501`
        
        **Ejemplo:** `http://192.168.0.10:8501`
        """)

# Estadísticas (si existe la base de datos)
db_path = Path("evento_inapsis.db")
if db_path.exists():
    st.markdown("---")
    st.markdown("### 📈 Estadísticas del Evento")
    
    try:
        from utils.db import get_db
        db = get_db()
        stats = db.get_stats()
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            total_interacciones = sum(stats["interacciones_por_app"].values())
            st.metric("Total Interacciones", total_interacciones)
        
        with col_s2:
            st.metric("Promedio Juego", f"{stats['promedio_aciertos_juego']}%")
        
        with col_s3:
            tokens = stats['total_tokens_usados']
            costo_estimado = tokens * 0.000002  # Aproximado para GPT-3.5
            st.metric("Tokens Usados", f"{tokens:,}")
            st.caption(f"Costo estimado: ${costo_estimado:.4f}")
            
        # Detalle por app
        if stats["interacciones_por_app"]:
            st.markdown("**Interacciones por Aplicación:**")
            for app, count in stats["interacciones_por_app"].items():
                st.write(f"- {app}: {count}")
                
    except Exception as e:
        st.warning(f"No se pudieron cargar estadísticas: {e}")

# Footer
st.markdown("""
    <div class="footer">
        <p class="brand">
            <a href="https://inapsis.com.ar" target="_blank" style="text-decoration: none; 
               background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
               background-clip: text; cursor: pointer;">
                Inapsis
            </a>
        </p>
        <p style="font-size: 0.95rem; margin-top: 0.5rem;">Innovación aplicada a sistemas</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar solo se usa en app_unificada.py, aquí no hace falta

