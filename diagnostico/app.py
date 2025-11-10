"""Aplicación de Diagnóstico Empresarial con IA"""
import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.openai_client import get_openai_client
from utils.db import get_db

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Diagnóstico Empresarial IA",
        page_icon="💼",
        layout="wide"
    )

# Estilos CSS con paleta Inapsis
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }
    .main-title h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .question-box {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #8B7BC8;
        margin: 1rem 0;
    }
    .result-box {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.15) 0%, rgba(255, 107, 90, 0.15) 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 4px solid #FF6B5A;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .result-box h3 {
        color: #8B7BC8;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'diagnostico_completado' not in st.session_state:
    st.session_state.diagnostico_completado = False
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

# Header
st.markdown("""
    <div class="main-title">
        <h1>💼 Diagnóstico Empresarial con IA</h1>
        <p>Descubre oportunidades de automatización para tu negocio</p>
    </div>
""", unsafe_allow_html=True)

# Introducción
if not st.session_state.diagnostico_completado:
    st.markdown("""
    ### 👋 Bienvenido al Diagnóstico Empresarial
    
    Responde algunas preguntas sobre tu negocio y nuestra IA te proporcionará un análisis 
    personalizado con sugerencias específicas de automatización y mejora.
    
    **Este diagnóstico te tomará aproximadamente 2-3 minutos.**
    """)
    
    st.markdown("---")
    
    # Formulario de diagnóstico
    with st.form("diagnostico_form"):
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        
        # Pregunta 1: Tipo de negocio
        st.markdown("#### 1️⃣ ¿Cuál es tu tipo de negocio?")
        tipo_negocio = st.selectbox(
            "Selecciona el sector",
            ["", "Retail/Comercio", "Servicios Profesionales", "Manufactura", 
             "Tecnología", "Salud", "Educación", "Restauración/Hostelería", 
             "Otro"],
            index=0
        )
        
        if tipo_negocio == "Otro":
            tipo_negocio_otro = st.text_input("Especifica tu sector:")
            if tipo_negocio_otro:
                tipo_negocio = tipo_negocio_otro
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pregunta 2: Tamaño
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("#### 2️⃣ ¿Cuál es el tamaño de tu empresa?")
        tamano = st.radio(
            "Número de empleados",
            ["Solo yo (emprendedor)", "2-10 empleados", "11-50 empleados", 
             "51-200 empleados", "Más de 200 empleados"],
            index=0
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pregunta 3: Principal desafío
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("#### 3️⃣ ¿Cuál es tu principal desafío operativo?")
        desafio = st.text_area(
            "Describe brevemente",
            placeholder="Ej: Gestión manual de inventario, atención al cliente lenta, reportes manuales...",
            height=100
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pregunta 4: Procesos repetitivos
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("#### 4️⃣ ¿Qué procesos realizas frecuentemente que son repetitivos?")
        procesos = st.multiselect(
            "Selecciona todos los que apliquen",
            ["Facturación", "Atención al cliente", "Gestión de inventario", 
             "Marketing/Publicidad", "Reportes y análisis", "Gestión de personal",
             "Contabilidad", "Logística/Envíos", "Ninguno específico"]
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pregunta 5: Presupuesto tecnológico
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("#### 5️⃣ ¿Cuál es tu nivel de inversión en tecnología?")
        presupuesto = st.select_slider(
            "Disposición a invertir",
            options=["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"],
            value="Medio"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de envío
        submitted = st.form_submit_button("🚀 Generar Diagnóstico", use_container_width=True, type="primary")
        
        if submitted:
            # Validar que se hayan completado los campos obligatorios
            if not tipo_negocio or not desafio or not procesos:
                st.error("⚠️ Por favor completa todos los campos obligatorios")
            else:
                # Guardar respuestas
                st.session_state.respuestas = {
                    "tipo_negocio": tipo_negocio,
                    "tamano": tamano,
                    "desafio": desafio,
                    "procesos": procesos,
                    "presupuesto": presupuesto
                }
                
                # Generar diagnóstico
                with st.spinner("🤖 Analizando tu negocio con IA..."):
                    try:
                        # Preparar el prompt
                        prompt = f"""Eres un consultor experto en transformación digital y automatización empresarial.

A continuación te presento la información de un negocio:

- Tipo de negocio: {tipo_negocio}
- Tamaño: {tamano}
- Principal desafío: {desafio}
- Procesos repetitivos: {', '.join(procesos)}
- Nivel de inversión: {presupuesto}

Por favor, genera un diagnóstico empresarial completo que incluya:

1. **Análisis de la situación actual** (2-3 párrafos)
2. **Top 3 oportunidades de automatización** específicas para este negocio
3. **Recomendaciones tecnológicas** concretas y viables
4. **Plan de acción** con pasos prioritarios
5. **ROI estimado** de implementar estas mejoras

El tono debe ser profesional pero cercano, con recomendaciones prácticas y accionables."""

                        # Llamar a OpenAI
                        client = get_openai_client()
                        messages = [
                            {"role": "system", "content": "Eres un consultor experto en transformación digital y automatización empresarial."},
                            {"role": "user", "content": prompt}
                        ]
                        
                        resultado = client.chat_completion(
                            messages=messages,
                            model="gpt-3.5-turbo",
                            temperature=0.7,
                            max_tokens=1000
                        )
                        
                        st.session_state.resultado = resultado
                        st.session_state.diagnostico_completado = True
                        
                        # Guardar en la base de datos
                        db = get_db()
                        db.log_interaccion(
                            app_name="Diagnóstico Empresarial",
                            user_data=st.session_state.respuestas,
                            result=resultado,
                            tokens_used=800  # Estimado
                        )
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error al generar el diagnóstico: {str(e)}")
                        st.info("💡 Verifica que tu archivo .env contiene una OPENAI_API_KEY válida")

# Mostrar resultado
else:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Tu Diagnóstico Empresarial")
    
    # Mostrar resumen de respuestas
    with st.expander("📋 Ver datos ingresados"):
        respuestas = st.session_state.respuestas
        st.write(f"**Tipo de negocio:** {respuestas['tipo_negocio']}")
        st.write(f"**Tamaño:** {respuestas['tamano']}")
        st.write(f"**Desafío principal:** {respuestas['desafio']}")
        st.write(f"**Procesos repetitivos:** {', '.join(respuestas['procesos'])}")
        st.write(f"**Presupuesto:** {respuestas['presupuesto']}")
    
    st.markdown("---")
    
    # Mostrar resultado de IA
    st.markdown(st.session_state.resultado)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Opciones adicionales
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Realizar Nuevo Diagnóstico", use_container_width=True):
            st.session_state.diagnostico_completado = False
            st.session_state.respuestas = {}
            st.rerun()
    
    with col2:
        if st.button("🏠 Volver al Portal Principal", use_container_width=True):
            if 'is_unified_app' in st.session_state:
                # Modo unificado: navegar a home
                st.session_state.pagina_actual = 'home'
                st.rerun()
            else:
                # Modo standalone: mostrar mensaje
                st.info("Cierra esta pestaña y regresa al portal principal en el puerto 8501")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>💼 Diagnóstico Empresarial con IA | Powered by Inapsis</p>
    </div>
""", unsafe_allow_html=True)

