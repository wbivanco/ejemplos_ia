#!/usr/bin/env python3
"""
Script para generar códigos QR a partir de URLs
Uso: python generar_qr.py <URL> [nombre_archivo] [--logo ruta_logo] [--color color]
"""

import sys
import qrcode
from pathlib import Path
from datetime import datetime
from PIL import Image
import argparse

def validar_color(color_str):
    """
    Valida y normaliza un color (hexadecimal o nombre)
    
    Args:
        color_str: Color en formato hex (#RRGGBB) o nombre de color
    
    Returns:
        Tupla RGB (r, g, b)
    """
    # Si es hexadecimal
    if color_str.startswith('#'):
        try:
            hex_color = color_str.lstrip('#')
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (r, g, b)
        except ValueError:
            pass
    
    # Colores predefinidos comunes
    colores_predefinidos = {
        'negro': (0, 0, 0),
        'black': (0, 0, 0),
        'azul': (0, 0, 255),
        'blue': (0, 0, 255),
        'rojo': (255, 0, 0),
        'red': (255, 0, 0),
        'verde': (0, 128, 0),
        'green': (0, 128, 0),
        'morado': (128, 0, 128),
        'purple': (128, 0, 128),
        'naranja': (255, 165, 0),
        'orange': (255, 165, 0),
        'rosa': (255, 192, 203),
        'pink': (255, 192, 203),
    }
    
    color_lower = color_str.lower()
    if color_lower in colores_predefinidos:
        return colores_predefinidos[color_lower]
    
    # Por defecto, negro
    return (0, 0, 0)

def agregar_logo(qr_img, logo_path, size_ratio=0.2):
    """
    Agrega un logo en el centro del código QR
    
    Args:
        qr_img: Imagen del código QR (PIL Image)
        logo_path: Ruta al archivo del logo
        size_ratio: Proporción del tamaño del logo respecto al QR (0.1 a 0.3 recomendado)
    
    Returns:
        Imagen PIL con el logo agregado
    """
    # Abrir y redimensionar logo
    logo = Image.open(logo_path)
    
    # Convertir a RGBA si tiene transparencia
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
    
    # Calcular tamaño del logo (20% del ancho del QR por defecto)
    qr_width, qr_height = qr_img.size
    logo_size = int(min(qr_width, qr_height) * size_ratio)
    
    # Redimensionar logo manteniendo aspecto
    logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Crear fondo blanco para el logo (para mejor visibilidad)
    logo_con_fondo = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 255))
    
    # Centrar logo en el fondo
    offset_x = (logo_size - logo.width) // 2
    offset_y = (logo_size - logo.height) // 2
    logo_con_fondo.paste(logo, (offset_x, offset_y), logo)
    
    # Calcular posición para centrar el logo en el QR
    pos_x = (qr_width - logo_size) // 2
    pos_y = (qr_height - logo_size) // 2
    
    # Pegar logo en el centro del QR
    qr_img.paste(logo_con_fondo, (pos_x, pos_y), logo_con_fondo)
    
    return qr_img

def buscar_logo(nombre_logo):
    """
    Busca el logo en la carpeta qr/
    
    Args:
        nombre_logo: Nombre del archivo del logo (con o sin extensión)
    
    Returns:
        Ruta completa al logo si existe, None si no se encuentra
    """
    carpeta_qr = Path("qr")
    
    if not carpeta_qr.exists():
        carpeta_qr.mkdir(parents=True, exist_ok=True)
        return None
    
    # Si ya tiene extensión, buscar directamente
    if Path(nombre_logo).suffix:
        logo_path = carpeta_qr / nombre_logo
        if logo_path.exists():
            return str(logo_path)
    else:
        # Buscar con extensiones comunes
        extensiones = ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']
        for ext in extensiones:
            logo_path = carpeta_qr / f"{nombre_logo}{ext}"
            if logo_path.exists():
                return str(logo_path)
    
    return None

def generar_qr(url, nombre_archivo=None, nombre_logo=None, color_fill=None, color_back=None):
    """
    Genera un código QR para una URL
    
    Args:
        url: URL para generar el código QR
        nombre_archivo: Nombre del archivo de salida (opcional)
        nombre_logo: Nombre del logo en la carpeta qr/ (opcional)
        color_fill: Color del código QR (hex o nombre, opcional)
        color_back: Color de fondo (hex o nombre, opcional)
    
    Returns:
        Ruta del archivo generado
    """
    # Validar URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Validar y convertir colores
    fill_color = validar_color(color_fill) if color_fill else (0, 0, 0)  # Negro por defecto
    back_color = validar_color(color_back) if color_back else (255, 255, 255)  # Blanco por defecto
    
    # Buscar logo en la carpeta qr/
    logo_path = None
    if nombre_logo:
        logo_path = buscar_logo(nombre_logo)
        if not logo_path:
            raise FileNotFoundError(
                f"El logo '{nombre_logo}' no se encontró en la carpeta 'qr/'. "
                f"Por favor, coloca el logo en la carpeta 'qr/' con ese nombre."
            )
    
    # Crear instancia de QRCode
    # Si hay logo, usar mayor corrección de errores para que el logo no rompa el código
    error_correction = qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_L
    
    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño del código (1-40)
        error_correction=error_correction,  # Mayor corrección si hay logo
        box_size=10,  # Tamaño de cada caja en píxeles
        border=4,  # Grosor del borde
    )
    
    # Agregar datos
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crear imagen con colores personalizados
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Agregar logo si se proporciona
    if logo_path:
        img = agregar_logo(img, logo_path)
    
    # Generar nombre de archivo si no se proporciona
    if not nombre_archivo:
        # Limpiar URL para nombre de archivo
        nombre_limpio = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        nombre_limpio = ''.join(c for c in nombre_limpio if c.isalnum() or c in ('_', '-', '.'))[:50]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"qr_{nombre_limpio}_{timestamp}.png"
    
    # Asegurar extensión .png
    if not nombre_archivo.endswith('.png'):
        nombre_archivo += '.png'
    
    # Guardar imagen
    img.save(nombre_archivo)
    
    return nombre_archivo

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Genera códigos QR a partir de URLs con opciones de personalización',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generar_qr.py https://inapsis.com.ar
  python generar_qr.py https://inapsis.com.ar --output mi_qr.png
  python generar_qr.py inapsis.com.ar --color "#8B7BC8"
  python generar_qr.py inapsis.com.ar --logo inapsis_logo --color "#FF6B5A"
  python generar_qr.py inapsis.com.ar --logo mi_logo.png --color azul --background blanco
  
Nota: Los logos deben estar en la carpeta 'qr/'
        """
    )
    
    parser.add_argument('url', help='URL para generar el código QR')
    parser.add_argument('--output', '-o', dest='nombre_archivo', 
                       help='Nombre del archivo de salida (opcional)')
    parser.add_argument('--logo', '-l', dest='nombre_logo',
                       help='Nombre del logo en la carpeta qr/ (opcional, ej: inapsis_logo.png o inapsis_logo)')
    parser.add_argument('--color', '-c', dest='color_fill',
                       help='Color del código QR (hexadecimal #RRGGBB o nombre: negro, azul, rojo, verde, morado, naranja, rosa)')
    parser.add_argument('--background', '-b', dest='color_back',
                       help='Color de fondo (hexadecimal #RRGGBB o nombre: blanco, negro, etc.)')
    
    args = parser.parse_args()
    
    try:
        print("=" * 60)
        print("🔲 GENERADOR DE CÓDIGOS QR")
        print("=" * 60)
        print(f"\n📎 URL: {args.url}")
        if args.nombre_logo:
            print(f"🖼️  Logo: {args.nombre_logo} (buscando en carpeta qr/)")
        if args.color_fill:
            print(f"🎨 Color: {args.color_fill}")
        if args.color_back:
            print(f"🎨 Fondo: {args.color_back}")
        print("\n⏳ Generando código QR...")
        
        archivo_generado = generar_qr(
            args.url, 
            args.nombre_archivo,
            args.nombre_logo,
            args.color_fill,
            args.color_back
        )
        
        print(f"\n✅ Código QR generado exitosamente!")
        print(f"📁 Archivo: {archivo_generado}")
        print(f"📂 Ubicación: {Path(archivo_generado).absolute()}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error al generar el código QR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

