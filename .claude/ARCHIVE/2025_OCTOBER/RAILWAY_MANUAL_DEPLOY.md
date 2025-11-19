# 🚀 Railway Manual Deployment Instructions

## El problema
Railway CLI no puede deployar porque necesita linkear a un servicio específico de forma interactiva.

## ✅ Solución: Deploy Manual desde Dashboard

### Paso 1: Accede al Dashboard
1. Ve a https://railway.app/dashboard
2. Login con: laleshootingart@gmail.com

### Paso 2: Encuentra el Proyecto
1. Busca: **zodiac-backend-api**
2. Click en el proyecto

### Paso 3: Trigger Deployment
1. En la barra lateral, busca **"Deployments"**
2. Verás una lista de deployments previos
3. Click en **"Deploy"** o **"Redeploy Latest"**
4. Railway detectará automáticamente el nuevo código de GitHub

### Paso 4: Monitorear Deployment
1. Verás un log en tiempo real del build
2. Espera a que diga: **"✅ Build Successful"**
3. Luego verá: **"🚀 Deployment Live"**

### Paso 5: Verificar
```bash
# Test health endpoint
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/ai/goals/health

# Expected response:
{
  "success": true,
  "service": "goalPlanner",
  "status": "healthy"
}
```

## 🔄 Alternativa: GitHub Auto-Deploy

Si Railway está conectado a GitHub (debería estarlo):

1. Ve a **Settings** en Railway
2. Verifica que **"Auto Deploy"** esté **ON**
3. Verifica que esté conectado a: `https://github.com/Lalezito/flutter-horoscope-backend`
4. Verifica branch: `main`

Con auto-deploy activo, cada push a `main` triggerea deployment automático.

## ✅ Último Commit

```
commit 33b85c6
feat: add AI-powered Goal Planner for Stellar tier premium users

Includes:
- goalPlannerService.js (AI service)
- goalPlanner.js (API routes)
- Database migration
- Full documentation
```

Este commit **ya está en GitHub**, solo falta que Railway lo detecte.

## 🔍 Troubleshooting

### Si no ve el nuevo código:
1. Verify en GitHub que el commit está ahí: https://github.com/Lalezito/flutter-horoscope-backend/commits/main
2. En Railway, click en **"Sync with GitHub"** si hay esa opción
3. Trigger manual deploy

### Si el build falla:
1. Check Railway logs en tiempo real
2. Verifica que todas las dependencies estén en `package.json`
3. Verifica que `OPENAI_API_KEY` esté en variables

### Si el endpoint no funciona después:
1. Check Railway logs: `railway logs` (si logras linkear el servicio)
2. Verifica que la migration se ejecutó
3. Check `/health` endpoint para ver version number

## 📊 Status Actual

- ✅ Código en GitHub (commit 33b85c6)
- ✅ OpenAI key en Railway
- ✅ Project linkeado: zodiac-backend-api
- ⏳ Esperando deployment trigger

**Próximo paso**: Trigger manual desde dashboard web
