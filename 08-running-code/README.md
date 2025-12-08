---

### Módulo 8: `08-running-code/README.md`

# 📚 Módulo 8: Running Repository Code

## 🎯 Objetivo del Módulo

Aprender a ejecutar scripts propios, herramientas de CLI y código Python del repositorio dentro del entorno del runner.

## 📖 Contenido

### 8.1 Checkout Code
El paso fundamental. Sin esto, el runner está vacío.

```yaml
- uses: actions/checkout@v4
8.2 Casos de Uso Reales (Ejemplos)
Caso 1: Ejecución de Scripts de Utilidad
Ejecutar scripts de mantenimiento o generación de datos ubicados en tu carpeta scripts/ o examples/.
```
```yaml

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: '3.10'
  
  - name: Install dependencies
    run: pip install -r requirements.txt

  # Ejecuta el script de demostración del repositorio
  - name: Run ML Pipeline Demo
    run: python examples/demo-ml-pipeline.py
```

Caso 2: Permisos y Shell Scripts
A veces necesitas ejecutar scripts bash (.sh) para tareas de infraestructura o linting.

```yaml

steps:
  - uses: actions/checkout@v4
  
  - name: Run Linting Suite
    run: |
      chmod +x scripts/run-linting.sh  # Asegurar permisos de ejecución
      ./scripts/run-linting.sh         # Ejecutar script
```
Caso 3: Working Directory (Contexto de Ejecución)
Si tienes una estructura compleja (ej. src/ separado), usa working-directory para no tener que cambiar rutas en tus comandos.

```yaml

jobs:
  test-src:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./src  # Todos los 'run' se ejecutan aquí
    steps:
      - uses: actions/checkout@v4
      - run: ls -la  # Listará el contenido de src/, no la raíz
