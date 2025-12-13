# 🔍 Test Coach Tracking - AHORA

## 🎯 Objetivo

Verificar por qué Coach Sessions NO está trackeando.

---

## ⚡ Quick Test (2 minutos)

### **Paso 1: Recompilar app**

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
flutter pub get
flutter run
```

**Por qué:** Hot reload puede no haber aplicado el cambio en `cosmic_chat_service.dart`

---

### **Paso 2: Usar Coach y buscar log**

```
1. Abre Cosmic Coach en la app
2. Envía UN mensaje (cualquiera, ej: "Hola")
3. MIRA LA CONSOLA (terminal donde corre flutter)
4. Busca este log:

   "📊 Coach sessions count: 1"

¿Lo ves?
```

---

## 📊 Resultados Posibles

### **Resultado A: SÍ veo el log "📊 Coach sessions count: 1"**

✅ **El tracking SÍ funciona**

**Problema:** Analytics NO está leyendo el contador correctamente

**Siguiente paso:**
1. Envía 2-3 mensajes más en Coach
2. Ve a Analytics
3. ¿El número de Coach Sessions aumentó?

**Si SÍ aumentó:**
→ ¡Funciona! Solo necesitabas recompilar

**Si NO aumentó:**
→ Analytics no lee de SharedPreferences correctamente
→ Revisar `analytics_data_provider.dart` línea 122-124

---

### **Resultado B: NO veo el log**

❌ **El método NO se está llamando**

**Posibles causas:**
1. El código no se compiló
2. Hay un error en el catch que no se muestra
3. `sendMessage()` no se está usando (¿usas otro método?)

**Debugging:**
```bash
# Ver todos los logs de Coach:
flutter logs | grep -i "coach"

# Ver todos los logs de Analytics:
flutter logs | grep "📊"
```

**Siguiente paso:** Reportar qué otros logs ves (si hay)

---

## 🔍 Debugging Avanzado (si Resultado B)

### **Verificar qué método se usa para enviar mensajes**

El tracking está en `sendMessage()` línea 257.

**¿Usas otro método?**
- `sendQuickReply()` → SÍ llama `sendMessage()` (debería funcionar)
- Otro método directo → NO trackeará

**Para verificar:**
```bash
# Busca logs de "Message sent" o "AI Response"
flutter logs | grep -i "message"
```

---

### **Agregar log temporal para debug**

Si NO ves `📊 Coach sessions count`, podemos agregar un log ANTES del try:

```dart
// En cosmic_chat_service.dart línea 256:
AppLogger.debug('🔍 ABOUT TO TRACK COACH SESSION'); // ← AGREGAR ESTO
await _incrementCoachSessionCount();
```

Esto nos dirá si el código llega hasta ahí o se corta antes.

---

## 📝 Formato de Reporte

### **Si ves el log:**
```
✅ LOG VISTO: "📊 Coach sessions count: 1"

Envié 3 mensajes en Coach
Vi estos logs:
- "📊 Coach sessions count: 1"
- "📊 Coach sessions count: 2"
- "📊 Coach sessions count: 3"

Fui a Analytics:
- Coach Sessions muestra: [número] ← REPORTA QUÉ VES
```

---

### **Si NO ves el log:**
```
❌ NO VI LOG de "📊 Coach sessions count"

Envié 3 mensajes en Coach
Vi estos otros logs (si hay):
[pegar logs que veas relacionados con Coach o message]

Fui a Analytics:
- Coach Sessions muestra: [número] ← REPORTA QUÉ VES
```

---

## 🎯 Comandos para Copiar/Pegar

### **Recompilar y correr:**
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app && flutter clean && flutter pub get && flutter run
```

### **Ver logs en tiempo real:**
```bash
# En otra terminal:
flutter logs | grep "📊"
```

### **Ver logs de Coach:**
```bash
flutter logs | grep -i "coach"
```

---

## ⏱️ Tiempo Estimado

- **Recompilar:** 1-2 minutos
- **Test:** 30 segundos (enviar mensaje y buscar log)
- **Reportar:** 30 segundos

**Total:** 2-3 minutos

---

## 🚨 Nota Importante

**El problema más probable es:**
- Hot reload NO aplicó el cambio en `cosmic_chat_service.dart`
- Por eso necesitas hacer `flutter clean` + full rebuild

**Si después de recompilar SÍ ves el log:**
→ ¡Problema resuelto! Solo era cache

**Si después de recompilar NO ves el log:**
→ Hay un problema más profundo que necesitamos investigar

---

**Comando para empezar:**
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
flutter pub get
flutter run
```

**Luego:** Usa Coach → Envía mensaje → Busca en consola: `📊 Coach sessions count: 1`

**Reporta:** ✅ Lo vi / ❌ No lo vi
