# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto **MLOps GHA Learning**! Este documento describe cómo puedes contribuir de manera efectiva.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Tipos de Contribuciones](#tipos-de-contribuciones)
- [Estándares de Código](#estándares-de-código)
- [Testing](#testing)
- [Documentación](#documentación)

## 🤝 Código de Conducta

Este proyecto sigue un código de conducta para asegurar un entorno inclusivo y respetuoso. Al participar, aceptas:

- **Respeto**: Trata a todos con respeto y consideración
- **Colaboración**: Ayuda a otros contribuidores
- **Calidad**: Contribuye con código y documentación de calidad
- **Comunicación**: Sé claro y constructivo en tus comunicaciones

## 🚀 Cómo Contribuir

### 1. Elige un Issue
- Revisa los [issues abiertos](https://github.com/your-username/MLOps-GHA-Learning/issues)
- Elige uno que puedas resolver
- Si no hay issues que te interesen, [crea uno nuevo](https://github.com/your-username/MLOps-GHA-Learning/issues/new)

### 2. Fork y Clone
```bash
git clone https://github.com/your-username/MLOps-GHA-Learning.git
cd MLOps-GHA-Learning
git checkout -b feature/nueva-funcionalidad
```

### 3. Configura el Entorno
```bash
make setup  # Configura todo el entorno de desarrollo
```

### 4. Desarrolla
```bash
# Sigue el proceso de desarrollo descrito abajo
make test    # Ejecuta tests
make lint    # Verifica calidad de código
```

### 5. Crea un Pull Request
- Asegúrate de que todos los tests pasan
- Actualiza la documentación si es necesario
- Usa el template de PR proporcionado

## 🛠️ Configuración del Entorno

### Prerrequisitos
- Python 3.8+
- Git
- Make (opcional, pero recomendado)

### Configuración Automática
```bash
# Configuración completa
make setup

# O configuración manual
pip install -e ".[dev]"
pre-commit install
```

### Verificación
```bash
# Verificar que todo funciona
make ci  # Ejecuta linting, tests y build
```

## 🔄 Proceso de Desarrollo

### Flujo de Trabajo
1. **Elige tarea** → 2. **Crea branch** → 3. **Desarrolla** → 4. **Test** → 5. **Commit** → 6. **PR**

### Branches
- `main`: Código estable y liberado
- `develop`: Desarrollo activo
- `feature/nombre`: Nuevas funcionalidades
- `bugfix/nombre`: Corrección de bugs
- `docs/nombre`: Cambios en documentación

### Commits
Usa commits convencionales:
```
feat: agregar nueva funcionalidad
fix: corregir bug en módulo X
docs: actualizar documentación
test: agregar tests para funcionalidad Y
refactor: mejorar estructura de código
```

## 📝 Tipos de Contribuciones

### 💻 Código
- Nuevas funcionalidades
- Corrección de bugs
- Mejoras de performance
- Refactoring

### 🧪 Tests
- Tests unitarios
- Tests de integración
- Tests de extremo a extremo

### 📚 Documentación
- Guías de usuario
- Documentación de API
- Tutoriales
- Traducciones

### 🎨 Diseño
- Mejoras en UI/UX
- Diseño de diagramas
- Mejoras visuales

### 🐛 Reporte de Bugs
- Issues detallados con pasos para reproducir
- Sugerencias de solución

## 📏 Estándares de Código

### Python
- Sigue [PEP 8](https://pep8.org/)
- Usa [Black](https://black.readthedocs.io/) para formateo
- Usa [isort](https://pycqa.github.io/isort/) para imports
- Documenta con docstrings

### Ejemplo de Código
```python
def process_data(data: pd.DataFrame, target_col: str = "target") -> np.ndarray:
    """
    Procesa datos para ML.

    Args:
        data: DataFrame con datos
        target_col: Nombre de columna target

    Returns:
        Datos procesados como array

    Raises:
        ValueError: Si target_col no existe
    """
    if target_col not in data.columns:
        raise ValueError(f"Columna {target_col} no encontrada")

    # Procesamiento...
    return processed_data
```

### GitHub Actions
- Usa actions oficiales cuando sea posible
- Documenta workflows complejos
- Incluye manejo de errores
- Optimiza para velocidad

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
make test

# Tests unitarios
make test-unit

# Tests de integración
make test-integration

# Con cobertura
make test-coverage
```

### Escribir Tests
```python
import pytest
from src.module import function_to_test

class TestFunctionToTest:
    def test_basic_functionality(self):
        # Arrange
        input_data = "test"
        expected = "expected_result"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == expected

    def test_edge_cases(self):
        # Test casos límite
        pass

    def test_error_handling(self):
        # Test manejo de errores
        pass
```

### Cobertura
- Mínimo 80% de cobertura
- Incluye branches y condiciones
- Reportes en `htmlcov/`

## 📖 Documentación

### Estándares
- Usa Markdown para documentación
- Incluye ejemplos de código
- Mantén actualizado con cambios
- Traduce a múltiples idiomas si es posible

### Archivos Importantes
- `README.md`: Documentación principal
- `docs/`: Documentación detallada
- `examples/`: Ejemplos de uso

## 🔍 Pull Request Process

### Antes de Crear PR
- [ ] Tests pasan localmente
- [ ] Linting aprobado
- [ ] Documentación actualizada
- [ ] Cambios probados manualmente

### Template de PR
Usa el template proporcionado que incluye:
- Descripción clara de cambios
- Checklist de verificación
- Capturas de pantalla si aplica
- Referencias a issues

### Review Process
1. **Automated Checks**: CI ejecuta tests y linting
2. **Peer Review**: Al menos un reviewer aprueba
3. **Merge**: Squash merge con mensaje descriptivo

## 🎯 Métricas de Contribución

### Principiante
- Corregir typos
- Mejorar documentación
- Agregar tests simples

### Intermedio
- Implementar nuevas funcionalidades
- Corregir bugs complejos
- Refactorizar código

### Avanzado
- Diseñar nuevas arquitecturas
- Contribuir a roadmap
- Mentorear otros contribuidores

## 🆘 Obtener Ayuda

### Recursos
- 📖 [Documentación del proyecto](README.md)
- 💬 [Discussions](https://github.com/your-username/MLOps-GHA-Learning/discussions)
- 🐛 [Issues](https://github.com/your-username/MLOps-GHA-Learning/issues)
- 📧 [Email de contacto](mailto:learning@mlops.dev)

### Preguntas Frecuentes

**¿Cómo empiezo?**
Lee `START-HERE.md` y sigue el roadmap en `LEARNING-ROADMAP.md`

**¿Necesito experiencia previa?**
No, este proyecto está diseñado para aprender. ¡Todos empezamos en algún lugar!

**¿Cómo reporto un bug?**
Usa el template de bug report en Issues

## 🙏 Reconocimiento

¡Todos los contribuidores son reconocidos!
- Lista en `CONTRIBUTORS.md`
- Créditos en releases
- Menciones en documentación

---

**¡Gracias por contribuir a MLOps GHA Learning!** 🚀🤖

Tu contribución, no importa cuán pequeña, hace una diferencia en la comunidad de aprendizaje de MLOps.
