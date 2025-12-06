# 📚 Módulo 10: Running Python Code in GitHub Actions

## 🎯 Objetivo del Módulo

Aprender a ejecutar código Python efectivamente en entornos de GitHub Actions.

## 📖 Contenido

### 10.1 Setup Python

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'
    cache: 'pip'  # Cache dependencies
```

### 10.2 Instalar Dependencias

#### requirements.txt:
```yaml
- name: Install dependencies
  run: pip install -r requirements.txt
```

#### Poetry:
```yaml
- name: Setup Poetry
  uses: snok/install-poetry@v1
- run: poetry install
```

### 10.3 Ejecutar Código Python

#### Scripts directos:
```yaml
- name: Run training script
  run: python src/train.py
```

#### Con variables de entorno:
```yaml
- name: Run with env vars
  env:
    MODEL_PATH: ./models/
  run: python src/train.py
```

### 10.4 Testing Python

```yaml
- name: Run tests
  run: |
    pip install pytest pytest-cov
    pytest tests/ --cov=src --cov-report=xml
```

## ⏳ Estado: Pendiente

Crear ejemplos específicos para proyectos ML en Python.
