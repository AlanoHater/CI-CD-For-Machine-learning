# 💻 Ejercicios Prácticos - Módulo 1: GitHub Actions Básico

## 🎯 Objetivo

Aplicar los conceptos aprendidos creando workflows funcionales de GitHub Actions.

## 📋 Lista de Ejercicios

### Ejercicio 1.1: Workflow de Bienvenida ⭐⭐

**Objetivo**: Crear un workflow básico que salude cuando hay un push.

**Tareas**:
1. Crear archivo `.github/workflows/welcome.yml`
2. Configurar para que se ejecute en todos los pushes
3. Agregar step que imprima "¡Bienvenido a GitHub Actions!"
4. Probar haciendo push y verificando en Actions tab

**Solución esperada**:
```yaml
name: Welcome Workflow

on: [push]

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - name: Welcome Message
        run: echo "¡Bienvenido a GitHub Actions!"
```

---

### Ejercicio 1.2: Explorando Context ⭐⭐⭐

**Objetivo**: Usar variables de contexto para mostrar información del evento.

**Tareas**:
1. Crear workflow que se ejecute en pull requests
2. Mostrar información del usuario que hizo el PR
3. Mostrar nombre del repositorio y branch
4. Mostrar tipo de evento

**Solución esperada**:
```yaml
name: Context Explorer

on: [pull_request]

jobs:
  explore:
    runs-on: ubuntu-latest
    steps:
      - name: Show Context Info
        run: |
          echo "Usuario: ${{ github.actor }}"
          echo "Repositorio: ${{ github.repository }}"
          echo "Branch: ${{ github.ref_name }}"
          echo "Evento: ${{ github.event_name }}"
```

---

### Ejercicio 1.3: Múltiples Jobs Paralelos ⭐⭐⭐

**Objetivo**: Crear workflow con jobs que se ejecuten en paralelo.

**Tareas**:
1. Crear 3 jobs independientes
2. Cada job debe imprimir un mensaje diferente
3. Configurar para que se ejecuten en paralelo (por defecto)
4. Verificar timing en logs

**Solución esperada**:
```yaml
name: Parallel Jobs

on: [push]

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: Job 1 Task
        run: echo "Ejecutando Job 1"

  job2:
    runs-on: ubuntu-latest
    steps:
      - name: Job 2 Task
        run: echo "Ejecutando Job 2"

  job3:
    runs-on: ubuntu-latest
    steps:
      - name: Job 3 Task
        run: echo "Ejecutando Job 3"
```

---

### Ejercicio 1.4: Diferentes Runners ⭐⭐⭐⭐

**Objetivo**: Experimentar con diferentes sistemas operativos.

**Tareas**:
1. Crear jobs para Ubuntu, Windows y macOS
2. Cada job debe mostrar información del sistema
3. Usar comandos específicos de cada OS
4. Comparar tiempos de ejecución

**Solución esperada**:
```yaml
name: Multi-OS Workflow

on: [push]

jobs:
  ubuntu:
    runs-on: ubuntu-latest
    steps:
      - name: Ubuntu Info
        run: |
          echo "Sistema: $(uname -a)"
          echo "Directorio: $(pwd)"

  windows:
    runs-on: windows-latest
    steps:
      - name: Windows Info
        run: |
          echo "Sistema: $env:OS"
          echo "Directorio: $pwd"

  macos:
    runs-on: macos-latest
    steps:
      - name: macOS Info
        run: |
          echo "Sistema: $(uname -a)"
          echo "Directorio: $(pwd)"
```

---

### Ejercicio 1.5: Usando Actions ⭐⭐⭐⭐

**Objetivo**: Incorporar actions pre-construidas.

**Tareas**:
1. Usar `actions/checkout@v4` para obtener código
2. Usar `actions/setup-python@v5` para configurar Python
3. Instalar dependencias desde requirements.txt
4. Ejecutar un script Python simple

**Solución esperada**:
```yaml
name: Using Actions

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Python script
        run: python hello.py
```

---

## 🔍 Verificación de Resultados

### Para cada ejercicio:

1. **Crear el archivo** en `.github/workflows/`
2. **Hacer commit y push**
3. **Ir a Actions tab** en GitHub
4. **Verificar que el workflow se ejecuta**
5. **Revisar logs** de cada step
6. **Capturar screenshot** del resultado exitoso

### Checklist de validación:

- [ ] Workflow se activa en el evento correcto
- [ ] Todos los jobs completan exitosamente
- [ ] Logs muestran la información esperada
- [ ] No hay errores de sintaxis YAML

## 🆘 Troubleshooting

### Problema común 1: YAML inválido
**Síntoma**: Workflow no aparece en Actions
**Solución**: Validar YAML en [yaml-validator](http://www.yamllint.com/)

### Problema común 2: Actions no found
**Síntoma**: Error "action not found"
**Solución**: Verificar sintaxis `uses: owner/action@version`

### Problema común 3: Context vacío
**Síntoma**: Variables `${{ }}` no se resuelven
**Solución**: Asegurar sintaxis correcta y contexto disponible

## 🎯 Criterios de Éxito

- ✅ Todos los ejercicios completados
- ✅ Workflows funcionales en GitHub
- ✅ Entendimiento de logs y debugging
- ✅ Capacidad para crear workflows básicos
- ✅ Conocimiento de actions comunes

## 📚 Próximos Pasos

Una vez completados estos ejercicios, estarás listo para el [Módulo 2: YAML Intermedio](../02-yaml-intermediate/) donde aprenderás sintaxis YAML avanzada para workflows complejos.

---

**💡 Tip**: Documenta tus aprendizajes y errores en un archivo `notes.md` en cada ejercicio. ¡Será útil para referencia futura!
