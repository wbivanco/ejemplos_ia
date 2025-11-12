"""Cliente simplificado para la API de OpenAI"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class OpenAIClient:
    """Cliente para interactuar con la API de OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en .env")
        self.client = OpenAI(api_key=self.api_key)
        # Leer modelo desde variable de entorno o usar default
        self.default_model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    
    def chat_completion(self, messages, model=None, temperature=0.7, max_tokens=500):
        """
        Genera una respuesta de chat usando OpenAI
        
        Args:
            messages: Lista de mensajes en formato OpenAI
            model: Modelo a usar (si es None, usa MODEL_NAME de .env o gpt-4o-mini por defecto)
            temperature: Creatividad de la respuesta (0-2)
            max_tokens: Máximo de tokens en la respuesta
            
        Returns:
            str: Respuesta del modelo
        """
        # Usar modelo pasado como parámetro, o el de la variable de entorno, o el default
        model_to_use = model if model else self.default_model
        
        try:
            response = self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al conectar con OpenAI: {str(e)}"
    
    def generate_image(self, prompt, size="1024x1024", quality="standard"):
        """
        Genera una imagen usando DALL-E
        
        Args:
            prompt: Descripción de la imagen
            size: Tamaño de la imagen (1024x1024, 1024x1792, 1792x1024)
            quality: Calidad (standard o hd)
            
        Returns:
            str: URL de la imagen generada
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            return None

# Instancia global para reutilizar
def get_openai_client():
    """Obtiene una instancia del cliente OpenAI"""
    return OpenAIClient()

