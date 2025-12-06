# 📚 Módulo 8: Running Repository Code

## 🎯 Objetivo del Módulo

Aprender a ejecutar código del repositorio dentro de workflows de GitHub Actions.

## 📖 Contenido

### 8.1 Checkout Code

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
    with:
      ref: main  # branch específica
      path: repo # directorio destino
```

### 8.2 Ejecutar Scripts

#### Python:
```yaml
- name: Run Python script
  run: python scripts/train_model.py
```

#### Shell scripts:
```yaml
- name: Run shell script
  run: bash scripts/deploy.sh
```

### 8.3 Working Directory

```yaml
- name: Change directory
  run: cd src && python main.py
```

## ⏳ Estado: Pendiente

Crear ejemplos prácticos de ejecución de código repositorio.
