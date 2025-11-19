# 🚂 GUÍA COMPLETA: Railway Deployment

**Fecha:** 19 Nov 2025
**Problema:** Auto-deploy no funciona, Railway CLI no linked
**Solución:** 3 métodos alternativos para deployar

---

## 🔍 DIAGNÓSTICO

### Problema Identificado
```bash
$ railway status
Error: No linked project found

$ railway up
# No hace nada porque no está linked al proyecto
```

**Root Cause:**
- Railway CLI instalado ✅
- PERO no está conectado al proyecto zodiac-backend ❌
- Git pushes NO triggerearon auto-deploy ❌
- Servidor corriendo 54+ minutos sin reiniciar ❌

---

## 🎯 MÉTODOS DE DEPLOYMENT

### Método 1: Railway Dashboard (MÁS FÁCIL) ⭐

**Tiempo:** 2-3 minutos
**Requiere:** Acceso a dashboard web

#### Pasos:

1. **Abrir Railway Dashboard:**
   ```
   https://railway.app/
   ```

2. **Login** con tu cuenta

3. **Seleccionar proyecto:**
   - Click en "zodiac-backend" (o el nombre de tu proyecto)

4. **Ir a Deployments:**
   - En el menú lateral → Click "Deployments"

5. **Trigger nuevo deploy:**

   **Opción A - Redeploy último:**
   - Click en el deployment más reciente
   - Click botón **"Redeploy"**
   - Confirmar

   **Opción B - Deploy desde commit:**
   - Buscar commit `095facd` o `ad39fbf` en la lista
   - Click **"Deploy"** en ese commit
   - Confirmar

6. **Monitorear build:**
   - Ver logs en tiempo real
   - Esperar "✅ Build successful"
   - Esperar "✅ Deployment live"

7. **Verificar:**
   ```bash
   ./verificar_deploy_completo.sh
   ```

---

### Método 2: Railway CLI (Después de Link)

**Tiempo:** 5 minutos (incluye setup)
**Requiere:** Railway CLI + Project ID

#### Setup Inicial (una vez):

1. **Login a Railway:**
   ```bash
   railway login
   ```
   - Abre browser automáticamente
   - Autoriza la CLI

2. **Link al proyecto:**

   **Opción A - Interactive:**
   ```bash
   cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
   railway link
   ```
   - Selecciona tu team
   - Selecciona proyecto "zodiac-backend"
   - Selecciona environment "production"

   **Opción B - Direct (si conoces project ID):**
   ```bash
   railway link --project <PROJECT_ID>
   ```

3. **Verificar link:**
   ```bash
   railway status
   # Debe mostrar: Project: zodiac-backend
   ```

#### Deploy:

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend

# Opción 1: Deploy automático
railway up

# Opción 2: Deploy con logs
railway up --detach=false

# Opción 3: Deploy específico
railway up --service backend
```

#### Monitorear:

```bash
# Ver logs
railway logs

# Ver status
railway status

# Abrir dashboard
railway open
```

---

### Método 3: Git Push + Manual Trigger

**Tiempo:** 1 minuto (si auto-deploy está configurado)
**Requiere:** Auto-deploy habilitado en Railway

#### Verificar Auto-Deploy Settings:

1. **Dashboard → Settings → Deployments**
2. Verificar:
   - ✅ **Auto-Deploy:** Enabled
   - ✅ **Branch:** main
   - ✅ **Deploy on Push:** ON

#### Si está deshabilitado:

1. **Habilitar:**
   - Toggle "Deploy on Push" → ON
   - Save changes

2. **Trigger redeploy:**
   ```bash
   cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend

   # Empty commit
   git commit --allow-empty -m "chore: trigger Railway deploy"
   git push origin main
   ```

3. **Esperar 2-3 minutos:**
   ```bash
   ./monitor_railway.sh
   ```

---

### Método 4: GitHub Actions (Avanzado)

**Tiempo:** 30 minutos setup inicial
**Beneficio:** Deploy automático en cada PR merge

#### Setup:

1. **Crear workflow file:**

```yaml
# .github/workflows/railway-deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          cd backend/flutter-horoscope-backend
          railway up --service backend
```

2. **Obtener Railway Token:**
   ```bash
   railway token
   ```

3. **Añadir secret a GitHub:**
   - GitHub repo → Settings → Secrets
   - New secret: `RAILWAY_TOKEN`
   - Value: token copiado

4. **Push workflow:**
   ```bash
   git add .github/workflows/railway-deploy.yml
   git commit -m "ci: add Railway auto-deploy"
   git push origin main
   ```

---

## ✅ VERIFICACIÓN POST-DEPLOY

### Después de cualquier método:

1. **Esperar 2-3 minutos** (tiempo de build + deploy)

2. **Ejecutar script de verificación:**
   ```bash
   cd /Users/alejandrocaceres/Desktop/appstore.zodia
   ./verificar_deploy_completo.sh
   ```

3. **Debe mostrar:**
   ```
   ✅ VERSION NUEVA DEPLOYADA!
   Version: 2.2.0
   ✅ horoscopeData PRESENTE en response!
   ✅ ✅ ✅  BACKEND LISTO PARA TESTING  ✅ ✅ ✅
   ```

4. **Si ✅ → Continuar con Flutter testing**

---

## 🔧 TROUBLESHOOTING

### Issue 1: Railway CLI "No linked project"

**Error:**
```
No linked project found. Run railway link
```

**Solución:**
```bash
railway login
railway link
# Seleccionar proyecto zodiac-backend
```

---

### Issue 2: "Unauthorized" al deployar

**Error:**
```
Error: Unauthorized
```

**Solución:**
```bash
# Re-login
railway logout
railway login

# Verificar autenticación
railway whoami
```

---

### Issue 3: Build falla con "Module not found"

**Error en logs:**
```
Error: Cannot find module 'xyz'
```

**Solución:**
```bash
# Verificar package.json está actualizado
cat package.json

# Limpiar node_modules y rebuild
rm -rf node_modules package-lock.json
npm install
git add package-lock.json
git commit -m "chore: update dependencies"
git push origin main
```

---

### Issue 4: Deploy exitoso pero version sigue vieja

**Síntoma:**
```bash
curl .../health | jq '.version'
# Output: "2.1.1-production-gpt4omini"  ← Vieja
```

**Causas posibles:**

1. **Cache de CDN/Load Balancer:**
   ```bash
   # Forzar refresh
   curl -H "Cache-Control: no-cache" https://.../health
   ```

2. **Deployment en environment incorrecto:**
   - Verificar que deployaste en "production" (no "staging")
   - Dashboard → Deployments → Ver environment

3. **Railway usando old release:**
   - Dashboard → Settings → Rollback
   - Seleccionar deployment correcto manualmente

---

### Issue 5: Auto-deploy no funciona después de git push

**Verificar:**

1. **GitHub Webhook:**
   - GitHub repo → Settings → Webhooks
   - Debe haber webhook de Railway
   - Recent Deliveries debe mostrar "200 OK"

2. **Railway settings:**
   - Dashboard → Settings → Deployments
   - "Deploy on Push" debe estar ON

3. **Branch correcta:**
   - Verifica que pusheaste a `main` (no `master` u otra)

**Solución temporal:**
```bash
# Trigger manual después de cada push
railway up
```

---

## 📊 COMPARACIÓN DE MÉTODOS

| Método | Tiempo Setup | Tiempo Deploy | Facilidad | Recomendado |
|--------|-------------|---------------|-----------|-------------|
| 1. Dashboard | 0 min | 2-3 min | ⭐⭐⭐⭐⭐ | ✅ **SÍ** |
| 2. Railway CLI | 5 min | 2-3 min | ⭐⭐⭐⭐ | ✅ **SÍ** (después de setup) |
| 3. Git Auto-Deploy | 2 min | 2-3 min | ⭐⭐⭐⭐⭐ | ✅ **SÍ** (si configurado) |
| 4. GitHub Actions | 30 min | 2-3 min | ⭐⭐⭐ | No (overkill para este caso) |

---

## 🎯 RECOMENDACIÓN PARA AHORA

### Acción Inmediata: **Método 1 (Dashboard)**

**Por qué:**
- ✅ No requiere setup
- ✅ Más rápido (2-3 minutos)
- ✅ Visual feedback del build
- ✅ 100% confiable

**Pasos:**

1. **Abrir:** https://railway.app/
2. **Login** → Seleccionar proyecto "zodiac-backend"
3. **Deployments** → Click "Redeploy" en último deployment
4. **Esperar 2-3 min** viendo logs
5. **Cuando termine:**
   ```bash
   ./verificar_deploy_completo.sh
   ```

---

## 📚 DOCUMENTACIÓN RAILWAY

### Links Útiles:

- **Dashboard:** https://railway.app/
- **Docs CLI:** https://docs.railway.app/reference/cli-api
- **Docs Deployments:** https://docs.railway.app/deploy/deployments
- **Troubleshooting:** https://docs.railway.app/troubleshoot/general

### Comandos Útiles:

```bash
# Status
railway status
railway whoami

# Logs
railway logs
railway logs --tail

# Environment variables
railway variables
railway variables set KEY=value

# Open dashboard
railway open

# Link/unlink project
railway link
railway unlink

# Deploy
railway up
railway up --detach=false  # Con logs en vivo
```

---

## ✅ CHECKLIST DE DEPLOYMENT EXITOSO

Después de deployar por cualquier método:

- [ ] Railway dashboard muestra "✅ Deployment live"
- [ ] `curl .../health` devuelve version "2.2.0"
- [ ] Uptime es bajo (< 300 segundos)
- [ ] `./verificar_deploy_completo.sh` muestra ✅
- [ ] horoscopeData presente en response
- [ ] Flutter app (hot restart) muestra pill + highlights

---

## 🚀 DESPUÉS DE DEPLOYMENT EXITOSO

1. **Hot restart Flutter:**
   ```
   En terminal Flutter → Presionar: R
   ```

2. **Probar en iPhone:**
   - Abrir Cosmic Coach
   - Enviar: "¿Cómo está mi día?"
   - Verificar pill + highlights aparecen

3. **Si todo funciona:**
   ```
   🎊 LISTO PARA LAUNCH 🎊
   ```

---

**Generado:** 19 Nov 2025
**Siguiente acción:** Usar Método 1 (Dashboard) para deployar
**Tiempo estimado:** 2-3 minutos
**Verificación:** `./verificar_deploy_completo.sh`
