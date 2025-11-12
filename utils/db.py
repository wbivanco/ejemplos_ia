"""Gestión de base de datos SQLite para logs y resultados"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class EventDB:
    """Gestor de base de datos para el evento"""
    
    def __init__(self, db_path="evento_inapsis.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializa las tablas de la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla para interacciones generales
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_data TEXT,
                    result TEXT,
                    tokens_used INTEGER DEFAULT 0
                )
            """)
            
            # Tabla para el juego
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS juego_resultados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    aciertos INTEGER,
                    total INTEGER,
                    porcentaje REAL
                )
            """)
            
            # Tabla para leads empresariales (Diagnóstico Empresarial)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads_empresariales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    empresa TEXT NOT NULL,
                    telefono TEXT,
                    tipo_negocio TEXT NOT NULL,
                    tamano_empresa TEXT NOT NULL,
                    desafio_principal TEXT,
                    procesos_repetitivos TEXT,
                    presupuesto_tecnologico TEXT NOT NULL,
                    diagnostico_ia TEXT,
                    oportunidades_identificadas TEXT,
                    fecha_registro TEXT NOT NULL,
                    ip_address TEXT,
                    seguimiento_realizado INTEGER DEFAULT 0
                )
            """)
            
            # Tabla para leads generales (Generador de Superhéroes)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads_generales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    nombre TEXT NOT NULL,
                    profesion TEXT NOT NULL,
                    hobby TEXT NOT NULL,
                    rasgo_dominante TEXT NOT NULL,
                    estilo_preferido TEXT NOT NULL,
                    descripcion_superheroe TEXT,
                    recibir_por_email INTEGER DEFAULT 0,
                    fecha_registro TEXT NOT NULL
                )
            """)
            
            # Tabla para estadísticas de uso de apps
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estadisticas_uso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    accion TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    datos_adicionales TEXT
                )
            """)
            
            conn.commit()
    
    def log_interaccion(self, app_name, user_data=None, result=None, tokens_used=0):
        """
        Registra una interacción en la base de datos
        
        Args:
            app_name: Nombre de la aplicación
            user_data: Datos del usuario (dict o str)
            result: Resultado de la interacción
            tokens_used: Cantidad de tokens consumidos
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            user_data_str = json.dumps(user_data) if isinstance(user_data, dict) else user_data
            result_str = json.dumps(result) if isinstance(result, dict) else result
            
            cursor.execute("""
                INSERT INTO interacciones (app_name, timestamp, user_data, result, tokens_used)
                VALUES (?, ?, ?, ?, ?)
            """, (
                app_name,
                datetime.now().isoformat(),
                user_data_str,
                result_str,
                tokens_used
            ))
            
            conn.commit()
    
    def log_juego_resultado(self, aciertos, total):
        """Registra el resultado de un juego"""
        porcentaje = (aciertos / total * 100) if total > 0 else 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO juego_resultados (timestamp, aciertos, total, porcentaje)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().isoformat(), aciertos, total, porcentaje))
            conn.commit()
    
    def save_lead_empresarial(self, email, nombre, empresa, telefono, tipo_negocio, 
                              tamano_empresa, desafio_principal, procesos_repetitivos,
                              presupuesto_tecnologico, diagnostico_ia, oportunidades_identificadas,
                              ip_address=None):
        """
        Guarda un lead empresarial en la base de datos
        
        Args:
            email: Email del contacto (obligatorio, único)
            nombre: Nombre del contacto (obligatorio)
            empresa: Nombre de la empresa (obligatorio)
            telefono: Teléfono (opcional)
            tipo_negocio: Tipo de negocio
            tamano_empresa: Tamaño de la empresa
            desafio_principal: Desafío principal descrito
            procesos_repetitivos: Lista de procesos (JSON string)
            presupuesto_tecnologico: Nivel de presupuesto
            diagnostico_ia: Diagnóstico generado por IA
            oportunidades_identificadas: Oportunidades identificadas (JSON string)
            ip_address: Dirección IP (opcional)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convertir listas a JSON si es necesario
            procesos_str = json.dumps(procesos_repetitivos) if isinstance(procesos_repetitivos, list) else procesos_repetitivos
            oportunidades_str = json.dumps(oportunidades_identificadas) if isinstance(oportunidades_identificadas, list) else oportunidades_identificadas
            
            try:
                cursor.execute("""
                    INSERT INTO leads_empresariales 
                    (email, nombre, empresa, telefono, tipo_negocio, tamano_empresa,
                     desafio_principal, procesos_repetitivos, presupuesto_tecnologico,
                     diagnostico_ia, oportunidades_identificadas, fecha_registro, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    email, nombre, empresa, telefono, tipo_negocio, tamano_empresa,
                    desafio_principal, procesos_str, presupuesto_tecnologico,
                    diagnostico_ia, oportunidades_str, datetime.now().isoformat(), ip_address
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Email ya existe, actualizar registro existente
                cursor.execute("""
                    UPDATE leads_empresariales
                    SET nombre = ?, empresa = ?, telefono = ?, tipo_negocio = ?,
                        tamano_empresa = ?, desafio_principal = ?, procesos_repetitivos = ?,
                        presupuesto_tecnologico = ?, diagnostico_ia = ?,
                        oportunidades_identificadas = ?, fecha_registro = ?
                    WHERE email = ?
                """, (
                    nombre, empresa, telefono, tipo_negocio, tamano_empresa,
                    desafio_principal, procesos_str, presupuesto_tecnologico,
                    diagnostico_ia, oportunidades_str, datetime.now().isoformat(), email
                ))
                conn.commit()
                return True
    
    def save_lead_general(self, nombre, profesion, hobby, rasgo_dominante, estilo_preferido,
                          descripcion_superheroe, email=None, recibir_por_email=False):
        """
        Guarda un lead general (Generador de Superhéroes) en la base de datos
        
        Args:
            nombre: Nombre del usuario (obligatorio)
            profesion: Profesión (obligatorio)
            hobby: Hobby principal (obligatorio)
            rasgo_dominante: Rasgo dominante (obligatorio)
            estilo_preferido: Estilo preferido (obligatorio)
            descripcion_superheroe: Descripción del superhéroe generado
            email: Email del usuario (opcional)
            recibir_por_email: Si desea recibir el superhéroe por email
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO leads_generales 
                (email, nombre, profesion, hobby, rasgo_dominante, estilo_preferido,
                 descripcion_superheroe, recibir_por_email, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email, nombre, profesion, hobby, rasgo_dominante, estilo_preferido,
                descripcion_superheroe, 1 if recibir_por_email else 0, datetime.now().isoformat()
            ))
            conn.commit()
            return True
    
    def get_leads_empresariales(self):
        """Obtiene todos los leads empresariales"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM leads_empresariales
                ORDER BY fecha_registro DESC
            """)
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_leads_generales(self):
        """Obtiene todos los leads generales con email"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM leads_generales
                WHERE email IS NOT NULL AND email != ''
                ORDER BY fecha_registro DESC
            """)
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def log_uso_app(self, app_name, accion="inicio", datos_adicionales=None):
        """
        Registra el uso de una app (inicio, completado, etc.)
        
        Args:
            app_name: Nombre de la aplicación
            accion: Acción realizada (inicio, completado, cancelado, etc.)
            datos_adicionales: Datos adicionales en formato dict (se convierte a JSON)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            datos_str = json.dumps(datos_adicionales) if isinstance(datos_adicionales, dict) else datos_adicionales
            
            cursor.execute("""
                INSERT INTO estadisticas_uso (app_name, accion, timestamp, datos_adicionales)
                VALUES (?, ?, ?, ?)
            """, (
                app_name,
                accion,
                datetime.now().isoformat(),
                datos_str
            ))
            conn.commit()
    
    def get_stats(self):
        """Obtiene estadísticas generales del evento"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total de interacciones por app
            cursor.execute("""
                SELECT app_name, COUNT(*) as total
                FROM interacciones
                GROUP BY app_name
            """)
            interacciones = cursor.fetchall()
            
            # Estadísticas de uso por app
            cursor.execute("""
                SELECT app_name, accion, COUNT(*) as total
                FROM estadisticas_uso
                GROUP BY app_name, accion
            """)
            uso_stats = cursor.fetchall()
            
            # Total de inicios por app
            cursor.execute("""
                SELECT app_name, COUNT(*) as total
                FROM estadisticas_uso
                WHERE accion = 'inicio'
                GROUP BY app_name
            """)
            inicios_por_app = cursor.fetchall()
            
            # Total de completados por app
            cursor.execute("""
                SELECT app_name, COUNT(*) as total
                FROM estadisticas_uso
                WHERE accion = 'completado'
                GROUP BY app_name
            """)
            completados_por_app = cursor.fetchall()
            
            # Promedio de aciertos en el juego IA
            cursor.execute("""
                SELECT AVG(porcentaje) as promedio
                FROM juego_resultados
            """)
            promedio_juego_ia = cursor.fetchone()[0] or 0
            
            # Total de partidas completadas en Juego IA
            cursor.execute("""
                SELECT COUNT(*) FROM juego_resultados
            """)
            total_partidas_ia = cursor.fetchone()[0] or 0
            
            # Total de tokens usados
            cursor.execute("""
                SELECT SUM(tokens_used) as total_tokens
                FROM interacciones
            """)
            total_tokens = cursor.fetchone()[0] or 0
            
            # Total de leads empresariales
            cursor.execute("""
                SELECT COUNT(*) FROM leads_empresariales
            """)
            total_leads_empresariales = cursor.fetchone()[0] or 0
            
            # Total de leads generales con email
            cursor.execute("""
                SELECT COUNT(*) FROM leads_generales
                WHERE email IS NOT NULL AND email != ''
            """)
            total_leads_generales = cursor.fetchone()[0] or 0
            
            # Total de superhéroes generados (todos, con o sin email)
            cursor.execute("""
                SELECT COUNT(*) FROM leads_generales
            """)
            total_superheroes = cursor.fetchone()[0] or 0
            
            # Estadísticas de empresas por tamaño
            cursor.execute("""
                SELECT tamano_empresa, COUNT(*) as total
                FROM leads_empresariales
                GROUP BY tamano_empresa
            """)
            empresas_por_tamano = cursor.fetchall()
            
            # Estadísticas de empresas por tipo de negocio
            cursor.execute("""
                SELECT tipo_negocio, COUNT(*) as total
                FROM leads_empresariales
                GROUP BY tipo_negocio
            """)
            empresas_por_tipo = cursor.fetchall()
            
            return {
                "interacciones_por_app": dict(interacciones),
                "uso_por_app_accion": {f"{app}_{accion}": total for app, accion, total in uso_stats},
                "inicios_por_app": dict(inicios_por_app),
                "completados_por_app": dict(completados_por_app),
                "promedio_aciertos_juego_ia": round(promedio_juego_ia, 2),
                "total_partidas_juego_ia": total_partidas_ia,
                "total_tokens_usados": total_tokens,
                "total_leads_empresariales": total_leads_empresariales,
                "total_leads_generales": total_leads_generales,
                "total_superheroes_generados": total_superheroes,
                "empresas_por_tamano": dict(empresas_por_tamano),
                "empresas_por_tipo": dict(empresas_por_tipo)
            }

# Instancia global
def get_db():
    """Obtiene una instancia de la base de datos"""
    return EventDB()

