### Módulo 8: `08-running-code/exercises.md`

```markdown
# 💻 Ejercicios Prácticos - Módulo 8: Running Repository Code

## 🎯 Objetivo
Dominar la action `checkout` y la ejecución de scripts alojados en el repositorio.

## 📋 Lista de Ejercicios

### Ejercicio 8.1: Checkout Básico y Listado ⭐⭐
**Objetivo**: Entender la estructura de directorios en el runner.
**Tareas**:
1. Usar `actions/checkout@v4`.
2. Listar archivos en la raíz (`ls -R`).
3. Verificar que `src/` existe.

**Solución esperada**:
```yaml
name: Checkout Demo
on: [push]
jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: List files
        run: ls -R
      - name: Check src
        run: test -d src && echo "src existe"
```
# 💻 Ejercicio 8.2: Ejecución de Script Shel

## 🎯 Objetivo
Dominar la action `checkout` y la ejecución de scripts alojados en el repositorio.

## 📋 Lista de Ejercicios

### Ejercicio 8.1: Checkout Básico y Listado ⭐⭐
**Objetivo**: EEjecutar scripts de mantenimiento (.sh).
**Tareas**:
1. Checkout del código.
2. Dar permisos de ejecución a scripts/run-linting.sh.
3. Ejecutar el script.

**Solución esperada**:
```yaml
name: Checkout Demo
on: [push]
jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: List files
        run: ls -R
      - name: Check src
        run: test -d src && echo "src existe"

```
# 💻 Ejercicio 8.3: Custom Working Directory

## 🎯 Objetivo
Ejecutar comandos dentro de subdirectorios específicos.
## 📋 Lista de Ejercicios

### Ejercicio 8.1: Checkout Básico y Listado ⭐⭐
**Objetivo**: EEjecutar scripts de mantenimiento (.sh).
**Tareas**:
1. Crear un job.
2. Definir defaults.run.working-directory como ./src.
3. Ejecutar ls (debe mostrar contenido de src, no root).

**Solución esperada**:
```yaml
name: Working Directory
on: [push]
jobs:
  src-check:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./src
    steps:
      - uses: actions/checkout@v4
      - run: ls -la # Listará contenido de src/
