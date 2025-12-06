# 📚 Módulo 1: Get Ready to Explore GitHub Actions (GHA)

## 🎯 Objetivo del Módulo

Entender los fundamentos de GitHub Actions como plataforma para CI/CD, sus componentes principales y cómo se integra con proyectos de Machine Learning.

## 📖 Contenido

### 1.1 ¿Qué es GitHub Actions?

**GitHub Actions (GHA)** es una plataforma de **CI/CD** integrada directamente en GitHub que permite automatizar workflows de desarrollo, testing y despliegue.

#### Características Clave:
- ✅ **Integración nativa** con repositorios GitHub
- ✅ **Infraestructura cloud** (runners gratuitos)
- ✅ **Ecosistema rico** de actions pre-construidas
- ✅ **YAML-based** configuración
- ✅ **Multi-plataforma** (Linux, Windows, macOS)

### 1.2 Arquitectura Básica

```
Evento → Workflow → Job → Step → Action
   ↓       ↓        ↓      ↓       ↓
 Push   YAML     Runner  Comando  Script
```

### 1.3 Componentes Principales

#### 🎯 **Workflow**
- Archivo YAML que define el proceso automatizado completo
- Ubicación: `.github/workflows/nombre.yml`
- Activado por eventos específicos

#### ⚡ **Event**
- Disparador que inicia el workflow
- Tipos comunes: `push`, `pull_request`, `schedule`
- Configurable por ramas y tipos específicos

#### 🧱 **Job**
- Conjunto de steps que se ejecutan en el mismo runner
- Pueden ejecutarse en paralelo o secuencialmente
- Cada job es independiente por defecto

#### 🚶 **Step**
- Tarea individual dentro de un job
- Puede ser un comando shell o una action
- Se ejecutan en orden secuencial

#### 🛠️ **Action**
- Aplicación reusable que realiza tareas complejas
- Desarrolladas por GitHub o la comunidad
- Sintaxis: `uses: owner/action-name@version`

#### 💻 **Runner**
- Máquina virtual donde se ejecuta el job
- Opciones: `ubuntu-latest`, `windows-latest`, `macos-latest`
- Hosted runners (gratuitos) o self-hosted

#### 📝 **Context**
- Variables de entorno y metadatos
- Información sobre el evento, repo, usuario
- Sintaxis: `${{ github.event_name }}`

## 🔍 Analogías con Machine Learning

| Componente GHA | Analogía ML | Ejemplo |
|----------------|-------------|---------|
| **Workflow** | Proyecto ML completo | Entrenamiento end-to-end |
| **Event** | Trigger de reentrenamiento | Nuevos datos disponibles |
| **Job** | Fase del proyecto | Preprocessing de datos |
| **Step** | Paso específico | Normalizar features |
| **Action** | Librería ML | scikit-learn |
| **Runner** | Hardware de entrenamiento | GPU/CPU instance |
| **Context** | Metadata del experimento | Parámetros del modelo |

## 🚀 Primeros Pasos Prácticos

### Paso 1: Crear tu primer workflow

```yaml
# .github/workflows/hello-world.yml
name: Hello World Workflow

on: [push]  # Se ejecuta en cualquier push

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Hello World
        run: echo "¡Hola, GitHub Actions!"
```

### Paso 2: Verificar funcionamiento

1. **Crear el archivo** en `.github/workflows/`
2. **Hacer commit y push**
3. **Ir a la pestaña "Actions"** en GitHub
4. **Ver el workflow ejecutándose**

### Paso 3: Explorar logs

- Click en el workflow ejecutado
- Explorar cada job y step
- Ver outputs y errores
- Entender timing de ejecución

## 📋 Checklist de Aprendizaje

- [ ] Entender qué es GitHub Actions
- [ ] Conocer los 7 componentes principales
- [ ] Crear primer workflow básico
- [ ] Ejecutar workflow y ver logs
- [ ] Entender analogías con ML

## 🎮 Ejercicios Prácticos

### Ejercicio 1.1: Workflow de Bienvenida
Crear un workflow que se ejecute en todos los pushes y diga "Bienvenido a GHA"

### Ejercicio 1.2: Explorar Context
Crear un workflow que imprima información del contexto (usuario, repo, branch)

### Ejercicio 1.3: Múltiples Jobs
Crear un workflow con 2 jobs que se ejecuten en paralelo

## 📚 Recursos Adicionales

- [Documentación oficial GHA](https://docs.github.com/en/actions)
- [Marketplace de Actions](https://github.com/marketplace?type=actions)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## ✅ Criterios de Éxito

- ✅ Puedes explicar qué hace cada componente de GHA
- ✅ Has creado y ejecutado al menos 3 workflows básicos
- ✅ Entiendes cómo leer logs de GHA
- ✅ Puedes relacionar GHA con conceptos de ML

## 🎯 Próximo Módulo

Cuando completes este módulo, estarás listo para [02-yaml-intermediate](02-yaml-intermediate/) donde aprenderás YAML avanzado para workflows complejos.

---

**Nota**: Este módulo está diseñado para darte una base sólida. ¡Los conceptos aquí son fundamentales para todo lo que sigue!
