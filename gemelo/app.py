"""Aplicación Gemelo IA - Genera perfiles personalizados con IA"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.openai_client import get_openai_client
from utils.db import get_db

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Gemelo IA",
        page_icon="👤",
        layout="wide"
    )

# Estilos CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .gemelo-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .stat-box {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'gemelo_generado' not in st.session_state:
    st.session_state.gemelo_generado = False
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

# Header
st.markdown("""
    <div class="main-title">
        <h1>👤 Tu Gemelo Digital con IA</h1>
        <p>Crea un perfil único generado por inteligencia artificial</p>
    </div>
""", unsafe_allow_html=True)

# Sección de entrada de datos
if not st.session_state.gemelo_generado:
    st.markdown("""
    ### ✨ Crea Tu Perfil Personalizado
    
    Nuestra IA creará un perfil único basado en tus características, intereses y personalidad.
    Cuantos más detalles proporciones, más preciso y personalizado será tu gemelo digital.
    """)
    
    st.markdown("---")
    
    with st.form("gemelo_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Información Básica")
            nombre = st.text_input("Nombre", placeholder="Tu nombre")
            edad = st.number_input("Edad", min_value=15, max_value=100, value=30)
            profesion = st.text_input("Profesión o Ocupación", placeholder="Ej: Ingeniero, Diseñador, Estudiante...")
            
        with col2:
            st.markdown("#### 🎯 Personalidad")
            personalidad = st.multiselect(
                "¿Cómo te describes?",
                ["Creativo", "Analítico", "Empático", "Líder", "Innovador", 
                 "Metódico", "Sociable", "Independiente", "Curioso", "Práctico"],
                max_selections=3
            )
            
            energia = st.select_slider(
                "Nivel de energía",
                options=["Muy tranquilo", "Tranquilo", "Equilibrado", "Energético", "Muy energético"],
                value="Equilibrado"
            )
        
        st.markdown("#### 💡 Intereses y Pasiones")
        intereses = st.text_area(
            "¿Qué te apasiona? ¿Hobbies? ¿Qué haces en tu tiempo libre?",
            placeholder="Ej: Me encanta la tecnología, practico yoga, leo ciencia ficción...",
            height=100
        )
        
        st.markdown("#### 🌟 Tu Superpoder")
        superpoder = st.text_input(
            "Si tuvieras un superpoder profesional o personal, ¿cuál sería?",
            placeholder="Ej: Resolver problemas complejos, conectar con personas, crear diseños innovadores..."
        )
        
        st.markdown("#### 🎨 Estilo de Perfil")
        estilo = st.radio(
            "¿Qué estilo prefieres para tu perfil?",
            ["Profesional y formal", "Creativo y moderno", "Inspirador y motivacional", "Divertido y casual"],
            horizontal=True
        )
        
        submitted = st.form_submit_button("✨ Generar Mi Gemelo IA", use_container_width=True, type="primary")
        
        if submitted:
            if not nombre or not profesion or not intereses or not personalidad:
                st.error("⚠️ Por favor completa todos los campos obligatorios")
            else:
                # Guardar datos
                st.session_state.datos_usuario = {
                    "nombre": nombre,
                    "edad": edad,
                    "profesion": profesion,
                    "personalidad": personalidad,
                    "energia": energia,
                    "intereses": intereses,
                    "superpoder": superpoder,
                    "estilo": estilo
                }
                
                # Generar gemelo
                with st.spinner("🤖 Creando tu gemelo digital con IA..."):
                    try:
                        client = get_openai_client()
                        
                        # Prompt para generar el perfil
                        prompt = f"""Eres un experto en crear perfiles personalizados y únicos. 

Crea un perfil de gemelo digital para esta persona con la siguiente información:

- Nombre: {nombre}
- Edad: {edad} años
- Profesión: {profesion}
- Rasgos de personalidad: {', '.join(personalidad)}
- Nivel de energía: {energia}
- Intereses y pasiones: {intereses}
- Superpoder: {superpoder}
- Estilo deseado: {estilo}

Genera un perfil único, inspirador y personalizado que incluya:

1. **Título Impactante**: Un título creativo que capture su esencia (máx 10 palabras)
2. **Bio Personalizada**: Descripción atractiva de quién es (2-3 párrafos)
3. **Fortalezas Clave**: 4-5 puntos fuertes específicos
4. **Lema Personal**: Una frase motivadora que lo/la represente
5. **Predicción IA**: Una predicción positiva sobre su futuro profesional/personal

El perfil debe ser único, motivador y reflejar genuinamente la personalidad descrita.
Usa un lenguaje {estilo.lower()} pero siempre inspirador."""

                        messages = [
                            {"role": "system", "content": "Eres un experto en crear perfiles personalizados únicos y memorables."},
                            {"role": "user", "content": prompt}
                        ]
                        
                        perfil = client.chat_completion(
                            messages=messages,
                            model="gpt-3.5-turbo",
                            temperature=0.9,  # Alta creatividad
                            max_tokens=800
                        )
                        
                        st.session_state.perfil = perfil
                        st.session_state.gemelo_generado = True
                        st.session_state.fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
                        
                        # Guardar en BD
                        db = get_db()
                        db.log_interaccion(
                            app_name="Gemelo IA",
                            user_data=st.session_state.datos_usuario,
                            result=perfil,
                            tokens_used=700
                        )
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error al generar tu gemelo: {str(e)}")
                        st.info("💡 Verifica que tu archivo .env contiene una OPENAI_API_KEY válida")

# Mostrar gemelo generado
else:
    datos = st.session_state.datos_usuario
    
    # Card principal del gemelo
    st.markdown('<div class="gemelo-card">', unsafe_allow_html=True)
    
    st.markdown(f"## 👤 Perfil de {datos['nombre']}")
    st.markdown(f"*Generado con IA el {st.session_state.fecha_generacion}*")
    
    # Estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f"**Edad**")
        st.markdown(f"### {datos['edad']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f"**Profesión**")
        st.markdown(f"### {datos['profesion'][:20]}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f"**Personalidad**")
        st.markdown(f"### {', '.join(datos['personalidad'][:2])}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f"**Energía**")
        st.markdown(f"### {datos['energia']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Perfil generado por IA
    st.markdown("---")
    st.markdown("### 🤖 Tu Perfil Generado por IA")
    
    st.markdown(st.session_state.perfil)
    
    # Información adicional
    with st.expander("📋 Ver datos ingresados"):
        st.write(f"**Nombre:** {datos['nombre']}")
        st.write(f"**Edad:** {datos['edad']}")
        st.write(f"**Profesión:** {datos['profesion']}")
        st.write(f"**Personalidad:** {', '.join(datos['personalidad'])}")
        st.write(f"**Nivel de energía:** {datos['energia']}")
        st.write(f"**Intereses:** {datos['intereses']}")
        st.write(f"**Superpoder:** {datos['superpoder']}")
        st.write(f"**Estilo:** {datos['estilo']}")
    
    # Compartir y generar nuevo
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Crear Nuevo Gemelo", use_container_width=True):
            st.session_state.gemelo_generado = False
            st.session_state.datos_usuario = {}
            st.rerun()
    
    with col2:
        st.download_button(
            label="📥 Descargar Perfil",
            data=st.session_state.perfil,
            file_name=f"gemelo_ia_{datos['nombre'].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("🏠 Volver al Portal", use_container_width=True):
            if 'is_unified_app' in st.session_state:
                # Modo unificado: navegar a home
                st.session_state.pagina_actual = 'home'
                st.rerun()
            else:
                # Modo standalone: mostrar mensaje
                st.info("Cierra esta pestaña y regresa al portal principal")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>👤 Gemelo IA | Powered by Inapsis</p>
    </div>
""", unsafe_allow_html=True)

