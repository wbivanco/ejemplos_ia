# 📧 Configuración de Email con Gmail

Esta guía te explica paso a paso cómo configurar el envío de emails automáticos desde `inapsis.info@gmail.com` usando Gmail SMTP.

## 🎯 ¿Qué necesitas hacer en Google?

### Paso 1: Activar Verificación en 2 Pasos

1. Ve a tu cuenta de Google: https://myaccount.google.com/security
2. Inicia sesión con `inapsis.info@gmail.com`
3. Busca la sección **"Iniciar sesión en Google"**
4. Si **"Verificación en 2 pasos"** está desactivada:
   - Haz clic en **"Verificación en 2 pasos"**
   - Sigue las instrucciones para activarla
   - Puede pedirte confirmar tu teléfono

**⚠️ Importante:** La verificación en 2 pasos es **obligatoria** para generar contraseñas de aplicación.

---

### Paso 2: Generar Contraseña de Aplicación

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

---

### Paso 3: Configurar en el Proyecto

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

---

## ✅ Verificar que Funciona

1. Ejecuta la aplicación:
   ```bash
   streamlit run app_unificada.py
   ```

2. Ve a **"Diagnóstico Empresarial"**

3. Completa el formulario con un email de prueba (puede ser el mismo `inapsis.info@gmail.com`)

4. Después de generar el diagnóstico, deberías ver:
   - ✅ **"Tu diagnóstico ha sido enviado a tu email"**
   - Y recibir el email en la bandeja de entrada

---

## 🔧 Solución de Problemas

### Error: "SMTP_PASSWORD no encontrada en .env"
- **Solución:** Verifica que el archivo `.env` existe y contiene `SMTP_PASSWORD=tu_contraseña`

### Error: "Error de autenticación"
- **Solución:** 
  - Verifica que copiaste la contraseña completa (16 caracteres, sin espacios)
  - Asegúrate de que la verificación en 2 pasos esté activada
  - Genera una nueva contraseña de aplicación si es necesario

### Error: "Error de conexión con el servidor"
- **Solución:**
  - Verifica tu conexión a internet
  - Asegúrate de que no haya un firewall bloqueando el puerto 587

### El email no llega
- **Solución:**
  - Revisa la carpeta de **Spam/Correo no deseado**
  - Verifica que el email de destino sea correcto
  - Espera unos minutos (puede haber demora)

---

## 📝 Notas Importantes

- **Límite de Gmail:** Puedes enviar hasta **500 emails por día** con una cuenta gratuita de Gmail
- **Seguridad:** La contraseña de aplicación es específica para esta aplicación y puede revocarse en cualquier momento desde Google
- **Producción:** Para producción con más volumen, considera usar SendGrid o Amazon SES (ver documentación)

---

## 🚀 Para Azure (Producción)

Si estás desplegando en Azure, también necesitas agregar estas variables en Azure Portal:

1. Ve a tu Web App en Azure Portal
2. **Configuration** → **Application settings**
3. Agrega:
   - `SMTP_EMAIL` = `inapsis.info@gmail.com`
   - `SMTP_PASSWORD` = `tu_contraseña_de_16_caracteres`
4. Haz clic en **"Save"**

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Verifica que seguiste todos los pasos
2. Revisa la sección de "Solución de Problemas" arriba
3. Asegúrate de que la verificación en 2 pasos esté activada

