"""Aplicación Generador de Superhéroes - Transforma personas en superhéroes con IA"""
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
        page_title="Generador de Superhéroes",
        page_icon="🦸",
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
    .hero-card {
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(139, 123, 200, 0.4);
    }
    .hero-card h2, .hero-card h3 {
        color: white !important;
    }
    .power-box {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .hero-image {
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 4px solid white;
        max-width: 100%;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main-title {
            padding: 1.5rem 1rem;
        }
        .main-title h1 {
            font-size: 1.8rem !important;
        }
        .hero-card {
            padding: 1.5rem;
        }
        .input-section {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'heroe_generado' not in st.session_state:
    st.session_state.heroe_generado = False
if 'datos_usuario' not in st.session_state:
    st.session_state.datos_usuario = {}

# Header
st.markdown("""
    <div class="main-title">
        <h1>🦸 Generador de Superhéroes IA</h1>
        <p>¡Descubre tu identidad secreta! Conviértete en un superhéroe único con poderes e imagen épica</p>
    </div>
""", unsafe_allow_html=True)

# Sección de entrada de datos
if not st.session_state.heroe_generado:
    st.markdown("""
    ### ✨ Crea Tu Superhéroe Personalizado
    
    Nuestra IA creará un superhéroe único con nombre, poderes, origen, debilidad y ¡una imagen épica generada!
    """)
    
    st.markdown("---")
    
    with st.form("hero_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Información Básica")
            nombre = st.text_input("Tu Nombre", placeholder="Ej: Juan Pérez")
            profesion = st.text_input("Profesión u Ocupación", placeholder="Ej: Ingeniero, Médico, Diseñador...")
            
        with col2:
            st.markdown("#### 🎯 Tu Esencia")
            hobby = st.text_input("Pasión o Hobby Principal", placeholder="Ej: Tocar guitarra, cocinar, programar...")
            rasgo = st.selectbox(
                "Tu mayor fortaleza",
                ["Creatividad", "Lógica", "Empatía", "Liderazgo", "Velocidad mental", 
                 "Persistencia", "Carisma", "Innovación", "Paciencia", "Valentía"]
            )
        
        st.markdown("#### 🎨 Preferencia de Estilo")
        estilo = st.radio(
            "¿Qué tipo de superhéroe prefieres?",
            ["Cómico y divertido", "Épico y poderoso", "Misterioso y oscuro", "Futurista y tecnológico"],
            horizontal=True
        )
        
        submitted = st.form_submit_button("✨ Generar Mi Superhéroe", use_container_width=True, type="primary")
        
        if submitted:
            if not nombre or not profesion or not hobby:
                st.error("⚠️ Por favor completa todos los campos")
            else:
                # Guardar datos
                st.session_state.datos_usuario = {
                    "nombre": nombre,
                    "profesion": profesion,
                    "hobby": hobby,
                    "rasgo": rasgo,
                    "estilo": estilo
                }
                
                # Generar superhéroe - PASO 1: Descripción
                try:
                    with st.spinner("🦸 Paso 1/2: Creando tu superhéroe..."):
                        client = get_openai_client()
                        
                        # Prompt para generar el superhéroe
                        prompt = f"""Eres un creador de superhéroes cómicos y creativos.

Crea un superhéroe DIVERTIDO y ORIGINAL basado en esta persona:
- Nombre: {nombre}
- Profesión: {profesion}
- Pasión: {hobby}
- Fortaleza: {rasgo}
- Estilo: {estilo}

Genera un perfil de superhéroe que incluya:

1. **Nombre de Superhéroe**: Un nombre gracioso y creativo relacionado con su profesión/hobby (ej: "El Programador Veloz", "La Doctora del Tiempo")

2. **Origen Épico**: Una historia de origen cómica de 2-3 líneas sobre cómo obtuvo sus poderes

3. **Superpoderes** (3-4 poderes específicos):
   - Relacionados con su profesión/hobby
   - Creativos y divertidos
   - Cada uno en una línea con emoji

4. **Lema Heroico**: Una frase pegajosa y motivadora

5. **Debilidad Graciosa**: Una debilidad cómica relacionada con su profesión/hobby

6. **Misión**: Qué tipo de problemas resuelve este superhéroe

Hazlo divertido, inspirador y memorable. Usa emojis apropiados."""

                        messages = [
                            {"role": "system", "content": "Eres un experto en crear superhéroes únicos, divertidos y memorables para eventos."},
                            {"role": "user", "content": prompt}
                        ]
                        
                        descripcion = client.chat_completion(
                            messages=messages,
                            model="gpt-3.5-turbo",
                            temperature=0.95,  # Máxima creatividad
                            max_tokens=600
                        )
                        
                        st.session_state.descripcion = descripcion
                    
                    # PASO 2: Generar imagen
                    st.success("✅ ¡Superhéroe creado!")
                    
                    # Indicador visual prominente de generación de imagen
                    banner_placeholder = st.empty()
                    banner_placeholder.markdown("""
                    <div style="background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%); 
                         padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
                        <h2 style="color: white; margin: 0;">🎨 Generando tu Imagen Épica</h2>
                        <p style="font-size: 1.2rem; margin: 0.5rem 0;">⏳ Esto puede tomar 10-20 segundos...</p>
                        <p style="font-size: 0.9rem; opacity: 0.9;">Por favor espera, estamos creando tu superhéroe visual</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress bar animada
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.info("🔄 Conectando con el servicio de generación de imágenes...")
                        progress_bar.progress(20)
                        
                        pollinations_client = get_pollinations_client()
                        status_text.info("🎨 Generando imagen con IA... (esto puede tardar un momento)")
                        progress_bar.progress(40)
                        
                        imagen = pollinations_client.generate_superhero(nombre, profesion, hobby, estilo)
                        progress_bar.progress(80)
                        
                        if imagen:
                            status_text.info("✨ Procesando imagen final...")
                            # Convertir PIL Image a bytes para Streamlit
                            buf = BytesIO()
                            imagen.save(buf, format="PNG")
                            st.session_state.imagen_bytes = buf.getvalue()
                            st.session_state.tiene_imagen = True
                            
                            progress_bar.progress(100)
                            status_text.success("✅ ¡Imagen generada exitosamente!")
                            
                            # Limpiar banner y progress bar antes del rerun
                            banner_placeholder.empty()
                            progress_bar.empty()
                            status_text.empty()
                        else:
                            banner_placeholder.empty()
                            progress_bar.empty()
                            status_text.warning("⚠️ La imagen no se generó correctamente")
                            st.session_state.tiene_imagen = False
                    except ValueError as e:
                        banner_placeholder.empty()
                        progress_bar.empty()
                        status_text.error(f"❌ Error: {str(e)}")
                        st.session_state.tiene_imagen = False
                    except Exception as e:
                        banner_placeholder.empty()
                        progress_bar.empty()
                        status_text.warning(f"⚠️ No se pudo generar la imagen: {str(e)}")
                        st.info("💡 Tu superhéroe se creó sin imagen. Puedes intentar de nuevo o continuar sin imagen.")
                        st.session_state.tiene_imagen = False
                    
                    st.session_state.heroe_generado = True
                    st.session_state.fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
                    
                    # Guardar en BD
                    db = get_db()
                    db.log_interaccion(
                        app_name="Generador de Superhéroes",
                        user_data=st.session_state.datos_usuario,
                        result=descripcion,
                        tokens_used=500
                    )
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al generar tu superhéroe: {str(e)}")
                    st.info("💡 Verifica tu archivo .env con OPENAI_API_KEY y HUGGINGFACE_API_KEY")

# Mostrar superhéroe generado
else:
    datos = st.session_state.datos_usuario
    
    # Botón para generar otro
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Crear Otro Superhéroe", use_container_width=True, type="secondary"):
            st.session_state.heroe_generado = False
            st.rerun()
    
    st.markdown("---")
    
    # Debug: Verificar estado de imagen
    tiene_imagen = st.session_state.get('tiene_imagen', False)
    
    # Mensaje de estado de imagen
    if tiene_imagen:
        st.success("✅ Superhéroe generado con imagen")
    else:
        st.warning("⚠️ Superhéroe generado sin imagen (hubo un error en la generación)")
    
    # Layout: Imagen a la izquierda, descripción a la derecha
    if tiene_imagen and 'imagen_bytes' in st.session_state:
        col_img, col_desc = st.columns([1, 2])
        
        with col_img:
            st.markdown("### 🎨 Tu Superhéroe")
            try:
                st.image(st.session_state.imagen_bytes, use_column_width=True, caption="¡Tu identidad secreta!")
            except Exception as e:
                st.error(f"Error al mostrar imagen: {str(e)}")
            
        with col_desc:
            # Card principal del superhéroe
            st.markdown('<div class="hero-card">', unsafe_allow_html=True)
            
            st.markdown(f"## 🦸 Superhéroe de {datos['nombre']}")
            st.markdown(f"*Generado con IA el {st.session_state.fecha_generacion}*")
            
            st.markdown("---")
            
            # Descripción del superhéroe
            st.markdown(st.session_state.descripcion)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Sin imagen: descripción en ancho completo
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        
        st.markdown(f"## 🦸 Superhéroe de {datos['nombre']}")
        st.markdown(f"*Generado con IA el {st.session_state.fecha_generacion}*")
        
        st.markdown("---")
        
        # Descripción del superhéroe
        st.markdown(st.session_state.descripcion)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Información adicional sobre por qué no hay imagen
        with st.expander("ℹ️ ¿Por qué no hay imagen?"):
            st.info("""
            **Posibles razones:**
            1. El servicio de generación está temporalmente no disponible
            2. Hubo un problema de conexión
            3. El servidor está sobrecargado
            
            **Solución:**
            - Intenta generar otro superhéroe
            - La generación de imágenes es gratuita e ilimitada
            - No se requiere configuración adicional
            """)
    
    st.markdown("---")
    
    # Stats del superhéroe
    st.markdown("### 📊 Datos del Origen")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="power-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f"**Identidad Civil**")
        st.markdown(f"### {datos['nombre']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="power-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f"**Profesión Base**")
        st.markdown(f"### {datos['profesion']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="power-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f"**Origen de Poderes**")
        st.markdown(f"### {datos['hobby']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="power-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f"**Rasgo Dominante**")
        st.markdown(f"### {datos['rasgo']}")
        st.markdown('</div>', unsafe_allow_html=True)

# Botón volver al portal
st.markdown("---")

if 'is_unified_app' in st.session_state and st.session_state.is_unified_app:
    if st.button("🏠 Volver al Portal", use_container_width=True):
        st.session_state.pagina_actual = 'home'
        st.rerun()
else:
    st.info("💡 **Modo standalone**: Ejecuta `streamlit run app_unificada.py` para acceder al portal completo")
