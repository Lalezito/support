# 📋 PLAN MAESTRO - Traducción Context-Aware Goals (16 Nov 2025)

**Objetivo:** Traducir TODOS los context-aware goals a 6 idiomas (EN, ES, PT, FR, DE, IT)

**Archivo objetivo:** `context_aware_goal_generator.dart` → Crear `context_aware_goal_translations.dart`

**Alcance:** 721 líneas de código, ~100 microHabits, 15 funciones

---

## 📊 INVENTARIO COMPLETO DE CONTENIDO A TRADUCIR

### CATEGORÍA 1: SLEEP GOALS (Líneas 8-299)

#### 1.1 Excellent Sleep Goals (7-9 horas) - Líneas 36-99
**2 goals completos:**

**Goal 1:** "Harness Your Peak Energy"
- ✅ Title: "Harness Your Peak Energy"
- ✅ Description: Con variable zodiacSign + función _getZodiacSleepQuality()
- ✅ 2 microHabits:
  - habit + when + why + difficulty
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con función _getZodiacMotivation()
- ✅ source: "Harvard Sleep Study 2023"

**Goal 2:** "Protect Your Sleep Wins"
- ✅ Title: "Protect Your Sleep Wins"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 1.2 Sleep Deprived Goals (<6 horas) - Líneas 101-187
**2 goals completos:**

**Goal 1:** "Recovery Mode: Gentle Goals Only"
- ✅ Title: "Recovery Mode: Gentle Goals Only"
- ✅ Description: Con variables hours + sleepDebt calculado
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign
- ✅ source: "NASA Fatigue Countermeasures Program"

**Goal 2:** "Tonight: Sleep Debt Payback Plan"
- ✅ Title: "Tonight: Sleep Debt Payback Plan"
- ✅ Description: Con variable zodiacSign
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable sleepDebt

#### 1.3 Too Much Sleep Goals (>9 horas) - Líneas 189-261
**2 goals completos:**

**Goal 1:** "Quality Over Quantity Check"
- ✅ Title: "Quality Over Quantity Check"
- ✅ Description: Con variable hours
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

**Goal 2:** "Evening Energy Anchor"
- ✅ Title: "Evening Energy Anchor"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 1.4 Decent Sleep Goals (6-7 horas) - Líneas 263-299
**1 goal completo:**

**Goal 1:** "Good Enough, But Let's Aim Higher"
- ✅ Title: "Good Enough, But Let's Aim Higher"
- ✅ Description: Con variable hours
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

**SUBTOTAL SLEEP:** 7 goals, 17 microHabits, 24 successIndicators

---

### CATEGORÍA 2: ZODIAC-SPECIFIC CONTENT (Líneas 301-353)

#### 2.1 Sleep Quality Phrases - Línea 302-318
**Función:** `_getZodiacSleepQuality(String zodiacSign)`

12 frases específicas por signo:
- ✅ aries: 'warrior-quality'
- ✅ taurus: 'luxurious'
- ✅ gemini: 'mentally refreshing'
- ✅ cancer: 'deeply restorative'
- ✅ leo: 'regal'
- ✅ virgo: 'perfectly optimized'
- ✅ libra: 'beautifully balanced'
- ✅ scorpio: 'intensely rejuvenating'
- ✅ sagittarius: 'adventure-ready'
- ✅ capricorn: 'productive'
- ✅ aquarius: 'innovative'
- ✅ pisces: 'dreamy and healing'
- ✅ default: 'excellent'

#### 2.2 Motivational Messages - Líneas 320-353
**Función:** `_getZodiacMotivation(String zodiacSign, String context)`

**Context: 'excellent' (12 motivaciones):**
- ✅ aries: "Channel this energy into conquering your boldest goal today!"
- ✅ taurus: "Your patient nature + great sleep = unstoppable determination."
- ✅ gemini: "Your mind is sharp and ready to learn something amazing today."
- ✅ cancer: "You're emotionally centered - perfect for nurturing your goals."
- ✅ leo: "Shine bright today - you have the energy to inspire others!"
- ✅ virgo: "Your attention to detail is at peak performance. Tackle complex tasks!"
- ✅ libra: "Your balanced energy creates harmony in everything you touch today."
- ✅ scorpio: "Your focus is laser-sharp. Go deep on something meaningful."
- ✅ sagittarius: "Adventure awaits - your optimistic energy will open doors!"
- ✅ capricorn: "Your disciplined nature + rest = massive progress today."
- ✅ aquarius: "Your innovative mind is ready to solve problems creatively."
- ✅ pisces: "Your intuition is crystal clear - trust your gut decisions today."
- ✅ default: "You're well-rested and ready to thrive!"

**SUBTOTAL ZODIAC:** 25 textos específicos

---

### CATEGORÍA 3: EMOTIONAL GOALS (Líneas 355-720)

#### 3.1 Stressed Goals - Líneas 387-428
**1 goal completo:**

**Goal 1:** "Cortisol Reset: Science-Backed Stress Relief"
- ✅ Title: "Cortisol Reset: Science-Backed Stress Relief"
- ✅ Description
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign
- ✅ source: "Harvard Medical School Stress Management Study"

#### 3.2 Anxious Goals - Líneas 431-469
**1 goal completo:**

**Goal 1:** "Anxiety Anchor: Ground Yourself"
- ✅ Title: "Anxiety Anchor: Ground Yourself"
- ✅ Description
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.3 Calm Goals - Líneas 472-503
**1 goal completo:**

**Goal 1:** "Leverage Your Calm for Deep Work"
- ✅ Title: "Leverage Your Calm for Deep Work"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.4 Energized Goals - Líneas 506-537
**1 goal completo:**

**Goal 1:** "High Energy = High Impact Actions"
- ✅ Title: "High Energy = High Impact Actions"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.5 Tired Goals - Líneas 540-578
**1 goal completo:**

**Goal 1:** "Energy Management, Not Time Management"
- ✅ Title: "Energy Management, Not Time Management"
- ✅ Description
- ✅ 3 microHabits
- ✅ 4 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.6 Motivated Goals - Líneas 581-612
**1 goal completo:**

**Goal 1:** "Motivation x Strategy = Momentum"
- ✅ Title: "Motivation x Strategy = Momentum"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.7 Unmotivated Goals - Líneas 615-646
**1 goal completo:**

**Goal 1:** "Micro-Progress: 2-Minute Wins"
- ✅ Title: "Micro-Progress: 2-Minute Wins"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.8 Confident Goals - Líneas 649-680
**1 goal completo:**

**Goal 1:** "Confidence = Risk-Taking Opportunity"
- ✅ Title: "Confidence = Risk-Taking Opportunity"
- ✅ Description
- ✅ 2 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

#### 3.9 Uncertain Goals - Líneas 683-720
**1 goal completo:**

**Goal 1:** "Clarity Through Action"
- ✅ Title: "Clarity Through Action"
- ✅ Description
- ✅ 3 microHabits
- ✅ 3 successIndicators
- ✅ motivationalMessage: Con variable zodiacSign

**SUBTOTAL EMOTIONAL:** 9 goals, 22 microHabits, 31 successIndicators

---

## 📈 TOTALES GENERALES

### Por categoría:
- **Sleep Goals:** 7 goals
- **Zodiac-specific:** 25 frases
- **Emotional Goals:** 9 goals
- **TOTAL GOALS:** 16 goals completos

### Por componente:
- **Titles:** 16 títulos
- **Descriptions:** 16 descripciones
- **MicroHabits:** 39 microHabits × 3 campos (habit, when, why) = 117 textos
- **SuccessIndicators:** 55 indicators totales
- **MotivationalMessages:** 16 mensajes
- **Zodiac-specific:** 25 textos
- **Sources:** 2 fuentes científicas

### Gran total de textos a traducir:
**245 textos únicos en inglés** × 5 idiomas adicionales = **~1,225 traducciones**

---

## 🗂️ ESTRUCTURA DEL ARCHIVO DE TRADUCCIONES

### Nombre del archivo:
`context_aware_goal_translations.dart`

### Estructura de clases:

```dart
class ContextAwareGoalTranslations {

  // ══════════════════════════════════════════════════════════════════════════
  // SLEEP GOALS - EXCELLENT (7-9 hours)
  // ══════════════════════════════════════════════════════════════════════════

  static Map<String, dynamic> excellentSleepGoal1(String lang, String zodiacSign) { }
  static Map<String, dynamic> excellentSleepGoal2(String lang, String zodiacSign) { }

  // ══════════════════════════════════════════════════════════════════════════
  // SLEEP GOALS - DEPRIVED (<6 hours)
  // ══════════════════════════════════════════════════════════════════════════

  static Map<String, dynamic> deprivedSleepGoal1(String lang, String zodiacSign, double hours, double sleepDebt) { }
  static Map<String, dynamic> deprivedSleepGoal2(String lang, String zodiacSign, double sleepDebt) { }

  // ══════════════════════════════════════════════════════════════════════════
  // SLEEP GOALS - TOO MUCH (>9 hours)
  // ══════════════════════════════════════════════════════════════════════════

  static Map<String, dynamic> tooMuchSleepGoal1(String lang, String zodiacSign, double hours) { }
  static Map<String, dynamic> tooMuchSleepGoal2(String lang, String zodiacSign) { }

  // ══════════════════════════════════════════════════════════════════════════
  // SLEEP GOALS - DECENT (6-7 hours)
  // ══════════════════════════════════════════════════════════════════════════

  static Map<String, dynamic> decentSleepGoal1(String lang, String zodiacSign, double hours) { }

  // ══════════════════════════════════════════════════════════════════════════
  // ZODIAC-SPECIFIC CONTENT
  // ══════════════════════════════════════════════════════════════════════════

  static String getZodiacSleepQuality(String lang, String zodiacSign) { }
  static String getZodiacMotivation(String lang, String zodiacSign, String context) { }

  // ══════════════════════════════════════════════════════════════════════════
  // EMOTIONAL GOALS
  // ══════════════════════════════════════════════════════════════════════════

  static Map<String, dynamic> stressedGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> anxiousGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> calmGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> energizedGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> tiredGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> motivatedGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> unmotivatedGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> confidentGoal(String lang, String zodiacSign) { }
  static Map<String, dynamic> uncertainGoal(String lang, String zodiacSign) { }
}
```

---

## 🎯 ESTRATEGIA DE TRADUCCIÓN

### Fase 1: EXTRACCIÓN (30 min)
**Objetivo:** Extraer TODO el texto en inglés a un formato canónico

**Pasos:**
1. Crear tabla maestra en formato Markdown
2. Organizar por categoría → goal → componente
3. Numerar cada texto único (1-245)
4. Incluir variables interpoladas (zodiacSign, hours, etc.)
5. Marcar textos que requieren adaptación cultural

**Deliverable:** `CANONICAL_TEXTS_ENGLISH.md`

### Fase 2: TRADUCCIÓN POR IDIOMA (2 horas × 5 idiomas)
**Objetivo:** Traducir los 245 textos a cada idioma

**Orden de idiomas:**
1. Español (ES) - más fácil para ti
2. Portugués (PT) - similar al español
3. Francés (FR) - idioma romance
4. Alemán (DE) - ya trabajado antes
5. Italiano (IT) - último

**Para cada idioma:**
1. Traducir respetando:
   - Signos de puntuación (¡! ¿? en español)
   - Género gramatical
   - Formalidad/informalidad (tú vs usted)
   - Referencias culturales
2. Mantener variables sin traducir: `$zodiacSign`, `${hours}`, etc.
3. Verificar longitud similar al inglés (UX consistency)

**Deliverable por idioma:**
- `TRANSLATIONS_ES.md`
- `TRANSLATIONS_PT.md`
- `TRANSLATIONS_FR.md`
- `TRANSLATIONS_DE.md`
- `TRANSLATIONS_IT.md`

### Fase 3: CODIFICACIÓN (3 horas)
**Objetivo:** Convertir traducciones a código Dart

**Pasos:**
1. Crear archivo `context_aware_goal_translations.dart`
2. Implementar 25 funciones estáticas
3. Usar switch statements por idioma (como biorhythm_micro_habits_translations.dart)
4. Verificar sintaxis Dart (comillas, escape characters)
5. Probar compilación

**Deliverable:** `context_aware_goal_translations.dart` (completo)

### Fase 4: INTEGRACIÓN (1 hora)
**Objetivo:** Modificar context_aware_goal_generator.dart para usar traducciones

**Cambios en `context_aware_goal_generator.dart`:**

```dart
// ANTES
static List<Map<String, dynamic>> _excellentSleepGoals(String zodiacSign) {
  return [
    {
      'title': 'Harness Your Peak Energy',
      'description': 'You had ${_getZodiacSleepQuality(zodiacSign)} sleep! ...',
      // ... más contenido hardcodeado
    },
  ];
}

// DESPUÉS
static List<Map<String, dynamic>> _excellentSleepGoals(
  String zodiacSign,
  String languageCode,
) {
  return [
    ContextAwareGoalTranslations.excellentSleepGoal1(languageCode, zodiacSign),
    ContextAwareGoalTranslations.excellentSleepGoal2(languageCode, zodiacSign),
  ];
}
```

**Pasos:**
1. Agregar parámetro `languageCode` a TODAS las funciones
2. Reemplazar hardcoded content con llamadas a translations
3. Propagar `languageCode` desde `generateSleepGoals()` y `generateEmotionalGoals()`
4. Verificar compilación

**Deliverable:** `context_aware_goal_generator.dart` (modificado)

### Fase 5: TESTING (1 hora)
**Objetivo:** Verificar que TODO funciona en los 6 idiomas

**Tests:**
1. Hot restart la app
2. Cambiar a cada idioma (EN, ES, PT, FR, DE, IT)
3. Generar nuevas metas en cada idioma
4. Verificar:
   - ✅ NO hay inglés mezclado
   - ✅ Variables se interpolan correctamente
   - ✅ Signos de puntuación correctos
   - ✅ Textos completos (no cortados)

**Deliverable:** `TESTING_REPORT_CONTEXT_AWARE.md`

---

## 📋 CHECKLIST DE EJECUCIÓN

### Pre-trabajo:
- [ ] Leer este plan completo
- [ ] Entender la estructura del archivo original
- [ ] Revisar archivo de referencia: `biorhythm_micro_habits_translations.dart`

### Fase 1 - Extracción:
- [ ] Crear `CANONICAL_TEXTS_ENGLISH.md`
- [ ] Extraer 16 titles
- [ ] Extraer 16 descriptions
- [ ] Extraer 39 microHabits (habit + when + why)
- [ ] Extraer 55 successIndicators
- [ ] Extraer 16 motivationalMessages
- [ ] Extraer 25 zodiac-specific texts
- [ ] Verificar total: 245 textos únicos

### Fase 2 - Traducción:
- [ ] Traducir a Español (245 textos)
- [ ] Traducir a Portugués (245 textos)
- [ ] Traducir a Francés (245 textos)
- [ ] Traducir a Alemán (245 textos)
- [ ] Traducir a Italiano (245 textos)
- [ ] Verificar variables no traducidas
- [ ] Verificar signos de puntuación

### Fase 3 - Codificación:
- [ ] Crear `context_aware_goal_translations.dart`
- [ ] Implementar sleep goals (7 funciones)
- [ ] Implementar zodiac-specific (2 funciones)
- [ ] Implementar emotional goals (9 funciones)
- [ ] Verificar sintaxis Dart
- [ ] Probar compilación

### Fase 4 - Integración:
- [ ] Modificar `generateSleepGoals()` - agregar languageCode
- [ ] Modificar `_excellentSleepGoals()` - usar translations
- [ ] Modificar `_sleepDeprivedGoals()` - usar translations
- [ ] Modificar `_tooMuchSleepGoals()` - usar translations
- [ ] Modificar `_decentSleepGoals()` - usar translations
- [ ] Modificar `_getZodiacSleepQuality()` - usar translations
- [ ] Modificar `_getZodiacMotivation()` - usar translations
- [ ] Modificar `generateEmotionalGoals()` - agregar languageCode
- [ ] Modificar todas las funciones emotional - usar translations
- [ ] Verificar compilación

### Fase 5 - Testing:
- [ ] Hot restart app
- [ ] Test EN (inglés)
- [ ] Test ES (español)
- [ ] Test PT (portugués)
- [ ] Test FR (francés)
- [ ] Test DE (alemán)
- [ ] Test IT (italiano)
- [ ] Verificar NO mixing languages
- [ ] Crear reporte de testing

---

## ⚠️ CONSIDERACIONES ESPECIALES

### Variables dinámicas:
Estos textos tienen interpolación de variables que NO se traducen:

1. **zodiacSign** - Nombre del signo (aries, taurus, etc.)
   - Usar en singular: "Your $zodiacSign wisdom"
   - NO traducir el nombre del signo

2. **hours** - Horas de sueño (número decimal)
   - Usar `.toStringAsFixed(1)` para formato
   - Ejemplo: "You slept ${hours.toStringAsFixed(1)}h"

3. **sleepDebt** - Déficit de sueño (calculado: 7 - hours)
   - Usado en frases: "${sleepDebt.toStringAsFixed(1)}h below optimal"

### Adaptaciones culturales:

1. **Formalidad:**
   - EN: "You" (neutral)
   - ES: "Tú" (informal - app es casual)
   - PT: "Você" (informal Brasil)
   - FR: "Tu" (informal)
   - DE: "Du" (informal)
   - IT: "Tu" (informal)

2. **Referencias científicas:**
   - NO traducir nombres de estudios: "Harvard Sleep Study 2023"
   - NO traducir "NASA" en "NASA study"
   - Mantener porcentajes sin cambio: "40% better focus"

3. **Técnicas específicas:**
   - "4-7-8 Breathing" → Mantener números
   - "5-4-3-2-1 Grounding" → Mantener números
   - "Navy SEALs" → NO traducir (nombre propio)

### Longitud de textos:

Algunas traducciones son naturalmente más largas:
- Alemán tiende a ser +20% más largo
- Francés tiende a ser +10% más largo
- Español similar al inglés
- Verificar que los textos no se corten en UI

---

## 🚀 ORDEN DE EJECUCIÓN

### Día 1 (3 horas):
1. ✅ Fase 1: Extracción (30 min)
2. ✅ Fase 2: Español + Portugués (1.5 horas)
3. ✅ Fase 2: Francés (1 hora)

### Día 2 (4 horas):
4. ✅ Fase 2: Alemán + Italiano (2 horas)
5. ✅ Fase 3: Codificación (2 horas)

### Día 3 (2 horas):
6. ✅ Fase 4: Integración (1 hora)
7. ✅ Fase 5: Testing (1 hora)

**TOTAL:** ~9 horas de trabajo

---

## 📊 MÉTRICAS DE PROGRESO

### Por fase:
- [ ] Fase 1: 0% → 100% (extracción completa)
- [ ] Fase 2: 0% → 100% (5 idiomas × 245 textos)
- [ ] Fase 3: 0% → 100% (18 funciones implementadas)
- [ ] Fase 4: 0% → 100% (integración completa)
- [ ] Fase 5: 0% → 100% (6 idiomas testeados)

### Por idioma (Fase 2):
- [ ] EN: 100% (ya existe - canónico)
- [ ] ES: 0/245 textos
- [ ] PT: 0/245 textos
- [ ] FR: 0/245 textos
- [ ] DE: 0/245 textos
- [ ] IT: 0/245 textos

---

## ✅ CRITERIOS DE ÉXITO

### Fase 1 (Extracción):
✅ Documento con 245 textos únicos numerados
✅ Organizados por categoría
✅ Variables marcadas claramente
✅ Sin duplicados

### Fase 2 (Traducción):
✅ 5 archivos con 245 traducciones cada uno
✅ Variables sin traducir
✅ Signos de puntuación correctos
✅ Longitud razonable

### Fase 3 (Codificación):
✅ Archivo compila sin errores
✅ 18 funciones implementadas
✅ Sintaxis Dart correcta
✅ Switch statements completos (6 idiomas cada uno)

### Fase 4 (Integración):
✅ Archivo modifica compila sin errores
✅ languageCode propagado correctamente
✅ Todas las llamadas actualizadas

### Fase 5 (Testing):
✅ App corre en los 6 idiomas
✅ NO hay texto en inglés mezclado
✅ Variables se interpolan correctamente
✅ UX consistente en todos los idiomas

---

## 🎯 PRÓXIMO PASO INMEDIATO

**COMENZAR FASE 1:** Extraer todos los textos en inglés a formato canónico.

¿Listo para empezar? Dime y comienzo con la Fase 1.

---

**Generado:** 16 Noviembre 2025 - 23:00
**Estimación:** 9 horas total
**Prioridad:** ALTA - Experiencia multiidioma completa
**Estado:** LISTO PARA EJECUTAR
