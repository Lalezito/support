# TODO-003: Backend Language Investigation - FINDINGS

**Fecha:** 2025-10-21 03:00 AM
**Status:** ✅ INVESTIGACIÓN COMPLETA

---

## 🎯 PROBLEMA ROOT CAUSE CONFIRMADO

### Backend Goal Generation Language Issue

**El problema:**
- Backend **SÍ acepta** `languageCode` parameter ✅
- Pero el prompt de AI **NO lo usa correctamente** ❌
- Resultado: AI genera contenido en inglés siempre

**Root Cause:**
```javascript
// backend/flutter-horoscope-backend/src/services/goalPlannerService.js:213
Make it deeply personal, actionable, and aligned with ${zodiacSign} characteristics. Language: ${languageCode}
```

El `languageCode` se menciona al **final del prompt** como una simple palabra. Esto NO funciona porque:
1. GPT-4 defaultea a inglés
2. No hay instrucción explícita de **responder EN** ese idioma
3. El system prompt NO menciona idioma

---

## ✅ SOLUCIÓN IDENTIFICADA

### Fix completo requiere:

1. **System Prompt mejorado** - Instrucciones de idioma específicas por lenguaje
2. **Main Prompt reforzado** - `languageCode` al INICIO con ejemplos
3. **Zodiac Traits expandidos** - Agregar element, modality, ruling planet
4. **Output Constraints** - Ejemplos de nombres buenos vs malos

---

## 📂 ARCHIVOS A MODIFICAR

### 1. `/backend/flutter-horoscope-backend/src/services/goalPlannerService.js`

**Cambios necesarios:**
- Línea 93-96: Add `_getSystemPrompt(languageCode)` method
- Línea 149-214: Refactor `_buildGoalPrompt()` con language enforcement
- Línea 42-55: Expand `zodiacTraits` con element/modality/planet

### 2. `/backend/flutter-horoscope-backend/src/routes/goalPlanner.js` (opcional)

**Mejora opcional:**
- Línea 161: Add Accept-Language header fallback

---

## 🔧 CÓDIGO DE FIX PROPUESTO

Ver detalles completos en el reporte del agente. Resumen:

### Fix 1: System Prompt con idioma
```javascript
_getSystemPrompt(languageCode) {
  const languageInstructions = {
    'es': 'Debes responder COMPLETAMENTE en español...',
    'en': 'You must respond COMPLETELY in English...',
    // etc
  };
  return `You are an expert astrologer...
  ${languageInstructions[languageCode]}
  Avoid fantasy names like "Rally's Ritual", "Golems"...`;
}
```

### Fix 2: Main Prompt reforzado
```javascript
return `IMPORTANT: Respond ENTIRELY in ${languageName}. All content must be in ${languageName}.

Generate a personalized SMART goal plan...
- Element: ${traits.element}
- Ruling Planet: ${traits.planet}
...`;
```

### Fix 3: Zodiac Traits completos
```javascript
aries: {
  element: 'Fire',
  modality: 'Cardinal',
  planet: 'Mars',
  strength: 'initiative',
  challenge: 'patience',
  style: 'action-oriented'
}
```

---

## 📊 IMPACTO ESTIMADO

- **Tiempo de implementación:** 1-2 horas
- **Breaking changes:** NO (backward compatible)
- **Testing requerido:** Generar metas en ES, EN, PT
- **Deploy:** Backend + Flutter app (para pasar languageCode)

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Aplicar Fix 1: System Prompt
2. ✅ Aplicar Fix 2: Main Prompt
3. ✅ Aplicar Fix 3: Zodiac Traits
4. ⏳ Modificar Flutter app para pasar `languageCode`
5. ⏳ Testing: Generar metas en español
6. ⏳ Deploy backend + app

---

**Reporte completo guardado para referencia.**
**Ready to implement.**
