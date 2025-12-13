# 📱 GUÍA TESTING MANUAL RÁPIDO - 19 Nov 2025

**Tiempo:** 10-15 minutos
**Device:** iPhone 00008150-0015244A2288401C
**App:** Running in background

---

## ⚡ QUICK START

La app está corriendo en el iPhone. Sigue este checklist en orden:

---

## ✅ TEST 1: Estado Vacío sin Quick Replies (2 min)

### Pasos:
1. **Abrir Cosmic Coach:**
   - Navegar a: Premium → Cosmic Coach

2. **Verificar estado vacío:**
   ```
   ┌─────────────────────────────────────┐
   │                                     │
   │     [Icono Cosmic Coach]            │
   │                                     │
   │   Pregúntame sobre tu horóscopo     │  ← Título
   │   Soy tu astrólogo personal...      │  ← Subtitle
   │                                     │
   │   Prueba preguntar:                 │  ← Label
   │                                     │
   │   • ¿Cómo está mi energía hoy?      │  ← Sugerencias
   │   • ¿Qué dice mi horóscopo?         │
   │   • Necesito un consejo             │
   │                                     │
   │                                     │
   │  [Input bar LIMPIA]                 │  ← SIN quick replies
   └─────────────────────────────────────┘
   ```

### ✅ Verificar:
- [ ] NO hay quick replies chips arriba del input
- [ ] Hay sugerencias en el estado vacío
- [ ] Input bar está limpia (solo placeholder)

### ❌ Si falla:
- Quick replies aparecen en input → BUG (reportar)

---

## ✅ TEST 2: Localización Español (2 min)

### Setup:
```
iPhone Settings → General → Language & Region → Español
```

### Verificar en estado vacío:
- [ ] Título: "**Pregúntame sobre tu horóscopo**"
- [ ] Subtitle: "**Soy tu astrólogo personal disponible 24/7...**"
- [ ] Label: "**Prueba preguntar:**"

### ❌ Si falla:
- Aparece en inglés → Verificar idioma del dispositivo

---

## ✅ TEST 3: Localización Inglés (2 min)

### Setup:
```
iPhone Settings → General → Language & Region → English
```

### Verificar en estado vacío:
- [ ] Título: "**Ask me about your horoscope**"
- [ ] Subtitle: "**I am your personal astrologer available 24/7...**"
- [ ] Label: "**Try asking:**"

### ❌ Si falla:
- Aparece en español → Reiniciar app completamente

---

## ✅ TEST 4: Quick Replies Dinámicas (1 min)

### Pasos:
1. **Enviar un mensaje:**
   - Escribir: "Hola"
   - Tap Send

2. **Esperar respuesta AI** (3-5 segundos)

3. **Verificar:**
   - [ ] Ahora SÍ aparecen quick replies arriba del input
   - [ ] Son sugerencias dinámicas del AI

### ❌ Si falla:
- No aparecen quick replies → Verificar backend responde

---

## ✅ TEST 5: Header Pill con Energía + Color (3 min)

**NOTA:** Requiere backend funcionando y devolviendo horoscopeData

### Pasos:
1. **Enviar mensaje:**
   - Escribir: "¿Cómo está mi día?"
   - Tap Send

2. **Esperar respuesta AI**

3. **Verificar header:**
   ```
   ┌────────────────────────────────────┐
   │  👤 Cosmic Coach                   │
   │  ⚡ Alta • 🎨 Dorado              │ ← PILL NUEVA
   ├────────────────────────────────────┤
   ```

### ✅ Verificar:
- [ ] Pill aparece debajo de "Cosmic Coach"
- [ ] Icono de energía (⚡ = alta, ☀️ = media, 🌙 = baja, ⚖️ = equilibrada)
- [ ] Label de energía en idioma correcto
  - ES: "Alta" / "Media" / "Baja" / "Equilibrada"
  - EN: "High" / "Medium" / "Low" / "Balanced"
- [ ] Separador: •
- [ ] Icono palette: 🎨
- [ ] Color mostrado: "Dorado" / "Gold" / etc.

### ❌ Si falla:
- Pill NO aparece → Backend no está devolviendo horoscopeData
- Solución: Verificar Railway deployment completó

---

## ✅ TEST 6: Daily Highlights Card (2 min)

**NOTA:** Requiere backend funcionando

### Pasos:
1. **Enviar mensaje**
2. **Verificar que ANTES del mensaje AI aparece card especial:**

```
┌─────────────────────────────────────┐
│ 🌟 Hoy para Leo                     │
│                                     │
│ ⚡ Energía: Alta                    │
│ ⏰ Horarios favorables:             │
│    14:00-16:00, 20:00-22:00        │
│ 🎨 Color de poder: Dorado          │
│                                     │
│ 💖 Amor: [texto de guidance]        │
│ 💼 Carrera: [texto de guidance]     │
│ 🧘 Bienestar: [texto de guidance]   │
└─────────────────────────────────────┘
```

### ✅ Verificar:
- [ ] Card aparece ANTES del mensaje AI (no después)
- [ ] Tiene gradiente morado de fondo
- [ ] Tiene borde morado translúcido
- [ ] Muestra emojis: 🌟⚡⏰🎨💖💼🧘
- [ ] Texto en idioma correcto (ES o EN)

### ❌ Si falla:
- Card NO aparece → Backend no devuelve horoscopeData
- Card aparece después → Revisar orden de inserción

---

## ✅ TEST 7: Botón Favoritos (2 min)

### Pasos:
1. **Enviar mensaje y esperar respuesta AI**

2. **Buscar botón Save:**
   ```
   ┌─────────────────────────────────────┐
   │  🤖 AI                              │
   │  Tu día está lleno de oportunida-  │
   │  des cósmicas...                    │
   │                                     │
   │  ⭐ Save                        ← ✅ │
   └─────────────────────────────────────┘
   ```

3. **Tap en "⭐ Save"**

4. **Verificar SnackBar:**
   ```
   ┌─────────────────────────────────────┐
   │  ⭐ Message saved to favorites      │ ← SnackBar morado
   └─────────────────────────────────────┘
   ```

### ✅ Verificar:
- [ ] Botón "⭐ Save" visible solo en mensajes AI
- [ ] Botón NO visible en mensajes del usuario
- [ ] Tap muestra SnackBar
- [ ] SnackBar tiene fondo morado
- [ ] SnackBar desaparece después de 2 segundos

### ❌ Si falla:
- Botón NO aparece → Verificar provider inicializado
- Error al guardar → Hot restart: `R` en terminal

---

## 📊 CHECKLIST RESUMEN

### Estado Vacío:
- [ ] Título localizado ✅
- [ ] Subtitle localizado ✅
- [ ] Label "Prueba preguntar:" localizado ✅
- [ ] NO quick replies en input ✅

### Multiidioma:
- [ ] Español funciona ✅
- [ ] Inglés funciona ✅
- [ ] (Opcional) Alemán/Francés/Italiano/Portugués ✅

### Quick Replies:
- [ ] Chat vacío → sin quick replies ✅
- [ ] Con mensajes → con quick replies ✅

### Header Pill:
- [ ] Aparece después de mensaje AI ✅
- [ ] Muestra energía correcta ✅
- [ ] Muestra color correcto ✅
- [ ] Localizado (ES/EN) ✅

### Daily Highlights:
- [ ] Card aparece ANTES de AI message ✅
- [ ] Gradiente morado ✅
- [ ] Emojis correctos ✅
- [ ] Texto localizado ✅

### Favoritos:
- [ ] Botón visible en AI messages ✅
- [ ] Tap funciona ✅
- [ ] SnackBar aparece ✅

---

## 🐛 TROUBLESHOOTING

### Problema: Backend no responde

**Síntomas:**
- Pill NO aparece
- Daily highlights NO aparecen
- Mensajes AI tardan mucho

**Solución:**
```bash
# Verificar Railway
curl https://zodiac-backend-api-production-8ded.up.railway.app/health

# Si falla, esperar 5-10 min más para deployment
```

---

### Problema: Pill aparece pero sin datos

**Síntomas:**
- Pill vacía o con valores por defecto

**Solución:**
1. Verificar datos test insertados en PostgreSQL
2. Ejecutar: `backend/SETUP_TEST_DATA_HOROSCOPE.sql`
3. Reiniciar backend

---

### Problema: Highlights no aparecen

**Diagnóstico:**
```
# Buscar en logs Flutter:
flutter: [HoroscopeChat] Response metadata: {...}
```

**Solución:**
- Verificar backend devuelve horoscopeData
- Hot restart: `R` en terminal
- Verificar service crea highlight message

---

### Problema: Favoritos no guarda

**Solución:**
1. Hot restart: `R` en terminal
2. Verificar provider inicializado
3. Verificar FavoriteMessageService.instance.initialize()

---

## 📸 SCREENSHOTS RECOMENDADOS

Si todo funciona, tomar capturas de:

1. **Estado vacío ES**
   - Con "Prueba preguntar:"

2. **Estado vacío EN**
   - Con "Try asking:"

3. **Header con pill**
   - Mostrando ⚡ Alta • 🎨 Dorado

4. **Daily highlights card**
   - Card completa con gradiente

5. **Botón favoritos + SnackBar**
   - Después de tap en Save

**Guardar en:**
```
/Users/alejandrocaceres/Desktop/appstore.zodia/screenshots/testing_nov19/
```

---

## ✅ RESULTADO ESPERADO

Si todo pasa:

```
╔═══════════════════════════════════════════════╗
║  TESTING MANUAL COMPLETO                      ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  ✅ Estado vacío sin quick replies           ║
║  ✅ Localización 6 idiomas                   ║
║  ✅ Quick replies dinámicas                  ║
║  ✅ Header pill funcional                    ║
║  ✅ Daily highlights card                    ║
║  ✅ Favoritos funcional                      ║
║                                               ║
║  🎊 OK PARA DEPLOY FINAL                      ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

**Siguiente:** Deploy final y documentación de release

---

**Generado:** 19 Nov 2025 - 10:15
**Estado:** App running - Testing en progreso
**Tiempo estimado:** 10-15 minutos
