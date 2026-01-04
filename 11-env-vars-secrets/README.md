# 📚 Módulo 11: Environment Variables and Secrets

## 🎯 Objetivo del Módulo

Aprender a manejar variables de entorno y secrets de forma segura en GitHub Actions.

## 📖 Contenido

### 11.1 Environment Variables

#### Variables globales:
```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com
```

#### Variables por step:
```yaml
steps:
  - name: Build
    env:
      BUILD_TYPE: release
    run: npm run build
```

#### Context variables:
```yaml
- name: Show context
  run: |
    echo "Repository: ${{ github.repository }}"
    echo "Branch: ${{ github.ref_name }}"
    echo "Actor: ${{ github.actor }}"
```

### 11.2 Secrets

#### Usar secrets:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: deploy.sh
```

#### GITHUB_TOKEN:
```yaml
- name: Create issue
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'New issue',
        body: 'Created by CI'
      })
```

### 11.3 Gestión Segura

#### Configurar secrets:
1. Ir a Settings → Secrets and variables → Actions
2. Agregar nuevos secrets
3. Usar en workflows con `${{ secrets.NOMBRE }}`

#### Buenas prácticas:
- Nunca logs con secrets
- Usar secrets para credenciales
- Variables de entorno para configuración no sensible

### 11.4 Casos de Uso Reales 

#### Caso 1: Despliegue con Credenciales Seguras
Inyectar claves de API solo en el momento de uso, manteniéndolas ocultas en los logs (`***`).

```yaml
name: Secure Deploy
on:
  push:
    branches: ['main']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Cloud
        env:
          # Se pasan como variables de entorno, NUNCA como argumentos de línea de comandos
          API_KEY: ${{ secrets.CLOUD_API_KEY }}
          REGION: 'us-east-1' # Configuración no sensible
        run: ./scripts/deploy.sh
```
Caso 2: Configuración Dinámica por Entorno
Usar variables para cambiar el comportamiento del pipeline según la rama (Dev vs Prod).

```yaml

name: Dynamic Config
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Configure Environment
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "ENV_NAME=production" >> $GITHUB_ENV
            echo "DB_HOST=prod-db.local" >> $GITHUB_ENV
          else
            echo "ENV_NAME=development" >> $GITHUB_ENV
            echo "DB_HOST=dev-db.local" >> $GITHUB_ENV
          fi
          
      - name: Show Config
        run: echo "Building for $ENV_NAME connecting to $DB_HOST"
```
Caso 3: Validar Existencia de Secretos
Evitar fallos silenciosos verificando si los secretos necesarios están configurados en el repo.

```yaml

steps:
  - name: Check Secrets
    env:
      HAS_TOKEN: ${{ secrets.HF_TOKEN != '' }}
    run: |
      if [ "$HAS_TOKEN" == "false" ]; then
        echo "❌ Error: El secreto HF_TOKEN no está configurado."
        exit 1
      fi
```

