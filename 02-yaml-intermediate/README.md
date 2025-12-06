# 📚 Módulo 2: Intermediate YAML

## 🎯 Objetivo del Módulo

Dominar la sintaxis YAML avanzada necesaria para crear workflows complejos de GitHub Actions.

## 📖 Contenido

### 2.1 Estructura YAML Básica

YAML (YAML Ain't Markup Language) es un formato de serialización de datos legible por humanos.

#### Elementos Básicos:
```yaml
# Comentarios empiezan con #
key: value                    # String
key: 123                      # Número
key: true                     # Booleano
key: [item1, item2, item3]     # Lista
key:                          # Diccionario
  subkey1: value1
  subkey2: value2
```

### 2.2 YAML en GitHub Actions

#### Estructura de Workflow:
```yaml
name: Nombre del workflow          # Opcional
on:                                # Requerido - Eventos
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:                             # Requerido - Jobs
  job_name:
    runs-on: ubuntu-latest        # Requerido
    steps:                        # Requerido - Pasos
      - name: Paso 1
        run: comando
```

### 2.3 Sintaxis Avanzada

#### Variables y Context:
```yaml
env:
  NODE_VERSION: '18'
  API_KEY: ${{ secrets.API_KEY }}

steps:
  - name: Use variable
    run: echo "Version: $NODE_VERSION"

  - name: Use context
    run: echo "Branch: ${{ github.ref_name }}"
```

#### Matrices (Matrix):
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [16, 18, 20]

runs-on: ${{ matrix.os }}
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node }}
```

#### Condicionales:
```yaml
steps:
  - name: Deploy to production
    if: github.ref == 'refs/heads/main'
    run: deploy-production.sh
```

## 🎮 Ejercicios Prácticos

### Ejercicio 2.1: Variables de Entorno
Crear un workflow que use variables de entorno globales y locales.

### Ejercicio 2.2: Matrix Strategy
Crear un workflow que testee en múltiples versiones de Python.

### Ejercicio 2.3: Condicionales
Crear un workflow que se comporte diferente según el branch.

## 📋 Checklist de Aprendizaje

- [ ] Entender sintaxis YAML básica y avanzada
- [ ] Usar variables y context en workflows
- [ ] Implementar matrices para testing paralelo
- [ ] Aplicar condicionales en steps

## ✅ Próximo Módulo

[Módulo 3: Find the Correct Combination](../03-gha-components/) - Combinar componentes efectivamente.
