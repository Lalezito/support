# 🤖 PLAN MULTIAGENTE - Context-Aware Translations (16 Nov 2025)

**Estrategia:** Usar sistema de agentes especializados trabajando en paralelo para traducir y codificar context-aware goals

**Inspiración:** Sistema exitoso usado en traducciones de Cosmic Coach (187 keys × 6 idiomas)

---

## 🎯 ARQUITECTURA MULTIAGENTE

### ORQUESTADOR PRINCIPAL (Master Agent)
**Responsabilidad:** Coordinar todos los agentes y verificar progreso

**Tareas:**
1. Distribuir trabajo entre agentes
2. Monitorear progreso de cada agente
3. Integrar resultados
4. Validar calidad final
5. Crear reportes de progreso

---

## 🤖 AGENTES ESPECIALIZADOS

### AGENTE 1: Extractor Canónico
**Nombre:** `canonical_extractor_agent`
**Lenguaje especializado:** English (nativo del código)
**Duración:** 30 minutos

**Responsabilidades:**
1. Leer `context_aware_goal_generator.dart`
2. Extraer TODOS los textos en inglés
3. Organizarlos por categoría
4. Numerar cada texto (1-245+)
5. Identificar variables dinámicas (zodiacSign, hours, etc.)
6. Marcar textos con interpolación

**Deliverable:**
`CANONICAL_TEXTS_ENGLISH.md` - Tabla maestra con estructura:

```markdown
## SLEEP GOALS - Excellent (7-9h)

### Goal 1: "Harness Your Peak Energy"

| ID | Type | Key | Text | Variables |
|----|------|-----|------|-----------|
| 001 | title | excellentSleep1_title | "Harness Your Peak Energy" | - |
| 002 | description | excellentSleep1_desc | "You had ${zodiacQuality} sleep! Use..." | zodiacQuality |
| 003 | microHabit | excellentSleep1_habit1_text | "Identify your #1 priority task..." | - |
| 004 | microHabit | excellentSleep1_habit1_when | "Right after checking this goal" | - |
| 005 | microHabit | excellentSleep1_habit1_why | "Peak mental clarity happens..." | - |
...
```

**Verificación:**
- [ ] Todos los textos extraídos
- [ ] IDs únicos secuenciales
- [ ] Variables marcadas
- [ ] Organización por categoría

---

### AGENTE 2: Traductor Español
**Nombre:** `spanish_translator_agent`
**Lenguaje especializado:** Español
**Duración:** 1.5 horas

**Responsabilidades:**
1. Leer `CANONICAL_TEXTS_ENGLISH.md`
2. Traducir TODOS los textos al español
3. Aplicar adaptaciones culturales:
   - Usar ¡! signos de exclamación
   - Tono cálido y motivacional
   - Referencias a "energía" y "balance"
4. Mantener variables sin traducir
5. Verificar género gramatical inclusivo

**Sistema de referencia:**
Usar como base las traducciones exitosas de:
- `assets/l10n/app_es.arb` (para estilo)
- `biorhythm_translations.dart` (para vocabulario zodiacal)

**Deliverable:**
`TRANSLATIONS_ES.md` - Misma estructura que canónico

**Ejemplo:**
```markdown
| ID | Type | Key | Text (ES) | Variables |
|----|------|-----|-----------|-----------|
| 001 | title | excellentSleep1_title | "⚡ Aprovecha tu Energía al Máximo" | - |
| 002 | description | excellentSleep1_desc | "¡Tuviste un sueño ${zodiacQuality}! Usa..." | zodiacQuality |
```

**Verificación:**
- [ ] 245+ textos traducidos
- [ ] Signos ¡! correctos
- [ ] Variables preservadas
- [ ] Tono consistente

---

### AGENTE 3: Traductor Portugués
**Nombre:** `portuguese_translator_agent`
**Lenguaje especializado:** Português (Brasil)
**Duración:** 1.5 horas

**Responsabilidades:**
1. Leer `CANONICAL_TEXTS_ENGLISH.md`
2. Traducir al portugués brasileño
3. Aplicar adaptaciones culturales:
   - Tono cálido y optimista
   - Usar "você" informal
   - Referencias a "jornada" y "caminho"
4. Mantener variables sin traducir

**Sistema de referencia:**
- `assets/l10n/app_pt.arb`
- `biorhythm_translations.dart`

**Deliverable:**
`TRANSLATIONS_PT.md`

**Verificación:**
- [ ] 245+ textos traducidos
- [ ] Tono brasileño (não português europeu)
- [ ] Variables preservadas

---

### AGENTE 4: Traductor Francés
**Nombre:** `french_translator_agent`
**Lenguaje especializado:** Français
**Duración:** 1.5 horas

**Responsabilidades:**
1. Leer `CANONICAL_TEXTS_ENGLISH.md`
2. Traducir al francés
3. Aplicar adaptaciones culturales:
   - Elegancia en el lenguaje
   - Referencias a "bien-être" y "équilibre"
   - Mantener tono sofisticado pero accesible
4. Usar "vous" (formal pero accesible)

**Sistema de referencia:**
- `assets/l10n/app_fr.arb`
- `biorhythm_translations.dart`

**Deliverable:**
`TRANSLATIONS_FR.md`

**Verificación:**
- [ ] 245+ textos traducidos
- [ ] Elegancia francesa
- [ ] Variables preservadas

---

### AGENTE 5: Traductor Alemán
**Nombre:** `german_translator_agent`
**Lenguaje especializado:** Deutsch
**Duración:** 1.5 horas

**Responsabilidades:**
1. Leer `CANONICAL_TEXTS_ENGLISH.md`
2. Traducir al alemán
3. Aplicar adaptaciones culturales:
   - Precisión y estructura
   - Mantener referencias científicas
   - Palabras compuestas alemanas apropiadas
4. Usar "du" informal

**Sistema de referencia:**
- `assets/l10n/app_de.arb`
- `biorhythm_translations.dart`

**Deliverable:**
`TRANSLATIONS_DE.md`

**Verificación:**
- [ ] 245+ textos traducidos
- [ ] Precisión alemana
- [ ] Referencias científicas intactas

---

### AGENTE 6: Traductor Italiano
**Nombre:** `italian_translator_agent`
**Lenguaje especializado:** Italiano
**Duración:** 1.5 horas

**Responsabilidades:**
1. Leer `CANONICAL_TEXTS_ENGLISH.md`
2. Traducir al italiano
3. Aplicar adaptaciones culturales:
   - Expresividad italiana
   - Referencias a "bellezza" y "armonia"
   - Tono apasionado pero profesional
4. Usar "tu" informal

**Sistema de referencia:**
- `assets/l10n/app_it.arb`
- `biorhythm_translations.dart`

**Deliverable:**
`TRANSLATIONS_IT.md`

**Verificación:**
- [ ] 245+ textos traducidos
- [ ] Expresividad italiana
- [ ] Variables preservadas

---

### AGENTE 7: Codificador Dart
**Nombre:** `dart_coder_agent`
**Lenguaje especializado:** Dart/Flutter
**Duración:** 2 horas

**Responsabilidades:**
1. Esperar que agentes 2-6 terminen traducciones
2. Leer todos los archivos `TRANSLATIONS_*.md`
3. Crear `context_aware_goal_translations.dart`
4. Implementar 18 funciones estáticas:
   - 7 funciones para sleep goals
   - 2 funciones para zodiac-specific
   - 9 funciones para emotional goals
5. Usar estructura switch/case por idioma
6. Verificar sintaxis Dart
7. Compilar y verificar

**Estructura de código:**
```dart
class ContextAwareGoalTranslations {

  static Map<String, dynamic> excellentSleepGoal1(
    String lang,
    String zodiacSign,
  ) {
    // Get zodiac quality translation
    final zodiacQuality = getZodiacSleepQuality(lang, zodiacSign);

    switch (lang) {
      case 'es':
        return {
          'title': '⚡ Aprovecha tu Energía al Máximo',
          'description': '¡Tuviste un sueño $zodiacQuality! Usa esta ventana...',
          'category': 'wellness',
          'difficulty': HabitDifficulty.medium,
          'microHabits': [
            {
              'habit': 'Identifica tu tarea #1 de prioridad en los próximos 30 minutos',
              'when': 'Justo después de revisar esta meta',
              'why': 'La claridad mental máxima ocurre en las primeras 3 horas...',
              'difficulty': 'easy',
            },
            // ... más microHabits
          ],
          'successIndicators': [
            'Completaste tu tarea más importante',
            'Te sentiste energizado y enfocado',
            // ...
          ],
          'motivationalMessage': getZodiacMotivation(lang, zodiacSign, 'excellent'),
          'scienceBacked': true,
          'source': 'Harvard Sleep Study 2023',
        };

      case 'pt':
        return {
          'title': '⚡ Aproveite sua Energia no Pico',
          'description': 'Você teve um sono $zodiacQuality! Use esta janela...',
          // ... similar structure
        };

      // ... FR, DE, IT

      default: // English
        return {
          'title': '⚡ Harness Your Peak Energy',
          'description': 'You had $zodiacQuality sleep! Use this high-energy...',
          // ... original English
        };
    }
  }

  // ... 17 more functions
}
```

**Deliverable:**
`context_aware_goal_translations.dart` (~2,000 líneas)

**Verificación:**
- [ ] 18 funciones implementadas
- [ ] Compila sin errores
- [ ] Switch statements completos (6 idiomas)
- [ ] Variables interpoladas correctamente

---

### AGENTE 8: Integrador
**Nombre:** `integration_agent`
**Lenguaje especializado:** Dart/Flutter
**Duración:** 1 hora

**Responsabilidades:**
1. Modificar `context_aware_goal_generator.dart`
2. Agregar import:
   ```dart
   import 'context_aware_goal_translations.dart';
   ```
3. Agregar parámetro `languageCode` a todas las funciones:
   - `generateSleepGoals(String zodiacSign, double sleepHours, String languageCode)`
   - `generateEmotionalGoals(String zodiacSign, String emotionalState, String languageCode)`
   - Y todas las funciones privadas
4. Reemplazar contenido hardcodeado con llamadas:
   ```dart
   // ANTES:
   static List<Map<String, dynamic>> _excellentSleepGoals(String zodiacSign) {
     return [
       {
         'title': 'Harness Your Peak Energy',
         // ... hardcoded
       },
     ];
   }

   // DESPUÉS:
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
5. Propagar `languageCode` desde puntos de entrada
6. Verificar compilación

**Deliverable:**
`context_aware_goal_generator.dart` (modificado)

**Verificación:**
- [ ] Import agregado
- [ ] languageCode propagado a todas las funciones
- [ ] Hardcoded content reemplazado
- [ ] Compila sin errores

---

### AGENTE 9: Verificador de Calidad
**Nombre:** `qa_validator_agent`
**Lenguaje especializado:** Testing/QA
**Duración:** 1 hora

**Responsabilidades:**
1. Esperar que todos los agentes terminen
2. Verificar que NO quede texto en inglés hardcodeado
3. Hacer grep de patientes comunes:
   ```bash
   grep -r "'habit':" context_aware_goal_generator.dart
   grep -r "'when':" context_aware_goal_generator.dart
   grep -r "'why':" context_aware_goal_generator.dart
   grep -r "You had" context_aware_goal_generator.dart
   grep -r "You're" context_aware_goal_generator.dart
   ```
4. Verificar que todas las traducciones tienen 6 idiomas
5. Verificar longitud de textos (UX consistency)
6. Crear reporte de hallazgos

**Deliverable:**
`QA_VALIDATION_REPORT.md`

**Verificación:**
- [ ] 0 textos hardcodeados en inglés en generator
- [ ] Todas las funciones tienen 6 idiomas
- [ ] Variables interpoladas correctamente
- [ ] Longitud de textos razonable

---

### AGENTE 10: Tester de Idiomas
**Nombre:** `language_tester_agent`
**Lenguaje especializado:** Flutter Testing
**Duración:** 1 hora

**Responsabilidades:**
1. Hot restart la app
2. Testear cada idioma:
   - Cambiar Settings → Language → [idioma]
   - Ir a Cosmic Coach
   - Presionar "Generar nuevas metas"
   - Verificar TODO en el idioma seleccionado
   - Screenshot de evidencia
3. Verificar interpolación de variables:
   - zodiacSign aparece correctamente
   - hours/sleepDebt con formato correcto
4. Verificar que NO hay mixing de idiomas

**Deliverable:**
`LANGUAGE_TESTING_REPORT.md` + Screenshots

**Verificación:**
- [ ] EN: 100% inglés ✓
- [ ] ES: 100% español ✓
- [ ] PT: 100% portugués ✓
- [ ] FR: 100% francés ✓
- [ ] DE: 100% alemán ✓
- [ ] IT: 100% italiano ✓

---

## 📊 CRONOGRAMA MULTIAGENTE

### FASE 1: EXTRACCIÓN (30 min)
**Agentes activos:** 1
- Agente 1 (Extractor Canónico)

**Duración:** 30 minutos
**Output:** `CANONICAL_TEXTS_ENGLISH.md`

---

### FASE 2: TRADUCCIÓN PARALELA (1.5 horas)
**Agentes activos:** 5 (en PARALELO)
- Agente 2 (Español)
- Agente 3 (Portugués)
- Agente 4 (Francés)
- Agente 5 (Alemán)
- Agente 6 (Italiano)

**Duración:** 1.5 horas (todos en paralelo)
**Output:** 5 archivos `TRANSLATIONS_*.md`

⚡ **GANANCIA DE TIEMPO:**
- Secuencial: 1.5h × 5 = 7.5 horas
- Paralelo: 1.5 horas
- **Ahorro: 6 horas** 🚀

---

### FASE 3: CODIFICACIÓN (2 horas)
**Agentes activos:** 1
- Agente 7 (Codificador Dart)

**Duración:** 2 horas
**Output:** `context_aware_goal_translations.dart`

---

### FASE 4: INTEGRACIÓN (1 hora)
**Agentes activos:** 1
- Agente 8 (Integrador)

**Duración:** 1 hora
**Output:** `context_aware_goal_generator.dart` (modificado)

---

### FASE 5: VALIDACIÓN Y TESTING (1 hora en paralelo)
**Agentes activos:** 2 (en PARALELO)
- Agente 9 (QA Validator)
- Agente 10 (Language Tester)

**Duración:** 1 hora (ambos en paralelo)
**Output:** 2 reportes + screenshots

⚡ **GANANCIA DE TIEMPO:**
- Secuencial: 1h + 1h = 2 horas
- Paralelo: 1 hora
- **Ahorro: 1 hora** 🚀

---

## ⏱️ TIEMPO TOTAL

### Sin multiagentes (secuencial):
- Extracción: 0.5h
- Traducciones: 1.5h × 5 = 7.5h
- Codificación: 2h
- Integración: 1h
- QA + Testing: 2h
- **TOTAL: 13 horas**

### Con multiagentes (paralelo):
- Extracción: 0.5h
- Traducciones: 1.5h (5 agentes en paralelo)
- Codificación: 2h
- Integración: 1h
- QA + Testing: 1h (2 agentes en paralelo)
- **TOTAL: 6 horas** ⚡

### ✅ AHORRO: 7 horas (54% más rápido)

---

## 🎯 COMANDOS DE EJECUCIÓN

### Lanzar TODOS los agentes en paralelo:

```bash
# FASE 2: Lanzar 5 traductores en paralelo
claude-agent run spanish_translator_agent &
claude-agent run portuguese_translator_agent &
claude-agent run french_translator_agent &
claude-agent run german_translator_agent &
claude-agent run italian_translator_agent &
wait

# FASE 5: Lanzar 2 validadores en paralelo
claude-agent run qa_validator_agent &
claude-agent run language_tester_agent &
wait
```

---

## 📋 CHECKLIST DE EJECUCIÓN MULTIAGENTE

### Pre-ejecución:
- [ ] Plan leído y entendido
- [ ] Sistema de agentes verificado
- [ ] Archivos de referencia listos (app_*.arb, biorhythm_translations.dart)

### Fase 1 - Extracción:
- [ ] Agente 1 lanzado
- [ ] `CANONICAL_TEXTS_ENGLISH.md` generado
- [ ] 245+ textos extraídos
- [ ] Variables identificadas

### Fase 2 - Traducción Paralela:
- [ ] 5 agentes lanzados en paralelo
- [ ] `TRANSLATIONS_ES.md` completado (245+ textos)
- [ ] `TRANSLATIONS_PT.md` completado (245+ textos)
- [ ] `TRANSLATIONS_FR.md` completado (245+ textos)
- [ ] `TRANSLATIONS_DE.md` completado (245+ textos)
- [ ] `TRANSLATIONS_IT.md` completado (245+ textos)
- [ ] Todos los agentes terminaron sin errores

### Fase 3 - Codificación:
- [ ] Agente 7 lanzado
- [ ] `context_aware_goal_translations.dart` generado
- [ ] 18 funciones implementadas
- [ ] Compila sin errores

### Fase 4 - Integración:
- [ ] Agente 8 lanzado
- [ ] `context_aware_goal_generator.dart` modificado
- [ ] languageCode propagado
- [ ] Compila sin errores

### Fase 5 - Validación Paralela:
- [ ] 2 agentes lanzados en paralelo
- [ ] QA report generado
- [ ] Testing report generado
- [ ] Screenshots capturados
- [ ] 6 idiomas verificados

---

## 🚀 VENTAJAS DEL SISTEMA MULTIAGENTE

### 1. Velocidad
⚡ **6 horas vs 13 horas** = 54% más rápido

### 2. Especialización
🎯 Cada agente es experto en su idioma/tarea

### 3. Consistencia
✅ Todos los agentes siguen mismas reglas desde archivos de referencia

### 4. Paralelización
🔄 5 traducciones simultáneas en vez de secuenciales

### 5. Validación automática
🤖 QA y testing automáticos

### 6. Reproducibilidad
📋 Proceso documentado y repetible

---

## 📊 ARQUITECTURA DE ARCHIVOS

```
zodiac_app/
├── lib/
│   └── services/
│       └── cosmic_coach/
│           ├── context_aware_goal_generator.dart (MODIFICADO)
│           └── context_aware_goal_translations.dart (NUEVO)
│
├── assets/
│   └── l10n/
│       ├── app_en.arb (REFERENCIA)
│       ├── app_es.arb (REFERENCIA)
│       ├── app_pt.arb (REFERENCIA)
│       ├── app_fr.arb (REFERENCIA)
│       ├── app_de.arb (REFERENCIA)
│       └── app_it.arb (REFERENCIA)
│
└── docs/
    └── translations/
        ├── CANONICAL_TEXTS_ENGLISH.md (NUEVO - Agente 1)
        ├── TRANSLATIONS_ES.md (NUEVO - Agente 2)
        ├── TRANSLATIONS_PT.md (NUEVO - Agente 3)
        ├── TRANSLATIONS_FR.md (NUEVO - Agente 4)
        ├── TRANSLATIONS_DE.md (NUEVO - Agente 5)
        ├── TRANSLATIONS_IT.md (NUEVO - Agente 6)
        ├── QA_VALIDATION_REPORT.md (NUEVO - Agente 9)
        └── LANGUAGE_TESTING_REPORT.md (NUEVO - Agente 10)
```

---

## ✅ CRITERIOS DE ÉXITO

### Agente 1 (Extractor):
✅ 245+ textos extraídos
✅ IDs únicos
✅ Variables marcadas
✅ Organización clara

### Agentes 2-6 (Traductores):
✅ 245+ textos traducidos cada uno
✅ Adaptaciones culturales aplicadas
✅ Variables sin traducir
✅ Tono consistente

### Agente 7 (Codificador):
✅ Archivo compila
✅ 18 funciones completas
✅ 6 idiomas por función
✅ Sintaxis correcta

### Agente 8 (Integrador):
✅ Generator modificado compila
✅ languageCode propagado
✅ Sin hardcoded text

### Agentes 9-10 (Validadores):
✅ 0 textos hardcodeados
✅ 6 idiomas testeados
✅ NO mixing languages
✅ Screenshots de evidencia

---

## 🎯 SIGUIENTE PASO

**¿Listo para ejecutar el plan multiagente?**

Dime y lanzo el **Agente 1 (Extractor Canónico)** para comenzar la Fase 1.

Después de que termine, lanzaré los **5 agentes traductores en paralelo** para la Fase 2.

**Tiempo estimado total: 6 horas** ⚡

---

**Generado:** 16 Noviembre 2025 - 23:30
**Tipo:** Plan de ejecución multiagente
**Ahorro de tiempo:** 54% (7 horas)
**Estado:** LISTO PARA EJECUTAR
