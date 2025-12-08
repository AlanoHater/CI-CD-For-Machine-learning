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

10.5 Casos de Uso Reales (Ejemplos)
Caso 1: Matrix Testing de Compatibilidad
Asegurar que tu librería de ML funciona en versiones antiguas y nuevas de Python.

```yaml

name: Compatibility Matrix
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - run: pip install -r requirements.txt
      - run: python -c "import sys; print(f'Testing on Python {sys.version}')"
      - run: pytest tests/
```
Caso 2: Entornos Virtuales y Dependencias de Desarrollo
Instalar dependencias extra solo para CI (como pytest o flake8) sin ensuciar el requirements.txt de producción.

```yaml

steps:
  - name: Install Dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip install -e ".[dev]"  # Instala extras definidos en pyproject.toml
```
Caso 3: Ejecución de Notebooks (Opcional)
Si usas Jupyter Notebooks para experimentos, puedes validarlos en CI.

```yaml

steps:
  - name: Install Jupyter tools
    run: pip install papermill jupyter
    
  - name: Execute Notebook
    run: papermill notebooks/experiment.ipynb out.ipynb
