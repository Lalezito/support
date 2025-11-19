# 🚂 SOLUCIÓN: Dos Proyectos Railway Diferentes

**Fecha:** 19 Nov 2025
**Problema:** Backend deployado en proyecto incorrecto
**Status:** Identificado - Solución en progreso

---

## 🔍 SITUACIÓN IDENTIFICADA

### Hay DOS proyectos Railway separados:

#### 1. Proyecto Viejo: `zodiac-backend-api`
```
URL: zodiac-backend-api-production-8ded.up.railway.app
Version: 2.2.0 (recién actualizada por Marlin)
Endpoints: Solo /health, /ping, /api/* (genéricos)
Features: NO tiene rutas de AI Coach, ni horoscopeData
Status: ✅ Deployado PERO es el backend simplificado
```

**Características:**
- Endpoints limitados
- Sin `/api/ai-coach/*`
- Sin `/api/docs`
- Solo health checks básicos

#### 2. Proyecto Nuevo: `jubilant-recreation`
```
Service: flutter-horoscope-backend
URL: ??? (por determinar)
Version: Debería ser 2.2.0 (building)
Features: ✅ Rutas completas de AI Coach
Status: Building (según capturas)
```

**Características:**
- Endpoints completos
- `/api/ai-coach/chat/*`
- `/api/docs`
- horoscopeData implementado

---

## 🎯 EL PROBLEMA

### Flutter apunta al backend VIEJO:

**Archivos Flutter usando URL vieja:**
```dart
// lib/services/backend_service.dart
'https://zodiac-backend-api-production-8ded.up.railway.app'

// lib/services/api_service.dart
static const String _baseUrl = 'https://zodiac-backend-api-production-8ded.up.railway.app';

// lib/services/weekly_horoscope_service.dart
'https://zodiac-backend-api-production-8ded.up.railway.app'

// Y 7 archivos más...
```

### Backend correcto está en otro proyecto:

El código con horoscopeData está en `jubilant-recreation/flutter-horoscope-backend`, pero Flutter no sabe su URL.

---

## 🔧 SOLUCIÓN EN 3 PASOS

### Paso 1: Encontrar URL del proyecto correcto

**Método A: Railway Dashboard**
1. Abrir: https://railway.app/
2. Buscar proyecto: `jubilant-recreation`
3. Click en servicio: `flutter-horoscope-backend`
4. Tab "Settings" → Section "Networking"
5. Ver "Public Domain" o "Service Domain"

**Método B: Railway CLI** (después de link)
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
railway login
railway link --project jubilant-recreation
railway domain
```

**Método C: Checking deployment logs**
En las capturas que mencionaste, cuando el build termine debería mostrar la URL.

---

### Paso 2: Verificar que el backend correcto responda

Una vez tengas la URL (ejemplo: `flutter-horoscope-backend-production.up.railway.app`):

```bash
# Test health
curl https://<URL-CORRECTA>/health

# Debe mostrar rutas completas
curl https://<URL-CORRECTA>/api/docs | jq '.endpoints'

# Debe incluir ai-coach
curl https://<URL-CORRECTA>/api/routes | jq '.routes[] | select(.path | contains("ai-coach"))'
```

---

### Paso 3: Actualizar Flutter para usar URL correcta

**Opción A: Actualizar todos los archivos (10 archivos)**

Buscar y reemplazar en todos los archivos Dart:
```dart
// ANTES:
'https://zodiac-backend-api-production-8ded.up.railway.app'

// DESPUÉS:
'https://flutter-horoscope-backend-production.up.railway.app'  // O la URL correcta
```

**Archivos a actualizar:**
1. `lib/services/weekly_horoscope_service.dart`
2. `lib/services/backend_service.dart`
3. `lib/services/network_security_service.dart`
4. `lib/services/payment_service.dart`
5. `lib/services/unified_notification_service.dart`
6. `lib/services/receipt_validation_service.dart`
7. `lib/services/api_service.dart`
8. `lib/services/goal_planner_service.dart`
9. Y cualquier otro que tenga la URL vieja

**Opción B: Usar variable de entorno** (MEJOR)

1. Crear constante centralizada:
```dart
// lib/config/api_config.dart
class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://flutter-horoscope-backend-production.up.railway.app',
  );
}
```

2. Actualizar todos los servicios para usar `ApiConfig.baseUrl`

3. Build con environment variable:
```bash
flutter build ios --dart-define=API_BASE_URL=https://flutter-horoscope-backend-production.up.railway.app
```

---

## 📋 CHECKLIST DE MIGRACIÓN

### 1. Identificar URL correcta
- [ ] Abrir Railway dashboard
- [ ] Encontrar proyecto `jubilant-recreation`
- [ ] Copiar URL del servicio `flutter-horoscope-backend`
- [ ] Verificar que responde con endpoints completos

### 2. Actualizar Flutter
- [ ] Buscar todos los archivos con URL vieja
- [ ] Reemplazar con URL nueva
- [ ] Hot restart app
- [ ] Verificar conexión funciona

### 3. Verificar Features
- [ ] Enviar mensaje en Cosmic Coach
- [ ] Verificar pill aparece
- [ ] Verificar daily highlights aparece
- [ ] Verificar horoscopeData en responses

---

## 🚀 COMANDO RÁPIDO PARA BUSCAR/REEMPLAZAR

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# 1. Buscar todas las ocurrencias
grep -r "zodiac-backend-api-production-8ded" lib/ --include="*.dart"

# 2. Verificar qué archivos cambiarían
grep -rl "zodiac-backend-api-production-8ded" lib/ --include="*.dart"

# 3. Hacer el reemplazo (después de confirmar URL correcta)
# Reemplazar YOUR_NEW_URL con la URL del proyecto jubilant-recreation
find lib/ -name "*.dart" -exec sed -i '' 's|zodiac-backend-api-production-8ded.up.railway.app|YOUR_NEW_URL|g' {} +

# 4. Verificar cambios
git diff lib/
```

---

## 🔍 CÓMO VERIFICAR QUE ESTÁS EN EL BACKEND CORRECTO

### Backend CORRECTO debe tener:

```bash
# 1. Endpoints de AI Coach
curl https://<URL>/api/routes | jq '.routes[] | select(.path | contains("ai-coach"))'
# Debe mostrar: /api/ai-coach/chat/start, /api/ai-coach/chat/message, etc.

# 2. Documentación completa
curl https://<URL>/api/docs | jq '.endpoints | keys'
# Debe mostrar: ai_coach, horoscopes, compatibility, etc.

# 3. horoscopeData en respuesta
curl -X POST https://<URL>/api/ai-coach/chat/message \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test","message":"Hola","userId":"test","zodiacSign":"Capricornio","language":"es"}' \
  | jq 'has("horoscopeData")'
# Debe mostrar: true
```

### Backend INCORRECTO (actual) tiene:

```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/routes
# Error: Endpoint not found

curl https://zodiac-backend-api-production-8ded.up.railway.app/api/docs
# Error: Endpoint not found

# Solo responde: /health, /ping, /api/*
```

---

## 📊 COMPARACIÓN VISUAL

```
┌─────────────────────────────────────────────────────────┐
│ Backend VIEJO (zodiac-backend-api)                      │
├─────────────────────────────────────────────────────────┤
│ URL: zodiac-backend-api-production-8ded...              │
│ Version: 2.2.0 ✅                                       │
│ Endpoints: ❌ LIMITADOS                                 │
│   • /health                                             │
│   • /ping                                               │
│   • /api/* (genérico)                                   │
│ Features: ❌ Sin AI Coach, sin horoscopeData            │
│ Flutter apunta aquí: ✅ SÍ (10 archivos)                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Backend CORRECTO (jubilant-recreation)                  │
├─────────────────────────────────────────────────────────┤
│ URL: ??? (por determinar)                               │
│ Version: 2.2.0 ✅ (código con horoscopeData)           │
│ Endpoints: ✅ COMPLETOS                                 │
│   • /api/ai-coach/chat/*                                │
│   • /api/docs                                           │
│   • /api/routes                                         │
│   • Todos los endpoints                                 │
│ Features: ✅ AI Coach + horoscopeData + todo            │
│ Flutter apunta aquí: ❌ NO (necesita actualización)     │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 PRÓXIMA ACCIÓN INMEDIATA

1. **Encontrar URL del proyecto `jubilant-recreation`:**
   - Railway dashboard → jubilant-recreation → flutter-horoscope-backend → Settings → Networking
   - Copiar "Public Domain"

2. **Verificar que ese backend tiene horoscopeData:**
   ```bash
   curl https://<URL-NUEVA>/health
   curl https://<URL-NUEVA>/api/docs
   ```

3. **Actualizar Flutter:**
   ```bash
   cd zodiac_app
   # Buscar/reemplazar URL vieja con URL nueva
   # Hot restart: R
   ```

4. **Probar en iPhone:**
   - Cosmic Coach → Enviar mensaje
   - Verificar pill + highlights aparecen

---

## 💡 ALTERNATIVA: Configurar CNAME/Alias

Si querés mantener la URL `zodiac-backend-api-production-8ded.up.railway.app`, podés:

1. Configurar Railway para que esa URL apunte al proyecto `jubilant-recreation`
2. O configurar un CNAME en el proyecto viejo que redirecte al nuevo
3. O renombrar/reconfigur ar dominios en Railway dashboard

Pero la forma más rápida es simplemente actualizar la URL en Flutter.

---

**Generado:** 19 Nov 2025 - 21:00
**Status:** Problema identificado - URL incorrecta en Flutter
**Solución:** Encontrar URL correcta y actualizar 10 archivos Dart
**Tiempo estimado:** 5-10 minutos
