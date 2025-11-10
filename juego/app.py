"""Juego IA - ¿Persona o IA? Adivina quién creó el contenido"""
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
    .question-card {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        border: 3px solid #8B7BC8;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .question-card:hover {
        border-color: #FF6B5A;
        box-shadow: 0 4px 20px rgba(139, 123, 200, 0.2);
    }
    .question-card {
        max-width: 600px;
        margin: 1rem auto;
    }
    /* Estilos para TODAS las imágenes en el juego */
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
    .score-box {
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }
    .correct {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.15) 0%, rgba(76, 175, 80, 0.15) 100%);
        border: 2px solid #4caf50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .incorrect {
        background: linear-gradient(135deg, rgba(255, 107, 90, 0.15) 0%, rgba(220, 53, 69, 0.15) 100%);
        border: 2px solid #FF6B5A;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .big-button {
        font-size: 1.2rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main-title {
            padding: 1.5rem 1rem;
        }
        .main-title h1 {
            font-size: 1.8rem !important;
        }
        .question-card {
            padding: 0.5rem;
            max-width: 100%;
        }
        [data-testid="stImage"] img {
            height: 200px !important;
        }
        .score-box {
            padding: 1rem;
        }
        .big-button {
            font-size: 1rem;
            padding: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Base de datos de imágenes - 20 Reales + 20 de IA
# Las imágenes de IA están en: assets/imagenes/ia/
# Las imágenes reales vienen de Unsplash
IMAGENES_BANCO = [
    # ========== FOTOS REALES (20) ==========
    
    # ANIMALES REALES
    {
        "tipo": "animales",
        "descripcion": "🐶 Un perro jugando en el parque",
        "url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800",
        "fuente": "real",
        "pista": "Las fotos reales capturan movimientos naturales y detalles orgánicos."
    },
    {
        "tipo": "animales",
        "descripcion": "🐱 Un gato descansando",
        "url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=800",
        "fuente": "real",
        "pista": "Los animales reales tienen texturas de pelo y poses naturales."
    },
    {
        "tipo": "animales",
        "descripcion": "🐘 Un elefante en la naturaleza",
        "url": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800",
        "fuente": "real",
        "pista": "Los animales salvajes reales tienen piel con texturas naturales."
    },
    {
        "tipo": "animales",
        "descripcion": "🦎 Un dragón de Komodo",
        "url": "https://images.unsplash.com/photo-1551739440-5dd934d3a94a?w=800",
        "fuente": "real",
        "pista": "Es el animal más parecido a un dragón que existe en la realidad."
    },
    
    # PAISAJES REALES
    {
        "tipo": "paisajes",
        "descripcion": "🏔️ Montañas nevadas",
        "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
        "fuente": "real",
        "pista": "Las montañas reales tienen rocas, nieve y detalles naturales."
    },
    {
        "tipo": "paisajes",
        "descripcion": "🏖️ Una playa tropical",
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "fuente": "real",
        "pista": "Las playas reales tienen arena natural y agua con movimiento."
    },
    {
        "tipo": "paisajes",
        "descripcion": "🌲 Un bosque de árboles altos",
        "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
        "fuente": "real",
        "pista": "Los bosques reales tienen árboles de diferentes tamaños y formas."
    },
    {
        "tipo": "paisajes",
        "descripcion": "🌌 Aurora boreal en el cielo",
        "url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800",
        "fuente": "real",
        "pista": "Aunque parezca mágico, es un fenómeno natural real."
    },
    
    # OBJETOS Y TRANSPORTE REALES
    {
        "tipo": "objetos",
        "descripcion": "🚗 Un auto deportivo moderno",
        "url": "https://images.unsplash.com/photo-1494905998402-395d579af36f?w=800",
        "fuente": "real",
        "pista": "Los autos reales tienen reflejos naturales y detalles de fabricación."
    },
    {
        "tipo": "objetos",
        "descripcion": "🏠 Una casa moderna",
        "url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
        "fuente": "real",
        "pista": "Las casas reales tienen materiales como vidrio, madera y concreto."
    },
    {
        "tipo": "objetos",
        "descripcion": "🚲 Una bicicleta de montaña",
        "url": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=800",
        "fuente": "real",
        "pista": "Las bicicletas reales tienen cadenas, ruedas y materiales metálicos."
    },
    {
        "tipo": "objetos",
        "descripcion": "🛹 Un skateboard en acción",
        "url": "https://images.unsplash.com/photo-1547447134-cd3f5c716030?w=800",
        "fuente": "real",
        "pista": "Las fotos de deportes reales capturan movimiento y acción natural."
    },
    
    # LUGARES Y ARQUITECTURA REALES
    {
        "tipo": "lugares",
        "descripcion": "🏰 Un castillo medieval",
        "url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800",
        "fuente": "real",
        "pista": "Los castillos reales tienen piedras antiguas y señales de desgaste."
    },
    {
        "tipo": "lugares",
        "descripcion": "🌆 Una ciudad costera",
        "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
        "fuente": "real",
        "pista": "Las ciudades reales tienen edificios de diferentes estilos y épocas."
    },
    {
        "tipo": "lugares",
        "descripcion": "🌺 Un jardín botánico",
        "url": "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=800",
        "fuente": "real",
        "pista": "Los jardines reales tienen plantas de muchas formas y colores naturales."
    },
    {
        "tipo": "lugares",
        "descripcion": "🌳 Una casa en el árbol",
        "url": "https://images.unsplash.com/photo-1542718610-a1d656d1884c?w=800",
        "fuente": "real",
        "pista": "Las casas de árbol reales están construidas con madera y cuerdas."
    },
    {
        "tipo": "lugares",
        "descripcion": "🚂 Un tren moderno",
        "url": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800",
        "fuente": "real",
        "pista": "Los trenes reales tienen vías, ruedas metálicas y vagones reales."
    },
    
    # EFECTOS NATURALES SORPRENDENTES
    {
        "tipo": "naturaleza",
        "descripcion": "🌅 Un atardecer colorido",
        "url": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=800",
        "fuente": "real",
        "pista": "Aunque tiene colores intensos, los atardeceres son fenómenos naturales."
    },
    {
        "tipo": "naturaleza",
        "descripcion": "🕳️ Una cueva con luz natural",
        "url": "https://images.unsplash.com/photo-1542224566-6e85f2e6772f?w=800",
        "fuente": "real",
        "pista": "Las cuevas reales se forman por erosión durante miles de años."
    },
    {
        "tipo": "naturaleza",
        "descripcion": "🌺 Flores exóticas",
        "url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=800",
        "fuente": "real",
        "pista": "Las flores reales tienen pétalos con texturas y variaciones naturales."
    },
    
    # ========== IMÁGENES DE IA (20) ==========
    
    # ANIMALES FANTÁSTICOS
    {
        "tipo": "fantasia",
        "descripcion": "🦄 Un unicornio mágico",
        "url": "assets/imagenes/ia/unicornio_magico.png",
        "fuente": "ia",
        "pista": "Los unicornios no existen, solo en cuentos e imágenes de IA."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🐉 Un dragón bebé",
        "url": "assets/imagenes/ia/dragon_amigable.png",
        "fuente": "ia",
        "pista": "Los dragones que escupen fuego solo existen en la imaginación."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🐱 Un gato con alas",
        "url": "assets/imagenes/ia/gato_alas.png",
        "fuente": "ia",
        "pista": "Los gatos no pueden volar, esto es creado por IA."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🤖 Un perro robot",
        "url": "assets/imagenes/ia/perro_robot.png",
        "fuente": "ia",
        "pista": "Los perros de metal no existen en la vida real."
    },
    {
        "tipo": "fantasia",
        "descripcion": "💎 Un elefante de cristal",
        "url": "assets/imagenes/ia/elefante_cristal.png",
        "fuente": "ia",
        "pista": "Los animales transparentes como cristal son creados por IA."
    },
    
    # PAISAJES IMPOSIBLES
    {
        "tipo": "fantasia",
        "descripcion": "☁️ Montañas flotando en el cielo",
        "url": "assets/imagenes/ia/montanas_flotantes.png",
        "fuente": "ia",
        "pista": "Las montañas que flotan son imposibles por la gravedad."
    },
    {
        "tipo": "fantasia",
        "descripcion": "💎 Una playa de cristal",
        "url": "assets/imagenes/ia/playa_cristal.png",
        "fuente": "ia",
        "pista": "Las playas no están hechas de cristal en la vida real."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🍭 Un bosque de dulces",
        "url": "assets/imagenes/ia/bosque_caramelo.png",
        "fuente": "ia",
        "pista": "Los árboles de caramelo solo existen en cuentos e IA."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🌊 Una ciudad bajo el agua",
        "url": "assets/imagenes/ia/ciudad_submarina.png",
        "fuente": "ia",
        "pista": "Las ciudades submarinas son de ciencia ficción."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🌈 Un planeta con arcoíris",
        "url": "assets/imagenes/ia/planeta_arcoiris.png",
        "fuente": "ia",
        "pista": "Los planetas de colores imposibles son creados por IA."
    },
    
    # OBJETOS FUTURISTAS
    {
        "tipo": "fantasia",
        "descripcion": "🚗 Un auto que vuela",
        "url": "assets/imagenes/ia/auto_volador.png",
        "fuente": "ia",
        "pista": "Los autos voladores todavía no existen en realidad."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🏠 Una casa del futuro",
        "url": "assets/imagenes/ia/casa_futuro.png",
        "fuente": "ia",
        "pista": "Las casas con tecnología imposible son imaginadas por IA."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🚲 Una bicicleta espacial",
        "url": "assets/imagenes/ia/bicicleta_espacial.png",
        "fuente": "ia",
        "pista": "Las bicicletas no funcionan en el espacio."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🎒 Una mochila mágica",
        "url": "assets/imagenes/ia/mochila_magica.png",
        "fuente": "ia",
        "pista": "Las mochilas con poderes mágicos son de fantasía."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🛹 Una patineta antigravedad",
        "url": "assets/imagenes/ia/patineta_antigravedad.png",
        "fuente": "ia",
        "pista": "Las patinetas que flotan son de películas, no reales."
    },
    
    # LUGARES MÁGICOS
    {
        "tipo": "fantasia",
        "descripcion": "🏰 Un castillo en las nubes",
        "url": "assets/imagenes/ia/castillo_nubes.png",
        "fuente": "ia",
        "pista": "Los castillos no pueden flotar en el aire."
    },
    {
        "tipo": "fantasia",
        "descripcion": "✨ Un portal mágico",
        "url": "assets/imagenes/ia/portal_magico.png",
        "fuente": "ia",
        "pista": "Los portales a otras dimensiones son de ciencia ficción."
    },
    {
        "tipo": "fantasia",
        "descripcion": "💎 Un jardín de cristal",
        "url": "assets/imagenes/ia/jardin_cristal.png",
        "fuente": "ia",
        "pista": "Las plantas no están hechas de cristal en la vida real."
    },
    {
        "tipo": "fantasia",
        "descripcion": "⏰ Un tren del tiempo",
        "url": "assets/imagenes/ia/tren_tiempo.png",
        "fuente": "ia",
        "pista": "Los trenes que viajan en el tiempo son de fantasía."
    },
    {
        "tipo": "fantasia",
        "descripcion": "🌳 Un árbol casa gigante",
        "url": "assets/imagenes/ia/arbol_casa.png",
        "fuente": "ia",
        "pista": "Los árboles no crecen en forma de casa perfecta."
    },
]

# Inicializar session state
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
if 'aciertos' not in st.session_state:
    st.session_state.aciertos = 0
if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
if 'respondido' not in st.session_state:
    st.session_state.respondido = False
if 'respuesta_usuario' not in st.session_state:
    st.session_state.respuesta_usuario = None

# Header
st.markdown("""
    <div class="main-title">
        <h1>🎮 ¿Foto Real o IA?</h1>
        <p>¡Adivina qué imágenes son reales y cuáles hizo la computadora!</p>
    </div>
""", unsafe_allow_html=True)

def preparar_juego(num_preguntas=5):
    """Prepara las imágenes del juego"""
    # Seleccionar imágenes aleatorias del banco
    imagenes = random.sample(IMAGENES_BANCO, min(num_preguntas, len(IMAGENES_BANCO)))
    random.shuffle(imagenes)
    return imagenes

# Pantalla de inicio
if not st.session_state.juego_iniciado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🎯 ¿Cómo Jugar?
        
        Te voy a mostrar **5 imágenes**. 
        
        Tienes que adivinar si son:
        - 📷 **Foto Real** (tomada con una cámara)
        - 🤖 **Hecha por IA** (creada por una computadora)
        
        ### 💡 Ayuditas:
        - 📷 Las fotos reales tienen pequeñas imperfecciones
        - 🤖 La IA puede crear cosas que no existen (unicornios, castillos voladores)
        - 🔍 Mira los detalles: ¡algunos se ven raros!
        
        ### ¿Listo? ¡Vamos a jugar! 😄
        """)
        
        st.markdown("---")
        
        # Configuración fija: 5 preguntas
        num_preguntas = 5
        
        if st.button("🚀 ¡Empezar!", use_container_width=True, type="primary"):
            with st.spinner("Preparando las imágenes..."):
                st.session_state.preguntas = preparar_juego(num_preguntas)
                st.session_state.juego_iniciado = True
                st.session_state.pregunta_actual = 0
                st.session_state.aciertos = 0
                st.session_state.respondido = False
                st.rerun()

# Juego en progreso
elif st.session_state.pregunta_actual < len(st.session_state.preguntas):
    pregunta = st.session_state.preguntas[st.session_state.pregunta_actual]
    total_preguntas = len(st.session_state.preguntas)
    
    # Barra de progreso y puntuación
    col1, col2 = st.columns([3, 1])
    
    with col1:
        progreso = (st.session_state.pregunta_actual + 1) / total_preguntas
        st.progress(progreso)
        st.markdown(f"**Pregunta {st.session_state.pregunta_actual + 1} de {total_preguntas}**")
    
    with col2:
        st.markdown(f'<div class="score-box"><h3>{st.session_state.aciertos}</h3>Aciertos</div>', 
                   unsafe_allow_html=True)
    
    # Mostrar imagen con título dentro de la tarjeta
    st.markdown(f"""
        <div class="question-card">
            <h3 style="margin: 0 0 1rem 0; text-align: center; color: #8B7BC8;">🖼️ {pregunta['descripcion']}</h3>
    """, unsafe_allow_html=True)
    st.image(pregunta['url'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.respondido:
        # Botones de respuesta - GRANDES para niños
        st.markdown("### 👇 ¿Qué crees?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📷 Foto Real", use_container_width=True, type="primary", key="real"):
                st.session_state.respuesta_usuario = "real"
                st.session_state.respondido = True
                if pregunta["fuente"] == "real":
                    st.session_state.aciertos += 1
                st.rerun()
        
        with col2:
            if st.button("🤖 Hecha por IA", use_container_width=True, type="primary", key="ia"):
                st.session_state.respuesta_usuario = "ia"
                st.session_state.respondido = True
                if pregunta["fuente"] == "ia":
                    st.session_state.aciertos += 1
                st.rerun()
    
    else:
        # Mostrar resultado
        correcto = st.session_state.respuesta_usuario == pregunta["fuente"]
        
        if correcto:
            st.markdown("""
                <div class="correct">
                    <h2>✅ ¡Genial!</h2>
                    <p style="font-size: 1.3rem;">¡Acertaste! Muy bien 🎉</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            fuente_correcta = "📷 una Foto Real" if pregunta["fuente"] == "real" else "🤖 Hecha por IA"
            st.markdown(f"""
                <div class="incorrect">
                    <h2>❌ ¡Ups!</h2>
                    <p style="font-size: 1.3rem;">Era {fuente_correcta}</p>
                    <p>¡No te preocupes! La próxima lo harás mejor 💪</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Explicación
        st.info(f"💡 **¿Por qué?** {pregunta['pista']}")
        
        # Botón siguiente - MÁS GRANDE Y VISIBLE
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➡️ Siguiente", use_container_width=True, type="primary", key="siguiente"):
            st.session_state.pregunta_actual += 1
            st.session_state.respondido = False
            st.session_state.respuesta_usuario = None
            st.rerun()

# Fin del juego
else:
    total_preguntas = len(st.session_state.preguntas)
    aciertos = st.session_state.aciertos
    porcentaje = (aciertos / total_preguntas * 100) if total_preguntas > 0 else 0
    
    st.markdown('<div class="score-box">', unsafe_allow_html=True)
    st.markdown("## 🎉 ¡Terminaste!")
    st.markdown(f"### Acertaste: {aciertos} de {total_preguntas}")
    st.markdown(f"### {porcentaje:.0f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mensaje personalizado según el resultado - MÁS SIMPLE PARA NIÑOS
    if porcentaje >= 80:
        mensaje = "🏆 ¡Eres súper bueno! Acertaste casi todas"
        emoji = "⭐⭐⭐"
    elif porcentaje >= 60:
        mensaje = "👍 ¡Muy bien! Acertaste bastantes"
        emoji = "⭐⭐"
    elif porcentaje >= 40:
        mensaje = "😊 ¡Bien! La IA te engañó un poquito"
        emoji = "⭐"
    else:
        mensaje = "😅 La IA es muy buena engañando, ¿no?"
        emoji = "🤖"
    
    st.markdown(f"### {emoji} {mensaje}")
    
    # Dato interesante - SIMPLIFICADO
    st.info("""
    💡 **¿Sabías qué?** Incluso los adultos y expertos tienen problemas 
    para saber si una imagen es real o hecha por computadora. 
    ¡La IA es muy buena creando cosas! 
    """)
    
    # Guardar resultado
    try:
        db = get_db()
        db.log_juego_resultado(aciertos, total_preguntas)
        db.log_interaccion(
            app_name="Juego IA",
            user_data={"preguntas": total_preguntas, "aciertos": aciertos},
            result=f"Puntuación: {porcentaje:.0f}%",
            tokens_used=100  # Estimado
        )
    except:
        pass
    
    # Opciones finales
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Jugar de Nuevo", use_container_width=True, type="primary"):
            st.session_state.juego_iniciado = False
            st.session_state.pregunta_actual = 0
            st.session_state.aciertos = 0
            st.session_state.preguntas = []
            st.session_state.respondido = False
            st.rerun()
    
    with col2:
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
        <p>🎮 Juego IA | Powered by Inapsis</p>
    </div>
""", unsafe_allow_html=True)

