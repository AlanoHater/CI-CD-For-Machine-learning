# 📚 Módulo 5: Setting a Basic CI Pipeline

## 🎯 Objetivo del Módulo

Implementar un pipeline básico de CI paso a paso.

## 📖 Contenido

### 5.1 Componentes Básicos

1. **Checkout code**: `actions/checkout@v4`
2. **Setup environment**: `actions/setup-python@v5`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run tests**: `pytest tests/`

### 5.2 Pipeline ML Básico

```yaml
name: Basic CI
on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

## ✅ Estado: Implementado

Ver [pipeline ejemplo](../.github/workflows/ci-ml-pipeline.yml) para implementación completa.
