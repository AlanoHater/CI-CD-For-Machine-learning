# 🚀 Integración de Prefect con GitHub Actions

## 🎯 Módulo Especial: Prefect para Orquestación de ML

Este módulo especial integra **Prefect** con los workflows de GitHub Actions, basándose en el tutorial de DataCamp sobre orquestación de workflows de ML.

## 📖 ¿Qué es Prefect?

**Prefect** es una plataforma open-source para orquestar y observar workflows de datos. Es especialmente útil para:

- ✅ **ML Pipelines**: Orquestar entrenamiento, evaluación y despliegue
- ✅ **Data Workflows**: Gestionar pipelines de procesamiento de datos
- ✅ **Task Dependencies**: Manejar dependencias complejas entre tareas
- ✅ **Error Handling**: Reintentos automáticos y manejo de fallos
- ✅ **Observability**: Monitoreo y logging detallado de ejecuciones

## 🏗️ Arquitectura de la Integración

### Componentes Implementados

```
📦 src/prefect_workflows/
├── __init__.py              # Configuración y utilities
├── ml_pipeline_flow.py      # Flows principales de ML
└── config.py                # Configuración multi-entorno

📦 examples/prefect/
├── basic_flow_example.py    # Conceptos básicos
├── advanced_flow_example.py # Manejo de errores
└── ml_pipeline_complete.py  # Pipeline completo

📦 .github/workflows/prefect/
└── prefect-ml-pipeline.yml  # CI/CD con Prefect
```

## 🚀 Inicio Rápido con Prefect

### 1. Instalación y Configuración

```bash
# Instalar Prefect
pip install prefect>=2.0.0 prefect-dask

# Configurar para desarrollo
python -c "from src.prefect_workflows import setup_prefect; setup_prefect()"
```

### 2. Iniciar Servidor Local (Opcional)

```bash
# Iniciar servidor Prefect UI
make prefect-server

# O usando el script
./scripts/run-prefect-demo.sh server
```

### 3. Ejecutar Primer Flow

```bash
# Ejecutar ejemplo básico
make prefect-basic

# O directamente
python examples/prefect/basic_flow_example.py
```

## 📚 Conceptos Clave de Prefect

### 1. **Flows y Tasks**

```python
from prefect import flow, task

@task
def process_data(data):
    # Lógica de procesamiento
    return processed_data

@flow
def ml_pipeline(data_path):
    raw_data = load_data(data_path)
    processed_data = process_data(raw_data)
    model = train_model(processed_data)
    return model
```

### 2. **Estados y Resultados**

Prefect maneja automáticamente los estados:
- `Pending` → `Running` → `Completed`
- `Failed` con información detallada
- `Retrying` para reintentos automáticos

### 3. **Artifacts y Logging**

```python
from prefect import get_run_logger
from prefect.artifacts import create_markdown_artifact

@task
def analyze_results(metrics):
    logger = get_run_logger()
    logger.info(f"Accuracy: {metrics['accuracy']:.4f}")

    # Crear artifact visual
    create_markdown_artifact(f"# Results\nAccuracy: {metrics['accuracy']}", "results")
```

## 🔧 Integración con GitHub Actions

### Workflow Básico con Prefect

```yaml
jobs:
  ml-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Prefect
        run: pip install prefect>=2.0.0

      - name: Run ML Pipeline
        run: |
          python -c "
          from src.prefect_workflows.ml_pipeline_flow import ml_training_pipeline
          results = ml_training_pipeline('data/dataset.csv')
          print(f'Accuracy: {results[\"evaluation\"][\"accuracy\"]}')
          "
```

### Workflow Avanzado con Prefect Server

```yaml
jobs:
  deploy-flows:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Prefect Cloud
        run: |
          prefect cloud login --key ${{ secrets.PREFECT_API_KEY }}
          python scripts/deploy_prefect_flows.py

  run-orchestrated-pipeline:
    needs: deploy-flows
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Prefect Flow Run
        run: |
          prefect deployment run ml-pipeline/main-deployment
```

## 📊 Casos de Uso en ML

### 1. **Pipeline de Entrenamiento Completo**

```python
@flow(name="ML Training Pipeline")
def training_pipeline(config_path: str):
    # Cargar configuración
    config = load_config(config_path)

    # Procesar datos
    data = load_and_preprocess_data(config['data_path'])

    # Entrenar modelo
    model = train_model(data, config['model_params'])

    # Evaluar y validar
    metrics = evaluate_model(model, data['test'])

    # Guardar y versionar
    save_model(model, config['model_path'])

    return {
        'accuracy': metrics['accuracy'],
        'model_path': config['model_path'],
        'config': config
    }
```

### 2. **Pipeline de Inferencia por Lotes**

```python
@flow(name="Batch Inference Pipeline")
def batch_inference(model_path: str, data_path: str):
    # Cargar modelo
    model = load_model(model_path)

    # Cargar datos para inferencia
    data = load_inference_data(data_path)

    # Realizar predicciones
    predictions = model.predict(data)

    # Guardar resultados
    save_predictions(predictions, "results/predictions.csv")

    return {"predictions_count": len(predictions)}
```

### 3. **Pipeline de Validación Continua**

```python
@flow(name="Model Validation Pipeline")
def validate_model_performance(model_path: str, threshold: float = 0.8):
    # Cargar modelo
    model = load_model(model_path)

    # Datos de validación
    X_val, y_val = load_validation_data()

    # Calcular métricas
    predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, predictions)

    # Validar threshold
    if accuracy < threshold:
        raise ValueError(f"Model accuracy {accuracy:.3f} below threshold {threshold}")

    return {"accuracy": accuracy, "passed": True}
```

## 🎮 Ejercicios Prácticos

### Ejercicio 1: Flow Básico de ML
Crea un flow que:
1. Cargue datos de ejemplo
2. Entrene un modelo simple
3. Guarde los resultados

### Ejercicio 2: Manejo de Errores
Implementa un flow que:
1. Maneje errores de carga de datos
2. Reintente operaciones fallidas
3. Proporcione logging detallado

### Ejercicio 3: Pipeline Completo
Construye un pipeline que integre:
1. Validación de datos
2. Entrenamiento de modelo
3. Evaluación de performance
4. Despliegue condicional

## 🔗 Integración con Herramientas ML

### MLflow Tracking

```python
import mlflow

@task
def log_to_mlflow(metrics: dict, model_params: dict):
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(model_params)

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log model
        mlflow.sklearn.log_model(model, "model")
```

### Dask para Computación Distribuida

```python
from prefect_dask import DaskTaskRunner

@flow(task_runner=DaskTaskRunner())
def distributed_training(data_path: str):
    # Entrenamiento distribuido con Dask
    model = train_with_dask(data_path)
    return model
```

## 📈 Monitoreo y Observabilidad

### Prefect UI Dashboard
- Visualización de flows y tareas
- Historial de ejecuciones
- Logs en tiempo real
- Métricas de performance

### Custom Logging

```python
@task
def monitor_training_progress():
    logger = get_run_logger()

    for epoch in range(100):
        # Training logic...
        loss = train_step()

        if epoch % 10 == 0:
            logger.info(f"Epoch {epoch}: Loss = {loss:.4f}")

            # Crear artifact de progreso
            create_markdown_artifact(
                f"# Training Progress\nEpoch: {epoch}\nLoss: {loss:.4f}",
                f"epoch-{epoch}-progress"
            )
```

## 🚀 Despliegue y Producción

### Configuración Multi-Entorno

```python
# config.py
def get_prod_config():
    return {
        'prefect_api_url': os.getenv('PREFECT_API_URL'),
        'database_url': os.getenv('DATABASE_URL'),
        'model_params': {
            'n_estimators': 200,
            'max_depth': None,
            'n_jobs': -1
        }
    }
```

### Deployment con GitHub Actions

```yaml
# .github/workflows/deploy-prefect.yml
name: Deploy Prefect Flows

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Prefect Cloud
        run: |
          prefect cloud login --key ${{ secrets.PREFECT_API_KEY }}
          python scripts/deploy_prefect_flows.py
```

## 📚 Recursos y Referencias

### Documentación Oficial
- [Prefect Docs](https://docs.prefect.io/)
- [Prefect Tutorials](https://docs.prefect.io/tutorials/)
- [Prefect API Reference](https://docs.prefect.io/api-ref/)

### Tutorial Base
- [DataCamp: ML Workflow Orchestration with Prefect](https://www.datacamp.com/es/tutorial/ml-workflow-orchestration-with-prefect)

### Comunidad
- [Prefect Slack Community](https://prefect.io/slack)
- [Prefect Discourse](https://discourse.prefect.io/)
- [Prefect GitHub](https://github.com/PrefectHQ/prefect)

## ✅ Checklist de Aprendizaje

- [ ] Entender conceptos básicos de flows y tasks
- [ ] Crear flows simples con dependencias
- [ ] Implementar manejo de errores y reintentos
- [ ] Usar Prefect UI para monitoreo
- [ ] Integrar con GitHub Actions
- [ ] Desplegar flows en producción
- [ ] Crear pipelines de ML orquestados

## 🎯 Próximos Pasos

1. **Experimenta** con los ejemplos incluidos
2. **Personaliza** los flows para tu caso de uso
3. **Integra** con tus pipelines existentes
4. **Despliega** en Prefect Cloud para producción
5. **Explora** integraciones avanzadas (MLflow, Dask)

---

**¡Prefect transforma tus scripts de ML en pipelines robustos y monitoreables!** 🚀🤖
