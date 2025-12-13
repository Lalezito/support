# 🧪 TESTING RÁPIDO - Puntos 1, 2 y 3

**Tiempo estimado:** 15 minutos
**Requisitos:** Backend deployado, iPhone conectado

---

## 🚀 PASO 1: Deploy Backend (3 min)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend

# Ver cambios
git diff src/services/aiCoachService.js

# Commit
git add src/services/aiCoachService.js
git commit -m "feat: Add horoscope data (energy + colors) to chat responses

- Modified _generateAIResponse to fetch daily horoscope
- Added horoscopeData to response object (energyLevel, luckyColors, etc.)
- Added horoscopeData to fallback response
- Modified sendMessage to include horoscopeData in final response
- Supports ES/EN for energy labels
- Backend ready for personalized header pill display"

# Push
git push origin main

# Monitorear deploy
railway logs --tail 50

# Esperar: "✅ Deployment successful" (1-2 min)
```

**Verificar:**
```bash
# Test con curl
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/horoscope-chat/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo está mi día?",
    "userId": "test-nov19",
    "zodiacSign": "Leo",
    "language": "es"
  }' | jq '.data.horoscopeData'

# Debe devolver:
# {
#   "energyLevel": "high",
#   "luckyColors": "dorado, púrpura",
#   "favorableTimes": "14:00-16:00, 20:00-22:00",
#   ...
# }
```

---

## 📱 PASO 2: Testing Flutter en iPhone (10 min)

### 2.1 Build y Run

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Run en iPhone físico
flutter run -d 00008150-0015244A2288401C

# Esperar: "✅ App running"
```

### 2.2 Testing Punto 1: Quick Replies

**Test:** Quick replies NO aparecen en chat vacío

1. Abrir Cosmic Coach
2. Verificar estado vacío (sin mensajes)
3. ✅ **ESPERADO:** Input bar limpia, SIN quick replies
4. Enviar mensaje: "Hola"
5. Esperar respuesta AI
6. ✅ **ESPERADO:** Ahora SÍ aparecen quick replies del AI

**Resultado:**
- [ ] Chat vacío → NO quick replies ✅
- [ ] Con mensajes → SÍ quick replies ✅

---

### 2.3 Testing Punto 2: Localización (6 idiomas)

**Test:** "Try asking:" traducido en cada idioma

#### Idioma 1: Español
```
iPhone Settings → General → Language & Region → Spanish
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Prueba preguntar:" ✅

#### Idioma 2: Inglés
```
iPhone Settings → General → Language & Region → English
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Try asking:" ✅

#### Idioma 3: Alemán
```
iPhone Settings → General → Language & Region → Deutsch
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Versuche zu fragen:" ✅

#### Idioma 4: Francés
```
iPhone Settings → General → Language & Region → Français
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Essayez de demander :" ✅

#### Idioma 5: Italiano
```
iPhone Settings → General → Language & Region → Italiano
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Prova a chiedere:" ✅

#### Idioma 6: Portugués
```
iPhone Settings → General → Language & Region → Português
Reiniciar app
```

**Verificar:**
- [ ] Estado vacío muestra: "Experimente perguntar:" ✅

**Atajos rápidos:** Si tienes prisa, testea solo ES + EN

---

### 2.4 Testing Punto 3: Header con Pill Personalizada

**Test:** Pill aparece con energía + color después de respuesta AI

**Cambiar a español:**
```
iPhone Settings → General → Language & Region → Spanish
Reiniciar app
```

#### Caso 1: Leo (alta energía, dorado)

1. Abrir Cosmic Coach
2. Enviar: "¿Cómo está mi día?"
3. Esperar respuesta AI (3-5s)
4. **Verificar header:**

```
┌────────────────────────────────────┐
│  👤 Cosmic Coach                   │
│  ⚡ Alta • 🎨 Dorado              │ ← ✨ PILL NUEVA
├────────────────────────────────────┤
```

**Checklist:**
- [ ] Pill aparece debajo de "Cosmic Coach" ✅
- [ ] Icono: ⚡ (bolt - energía alta) ✅
- [ ] Color icono: Amarillo/amber ✅
- [ ] Texto: "Alta" (español) ✅
- [ ] Separador: • ✅
- [ ] Icono: 🎨 (palette) ✅
- [ ] Color: "Dorado" ✅
- [ ] Background: Morado con transparencia ✅

#### Caso 2: Aries (energía muy alta, rojo)

1. Cambiar signo a Aries en app (Settings → Profile → Sign → Aries)
2. Volver a Cosmic Coach
3. Enviar: "¿Qué me recomiendas hoy?"
4. **Verificar pill muestra datos de Aries:**

**Checklist:**
- [ ] Icono: ⚡ (energía muy alta) ✅
- [ ] Texto: "Alta" ✅
- [ ] Color: "Rojo" ✅

#### Caso 3: En inglés

**Cambiar a inglés:**
```
iPhone Settings → General → Language & Region → English
Reiniciar app
```

1. Abrir Cosmic Coach
2. Enviar: "How is my day?"
3. **Verificar pill en inglés:**

**Checklist:**
- [ ] Icono: ⚡ ✅
- [ ] Texto: "High" (inglés, NO "Alta") ✅
- [ ] Color: "Gold" (inglés, NO "Dorado") ✅

---

## 📸 PASO 3: Screenshots (2 min)

**Tomar capturas de:**

1. **Estado vacío en español**
   - Mostrar "Prueba preguntar:"
   - Suggestions visibles

2. **Estado vacío en inglés**
   - Mostrar "Try asking:"

3. **Header con pill - Leo ES**
   - Cosmic Coach header
   - Pill: ⚡ Alta • 🎨 Dorado

4. **Header con pill - Leo EN**
   - Cosmic Coach header
   - Pill: ⚡ High • 🎨 Gold

**Guardar en:**
```
/Users/alejandrocaceres/Desktop/appstore.zodia/screenshots/cosmic_coach_improvements_nov19/
```

---

## ✅ CHECKLIST COMPLETO

### Backend
- [ ] Deploy a Railway exitoso
- [ ] Logs sin errores
- [ ] Curl test devuelve horoscopeData
- [ ] horoscopeData incluye: energyLevel, luckyColors

### Flutter - Punto 1
- [ ] Chat vacío sin quick replies
- [ ] Chat con mensajes muestra quick replies

### Flutter - Punto 2
- [ ] Español: "Prueba preguntar:"
- [ ] Inglés: "Try asking:"
- [ ] (Opcional) Alemán: "Versuche zu fragen:"
- [ ] (Opcional) Francés: "Essayez de demander :"
- [ ] (Opcional) Italiano: "Prova a chiedere:"
- [ ] (Opcional) Portugués: "Experimente perguntar:"

### Flutter - Punto 3
- [ ] Pill aparece en header
- [ ] Icono de energía correcto (⚡/☀️/🌙/⚖️)
- [ ] Color de icono correcto
- [ ] Label de energía en idioma correcto
- [ ] Color de la suerte mostrado
- [ ] Color mapeado a inglés si idioma EN

### Screenshots
- [ ] 4 screenshots tomadas
- [ ] Guardadas en carpeta apropiada

---

## 🐛 TROUBLESHOOTING

### Problema: Pill NO aparece

**Diagnóstico:**
```bash
# En terminal donde corre flutter run, buscar:
flutter: [HoroscopeChat] Response metadata: {...}

# Debe mostrar:
# metadata: {horoscopeData: {energyLevel: high, luckyColors: dorado, púrpura, ...}}
```

**Soluciones:**

1. **Backend no devuelve horoscopeData:**
   - Verificar logs Railway: `railway logs | grep horoscopeData`
   - Asegurar datos test insertados en PostgreSQL
   - Ejecutar: `backend/SETUP_TEST_DATA_HOROSCOPE.sql`

2. **Flutter no captura metadata:**
   - Verificar línea 179-186 de `horoscope_chat_models.dart`
   - Debe tener: `if (json['horoscopeData'] != null) { metadata = {...} }`

3. **Consumer no detecta cambio:**
   - Hot reload NO funciona para providers
   - Hot restart: `r` en terminal
   - O rerun completo: `R`

---

### Problema: Localización no funciona

**Diagnóstico:**
```dart
// En cosmic_coach_chat_screen.dart, añadir log temporal:
final languageCode = Localizations.localeOf(context).languageCode;
print('DEBUG: languageCode = $languageCode');
```

**Soluciones:**

1. **Idioma no cambia:**
   - Cerrar app completamente
   - Cambiar idioma en Settings iPhone
   - Reabrir app (NO hot reload)

2. **Traducción incorrecta:**
   - Verificar método `_getEmptyStateTryAskingLabel` líneas 908-925
   - Verificar switch tiene todos los idiomas

---

### Problema: Quick replies aparecen en chat vacío

**Diagnóstico:**
```dart
// Línea 478-480
final quickReplies = state.messages.isEmpty
    ? <QuickReply>[]
    : _getQuickRepliesFromState(state, context);

// Añadir log:
print('DEBUG: messages.isEmpty = ${state.messages.isEmpty}');
print('DEBUG: quickReplies count = ${quickReplies.length}');
```

**Solución:**
- Si aparecen, verificar que código es exactamente como arriba
- Hot restart: `R`

---

## 📝 REPORTE DE TESTING

**Formato:**

```markdown
# Testing Puntos 1-2-3 - 19 Nov 2025

## Punto 1: Quick Replies
- ✅ Chat vacío sin quick replies
- ✅ Chat con mensajes muestra quick replies

## Punto 2: Localización
- ✅ ES: "Prueba preguntar:"
- ✅ EN: "Try asking:"
- ⏸️ DE/FR/IT/PT: No testeado

## Punto 3: Header Pill
- ✅ Pill aparece después de mensaje AI
- ✅ Icono de energía correcto
- ✅ Label en español: "Alta"
- ✅ Label en inglés: "High"
- ✅ Color mostrado: "Dorado" / "Gold"

## Issues encontrados
- Ninguno / [Describir si hubo]

## Screenshots
- [x] 4 screenshots tomadas

## Conclusión
✅ Todo funciona según esperado
```

---

**Tiempo total:** 15 minutos
**Estado:** Listo para ejecutar
**Próximo:** Después de testing exitoso → Punto 4 o commit final
