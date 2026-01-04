### Módulo 9: `09-feature-branches/README.md`

# 📚 Módulo 9: Feature Branches & Git Flow

## 🎯 Objetivo del Módulo

Implementar estrategias de CI diferenciadas según la rama (Feature vs. Main) para optimizar recursos y velocidad.

## 📖 Contenido

### 9.1 Estrategia de Ramas para ML
- **Feature Branches (`feature/*`)**: Iteración rápida, tests unitarios, linting rápido.
- **Main Branch (`main`)**: Tests de integración, entrenamiento completo, deploy a staging.

### 9.2 Casos de Uso Reales (Ejemplos)

#### Caso 1: Validación Rápida en Feature Branches
En ramas de desarrollo, queremos feedback rápido. Solo corremos tests unitarios y linting, saltando el entrenamiento pesado.

```yaml
name: Feature Branch CI
on:
  push:
    branches: ['feature/**']  # Solo en ramas feature

jobs:
  fast-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      
      # Solo validación estática y tests rápidos
      - run: ./scripts/run-linting.sh
      - run: pytest tests/test_data_utils.py  # Tests ligeros solamente
```
Caso 2: Pipeline Completo en Main
Cuando el código llega a producción (main), ejecutamos todo el flujo pesado.

```yaml

name: Main Branch Release
on:
  push:
    branches: ['main']

jobs:
  full-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # ... setup python ...
      
      # Pipeline completo de ML
      - name: Run Full ML Demo
        run: python examples/demo-ml-pipeline.py
        
      # Generar reportes de cobertura
      - run: pytest tests/ --cov=src
```

Caso 3: Lógica Condicional dentro de un Job
Usar expresiones if para pasos condicionales en un mismo workflow.

```yaml

steps:
  - name: Deploy to Production
    if: github.ref == 'refs/heads/main'  # Solo si estamos en main
    run: ./scripts/deploy.sh
