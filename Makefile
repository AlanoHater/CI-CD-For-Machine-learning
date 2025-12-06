# Makefile para automatizar tareas comunes en el proyecto MLOps GHA Learning

.PHONY: help install test lint clean build docs setup update

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy

# Colores para output
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# Default target
help: ## Mostrar ayuda
	@echo "$(BLUE)🚀 MLOps GHA Learning - Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

# Setup y instalación
setup: ## Configurar entorno de desarrollo completo
	@echo "$(BLUE)🔧 Configurando entorno de desarrollo...$(NC)"
	$(PIP) install -e ".[dev]"
	pre-commit install
	@echo "$(GREEN)✅ Entorno configurado$(NC)"

install: ## Instalar dependencias básicas
	@echo "$(BLUE)📦 Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

install-dev: ## Instalar dependencias de desarrollo
	@echo "$(BLUE)📦 Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✅ Dependencias de desarrollo instaladas$(NC)"

# Testing
test: ## Ejecutar todos los tests
	@echo "$(BLUE)🧪 Ejecutando tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Tests completados$(NC)"

test-unit: ## Ejecutar solo tests unitarios
	@echo "$(BLUE)🧪 Ejecutando tests unitarios...$(NC)"
	$(PYTHON) -m pytest tests/ -v -k "not integration"
	@echo "$(GREEN)✅ Tests unitarios completados$(NC)"

test-integration: ## Ejecutar tests de integración
	@echo "$(BLUE)🧪 Ejecutando tests de integración...$(NC)"
	$(PYTHON) -m pytest tests/ -v -k "integration"
	@echo "$(GREEN)✅ Tests de integración completados$(NC)"

test-coverage: ## Generar reporte de cobertura
	@echo "$(BLUE)📊 Generando reporte de cobertura...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=src --cov-report=html
	@echo "$(GREEN)✅ Reporte generado en htmlcov/$(NC)"

# Code Quality
lint: ## Ejecutar todos los linters
	@echo "$(BLUE)🧹 Ejecutando linting completo...$(NC)"
	$(MAKE) format-check
	$(MAKE) flake8
	$(MAKE) mypy
	@echo "$(GREEN)✅ Linting completado$(NC)"

format: ## Formatear código con black e isort
	@echo "$(BLUE)🎨 Formateando código...$(NC)"
	$(BLACK) src/ tests/ examples/
	$(ISORT) src/ tests/ examples/
	@echo "$(GREEN)✅ Código formateado$(NC)"

format-check: ## Verificar formato sin modificar
	@echo "$(BLUE)🔍 Verificando formato...$(NC)"
	$(BLACK) --check --diff src/ tests/ examples/
	$(ISORT) --check-only --diff src/ tests/ examples/

flake8: ## Ejecutar flake8
	@echo "$(BLUE)🐛 Ejecutando flake8...$(NC)"
	$(FLAKE8) src/ tests/ examples/

mypy: ## Ejecutar mypy
	@echo "$(BLUE)🔍 Ejecutando mypy...$(NC)"
	$(MYPY) src/

# Desarrollo
run-demo: ## Ejecutar demo del pipeline ML
	@echo "$(BLUE)🚀 Ejecutando demo del pipeline ML...$(NC)"
	$(PYTHON) examples/demo-ml-pipeline.py

run-data-gen: ## Generar datos de ejemplo
	@echo "$(BLUE)📊 Generando datos de ejemplo...$(NC)"
	$(PYTHON) -c "
	from src.data_utils import generate_sample_data, save_processed_data, preprocess_data
	import os
	os.makedirs('data/sample', exist_ok=True)
	df = generate_sample_data(1000, 8, 42)
	X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
	save_processed_data(X_train, X_test, y_train, y_test, scaler, 'data/sample/')
	print('✅ Datos generados en data/sample/')
	"

train-model: ## Entrenar un modelo de ejemplo
	@echo "$(BLUE)🏋️ Entrenando modelo de ejemplo...$(NC)"
	$(PYTHON) -c "
	from src.data_utils import generate_sample_data, preprocess_data
	from src.model import create_and_train_model
	df = generate_sample_data(500, 6, 42)
	X_train, X_test, y_train, y_test, _ = preprocess_data(df)
	model = create_and_train_model(X_train, y_train)
	results = model.evaluate(X_test, y_test)
	print(f'📊 Accuracy: {results[\"accuracy\"]:.4f}')
	model.save_model('models/trained_model.pkl')
	print('✅ Modelo guardado en models/trained_model.pkl')
	"

# Utilidades
clean: ## Limpiar archivos generados
	@echo "$(BLUE)🧹 Limpiando archivos generados...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-models: ## Limpiar modelos guardados
	@echo "$(BLUE)🧹 Limpiando modelos...$(NC)"
	find . -name "*.pkl" -path "./models/*" -delete
	@echo "$(GREEN)✅ Modelos limpiados$(NC)"

clean-data: ## Limpiar datos generados
	@echo "$(BLUE)🧹 Limpiando datos...$(NC)"
	rm -rf data/
	@echo "$(GREEN)✅ Datos limpiados$(NC)"

# Build y distribución
build: ## Construir paquete
	@echo "$(BLUE)📦 Construyendo paquete...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)✅ Paquete construido$(NC)"

check-build: ## Verificar construcción del paquete
	@echo "$(BLUE)🔍 Verificando paquete...$(NC)"
	$(PYTHON) -m twine check dist/*
	@echo "$(GREEN)✅ Paquete verificado$(NC)"

# Documentación
docs: ## Generar documentación (placeholder)
	@echo "$(BLUE)📚 Generando documentación...$(NC)"
	@echo "Documentación disponible en docs/"
	@echo "$(GREEN)✅ Documentación generada$(NC)"

# CI/CD
ci: ## Ejecutar checks de CI localmente
	@echo "$(BLUE)🚀 Ejecutando CI local...$(NC)"
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) build
	$(MAKE) check-build
	@echo "$(GREEN)✅ CI local completado$(NC)"

# Actualización
update: ## Actualizar dependencias
	@echo "$(BLUE)⬆️ Actualizando dependencias...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	@echo "$(GREEN)✅ Dependencias actualizadas$(NC)"

update-dev: ## Actualizar dependencias de desarrollo
	@echo "$(BLUE)⬆️ Actualizando dependencias de desarrollo...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -e ".[dev]"
	@echo "$(GREEN)✅ Dependencias de desarrollo actualizadas$(NC)"

# Información
info: ## Mostrar información del proyecto
	@echo "$(BLUE)📊 Información del proyecto:$(NC)"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Archivos Python: $(shell find src/ tests/ -name "*.py" | wc -l)"
	@echo "Tests: $(shell find tests/ -name "test_*.py" | wc -l)"
	@echo "Ejemplos: $(shell find examples/ -name "*.py" | wc -l)"
	@echo "Workflows: $(shell find .github/workflows/ -name "*.yml" | wc -l)"

# Prefect workflows
prefect-setup: ## Configurar Prefect para desarrollo
	@echo "$(BLUE)🚀 Configurando Prefect...$(NC)"
	pip install prefect>=2.0.0 prefect-dask
	prefect config set PREFECT_API_URL http://127.0.0.1:4200/api
	@echo "$(GREEN)✅ Prefect configurado$(NC)"

prefect-server: ## Iniciar servidor Prefect local
	@echo "$(BLUE)🖥️  Iniciando servidor Prefect...$(NC)"
	@echo "💡 Servidor disponible en: http://127.0.0.1:4200"
	prefect server start

prefect-demo: ## Ejecutar demos de Prefect
	@echo "$(BLUE)🤖 Ejecutando demos de Prefect...$(NC)"
	./scripts/run-prefect-demo.sh all
	@echo "$(GREEN)✅ Demos de Prefect completados$(NC)"

prefect-basic: ## Ejecutar demo básico de Prefect
	@echo "$(BLUE)🎭 Ejecutando demo básico...$(NC)"
	./scripts/run-prefect-demo.sh basic
	@echo "$(GREEN)✅ Demo básico completado$(NC)"

prefect-advanced: ## Ejecutar demo avanzado de Prefect
	@echo "$(BLUE)🎪 Ejecutando demo avanzado...$(NC)"
	./scripts/run-prefect-demo.sh advanced
	@echo "$(GREEN)✅ Demo avanzado completado$(NC)"

prefect-ml: ## Ejecutar pipeline completo de ML con Prefect
	@echo "$(BLUE)🤖 Ejecutando pipeline ML...$(NC)"
	./scripts/run-prefect-demo.sh complete
	@echo "$(GREEN)✅ Pipeline ML completado$(NC)"

# Desarrollo avanzado
pre-commit: ## Ejecutar pre-commit en todos los archivos
	@echo "$(BLUE)🔍 Ejecutando pre-commit...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✅ Pre-commit completado$(NC)"

benchmark: ## Ejecutar benchmarks de performance
	@echo "$(BLUE)⚡ Ejecutando benchmarks...$(NC)"
	$(PYTHON) -c "
	import time
	from src.data_utils import generate_sample_data, preprocess_data
	from src.model import create_and_train_model

	# Benchmark data processing
	start = time.time()
	df = generate_sample_data(1000, 10)
	X_train, X_test, y_train, y_test, _ = preprocess_data(df)
	data_time = time.time() - start

	# Benchmark model training
	start = time.time()
	model = create_and_train_model(X_train, y_train)
	train_time = time.time() - start

	print(f'📊 Data processing: {data_time:.2f}s')
	print(f'🏋️ Model training: {train_time:.2f}s')
	print(f'📈 Total: {data_time + train_time:.2f}s')
	"
	@echo "$(GREEN)✅ Benchmarks completados$(NC)"

# Atajos útiles
all: clean install-dev lint test build ## Ejecutar todo el pipeline completo
quick: format test ## Formatear y testear rápidamente
check: lint test ## Verificar calidad sin modificar archivos
