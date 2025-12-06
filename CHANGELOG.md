# 📋 Changelog - MLOps GHA Learning

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 🚀 **Repositorio completamente estructurado** para aprendizaje de GitHub Actions en MLOps
- 📚 **Documentación completa** con 11 módulos de aprendizaje
- 💻 **Código de ejemplo** para ML (data_utils.py, model.py)
- 🧪 **Tests comprehensivos** (90+ tests unitarios)
- ⚙️ **CI/CD pipeline** funcional con múltiples jobs
- 🛠️ **Scripts de utilidad** para desarrollo y testing
- 📦 **Configuración profesional** (pyproject.toml, pre-commit, Docker)
- 🎯 **Sistema de seguimiento** de progreso personal
- 📖 **Quiz interactivo** para validación de aprendizaje
- 🤝 **Templates** para issues y pull requests
- 🏗️ **Makefile** para automatización de tareas comunes
- 🔄 **Orquestación ML con Prefect** - Workflows avanzados basados en DataCamp tutorial

### Changed
- N/A (versión inicial)

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- 🐛 Corregir todas las barras invertidas sin escapar en `pyproject.toml` que causaban errores en Black durante CI/CD
- 🐛 Solucionar expresiones regulares en configuración de coverage para compatibilidad con TOML

### Security
- 🔒 Configuración segura de secrets y variables de entorno
- 🛡️ Pre-commit hooks para validación de seguridad
- 🔍 Escaneo automático de secrets

---

## [0.1.0] - 2025-12-XX

### Added
- 🎯 **Módulo 1: Introducción a GHA** - Conceptos básicos y primeros workflows
- 📚 **Módulo 2: YAML Intermedio** - Variables, context y matrices
- 📖 **README completo** con guía de inicio
- 📊 **Sistema de progreso** personal
- 🚀 **Primer CI pipeline** funcional

### Changed
- Estructura inicial del repositorio

---

## 📝 Guía para Mantener el Changelog

### Tipos de Cambios
- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades obsoletas
- **Removed**: Funcionalidades eliminadas
- **Fixed**: Corrección de bugs
- **Security**: Cambios relacionados con seguridad

### Formato de Versiones
- **MAJOR.MINOR.PATCH** (ej: 1.0.0)
- **MAJOR**: Cambios incompatibles
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Corrección de bugs

### Commits Convencionales
```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: cambios de formato
refactor: refactoring de código
test: agregar o modificar tests
chore: cambios de mantenimiento
```

### Ejemplos de Entradas

#### Nueva Funcionalidad
```
### Added
- ✨ Nueva funcionalidad de análisis de datos en `src/analytics.py`
- 🧪 Tests unitarios para nueva funcionalidad
- 📚 Documentación de la nueva API
```

#### Corrección de Bug
```
### Fixed
- 🐛 Error en cálculo de métricas cuando dataset está vacío
- 🔧 Validación mejorada de parámetros de entrada
```

#### Cambio Breaking
```
### Changed
- 💥 **BREAKING**: Cambiada API de `process_data()` - ahora requiere parámetro `validate_input`
- 🔄 Migración automática disponible en `scripts/migrate_v1_to_v2.py`
```

---

## 🤝 Contribución al Changelog

### Proceso
1. **Commits**: Usa [Conventional Commits](https://conventionalcommits.org/)
2. **PRs**: Incluye descripción de cambios en el PR
3. **Release**: Actualiza changelog antes de cada release
4. **Version**: Incrementa versión según semver

### Tools de Ayuda
```bash
# Generar changelog automáticamente
pip install git-changelog
git-changelog -o CHANGELOG.md

# Validar formato de commits
pip install commitizen
cz check
```

---

*Para más información sobre cómo contribuir, ver [CONTRIBUTING.md](CONTRIBUTING.md)*
