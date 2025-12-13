# 🔧 PLAN DE ARREGLOS - Cosmic Coach NOV 19

**Fecha:** 19 Nov 2025, 21:20 NZDT
**Problemas Identificados:** 7 críticos
**Status:** Backend OK, Flutter necesita fixes

---

## 🐛 PROBLEMAS ENCONTRADOS (de screenshot + feedback)

### 1. ❌ **Endpoint incorrecto** - CRÍTICO
**Problema:**
Flutter llama a: `/api/horoscope-chat/chat` ❌
Backend tiene: `/api/ai-coach/chat/message` ✅

**Resultado:**
- Sin horoscopeData
- Sin pill de energía/color
- Sin daily highlights card
- Respuestas genéricas desde templates locales

**Archivo:** `zodiac_app/lib/services/horoscope_chat_service.dart:392`

---

### 2. ❌ **Botón scroll invertido** - UI Bug
**Problema:**
Botón "bajar al final" → sube al inicio

**Archivo:** Probablemente en `chat_screen.dart` o `horoscope_chat_screen.dart`

**Fix esperado:**
```dart
// ANTES:
_scrollController.animateTo(0, ...)  // Sube al inicio

// DESPUÉS:
_scrollController.animateTo(
  _scrollController.position.maxScrollExtent,  // Baja al final
  ...
)
```

---

### 3. ⚠️ **Mensajes genéricos y cortos**
**Problema:**
- "Capricórnio, o cosmos te envia energia equilibrada hoje..."
- Muy básico, sin personalización
- Se acaban rápido (pocos templates)

**Causa:** Usando templates locales en vez de AI backend

**Fix:** Una vez que endpoint correcto funcione, esto se resuelve automáticamente.

---

### 4. ❌ **Historial no guarda conversaciones**
**Problema:**
- Auto-save activado
- Conversaciones NO se guardan
- Botón "Historial" vacío

**Posibles causas:**
1. `_saveMessages()` no se llama correctamente
2. SharedPreferences no persiste
3. `_loadMessages()` no recupera datos

**Archivo:** `horoscope_chat_service.dart` métodos save/load

---

### 5. ✅ **Favoritos funciona** - OK

---

### 6. ❓ **Auto-save confuso**
**Tu pregunta:** "¿Auto-save es para guardar conversaciones o para memoria del chat?"

**Respuesta:**
Auto-save debería:
- **Guardar conversaciones** en caché local cuando:
  - Usuario limpia el chat
  - Usuario sale de la pantalla
  - App va a background
- **NO es para memoria** de contexto del AI (eso es session backend)

**Si está activado pero no funciona** → Bug en el guardado/carga

---

### 7. ⚠️ **Límite de mensajes muy bajo**
**Tu feedback:** "Tendría que haber un límite de 30 mensajes"

**Actualmente:** Probablemente 5-10 mensajes (free tier)

**Archivo:** Buscar `dailyMessages` o `messageLimit`

---

## 🎯 PLAN DE FIXES - ORDEN DE PRIORIDAD

### 🔴 PRIORIDAD 1: Endpoint Correcto (10 min)

**Cambiar en `horoscope_chat_service.dart`:**

```dart
// LÍNEA 392 - ANTES:
final url = Uri.parse('$_backendUrl/api/horoscope-chat/chat');

// DESPUÉS:
final url = Uri.parse('$_backendUrl/api/ai-coach/chat/message');
```

**PERO ESPERA:** El endpoint `/api/ai-coach/chat/message` requiere primero `/chat/start` para obtener sessionId.

**Necesitamos:**
1. Llamar `/api/ai-coach/chat/start` una vez al inicio
2. Guardar `sessionId`
3. Usar `/api/ai-coach/chat/message` con ese sessionId

**Alternativa rápida:**
Verificar si backend tiene endpoint compatible con la estructura actual. Déjame revisar el código del backend.

---

### 🔴 PRIORIDAD 2: Botón Scroll (5 min)

Buscar archivo con el botón:
```bash
grep -r "FloatingActionButton\|scroll.*Down\|animateTo" lib/screens/*chat*.dart
```

Fix:
```dart
// Cambiar de:
_scrollController.animateTo(0, ...)

// A:
_scrollController.animateTo(
  _scrollController.position.maxScrollExtent,
  duration: Duration(milliseconds: 300),
  curve: Curves.easeOut,
)
```

---

### 🟡 PRIORIDAD 3: Auto-save / Historial (15 min)

**Verificar:**
1. `_saveMessages()` se llama:
   - Al agregar mensaje
   - Al salir de pantalla
   - Al limpiar chat

2. `_loadMessages()` funciona:
   - Lee de SharedPreferences
   - Parsea JSON correctamente
   - Agrega a state

**Debugging:**
Agregar logs:
```dart
Future<void> _saveMessages() async {
  debugPrint('💾 Saving ${_state.messages.length} messages...');
  // ... existing code
  debugPrint('✅ Messages saved');
}
```

---

### 🟡 PRIORIDAD 4: Aumentar Límite de Mensajes (2 min)

Buscar:
```bash
grep -n "dailyMessages\|messageLimit\|maxMessages" lib/services/horoscope_chat_service.dart
```

Cambiar de 5 → 30 para free tier.

---

### 🟢 PRIORIDAD 5: Mejorar Respuestas (automático)

Una vez que endpoint correcto funcione:
- ✅ Respuestas personalizadas por AI
- ✅ horoscopeData en metadata
- ✅ Pill de energía/color
- ✅ Daily highlights card

---

## 📝 IMPLEMENTACIÓN DETALLADA

### Fix 1: Migrar a `/api/ai-coach`

**Opción A: Cambio Completo (recomendado)**

Necesitamos:
1. Agregar método `startSession()`
2. Guardar `sessionId` en estado
3. Usar `sendMessage()` con sessionId

**Cambios en `horoscope_chat_service.dart`:**

```dart
// Agregar a clase:
String? _currentSessionId;

// Nuevo método:
Future<String> startSession({
  required String userId,
  required String zodiacSign,
  required String language,
}) async {
  final url = Uri.parse('$_backendUrl/api/ai-coach/chat/start');

  final response = await _httpClient.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'userId': userId,
      'zodiacSign': zodiacSign,
      'language': language,
    }),
  ).timeout(_requestTimeout);

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    if (data['success'] == true) {
      _currentSessionId = data['sessionId'];
      return _currentSessionId!;
    }
  }

  throw Exception('Failed to start session');
}

// Modificar _callBackend:
Future<HoroscopeResponse> _callBackend({
  required String message,
  required String userId,
  required String zodiacSign,
  required String language,
  required HoroscopeQuestionCategory category,
}) async {
  // Si no hay sesión, crear una
  if (_currentSessionId == null) {
    await startSession(
      userId: userId,
      zodiacSign: zodiacSign,
      language: language,
    );
  }

  final url = Uri.parse('$_backendUrl/api/ai-coach/chat/message');

  final response = await _httpClient.post(
    url,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: jsonEncode({
      'sessionId': _currentSessionId,
      'message': message,
      'userId': userId,
      'zodiacSign': zodiacSign,
      'language': language,
      // 'category': category.name,  // Verificar si backend lo usa
    }),
  ).timeout(_requestTimeout);

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    if (data['success'] == true) {
      // ✅ AQUÍ VIENE horoscopeData
      return HoroscopeResponse(
        text: data['content'] ?? data['message'],
        category: category,
        metadata: {
          'source': 'ai_backend',
          'horoscopeData': data['horoscopeData'],  // ✅ KEY FIX
        },
      );
    }
  }

  throw Exception('Backend error: ${response.statusCode}');
}
```

---

**Opción B: Fix Rápido (menos óptimo)**

Si el backend tiene un endpoint `/api/coaching/getTodaysHoroscope` que devuelva horoscopeData, usarlo temporalmente.

Pero mejor hacer Opción A.

---

### Fix 2: Scroll Button

Buscar archivo con FloatingActionButton:

```bash
find lib/screens -name "*chat*.dart" -exec grep -l "FloatingActionButton" {} \;
```

Luego cambiar:
```dart
// Si tiene algo como:
onPressed: () {
  _scrollController.animateTo(
    0,  // ❌ ESTO ES EL PROBLEMA
    duration: Duration(milliseconds: 300),
    curve: Curves.easeOut,
  );
}

// Cambiar a:
onPressed: () {
  _scrollController.animateTo(
    _scrollController.position.maxScrollExtent,  // ✅ Baja al final
    duration: Duration(milliseconds: 300),
    curve: Curves.easeOut,
  );
}
```

---

### Fix 3: Auto-save

Agregar logs de debug:

```dart
Future<void> _saveMessages() async {
  if (_sharedPrefs == null) {
    debugPrint('❌ SharedPrefs not initialized');
    return;
  }

  try {
    debugPrint('💾 Saving ${_state.messages.length} messages');

    final messagesJson = _state.messages
        .map((m) => m.toJson())
        .toList();

    final jsonString = jsonEncode(messagesJson);

    await _sharedPrefs!.setString('cosmic_coach_messages', jsonString);

    debugPrint('✅ Messages saved: ${jsonString.length} chars');
  } catch (e) {
    debugPrint('❌ Save failed: $e');
  }
}

Future<void> _loadMessages() async {
  if (_sharedPrefs == null) {
    debugPrint('❌ SharedPrefs not initialized for load');
    return;
  }

  try {
    final jsonString = _sharedPrefs!.getString('cosmic_coach_messages');

    if (jsonString == null || jsonString.isEmpty) {
      debugPrint('📭 No saved messages found');
      return;
    }

    debugPrint('📥 Loading messages: ${jsonString.length} chars');

    final List<dynamic> messagesJson = jsonDecode(jsonString);
    final messages = messagesJson
        .map((json) => ChatMessage.fromJson(json))
        .toList();

    _state = _state.copyWith(messages: messages);

    debugPrint('✅ Loaded ${messages.length} messages');
  } catch (e) {
    debugPrint('❌ Load failed: $e');
  }
}
```

Y llamar `_saveMessages()` en:
- `sendMessage()` después de agregar respuesta
- `clearChat()` antes de limpiar
- Lifecycle hook cuando screen se va a background

---

### Fix 4: Aumentar Límite

Buscar en servicio:

```dart
// Cambiar de:
static const int _maxMessagesPerDay = 5;

// A:
static const int _maxMessagesPerDay = 30;
```

O si está en un config:
```dart
final limits = {
  'free': 30,  // Era 5
  'premium': 100,
};
```

---

## ✅ ORDEN DE EJECUCIÓN

1. **Fix Endpoint** (30 min) - CRÍTICO
   - Implementar `startSession()`
   - Modificar `_callBackend()`
   - Parsear `horoscopeData` del response
   - Test en iPhone

2. **Fix Scroll Button** (5 min)
   - Encontrar archivo
   - Cambiar `0` → `maxScrollExtent`
   - Test en iPhone

3. **Fix Auto-save** (15 min)
   - Agregar logs
   - Verificar llamadas
   - Test guardado/carga

4. **Aumentar Límite** (2 min)
   - Cambiar constante
   - Test conteo

5. **Test Completo** (10 min)
   - Pill aparece
   - Highlights aparecen
   - Scroll funciona
   - Historial guarda
   - 30 mensajes disponibles

---

## 🎯 RESULTADO ESPERADO

### ANTES:
- ❌ Sin pill
- ❌ Sin daily highlights
- ❌ Mensajes genéricos cortos
- ❌ Botón scroll invertido
- ❌ Historial no guarda
- ⚠️ Solo 5 mensajes

### DESPUÉS:
- ✅ Pill: ⚡ Alta • 🎨 Dorado, Verde
- ✅ Daily Highlights: numbers, hours, advice
- ✅ Respuestas AI personalizadas largas
- ✅ Botón baja al final
- ✅ Historial guarda conversaciones
- ✅ 30 mensajes disponibles

---

**¿Quieres que empiece con el Fix 1 (endpoint correcto)?**

Ese es el más crítico y desbloquea pill + highlights.

---

**Tiempo estimado total:** 1 hora
**Prioridad máxima:** Fix 1 (endpoint)
