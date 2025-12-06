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

## ⏳ Estado: Pendiente

Crear ejemplos prácticos de manejo seguro de secrets y variables.
