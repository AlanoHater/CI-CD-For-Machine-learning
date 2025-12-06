# 📚 Módulo 3: Find the Correct Combination

## 🎯 Objetivo del Módulo

Aprender a combinar efectivamente los diferentes componentes de GitHub Actions para crear workflows poderosos.

## 📖 Contenido

### 3.1 Combinaciones Básicas

#### Event + Job:
```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]
```

#### Job + Múltiples Steps:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```

### 3.2 Combinaciones Avanzadas

#### Dependencias entre Jobs:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]
  deploy:
    needs: test  # Espera a que test termine
    runs-on: ubuntu-latest
    steps: [...]
```

#### Servicios y Contenedores:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_PASSWORD: postgres
    steps: [...]
```

## 🎮 Ejercicios Prácticos

### Ejercicio 3.1: Job Dependencies
Crear workflow con jobs dependientes.

### Ejercicio 3.2: Services Integration
Usar base de datos en workflow.

### Ejercicio 3.3: Complex Workflow
Combinar múltiples componentes en un workflow complejo.

## ✅ Próximo Módulo

[Módulo 4: Design a Continuous Integration Workflow](../04-ci-design/) - Diseño de CI completo.
