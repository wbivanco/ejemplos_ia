"""Generador de Brainrot Italiano para Niños - Crea memes absurdos con estilo italiano"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.openai_client import get_openai_client
from utils.pollinations_client import get_pollinations_client
from utils.db import get_db

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Generador de Brainrot Italiano",
        page_icon="🍝",
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
    .input-section {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #8B7BC8;
    }
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #8B7BC8;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(139, 123, 200, 0.2);
        text-align: center;
    }
    .result-card img {
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    /* Estilos para imágenes - tamaño similar al juego */
    [data-testid="stImage"] {
        max-width: 600px !important;
        margin: 0 auto !important;
    }
    [data-testid="stImage"] img {
        width: 100% !important;
        height: 250px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
    }
    /* Responsive para móviles */
    @media (max-width: 768px) {
        [data-testid="stImage"] img {
            height: 200px !important;
        }
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main-title {
            padding: 1.5rem 1rem;
        }
        .main-title h1 {
            font-size: 1.8rem !important;
        }
        .input-section {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'brainrot_generado' not in st.session_state:
    st.session_state.brainrot_generado = False
if 'brainrot_iniciado' not in st.session_state:
    st.session_state.brainrot_iniciado = False
    # Registrar inicio de la app
    try:
        db = get_db()
        db.log_uso_app("Generador de Brainrot Italiano", "inicio")
    except:
        pass
    st.session_state.brainrot_iniciado = True

# Header
st.markdown("""
    <div class="main-title">
        <h1>🍝 Generador de Brainrot Italiano</h1>
        <p>¡Crea memes absurdos con estilo italiano! Divertido y colorido</p>
    </div>
""", unsafe_allow_html=True)

# Sección de entrada de datos
if not st.session_state.brainrot_generado:
    st.markdown("""
    ### ✨ Crea Tu Brainrot Italiano
    
    Llena el formulario y crearemos una imagen absurda y divertida con estilo italiano.
    """)
    
    st.markdown("---")
    
    with st.form("brainrot_form"):
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        # Nombre del niño
        nombre = st.text_input("👤 Tu Nombre", placeholder="Ej: Juan", help="Tu nombre aparecerá en el brainrot")
        
        # Animal o cosa
        animal_cosa = st.text_input("🐾 Animal o Cosa", placeholder="Ej: gato, pizza, unicornio, robot...", help="¿Qué quieres incluir en tu brainrot?")
        
        st.markdown("---")
        
        # Checkbox para generar nombre del brainrot automáticamente
        nombre_brainrot_automatico = st.checkbox(
            "🎭 Generar nombre del brainrot automáticamente",
            value=True,  # Por defecto tildado
            help="Si está marcado, generaremos un nombre absurdo para tu brainrot. Si no, usaremos tu nombre."
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🎨 ¡Crear Mi Brainrot!", use_container_width=True, type="primary")
        
        if submitted:
            if not nombre or not animal_cosa:
                st.error("⚠️ Por favor completa tu nombre y el animal/cosa")
            else:
                # Guardar datos (el texto siempre se genera en italiano automáticamente)
                st.session_state.datos_brainrot = {
                    "nombre": nombre,
                    "animal_cosa": animal_cosa,
                    "nombre_brainrot_automatico": nombre_brainrot_automatico
                }
                
                # Generar brainrot
                try:
                    with st.spinner("🍝 Generando tu brainrot italiano..."):
                        # Paso 1: Generar nombre del brainrot si es automático, sino usar el nombre del niño
                        nombre_brainrot = ""
                        if nombre_brainrot_automatico:
                            try:
                                client = get_openai_client()
                                prompt_nombre = f"""
Genera un nombre absurdo y divertido en italiano para un meme tipo brainrot.

Contexto: El meme incluye un/a {animal_cosa}.

Reglas:
- No usar el nombre del niño ("{nombre}").
- Debe sonar como un título corto (máx. 3 o 4 palabras).
- Estilo italiano, humorístico y absurdo.
- Puede incluir emojis.
- No des explicaciones, solo devuelve el nombre.

Ejemplos de estilo:
- Il Gatto Pazzo
- Super Pizza Volante
- Mamma Mia Robot
- Il Brainrot Assurdo
"""
                                messages_nombre = [
                                    {"role": "system", "content": "Eres un generador creativo de nombres absurdos y divertidos en italiano para memes tipo brainrot."},
                                    {"role": "user", "content": prompt_nombre}
                                ]
                                
                                nombre_brainrot = client.chat_completion(
                                    messages=messages_nombre,
                                    temperature=0.9,
                                    max_tokens=30
                                ).strip()
                                
                                st.session_state.nombre_brainrot = nombre_brainrot
                            except Exception as e:
                                st.warning(f"⚠️ No se pudo generar nombre automático: {str(e)}")
                                # Fallback a nombre genérico (sin usar el nombre del niño)
                                nombre_brainrot = f"Il Brainrot Pazzo"
                                st.session_state.nombre_brainrot = nombre_brainrot
                        else:
                            # Si no está tildado, usar el nombre del niño
                            nombre_brainrot = nombre
                            st.session_state.nombre_brainrot = nombre_brainrot
                        
                        # Paso 2: Generar texto italiano automáticamente (siempre)
                        texto_italiano = ""
                        try:
                            client = get_openai_client()
                            prompt_italiano = f"""Genera una frase absurda y divertida en italiano para un meme/brainrot.
                            
Contexto: Un brainrot llamado "{nombre_brainrot}" con un/a {animal_cosa} en un estilo de meme italiano absurdo.

La frase debe ser:
- En italiano
- Absurda y divertida
- Corta (máximo 10 palabras)
- Estilo meme/brainrot italiano
- Puede incluir emojis

Ejemplos de estilo:
- "Mamma mia! Questo {animal_cosa} è pazzo! 🤪"
- "Io {nombre_brainrot} sono pazzo! 🍝"
- "Questo è il brainrot più italiano! 🇮🇹"

Solo devuelve la frase, sin explicaciones."""

                            messages = [
                                {"role": "system", "content": "Eres un experto en memes italianos y frases absurdas divertidas."},
                                {"role": "user", "content": prompt_italiano}
                            ]
                            
                            texto_italiano = client.chat_completion(
                                messages=messages,
                                temperature=0.9,
                                max_tokens=50
                            ).strip()
                            
                            st.session_state.texto_italiano = texto_italiano
                        except Exception as e:
                            st.warning(f"⚠️ No se pudo generar texto italiano automático: {str(e)}")
                            # Fallback a texto simple
                            texto_italiano = f"Mamma mia! {nombre_brainrot} e {animal_cosa} sono pazzi! 🇮🇹"
                            st.session_state.texto_italiano = texto_italiano
                        
                        # Paso 3: Generar imagen con Pollinations.ai
                        st.info("🎨 Creando la imagen... (esto puede tardar 10-20 segundos)")
                        
                        pollinations_client = get_pollinations_client()
                        
                        # Construir prompt para la imagen
                        prompt_imagen = f"""Brainrot italiano meme style: {nombre_brainrot} con un/a {animal_cosa} absurdo/a, 
                        texto italiano: "{texto_italiano}", colores vibrantes neón, estilo meme italiano absurdo, 
                        composición divertida y colorida, alta calidad, estilo brainrot, fondo colorido, 
                        diseño absurdo y divertido"""
                        
                        imagen = pollinations_client.generate_brainrot(nombre_brainrot, animal_cosa, texto_italiano)
                        
                        if imagen:
                            # Convertir PIL Image a bytes para Streamlit
                            buf = BytesIO()
                            imagen.save(buf, format="PNG")
                            st.session_state.imagen_bytes = buf.getvalue()
                            st.session_state.brainrot_generado = True
                            st.session_state.fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
                            
                            # Guardar en BD
                            try:
                                db = get_db()
                                db.log_interaccion(
                                    app_name="Generador de Brainrot Italiano",
                                    user_data=st.session_state.datos_brainrot,
                                    result=f"Nombre: {nombre_brainrot}, Texto: {texto_italiano}",
                                    tokens_used=150  # Estimado (nombre + texto)
                                )
                                db.log_uso_app("Generador de Brainrot Italiano", "completado", {
                                    "nombre": nombre,
                                    "nombre_brainrot": nombre_brainrot,
                                    "animal_cosa": animal_cosa,
                                    "nombre_brainrot_automatico": nombre_brainrot_automatico
                                })
                            except:
                                pass
                            
                            st.rerun()
                        else:
                            st.error("❌ No se pudo generar la imagen. Intenta de nuevo.")
                            
                except Exception as e:
                    st.error(f"❌ Error al generar tu brainrot: {str(e)}")
                    st.info("💡 Verifica tu archivo .env con OPENAI_API_KEY")

# Mostrar brainrot generado
else:
    datos = st.session_state.datos_brainrot
    
    # Botón para generar otro
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Crear Otro Brainrot", use_container_width=True, type="secondary"):
            st.session_state.brainrot_generado = False
            st.rerun()
    
    st.markdown("---")
    
    # Mostrar resultado
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    nombre_brainrot = st.session_state.get('nombre_brainrot', datos.get('nombre', 'Brainrot'))
    st.markdown(f"## 🍝 {nombre_brainrot}")
    st.markdown(f"*Creado por {datos['nombre']} - {st.session_state.fecha_generacion}*")
    
    st.markdown("---")
    
    # Mostrar imagen
    if 'imagen_bytes' in st.session_state:
        st.image(st.session_state.imagen_bytes, caption="¡Tu brainrot italiano!")
        
        # Botón de descarga
        st.markdown("---")
        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = nombre_brainrot.replace(" ", "_").replace("'", "").replace("!", "").replace("?", "")
        st.download_button(
            label="📥 Descargar Imagen",
            data=st.session_state.imagen_bytes,
            file_name=f"brainrot_{nombre_archivo}_{fecha}.png",
            mime="image/png",
            use_container_width=True,
            type="primary"
        )
    
    # Mostrar texto generado
    if 'texto_italiano' in st.session_state:
        st.markdown("---")
        st.info(f"**🇮🇹 Texto italiano generado:**\n\n*{st.session_state.texto_italiano}*")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Info adicional
    st.markdown("---")
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown(f"**👤 Nombre:** {datos['nombre']}")
        st.markdown(f"**🎭 Nombre del Brainrot:** {nombre_brainrot}")
        st.markdown(f"**🐾 Animal/Cosa:** {datos['animal_cosa']}")
    
    with col_info2:
        modo_nombre = "Automático 🎭" if datos.get('nombre_brainrot_automatico', True) else "Personalizado ✍️"
        modo_texto = "Automático 🇮🇹"  # Siempre automático (checkbox eliminado)
        st.markdown(f"**🎭 Nombre:** {modo_nombre}")
        st.markdown(f"**📝 Texto:** {modo_texto}")

# Botón volver al portal
st.markdown("---")

if 'is_unified_app' in st.session_state and st.session_state.is_unified_app:
    if st.button("🏠 Volver al Portal", use_container_width=True):
        st.session_state.pagina_actual = 'home'
        st.rerun()
else:
    st.info("💡 **Modo standalone**: Ejecuta `streamlit run app_unificada.py` para acceder al portal completo")

