# ☁️ Configuración desde el Portal Web de Azure

## 🎯 Setup Completo (15 minutos)

### 1️⃣ Crear Web App desde el Portal

1. Ve a: https://portal.azure.com
2. Click en **"Create a resource"**
3. Busca **"Web App"**
4. Click **"Create"**

**Configuración:**
- **Subscription:** Tu suscripción
- **Resource Group:** Crear nuevo → `inapsis-ia-rg`
- **Name:** `inapsis-ia-app` (o el que prefieras)
- **Publish:** Code
- **Runtime stack:** Python 3.11
- **Operating System:** Linux
- **Region:** East US (o tu preferencia)

**Plan:**
- **Pricing plan:** Basic B1 ($13/mes)

Click **"Review + Create"** → **"Create"**

---

### 2️⃣ Configurar Variables de Entorno

1. Ve a tu Web App en el portal
2. En el menú izquierdo: **Configuration** → **Application settings**
3. Click **"New application setting"**

Añadir:
- **Name:** `OPENAI_API_KEY`
- **Value:** Tu clave de OpenAI
- Click **OK**

4. Click **"Save"** arriba
5. Click **"Continue"** cuando pregunte

---

### 3️⃣ Configurar Startup Command

1. En tu Web App: **Configuration** → **General settings**
2. **Startup Command:** `startup_single.sh`
3. Click **"Save"**

---

### 4️⃣ Habilitar Autenticación Básica (Requerido)

⚠️ **Paso crítico:** Azure necesita esto para GitHub Actions

1. En tu Web App: **Configuration** → **General settings**
2. Baja hasta la sección **"Platform settings"**
3. Encuentra **"Basic Auth Publishing Credentials"** o **"SCM Basic Auth Publishing Credentials"**
4. Cambia a **"On"** (Activar)
5. Click **"Save"**

---

### 5️⃣ Obtener Publish Profile para GitHub

1. En tu Web App, click **"Get publish profile"** (arriba)
2. Se descarga un archivo `.PublishSettings`
3. Abre el archivo con un editor de texto
4. **Copia TODO el contenido**

---

### 6️⃣ Configurar GitHub Secret

1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
5. **Value:** Pega el contenido del archivo .PublishSettings
6. Click **"Add secret"**

---

### 7️⃣ Deploy Inicial

```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

GitHub Actions se ejecutará automáticamente y deployará tu app.

---

## 🌐 Acceder a tu App

Tu app estará en:
```
https://inapsis-ia-app.azurewebsites.net
```

(Reemplaza `inapsis-ia-app` con el nombre que elegiste)

---

## 📊 Monitorear el Deployment

### En GitHub:
1. Ve a tu repositorio
2. Pestaña **"Actions"**
3. Verás el workflow ejecutándose
4. Click en el workflow para ver detalles

### En Azure Portal:
1. Ve a tu Web App
2. **Deployment Center** (menú izquierdo)
3. Verás el historial de deployments

---

## 🔧 Ver Logs en Azure Portal

1. Ve a tu Web App
2. **Monitoring** → **Log stream** (menú izquierdo)
3. Verás los logs en tiempo real

O usa **Diagnose and solve problems** para troubleshooting avanzado.

---

## ⚙️ Configuraciones Opcionales

### Habilitar HTTPS Only
1. Web App → **Configuration** → **General settings**
2. **HTTPS Only:** On
3. Save

### Cambiar el Plan de Pricing
1. Web App → **Scale up (App Service plan)**
2. Elige otro plan (F1 gratis, B2, P1V2, etc.)
3. Apply

### Custom Domain (opcional)
1. Web App → **Custom domains**
2. Add custom domain
3. Sigue las instrucciones

---

## 🔄 Workflow de Desarrollo

1. **Desarrollar localmente** (opcional)
2. **Commit** cambios
3. **Push** a `main`
4. **GitHub Actions** despliega automáticamente
5. **Verificar** en tu URL de Azure

```bash
git add .
git commit -m "Descripción de cambios"
git push origin main
# ¡Auto-deploy en 3-5 minutos!
```

---

## 🆘 Troubleshooting desde el Portal

### App no carga
1. **Log stream** → Revisar errores
2. **Diagnose and solve problems** → Availability
3. **Restart** → Arriba en el overview

### Ver configuración actual
1. **Configuration** → Ver todas las settings
2. Verificar que `OPENAI_API_KEY` está presente

### Deployment falló
1. **Deployment Center** → Ver logs del deployment
2. GitHub Actions → Ver logs detallados

---

## ✅ Checklist Completo

- [ ] Web App creada en Azure Portal
- [ ] Plan de pricing seleccionado
- [ ] OPENAI_API_KEY configurada
- [ ] Startup command configurada
- [ ] **Autenticación básica habilitada** ⚠️
- [ ] Publish profile descargado
- [ ] Secret añadido en GitHub
- [ ] Código pusheado a main
- [ ] Workflow ejecutado exitosamente
- [ ] App funcionando en la URL

---

## 💡 Tips

- **Monitoreo:** Usa Application Insights para métricas avanzadas
- **Scaling:** Ajusta el plan según tu tráfico
- **Backup:** Azure hace backups automáticos
- **SSL:** HTTPS viene incluido gratis

---

**¡Todo configurado desde el portal web! No necesitas CLI.** ✅

