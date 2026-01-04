### Módulo 11: `11-env-vars-secrets/exercises.md`

```markdown
# 💻 Ejercicios Prácticos - Módulo 11: Env Vars & Secrets

## 🎯 Objetivo
Manejar configuración sensible y no sensible de forma segura.

## 📋 Lista de Ejercicios

### Ejercicio 11.1: Jerarquía de Variables de Entorno ⭐⭐
**Objetivo**: Entender precedencia (Global vs Job vs Step).
**Tareas**:
1. Definir `VAR=Global` a nivel workflow.
2. Definir `VAR=Job` a nivel job.
3. Imprimir `$VAR` en un step (debería ser Job).
4. Sobrescribir en un step específico con `env`.

**Solución esperada**:
```yaml
name: Env Precedence
on: [push]
env:
  TEST_VAR: 'Global'

jobs:
  test-env:
    runs-on: ubuntu-latest
    env:
      TEST_VAR: 'Job'
    steps:
      - name: Print Job Var
        run: echo "Var is: $TEST_VAR" # Output: Job

      - name: Print Step Var
        env:
          TEST_VAR: 'Step'
        run: echo "Var is: $TEST_VAR" # Output: Step
Ejercicio 11.2: Uso Seguro de Secrets (Simulado) ⭐⭐⭐
Objetivo: Pasar secrets a scripts sin exponerlos. Tareas:

Asumir existencia de secrets.API_KEY (o usar uno ficticio).

Pasarlo como variable de entorno a un script Python.

Nunca imprimirlo en logs.

Solución esperada:

YAML

name: Secure Secrets
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Deploy Script
        env:
          # Se pasa como env var, NO como argumento de comando
          API_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Usamos token default para demo
        run: |
          # Simulación de script que usa la variable
          echo "Conectando con token longitud: ${#API_TOKEN}"
Ejercicio 11.3: GITHUB_TOKEN Permisos ⭐⭐⭐⭐
Objetivo: Modificar permisos del token automático. Tareas:

Definir bloque permissions.

Dar permiso solo de lectura a contents.

Intentar crear un archivo (fallará) o leer (funcionará).

Solución esperada:

YAML

name: Token Permissions
on: [push]

permissions:
  contents: read

jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Try to write (should fail push)
        run: |
          echo "test" > test.txt
          # No podemos hacer push porque el token es read-only
          # Esto es solo demostrativo de permisos
