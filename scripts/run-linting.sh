#!/bin/bash
# Script para ejecutar linting localmente
# Uso: ./scripts/run-linting.sh

set -e  # Salir si hay error

echo "🧹 Ejecutando linting..."

# Verificar que estamos en el directorio correcto
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

# Instalar herramientas de linting si no están instaladas
echo "📦 Verificando herramientas de linting..."
if ! python -c "import black, flake8, isort, mypy" 2>/dev/null; then
    echo "Instalando herramientas de linting..."
    pip install black flake8 isort mypy
fi

echo "🔍 Ejecutando Black (formateo)..."
black --check --diff src/ tests/ || (
    echo "💡 Para arreglar: black src/ tests/"
    exit 1
)

echo "📏 Ejecutando isort (imports)..."
isort --check-only --diff src/ tests/ || (
    echo "💡 Para arreglar: isort src/ tests/"
    exit 1
)

echo "🐛 Ejecutando flake8 (linting)..."
flake8 src/ tests/

echo "🔍 Ejecutando mypy (tipos)..."
mypy src/ --ignore-missing-imports

echo "✅ Linting completado exitosamente!"
