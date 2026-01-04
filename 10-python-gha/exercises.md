### Módulo 10: `10-python-gha/exercises.md`

```markdown
# 💻 Ejercicios Prácticos - Módulo 10: Python in GitHub Actions

## 🎯 Objetivo
Configurar entornos Python eficientes para ML, incluyendo gestión de dependencias y caching.

## 📋 Lista de Ejercicios

### Ejercicio 10.1: Setup Python con Caching ⭐⭐⭐
**Objetivo**: Acelerar la instalación de dependencias usando caché.
**Tareas**:
1. Checkout código.
2. Usar `actions/setup-python@v5`.
3. Configurar `cache: 'pip'`.
4. Instalar `requirements.txt`.

**Solución esperada**:
```yaml
name: Python Setup
on: [push]
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'
      - name: Install
        run: pip install -r requirements.txt

```
# 💻 Ejercicio 10.2: Ejecución de Script ML

## 🎯 Objetivo
Crear y ejecutar un ml-pipeline

**Tareas**:
1. Instalar dependencias completas.
2. Configurar PYTHONPATH si es necesario.
3. Ejecutar el script.

**Solución esperada**:
```yaml
name: Run ML Demo
on: [push]
jobs:
  ml-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - name: Execute Pipeline
        run: python examples/demo-ml-pipeline.py
