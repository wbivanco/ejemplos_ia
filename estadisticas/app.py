"""Dashboard de Estadísticas - Inapsis"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json
import csv
from io import StringIO

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import get_db

def run_estadisticas_app():
    """Función principal de la app de estadísticas"""
    
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
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #8B7BC8;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stat-card h3 {
        color: #8B7BC8;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
    }
    .stat-card .number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FF6B5A;
        margin: 0;
    }
    .section-header {
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #8B7BC8;
        margin: 2rem 0 1rem 0;
    }
    .section-header h2 {
        color: #8B7BC8;
        margin: 0;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main-title {
            padding: 1.5rem 1rem;
        }
        .stat-card .number {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-title">
        <h1>📊 Dashboard de Estadísticas</h1>
        <p>Métricas y análisis del evento Inapsis</p>
    </div>
    """, unsafe_allow_html=True)

    # Obtener estadísticas
    try:
        db = get_db()
        stats = db.get_stats()
        
        # ========== RESUMEN GENERAL ==========
        st.markdown('<div class="section-header"><h2>📈 Resumen General</h2></div>', unsafe_allow_html=True)
    
        col1, col2, col3, col4 = st.columns(4)
    
        inicios = stats.get('inicios_por_app', {})
        completados = stats.get('completados_por_app', {})
        total_inicios = sum(inicios.values())
        total_completados = sum(completados.values())
    
        with col1:
            st.markdown("""
        <div class="stat-card">
            <h3>🎮 Apps Iniciadas</h3>
            <p class="number">{}</p>
        </div>
        """.format(total_inicios), unsafe_allow_html=True)
    
        with col2:
            st.markdown("""
        <div class="stat-card">
            <h3>✅ Apps Completadas</h3>
            <p class="number">{}</p>
        </div>
        """.format(total_completados), unsafe_allow_html=True)
    
        with col3:
            tasa = (total_completados / total_inicios * 100) if total_inicios > 0 else 0
        st.markdown("""
        <div class="stat-card">
            <h3>📊 Tasa de Completado</h3>
            <p class="number">{:.1f}%</p>
        </div>
        """.format(tasa), unsafe_allow_html=True)
    
        with col4:
            total_leads = stats.get('total_leads_empresariales', 0) + stats.get('total_leads_generales', 0)
        st.markdown("""
        <div class="stat-card">
            <h3>📧 Total Leads</h3>
            <p class="number">{}</p>
        </div>
        """.format(total_leads), unsafe_allow_html=True)
    
        # ========== USO POR APLICACIÓN ==========
        st.markdown('<div class="section-header"><h2>🎮 Uso por Aplicación</h2></div>', unsafe_allow_html=True)
    
        apps_info = {
        "Diagnóstico Empresarial": {"emoji": "💼", "color": "#8B7BC8"},
        "Generador de Superhéroes": {"emoji": "🦸", "color": "#FF6B5A"},
        "Generador de Brainrot Italiano": {"emoji": "🍝", "color": "#FF9800"},
        # "Juego IA": {"emoji": "🎮", "color": "#4CAF50"},  # COMENTADO - Juego para niños deshabilitado
        "Juego de Lógica": {"emoji": "🧩", "color": "#2196F3"}
        }
    
        for app_name, info in apps_info.items():
            total_inicios_app = inicios.get(app_name, 0)
        total_completados_app = completados.get(app_name, 0)
        tasa_app = (total_completados_app / total_inicios_app * 100) if total_inicios_app > 0 else 0
        
        col_a, col_b, col_c = st.columns([1, 1, 2])
        
        with col_a:
            st.markdown(f"""
            <div class="stat-card">
                <h3>{info['emoji']} {app_name}</h3>
                <p style="font-size: 1.2rem; color: {info['color']}; font-weight: 600; margin: 0.5rem 0;">Inicios: {total_inicios_app}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Completados</h3>
                <p style="font-size: 1.2rem; color: {info['color']}; font-weight: 600; margin: 0.5rem 0;">{total_completados_app}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown(f"""
            <div class="stat-card">
                <h3>Tasa de Completado</h3>
                <div style="background: {info['color']}20; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                    <div style="background: {info['color']}; width: {tasa_app}%; height: 30px; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;">
                        {tasa_app:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # ========== ESTADÍSTICAS DE JUEGOS ==========
        st.markdown('<div class="section-header"><h2>🎯 Estadísticas de Juegos</h2></div>', unsafe_allow_html=True)
    
        # JUEGO IA - COMENTADO (juego para niños deshabilitado temporalmente)
        # col_j1, col_j2 = st.columns(2)
        # 
        # with col_j1:
        #     total_partidas_ia = stats.get('total_partidas_juego_ia', 0)
        #     promedio_ia = stats.get('promedio_aciertos_juego_ia', 0)
        #     
        #     st.markdown("""
        #     <div class="stat-card">
        #         <h3>🎮 Juego IA - ¿Foto Real o IA?</h3>
        #         <p style="font-size: 1.5rem; color: #4CAF50; font-weight: 600; margin: 0.5rem 0;">
        #             Partidas: <strong>{}</strong>
        #         </p>
        #         <p style="font-size: 1.2rem; color: #666; margin: 0.5rem 0;">
        #             Promedio de aciertos: <strong>{:.1f}%</strong>
        #         </p>
        #     </div>
        #     """.format(total_partidas_ia, promedio_ia), unsafe_allow_html=True)
    
        # Solo mostrar Juego de Lógica
        col_j2 = st.columns(1)[0]
        with col_j2:
            interacciones_logica = stats.get('interacciones_por_app', {}).get('Juego de Lógica', 0)
        
        st.markdown("""
        <div class="stat-card">
            <h3>🧩 Juego de Lógica</h3>
            <p style="font-size: 1.5rem; color: #2196F3; font-weight: 600; margin: 0.5rem 0;">
                Partidas: <strong>{}</strong>
            </p>
            <p style="font-size: 1rem; color: #666; margin: 0.5rem 0;">
                Inteligencia Natural en acción
            </p>
        </div>
        """.format(interacciones_logica), unsafe_allow_html=True)
    
        # ========== LEADS EMPRESARIALES ==========
        st.markdown('<div class="section-header"><h2>💼 Leads Empresariales</h2></div>', unsafe_allow_html=True)
    
        total_leads_empresariales = stats.get('total_leads_empresariales', 0)
    
        if total_leads_empresariales > 0:
            col_l1, col_l2 = st.columns(2)
            
            with col_l1:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>📧 Total de Leads</h3>
                    <p class="number">{total_leads_empresariales}</p>
                </div>
                """, unsafe_allow_html=True)
                
                empresas_por_tamano = stats.get('empresas_por_tamano', {})
                if empresas_por_tamano:
                    st.markdown("#### Por Tamaño:")
                    for tamano, cantidad in empresas_por_tamano.items():
                        porcentaje = (cantidad / total_leads_empresariales * 100)
                        st.progress(porcentaje / 100)
                        st.caption(f"{tamano}: {cantidad} ({porcentaje:.1f}%)")
            
            with col_l2:
                empresas_por_tipo = stats.get('empresas_por_tipo', {})
                if empresas_por_tipo:
                    st.markdown("#### Por Tipo de Negocio:")
                    for tipo, cantidad in empresas_por_tipo.items():
                        porcentaje = (cantidad / total_leads_empresariales * 100)
                        st.progress(porcentaje / 100)
                        st.caption(f"{tipo}: {cantidad} ({porcentaje:.1f}%)")
        else:
            st.info("📭 Aún no hay leads empresariales registrados")
    
        # ========== SUPERHÉROES ==========
        st.markdown('<div class="section-header"><h2>🦸 Generador de Superhéroes</h2></div>', unsafe_allow_html=True)
    
        col_s1, col_s2, col_s3 = st.columns(3)
    
        total_superheroes = stats.get('total_superheroes_generados', 0)
        total_leads_generales = stats.get('total_leads_generales', 0)
    
        with col_s1:
            st.markdown(f"""
        <div class="stat-card">
            <h3>Total Generados</h3>
            <p class="number">{total_superheroes}</p>
        </div>
        """, unsafe_allow_html=True)
    
        with col_s2:
            st.markdown(f"""
        <div class="stat-card">
            <h3>Con Email</h3>
            <p class="number">{total_leads_generales}</p>
        </div>
        """, unsafe_allow_html=True)
    
        with col_s3:
            tasa_email = (total_leads_generales / total_superheroes * 100) if total_superheroes > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <h3>Tasa de Captura</h3>
            <p class="number">{tasa_email:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
        # ========== RECURSOS Y COSTOS ==========
        st.markdown('<div class="section-header"><h2>⚙️ Recursos y Costos</h2></div>', unsafe_allow_html=True)
    
        col_r1, col_r2 = st.columns(2)
    
        with col_r1:
            total_tokens = stats.get('total_tokens_usados', 0)
        st.markdown(f"""
        <div class="stat-card">
            <h3>🔢 Tokens Usados</h3>
            <p class="number">{total_tokens:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
        with col_r2:
            if total_tokens > 0:
                # Estimación de costo (GPT-4o-mini: ~$0.0006 por 1K tokens de salida, ~$0.00015 por entrada)
                # Usamos promedio de $0.0004 por 1K tokens (mix entrada/salida)
                costo_estimado = (total_tokens / 1000) * 0.0004
                st.markdown(f"""
                <div class="stat-card">
                    <h3>💰 Costo Estimado</h3>
                    <p class="number">${costo_estimado:.2f}</p>
                    <p style="font-size: 0.8rem; color: #666; margin: 0.5rem 0 0 0;">USD (GPT-4o-mini)</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="stat-card">
                    <h3>💰 Costo Estimado</h3>
                    <p class="number">$0.00</p>
                </div>
                """, unsafe_allow_html=True)
    
        # ========== PESTAÑAS PARA LEADS ==========
        st.markdown("---")
        st.markdown('<div class="section-header"><h2>📋 Leads Detallados</h2></div>', unsafe_allow_html=True)
    
        tab1, tab2 = st.tabs(["💼 Leads Empresariales", "🦸 Leads Generales"])
    
        with tab1:
            leads_empresariales = db.get_leads_empresariales()
        
        if leads_empresariales:
            st.success(f"📊 Total: {len(leads_empresariales)} leads empresariales")
            
            # Filtros
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtro_tamano = st.selectbox(
                    "Filtrar por tamaño",
                    ["Todos"] + list(set([lead['tamano_empresa'] for lead in leads_empresariales]))
                )
            with col_f2:
                filtro_tipo = st.selectbox(
                    "Filtrar por tipo",
                    ["Todos"] + list(set([lead['tipo_negocio'] for lead in leads_empresariales]))
                )
            
            # Aplicar filtros
            leads_filtrados = leads_empresariales
            if filtro_tamano != "Todos":
                leads_filtrados = [l for l in leads_filtrados if l['tamano_empresa'] == filtro_tamano]
            if filtro_tipo != "Todos":
                leads_filtrados = [l for l in leads_filtrados if l['tipo_negocio'] == filtro_tipo]
            
            st.info(f"Mostrando {len(leads_filtrados)} de {len(leads_empresariales)} leads")
            
            # Mostrar leads
            for i, lead in enumerate(leads_filtrados, 1):
                with st.expander(f"📧 {lead['nombre']} - {lead['empresa']} ({lead['email']})", expanded=False):
                    col_l1, col_l2 = st.columns(2)
                    
                    with col_l1:
                        st.markdown(f"**👤 Nombre:** {lead['nombre']}")
                        st.markdown(f"**📧 Email:** {lead['email']}")
                        st.markdown(f"**🏢 Empresa:** {lead['empresa']}")
                        if lead['telefono']:
                            st.markdown(f"**📱 Teléfono:** {lead['telefono']}")
                    
                    with col_l2:
                        st.markdown(f"**💼 Tipo de negocio:** {lead['tipo_negocio']}")
                        st.markdown(f"**👥 Tamaño:** {lead['tamano_empresa']}")
                        st.markdown(f"**💰 Presupuesto:** {lead['presupuesto_tecnologico']}")
                        st.markdown(f"**📅 Fecha:** {lead['fecha_registro'][:10]}")
                        seguimiento = "✅ Realizado" if lead['seguimiento_realizado'] else "⏳ Pendiente"
                        st.markdown(f"**📊 Seguimiento:** {seguimiento}")
                    
                    if lead['desafio_principal']:
                        st.markdown("---")
                        st.markdown(f"**🎯 Desafío principal:**")
                        st.info(lead['desafio_principal'])
                    
                    if lead['procesos_repetitivos']:
                        try:
                            procesos = json.loads(lead['procesos_repetitivos']) if isinstance(lead['procesos_repetitivos'], str) else lead['procesos_repetitivos']
                            st.markdown(f"**⚙️ Procesos repetitivos:** {', '.join(procesos) if isinstance(procesos, list) else procesos}")
                        except:
                            st.markdown(f"**⚙️ Procesos repetitivos:** {lead['procesos_repetitivos']}")
        else:
            st.info("📭 Aún no hay leads empresariales registrados")
    
        with tab2:
            leads_generales = db.get_leads_generales()
        
        if leads_generales:
            st.success(f"📊 Total: {len(leads_generales)} leads con email")
            
            # Mostrar leads
            for i, lead in enumerate(leads_generales, 1):
                with st.expander(f"🦸 {lead['nombre']} ({lead['email']})", expanded=False):
                    col_g1, col_g2 = st.columns(2)
                    
                    with col_g1:
                        st.markdown(f"**👤 Nombre:** {lead['nombre']}")
                        st.markdown(f"**📧 Email:** {lead['email']}")
                        st.markdown(f"**💼 Profesión:** {lead['profesion']}")
                        st.markdown(f"**🎨 Hobby:** {lead['hobby']}")
                    
                    with col_g2:
                        st.markdown(f"**🌟 Rasgo dominante:** {lead['rasgo_dominante']}")
                        st.markdown(f"**🎭 Estilo preferido:** {lead['estilo_preferido']}")
                        recibir = "✅ Sí" if lead['recibir_por_email'] else "❌ No"
                        st.markdown(f"**📧 Recibir por email:** {recibir}")
                        st.markdown(f"**📅 Fecha:** {lead['fecha_registro'][:10]}")
                    
                    if lead['descripcion_superheroe']:
                        st.markdown("---")
                        st.markdown("**🦸 Superhéroe generado:**")
                        st.info(lead['descripcion_superheroe'][:500] + "..." if len(lead['descripcion_superheroe']) > 500 else lead['descripcion_superheroe'])
        else:
            st.info("📭 Aún no hay leads generales con email registrados")
    
        # ========== ACCIONES ==========
        st.markdown("---")
    
        # Funciones para generar CSV en memoria
        def generar_csv_empresariales():
            """Genera CSV de leads empresariales en memoria"""
        leads = db.get_leads_empresariales()
        
        if not leads:
            return None
        
        output = StringIO()
        fieldnames = ['id', 'email', 'nombre', 'empresa', 'telefono', 'tipo_negocio',
                     'tamano_empresa', 'desafio_principal', 'procesos_repetitivos',
                     'presupuesto_tecnologico', 'fecha_registro', 'seguimiento_realizado']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for lead in leads:
            row = {
                'id': lead['id'],
                'email': lead['email'],
                'nombre': lead['nombre'],
                'empresa': lead['empresa'],
                'telefono': lead['telefono'] or '',
                'tipo_negocio': lead['tipo_negocio'],
                'tamano_empresa': lead['tamano_empresa'],
                'desafio_principal': lead['desafio_principal'] or '',
                'procesos_repetitivos': lead['procesos_repetitivos'] or '',
                'presupuesto_tecnologico': lead['presupuesto_tecnologico'],
                'fecha_registro': lead['fecha_registro'],
                'seguimiento_realizado': 'Sí' if lead['seguimiento_realizado'] else 'No'
            }
            writer.writerow(row)
        
        return output.getvalue()
    
        def generar_csv_generales():
            """Genera CSV de leads generales en memoria"""
        leads = db.get_leads_generales()
        
        if not leads:
            return None
        
        output = StringIO()
        fieldnames = ['id', 'email', 'nombre', 'profesion', 'hobby', 'rasgo_dominante',
                     'estilo_preferido', 'recibir_por_email', 'fecha_registro']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for lead in leads:
            row = {
                'id': lead['id'],
                'email': lead['email'],
                'nombre': lead['nombre'],
                'profesion': lead['profesion'],
                'hobby': lead['hobby'],
                'rasgo_dominante': lead['rasgo_dominante'],
                'estilo_preferido': lead['estilo_preferido'],
                'recibir_por_email': 'Sí' if lead['recibir_por_email'] else 'No',
                'fecha_registro': lead['fecha_registro']
            }
            writer.writerow(row)
        
        return output.getvalue()
    
        # Botones de acción
        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    
        with col_act1:
            if st.button("🔄 Actualizar Estadísticas", use_container_width=True):
                st.rerun()
        
        with col_act2:
            csv_empresariales = generar_csv_empresariales()
            if csv_empresariales:
                fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="📥 Exportar Leads Empresariales",
                    data=csv_empresariales,
                    file_name=f"leads_empresariales_{fecha}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("📥 Exportar Leads Empresariales", disabled=True, use_container_width=True)
        
        with col_act3:
            csv_generales = generar_csv_generales()
            if csv_generales:
                fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="🦸 Exportar Leads Generales",
                    data=csv_generales,
                    file_name=f"leads_generales_{fecha}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("🦸 Exportar Leads Generales", disabled=True, use_container_width=True)
        
        with col_act4:
            if st.button("🏠 Volver al Portal", use_container_width=True):
                if 'is_unified_app' in st.session_state:
                    st.session_state.pagina_actual = 'home'
                    st.rerun()
    
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>📊 Dashboard de Estadísticas | Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p style="font-size: 0.9rem;">Powered by Inapsis</p>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error al cargar estadísticas: {str(e)}")
        st.info("💡 Asegúrate de que la base de datos esté inicializada correctamente")

# Para ejecución standalone
if __name__ == "__main__" or ('is_unified_app' not in st.session_state or 
                               st.session_state.get('is_unified_app') is None):
    # Configuración de página solo si no está en modo unificado
    if 'is_unified_app' not in st.session_state:
        st.set_page_config(
            page_title="Estadísticas - Inapsis",
            page_icon="📊",
            layout="wide"
        )
    run_estadisticas_app()

