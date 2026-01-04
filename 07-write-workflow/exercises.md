# 💻 Ejercicios Prácticos - Módulo 7: Write a GitHub Actions Workflow

## 🎯 Objetivo
Diseñar y escribir workflows desde cero para casos de uso específicos que van más allá del trigger `push` estándar.

## 📋 Lista de Ejercicios

### Ejercicio 7.1: Workflow Manual (Dispatch) 
**Objetivo**: Crear un workflow que solo se active manualmente desde la interfaz de GitHub.
**Tareas**:
1. Configurar el trigger `workflow_dispatch`.
2. Definir un input llamado `log_level` (opciones: info, debug, warn).
3. Imprimir el valor seleccionado en un step.

**Solución esperada**:
```yaml
name: Manual Trigger
on:
  workflow_dispatch:
    inputs:
      log_level:
        description: 'Log Level'
        required: true
        default: 'info'
        type: choice
        options:
        - info
        - debug
        - warn
```
jobs:
  print-input:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Log level seleccionado: ${{ inputs.log_level }}"
### Ejercicio 7.2:cheduled Workflow (Cron)
**Objetivo**: Ejecutar una tarea recurrente (ej. reentrenamiento semanal).
**Tareas**:
1. Configurar trigger schedule
2. Definir cron para ejecutar todos los lunes a las 8:00 AM UTC.
3. Imprimir la fecha actual.
**Solución esperada**:
```yaml
name: Weekly Retrain
on:
  schedule:
    - cron: '0 8 * * 1' # Lunes 8am UTC

jobs:
  cron-job:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Ejecutando tarea programada: $(date)"
