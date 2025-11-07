# ☁️ Deployment en Azure con GitHub Actions

## 🎯 Archivos en esta carpeta

- **`startup_single.sh`** - Script de inicio para Azure
- **`Dockerfile`** - Para deployment con Docker (backup)
- **`SETUP_PORTAL_WEB.md`** - ⭐ Guía completa con portal web

**Nota:** `app_unificada.py` (app integrada) está ahora en la raíz del proyecto para poder probarlo localmente

---

## 🚀 Setup desde el Portal Web de Azure

### Pasos (15 minutos):

1. **Crear Web App** en https://portal.azure.com
   - Resource Group: `inapsis-ia-rg`
   - Name: `inapsis-ia-app`
   - Runtime: Python 3.11
   - Plan: Basic B1

2. **Configurar variables**
   - Configuration → Application settings
   - Añadir: `OPENAI_API_KEY` con tu clave

3. **Configurar startup**
   - Configuration → General settings
   - Startup Command: `startup_single.sh`

4. **Obtener publish profile**
   - Click "Get publish profile" en tu Web App
   - Copiar contenido del archivo

5. **Añadir secret en GitHub**
   - Settings → Secrets → Actions
   - New secret: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Pegar contenido del publish profile

6. **Push y deploy**
   ```bash
   git push origin main
   ```

**📖 Guía detallada con screenshots:** Ver `SETUP_PORTAL_WEB.md`

---

## 🌐 URL Resultante

```
https://inapsis-ia-app.azurewebsites.net
```

---

## 💰 Costos

- Azure App Service B1: $13/mes
- OpenAI API: ~$5-20/mes
- **Total: ~$18-33/mes**

---

## 📚 Documentación

- **Inicio rápido:** `AZURE_SETUP_RAPIDO.txt`
- **Guía completa:** `AZURE_DEPLOY.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`

---

## 🔄 Workflow

El workflow de GitHub Actions está en:
```
../.github/workflows/azure-single-app.yml
```

Se ejecuta automáticamente en cada push a `main`

---

**Volver al README principal:** `../README.md`

