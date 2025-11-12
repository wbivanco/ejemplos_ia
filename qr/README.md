# 🔲 Generador de Códigos QR

Herramienta independiente y portable para generar códigos QR personalizados con logos y colores.

## 📦 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso Básico

```bash
# QR simple
python generar_qr.py https://inapsis.com.ar

# QR con color personalizado
python generar_qr.py https://inapsis.com.ar --color "#8B7BC8"

# QR con logo y color
python generar_qr.py https://inapsis.com.ar --logo mi_logo --color "#FF6B5A"

# QR completo: logo, color y fondo personalizado
python generar_qr.py inapsis.com.ar --logo mi_logo.png --color azul --background blanco

# Con nombre de archivo personalizado
python generar_qr.py inapsis.com.ar --logo mi_logo --color "#8B7BC8" --output mi_qr_personalizado.png
```

## 📋 Opciones Disponibles

- `url`: URL para generar el código QR (requerido)
- `--logo` o `-l`: Nombre del logo en esta carpeta (opcional)
- `--color` o `-c`: Color del código QR (hexadecimal `#RRGGBB` o nombre)
- `--background` o `-b`: Color de fondo (hexadecimal `#RRGGBB` o nombre)
- `--output` o `-o`: Nombre del archivo de salida (opcional)

## 🎨 Colores Disponibles

Puedes usar colores en formato hexadecimal (`#RRGGBB`) o por nombre:
- `negro` / `black`
- `azul` / `blue`
- `rojo` / `red`
- `verde` / `green`
- `morado` / `purple`
- `naranja` / `orange`
- `rosa` / `pink`

## 🖼️ Logos

Coloca tus logos en esta misma carpeta. El script los buscará automáticamente.

Puedes especificar el logo de dos formas:
- **Con extensión**: `--logo mi_logo.png`
- **Sin extensión**: `--logo mi_logo` (buscará automáticamente .png, .jpg, .jpeg, .svg, .gif, .webp)

### Formatos soportados
- PNG (recomendado, soporta transparencia)
- JPG/JPEG
- SVG
- GIF
- WebP

## 📝 Ejemplos

```bash
# Ejemplo 1: QR básico
python generar_qr.py https://inapsis.com.ar

# Ejemplo 2: QR con color corporativo
python generar_qr.py https://inapsis.com.ar --color "#8B7BC8"

# Ejemplo 3: QR con logo
python generar_qr.py https://inapsis.com.ar --logo inapsis_logo

# Ejemplo 4: QR completo personalizado
python generar_qr.py https://inapsis.com.ar --logo inapsis_logo --color "#8B7BC8" --background blanco --output qr_inapsis.png
```

## 🔧 Características Técnicas

- **Corrección de errores**: Si agregas un logo, el script usa corrección de errores alta (ERROR_CORRECT_H) para mantener la legibilidad
- **Tamaño del logo**: Se redimensiona automáticamente al 20% del tamaño del QR
- **Fondo del logo**: Se agrega un fondo blanco al logo para mejor visibilidad
- **Transparencia**: Soporta imágenes con transparencia (PNG con alpha)

## 📦 Portabilidad

Esta carpeta es completamente independiente. Puedes:
- Copiarla a otros proyectos
- Usarla como herramienta standalone
- Compartirla con otros desarrolladores

Solo necesitas instalar las dependencias con `pip install -r requirements.txt`

## 📁 Estructura

```
qr/
├── generar_qr.py      # Script principal
├── requirements.txt   # Dependencias
├── README.md          # Esta documentación
└── [tus_logos].png    # Logos que quieras usar
```

