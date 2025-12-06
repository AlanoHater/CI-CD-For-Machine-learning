# 💻 Ejercicios Prácticos - Módulo 2: YAML Intermedio

## 🎯 Objetivo

Dominar la sintaxis YAML avanzada necesaria para workflows complejos de GitHub Actions.

## 📋 Lista de Ejercicios

### Ejercicio 2.1: Variables de Entorno y Context ⭐⭐

**Objetivo**: Aprender a usar variables de entorno y contexto de GitHub.

**Tareas**:
1. Crear workflow que use variables globales de entorno
2. Mostrar información del contexto de GitHub (actor, repo, branch)
3. Usar variables en steps individuales
4. Combinar variables de entorno con context

**Solución esperada**:
```yaml
name: Environment Variables Demo

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.10'

on: [push, pull_request]

jobs:
  demo:
    runs-on: ubuntu-latest
    env:
      JOB_ENV: 'demo_job'
    steps:
      - name: Show global env vars
        run: |
          echo "Node version: $NODE_VERSION"
          echo "Python version: $PYTHON_VERSION"

      - name: Show GitHub context
        run: |
          echo "Actor: ${{ github.actor }}"
          echo "Repository: ${{ github.repository }}"
          echo "Branch: ${{ github.ref_name }}"
          echo "Event: ${{ github.event_name }}"

      - name: Show job env var
        run: echo "Job env: $JOB_ENV"
```

---

### Ejercicio 2.2: Matrix Strategy Básico ⭐⭐⭐

**Objetivo**: Usar matrix strategy para testing en múltiples entornos.

**Tareas**:
1. Crear matrix con diferentes versiones de Python
2. Ejecutar tests en cada versión
3. Mostrar versión de Python en cada job
4. Verificar que todos los jobs pasen

**Solución esperada**:
```yaml
name: Matrix Testing

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Show Python version
        run: python --version
      - name: Run tests
        run: |
          python -c "print('Tests passed for Python ${{ matrix.python-version }}')"
```

---

### Ejercicio 2.3: Matrix Strategy Avanzado ⭐⭐⭐⭐

**Objetivo**: Matrix con múltiples dimensiones (OS y Python).

**Tareas**:
1. Crear matrix 2D: OS × Python versions
2. Excluir combinaciones problemáticas
3. Incluir combinaciones específicas
4. Mostrar información de cada combinación

**Solución esperada**:
```yaml
name: Advanced Matrix

on: [push]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']
        exclude:
          # Excluir Python 3.11 en Windows (ejemplo)
          - os: windows-latest
            python-version: '3.11'
        include:
          # Agregar combinación específica
          - os: ubuntu-latest
            python-version: '3.12'
            node-version: '18'
    steps:
      - name: Show matrix info
        run: |
          echo "OS: ${{ matrix.os }}"
          echo "Python: ${{ matrix.python-version }}"
          echo "Node: ${{ matrix.node-version }}"
```

---

### Ejercicio 2.4: Condicionales Básicos ⭐⭐⭐

**Objetivo**: Usar condicionales para controlar ejecución de steps.

**Tareas**:
1. Crear step que solo ejecute en main branch
2. Crear step que solo ejecute en pull requests
3. Crear step que solo ejecute en pushes (no PRs)
4. Combinar múltiples condiciones

**Solución esperada**:
```yaml
name: Conditional Steps

on: [push, pull_request]

jobs:
  conditional:
    runs-on: ubuntu-latest
    steps:
      - name: Always runs
        run: echo "This step always runs"

      - name: Only on main branch
        if: github.ref == 'refs/heads/main'
        run: echo "Only runs on main branch"

      - name: Only on pull requests
        if: github.event_name == 'pull_request'
        run: echo "Only runs on pull requests"

      - name: Only on push (not PR)
        if: github.event_name == 'push' && github.ref != 'refs/heads/main'
        run: echo "Only runs on push to non-main branches"

      - name: Complex condition
        if: contains(github.event.head_commit.message, '[deploy]')
        run: echo "Only runs when commit message contains [deploy]"
```

---

### Ejercicio 2.5: Secrets y Variables Seguras ⭐⭐⭐⭐

**Objetivo**: Manejar información sensible en workflows.

**Tareas**:
1. Configurar secrets en repository settings
2. Usar secrets en workflow
3. Crear variables de repository
4. Combinar secrets con condicionales

**Solución esperada**:
```yaml
name: Secrets and Variables

on: [push]

jobs:
  secrets-demo:
    runs-on: ubuntu-latest
    steps:
      - name: Use repository variable
        run: echo "App name: ${{ vars.APP_NAME }}"

      - name: Use secret (masked automatically)
        run: echo "API key length: ${{ secrets.API_KEY }}"
        # Nota: los secrets se enmascaran automáticamente en logs

      - name: Use secret in script
        if: github.ref == 'refs/heads/main'
        run: |
          # Pasar secret como env var (no se loguea)
          echo "Deploying with key: ***"
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}

      - name: Check if secrets exist
        run: |
          if [ -n "${{ secrets.API_KEY }}" ]; then
            echo "API_KEY is configured"
          else
            echo "API_KEY not configured"
          fi
```

---

## 🔍 Verificación de Resultados

### **Para cada ejercicio**:

1. **Crear archivo**: `.github/workflows/ejercicio-2-X.yml`
2. **Configurar secrets**: Si el ejercicio los requiere
3. **Hacer commit y push**
4. **Ver ejecución**: En Actions tab
5. **Verificar logs**: Cada step debe mostrar información correcta
6. **Capturar evidencia**: Screenshot de workflow exitoso

### **Checklist de validación**:

- [ ] Sintaxis YAML válida (sin errores de parsing)
- [ ] Variables de entorno funcionan correctamente
- [ ] Context variables muestran información correcta
- [ ] Matrix strategy ejecuta en todas las combinaciones
- [ ] Condicionales funcionan como esperado
- [ ] Secrets no se muestran en logs (aparecen como ***)

## 🆘 Troubleshooting Común

### **Problema**: `Unexpected value 'matrix'`
**Causa**: Matrix mal formateado
**Solución**: Verificar indentación y sintaxis

### **Problema**: Variables no se resuelven
**Causa**: Sintaxis incorrecta `${{ }}`
**Solución**: Asegurar doble llave y espacio correcto

### **Problema**: Secrets aparecen en logs
**Causa**: Imprimiendo secrets directamente
**Solución**: Nunca loguear secrets, usar como env vars

### **Problema**: Condicionales no funcionan
**Causa**: Operadores o sintaxis incorrecta
**Solución**: Revisar [documentación de expressions](https://docs.github.com/en/actions/learn-github-actions/expressions)

## 🎯 Criterios de Éxito

- ✅ Todos los ejercicios completados y funcionales
- ✅ Entendimiento completo de variables y context
- ✅ Matrix strategies funcionando correctamente
- ✅ Condicionales controlando flujo adecuadamente
- ✅ Secrets manejados de forma segura

## 📚 Próximos Pasos

Una vez completados estos ejercicios, estarás listo para [Módulo 3: Combinaciones Efectivas](../03-gha-components/) donde aprenderás a combinar múltiples componentes en workflows complejos.

---

**💡 Tip**: Crea una tabla de referencia con sintaxis YAML común para consultar rápidamente. Te será muy útil en módulos futuros.
