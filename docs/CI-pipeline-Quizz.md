# =============================================================================
# QUIZ COMPLETO: CI PIPELINE PARA MACHINE LEARNING CON GITHUB ACTIONS
# =============================================================================
# Este quiz evalúa el entendimiento de Continuous Integration (CI) en el contexto
# de Machine Learning, GitHub Actions, y la interpretación de workflows YAML.
# Relacionado con: GHA-CI.sty y GHA-Pipeline-Example.yml
#
# Instrucciones:
# - Responde todas las preguntas
# - Para preguntas de código, proporciona la respuesta exacta
# - Las preguntas están organizadas por dificultad: Básico → Intermedio → Avanzado

---

## 📚 SECCIÓN 1: CONCEPTOS FUNDAMENTALES (BÁSICO)

### Pregunta 1.1: Definición de CI (Múltiple Choice)
¿Cuál de las siguientes es la definición más precisa de Continuous Integration?
a) Un proceso que ejecuta tests solo cuando se hace deploy a producción
b) Una práctica que integra automáticamente cambios de código y los valida con tests
c) Un sistema que guarda versiones del código sin validación automática
d) Una herramienta específica de GitHub para control de versiones

**Respuesta correcta: b**

### Pregunta 1.2: Rol de CI en ML (Verdadero/Falso)
En Machine Learning, CI es especialmente importante porque previene que cambios en el código
rompan pipelines de entrenamiento existentes.
**Verdadero/Falso:** Verdadero

### Pregunta 1.3: Componentes de GitHub Actions (Completar)
Completa la analogía: En GitHub Actions, un "_____" es como un proyecto ML completo,
mientras que un "_____" es como una fase específica del proyecto (e.g., preprocessing).
**Respuesta:** Workflow, Job

### Pregunta 1.4: Eventos en GHA (Selección Múltiple)
¿Cuáles de estos son eventos válidos en GitHub Actions? (Selecciona todas las correctas)
a) push
b) pull_request
c) merge_commit
d) issues
e) deployment
**Respuestas correctas: a, b, d, e**

---

## 🔧 SECCIÓN 2: INTERPRETACIÓN DEL WORKFLOW YAML (INTERMEDIO)

### Pregunta 2.1: Evento Principal (Interpretación de YAML)
Según el archivo GHA-Pipeline-Example.yml, ¿cuál es el evento más crítico que dispara el CI?
**Respuesta:** pull_request hacia la rama main

### Pregunta 2.2: Jobs en el Pipeline (Contar)
¿Cuántos jobs tiene definidos el workflow GHA-Pipeline-Example.yml?
**Respuesta:** 3 (code_quality, test, ml_validation)

### Pregunta 2.3: Dependencias entre Jobs (Análisis)
En el pipeline, ¿qué job debe completarse exitosamente antes de que se ejecute el job "test"?
**Respuesta:** code_quality

### Pregunta 2.4: Variables de Entorno (YAML Syntax)
¿Qué variable de entorno global se define en el workflow para la versión de Python?
**Respuesta:** PYTHON_VERSION: '3.10'

### Pregunta 2.5: Actions Utilizadas (Identificación)
¿Cuál de estas actions NO se utiliza en el pipeline GHA-Pipeline-Example.yml?
a) actions/checkout@v4
b) actions/setup-python@v5
c) codecov/codecov-action@v3
d) actions/setup-node@v3
**Respuesta correcta: d**

---

## 🧪 SECCIÓN 3: ACCIONES CONCRETAS EN CI (INTERMEDIO-AVANZADO)

### Pregunta 3.1: Categorías de Validación (Clasificación)
Según las notas en GHA-CI.sty, ¿cuáles son las dos categorías principales de acciones
que se ejecutan típicamente en un CI para ML?
**Respuesta:** 1) Pruebas Unitarias (Funcionalidad) - 2) Linting/Formato (Estilo)

### Pregunta 3.2: Herramientas de Linting (Múltiple Choice)
¿Cuáles de estas herramientas se recomiendan para linting en proyectos ML?
a) pytest
b) black
c) flake8
d) mypy
e) docker
**Respuestas correctas: b, c, d**

### Pregunta 3.3: Comando de Testing (Interpretación)
En el job "test", ¿qué comando se ejecuta para validar que los tests pasan?
**Respuesta:** if [ $? -ne 0 ]; then echo "❌ Tests fallaron - revisa la implementación"; exit 1; fi

### Pregunta 3.4: Cobertura de Código (Configuración)
¿Qué porcentaje mínimo de cobertura de código se requiere en el pipeline?
**Respuesta:** 80%

---

## 🤖 SECCIÓN 4: CONFIGURACIÓN ESPECÍFICA PARA ML (AVANZADO)

### Pregunta 4.1: Validación ML (Código Analysis)
En el job "ml_validation", ¿qué tipo de datos se generan para testing?
**Respuesta:** Datos sintéticos usando numpy (np.random.randn(100, 4))

### Pregunta 4.2: Modelo de Validación (ML Knowledge)
¿Qué tipo de modelo se utiliza en la validación ML del pipeline?
**Respuesta:** RandomForestClassifier de scikit-learn

### Pregunta 4.3: Métricas de Validación (Interpretación)
¿Qué métrica se calcula para validar que el modelo ML funciona correctamente?
**Respuesta:** Accuracy score (accuracy_score)

### Pregunta 4.4: Threshold de Validación (Configuración)
¿Cuál es el threshold mínimo de accuracy que debe superar el modelo en la validación?
**Respuesta:** 0.5 (50%)

---

## 🛠️ SECCIÓN 5: TROUBLESHOOTING Y MEJORES PRÁCTICAS (AVANZADO)

### Pregunta 5.1: Branch Protection (Configuración)
Según las notas al final del YAML, ¿cuáles son los tres requerimientos principales para
Branch Protection Rules?
**Respuesta:** 1) Require status checks to pass, 2) Require branches to be up to date before merging, 3) Include administrators

### Pregunta 5.2: Status Checks Requeridos (YAML Analysis)
¿Cuáles son los status checks que deben pasar antes de permitir un merge?
**Respuesta:** code_quality, test, ml_validation

### Pregunta 5.3: Problema de Linting (Debugging)
Si Black falla en el CI, ¿qué comando sugiere el pipeline para solucionarlo?
**Respuesta:** black src/ tests/

### Pregunta 5.4: Reportes de CI (GitHub Features)
¿Qué variable de entorno se utiliza para generar reportes en el summary de GitHub?
**Respuesta:** $GITHUB_STEP_SUMMARY

### Pregunta 5.5: Dependencies de Job (Workflow Logic)
¿Cuál es la lógica de dependencies en el pipeline? Explica por qué "ml_validation" necesita "test".
**Respuesta:** ml_validation solo se ejecuta si los tests unitarios pasan, asegurando que el código básico funcione antes de validar el pipeline ML completo.

---

## 💻 SECCIÓN 6: PREGUNTAS DE CÓDIGO (EXPERTO)

### Pregunta 6.1: Configuración de Evento (YAML Writing)
Escribe la configuración YAML correcta para que el workflow se ejecute solo en pull requests hacia main:
```yaml
# Tu respuesta aquí
```
**Respuesta correcta:**
```yaml
on:
  pull_request:
    branches: [ main ]
```

### Pregunta 6.2: Job con Dependencies (YAML Writing)
Escribe la configuración YAML para un job que depende de otro job llamado "lint":
```yaml
# Tu respuesta aquí
```
**Respuesta correcta:**
```yaml
jobs:
  my_job:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      # ... steps here
```

### Pregunta 6.3: Step de Linting (YAML Writing)
Escribe un step que ejecute flake8 en los directorios src/ y tests/:
```yaml
# Tu respuesta aquí
```
**Respuesta correcta:**
```yaml
- name: Run flake8
  run: flake8 src/ tests/ --max-line-length=88
```

### Pregunta 6.4: Validación ML (Python Code)
Escribe el código Python que valida que un modelo tiene accuracy > 0.7:
```python
# Tu respuesta aquí
```
**Respuesta correcta:**
```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true, y_pred)
assert accuracy > 0.7, f"Accuracy {accuracy:.3f} es menor al threshold 0.7"
```

---

## 📊 SECCIÓN 7: ANÁLISIS DE ESCENARIOS (EXPERTO)

### Escenario 7.1: Debug de Pipeline Fallido
**Situación:** El job "code_quality" falla en el step de Black.
**Pregunta:** ¿Qué acciones tomarías para solucionarlo?
**Respuesta esperada:**
1. Revisar los archivos que fallan el formateo
2. Ejecutar `black src/ tests/` localmente
3. Hacer commit de los cambios formateados
4. Push y re-ejecutar el CI

### Escenario 7.2: Tests que no pasan
**Situación:** Los tests pasan localmente pero fallan en CI.
**Pregunta:** ¿Cuáles podrían ser las causas y soluciones?
**Respuesta esperada:**
- **Causa:** Diferencias en dependencias o entorno
- **Solución:** Verificar requirements.txt, usar mismas versiones, revisar paths relativos

### Escenario 7.3: ML Validation falla
**Situación:** El job ml_validation falla con "Accuracy muy baja".
**Pregunta:** ¿Qué investigarías?
**Respuesta esperada:**
- Revisar la generación de datos sintéticos
- Verificar que el modelo se entrena correctamente
- Considerar si el threshold (0.5) es apropiado para el caso de uso
- Revisar si hay problemas con las dependencias de ML

### Escenario 7.4: Branch Protection bloquea merge
**Situación:** Un PR no se puede mergear porque faltan status checks.
**Pregunta:** ¿Cómo configurarías Branch Protection Rules correctamente?
**Respuesta esperada:**
- Ir a Settings → Branches → Branch protection rules
- Seleccionar rama "main"
- Activar "Require status checks to pass"
- Agregar los checks: code_quality, test, ml_validation

---

## 🎯 SECCIÓN 8: EVALUACIÓN FINAL (SINTESIS)

### Pregunta 8.1: Diseño de Pipeline (Ensayo Corto)
Explica en 3-4 oraciones por qué este pipeline es adecuado para proyectos de ML,
mencionando al menos 3 características específicas.
**Puntos clave a cubrir:**
- Jobs separados para diferentes validaciones
- Enfoque en pull_request para validación previa
- Herramientas específicas para ML
- Cobertura de código y métricas

### Pregunta 8.2: Mejoras Sugeridas (Crítico Constructivo)
¿ Qué mejoras agregarías a este pipeline para un proyecto ML más complejo?
**Sugerencias posibles:**
- Matrix testing para múltiples versiones de Python
- Caching de dependencias para acelerar builds
- Security scanning con CodeQL
- Performance testing para modelos
- Integration con MLflow para tracking de experimentos

---

## 📋 CLAVE DE RESPUESTAS (PARA REVISIÓN)

### Resumen de Puntajes:
- Sección 1 (Básico): 4 preguntas
- Sección 2 (Intermedio): 5 preguntas
- Sección 3 (Intermedio-Avanzado): 4 preguntas
- Sección 4 (Avanzado): 4 preguntas
- Sección 5 (Avanzado): 5 preguntas
- Sección 6 (Experto): 4 preguntas
- Sección 7 (Experto): 4 escenarios
- Sección 8 (Síntesis): 2 preguntas

### Puntuación Sugerida:
- Básico: 0-40 puntos
- Intermedio: 41-70 puntos
- Avanzado: 71-85 puntos
- Experto: 86-100 puntos

### Recursos Adicionales:
- Documentación oficial: https://docs.github.com/en/actions
- GHA-CI.sty (notas completas)
- GHA-Pipeline-Example.yml (pipeline de referencia)

---

*Este quiz ha sido diseñado para evaluar comprensión completa de CI en ML con GitHub Actions.
Las preguntas se basan directamente en el contenido de GHA-CI.sty y GHA-Pipeline-Example.yml.*
