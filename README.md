# 🧠 Sistema de Aplicaciones IA - Inapsis

Sistema de aplicaciones interactivas con IA deployado en Azure con CI/CD automático mediante GitHub Actions.

## 🎯 Características

- **💼 Diagnóstico Empresarial**: Chat inteligente que analiza negocios y sugiere automatizaciones
- **👤 Gemelo IA**: Generador de perfiles personalizados con IA
- **🎮 Juego IA**: Actividad interactiva "¿Persona o IA?"

---

## 📂 Estructura del Proyecto

```
ejemplos_expo/
│
├── ☁️ azure/                      → Configuración Azure
│   ├── startup_single.sh         → Script de inicio
│   ├── Dockerfile                → Docker config
│   ├── SETUP_PORTAL_WEB.md       → ⭐ Guía completa
│   └── README_AZURE.md           → Resumen rápido
│
├── 🎨 Aplicaciones
│   ├── app_unificada.py          → App integrada (todas en una)
│   ├── main_menu.py              → Portal principal
│   ├── diagnostico/app.py        → Diagnóstico empresarial
│   ├── gemelo/app.py             → Generador de gemelo IA
│   └── juego/app.py              → Juego interactivo
│
├── 🖼️ Assets
│   ├── inapsis_logo.png          → Logo de Inapsis
│   ├── inapsis_styles.py         → Paleta y estilos
│   ├── README.md                 → Guía de estilos
│   └── INSTRUCCIONES_LOGO.txt    → Cómo usar el logo
│
├── 🛠️ Utilidades
│   └── utils/
│       ├── openai_client.py      → Cliente OpenAI
│       └── db.py                 → Base de datos SQLite
│
├── ⚙️ Configuración
│   ├── requirements.txt          → Dependencias Python
│   └── env_template              → Template de variables
│
└── 🤖 CI/CD
    └── .github/workflows/
        └── azure-single-app.yml  → GitHub Actions
```

---

## 🎨 Diseño Visual

El sistema utiliza la **paleta de colores oficial de Inapsis**, basada en el logo corporativo:

### Colores de Marca
- **🟣 Púrpura Inapsis**: `#8B7BC8` - Color principal
- **🧡 Coral Inapsis**: `#FF6B5A` - Color de acento

### Características Visuales
- ✨ **Gradientes**: Transiciones suaves entre púrpura y coral
- 🎯 **Animaciones**: Efectos hover y transiciones fluidas
- 📱 **Responsive**: Adaptado a todos los dispositivos
- 🖼️ **Logo integrado**: Aparece en portal principal y sidebar

### Personalizar
Para modificar estilos y ver la paleta completa, consulta:
- 📄 `assets/README.md` - Guía completa de estilos
- 🎨 `assets/inapsis_styles.py` - Módulo de estilos Python
- 📝 `CAMBIOS_VISUALES.md` - Documentación de cambios visuales

**Nota**: Para usar el logo real de Inapsis, guarda la imagen como `assets/inapsis_logo.png` (ver `assets/INSTRUCCIONES_LOGO.txt`).

---

## 🧪 Probar Localmente (Antes de Desplegar)

Para probar todo el sistema en tu equipo antes de desplegar a Azure:

### Setup inicial

1. **Clonar el repositorio**
```bash
git clone <tu-repo>
cd ejemplos_expo
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar OpenAI API Key**
```bash
cp env_template .env
# Editar .env y añadir tu OPENAI_API_KEY
```

### Ejecutar aplicación unificada

```bash
streamlit run app_unificada.py
```

Esto abrirá la aplicación en `http://localhost:8501` con:
- ✅ Las 3 aplicaciones integradas (Diagnóstico, Gemelo, Juego)
- ✅ Navegación por sidebar
- ✅ Exactamente como se verá en Azure

### Ejecutar apps individuales (opcional)

Si prefieres probar las apps por separado:

```bash
# Portal principal
streamlit run main_menu.py

# Apps individuales
streamlit run diagnostico/app.py
streamlit run gemelo/app.py
streamlit run juego/app.py
```

---

## 🚀 Deployment en Azure (CI/CD Automático)

### Setup desde el Portal Web (15 minutos)

**📖 Guía completa:** [`azure/SETUP_PORTAL_WEB.md`](azure/SETUP_PORTAL_WEB.md)

### Pasos resumidos:

#### 1️⃣ Crear Web App en Azure Portal

1. Ve a https://portal.azure.com
2. **Create a resource** → **Web App**
3. Configurar:
   - Resource Group: `inapsis-ia-rg` (nuevo)
   - Name: `inapsis-ia-app`
   - Runtime: Python 3.11, Linux
   - Plan: Basic B1 ($13/mes)

#### 2️⃣ Configurar variables en el portal

1. Tu Web App → **Configuration** → **Application settings**
2. **New application setting:**
   - Name: `OPENAI_API_KEY`
   - Value: tu clave de OpenAI
3. **Save**

#### 3️⃣ Configurar startup command

1. **Configuration** → **General settings**
2. **Startup Command:** `startup_single.sh`
3. **Save**

#### 4️⃣ Obtener publish profile

1. En tu Web App, click **"Get publish profile"**
2. Abre el archivo descargado
3. Copia TODO el contenido

#### 5️⃣ Configurar GitHub Secret

1. Tu repositorio en GitHub → **Settings** → **Secrets** → **Actions**
2. **New repository secret:**
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: Pegar contenido del publish profile
3. **Add secret**

#### 6️⃣ Push y deploy automático

```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

¡GitHub Actions despliega automáticamente! 🎉

**Ver progreso:** Pestaña "Actions" en GitHub

---

## 🌐 URLs de Acceso

### Portal Principal
```
https://ejemplos-ia.azurewebsites.net
```
(Reemplaza `ejemplos-ia` con el nombre de tu Web App)

### 📊 Dashboard de Estadísticas (Acceso Privado)
```
https://ejemplos-ia.azurewebsites.net/?pagina_actual=estadisticas
```

**Nota:** El dashboard de estadísticas solo es accesible mediante esta URL directa. No aparece en el menú de navegación para mantenerlo privado.

---

## 💰 Costos

| Concepto | Costo/mes |
|----------|-----------|
| Azure App Service B1 | $13 |
| OpenAI API | $5-20 |
| **Total** | **$18-33** |

💡 **Azure Free Tier:** Nuevas cuentas reciben $200 créditos por 30 días

---

## 🔄 Flujo de Trabajo Diario

```bash
# 1. Editar código en tu editor
# 2. Commit y push
git add .
git commit -m "Descripción de cambios"
git push origin main

# 3. GitHub Actions despliega automáticamente (3-5 min)
# 4. Verificar en: https://tu-app.azurewebsites.net
```

---

## 🛠️ Gestión desde el Portal Web

### Ver logs en tiempo real
1. portal.azure.com → Tu Web App
2. **Monitoring** → **Log stream**

### Reiniciar aplicación
1. Tu Web App → **Overview**
2. Click **Restart**

### Ver configuración
1. Tu Web App → **Configuration**
2. Ver todas las application settings

### Ver deployments
- **Azure:** Tu Web App → **Deployment Center**
- **GitHub:** Pestaña **Actions**

### Troubleshooting automático
1. Tu Web App → **Diagnose and solve problems**
2. Herramientas de diagnóstico inteligentes

---

## 🔧 Troubleshooting

### Build falla en GitHub Actions
1. GitHub → **Actions** → Click workflow fallido
2. Ver logs detallados
3. Verificar secret `AZURE_WEBAPP_PUBLISH_PROFILE`

### App no carga
1. Azure Portal → **Log stream**
2. Ver errores en tiempo real
3. **Restart** si es necesario

### Error de API Key
1. **Configuration** → **Application settings**
2. Verificar `OPENAI_API_KEY`
3. **Save** y **Restart**

---

## 📊 Monitoreo (Opcional)

### Habilitar Application Insights

1. Tu Web App → **Application Insights**
2. **Turn on Application Insights**
3. Seguir instrucciones

Obtendrás:
- Requests y respuestas
- Tiempos de carga
- Errores automáticos
- Dependencias (OpenAI)

---

## 🎨 Personalización

### Cambiar plan de App Service

1. Tu Web App → **Scale up (App Service plan)**
2. Seleccionar:
   - **F1** - Gratis (limitado, para testing)
   - **B1** - $13/mes (actual)
   - **B2** - $26/mes (más potente)
   - **P1V2** - $90/mes (producción)

### Configurar dominio personalizado

1. Tu Web App → **Custom domains**
2. **Add custom domain**
3. Seguir instrucciones DNS

### Ajustar configuración de IA

Editar `utils/openai_client.py`:

```python
def chat_completion(self, messages, 
                   model="gpt-3.5-turbo",     # Cambiar modelo
                   temperature=0.7,            # Creatividad (0-2)
                   max_tokens=500):            # Límite respuesta
```

---

## 📚 Documentación Detallada

| Guía | Descripción | Tiempo |
|------|-------------|--------|
| [`azure/SETUP_PORTAL_WEB.md`](azure/SETUP_PORTAL_WEB.md) | ⭐ Guía completa paso a paso | 15 min |
| [`azure/README_AZURE.md`](azure/README_AZURE.md) | Resumen ejecutivo | 5 min |

---

## ✅ Checklist de Deployment

- [ ] Cuenta de Azure activa
- [ ] Web App creada en portal.azure.com
- [ ] Runtime: Python 3.11, Linux
- [ ] Plan: B1 (o el que prefieras)
- [ ] `OPENAI_API_KEY` configurada
- [ ] Startup command: `startup_single.sh`
- [ ] Publish profile descargado
- [ ] Secret en GitHub configurado
- [ ] Código pusheado a `main`
- [ ] Workflow ejecutado ✅
- [ ] App funcionando

---

## 🎯 Tecnologías

- **Python 3.11** - Backend
- **Streamlit** - Framework web interactivo
- **OpenAI API** - GPT-3.5-turbo
- **SQLite** - Base de datos local
- **Azure App Service** - Hosting
- **GitHub Actions** - CI/CD automático

---

## 🔒 Seguridad y Privacidad

### Datos almacenados:
- Diagnóstico: tipo de negocio, respuestas, resultado
- Gemelo: nombre, edad, intereses, perfil generado
- Juego: aciertos, total, porcentaje

### NO se almacena:
- ❌ Direcciones IP
- ❌ Información sensible
- ❌ Cookies de tracking
- ❌ Datos bancarios

### Base de datos:
- Archivo: `evento_inapsis.db`
- Formato: SQLite
- Ubicación: En Azure (efímera) o local según config

---

## ✨ Características del Sistema

- ✅ **CI/CD automático** - Deploy en cada push
- ✅ **Escalabilidad** - Azure ajusta recursos
- ✅ **Monitoreo** - Logs y métricas en tiempo real
- ✅ **Seguridad** - HTTPS/SSL automático
- ✅ **Disponibilidad** - 24/7 global
- ✅ **Sin CLI** - Todo desde el navegador
- ✅ **Bajo mantenimiento** - Azure lo gestiona

---

## 🚀 Próximas Mejoras (Ideas)

- [ ] Generación de imágenes con DALL-E
- [ ] Dashboard avanzado con gráficos
- [ ] Multi-idioma (inglés, portugués)
- [ ] Exportar resultados en PDF
- [ ] Sistema de puntos/gamificación
- [ ] Integración con WhatsApp/Telegram
- [ ] Análisis de sentimiento

---

## 📞 Recursos Útiles

- **Azure Portal:** https://portal.azure.com
- **OpenAI Platform:** https://platform.openai.com
- **GitHub Actions:** Ver pestaña "Actions" en tu repo
- **Streamlit Docs:** https://docs.streamlit.io

---

## 📊 Verificación del Sistema

```bash
# Verificar archivos clave
ls azure/        # → startup_single.sh, app_unificada.py, SETUP_PORTAL_WEB.md
ls utils/        # → openai_client.py, db.py
ls */app.py      # → diagnostico, gemelo, juego

# Ver dependencias
cat requirements.txt

# Verificar workflow
ls .github/workflows/  # → azure-single-app.yml
```

---

## 🎉 ¡Listo para Producción!

Tu sistema está deployado en Azure con:

✅ **Configuración desde portal web** - Sin CLI  
✅ **CI/CD automático** - Deploy en cada push  
✅ **Una sola Web App** - $13/mes económico  
✅ **Gestión visual** - Todo desde navegador  
✅ **Escalable** - Ajusta según demanda  

---

**Desarrollado para:** Inapsis 🚀  
**Deployment:** Azure App Service + GitHub Actions  
**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025

---

**¿Listo para deployar?** → [`azure/SETUP_PORTAL_WEB.md`](azure/SETUP_PORTAL_WEB.md)
