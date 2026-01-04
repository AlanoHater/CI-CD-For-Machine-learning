### Módulo 9: `09-feature-branches/exercises.md`

```markdown
# 💻 Ejercicios Prácticos - Módulo 9: Feature Branches

## 🎯 Objetivo
Configurar CI diferenciado según la rama (Git Flow) y protección de ramas.

## 📋 Lista de Ejercicios

### Ejercicio 9.1: CI Específico para Feature Branches ⭐⭐⭐
**Objetivo**: Workflow que corre tests rápidos en ramas `feature/*` y completos en `main`.
**Tareas**:
1. Trigger `push` para `main` y `feature/**`.
2. Usar condicional `if` para detectar la rama.
3. Echo "Fast tests" si es feature, "Full tests" si es main.

**Solución esperada**:
```yaml
name: Branch Strategy
on:
  push:
    branches:
      - main
      - 'feature/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Feature Branch Checks
        if: startsWith(github.ref, 'refs/heads/feature/')
        run: echo "Ejecutando tests rápidos..."

      - name: Main Branch Checks
        if: github.ref == 'refs/heads/main'
        run: echo "Ejecutando suite completa..."
