# 🔧 PLAN DE REFACTOR - COSMIC COACH

**Fecha:** 23 Nov 2025
**Basado en:** Análisis exhaustivo del sistema de chat
**Prioridad:** Alta → Baja

---

## 🎯 PROBLEMAS IDENTIFICADOS (8 críticos)

### 1. 🔴 CRÍTICO: Doble fuente de verdad (Legacy + Nuevo)
**Archivos:**
- `lib/screens/cosmic_coach_chat_screen.dart:17-207`
- `lib/services/cosmic_chat_service.dart:12-740`
- `lib/services/horoscope_chat_service.dart`

**Problema:**
- Screen usa `horoscopeChatStateStreamProvider` (nuevo)
- Pero también instancia `CosmicChatService` (legacy)
- Dos caches, dos flujos, dos inicializaciones
- Causa bloqueos en debug mode

**Impacto:**
- ❌ Debug mode se tranca
- ❌ Historial duplicado en storage
- ❌ Confusión en logs
- ❌ Difícil de mantener

---

### 2. 🔴 Inicialización de sesión sin validación
**Archivo:** `lib/services/cosmic_chat_service.dart:145-193`

**Problema:**
- `_createOrLoadSession` usa `_sessionCache` global
- `last_chat_session_id` puede apuntar a sesión inexistente
- Hot reload deja estado inconsistente
- No hay limpieza de caché huérfana

**Impacto:**
- ❌ Sesiones zombie
- ❌ SharedPreferences crece sin control
- ❌ Debug confuso

---

### 3. 🟡 Backend calls sin resiliencia
**Archivo:** `lib/services/horoscope_chat_service.dart:403-536`

**Problema:**
- `_callBackend` no tiene reintentos
- No cancela request al salir de pantalla
- No invalida `_currentSessionId` si backend retorna 404
- Timeout fijo sin backoff

**Impacto:**
- ⚠️ UX mala en conexión inestable
- ⚠️ Sesiones expiradas no se recuperan
- ⚠️ Request orphans

---

### 4. 🟡 Límites diarios: feedback genérico
**Archivo:** `lib/screens/cosmic_coach_chat_screen.dart:497-599`

**Problema:**
- Backend retorna `limit_exceeded`, `premium_required`
- UI solo muestra SnackBar genérico
- No hay CTA de upgrade
- No muestra contador de mensajes restantes

**Impacto:**
- ⚠️ Usuario no entiende por qué falla
- ⚠️ Perdemos conversión a premium

---

### 5. 🟢 horoscopeData solo en último mensaje
**Archivo:** `lib/screens/cosmic_coach_chat_screen.dart:309-330`

**Problema:**
- Solo pinta "pill" del último mensaje AI
- No se persiste con el historial
- No se muestra en detalle (modals/cards)

**Impacto:**
- 🔍 Datos ricos no se aprovechan
- 🔍 Historial pierde contexto

---

### 6. 🟢 Logging sin normalizar
**Archivos:** Múltiples

**Problema:**
- Mix de `debugPrint`, `logInfo`, `AppLogger`
- Algunos logs sin prefijo requerido
- Difícil filtrar en Xcode

**Impacto:**
- 🔍 Debugging lento
- 🔍 No se pueden filtrar por tipo

---

### 7. 🟢 Quick replies no usan backend
**Archivo:** `lib/screens/cosmic_coach_chat_screen.dart:497-570`

**Problema:**
- Quick replies derivan de mensajes AI
- No consideran `suggestedReplies` del backend
- No hay historial por categoría

**Impacto:**
- 🔍 UX subóptima
- 🔍 No hay analytics de clicks

---

### 8. 🟢 Backend rechaza debug sin receiptData
**Archivo:** `backend/.../aiCoachService.js:119-222`

**Problema:**
- `startChatSession` requiere `receiptData`
- App en debug no pasa receipt → 402 error
- No hay modo sandbox

**Impacto:**
- 🔍 Testing difícil
- 🔍 Requiere mock manual

---

## 📋 PLAN DE ACCIÓN (4 fases)

### 🔴 FASE 1: QUICK WINS (2 horas)
**Objetivo:** Resolver problemas críticos que afectan UX actual

#### Task 1.1: Normalizar Logging (30 min)
**Cambios:**
- Reemplazar todos `debugPrint` → `AppLogger`
- Agregar prefijos consistentes:
  - 💾 Storage/cache
  - 🔵 Network
  - 📤 Requests
  - ✅ Success
  - ⚠️ Warnings
  - ❌ Errors

**Archivos:**
- `lib/services/horoscope_chat_service.dart`
- `lib/services/cosmic_chat_service.dart`
- `lib/screens/cosmic_coach_chat_screen.dart`

**Beneficio:** Debug más rápido, logs filtrables

---

#### Task 1.2: Mejorar Feedback de Errores (30 min)
**Cambios:**
- Mapear códigos de error backend → mensajes específicos
- Mostrar CTA de upgrade cuando `premium_required`
- Mostrar contador de mensajes restantes
- Card modal explicativa en vez de SnackBar

**Código:**
```dart
// En cosmic_coach_chat_screen.dart
void _handleChatError(String errorCode) {
  switch (errorCode) {
    case 'limit_exceeded':
      _showUpgradeDialog(
        title: 'Daily Limit Reached',
        message: 'You've used all your free messages today.\nUpgrade to Premium for 100 messages/day!',
        ctaText: 'Upgrade Now',
        onPressed: () => _navigateToPremium(),
      );
      break;
    case 'premium_required':
      _showUpgradeDialog(
        title: 'Premium Feature',
        message: 'This feature is only available for Premium users.',
        ctaText: 'See Premium Benefits',
        onPressed: () => _navigateToPremium(),
      );
      break;
    case 'session_expired':
      _showRetryDialog('Your session expired. Tap to reconnect.');
      break;
    default:
      _showGenericError(errorCode);
  }
}
```

**Beneficio:** Mejor UX, más conversión a premium

---

#### Task 1.3: Invalidar Sesión al Error 404 (15 min)
**Cambios en `horoscope_chat_service.dart`:**

```dart
Future<HoroscopeResponse> _callBackend(...) async {
  try {
    final response = await _httpClient.post(...);

    if (response.statusCode == 404 || response.statusCode == 401) {
      AppLogger.warn('⚠️ Session expired or not found - invalidating');
      _currentSessionId = null; // ✅ NUEVO
      throw SessionExpiredException();
    }

    // ... resto del código
  } catch (e) {
    AppLogger.error('❌ Backend call failed: $e');
    rethrow;
  }
}
```

**Beneficio:** Auto-recuperación de sesiones expiradas

---

#### Task 1.4: Limpiar Caché Huérfana al Inicio (45 min)
**Cambios en `cosmic_chat_service.dart`:**

```dart
Future<void> _cleanOrphanedCache() async {
  final lastSessionId = _prefs?.getString('last_chat_session_id');

  if (lastSessionId != null) {
    final sessionKey = 'chat_session_$lastSessionId';
    final sessionExists = _prefs?.containsKey(sessionKey) ?? false;

    if (!sessionExists) {
      AppLogger.warn('💾 Cleaning orphaned session ID: $lastSessionId');
      await _prefs?.remove('last_chat_session_id');
    }
  }

  // Limpiar sesiones antiguas (>30 días)
  final allKeys = _prefs?.getKeys() ?? {};
  final sessionKeys = allKeys.where((k) => k.startsWith('chat_session_'));

  for (final key in sessionKeys) {
    final sessionJson = _prefs?.getString(key);
    if (sessionJson != null) {
      final session = jsonDecode(sessionJson);
      final createdAt = DateTime.parse(session['createdAt']);

      if (DateTime.now().difference(createdAt).inDays > 30) {
        AppLogger.info('💾 Removing old session: $key');
        await _prefs?.remove(key);
      }
    }
  }
}

Future<void> initialize() async {
  _prefs = await SharedPreferences.getInstance();
  await _cleanOrphanedCache(); // ✅ NUEVO
  // ... resto de inicialización
}
```

**Beneficio:** Storage limpio, sin leaks de memoria

---

### 🟡 FASE 2: REFACTOR ESTRUCTURAL (4 horas)
**Objetivo:** Unificar servicios y eliminar legacy

#### Task 2.1: Migrar CosmicChatService a Fachada (2h)
**Plan:**
1. Identificar todos los usos de `CosmicChatService`
2. Crear adaptador que delegue a `HoroscopeChatService`
3. Remover lógica duplicada de persistencia
4. Mantener solo la interfaz pública

**Archivos:**
- `lib/services/cosmic_chat_service.dart` → convertir a fachada
- `lib/screens/cosmic_coach_chat_screen.dart` → usar solo provider

**Pseudocódigo:**
```dart
// cosmic_chat_service.dart (NUEVO DISEÑO)
class CosmicChatService {
  final HoroscopeChatService _delegate;

  CosmicChatService(this._delegate);

  // Solo métodos de conveniencia, delega TODO al servicio real
  Future<void> sendMessage(String text) => _delegate.sendMessage(...);
  Stream<List<ChatMessage>> get messages => _delegate.messagesStream;

  // NO más caché propio, NO más SharedPreferences
}
```

**Beneficio:** Una sola fuente de verdad, menos bugs

---

#### Task 2.2: Agregar Reintentos con Backoff (1h)
**Implementar en `horoscope_chat_service.dart`:**

```dart
Future<T> _retryWithBackoff<T>(
  Future<T> Function() operation, {
  int maxRetries = 3,
  Duration initialDelay = const Duration(seconds: 1),
}) async {
  int attempt = 0;
  Duration delay = initialDelay;

  while (true) {
    try {
      return await operation();
    } catch (e) {
      attempt++;

      if (attempt >= maxRetries) {
        AppLogger.error('❌ Max retries ($maxRetries) exceeded');
        rethrow;
      }

      AppLogger.warn('⚠️ Retry $attempt/$maxRetries after ${delay.inSeconds}s');
      await Future.delayed(delay);
      delay *= 2; // Exponential backoff
    }
  }
}

// Uso:
Future<HoroscopeResponse> _callBackend(...) async {
  return _retryWithBackoff(() async {
    final response = await _httpClient.post(...).timeout(_requestTimeout);
    // ... procesar response
  });
}
```

**Beneficio:** UX robusta en conexión inestable

---

#### Task 2.3: Cancelar Requests al Salir de Pantalla (1h)
**Implementar:**

```dart
class HoroscopeChatService {
  final Map<String, CancelToken> _activeRequests = {};

  Future<HoroscopeResponse> sendMessage(...) async {
    final requestId = Uuid().v4();
    final cancelToken = CancelToken();
    _activeRequests[requestId] = cancelToken;

    try {
      final response = await _callBackend(..., cancelToken: cancelToken);
      return response;
    } finally {
      _activeRequests.remove(requestId);
    }
  }

  void cancelAllRequests() {
    AppLogger.info('🔵 Cancelling ${_activeRequests.length} active requests');
    for (final token in _activeRequests.values) {
      token.cancel('Screen disposed');
    }
    _activeRequests.clear();
  }

  @override
  void dispose() {
    cancelAllRequests();
    super.dispose();
  }
}
```

**Beneficio:** No requests huérfanos, mejor performance

---

### 🟢 FASE 3: MEJORAS DE UX (2 horas)

#### Task 3.1: Persistir horoscopeData en Historial (1h)
**Cambios:**

```dart
// En ChatMessage model
class ChatMessage {
  final String id;
  final String text;
  final MessageType type;
  final Map<String, dynamic>? metadata; // ✅ Ya existe
  final HoroscopeData? horoscopeData; // ✅ NUEVO - extraer de metadata

  HoroscopeData? get horoscopeData {
    if (metadata?['horoscopeData'] != null) {
      return HoroscopeData.fromJson(metadata!['horoscopeData']);
    }
    return null;
  }
}

// En cosmic_coach_chat_screen.dart
Widget _buildMessageList() {
  return ListView.builder(
    itemBuilder: (context, index) {
      final message = messages[index];
      return Column(
        children: [
          MessageBubble(message: message),
          if (message.horoscopeData != null)
            HoroscopePill(data: message.horoscopeData!),
          if (message.horoscopeData != null)
            DailyHighlightsCard(data: message.horoscopeData!),
        ],
      );
    },
  );
}
```

**Beneficio:** Historial rico, datos persistentes

---

#### Task 3.2: Usar suggestedReplies del Backend (1h)
**Cambios:**

```dart
// En HoroscopeResponse
class HoroscopeResponse {
  final String text;
  final List<String> suggestedReplies; // ✅ Parsear del backend
  final HoroscopeData? horoscopeData;
}

// En cosmic_coach_chat_screen.dart
Widget _buildQuickReplies() {
  final lastAiMessage = messages.lastWhere(
    (m) => m.type == MessageType.ai,
    orElse: () => null,
  );

  if (lastAiMessage?.suggestedReplies?.isNotEmpty ?? false) {
    return QuickRepliesRow(
      replies: lastAiMessage!.suggestedReplies!,
      onTap: (reply) {
        _analytics.logEvent('quick_reply_tapped', {'reply': reply});
        _sendMessage(reply);
      },
    );
  }

  return SizedBox.shrink();
}
```

**Beneficio:** UX guiada, analytics de engagement

---

### 🟢 FASE 4: BACKEND & TESTING (2 horas)

#### Task 4.1: Modo Debug en Backend (1h)
**Archivo:** `backend/.../aiCoachService.js`

**Cambios:**
```javascript
async startChatSession(userId, zodiacSign, language, receiptData, debugMode = false) {
  // ✅ NUEVO: Bypass premium check en debug
  if (debugMode || process.env.NODE_ENV === 'development') {
    console.log('⚠️ DEBUG MODE: Bypassing receipt validation');
    const isPremium = true;
    const messageLimit = 100;
    // ... crear sesión sin validar receipt
  }

  // Modo producción normal
  const premiumStatus = await this.validateReceipt(receiptData);
  // ...
}
```

**Beneficio:** Testing más fácil, desarrollo más rápido

---

#### Task 4.2: Agregar Métricas y Tracing (1h)
**Backend:**

```javascript
// Middleware de logging
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const latency = Date.now() - start;
    console.log(`🔵 ${req.method} ${req.path} - ${res.statusCode} - ${latency}ms`);

    // Log a analytics
    analytics.track({
      event: 'api_request',
      endpoint: req.path,
      latency,
      statusCode: res.statusCode,
      userId: req.user?.id,
    });
  });

  next();
});

// En aiCoachService.js
async generateResponse(sessionId, message) {
  const start = Date.now();

  try {
    const response = await openai.chat.completions.create(...);

    const latency = Date.now() - start;
    const tokensUsed = response.usage.total_tokens;

    console.log(`✨ AI Response generated - ${latency}ms - ${tokensUsed} tokens`);

    // Track costs
    await this.trackUsage(sessionId, tokensUsed, latency);

    return response;
  } catch (error) {
    console.error(`❌ AI generation failed: ${error.message}`);
    throw error;
  }
}
```

**Beneficio:** Visibilidad de costos, performance monitoring

---

## 🎯 RESUMEN DE IMPACTO

### Después de Fase 1 (Quick Wins):
- ✅ Logs normalizados y filtrables
- ✅ Errores claros con CTAs
- ✅ Auto-recuperación de sesiones
- ✅ Storage limpio sin leaks
- **Tiempo:** 2 horas
- **Esfuerzo:** Bajo
- **Impacto:** Alto

### Después de Fase 2 (Refactor):
- ✅ Una sola fuente de verdad
- ✅ Debug mode funciona
- ✅ Reintentos automáticos
- ✅ No request leaks
- **Tiempo:** +4 horas
- **Esfuerzo:** Medio
- **Impacto:** Muy Alto

### Después de Fase 3 (UX):
- ✅ horoscopeData en historial
- ✅ Quick replies del backend
- ✅ Analytics de engagement
- **Tiempo:** +2 horas
- **Esfuerzo:** Bajo
- **Impacto:** Medio

### Después de Fase 4 (Backend):
- ✅ Debug mode sin mocks
- ✅ Métricas de costos
- ✅ Performance tracking
- **Tiempo:** +2 horas
- **Esfuerzo:** Bajo
- **Impacto:** Medio

---

## 🚀 RECOMENDACIÓN

**Empezar con FASE 1** (2 horas):
- Impacto inmediato en UX
- No requiere cambios arquitectónicos
- Bajo riesgo de regresión
- Facilita el resto del trabajo

**Luego evaluar:**
- Si debug mode sigue siendo problema → Fase 2
- Si queremos mejorar engagement → Fase 3
- Si necesitamos visibilidad de costos → Fase 4

---

## 📋 SIGUIENTE PASO INMEDIATO

**¿Quieres que empiece con Task 1.1 (Normalizar Logging)?**

Es el cambio más seguro y te va a facilitar TODO el debugging futuro.

**Tiempo:** 30 minutos
**Riesgo:** Cero
**Beneficio:** Logs filtrables por emoji en Xcode

---

**Fecha:** 2025-11-23
**Status:** PLAN LISTO
**Esperando tu go/no-go** 🚀
