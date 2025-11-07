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
            
            # Promedio de aciertos en el juego
            cursor.execute("""
                SELECT AVG(porcentaje) as promedio
                FROM juego_resultados
            """)
            promedio_juego = cursor.fetchone()[0] or 0
            
            # Total de tokens usados
            cursor.execute("""
                SELECT SUM(tokens_used) as total_tokens
                FROM interacciones
            """)
            total_tokens = cursor.fetchone()[0] or 0
            
            return {
                "interacciones_por_app": dict(interacciones),
                "promedio_aciertos_juego": round(promedio_juego, 2),
                "total_tokens_usados": total_tokens
            }

# Instancia global
def get_db():
    """Obtiene una instancia de la base de datos"""
    return EventDB()

