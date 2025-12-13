# ✅ PRE-DEPLOY CHECKLIST - Verificación Final

**Fecha:** 19 Noviembre 2025 04:40
**Estado del código:** ✅ TODOS LOS FIXES IMPLEMENTADOS
**Próximo paso:** Deploy limpio en iPhone

---

## 🎯 CONFIRMACIÓN DE ESTADO

### ✅ Verificado en Disco (por usuario)

| Fix | Ubicación | Estado |
|-----|-----------|--------|
| **Padding dinámico** | `chat_history_widget.dart:220-243` | ✅ `bottom = 160 + systemBottom` |
| **Quick replies** | `horoscope_chat_service.dart:1020-1094` | ✅ Normalización + pool 12 + Set tracking |
| **Modo Balanced** | `horoscope_chat_service.dart:230-259` | ✅ `confidenceThreshold = 0.95` |
| **Provider estable** | `consolidated_providers.dart:368-385` | ✅ `ref.read` (no se recrea) |
| **Cosmic Profiles** | `cosmic_profile_service.dart:52-70` | ✅ Aplica y persiste perfil |
| **Settings premium** | Multiple files | ✅ `subscriptionService.isPremium` |

**Conclusión:** Código está correcto. Si hay síntomas en device → problema de cache/build artifacts.

---

## 🚀 PASOS PRE-DEPLOY (OBLIGATORIOS)

### 1. Limpiar TODOS los artefactos

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Limpiar Flutter cache
flutter clean

# Eliminar herramientas de análisis
rm -rf .dart_tool/

# Eliminar builds anteriores
rm -rf build/

# Limpiar pods (iOS)
cd ios
rm -rf Pods/
rm -rf Podfile.lock
cd ..
```

**Por qué:** Artefactos viejos pueden contener código pre-fix compilado.

---

### 2. Reinstalar dependencias

```bash
# Recargar packages
flutter pub get

# Reinstalar pods de iOS
cd ios
pod install
cd ..
```

**Por qué:** Asegurar que todas las dependencias están sincronizadas.

---

### 3. Verificar análisis estático

```bash
flutter analyze
```

**Esperado:**
```
Analyzing zodiac_app...
No issues found!
(o solo warnings/info en example/ files)
```

**Si hay errores:** Reportar antes de continuar.

---

### 4. Deploy en DEBUG primero (para logs)

```bash
flutter run -d 00008150-0015244A2288401C --debug
```

**Por qué:** Modo debug permite ver logs en tiempo real en Xcode console.

---

## 📊 VERIFICACIÓN EN DEVICE (Checklist de Testing)

### Test #1: Chat NO se resetea (Bug #4 - CRÍTICO)

**Pasos:**
1. Abrir Cosmic Coach chat
2. Enviar 3-4 mensajes (tener conversación visible)
3. Ir a Settings → cambiar modo (quick → balanced)
4. Volver al chat

**✅ Esperado:** Historial de mensajes permanece intacto

**❌ Si falla:** El provider está usando `ref.watch` o hay otro listener recreando el servicio

**Logs a buscar en Xcode:**
```
🗑️ HoroscopeChatService disposing...  // ❌ NO debería aparecer al cambiar settings
```

---

### Test #2: Quick replies visibles (Bug #1)

**Pasos:**
1. En chat, enviar mensaje
2. Esperar respuesta del bot
3. Observar quick replies en la parte inferior

**✅ Esperado:**
- Quick replies 100% visibles
- No hay overlap con mensajes
- No quedan cortados por el borde inferior

**❌ Si falla:**
- Verificar en qué device (iPhone SE vs Pro Max)
- Revisar `MediaQuery.viewPadding.bottom` en logs

**Debug opcional - añadir log temporal:**
```dart
// En chat_history_widget.dart línea ~230
final systemBottom = viewPadding.bottom;
debugPrint('📏 Device viewPadding.bottom: $systemBottom');
debugPrint('📏 Effective bottom padding: ${160.0 + systemBottom}');
```

---

### Test #3: Quick replies NO se repiten (Bug #2)

**Pasos:**
1. Tener conversación de 15+ mensajes
2. Observar las 3 sugerencias en cada respuesta
3. Anotar cuáles aparecen

**✅ Esperado:**
- No se repiten las mismas sugerencias en período corto
- Variedad durante toda la conversación
- Después de ~12 usos, las más antiguas pueden reaparecer

**❌ Si falla:**
- Verificar que `_recentlyUsedReplies` se está poblando
- Revisar normalización (toLowerCase + trim)

**Logs a buscar:**
```dart
// Añadir temporalmente en horoscope_chat_service.dart ~línea 1090
debugPrint('🎲 Recently used replies: ${_recentlyUsedReplies.length}/12');
debugPrint('🎲 Available pool: ${availableReplies.length}');
```

---

### Test #4: Respuestas coherentes (Bug #3)

**Pasos:**
1. Modo balanced (default)
2. Preguntar: "horóscopo de hoy" → debería usar template
3. Preguntar: "qué opinas sobre mi futuro amoroso" → debería usar backend
4. Observar logs en Xcode console

**✅ Esperado - Logs en Xcode:**
```
🎯 Chat mode: balanced | preferBackend: false | confidence: 0.95
📱 Using LOCAL template (high confidence 0.95)

🎯 Chat mode: balanced | preferBackend: false | confidence: 0.75
☁️ Calling BACKEND (low confidence 0.75)
```

**❌ Si falla:**
- Si preguntas complejas usan template → verificar threshold (debe ser 0.95)
- Si todo va a backend → verificar getConfidence() en HoroscopeTemplate

---

### Test #5: Cosmic Profiles funcionan

**Pasos:**
1. Ir a Cosmic Coach Settings
2. Aplicar perfil "Starter"
3. Verificar en UI: modo = Quick, personalidad = Friendly
4. Aplicar perfil "Power User"
5. Verificar: modo = Balanced, personalidad = Wise
6. Aplicar perfil "Mystic"
7. Verificar: modo = Detailed, personalidad = Motivational

**✅ Esperado - Logs en Xcode:**
```
🎯 CosmicProfileService: Applying profile "starter"
   ├─ chatMode: quick
   ├─ personality: friendly
   ├─ showQuickReplies: true
   ├─ preferBackendAI: false
   ├─ dailyMessageLimit: 10
🎯 PreferencesService: Changing chatMode: "balanced" → "quick"
✅ PreferencesService: chatMode updated to "quick" and persisted
🔔 PreferencesService: notifyListeners() → 3 listeners
✅ CosmicProfileService: Profile "starter" applied successfully
```

**❌ Si falla:**
- Verificar que `cosmicProfileServiceProvider` está correctamente inyectado
- Revisar que PreferencesService persiste los cambios

---

### Test #6: Engine Modes afectan comportamiento

**Pasos:**
1. **Modo Quick** → Preguntar algo complejo ("analiza mi carta astral completa")
   - **Esperado:** Respuesta genérica de template
   - **Log:** `📱 Using LOCAL template (quick mode)`

2. **Modo Balanced** → Preguntar "horóscopo hoy"
   - **Esperado:** Template (alta confianza)
   - **Log:** `📱 Using LOCAL template (high confidence 0.95)`

3. **Modo Balanced** → Preguntar "qué dice mi carta sobre el amor"
   - **Esperado:** Backend (baja confianza)
   - **Log:** `☁️ Calling BACKEND (low confidence 0.75)`

4. **Modo Detailed** → Cualquier pregunta
   - **Esperado:** Siempre backend
   - **Log:** `☁️ Calling BACKEND (detailed mode)`

**✅ Esperado:** Cada modo tiene comportamiento distinto y observable

---

### Test #7: Premium Status correcto

**Pasos:**
1. Verificar que RevenueCat está inicializado
2. En Settings, verificar badge premium si corresponde
3. En Status Panel, verificar badge premium

**✅ Esperado:**
- Si test mode → badge premium visible
- Si usuario tiene suscripción activa → badge visible
- Si free tier → NO badge (o badge bloqueado)

**❌ Si falla:**
- Verificar `subscriptionService.isPremium`
- Revisar inicialización de RevenueCat
- Verificar API key de RevenueCat

**Debug:**
```dart
// Temporal en cosmic_status_panel.dart
debugPrint('🔐 Premium status: ${subscriptionService.isPremium}');
debugPrint('🔐 Current tier: ${subscriptionService.currentTier}');
```

---

## 🔍 TROUBLESHOOTING

### Síntoma: Chat sigue resetándose

**Posibles causas:**
1. Cache de build antiguo → ejecutar limpieza completa (paso 1)
2. Hot reload no capturó cambio → full restart de app
3. Otro listener está recreando el servicio

**Verificación:**
```bash
# Buscar ref.watch en consolidated_providers.dart
grep -n "ref.watch.*preferences" lib/providers/consolidated_providers.dart

# Debe mostrar CERO resultados en horoscopeChatServiceProvider
```

---

### Síntoma: Quick replies se siguen repitiendo

**Posibles causas:**
1. Normalización no está funcionando
2. Set no se está persistiendo entre llamadas

**Debug temporal:**
```dart
// En horoscope_chat_service.dart, método _generateQuickReplies
debugPrint('🎲 Pool size: ${allReplies.length}');
debugPrint('🎲 Recently used: ${_recentlyUsedReplies.toList()}');
debugPrint('🎲 Available after filter: ${availableReplies.length}');
debugPrint('🎲 Selected: $selectedReplies');
```

---

### Síntoma: Todas las preguntas van a backend

**Posibles causas:**
1. Threshold demasiado alto (pero 0.95 es correcto)
2. getConfidence() retorna valores muy bajos
3. Templates no están matching

**Debug temporal:**
```dart
// En horoscope_chat_service.dart, antes de decidir fuente
debugPrint('🎯 Category: ${categoryMatch.category}');
debugPrint('🎯 Confidence: ${categoryMatch.confidence}');
debugPrint('🎯 Has template: ${categoryMatch.matchedTemplate != null}');
debugPrint('🎯 Threshold: $confidenceThreshold');
```

---

### Síntoma: Padding sigue mal

**Posibles causas:**
1. Device específico (notch diferente)
2. Safe area no está calculándose bien

**Debug temporal:**
```dart
// En chat_history_widget.dart
final viewPadding = MediaQuery.of(context).viewPadding;
debugPrint('📱 Device model: ${Platform.operatingSystemVersion}');
debugPrint('📱 viewPadding.bottom: ${viewPadding.bottom}');
debugPrint('📱 Effective padding: ${160.0 + viewPadding.bottom}');
```

---

## 📱 COMANDO FINAL DE DEPLOY

### Deploy en Debug (con logs - RECOMENDADO para primera prueba)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Limpieza completa
flutter clean && rm -rf .dart_tool/ build/ ios/Pods/ ios/Podfile.lock

# Reinstalar
flutter pub get && cd ios && pod install && cd ..

# Deploy
flutter run -d 00008150-0015244A2288401C --debug
```

**Abrir Xcode console para ver logs:**
- Xcode → Window → Devices and Simulators
- Seleccionar iPhone conectado
- Click en "Open Console"
- Filtrar por "🎯" o "✅" para ver logs relevantes

---

### Deploy en Release (después de verificar debug)

```bash
flutter run -d 00008150-0015244A2288401C --release
```

**Nota:** En release mode no habrá logs, pero performance será óptima.

---

## ✅ CHECKLIST FINAL

Antes de reportar que todo funciona:

- [ ] Limpieza completa ejecutada (flutter clean + pods)
- [ ] Deploy en debug exitoso
- [ ] Test #1: Chat NO se resetea ✅
- [ ] Test #2: Quick replies visibles ✅
- [ ] Test #3: Quick replies NO se repiten ✅
- [ ] Test #4: Respuestas coherentes (logs verificados) ✅
- [ ] Test #5: Profiles aplican correctamente ✅
- [ ] Test #6: Engine modes funcionan ✅
- [ ] Test #7: Premium status correcto ✅
- [ ] Logs en Xcode muestran comportamiento esperado ✅
- [ ] Deploy en release funciona ✅

---

## 📊 LOGS ESPERADOS EN XCODE

Durante una sesión normal, deberías ver:

```
[Inicio de app]
🔐 Premium status: true
🔐 Current tier: premium

[Aplicar perfil Power User]
🎯 CosmicProfileService: Applying profile "powerUser"
   ├─ chatMode: balanced
   ├─ personality: wise
🎯 PreferencesService: Changing chatMode: "quick" → "balanced"
✅ PreferencesService: chatMode updated to "balanced" and persisted
🔔 PreferencesService: notifyListeners() → 3 listeners
✅ CosmicProfileService: Profile "powerUser" applied successfully

[Usuario pregunta "horóscopo de hoy"]
🎯 Chat mode: balanced | preferBackend: false | confidence: 0.95
📱 Using LOCAL template (high confidence 0.95)
🎲 Recently used replies: 0/12
🎲 Available pool: 15

[Usuario pregunta "analiza mi futuro"]
🎯 Chat mode: balanced | preferBackend: false | confidence: 0.75
☁️ Calling BACKEND (low confidence 0.75)
🎲 Recently used replies: 3/12
🎲 Available pool: 12

[Usuario cambia a modo Detailed]
🎯 PreferencesService: Changing chatMode: "balanced" → "detailed"
✅ PreferencesService: chatMode updated to "detailed" and persisted
🔔 PreferencesService: notifyListeners() → 4 listeners

[Usuario pregunta "horóscopo hoy" en modo detailed]
🎯 Chat mode: detailed | preferBackend: true | confidence: 0.95
☁️ Calling BACKEND (detailed mode)
```

**Nota:** Si NO ves estos logs, el deploy puede estar usando build cache antiguo.

---

## 🎯 SI TODO FALLA

Si después de limpieza completa y deploy limpio siguen habiendo problemas:

1. **Reportar con logs específicos:**
   - Captura de pantalla del síntoma
   - Logs de Xcode console relevantes
   - Pasos exactos para reproducir

2. **Verificar versión de Flutter:**
   ```bash
   flutter --version
   ```

3. **Verificar device iOS version:**
   - Settings → General → About → iOS Version

4. **Última opción - Reset completo de build:**
   ```bash
   cd ios
   xcodebuild clean
   rm -rf ~/Library/Developer/Xcode/DerivedData/*
   cd ..
   flutter clean
   flutter pub get
   cd ios
   pod install
   cd ..
   flutter run -d 00008150-0015244A2288401C --debug
   ```

---

**Generado:** 19 Noviembre 2025 04:40
**Versión:** 1.0
**Estado:** Listo para deploy limpio
