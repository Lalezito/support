# 🔧 BACKEND ENDPOINTS PENDIENTES

**Status**: Backend online pero con endpoints limitados
**Backend URL**: https://zodiac-backend-api-production-8ded.up.railway.app
**Health Status**: ✅ Online (200 OK)
**Version**: 2.1.0-production

---

## 📊 Estado Actual

### ✅ Endpoints Funcionando
- `GET /health` - Health check ✅
- `GET /ping` - Ping test ✅

### ❌ Endpoints Faltantes (Causando 404 en App)

#### 1. FCM Registration (Prioridad ALTA)
**Endpoint**: `POST /api/fcm/register`
**Request Body**:
```json
{
  "token": "string",
  "userId": "string"
}
```
**Response**:
```json
{
  "success": true,
  "message": "FCM token registered successfully"
}
```
**Impacto Actual**:
- ❌ App recibe HTTP 500 al registrar token
- ⚠️ Push notifications no funcionan
- ✅ App continúa funcionando (usa notificaciones locales)

**Prioridad**: ALTA (v1.1)
**Estimación**: 2-4 horas

---

#### 2. Neural Compatibility Calculation (Prioridad MEDIA)
**Endpoint**: `POST /api/neural-compatibility/calculate`
**Request Body**:
```json
{
  "sign1": "string",
  "sign2": "string",
  "includeDailyFactors": boolean
}
```
**Response**:
```json
{
  "compatibilityScore": number,
  "dailyHarmony": number,
  "communicationFlow": number,
  "energySync": number,
  "challenges": string[],
  "advice": string[]
}
```
**Impacto Actual**:
- ❌ Backend retorna 404
- ✅ App usa cálculos locales (fallback v1.0)
- ✅ Funcionalidad completa disponible offline

**Prioridad**: MEDIA (v2.0)
**Estimación**: 6-8 horas (requiere modelo neural)

---

#### 3. Historical Horoscopes (Prioridad BAJA)
**Endpoint**: `GET /api/horoscopes/history`
**Query Parameters**:
```typescript
{
  sign: string;
  days?: number;  // default: 30, max: 90
  language?: string;
}
```
**Response**:
```json
{
  "timeline": [
    {
      "date": "ISO8601",
      "horoscope": "string",
      "energyLevel": number,
      "luckyNumbers": number[],
      "mood": "string"
    }
  ],
  "stats": {
    "averageEnergy": number,
    "totalDays": number
  }
}
```
**Impacto Actual**:
- Feature no implementada en app
- Retorna lista vacía
- No afecta experiencia usuario

**Prioridad**: BAJA (v2.0)
**Estimación**: 8-12 horas (requiere storage histórico)

---

## 🎯 Plan de Implementación

### Fase 1: v1.1 (1 mes post-launch)
**Objetivo**: Habilitar push notifications

**Tareas**:
1. Implementar `POST /api/fcm/register`
2. Implementar `DELETE /api/fcm/unregister`
3. Agregar endpoint `POST /api/fcm/send` para testing
4. Configurar Firebase Admin SDK correctamente
5. Testing con tokens reales iOS/Android

**Entregables**:
- ✅ Push notifications funcionando
- ✅ Backend puede enviar notificaciones custom
- ✅ Logs de registro/desregistro

**Tiempo**: 1 sprint (2 semanas)

---

### Fase 2: v2.0 (2-3 meses post-launch)
**Objetivo**: Habilitar features avanzadas

**Tareas Neural Compatibility**:
1. Implementar modelo neural o conectar a servicio AI
2. Crear `POST /api/neural-compatibility/calculate`
3. Implementar cálculos planetarios en tiempo real
4. Agregar cache para resultados frecuentes
5. Testing de precisión vs fallback local

**Tareas Historical Horoscopes**:
1. Diseñar schema de base de datos para horoscopos históricos
2. Implementar job diario que almacene horoscope del día
3. Crear `GET /api/horoscopes/history`
4. Backfill histórico (opcional - últimos 30 días)
5. Testing de queries y performance

**Entregables**:
- ✅ Compatibility usando AI backend
- ✅ Timeline histórico con 30+ días de datos
- ✅ Reducción de uso de fallback local

**Tiempo**: 2 sprints (4 semanas)

---

## 🔍 Diagnóstico Actual

### Backend Health Check
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/health
```

**Response**:
```json
{
  "status": "healthy",
  "uptime": 157324.67,
  "version": "2.1.0-production",
  "services": {
    "firebase": {
      "initialized": true,
      "hasServiceAccount": true
    }
  }
}
```

### Test FCM Registration
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/fcm/register \
  -H "Content-Type: application/json" \
  -d '{"token":"test","userId":"test"}'
```

**Response**:
```json
{
  "error": "Endpoint not found",
  "path": "/api/fcm/register",
  "availableEndpoints": ["/health", "/ping", "/api/*"]
}
```

### Test Neural Compatibility
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/neural-compatibility/calculate \
  -H "Content-Type: application/json" \
  -d '{"sign1":"aries","sign2":"aries"}'
```

**Response**:
```json
{
  "error": "Endpoint not found",
  "path": "/api/neural-compatibility/calculate",
  "availableEndpoints": ["/health", "/ping", "/api/*"]
}
```

---

## 📋 Checklist de Implementación

### FCM Registration Endpoint
- [ ] Crear archivo `src/routes/fcm.js`
- [ ] Implementar `POST /register` handler
- [ ] Implementar `DELETE /unregister` handler
- [ ] Validar token format (iOS/Android)
- [ ] Almacenar tokens en Firebase Firestore
- [ ] Implementar cleanup de tokens expirados
- [ ] Agregar logs de registro/error
- [ ] Testing con tokens reales
- [ ] Deploy a Railway
- [ ] Verificar en app móvil

### Neural Compatibility Endpoint
- [ ] Diseñar arquitectura (modelo local vs API externa)
- [ ] Implementar cálculos planetarios
- [ ] Crear `POST /calculate` handler
- [ ] Implementar cache (Redis o in-memory)
- [ ] Agregar rate limiting
- [ ] Testing de precisión
- [ ] Comparar con fallback local
- [ ] Deploy a Railway
- [ ] Integrar en app móvil
- [ ] Monitorear uso y performance

### Historical Horoscopes Endpoint
- [ ] Diseñar schema Firestore/PostgreSQL
- [ ] Implementar daily cron job (almacenar horóscopo)
- [ ] Crear `GET /history` handler
- [ ] Implementar paginación
- [ ] Agregar cache de queries frecuentes
- [ ] Backfill datos históricos (opcional)
- [ ] Testing de queries
- [ ] Deploy a Railway
- [ ] Integrar en app móvil
- [ ] Monitorear storage usage

---

## 🚀 Impacto en Producción

### v1.0 (Estado Actual)
**Backend Limitado**: ✅ NO BLOQUEA LANZAMIENTO
- App usa graceful degradation
- Todas las features críticas funcionan offline/local
- Experiencia usuario completa disponible

### v1.1 (Con FCM)
**Push Notifications**: ✅ MEJORA ENGAGEMENT
- Notificaciones diarias personalizadas
- Recordatorios de compatibilidad
- Alerts de eventos astrológicos importantes

### v2.0 (Con Todos los Endpoints)
**Features Completas**: ✅ EXPERIENCIA PREMIUM
- Cálculos AI más precisos
- Timeline histórico personal
- Menor uso de batería (menos cálculos locales)
- Datos sincronizados cross-device

---

## 📊 Métricas de Éxito

### v1.1 (FCM)
- [ ] >90% de usuarios con token registrado
- [ ] <5% tasa de error en registro
- [ ] Notificaciones entregadas en <30 segundos

### v2.0 (Full Backend)
- [ ] <10% uso de fallback local (neural compatibility)
- [ ] >80% usuarios acceden a timeline histórico
- [ ] Latencia API <500ms (p95)
- [ ] Uptime >99.5%

---

## 🔗 Referencias

**Documentación**:
- `.claude/MIGRATION_ROADMAP.md` - Roadmap completo v2.0
- `.claude/GRACEFUL_DEGRADATION_STRATEGY.md` - Estrategia de fallbacks
- `.claude/CONSOLE_TODO_RESOLUTION_PLAN.md` - Plan de resolución TODO

**Backend Repository**:
- `/backend/flutter-horoscope-backend/` - Código fuente
- Railway Dashboard: https://railway.app (verificar deployment)

**API Contracts**:
- Ver `.claude/MIGRATION_ROADMAP.md` líneas 254-323

---

**Creado**: October 7, 2025
**Actualizado**: October 7, 2025
**Owner**: Backend Team
**Status**: ⏳ PENDIENTE - 3 endpoints críticos
