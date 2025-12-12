#!/bin/bash

# =======================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA - NAXO STACK
# Para Ubuntu 20.04 / 22.04 / 24.04
# =======================================================================

set -e # Detener script si hay error

echo "🚀 Iniciando instalación de NAXO..."

# 1. Actualizar sistema
echo "📦 Actualizando repositorios..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Instalar herramientas básicas
echo "🛠️ Instalando git, curl y utilidades..."
sudo apt-get install -y git curl apt-transport-https ca-certificates software-properties-common

# 3. Instalar Docker y Docker Compose
if ! command -v docker &> /dev/null; then
    echo "🐳 Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    # Dar permisos al usuario actual para usar docker sin sudo
    sudo usermod -aG docker $USER
    echo "⚠️ Docker instalado. Es posible que necesites cerrar sesión y volver a entrar para usar 'docker' sin sudo."
else
    echo "✅ Docker ya está instalado."
fi

# 4. Clonar el repositorio
REPO_DIR="NAXO"
REPO_URL="https://github.com/Akshoon/NAXO.git"

if [ -d "$REPO_DIR" ]; then
    echo "📂 El directorio $REPO_DIR ya existe. Actualizando..."
    cd $REPO_DIR
    git pull
else
    echo "📥 Clonando repositorio..."
    git clone $REPO_URL
    cd $REPO_DIR
fi

# 5. Configurar variables de entorno
if [ ! -f .env ]; then
    echo "⚙️ Configurando variables de entorno..."
    echo "Por favor, ingresa tu GEMINI_API_KEY:"
    read -r API_KEY
    
    echo "GEMINI_API_KEY=$API_KEY" > .env
    echo "FLASK_ENV=production" >> .env
    echo "✅ Archivo .env creado."
else
    echo "✅ Archivo .env ya existe."
fi

# 6. Levantar el stack
echo "🚀 Levantando servicios con Docker Compose..."
# Forzamos rebuild para asegurar últimos cambios
sudo docker compose up -d --build

echo ""
echo "======================================================="
echo "🎉 ¡INSTALACIÓN COMPLETADA!"
echo "======================================================="
echo "🌍 Tu aplicación debería estar corriendo en:"
echo "   http://$(curl -s ifconfig.me):8080"
echo ""
echo "📝 Comandos útiles:"
echo "   - Ver logs:        cd ~/NAXO && sudo docker compose logs -f"
echo "   - Reiniciar todo:  cd ~/NAXO && sudo docker compose restart"
echo "   - Detener todo:    cd ~/NAXO && sudo docker compose down"
echo "======================================================="
