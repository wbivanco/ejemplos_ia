"""Cliente para Pollinations.ai - Generación de Imágenes 100% GRATIS sin API Key"""
import requests
from io import BytesIO
from PIL import Image
import urllib.parse

class PollinationsClient:
    def __init__(self):
        # Pollinations.ai no requiere API key!
        self.base_url = "https://image.pollinations.ai/prompt"
        
    def generate_image(self, prompt, width=512, height=768):
        """
        Genera una imagen usando Pollinations.ai (100% gratis, sin API key)
        
        Args:
            prompt: Descripción de la imagen a generar
            width: Ancho de la imagen (default: 512)
            height: Alto de la imagen (default: 768 para superhéroes)
            
        Returns:
            Image object (PIL) o None si hay error
        """
        try:
            # Codificar el prompt para URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Construir URL con parámetros
            url = f"{self.base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true&enhance=true"
            
            # Hacer request - Pollinations genera la imagen on-the-fly
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                # Convertir bytes a imagen PIL
                image = Image.open(BytesIO(response.content))
                return image
            else:
                raise Exception(f"Error {response.status_code}: No se pudo generar la imagen")
                
        except requests.exceptions.Timeout:
            raise Exception("Timeout: La generación tardó demasiado. Intenta de nuevo.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al generar imagen: {str(e)}")
    
    def generate_superhero(self, nombre, profesion, hobby, estilo="comic"):
        """
        Genera una imagen de superhéroe basada en los datos
        
        Args:
            nombre: Nombre de la persona
            profesion: Profesión
            hobby: Hobby o pasión
            estilo: Estilo visual (descripción textual)
            
        Returns:
            PIL Image object
        """
        # Mapeo de estilos
        style_map = {
            "Cómico y divertido": "fun vibrant comic book style, colorful, cartoon superhero",
            "Épico y poderoso": "epic powerful superhero, dramatic cinematic lighting, heroic",
            "Misterioso y oscuro": "dark mysterious superhero, noir style, dramatic shadows",
            "Futurista y tecnológico": "futuristic sci-fi superhero, high-tech suit, neon cyberpunk"
        }
        
        style_desc = style_map.get(estilo, "comic book superhero style")
        
        # Prompt optimizado para superhéroes - más simple y directo
        prompt = f"""superhero character, {style_desc}, 
full body portrait, inspired by {profesion} and {hobby}, 
wearing colorful costume, heroic pose, cape, 
high quality digital art, vibrant colors, clean background"""
        
        return self.generate_image(prompt, width=512, height=768)
    
    def generate_brainrot(self, nombre_brainrot, animal_cosa, texto_italiano):
        """
        Genera una imagen de brainrot italiano basada en los datos
        
        Args:
            nombre_brainrot: Nombre del brainrot generado
            animal_cosa: Animal o cosa a incluir
            texto_italiano: Texto en italiano para incluir en la imagen
            
        Returns:
            PIL Image object
        """
        # Prompt optimizado para brainrot italiano
        prompt = f"""Italian brainrot meme style: {nombre_brainrot} with a {animal_cosa}, 
        Italian text: "{texto_italiano}", vibrant neon colors, absurd Italian meme style, 
        funny colorful composition, high quality, brainrot aesthetic, colorful background, 
        absurd and funny design, meme format, bright colors, Italian flag colors, 
        chaotic fun style, digital art"""
        
        return self.generate_image(prompt, width=512, height=512)


def get_pollinations_client():
    """Obtiene una instancia del cliente de Pollinations"""
    return PollinationsClient()

