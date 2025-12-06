# 📚 Módulo 9: Feature Branches in Shared Repository Model

## 🎯 Objetivo del Módulo

Entender el flujo de trabajo con ramas feature en repositorios compartidos.

## 📖 Contenido

### 9.1 Git Flow Básico

```
main (stable)
├── feature/new-model
├── feature/bug-fix
└── hotfix/critical-bug
```

### 9.2 CI en Feature Branches

#### Ejecutar CI en todas las branches:
```yaml
on:
  push:
  pull_request:
    branches: [main, develop]
```

#### Solo en branches específicas:
```yaml
on:
  push:
    branches: [main, 'feature/**']
```

### 9.3 Branch Protection

Configurar reglas para proteger `main`:
- Require PR reviews
- Require status checks
- Require up-to-date branches

## ⏳ Estado: Pendiente

Crear guía completa para manejo de feature branches.
