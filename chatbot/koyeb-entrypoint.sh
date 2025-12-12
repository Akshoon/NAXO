#!/bin/bash
set -e

# Script de entrada para Koyeb
# Detecta el puerto asignado dinámicamente y arranca gunicorn

# El puerto es asignado por Koyeb via variable de entorno PORT
PORT=${PORT:-5000}

echo "🚀 Iniciando Chatbot API en puerto $PORT"
echo "📊 Configuración:"
echo "   - Workers: 2"
echo "   - Timeout: 120s"
echo "   - Max requests: 1000 (recicla workers para evitar memory leaks)"

# Arrancar con gunicorn (más robusto que Flask development server)
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --max-requests 1000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    api_chatbot:app
