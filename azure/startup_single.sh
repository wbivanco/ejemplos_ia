#!/bin/bash

# Startup para UNA SOLA Web App con todas las funcionalidades

echo "🚀 Iniciando aplicación unificada Inapsis IA en Azure..."

# Instalar dependencias si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias desde requirements.txt..."
    pip install --no-cache-dir -r requirements.txt
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  No se encontró requirements.txt"
fi

# Ejecutar la app unificada en puerto 8000 (Azure usa este puerto por defecto)
echo "🌐 Iniciando Streamlit..."
streamlit run app_unificada.py \
    --server.port=8000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false

