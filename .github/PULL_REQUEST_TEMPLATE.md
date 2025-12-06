## 📋 Descripción

[Breve descripción de los cambios realizados]

## 🎯 Tipo de Cambio

- [ ] 🐛 **Bug fix** (cambio que arregla un problema)
- [ ] ✨ **New feature** (cambio que añade funcionalidad)
- [ ] 💥 **Breaking change** (cambio que rompe compatibilidad)
- [ ] 📚 **Documentation** (cambios en documentación)
- [ ] 🎨 **Style** (cambios de formato, linting)
- [ ] ♻️ **Refactor** (cambio que no arregla bug ni añade feature)
- [ ] ⚡ **Performance** (cambio que mejora performance)
- [ ] ✅ **Tests** (añadiendo o modificando tests)
- [ ] 🔧 **CI/CD** (cambios en configuración de CI/CD)

## 📋 Checklist

### ✅ Código
- [ ] Mi código sigue las guías de estilo del proyecto
- [ ] He ejecutado linting localmente (`./scripts/run-linting.sh`)
- [ ] He ejecutado tests localmente (`./scripts/run-tests.sh`)

### ✅ Tests
- [ ] He añadido tests que cubren mis cambios
- [ ] Todos los tests pasan
- [ ] Coverage > 80%

### ✅ Documentación
- [ ] He actualizado la documentación relevante
- [ ] He añadido docstrings a nuevas funciones
- [ ] He actualizado el README si aplica

### ✅ CI/CD
- [ ] El pipeline de CI pasa completamente
- [ ] He verificado que no rompe funcionalidades existentes
- [ ] He probado los cambios en un entorno similar a producción

## 🔍 ¿Cómo probar?

[Pasos detallados para probar los cambios]

```bash
# Ejemplo de comandos para testing
git checkout [branch-name]
python examples/demo-ml-pipeline.py
pytest tests/ -v
```

## 📊 Impacto

### 🔄 Cambios Breaking
[Lista de cambios que podrían romper compatibilidad]

### 📈 Mejoras de Performance
[Si aplica, métricas de mejora]

### 🛡️ Seguridad
[Cambios relacionados con seguridad]

## 🎯 Issues Relacionados

- Closes #[número de issue]
- Relates to #[número de issue]

## 💡 Información Adicional

[Cualquier información extra que el reviewer deba saber]

## 📸 Screenshots/Demos

[Si aplica, capturas de pantalla o demos de la funcionalidad]

---

**Nota**: Asegúrate de que el CI pase completamente antes de solicitar review. Los reviewers se enfocarán en la calidad del código y arquitectura de la solución.
