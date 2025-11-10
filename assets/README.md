# Assets de Inapsis IA

Esta carpeta contiene los recursos visuales del sistema de aplicaciones IA de Inapsis.

## 🎨 Paleta de Colores Oficial

Basada en el logo de Inapsis:

### Colores Principales

- **Púrpura Inapsis**: `#8B7BC8` (rgb(139, 123, 200))
  - Color principal usado en "Ina"
  - Usado en gradientes, bordes y elementos de marca
  
- **Coral Inapsis**: `#FF6B5A` (rgb(255, 107, 90))
  - Color de acento usado en "psis"
  - Usado en botones, highlights y elementos interactivos

### Colores Secundarios

- **Negro/Oscuro**: `#1a1a1a` (rgb(26, 26, 26))
  - Fondos oscuros y textos principales
  
- **Gris Claro**: `#f8f9fa` (rgb(248, 249, 250))
  - Fondos de tarjetas y secciones
  
- **Gris Texto**: `#666666` (rgb(102, 102, 102))
  - Textos secundarios y subtítulos
  
- **Blanco**: `#ffffff` (rgb(255, 255, 255))
  - Fondos principales y textos sobre fondos oscuros

## 🌈 Gradientes Utilizados

### Gradiente Principal (Púrpura → Coral)
```css
background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
```
**Uso**: Headers, botones principales, sidebar

### Gradiente Suave (Fondos)
```css
background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
```
**Uso**: Tarjetas, cajas de información, fondos sutiles

## 📁 Archivos en esta Carpeta

### `inapsis_logo.png`
Logo oficial de Inapsis
- **Formato**: PNG con fondo transparente
- **Uso**: Portal principal, sidebar de app unificada
- **Dimensiones recomendadas**: 300-500px de ancho

### `inapsis_styles.py`
Módulo Python con:
- Paleta de colores en constantes
- CSS común para todas las aplicaciones
- Funciones helper para generar componentes estilizados

## 🎯 Guía de Uso

### Guardar el Logo

Para reemplazar el placeholder del logo con el archivo real:

1. Guarda la imagen del logo como `inapsis_logo.png` en esta carpeta
2. Asegúrate que tenga fondo transparente (PNG)
3. El logo se mostrará automáticamente en:
   - Portal principal (`main_menu.py`)
   - Sidebar de la app unificada (`app_unificada.py`)

### Aplicar Estilos Consistentes

Para mantener consistencia visual en todas las apps:

```python
# Usar los gradientes de Inapsis
st.markdown("""
    <style>
    .custom-element {
        background: linear-gradient(135deg, #8B7BC8 0%, #FF6B5A 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)
```

## 📐 Especificaciones de Diseño

### Headers
- Gradiente: Púrpura → Coral (135deg)
- Border-radius: 15px
- Box-shadow: `0 4px 15px rgba(255, 107, 90, 0.3)`
- Padding: 2.5rem 1rem

### Tarjetas (Cards)
- Background: Gradiente suave (10% opacity)
- Border-left: 4px solid con color Inapsis
- Border-radius: 12px
- Hover: Transform translateX(8px)

### Botones
- Background: Gradiente Púrpura → Coral
- Border-radius: 8px
- Padding: 0.75rem 2rem
- Hover: Transform translateY(-2px) + box-shadow

### Sidebar
- Background: Gradiente vertical Púrpura → Coral
- Botones: rgba(255, 255, 255, 0.2) con border blanco

## 🚀 Próximos Pasos

1. ✅ Aplicar paleta a todas las aplicaciones
2. ✅ Integrar logo en interfaces principales
3. ⏳ Crear favicon basado en el logo
4. ⏳ Optimizar logo para diferentes tamaños (responsive)
5. ⏳ Crear variante del logo para fondos claros

---

**Nota**: Mantén esta paleta de colores en todos los componentes nuevos para garantizar consistencia visual con la marca Inapsis.

