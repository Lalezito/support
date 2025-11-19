# 📱 TESTING FLUTTER OFFLINE - 19 Nov 2025

**Tiempo:** 10-15 minutos
**Objetivo:** Validar puntos 1, 2, 5 mientras backend deploya
**Device:** iPhone 00008150-0015244A2288401C

---

## ⚡ QUICK START (30 segundos)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Run en iPhone
flutter run -d 00008150-0015244A2288401C

# Esperar: "Flutter run key commands"
# App abrirá automáticamente
```

---

## 🧪 TESTS QUE PODEMOS HACER SIN BACKEND

### ✅ Punto 1: Quick Replies Condicionales
**Funciona offline:** SÍ - Es lógica local Flutter

### ✅ Punto 2: Localización 6 Idiomas
**Funciona offline:** SÍ - Traducciones están en código

### ✅ Punto 5: Botón Favoritos
**Funciona offline:** SÍ - Guarda en SharedPreferences local

### ⏸️ Punto 3: Header Pill
**Funciona offline:** NO - Necesita horoscopeData del backend

### ⏸️ Punto 4: Daily Highlights
**Funciona offline:** NO - Necesita horoscopeData del backend

---

## 📋 TEST 1: QUICK REPLIES (2 min)

### Pasos:
1. Abrir app en iPhone
2. Navegar a: Premium → Cosmic Coach
3. **Verificar estado inicial:**
   - Chat debe estar vacío
   - Input bar debe estar limpia
   - ❌ NO debe haber quick replies chips arriba del input

4. **Enviar un mensaje:**
   - Escribir: "Hola"
   - Tap Send

5. **Verificar después de respuesta AI:**
   - Debe aparecer respuesta del bot
   - ✅ Ahora SÍ deben aparecer quick replies chips

### ✅ Test PASS si:
- Chat vacío → Sin quick replies
- Con mensajes → Con quick replies

### ❌ Test FAIL si:
- Chat vacío muestra quick replies (no debería)

---

## 📋 TEST 2: LOCALIZACIÓN - ESPAÑOL (2 min)

### Setup:
```
iPhone Settings → General → Language & Region → Español
(Si ya está en español, skip este paso)
```

### Pasos:
1. Cerrar app completamente (swipe up)
2. Reabrir app
3. Navegar a: Premium → Cosmic Coach
4. Si hay mensajes previos, borrarlos:
   - Long press en mensaje → Delete all

5. **Verificar estado vacío en español:**

```
┌─────────────────────────────────────┐
│                                     │
│     [Icono Cosmic Coach]            │
│                                     │
│   Welcome to your Cosmic Coach      │
│   Ask me anything...                │
│                                     │
│   Prueba preguntar:            ← ✅ │
│                                     │
│   • ¿Cómo está mi energía hoy?      │
│   • ¿Qué dice mi horóscopo?         │
│   • Necesito un consejo             │
│                                     │
└─────────────────────────────────────┘
```

### ✅ Test PASS si:
- Aparece: "**Prueba preguntar:**" (no "Try asking:")
- Sugerencias en español

### ❌ Test FAIL si:
- Dice "Try asking:" en lugar de "Prueba preguntar:"

---

## 📋 TEST 3: LOCALIZACIÓN - INGLÉS (2 min)

### Setup:
```
iPhone Settings → General → Language & Region → English
```

### Pasos:
1. Cerrar app completamente
2. Reabrir app
3. Navegar a: Premium → Cosmic Coach
4. Limpiar chat si hay mensajes

5. **Verificar estado vacío en inglés:**

```
┌─────────────────────────────────────┐
│                                     │
│     [Cosmic Coach Icon]             │
│                                     │
│   Welcome to your Cosmic Coach      │
│   Ask me anything...                │
│                                     │
│   Try asking:                  ← ✅ │
│                                     │
│   • How is my energy today?         │
│   • What does my horoscope say?     │
│   • I need some advice              │
│                                     │
└─────────────────────────────────────┘
```

### ✅ Test PASS si:
- Aparece: "**Try asking:**"
- Sugerencias en inglés

---

## 📋 TEST 4: LOCALIZACIÓN - ALEMÁN (Opcional, 2 min)

### Setup:
```
iPhone Settings → General → Language & Region → Deutsch (German)
```

### Verificar:
```
Versuche zu fragen:  ← ✅ Debe aparecer esto

(No "Try asking:" ni "Prueba preguntar:")
```

### Otros idiomas (opcional):
- **Francés:** "Essayez de demander :"
- **Italiano:** "Prova a chiedere:"
- **Portugués:** "Experimente perguntar:"

---

## 📋 TEST 5: BOTÓN FAVORITOS (3 min)

### Pasos:

1. **Cambiar de vuelta a español o inglés**
   - Settings iPhone → Language → Español/English

2. **Abrir Cosmic Coach**
   - Premium → Cosmic Coach

3. **Enviar un mensaje:**
   - Escribir: "¿Cómo está mi día?"
   - Esperar respuesta AI

4. **Buscar el botón Save:**
   - Debe aparecer debajo del mensaje AI
   - Icono: ⭐ (estrella outline)
   - Texto: "Save"

```
┌─────────────────────────────────────┐
│  🤖 AI                              │
│  Tu día está lleno de oportunida-  │
│  des cósmicas...                    │
│                                     │
│  ⭐ Save                        ← ✅ │
│                                     │
└─────────────────────────────────────┘
```

5. **Tap en "Save":**
   - Debe aparecer SnackBar (notificación abajo)
   - Texto: "⭐ Message saved to favorites"
   - Color: Morado
   - Duración: 2 segundos

### ✅ Test PASS si:
- Botón "⭐ Save" visible en mensajes AI
- Tap muestra SnackBar de confirmación
- No da error

### ❌ Test FAIL si:
- Botón no aparece
- Tap da error
- No hay feedback visual

---

## 📋 TEST 6: UI GENERAL (2 min)

### Verificar que no se rompió nada:

**Header:**
- [ ] Muestra "👤 Cosmic Coach"
- [ ] Tiene botón back funcional
- [ ] (No veremos pill porque backend no responde aún)

**Chat Input:**
- [ ] Placeholder text visible
- [ ] Se puede escribir
- [ ] Botón send funcional

**Mensajes:**
- [ ] Se muestran correctamente
- [ ] User messages alineados a derecha
- [ ] AI messages alineados a izquierda
- [ ] Timestamps visibles

**No hay crashes:**
- [ ] App no crashea al abrir chat
- [ ] App no crashea al enviar mensaje
- [ ] App no crashea al cambiar idioma

---

## 📊 REPORTE DE RESULTADOS

### Formato sugerido:

```markdown
# Testing Offline - 19 Nov 2025 - [HH:MM]

## Punto 1: Quick Replies
- Chat vacío: ✅ / ❌
- Con mensajes: ✅ / ❌

## Punto 2: Localización
- Español: ✅ / ❌ ("Prueba preguntar:")
- Inglés: ✅ / ❌ ("Try asking:")
- Alemán: ✅ / ❌ / ⏸️ (opcional)

## Punto 5: Favoritos
- Botón visible: ✅ / ❌
- Tap funciona: ✅ / ❌
- SnackBar aparece: ✅ / ❌

## UI General
- Sin crashes: ✅ / ❌
- Header correcto: ✅ / ❌
- Input funcional: ✅ / ❌

## Issues encontrados
- [Listar cualquier problema]

## Conclusión
✅ Todo funciona / ⚠️ Issues encontrados / ❌ Tests fallaron
```

---

## 🎯 DESPUÉS DEL TESTING OFFLINE

### Si todo funciona (esperado):
✅ Puntos 1, 2, 5 validados
⏸️ Puntos 3, 4 esperan backend

**Siguiente acción:**
- Verificar Railway deployment completado
- Re-testear backend con curl
- Testing completo con backend funcionando

### Si algo falla:
❌ Documentar el issue
🔧 Investigar y fixear
🧪 Re-testear

---

## ⚡ COMANDOS ÚTILES

### Ver logs mientras testeas:
```bash
# En la terminal donde corre flutter run, los logs aparecerán automáticamente

# Buscar logs específicos:
# Filtrar por "HoroscopeChat":
# Los logs mostrarán información del service
```

### Hot reload durante testing:
```
r    → Hot reload (para cambios UI pequeños)
R    → Hot restart (para cambios de estado)
q    → Quit
```

### Si app crashea:
```bash
# Re-run:
flutter run -d 00008150-0015244A2288401C

# O con verbose:
flutter run -d 00008150-0015244A2288401C -v
```

---

## 📸 SCREENSHOTS RECOMENDADOS

Mientras testeas, toma capturas de:

1. **Estado vacío - Español**
   - Mostrando "Prueba preguntar:"

2. **Estado vacío - Inglés**
   - Mostrando "Try asking:"

3. **Botón Save en mensaje AI**
   - Con el botón "⭐ Save" visible

4. **SnackBar de confirmación**
   - Después de tap en Save

**Guardar en:**
```
/Users/alejandrocaceres/Desktop/appstore.zodia/screenshots/testing_offline_nov19/
```

---

## ✅ CHECKLIST RÁPIDO

Antes de empezar:
- [ ] iPhone conectado y desbloqueado
- [ ] Terminal abierto en `zodiac_app/`
- [ ] Listo para tomar screenshots

Durante testing:
- [ ] Test 1: Quick replies → 2 min
- [ ] Test 2: Localización ES → 2 min
- [ ] Test 3: Localización EN → 2 min
- [ ] Test 4: Localización DE (opcional) → 2 min
- [ ] Test 5: Botón favoritos → 3 min
- [ ] Test 6: UI general → 2 min

Después:
- [ ] Crear reporte de resultados
- [ ] Guardar screenshots
- [ ] Documentar issues (si hay)

**Tiempo total:** 10-15 minutos

---

**Generado:** 19 Nov 2025 - 09:30
**Autor:** Claude Code Agent
**Estado:** ✅ Listo para ejecutar

🚀 **Run:** `flutter run -d 00008150-0015244A2288401C`
