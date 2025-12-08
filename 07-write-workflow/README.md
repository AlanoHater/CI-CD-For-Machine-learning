# 📚 Módulo 7: Write a GitHub Actions Workflow

## 🎯 Objetivo del Módulo

Crear workflows de GitHub Actions desde cero para casos específicos.

## 📖 Contenido

### 7.1 Proceso de Escritura

1. **Definir objetivo**: ¿Qué automatizar?
2. **Elegir eventos**: ¿Cuándo ejecutar?
3. **Planear jobs**: ¿Qué tareas?
4. **Seleccionar steps**: ¿Cómo implementar?
5. **Probar**: Validar funcionamiento

### 7.2 Templates Comunes

#### CI Básico:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test  # o python test
```

#### Deploy:
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: deploy-to-production
```

