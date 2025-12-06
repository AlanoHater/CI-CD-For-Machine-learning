#!/bin/bash
# Script para ejecutar demos de Prefect localmente
# Uso: ./scripts/run-prefect-demo.sh [basic|advanced|complete|all]

set -e  # Salir si hay error

# Función de ayuda
show_help() {
    echo "🚀 Script para ejecutar demos de Prefect"
    echo ""
    echo "Uso: $0 [OPCION]"
    echo ""
    echo "Opciones:"
    echo "  basic     - Ejecutar ejemplo básico de flows"
    echo "  advanced  - Ejecutar ejemplo avanzado con errores"
    echo "  complete  - Ejecutar pipeline completo de ML"
    echo "  all       - Ejecutar todos los ejemplos"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 basic"
    echo "  $0 all"
    echo "  $0 help"
}

# Función para verificar dependencias
check_dependencies() {
    echo "📦 Verificando dependencias..."

    if ! python -c "import prefect" 2>/dev/null; then
        echo "Instalando Prefect..."
        pip install prefect>=2.0.0
    fi

    if ! python -c "import src.prefect_workflows" 2>/dev/null; then
        echo "⚠️  Módulos locales no encontrados, instalando en modo desarrollo..."
        pip install -e .
    fi

    echo "✅ Dependencias verificadas"
}

# Función para ejecutar ejemplo básico
run_basic() {
    echo "🎭 Ejecutando ejemplo básico de Prefect..."
    echo "=" * 50

    python examples/prefect/basic_flow_example.py

    echo ""
    echo "✅ Ejemplo básico completado"
}

# Función para ejecutar ejemplo avanzado
run_advanced() {
    echo "🎪 Ejecutando ejemplo avanzado de Prefect..."
    echo "=" * 50

    python examples/prefect/advanced_flow_example.py

    echo ""
    echo "✅ Ejemplo avanzado completado"
}

# Función para ejecutar pipeline completo
run_complete() {
    echo "🤖 Ejecutando pipeline completo de ML con Prefect..."
    echo "=" * 60

    python examples/prefect/ml_pipeline_complete.py

    echo ""
    echo "✅ Pipeline completo ejecutado"
}

# Función para configurar Prefect (opcional)
setup_prefect_server() {
    echo "🔧 Configurando servidor Prefect local..."

    # Verificar si el servidor ya está corriendo
    if curl -s http://127.0.0.1:4200/api/health > /dev/null 2>&1; then
        echo "✅ Servidor Prefect ya está ejecutándose"
        return
    fi

    echo "🚀 Iniciando servidor Prefect..."
    echo "💡 El servidor estará disponible en: http://127.0.0.1:4200"
    echo "💡 Presiona Ctrl+C para detener el servidor"

    # Iniciar servidor en background
    prefect server start &

    # Esperar a que esté listo
    echo "⏳ Esperando que el servidor inicie..."
    for i in {1..30}; do
        if curl -s http://127.0.0.1:4200/api/health > /dev/null 2>&1; then
            echo "✅ Servidor Prefect listo!"
            return
        fi
        sleep 2
    done

    echo "⚠️  Servidor Prefect no pudo iniciar en 60 segundos"
    echo "💡 Puedes iniciarlo manualmente con: prefect server start"
}

# Procesar argumentos
case "${1:-all}" in
    "basic")
        check_dependencies
        run_basic
        ;;
    "advanced")
        check_dependencies
        run_advanced
        ;;
    "complete")
        check_dependencies
        run_complete
        ;;
    "all")
        check_dependencies
        echo "🚀 Ejecutando TODOS los ejemplos de Prefect"
        echo "=" * 60
        run_basic
        echo ""
        run_advanced
        echo ""
        run_complete
        ;;
    "server")
        setup_prefect_server
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Opción inválida: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "🎉 ¡Ejecución completada!"
echo ""
echo "💡 Recursos adicionales:"
echo "  • Prefect UI: http://127.0.0.1:4200 (si el servidor está corriendo)"
echo "  • Documentación: https://docs.prefect.io/"
echo "  • Tutorial usado: https://www.datacamp.com/es/tutorial/ml-workflow-orchestration-with-prefect"
