# 🧠 Sistema de Aplicaciones IA - Inapsis

Sistema de aplicaciones interactivas con IA deployado en Azure con CI/CD automático mediante GitHub Actions.

## 🎯 Características

- **💼 Diagnóstico Empresarial**: Analiza negocios y genera diagnósticos personalizados con IA. Envía resultados por email automáticamente.
- **🦸 Generador de Superhéroes**: Crea superhéroes personalizados con poderes, origen e imagen generada por IA
- **🍝 Generador de Brainrot Italiano**: Crea memes absurdos con estilo italiano para niños (nombre, animal/cosa, texto italiano e imagen)
- **🧩 Juego de Lógica**: Desafíos de razonamiento lógico sin IA
- **📊 Dashboard de Estadísticas**: Visualiza métricas, leads y exporta datos a CSV (acceso privado)

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
│   ├── diagnostico/app.py        → Diagnóstico empresarial (con envío por email)
│   ├── gemelo/app.py             → Generador de superhéroes
│   ├── brainrot/app.py           → Generador de brainrot italiano
│   ├── logica/app.py             → Juego de lógica
│   ├── estadisticas/app.py       → Dashboard de estadísticas
│   └── juego/app.py              → Juego IA (comentado/deshabilitado)
│
├── 🖼️ Assets
│   ├── inapsis_logo.png          → Logo de Inapsis
│   └── imagenes/                 → Imágenes para juegos
│
├── 🛠️ Utilidades
│   └── utils/
│       ├── openai_client.py      → Cliente OpenAI
│       ├── db.py                 → Base de datos SQLite
│       ├── email_service.py      → Servicio de email (Gmail SMTP)
│       └── pollinations_client.py → Cliente Pollinations.ai (imágenes)
│
├── 🔲 QR Generator
│   └── qr/
│       ├── generar_qr.py         → Generador de códigos QR
│       ├── README.md             → Documentación QR
│       └── requirements.txt      → Dependencias QR
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

**Nota**: Para usar el logo real de Inapsis, guarda la imagen como `assets/inapsis_logo.png`.

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

4. **Configurar variables de entorno**
```bash
cp env_template .env
# Editar .env y añadir:
# - OPENAI_API_KEY (obligatorio)
# - MODEL_NAME (opcional, default: gpt-4o-mini)
# - SMTP_EMAIL y SMTP_PASSWORD (opcional, para envío de emails)
```

### 📧 Configuración de Email (Opcional)

Para habilitar el envío automático de diagnósticos por email desde `inapsis.info@gmail.com` usando Gmail SMTP:

#### Paso 1: Activar Verificación en 2 Pasos

1. Ve a tu cuenta de Google: https://myaccount.google.com/security
2. Inicia sesión con `inapsis.info@gmail.com`
3. Busca la sección **"Iniciar sesión en Google"**
4. Si **"Verificación en 2 pasos"** está desactivada:
   - Haz clic en **"Verificación en 2 pasos"**
   - Sigue las instrucciones para activarla
   - Puede pedirte confirmar tu teléfono

**⚠️ Importante:** La verificación en 2 pasos es **obligatoria** para generar contraseñas de aplicación.

#### Paso 2: Generar Contraseña de Aplicación

1. En la misma página de seguridad (https://myaccount.google.com/security)
2. Busca la sección **"Contraseñas de aplicaciones"**
   - Si no la ves, asegúrate de que la verificación en 2 pasos esté activada
   - También puedes ir directamente a: https://myaccount.google.com/apppasswords

3. Haz clic en **"Contraseñas de aplicaciones"**

4. Se abrirá una nueva página. Completa:
   - **Seleccionar app:** Elige **"Correo"**
   - **Seleccionar dispositivo:** Elige **"Otro (nombre personalizado)"**
   - Escribe: **"Inapsis Diagnostico"**
   - Haz clic en **"Generar"**

5. **Google te mostrará una contraseña de 16 caracteres** (sin espacios)
   - Ejemplo: `abcd efgh ijkl mnop`
   - **⚠️ IMPORTANTE:** Esta contraseña solo se muestra **UNA VEZ**
   - **Cópiala inmediatamente** antes de cerrar la ventana

#### Paso 3: Configurar en el Proyecto

1. Abre el archivo `.env` en la raíz del proyecto
2. Busca las líneas:
   ```env
   SMTP_EMAIL=inapsis.info@gmail.com
   SMTP_PASSWORD=
   ```

3. Pega la contraseña de 16 caracteres (sin espacios) en `SMTP_PASSWORD`:
   ```env
   SMTP_EMAIL=inapsis.info@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop
   ```

4. Guarda el archivo

#### Verificar que Funciona

1. Ejecuta la aplicación:
   ```bash
   streamlit run app_unificada.py
   ```

2. Ve a **"Diagnóstico Empresarial"**

3. Completa el formulario con un email de prueba (puede ser el mismo `inapsis.info@gmail.com`)

4. Después de generar el diagnóstico, deberías ver:
   - ✅ **"Tu diagnóstico ha sido enviado a tu email"**
   - Y recibir el email en la bandeja de entrada

#### Solución de Problemas

**Error: "SMTP_PASSWORD no encontrada en .env"**
- Verifica que el archivo `.env` existe y contiene `SMTP_PASSWORD=tu_contraseña`

**Error: "Error de autenticación"**
- Verifica que copiaste la contraseña completa (16 caracteres, sin espacios)
- Asegúrate de que la verificación en 2 pasos esté activada
- Genera una nueva contraseña de aplicación si es necesario

**Error: "Error de conexión con el servidor"**
- Verifica tu conexión a internet
- Asegúrate de que no haya un firewall bloqueando el puerto 587

**El email no llega**
- Revisa la carpeta de **Spam/Correo no deseado**
- Verifica que el email de destino sea correcto
- Espera unos minutos (puede haber demora)

#### Notas Importantes

- **Límite de Gmail:** Puedes enviar hasta **500 emails por día** con una cuenta gratuita de Gmail
- **Seguridad:** La contraseña de aplicación es específica para esta aplicación y puede revocarse en cualquier momento desde Google
- **Producción:** Para producción con más volumen, considera usar SendGrid o Amazon SES

#### Para Azure (Producción)

Si estás desplegando en Azure, también necesitas agregar estas variables en Azure Portal:

1. Ve a tu Web App en Azure Portal
2. **Configuration** → **Application settings**
3. Agrega:
   - `SMTP_EMAIL` = `inapsis.info@gmail.com`
   - `SMTP_PASSWORD` = `tu_contraseña_de_16_caracteres`
4. Haz clic en **"Save"**

### Ejecutar aplicación unificada

```bash
streamlit run app_unificada.py
```

Esto abrirá la aplicación en `http://localhost:8501` con:
- ✅ Todas las aplicaciones integradas (Diagnóstico, Superhéroes, Brainrot, Lógica)
- ✅ Navegación por sidebar
- ✅ Dashboard de estadísticas (acceso por URL)
- ✅ Exactamente como se verá en Azure

### Ejecutar apps individuales (opcional)

Si prefieres probar las apps por separado:

```bash
# Portal principal
streamlit run main_menu.py

# Apps individuales
streamlit run diagnostico/app.py
streamlit run gemelo/app.py
streamlit run brainrot/app.py
streamlit run logica/app.py
streamlit run estadisticas/app.py
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
   - (Opcional) Name: `MODEL_NAME`
   - (Opcional) Value: `gpt-4o-mini` (o el modelo que prefieras)
   - (Opcional) Name: `SMTP_EMAIL`
   - (Opcional) Value: `inapsis.info@gmail.com`
   - (Opcional) Name: `SMTP_PASSWORD`
   - (Opcional) Value: tu contraseña de aplicación de Gmail
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

Cambiar modelo en `.env`:

```env
MODEL_NAME=gpt-4o-mini  # o gpt-3.5-turbo, gpt-4, etc.
```

O editar `utils/openai_client.py` para cambiar el default:

```python
self.default_model = os.getenv("MODEL_NAME", "gpt-4o-mini")  # Cambiar default aquí
```

---

## 📚 Documentación Detallada

| Guía | Descripción | Tiempo |
|------|-------------|--------|
| [`azure/SETUP_PORTAL_WEB.md`](azure/SETUP_PORTAL_WEB.md) | ⭐ Guía completa paso a paso | 15 min |
| [`azure/README_AZURE.md`](azure/README_AZURE.md) | Resumen ejecutivo | 5 min |
| [`qr/README.md`](qr/README.md) | 🔲 Generador de códigos QR | 5 min |

---

## ✅ Checklist de Deployment

- [ ] Cuenta de Azure activa
- [ ] Web App creada en portal.azure.com
- [ ] Runtime: Python 3.11, Linux
- [ ] Plan: B1 (o el que prefieras)
- [ ] `OPENAI_API_KEY` configurada
- [ ] (Opcional) `SMTP_EMAIL` y `SMTP_PASSWORD` configuradas
- [ ] Startup command: `startup_single.sh`
- [ ] Publish profile descargado
- [ ] Secret en GitHub configurado
- [ ] Código pusheado a `main`
- [ ] Workflow ejecutado ✅
- [ ] App funcionando

---

## 🎯 Tecnologías

- **Python 3.11** - Backend
- **Streamlit 1.28.2** - Framework web interactivo
- **OpenAI API** - GPT-4o-mini (texto, más barato y mejor que GPT-3.5-turbo)
- **Pollinations.ai** - Generación gratuita de imágenes
- **SQLite** - Base de datos local
- **Gmail SMTP** - Envío de emails
- **Azure App Service** - Hosting
- **GitHub Actions** - CI/CD automático

---

## 🔒 Seguridad y Privacidad

### Datos almacenados:
- **Diagnóstico Empresarial**: Email, nombre, empresa, teléfono, tipo de negocio, desafíos, diagnóstico generado
- **Generador de Superhéroes**: Nombre, profesión, hobby, rasgos, descripción del superhéroe, email (opcional)
- **Brainrot Italiano**: Nombre, animal/cosa, nombre brainrot, texto italiano
- **Juego de Lógica**: Puntaje, total de desafíos, porcentaje
- **Estadísticas**: Uso de apps, leads empresariales y generales

### NO se almacena:
- ❌ Direcciones IP (excepto en leads empresariales, opcional)
- ❌ Información sensible no relacionada con el servicio
- ❌ Cookies de tracking
- ❌ Datos bancarios

### Base de datos:
- Archivo: `evento_inapsis.db`
- Formato: SQLite
- Ubicación: En Azure (efímera) o local según config
- Tablas: `interacciones`, `leads_empresariales`, `leads_generales`, `estadisticas_uso`, `resultados_juegos`

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

## ✨ Funcionalidades Implementadas

- ✅ **Envío automático de emails** - Diagnósticos empresariales enviados por Gmail SMTP
- ✅ **Dashboard de estadísticas** - Visualización de métricas y leads con exportación CSV
- ✅ **Generación de imágenes** - Pollinations.ai para superhéroes y brainrot
- ✅ **Recolección de leads** - Leads empresariales y generales con información completa
- ✅ **Generador de QR** - Script portable para generar códigos QR personalizados
- ✅ **Tracking de uso** - Estadísticas de inicio y completado por aplicación

## 🚀 Próximas Mejoras (Ideas)

- [ ] Integración con WhatsApp para envío de diagnósticos
- [ ] Dashboard avanzado con gráficos interactivos
- [ ] Multi-idioma (inglés, portugués)
- [ ] Exportar resultados en PDF
- [ ] Sistema de puntos/gamificación
- [ ] Análisis de sentimiento
- [ ] Notificaciones push

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
**Versión:** 2.0.0  
**Última actualización:** Diciembre 2024

### 📝 Changelog v2.0.0
- ✅ Envío automático de diagnósticos por email (Gmail SMTP)
- ✅ Dashboard de estadísticas con exportación CSV
- ✅ Generador de Brainrot Italiano para niños
- ✅ Recolección de leads empresariales y generales
- ✅ Tracking de uso de aplicaciones
- ✅ Generador de códigos QR portable
- ✅ Limpieza de código (archivos no usados eliminados)

---

**¿Listo para deployar?** → [`azure/SETUP_PORTAL_WEB.md`](azure/SETUP_PORTAL_WEB.md)
