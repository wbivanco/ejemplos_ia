"""Servicio de envío de emails usando Gmail SMTP"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class EmailService:
    """Servicio para enviar emails a través de Gmail SMTP"""
    
    def __init__(self):
        self.smtp_email = os.getenv("SMTP_EMAIL", "inapsis.info@gmail.com")
        smtp_password_raw = os.getenv("SMTP_PASSWORD")
        # Quitar espacios de la contraseña (Google la muestra con espacios pero SMTP no los acepta)
        self.smtp_password = smtp_password_raw.replace(" ", "") if smtp_password_raw else None
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not self.smtp_password:
            raise ValueError("SMTP_PASSWORD no encontrada en .env. Por favor configura tu contraseña de aplicación de Gmail.")
    
    def _crear_template_diagnostico(self, nombre, empresa, diagnostico, oportunidades):
        """Crea el template HTML para el email del diagnóstico"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 10px 10px 0 0;
                    margin: -30px -30px 30px -30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    margin: 20px 0;
                }}
                .diagnostico-box {{
                    background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #8B7BC8;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #f0f0f0;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                }}
                .cta-box {{
                    background: #fff3cd;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #ffc107;
                    margin: 20px 0;
                }}
                h2 {{
                    color: #8B7BC8;
                    margin-top: 25px;
                }}
                p {{
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💼 Tu Diagnóstico Empresarial</h1>
                </div>
                
                <div class="content">
                    <p>Hola <strong>{nombre}</strong>,</p>
                    
                    <p>Gracias por completar el diagnóstico empresarial para <strong>{empresa}</strong>.</p>
                    
                    <p>Como prometimos, aquí tienes tu diagnóstico completo generado con Inteligencia Artificial:</p>
                    
                    <div class="diagnostico-box">
                        {diagnostico.replace(chr(10), '<br>')}
                    </div>
                    
                    {f'<h2>🎯 Oportunidades Identificadas</h2><p>{oportunidades}</p>' if oportunidades else ''}
                    
                    <div class="cta-box">
                        <p><strong>💡 ¿Necesitas un análisis más profundo?</strong></p>
                        <p>Este diagnóstico gratuito te ha dado una visión general. Para mayor precisión y un plan de acción detallado, considera reservar una <strong>consulta profesional</strong> con nuestros expertos en transformación digital.</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Inapsis</strong> - Transformación Digital con IA</p>
                    <p>📧 inapsis.info@gmail.com | 🌐 <a href="https://inapsis.com.ar" style="color: #8B7BC8;">inapsis.com.ar</a></p>
                    <p style="font-size: 12px; color: #999; margin-top: 15px;">
                        Este email fue generado automáticamente. Si tienes preguntas, no dudes en contactarnos.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def enviar_diagnostico(self, email_destino, nombre, empresa, diagnostico, oportunidades=None):
        """
        Envía el diagnóstico empresarial por email
        
        Args:
            email_destino: Email del destinatario
            nombre: Nombre del destinatario
            empresa: Nombre de la empresa
            diagnostico: Texto del diagnóstico generado
            oportunidades: Texto con oportunidades identificadas (opcional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"💼 Tu Diagnóstico Empresarial - {empresa}"
            msg['From'] = self.smtp_email
            msg['To'] = email_destino
            
            # Crear versión HTML
            html_content = self._crear_template_diagnostico(nombre, empresa, diagnostico, oportunidades)
            
            # Crear versión texto plano (fallback)
            # Construir sección de oportunidades (si existe)
            oportunidades_section = ""
            if oportunidades:
                newline = "\n"  # Variable para evitar backslash en f-string
                oportunidades_section = f"Oportunidades Identificadas:{newline}{oportunidades}\n\n"
            
            text_content = f"""
Hola {nombre},

Gracias por completar el diagnóstico empresarial para {empresa}.

Tu Diagnóstico Empresarial:

{diagnostico}

{oportunidades_section}¿Necesitas un análisis más profundo?
Este diagnóstico gratuito te ha dado una visión general. Para mayor precisión y un plan de acción detallado, considera reservar una consulta profesional con nuestros expertos en transformación digital.

Inapsis - Transformación Digital con IA
📧 inapsis.info@gmail.com
🌐 https://inapsis.com.ar
            """
            
            # Adjuntar ambas versiones
            part1 = MIMEText(text_content, 'plain', 'utf-8')
            part2 = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Conectar y enviar
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Habilitar encriptación
            server.login(self.smtp_email, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            return True, "Email enviado exitosamente"
            
        except smtplib.SMTPAuthenticationError:
            return False, "Error de autenticación. Verifica tu contraseña de aplicación de Gmail."
        except smtplib.SMTPRecipientsRefused:
            return False, "El email de destino no es válido."
        except smtplib.SMTPServerDisconnected:
            return False, "Error de conexión con el servidor de email."
        except Exception as e:
            return False, f"Error al enviar email: {str(e)}"


def get_email_service():
    """Obtiene una instancia del servicio de email"""
    try:
        return EmailService()
    except ValueError as e:
        return None

