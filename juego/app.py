"""Juego IA - ¿Persona o IA? Adivina quién creó el contenido"""
import streamlit as st
import sys
from pathlib import Path
import random

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.openai_client import get_openai_client
from utils.db import get_db

# Configuración de la página
st.set_page_config(
    page_title="Juego IA - ¿Persona o IA?",
    page_icon="🎮",
    layout="wide"
)

# Estilos CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .question-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #667eea;
        margin: 2rem 0;
        min-height: 250px;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .correct {
        background: #d4edda;
        border: 2px solid #28a745;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .incorrect {
        background: #f8d7da;
        border: 2px solid #dc3545;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .big-button {
        font-size: 1.2rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Base de datos de preguntas (mezcla de contenido humano y generado por IA)
PREGUNTAS_BANCO = [
    {
        "tipo": "texto_corto",
        "contenido": "La vida es como una caja de chocolates, nunca sabes lo que te va a tocar.",
        "fuente": "humano",
        "explicacion": "Frase icónica de la película Forrest Gump (1994)."
    },
    {
        "tipo": "texto_corto",
        "contenido": "El éxito empresarial en la era digital requiere una sinergia estratégica entre innovación disruptiva y transformación organizacional sostenible.",
        "fuente": "ia",
        "explicacion": "Uso excesivo de buzzwords y lenguaje corporativo genérico, típico de IA."
    },
    {
        "tipo": "texto_largo",
        "contenido": "A veces pienso que el café es lo único que me mantiene funcionando. No es que sea adicta o algo así, pero honestamente, ese primer sorbo en la mañana es como magia. Y no me vengan con té, eso es agua con sabor a pasto.",
        "fuente": "humano",
        "explicacion": "Tono coloquial, opiniones subjetivas fuertes y humor natural."
    },
    {
        "tipo": "consejo",
        "contenido": "Para mejorar la productividad: 1) Establezca objetivos claros y medibles. 2) Implemente técnicas de gestión del tiempo. 3) Elimine distracciones. 4) Mantenga un equilibrio saludable entre trabajo y vida personal. 5) Revise y ajuste regularmente su progreso.",
        "fuente": "ia",
        "explicacion": "Lista estructurada, formal y genérica sin personalidad."
    },
    {
        "tipo": "historia",
        "contenido": "Mi abuela siempre decía que los domingos eran sagrados. No para ir a misa (aunque también), sino para el asado familiar. Recuerdo el olor a carne y chimichurri, los primos corriendo por el patio, y ella gritando que no pisáramos sus plantas. Esos domingos no vuelven más.",
        "fuente": "humano",
        "explicacion": "Detalles sensoriales específicos, nostalgia genuina y contexto cultural."
    },
    {
        "tipo": "descripcion",
        "contenido": "El atardecer desplegaba una paleta cromática de tonalidades cálidas sobre el horizonte, mientras las aves ejecutaban sus patrones de vuelo vespertino en formaciones perfectamente simétricas.",
        "fuente": "ia",
        "explicacion": "Lenguaje excesivamente florido y descriptivo, sin emoción real."
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
        <h1>🎮 ¿Persona o IA?</h1>
        <p>Pon a prueba tu intuición - ¿Puedes distinguir entre humanos e IA?</p>
    </div>
""", unsafe_allow_html=True)

def generar_pregunta_ia(client, categoria):
    """Genera una pregunta con IA"""
    prompts = {
        "texto_corto": "Escribe una frase corta y natural sobre la vida cotidiana, como si fueras una persona común escribiendo en redes sociales.",
        "texto_largo": "Escribe un párrafo personal y coloquial sobre una experiencia cotidiana, como si fueras una persona real compartiendo sus pensamientos.",
        "consejo": "Da un consejo práctico sobre productividad o bienestar, como si fueras un experto escribiendo para un blog.",
        "historia": "Cuenta una breve anécdota personal emotiva, como si fueras alguien compartiendo un recuerdo en redes sociales.",
        "descripcion": "Describe un momento o lugar de forma literaria y evocadora."
    }
    
    prompt = prompts.get(categoria, prompts["texto_corto"])
    
    try:
        messages = [
            {"role": "system", "content": "Eres un escritor creativo. Genera contenido natural y auténtico."},
            {"role": "user", "content": f"{prompt} Máximo 3 oraciones en español."}
        ]
        
        contenido = client.chat_completion(
            messages=messages,
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=150
        )
        
        return {
            "tipo": categoria,
            "contenido": contenido.strip(),
            "fuente": "ia",
            "explicacion": "Contenido generado por IA para este juego."
        }
    except:
        return None

def preparar_juego(num_preguntas=6, usar_ia_real=False):
    """Prepara las preguntas del juego"""
    preguntas = []
    
    if usar_ia_real:
        # Mezclar preguntas del banco con algunas generadas en tiempo real
        preguntas = random.sample(PREGUNTAS_BANCO, min(4, len(PREGUNTAS_BANCO)))
        
        # Intentar agregar 2 preguntas generadas por IA en tiempo real
        try:
            client = get_openai_client()
            categorias = ["texto_corto", "historia"]
            for cat in categorias:
                pregunta_ia = generar_pregunta_ia(client, cat)
                if pregunta_ia:
                    preguntas.append(pregunta_ia)
        except:
            # Si falla, usar más del banco
            preguntas.extend(random.sample(PREGUNTAS_BANCO, 2))
    else:
        # Solo usar preguntas del banco
        preguntas = random.sample(PREGUNTAS_BANCO, min(num_preguntas, len(PREGUNTAS_BANCO)))
    
    random.shuffle(preguntas)
    return preguntas

# Pantalla de inicio
if not st.session_state.juego_iniciado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🎯 ¿Cómo Jugar?
        
        Te mostraremos varios textos. Tu misión es adivinar si fueron escritos por:
        - 🧑 **Una persona real**
        - 🤖 **Una inteligencia artificial**
        
        Presta atención a:
        - El estilo de escritura
        - Las emociones expresadas
        - Los detalles específicos
        - El uso del lenguaje
        
        ¿Listo para el desafío?
        """)
        
        st.markdown("---")
        
        num_preguntas = st.slider("Número de preguntas", 3, 6, 5)
        
        usar_ia_real = st.checkbox(
            "Incluir preguntas generadas en tiempo real por IA",
            value=False,
            help="Esto consumirá tokens de OpenAI pero hará el juego más interesante"
        )
        
        if st.button("🚀 ¡Comenzar Juego!", use_container_width=True, type="primary"):
            with st.spinner("Preparando el juego..."):
                st.session_state.preguntas = preparar_juego(num_preguntas, usar_ia_real)
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
    
    # Mostrar pregunta
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Lee el siguiente texto:")
    st.markdown(f"*{pregunta['contenido']}*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.respondido:
        # Botones de respuesta
        st.markdown("### ¿Quién lo escribió?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧑 Persona Real", use_container_width=True, type="primary"):
                st.session_state.respuesta_usuario = "humano"
                st.session_state.respondido = True
                if pregunta["fuente"] == "humano":
                    st.session_state.aciertos += 1
                st.rerun()
        
        with col2:
            if st.button("🤖 Inteligencia Artificial", use_container_width=True, type="primary"):
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
                    <h3>✅ ¡Correcto!</h3>
                    <p>Has acertado. Buen ojo para los detalles.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="incorrect">
                    <h3>❌ Incorrecto</h3>
                    <p>No te preocupes, distinguir entre humano e IA puede ser muy difícil.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Explicación
        fuente_texto = "una persona" if pregunta["fuente"] == "humano" else "IA"
        st.info(f"**Respuesta correcta:** Este texto fue escrito por **{fuente_texto}**.\n\n"
               f"💡 **Por qué:** {pregunta['explicacion']}")
        
        # Botón siguiente
        if st.button("➡️ Siguiente Pregunta", use_container_width=True, type="primary"):
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
    st.markdown("## 🎉 ¡Juego Completado!")
    st.markdown(f"### Puntuación: {aciertos} de {total_preguntas}")
    st.markdown(f"### {porcentaje:.0f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mensaje personalizado según el resultado
    if porcentaje >= 80:
        mensaje = "🏆 ¡Excelente! Tienes un gran ojo para distinguir entre humanos e IA."
        emoji = "🌟"
    elif porcentaje >= 60:
        mensaje = "👍 ¡Bien hecho! Tienes buena intuición."
        emoji = "💪"
    elif porcentaje >= 40:
        mensaje = "🤔 No está mal, pero la IA te engañó varias veces."
        emoji = "🎯"
    else:
        mensaje = "😅 La IA es más convincente de lo que parece, ¿verdad?"
        emoji = "🤖"
    
    st.markdown(f"### {emoji} {mensaje}")
    
    # Dato interesante
    st.info("""
    💡 **Dato interesante:** A medida que la IA se vuelve más sofisticada, 
    incluso expertos tienen dificultades para distinguir contenido generado por IA 
    del contenido humano, especialmente en textos cortos.
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
            st.info("Cierra esta pestaña y regresa al portal principal")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🎮 Juego IA | Powered by Inapsis</p>
    </div>
""", unsafe_allow_html=True)

