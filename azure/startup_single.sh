#!/bin/bash

# Startup para UNA SOLA Web App con todas las funcionalidades

echo "🚀 Iniciando aplicación unificada Inapsis IA en Azure..."

# Ejecutar la app unificada en puerto 8000 (Azure usa este puerto por defecto)
streamlit run app_unificada.py \
    --server.port=8000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false

