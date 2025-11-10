"""Juego de Lógica - Demuestra tu Inteligencia Natural"""
import streamlit as st
import sys
from pathlib import Path
import random

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuración de la página (solo si no está en modo unificado)
if 'is_unified_app' not in st.session_state:
    st.set_page_config(
        page_title="Juego de Lógica",
        page_icon="🧩",
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
    .challenge-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #8B7BC8;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(139, 123, 200, 0.2);
    }
    .challenge-card h3 {
        color: #8B7BC8;
        margin-bottom: 1rem;
    }
    .answer-box {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #8B7BC8;
        margin: 1rem 0;
    }
    .correct-answer {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(56, 142, 60, 0.15) 100%);
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .wrong-answer {
        background: linear-gradient(135deg, rgba(255, 107, 90, 0.15) 0%, rgba(220, 53, 69, 0.15) 100%);
        border-left: 4px solid #FF6B5A;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .score-display {
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main-title {
            padding: 1.5rem 1rem;
        }
        .main-title h1 {
            font-size: 1.8rem !important;
        }
        .challenge-card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'logica_iniciado' not in st.session_state:
    st.session_state.logica_iniciado = False
if 'pregunta_actual' not in st.session_state:
    st.session_state.pregunta_actual = 0
if 'puntaje' not in st.session_state:
    st.session_state.puntaje = 0
if 'respondido' not in st.session_state:
    st.session_state.respondido = False

# Base de datos de desafíos de lógica
DESAFIOS = [
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue en la secuencia?",
        "datos": "2, 4, 8, 16, ?",
        "opciones": ["24", "32", "28", "20"],
        "respuesta_correcta": 1,  # Índice 1 = "32"
        "explicacion": "Cada número se multiplica por 2: 2×2=4, 4×2=8, 8×2=16, 16×2=32"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué figura completa el patrón?",
        "datos": "🔴 → 🔵 → 🔴 → 🔵 → ?",
        "opciones": ["🔴", "🔵", "🟢", "🟡"],
        "respuesta_correcta": 0,  # Índice 0 = "🔴"
        "explicacion": "El patrón alterna entre rojo y azul. Después de azul viene rojo."
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo 15 manzanas y regalo 7, ¿cuántas me quedan?",
        "datos": "",
        "opciones": ["6", "7", "8", "9"],
        "respuesta_correcta": 2,  # Índice 2 = "8"
        "explicacion": "15 - 7 = 8 manzanas"
    },
    {
        "tipo": "logica",
        "pregunta": "Si todos los gatos son animales y Fluffy es un gato, entonces:",
        "datos": "",
        "opciones": [
            "Fluffy es un animal",
            "Fluffy es un perro",
            "Fluffy no es un animal",
            "No se puede saber"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Si todos los gatos son animales y Fluffy es un gato, entonces Fluffy es un animal."
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué letra sigue?",
        "datos": "A, C, E, G, ?",
        "opciones": ["H", "I", "J", "K"],
        "respuesta_correcta": 1,  # Índice 1 = "I"
        "explicacion": "Se saltan letras: A (B) C (D) E (F) G (H) I"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número falta?",
        "datos": "5, 10, 15, ?, 25",
        "opciones": ["18", "20", "22", "24"],
        "respuesta_correcta": 1,  # Índice 1 = "20"
        "explicacion": "La secuencia suma 5 cada vez: 5+5=10, 10+5=15, 15+5=20, 20+5=25"
    },
    {
        "tipo": "logica",
        "pregunta": "Si llueve, llevo paraguas. No llevo paraguas. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente no está lloviendo",
            "Está lloviendo",
            "Puede estar lloviendo o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "No llevar paraguas no significa que no llueva. Puede que simplemente no lo tengas o prefieras mojarte."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un tren viaja 60 km en 2 horas. ¿Cuántos km recorre en 1 hora?",
        "datos": "",
        "opciones": ["25 km", "30 km", "35 km", "40 km"],
        "respuesta_correcta": 1,  # Índice 1 = "30 km"
        "explicacion": "60 km ÷ 2 horas = 30 km por hora"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué figura completa la serie?",
        "datos": "⬛ ⬜ ⬛ ⬜ ⬛ ?",
        "opciones": ["⬛", "⬜", "🟨", "🟩"],
        "respuesta_correcta": 1,  # Índice 1 = "⬜"
        "explicacion": "El patrón alterna entre cuadrado negro y blanco."
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "1, 4, 9, 16, ?",
        "opciones": ["20", "24", "25", "30"],
        "respuesta_correcta": 2,  # Índice 2 = "25"
        "explicacion": "Son los cuadrados perfectos: 1²=1, 2²=4, 3²=9, 4²=16, 5²=25"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si compro 3 libros a $5 cada uno, ¿cuánto gasto?",
        "datos": "",
        "opciones": ["$12", "$15", "$18", "$20"],
        "respuesta_correcta": 1,  # Índice 1 = "$15"
        "explicacion": "3 libros × $5 = $15"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "3, 6, 12, 24, ?",
        "opciones": ["36", "42", "48", "54"],
        "respuesta_correcta": 2,  # Índice 2 = "48"
        "explicacion": "Cada número se multiplica por 2: 3×2=6, 6×2=12, 12×2=24, 24×2=48"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra completa la serie?",
        "datos": "B, D, F, H, ?",
        "opciones": ["I", "J", "K", "L"],
        "respuesta_correcta": 1,  # Índice 1 = "J"
        "explicacion": "Se saltan letras: B (C) D (E) F (G) H (I) J"
    },
    {
        "tipo": "logica",
        "pregunta": "Todos los perros ladran. Max es un perro. Entonces:",
        "datos": "",
        "opciones": [
            "Max ladra",
            "Max no ladra",
            "Max es un gato",
            "No se puede saber"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Si todos los perros ladran y Max es un perro, entonces Max ladra."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un pastel se divide en 8 porciones iguales. Si como 3, ¿cuántas quedan?",
        "datos": "",
        "opciones": ["3", "4", "5", "6"],
        "respuesta_correcta": 2,  # Índice 2 = "5"
        "explicacion": "8 porciones - 3 que comí = 5 porciones restantes"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "10, 20, 30, 40, ?",
        "opciones": ["45", "50", "55", "60"],
        "respuesta_correcta": 1,  # Índice 1 = "50"
        "explicacion": "La secuencia suma 10 cada vez: 10+10=20, 20+10=30, 30+10=40, 40+10=50"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número completa el patrón?",
        "datos": "1, 3, 5, 7, ?",
        "opciones": ["8", "9", "10", "11"],
        "respuesta_correcta": 1,  # Índice 1 = "9"
        "explicacion": "Son números impares consecutivos: 1, 3, 5, 7, 9"
    },
    {
        "tipo": "logica",
        "pregunta": "Si estudio, apruebo. Aprobé. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente estudié",
            "No estudié",
            "Puede que haya estudiado o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "Aprobar no garantiza que hayas estudiado. Puedes aprobar por otras razones."
    },
    {
        "tipo": "matematico",
        "pregunta": "Tengo $50 y gasto $23. ¿Cuánto me queda?",
        "datos": "",
        "opciones": ["$25", "$27", "$28", "$30"],
        "respuesta_correcta": 1,  # Índice 1 = "$27"
        "explicacion": "$50 - $23 = $27"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "1, 3, 6, 10, ?",
        "opciones": ["13", "15", "16", "18"],
        "respuesta_correcta": 1,  # Índice 1 = "15"
        "explicacion": "Se suma 2, luego 3, luego 4, luego 5: 1+2=3, 3+3=6, 6+4=10, 10+5=15"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué figura sigue?",
        "datos": "🔺 🔷 🔺 🔷 ?",
        "opciones": ["🔺", "🔷", "🔴", "🔵"],
        "respuesta_correcta": 0,  # Índice 0 = "🔺"
        "explicacion": "El patrón alterna entre triángulo y diamante. Después de diamante viene triángulo."
    },
    {
        "tipo": "matematico",
        "pregunta": "Si camino 4 km por día durante 5 días, ¿cuántos km camino en total?",
        "datos": "",
        "opciones": ["16 km", "18 km", "20 km", "22 km"],
        "respuesta_correcta": 2,  # Índice 2 = "20 km"
        "explicacion": "4 km × 5 días = 20 km"
    },
    {
        "tipo": "logica",
        "pregunta": "Si hace frío, uso abrigo. Uso abrigo. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente hace frío",
            "No hace frío",
            "Puede hacer frío o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "Usar abrigo no significa que haga frío. Puedes usarlo por moda, por costumbre, etc."
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "7, 14, 21, 28, ?",
        "opciones": ["32", "35", "38", "42"],
        "respuesta_correcta": 1,  # Índice 1 = "35"
        "explicacion": "Múltiplos de 7: 7×1=7, 7×2=14, 7×3=21, 7×4=28, 7×5=35"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número falta?",
        "datos": "2, 6, 18, ?, 162",
        "opciones": ["36", "54", "72", "90"],
        "respuesta_correcta": 1,  # Índice 1 = "54"
        "explicacion": "Cada número se multiplica por 3: 2×3=6, 6×3=18, 18×3=54, 54×3=162"
    },
    {
        "tipo": "matematico",
        "pregunta": "Un paquete tiene 12 galletas. Si comparto 4 con un amigo, ¿cuántas me quedan?",
        "datos": "",
        "opciones": ["6", "7", "8", "9"],
        "respuesta_correcta": 2,  # Índice 2 = "8"
        "explicacion": "12 galletas - 4 que compartí = 8 galletas que me quedan"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué letra sigue?",
        "datos": "Z, Y, X, W, ?",
        "opciones": ["U", "V", "T", "S"],
        "respuesta_correcta": 1,  # Índice 1 = "V"
        "explicacion": "Letras en orden inverso: Z, Y, X, W, V"
    },
    {
        "tipo": "logica",
        "pregunta": "Todos los pájaros vuelan. Un pingüino es un pájaro. Entonces:",
        "datos": "",
        "opciones": [
            "El pingüino vuela",
            "El pingüino no vuela",
            "El pingüino no es un pájaro",
            "No se puede saber"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Aunque la premisa dice que todos los pájaros vuelan, sabemos que los pingüinos no vuelan. Esto muestra que la premisa es incorrecta o hay excepciones."
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo 24 lápices y los reparto en grupos de 6, ¿cuántos grupos tengo?",
        "datos": "",
        "opciones": ["3 grupos", "4 grupos", "5 grupos", "6 grupos"],
        "respuesta_correcta": 1,  # Índice 1 = "4 grupos"
        "explicacion": "24 lápices ÷ 6 por grupo = 4 grupos"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número completa la secuencia?",
        "datos": "100, 90, 80, 70, ?",
        "opciones": ["60", "65", "55", "50"],
        "respuesta_correcta": 0,  # Índice 0 = "60"
        "explicacion": "La secuencia resta 10 cada vez: 100-10=90, 90-10=80, 80-10=70, 70-10=60"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo 18 caramelos y doy 9, ¿cuántos me quedan?",
        "datos": "",
        "opciones": ["7", "8", "9", "10"],
        "respuesta_correcta": 2,  # Índice 2 = "9"
        "explicacion": "18 caramelos - 9 que di = 9 caramelos restantes"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "0, 5, 10, 15, ?",
        "opciones": ["18", "20", "22", "25"],
        "respuesta_correcta": 1,  # Índice 1 = "20"
        "explicacion": "Múltiplos de 5: 0, 5, 10, 15, 20"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra completa la serie?",
        "datos": "M, O, Q, S, ?",
        "opciones": ["T", "U", "V", "W"],
        "respuesta_correcta": 1,  # Índice 1 = "U"
        "explicacion": "Se saltan letras: M (N) O (P) Q (R) S (T) U"
    },
    {
        "tipo": "logica",
        "pregunta": "Si hace sol, voy a la playa. No voy a la playa. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente no hace sol",
            "Hace sol",
            "Puede hacer sol o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "No ir a la playa no significa que no haga sol. Puedes no ir por otras razones."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un autobús tiene 40 asientos. Si 25 están ocupados, ¿cuántos están libres?",
        "datos": "",
        "opciones": ["12", "13", "14", "15"],
        "respuesta_correcta": 3,  # Índice 3 = "15"
        "explicacion": "40 asientos - 25 ocupados = 15 asientos libres"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "11, 22, 33, 44, ?",
        "opciones": ["52", "54", "55", "56"],
        "respuesta_correcta": 2,  # Índice 2 = "55"
        "explicacion": "Números repetidos: 11, 22, 33, 44, 55"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número falta?",
        "datos": "4, 8, 12, ?, 20",
        "opciones": ["14", "15", "16", "18"],
        "respuesta_correcta": 2,  # Índice 2 = "16"
        "explicacion": "Múltiplos de 4: 4, 8, 12, 16, 20"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si compro 2 pizzas a $8 cada una, ¿cuánto pago?",
        "datos": "",
        "opciones": ["$14", "$16", "$18", "$20"],
        "respuesta_correcta": 1,  # Índice 1 = "$16"
        "explicacion": "2 pizzas × $8 = $16"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "13, 26, 39, 52, ?",
        "opciones": ["63", "64", "65", "66"],
        "respuesta_correcta": 2,  # Índice 2 = "65"
        "explicacion": "Múltiplos de 13: 13×1=13, 13×2=26, 13×3=39, 13×4=52, 13×5=65"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra sigue?",
        "datos": "D, G, J, M, ?",
        "opciones": ["N", "O", "P", "Q"],
        "respuesta_correcta": 2,  # Índice 2 = "P"
        "explicacion": "Se saltan 2 letras: D (E,F) G (H,I) J (K,L) M (N,O) P"
    },
    {
        "tipo": "logica",
        "pregunta": "Todos los estudiantes estudian. Ana es estudiante. Entonces:",
        "datos": "",
        "opciones": [
            "Ana estudia",
            "Ana no estudia",
            "Ana es profesora",
            "No se puede saber"
        ],
        "respuesta_correcta": 0,
        "explicacion": "Si todos los estudiantes estudian y Ana es estudiante, entonces Ana estudia."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un libro tiene 120 páginas. Si leo 45, ¿cuántas me faltan?",
        "datos": "",
        "opciones": ["70", "75", "80", "85"],
        "respuesta_correcta": 1,  # Índice 1 = "75"
        "explicacion": "120 páginas - 45 leídas = 75 páginas restantes"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "50, 45, 40, 35, ?",
        "opciones": ["28", "30", "32", "34"],
        "respuesta_correcta": 1,  # Índice 1 = "30"
        "explicacion": "La secuencia resta 5 cada vez: 50-5=45, 45-5=40, 40-5=35, 35-5=30"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número completa el patrón?",
        "datos": "9, 18, 27, 36, ?",
        "opciones": ["42", "44", "45", "48"],
        "respuesta_correcta": 2,  # Índice 2 = "45"
        "explicacion": "Múltiplos de 9: 9×1=9, 9×2=18, 9×3=27, 9×4=36, 9×5=45"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo 30 monedas y las reparto en 5 montones iguales, ¿cuántas hay en cada montón?",
        "datos": "",
        "opciones": ["5", "6", "7", "8"],
        "respuesta_correcta": 1,  # Índice 1 = "6"
        "explicacion": "30 monedas ÷ 5 montones = 6 monedas por montón"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "2, 5, 11, 23, ?",
        "opciones": ["45", "47", "49", "51"],
        "respuesta_correcta": 1,  # Índice 1 = "47"
        "explicacion": "Se multiplica por 2 y se suma 1: 2×2+1=5, 5×2+1=11, 11×2+1=23, 23×2+1=47"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra sigue?",
        "datos": "K, L, M, N, ?",
        "opciones": ["O", "P", "Q", "R"],
        "respuesta_correcta": 0,  # Índice 0 = "O"
        "explicacion": "Letras consecutivas: K, L, M, N, O"
    },
    {
        "tipo": "logica",
        "pregunta": "Si tengo hambre, como. Estoy comiendo. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente tengo hambre",
            "No tengo hambre",
            "Puede que tenga hambre o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "Comer no siempre significa tener hambre. Puedes comer por costumbre, por gusto, etc."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un reloj marca las 3:00. ¿Cuántas horas pasan hasta las 7:00?",
        "datos": "",
        "opciones": ["3 horas", "4 horas", "5 horas", "6 horas"],
        "respuesta_correcta": 1,  # Índice 1 = "4 horas"
        "explicacion": "De 3:00 a 7:00 = 4 horas"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "6, 12, 24, 48, ?",
        "opciones": ["90", "94", "96", "98"],
        "respuesta_correcta": 2,  # Índice 2 = "96"
        "explicacion": "Cada número se multiplica por 2: 6×2=12, 12×2=24, 24×2=48, 48×2=96"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número falta?",
        "datos": "8, 16, 24, ?, 40",
        "opciones": ["30", "32", "34", "36"],
        "respuesta_correcta": 1,  # Índice 1 = "32"
        "explicacion": "Múltiplos de 8: 8, 16, 24, 32, 40"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo $100 y gasto $37, ¿cuánto me queda?",
        "datos": "",
        "opciones": ["$61", "$62", "$63", "$64"],
        "respuesta_correcta": 2,  # Índice 2 = "$63"
        "explicacion": "$100 - $37 = $63"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "17, 34, 51, 68, ?",
        "opciones": ["83", "84", "85", "86"],
        "respuesta_correcta": 2,  # Índice 2 = "85"
        "explicacion": "Múltiplos de 17: 17×1=17, 17×2=34, 17×3=51, 17×4=68, 17×5=85"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra completa la serie?",
        "datos": "R, S, T, U, ?",
        "opciones": ["V", "W", "X", "Y"],
        "respuesta_correcta": 0,  # Índice 0 = "V"
        "explicacion": "Letras consecutivas: R, S, T, U, V"
    },
    {
        "tipo": "logica",
        "pregunta": "Si duermo bien, me siento descansado. Me siento descansado. Entonces:",
        "datos": "",
        "opciones": [
            "Definitivamente dormí bien",
            "No dormí bien",
            "Puede que haya dormido bien o no",
            "No se puede saber"
        ],
        "respuesta_correcta": 2,
        "explicacion": "Sentirse descansado no garantiza haber dormido bien. Puedes estar descansado por otras razones."
    },
    {
        "tipo": "matematico",
        "pregunta": "Un cuaderno tiene 80 hojas. Si uso 25, ¿cuántas quedan?",
        "datos": "",
        "opciones": ["53", "54", "55", "56"],
        "respuesta_correcta": 2,  # Índice 2 = "55"
        "explicacion": "80 hojas - 25 usadas = 55 hojas restantes"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "19, 38, 57, 76, ?",
        "opciones": ["93", "94", "95", "96"],
        "respuesta_correcta": 2,  # Índice 2 = "95"
        "explicacion": "Múltiplos de 19: 19×1=19, 19×2=38, 19×3=57, 19×4=76, 19×5=95"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número completa el patrón?",
        "datos": "15, 30, 45, 60, ?",
        "opciones": ["70", "75", "80", "85"],
        "respuesta_correcta": 1,  # Índice 1 = "75"
        "explicacion": "Múltiplos de 15: 15, 30, 45, 60, 75"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si camino 6 km por día durante 4 días, ¿cuántos km camino en total?",
        "datos": "",
        "opciones": ["22 km", "24 km", "26 km", "28 km"],
        "respuesta_correcta": 1,  # Índice 1 = "24 km"
        "explicacion": "6 km × 4 días = 24 km"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "4, 9, 16, 25, ?",
        "opciones": ["34", "35", "36", "38"],
        "respuesta_correcta": 2,  # Índice 2 = "36"
        "explicacion": "Cuadrados perfectos: 2²=4, 3²=9, 4²=16, 5²=25, 6²=36"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra sigue?",
        "datos": "F, I, L, O, ?",
        "opciones": ["Q", "R", "S", "T"],
        "respuesta_correcta": 1,  # Índice 1 = "R"
        "explicacion": "Se saltan 2 letras: F (G,H) I (J,K) L (M,N) O (P,Q) R"
    },
    {
        "tipo": "logica",
        "pregunta": "Todos los peces nadan. Un delfín nada. Entonces:",
        "datos": "",
        "opciones": [
            "El delfín es un pez",
            "El delfín no es un pez",
            "El delfín no nada",
            "No se puede saber"
        ],
        "respuesta_correcta": 1,
        "explicacion": "Aunque los delfines nadan, no son peces. Son mamíferos. Esto muestra que la premisa no es suficiente."
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo 42 canicas y las reparto en 7 grupos iguales, ¿cuántas hay en cada grupo?",
        "datos": "",
        "opciones": ["5", "6", "7", "8"],
        "respuesta_correcta": 1,  # Índice 1 = "6"
        "explicacion": "42 canicas ÷ 7 grupos = 6 canicas por grupo"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "21, 42, 63, 84, ?",
        "opciones": ["103", "104", "105", "106"],
        "respuesta_correcta": 2,  # Índice 2 = "105"
        "explicacion": "Múltiplos de 21: 21×1=21, 21×2=42, 21×3=63, 21×4=84, 21×5=105"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número falta?",
        "datos": "12, 24, 36, ?, 60",
        "opciones": ["46", "48", "50", "52"],
        "respuesta_correcta": 1,  # Índice 1 = "48"
        "explicacion": "Múltiplos de 12: 12, 24, 36, 48, 60"
    },
    {
        "tipo": "matematico",
        "pregunta": "Un paquete tiene 16 chocolates. Si como 7, ¿cuántos quedan?",
        "datos": "",
        "opciones": ["7", "8", "9", "10"],
        "respuesta_correcta": 2,  # Índice 2 = "9"
        "explicacion": "16 chocolates - 7 que comí = 9 chocolates restantes"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "25, 50, 75, 100, ?",
        "opciones": ["120", "125", "130", "135"],
        "respuesta_correcta": 1,  # Índice 1 = "125"
        "explicacion": "Múltiplos de 25: 25, 50, 75, 100, 125"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué letra completa la serie?",
        "datos": "V, W, X, Y, ?",
        "opciones": ["Z", "A", "B", "C"],
        "respuesta_correcta": 0,  # Índice 0 = "Z"
        "explicacion": "Letras consecutivas: V, W, X, Y, Z"
    },
    {
        "tipo": "matematico",
        "pregunta": "Si tengo $75 y gasto $28, ¿cuánto me queda?",
        "datos": "",
        "opciones": ["$45", "$46", "$47", "$48"],
        "respuesta_correcta": 2,  # Índice 2 = "$47"
        "explicacion": "$75 - $28 = $47"
    },
    {
        "tipo": "secuencia",
        "pregunta": "¿Qué número sigue?",
        "datos": "8, 16, 32, 64, ?",
        "opciones": ["126", "128", "130", "132"],
        "respuesta_correcta": 1,  # Índice 1 = "128"
        "explicacion": "Cada número se multiplica por 2: 8×2=16, 16×2=32, 32×2=64, 64×2=128"
    },
    {
        "tipo": "patron",
        "pregunta": "¿Qué número completa el patrón?",
        "datos": "20, 40, 60, 80, ?",
        "opciones": ["95", "100", "105", "110"],
        "respuesta_correcta": 1,  # Índice 1 = "100"
        "explicacion": "Múltiplos de 20: 20, 40, 60, 80, 100"
    },
    {
        "tipo": "matematico",
        "pregunta": "Un álbum tiene 50 fotos. Si pego 18, ¿cuántas quedan por pegar?",
        "datos": "",
        "opciones": ["30", "31", "32", "33"],
        "respuesta_correcta": 2,  # Índice 2 = "32"
        "explicacion": "50 fotos - 18 pegadas = 32 fotos restantes"
    }
]

# Header
st.markdown("""
    <div class="main-title">
        <h1>🧩 Juego de Lógica</h1>
        <p>Demuestra tu Inteligencia Natural - Sin IA, solo tu mente</p>
    </div>
""", unsafe_allow_html=True)

# Pantalla de inicio
if not st.session_state.logica_iniciado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🎯 ¿Qué es esto?
        
        Este juego **NO usa Inteligencia Artificial**. 
        
        Aquí demuestras tu **Inteligencia Natural** - tu capacidad de:
        - 🔍 **Razonar** y encontrar patrones
        - 🧮 **Calcular** y resolver problemas
        - 💭 **Pensar** lógicamente
        - 🎨 **Identificar** secuencias y relaciones
        
        ### 💡 ¿Por qué es importante?
        
        La IA es poderosa, pero **tu mente humana** tiene habilidades únicas:
        - Creatividad espontánea
        - Comprensión profunda
        - Intuición
        - Razonamiento contextual
        
        ### 🎮 ¿Cómo jugar?
        
        Responde **5 desafíos** de lógica, matemáticas y patrones.
        Cada respuesta correcta suma puntos.
        
        ### ¿Listo para demostrar tu inteligencia? 🧠
        """)
        
        st.markdown("---")
        
        if st.button("🚀 ¡Comenzar!", use_container_width=True, type="primary"):
            # Mezclar desafíos - seleccionar 5 aleatorias de las 50 disponibles
            desafios_mezclados = random.sample(DESAFIOS, min(5, len(DESAFIOS)))
            st.session_state.desafios = desafios_mezclados
            st.session_state.logica_iniciado = True
            st.session_state.pregunta_actual = 0
            st.session_state.puntaje = 0
            st.session_state.respondido = False
            st.rerun()

# Juego en progreso
elif st.session_state.pregunta_actual < len(st.session_state.desafios):
    desafio = st.session_state.desafios[st.session_state.pregunta_actual]
    total_preguntas = len(st.session_state.desafios)
    
    # Barra de progreso y puntuación
    col1, col2 = st.columns([3, 1])
    
    with col1:
        progreso = (st.session_state.pregunta_actual + 1) / total_preguntas
        st.progress(progreso)
        st.markdown(f"**Pregunta {st.session_state.pregunta_actual + 1} de {total_preguntas}**")
    
    with col2:
        st.markdown(f"""
        <div class="score-display">
            <h3 style="margin: 0; color: white;">{st.session_state.puntaje}</h3>
            <p style="margin: 0; font-size: 0.9rem;">Puntos</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar desafío
    st.markdown('<div class="challenge-card">', unsafe_allow_html=True)
    st.markdown(f"### {desafio['pregunta']}")
    
    if desafio['datos']:
        st.markdown(f"""
        <div class="answer-box">
            <p style="font-size: 1.5rem; text-align: center; margin: 0;">
                <strong>{desafio['datos']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.respondido:
        # Botones de respuesta
        st.markdown("### 👇 Elige tu respuesta:")
        
        col1, col2 = st.columns(2)
        
        for i, opcion in enumerate(desafio['opciones']):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"{opcion}", use_container_width=True, key=f"opcion_{i}"):
                    st.session_state.respuesta_usuario = i
                    st.session_state.respondido = True
                    
                    if i == desafio['respuesta_correcta']:
                        st.session_state.puntaje += 1
                    
                    st.rerun()
    else:
        # Mostrar resultado
        correcto = st.session_state.respuesta_usuario == desafio['respuesta_correcta']
        
        if correcto:
            st.markdown(f"""
            <div class="correct-answer">
                <h3>✅ ¡Correcto!</h3>
                <p><strong>Respuesta correcta:</strong> {desafio['opciones'][desafio['respuesta_correcta']]}</p>
                <p><strong>Explicación:</strong> {desafio['explicacion']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="wrong-answer">
                <h3>❌ Incorrecto</h3>
                <p><strong>Tu respuesta:</strong> {desafio['opciones'][st.session_state.respuesta_usuario]}</p>
                <p><strong>Respuesta correcta:</strong> {desafio['opciones'][desafio['respuesta_correcta']]}</p>
                <p><strong>Explicación:</strong> {desafio['explicacion']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("➡️ Siguiente Pregunta", use_container_width=True, type="primary"):
            st.session_state.pregunta_actual += 1
            st.session_state.respondido = False
            st.rerun()

# Pantalla final
else:
    porcentaje = (st.session_state.puntaje / len(st.session_state.desafios)) * 100
    
    st.markdown("""
    <div class="main-title">
        <h1>🎉 ¡Juego Completado!</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="score-display">
        <h2 style="color: white; margin: 0;">Puntaje Final</h2>
        <h1 style="color: white; font-size: 4rem; margin: 1rem 0;">
            {st.session_state.puntaje} / {len(st.session_state.desafios)}
        </h1>
        <p style="font-size: 1.5rem; margin: 0;">
            {porcentaje:.0f}% de aciertos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mensaje según puntaje
    if porcentaje >= 90:
        mensaje = "🌟 ¡Excelente! Tu inteligencia natural es excepcional"
        emoji = "🧠✨"
    elif porcentaje >= 70:
        mensaje = "👍 ¡Muy bien! Tienes buena capacidad de razonamiento"
        emoji = "💪"
    elif porcentaje >= 50:
        mensaje = "👏 Bien hecho. Sigue practicando tu lógica"
        emoji = "📚"
    else:
        mensaje = "💪 No te rindas. La práctica mejora el razonamiento"
        emoji = "🎯"
    
    st.markdown(f"""
    <div class="challenge-card" style="text-align: center;">
        <h2>{emoji}</h2>
        <h3>{mensaje}</h3>
        <p style="font-size: 1.1rem; color: #666;">
            Recuerda: Esta es tu <strong>inteligencia natural</strong>, no IA.
            <br>Tu mente humana tiene habilidades únicas que las máquinas no pueden replicar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Jugar de Nuevo", use_container_width=True, type="primary"):
            st.session_state.logica_iniciado = False
            st.session_state.pregunta_actual = 0
            st.session_state.puntaje = 0
            st.session_state.respondido = False
            st.rerun()

# Botón volver al portal
st.markdown("---")

if 'is_unified_app' in st.session_state and st.session_state.is_unified_app:
    if st.button("🏠 Volver al Portal", use_container_width=True):
        st.session_state.pagina_actual = 'home'
        st.rerun()
else:
    st.info("💡 **Modo standalone**: Ejecuta `streamlit run app_unificada.py` para acceder al portal completo")

