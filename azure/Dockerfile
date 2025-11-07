# Dockerfile para Azure Container Apps o Azure App Service

FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer puertos
EXPOSE 8501 8502 8503 8504

# Variable de entorno para indicar que estamos en Azure
ENV AZURE_DEPLOYMENT=true

# Script de inicio que puede ejecutar múltiples apps
COPY startup.sh /app/
RUN chmod +x /app/startup.sh

# Comando de inicio
CMD ["/app/startup.sh"]

