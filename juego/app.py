"""Juego IA - ¿Foto Real o IA? para Niños"""
import streamlit as st
import sys
import random
from pathlib import Path
from datetime import datetime
from io import BytesIO
import os

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import get_db

def run_juego_app():
    """Función principal de la app de juego IA"""
    
    # Estilos CSS
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    .main-title h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .game-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #4CAF50;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.2);
        text-align: center;
    }
    .score-display {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
    .correct-answer {
        background: #4CAF50;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .wrong-answer {
        background: #f44336;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
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
    @media (max-width: 768px) {
        [data-testid="stImage"] img {
            height: 200px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'juego_iniciado' not in st.session_state:
        st.session_state.juego_iniciado = False
        # Registrar inicio del juego
        try:
            db = get_db()
            db.log_uso_app("Juego IA", "inicio")
        except:
            pass
    
    if 'pregunta_actual' not in st.session_state:
        st.session_state.pregunta_actual = 0
    
    if 'puntaje' not in st.session_state:
        st.session_state.puntaje = 0
    
    if 'respondido' not in st.session_state:
        st.session_state.respondido = False
    
    if 'imagenes_juego' not in st.session_state:
        st.session_state.imagenes_juego = []  # Lista de 5 imágenes pre-generadas
    
    if 'respuestas_juego' not in st.session_state:
        st.session_state.respuestas_juego = []  # Lista de respuestas (True=IA, False=Real)
    
    # Header
    st.markdown("""
    <div class="main-title">
        <h1>🎮 ¿Foto Real o IA?</h1>
        <p>¡Adivina qué imágenes son reales y cuáles fueron creadas por inteligencia artificial!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pantalla de inicio
    if not st.session_state.juego_iniciado:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🎯 ¿Cómo se juega?
            
            Te mostraremos **5 imágenes** y tendrás que adivinar:
            - 📸 **¿Es una foto real?**
            - 🤖 **¿Fue creada por IA?**
            
            Cada respuesta correcta suma puntos.
            
            ### 🎨 Tipos de imágenes
            
            - **Fotos reales**: Imágenes tomadas con cámaras
            - **Imágenes IA**: Creadas por computadoras usando inteligencia artificial
            
            ### ¿Listo para jugar? 🎮
            """)
            
            st.markdown("---")
            
            if st.button("🚀 ¡Comenzar Juego!", use_container_width=True, type="primary"):
                st.session_state.juego_iniciado = True
                st.session_state.pregunta_actual = 0
                st.session_state.puntaje = 0
                st.session_state.respondido = False
                st.session_state.imagenes_juego = []
                st.session_state.respuestas_juego = []
                st.rerun()
    
    # Juego en progreso
    elif st.session_state.pregunta_actual < 5:
        # Cargar imágenes pre-generadas si no están cargadas
        if len(st.session_state.imagenes_juego) < 5:
            try:
                # Rutas a las carpetas de imágenes
                base_path = Path(__file__).parent.parent
                carpeta_ia = base_path / "assets" / "imagenes" / "ia"
                carpeta_reales = base_path / "assets" / "imagenes" / "reales"
                
                # Obtener listas de imágenes disponibles (PNG y JPG)
                imagenes_ia = []
                imagenes_reales = []
                
                if carpeta_ia.exists():
                    imagenes_ia = list(carpeta_ia.glob("*.png")) + list(carpeta_ia.glob("*.jpg")) + list(carpeta_ia.glob("*.jpeg"))
                
                if carpeta_reales.exists():
                    imagenes_reales = list(carpeta_reales.glob("*.png")) + list(carpeta_reales.glob("*.jpg")) + list(carpeta_reales.glob("*.jpeg"))
                
                # Si no hay imágenes reales, usar algunas de IA como "reales" para el juego
                if not imagenes_reales and imagenes_ia:
                    imagenes_reales = imagenes_ia.copy()
                
                # Verificar que tengamos imágenes disponibles
                if not imagenes_ia:
                    st.error("❌ No se encontraron imágenes de IA en la carpeta.")
                    return
                
                if not imagenes_reales:
                    st.warning("⚠️ No se encontraron imágenes reales. Usando algunas de IA como reales para el juego.")
                    imagenes_reales = imagenes_ia.copy()
                
                # Crear lista de pares (imagen_path, es_ia) para asegurar que cada imagen tenga su respuesta fija
                todas_imagenes = []
                
                # Agregar todas las imágenes de IA con su marca
                for img_path in imagenes_ia:
                    todas_imagenes.append((img_path, True))  # (path, es_ia)
                
                # Agregar todas las imágenes reales con su marca
                for img_path in imagenes_reales:
                    todas_imagenes.append((img_path, False))  # (path, es_ia)
                
                # Mezclar aleatoriamente todas las imágenes disponibles
                random.shuffle(todas_imagenes)
                
                # Seleccionar 5 imágenes aleatoriamente (ya mezcladas)
                imagenes_seleccionadas = []
                respuestas_seleccionadas = []
                paths_usados = set()  # Para evitar duplicados
                
                for img_path, es_ia in todas_imagenes:
                    # Evitar duplicados verificando el path
                    if img_path not in paths_usados and len(imagenes_seleccionadas) < 5:
                        paths_usados.add(img_path)
                        
                        # Leer la imagen
                        with open(img_path, 'rb') as f:
                            imagen_bytes = f.read()
                        
                        imagenes_seleccionadas.append(imagen_bytes)
                        respuestas_seleccionadas.append(es_ia)
                    
                    if len(imagenes_seleccionadas) >= 5:
                        break
                
                # Verificar que seleccionamos 5 imágenes
                if len(imagenes_seleccionadas) < 5:
                    st.error(f"❌ No hay suficientes imágenes disponibles. Solo se encontraron {len(imagenes_seleccionadas)}.")
                    return
                
                # Mezclar nuevamente el orden final para que no sea predecible
                indices = list(range(5))
                random.shuffle(indices)
                
                imagenes_seleccionadas = [imagenes_seleccionadas[i] for i in indices]
                respuestas_seleccionadas = [respuestas_seleccionadas[i] for i in indices]
                
                # Guardar en session state
                st.session_state.imagenes_juego = imagenes_seleccionadas
                st.session_state.respuestas_juego = respuestas_seleccionadas
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al cargar imágenes: {str(e)}")
        
        # Si ya tenemos todas las imágenes, mostrar la pregunta actual
        if len(st.session_state.imagenes_juego) == 5:
            # Mostrar progreso
            col1, col2 = st.columns([3, 1])
            
            with col1:
                progreso = (st.session_state.pregunta_actual + 1) / 5
                st.progress(progreso)
                st.markdown(f"**Pregunta {st.session_state.pregunta_actual + 1} de 5**")
            
            with col2:
                st.markdown(f"""
                <div class="score-display">
                    <h3 style="margin: 0; color: white;">{st.session_state.puntaje}</h3>
                    <p style="margin: 0; font-size: 0.9rem;">Puntos</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Obtener imagen y respuesta de la pregunta actual
            imagen_actual = st.session_state.imagenes_juego[st.session_state.pregunta_actual]
            es_ia_actual = st.session_state.respuestas_juego[st.session_state.pregunta_actual]
            
            # Mostrar imagen
            st.markdown('<div class="game-card">', unsafe_allow_html=True)
            st.image(imagen_actual, caption="¿Qué crees que es?")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Botones de respuesta
            if not st.session_state.respondido:
                st.markdown("### 👇 Elige tu respuesta:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📸 Foto Real", use_container_width=True, type="primary", key=f"real_{st.session_state.pregunta_actual}"):
                        st.session_state.respuesta_usuario = False
                        st.session_state.respondido = True
                        
                        if not es_ia_actual:
                            st.session_state.puntaje += 1
                        
                        st.rerun()
                
                with col2:
                    if st.button("🤖 Creada por IA", use_container_width=True, type="primary", key=f"ia_{st.session_state.pregunta_actual}"):
                        st.session_state.respuesta_usuario = True
                        st.session_state.respondido = True
                        
                        if es_ia_actual:
                            st.session_state.puntaje += 1
                        
                        st.rerun()
            else:
                # Mostrar resultado
                correcto = st.session_state.respuesta_usuario == es_ia_actual
                
                if correcto:
                    st.markdown(f"""
                    <div class="correct-answer">
                        <h3>✅ ¡Correcto!</h3>
                        <p>La imagen <strong>{"fue creada por IA" if es_ia_actual else "es una foto real"}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="wrong-answer">
                        <h3>❌ Incorrecto</h3>
                        <p>La imagen <strong>{"fue creada por IA" if es_ia_actual else "es una foto real"}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                if st.button("➡️ Siguiente Pregunta", use_container_width=True, type="primary", key=f"next_{st.session_state.pregunta_actual}"):
                    st.session_state.pregunta_actual += 1
                    st.session_state.respondido = False
                    st.rerun()
    
    # Pantalla final
    else:
        porcentaje = (st.session_state.puntaje / 5) * 100
        
        st.markdown("""
        <div class="main-title">
            <h1>🎉 ¡Juego Completado!</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="score-display">
            <h2 style="color: white; margin: 0;">Puntaje Final</h2>
            <h1 style="color: white; font-size: 4rem; margin: 1rem 0;">
                {st.session_state.puntaje} / 5
            </h1>
            <p style="font-size: 1.5rem; margin: 0;">
                {porcentaje:.0f}% de aciertos
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mensaje según puntaje
        if porcentaje >= 80:
            mensaje = "🌟 ¡Excelente! Tienes muy buen ojo para detectar IA"
            emoji = "🎯✨"
        elif porcentaje >= 60:
            mensaje = "👍 ¡Muy bien! Estás aprendiendo a distinguir"
            emoji = "👏"
        elif porcentaje >= 40:
            mensaje = "👏 Bien hecho. Sigue practicando"
            emoji = "📚"
        else:
            mensaje = "💪 No te rindas. La práctica hace al maestro"
            emoji = "🎮"
        
        st.markdown(f"""
        <div class="game-card" style="text-align: center;">
            <h2>{emoji}</h2>
            <h3>{mensaje}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Registrar completado del juego
        try:
            db = get_db()
            db.log_uso_app("Juego IA", "completado", {
                "puntaje": st.session_state.puntaje,
                "total": 5,
                "porcentaje": porcentaje
            })
            db.log_interaccion(
                app_name="Juego IA",
                user_data={"puntaje": st.session_state.puntaje, "total": 5},
                result=f"Puntuación: {porcentaje:.0f}%",
                tokens_used=0  # No usa tokens de OpenAI directamente
            )
        except:
            pass
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Jugar de Nuevo", use_container_width=True, type="primary"):
                st.session_state.juego_iniciado = False
                st.session_state.pregunta_actual = 0
                st.session_state.puntaje = 0
                st.session_state.respondido = False
                st.session_state.imagen_actual = None
                if 'imagen_bytes' in st.session_state:
                    del st.session_state.imagen_bytes
                st.rerun()
    
    # Botón volver al portal
    st.markdown("---")
    
    if 'is_unified_app' in st.session_state and st.session_state.is_unified_app:
        if st.button("🏠 Volver al Portal", use_container_width=True):
            st.session_state.pagina_actual = 'home'
            st.rerun()
    else:
        st.info("💡 **Modo standalone**: Ejecuta `streamlit run app_unificada.py` para acceder al portal completo")

# Para ejecución standalone
if __name__ == "__main__" or ('is_unified_app' not in st.session_state or 
                               st.session_state.get('is_unified_app') is None):
    # Configuración de página solo si no está en modo unificado
    if 'is_unified_app' not in st.session_state:
        st.set_page_config(
            page_title="Juego IA - ¿Persona o IA?",
            page_icon="🎮",
            layout="wide"
        )
    run_juego_app()
