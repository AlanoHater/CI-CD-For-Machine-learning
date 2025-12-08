Markdown

# 📚 Módulo 7: Write a GitHub Actions Workflow

## 🎯 Objetivo del Módulo

Crear workflows de GitHub Actions desde cero para casos específicos, yendo más allá de los triggers básicos.

## 📖 Contenido

### 7.1 Proceso de Escritura

1. **Definir objetivo**: ¿Qué automatizar? (Ej. Reentrenamiento, Deploy)
2. **Elegir eventos**: ¿Cuándo ejecutar? (Ej. Cron, Manual)
3. **Planear jobs**: ¿Qué tareas? (Ej. Train, Evaluate)
4. **Seleccionar steps**: ¿Cómo implementar? (Ej. Scripts, Actions)

### 7.2 Casos de Uso Reales

#### Caso 1: Reentrenamiento Nocturno (Scheduled)
Automatizar el reentrenamiento del modelo cada noche para incorporar nuevos datos.

```yaml
name: 🌙 Nightly Model Retraining
on:
  schedule:
    - cron: '0 2 * * *' # 2:00 AM UTC todos los días

jobs:
  retrain:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - name: Ejecutar Pipeline de Entrenamiento
        run: python examples/demo-ml-pipeline.py
```
Caso 2: Despliegue Manual a Producción (Workflow Dispatch)
Permitir a los MLOps Engineers desplegar un modelo específico manualmente tras aprobación.

```yaml

name: 🚀 Manual Deploy to Prod
on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Versión del modelo a desplegar'
        required: true
        default: 'v1.0.0'
      environment:
        description: 'Entorno destino'
        type: choice
        options:
        - staging
        - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Desplegando versión ${{ inputs.model_version }} a ${{ inputs.environment }}..."
      # Aquí irían los steps de deploy reales (ej. AWS, Azure, etc.)
Caso 3: CI Optimizado (Paths Filter)
Evitar gastar minutos de cómputo ejecutando el pipeline de ML cuando solo cambia la documentación.
```
```yaml

name: Code-Only CI
on:
  push:
    paths-ignore:
      - 'docs/**'
      - '**.md'
      - 'LICENSE'
