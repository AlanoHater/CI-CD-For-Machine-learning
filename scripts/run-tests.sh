#!/bin/bash
# Script para ejecutar tests localmente
# Uso: ./scripts/run-tests.sh

set -e  # Salir si hay error

echo "🧪 Ejecutando tests locales..."

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

# Instalar dependencias si no están instaladas
echo "📦 Verificando dependencias..."
if ! python -c "import pytest, numpy, pandas, sklearn" 2>/dev/null; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
    pip install pytest pytest-cov
fi

# Ejecutar tests
echo "🏃 Ejecutando tests..."
pytest tests/ -v \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=80

echo "✅ Tests completados exitosamente!"
