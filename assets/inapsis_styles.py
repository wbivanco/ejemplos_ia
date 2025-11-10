"""
Estilos y paleta de colores de Inapsis
Basado en el logo oficial de la empresa
"""

# Paleta de colores oficial de Inapsis
INAPSIS_COLORS = {
    'coral': '#FF6B5A',        # Color principal (naranja coral)
    'purple': '#8B7BC8',       # Color secundario (púrpura)
    'dark': '#1a1a1a',         # Negro/Gris oscuro
    'light': '#f8f9fa',        # Gris claro para fondos
    'text_gray': '#666666',    # Gris para textos secundarios
    'white': '#ffffff',
}

# CSS común para todas las aplicaciones
INAPSIS_CSS = f"""
<style>
    /* Estilos generales */
    .main-header {{
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, {INAPSIS_COLORS['purple']} 0%, {INAPSIS_COLORS['coral']} 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 90, 0.3);
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .main-header p {{
        font-size: 1.2rem;
        opacity: 0.95;
    }}
    
    /* Cards de aplicaciones */
    .app-card {{
        padding: 2rem;
        border-radius: 12px;
        background: white;
        border-left: 5px solid {INAPSIS_COLORS['coral']};
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .app-card:hover {{
        transform: translateX(8px);
        box-shadow: 0 4px 20px rgba(139, 123, 200, 0.2);
        border-left-color: {INAPSIS_COLORS['purple']};
    }}
    
    .app-card h3 {{
        color: {INAPSIS_COLORS['purple']};
        margin-bottom: 1rem;
    }}
    
    /* Botones personalizados */
    .stButton > button {{
        background: linear-gradient(135deg, {INAPSIS_COLORS['coral']} 0%, {INAPSIS_COLORS['purple']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 90, 0.4);
    }}
    
    /* Info boxes */
    .info-box {{
        background: linear-gradient(135deg, rgba(139, 123, 200, 0.1) 0%, rgba(255, 107, 90, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {INAPSIS_COLORS['purple']};
        margin: 1rem 0;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 3rem 0 2rem 0;
        color: {INAPSIS_COLORS['text_gray']};
        margin-top: 4rem;
        border-top: 2px solid {INAPSIS_COLORS['light']};
    }}
    
    .footer .brand {{
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {INAPSIS_COLORS['purple']} 0%, {INAPSIS_COLORS['coral']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {INAPSIS_COLORS['purple']} 0%, {INAPSIS_COLORS['coral']} 100%);
    }}
    
    [data-testid="stSidebar"] .element-container {{
        color: white;
    }}
    
    /* Métricas */
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-top: 3px solid {INAPSIS_COLORS['coral']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }}
    
    /* Logo container */
    .logo-container {{
        text-align: center;
        padding: 2rem 0;
    }}
    
    .logo-container img {{
        max-width: 300px;
        height: auto;
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
    }}
    
    .badge-coral {{
        background: {INAPSIS_COLORS['coral']};
        color: white;
    }}
    
    .badge-purple {{
        background: {INAPSIS_COLORS['purple']};
        color: white;
    }}
    
    /* Animaciones */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
</style>
"""

def get_logo_html(width="250px"):
    """Retorna el HTML para mostrar el logo de Inapsis"""
    return f"""
    <div class="logo-container fade-in">
        <img src="data:image/png;base64,{{LOGO_BASE64}}" width="{width}" alt="Inapsis Logo">
    </div>
    """

def get_header_html(title, subtitle=""):
    """Retorna el HTML para el header principal con estilos Inapsis"""
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    return f"""
    <div class="main-header fade-in">
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """

def get_footer_html():
    """Retorna el HTML para el footer con branding Inapsis"""
    return """
    <div class="footer">
        <p class="brand">Inapsis</p>
        <p style="font-size: 0.95rem; margin-top: 0.5rem;">Innovación aplicada a sistemas</p>
    </div>
    """

