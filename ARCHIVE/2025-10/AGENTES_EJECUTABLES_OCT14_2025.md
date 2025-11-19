# 🤖 AGENTES EJECUTABLES - Sistema Multiagente
## Zodiac App - Limpieza + Integración Traducciones
## Fecha: 14 de Octubre 2025

---

## 📑 TABLA DE CONTENIDOS

- [⚡ QUICK START](#-quick-start-3-segundos) - **Empieza aquí** (3 segundos)
- [🎯 RESUMEN EJECUTIVO](#-resumen-ejecutivo) - ¿Qué hace esto?
- [📋 INSTRUCCIONES DE USO](#-instrucciones-de-uso---super-simple) - Cómo ejecutar
- [🤖 AGENTE 1](#-agente-1-duplicate-model-resolver) - Unificar modelos Goal
- [🤖 AGENTE 2](#-agente-2-translations-integration-specialist) - Integrar traducciones
- [🤖 AGENTE 3](#-agente-3-documentation-consolidator) - Organizar docs
- [🤖 AGENTE 4](#-agente-4-code-duplication-auditor) - Auditar duplicados
- [✅ CHECKLIST](#-checklist-de-completado) - Verificar resultados

---

## 🎯 RESUMEN EJECUTIVO

**¿Qué hace esto?**
Lanza 4 agentes especializados en paralelo para:

1. 🗂️ **Unificar modelos Goal duplicados** (90 min)
2. 🌍 **Integrar 4 traducciones** FR/DE/IT/PT en la app (4 horas)
3. 📚 **Organizar 116 archivos .md** del root (90 min)
4. 🔍 **Auditar código duplicado** (60 min)

**Tiempo total**: 4-6 horas (en paralelo, no secuencial)
**Beneficio**: App lista con 5 idiomas + código limpio + documentación organizada

---

## ⚡ QUICK START (3 segundos)

**Dile a Claude**:
```
Ejecuta los 4 agentes del archivo AGENTES_EJECUTABLES_OCT14_2025.md en paralelo
```

¡Ya está! Claude hará todo automáticamente. 🚀

---

## ⚠️ ADVERTENCIAS IMPORTANTES

**ANTES de ejecutar**:
1. ✅ Haz backup: `git commit -am "Pre-agents backup"`
2. ✅ Verifica que tienes espacio (generará ~50 MB de reportes)
3. ✅ Los agentes tardan 4-6 horas - déjalos correr sin interrumpir
4. ⚠️ **AGENTE 1 eliminará archivos** (goal.dart duplicado) - revisa antes

**Durante la ejecución**:
- ✅ Puedes cerrar la terminal (corren en background)
- ✅ Puedes hacer otras cosas
- ❌ NO interrumpas manualmente (`Ctrl+C` puede dejar cambios a medias)

**Después de ejecutar**:
- ✅ Revisa los 4 reportes generados
- ✅ Ejecuta `flutter analyze` para verificar compilación
- ✅ Haz commit: `git add . && git commit -m "Apply agents improvements"`

---

## 📋 INSTRUCCIONES DE USO - SUPER SIMPLE

### 🚀 Opción A: Ejecución Automática (RECOMENDADO) ⭐

**Solo dile a Claude**:
```
Ejecuta los 4 agentes del archivo AGENTES_EJECUTABLES_OCT14_2025.md en paralelo
```

Claude leerá este archivo automáticamente y lanzará los 4 agentes.

**Tiempo**: 4-6 horas en paralelo (no secuencial)
**Reportes generados**: 4 archivos .md con análisis completo

---

### 📋 Opción B: Ejecución Manual (copiar/pegar)

1. **Selecciona** desde la línea 32 (`Eres un especialista...`) hasta la línea 693 (último cierre)
2. **Copia** todo ese bloque completo
3. **En un mensaje nuevo a Claude**, pega:
   ```
   Ejecuta estos 4 agentes EN PARALELO usando Task tool (general-purpose):

   [pegar el texto copiado aquí]
   ```
4. **Envía y espera** los 4 reportes (4-6 horas)
5. **Revisa** GOAL_MODEL_UNIFICATION_REPORT.md, TRANSLATIONS_INTEGRATION_COMPLETE.md, etc.

---

## 🤖 AGENTE 1: DUPLICATE MODEL RESOLVER

### Prompt para Task tool:

```
Eres un especialista en resolución de código duplicado en Flutter.

**CONTEXTO**:
Se encontraron 2 modelos Goal duplicados en el proyecto Zodiac App:
- lib/models/goal.dart (213 líneas) - Creado Oct 13, NO se usa
- lib/models/goal/goal.dart (285 líneas) - Existente desde Oct 8, 10 imports activos

**TU MISIÓN** (90 minutos):

1. **ANALIZAR AMBOS MODELOS** (20 min)
   - Lee ambos archivos completos
   - Compara campos, métodos, funcionalidad
   - Identifica cuál es más completo
   - Busca qué screens los usan: grep -r "import.*goal" lib/features

2. **DECIDIR ESTRATEGIA** (10 min)
   Evalúa:
   - ¿Cuál tiene más funcionalidad? (goal/goal.dart tiene MainGoal, WeeklyFocus, Enums)
   - ¿Cuál usan las screens? (goal/goal.dart tiene 10 imports)
   - **RECOMENDACIÓN**: Eliminar lib/models/goal.dart (el nuevo), mantener goal/goal.dart

3. **IMPLEMENTAR UNIFICACIÓN** (40 min)
   ```bash
   # Verificar imports antes
   grep -r "import.*models/goal\.dart" lib --include="*.dart"
   grep -r "import.*models/goal/goal\.dart" lib --include="*.dart"

   # Si goal.dart NO tiene imports activos:
   cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
   git rm lib/models/goal.dart
   git rm lib/models/goal_check_in.dart # También revisar este

   # Verificar que goal_check_in.dart se usa
   grep -r "import.*goal_check_in" lib
   ```

4. **VERIFICAR COMPILACIÓN** (15 min)
   ```bash
   flutter clean
   flutter pub get
   flutter analyze
   # Verificar 0 errores en goal/goal.dart imports
   ```

5. **CREAR REPORTE** (5 min)
   Archivo: `GOAL_MODEL_UNIFICATION_REPORT.md`
   ```markdown
   # Goal Model Unification Report

   ## Decisión Tomada
   - [x] Eliminado: lib/models/goal.dart (no usado)
   - [x] Mantenido: lib/models/goal/goal.dart (10 imports activos)

   ## Archivos Eliminados
   - lib/models/goal.dart (213 líneas)
   - lib/models/goal_check_in.dart (172 líneas) [si no se usa]

   ## Verificación
   - Imports activos: 10 (todos a goal/goal.dart)
   - Compilación: ✅ Sin errores
   - Screens funcionando: ✅

   ## Archivos Impactados
   [lista de screens que usan Goal model]
   ```

**IMPORTANTE**:
- NO migres código entre archivos (demasiado riesgo)
- Elimina el archivo NO usado
- Verifica compilación ANTES y DESPUÉS
- Si hay dudas, reporta sin eliminar

**ENTREGABLES**:
1. ✅ Solo 1 modelo Goal en el proyecto
2. ✅ App compila sin errores
3. ✅ Reporte: GOAL_MODEL_UNIFICATION_REPORT.md
```

---

## 🤖 AGENTE 2: TRANSLATIONS INTEGRATION SPECIALIST

### Prompt para Task tool:

```
Eres un especialista en internacionalización (i18n) de Flutter.

**CONTEXTO**:
Hay 4 traducciones completas (356 strings) listas pero NO integradas:
- COSMIC_GOALS_FRENCH_TRANSLATIONS.json (89 strings)
- COSMIC_GOALS_GERMAN_TRANSLATIONS.json (89 strings)
- COSMIC_GOALS_ITALIAN_TRANSLATIONS.json (89 strings)
- COSMIC_GOALS_PORTUGUESE_TRANSLATIONS.json (89 strings)

**TU MISIÓN** (4 horas):

**FASE 1: SETUP LOCALIZATION** (30 min)

1. Verifica pubspec.yaml:
   ```bash
   cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
   grep -A 5 "flutter_localizations" pubspec.yaml
   ```

2. Si NO existe, agregar:
   ```yaml
   dependencies:
     flutter_localizations:
       sdk: flutter
     intl: any

   flutter:
     generate: true
   ```

3. Crear l10n.yaml:
   ```yaml
   arb-dir: lib/l10n
   template-arb-file: app_en.arb
   output-localization-file: app_localizations.dart
   ```

4. Crear directorio:
   ```bash
   mkdir -p lib/l10n
   ```

**FASE 2: CONVERTIR JSON → ARB** (90 min)

Para cada idioma, crear archivo .arb en lib/l10n/:

**app_en.arb** (BASE - extraer de código actual):
```bash
# Buscar strings actuales en smart_goal_recommender.dart
grep -A 1 "fitness_Aries" lib/services/smart_goal_recommender.dart
```

Estructura:
```json
{
  "@@locale": "en",
  "fitness_Aries": "🏃 Aries: Your natural energy peaks in the morning. Use that Martian fire!",
  "@fitness_Aries": {
    "description": "Fitness tip for Aries zodiac sign"
  }
}
```

**app_fr.arb** (desde COSMIC_GOALS_FRENCH_TRANSLATIONS.json):
```python
# Script de conversión
import json

with open('../../COSMIC_GOALS_FRENCH_TRANSLATIONS.json') as f:
    data = json.load(f)

arb = {"@@locale": "fr"}
for key, value in data['1_tips_database']['strings'].items():
    arb[key] = value
    arb[f"@{key}"] = {"description": f"Tip for {key}"}

# Repetir para categories 2 y 3
```

**Hacer lo mismo para DE, IT, PT**

**FASE 3: GENERAR CLASES** (15 min)
```bash
flutter pub get
flutter gen-l10n
# Esto crea: .dart_tool/flutter_gen/gen_l10n/app_localizations.dart
```

**FASE 4: HELPER CLASSES** (60 min)

Crear `lib/l10n/tips_localizer.dart`:
```dart
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class TipsLocalizer {
  static String getTip(BuildContext context, {
    required String category,
    required String zodiacSign,
  }) {
    final l10n = AppLocalizations.of(context)!;
    final key = '${category}_${zodiacSign}';

    // Map dinámico basado en key
    switch (key) {
      case 'fitness_Aries':
        return l10n.fitness_Aries;
      case 'mindfulness_Aries':
        return l10n.mindfulness_Aries;
      // ... mapear todos los 89 tips
      default:
        return l10n.fitness_Aries; // fallback
    }
  }

  static String getGenericTip(BuildContext context, String category) {
    final l10n = AppLocalizations.of(context)!;

    switch (category) {
      case 'fitness':
        return l10n.fitness;
      case 'mindfulness':
        return l10n.mindfulness;
      // ... resto
      default:
        return '';
    }
  }
}
```

Crear `lib/l10n/celebration_localizer.dart`:
```dart
class CelebrationLocalizer {
  static List<String> getCelebrations(BuildContext context, String category) {
    final l10n = AppLocalizations.of(context)!;

    switch (category) {
      case 'fitness':
        return [
          l10n.fitness_celebration_1,
          l10n.fitness_celebration_2,
          l10n.fitness_celebration_3,
        ];
      // ... resto de categorías (39 total)
    }
  }
}
```

**FASE 5: ACTUALIZAR SCREENS** (45 min)

1. **smart_goal_recommender.dart**:
   ```dart
   // ANTES:
   final tip = "🏃 Aries: Your natural energy...";

   // DESPUÉS:
   import '../l10n/tips_localizer.dart';
   final tip = TipsLocalizer.getTip(
     context,
     category: 'fitness',
     zodiacSign: 'Aries',
   );
   ```

2. **goal_completion_celebration.dart**:
   ```dart
   import '../l10n/celebration_localizer.dart';
   final messages = CelebrationLocalizer.getCelebrations(context, 'fitness');
   ```

3. **cosmic_coach_screen.dart**:
   ```dart
   // UI strings
   final l10n = AppLocalizations.of(context)!;
   Text(l10n.goals_empty_state)
   Text(l10n.smart_goals_generated)
   ```

**FASE 6: CONFIGURAR APP** (15 min)

En `main.dart`:
```dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

MaterialApp(
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
  locale: _userLocale, // Desde settings
  ...
)
```

**FASE 7: TESTING** (30 min)
```bash
# Compilar
flutter clean
flutter pub get
flutter gen-l10n
flutter build apk --debug

# Probar cada idioma manualmente
# Verificar que emojis renderizan
# Validar que placeholders {userSign} se reemplazan
```

**ENTREGABLES**:
1. ✅ 5 archivos .arb (en, fr, de, it, pt)
2. ✅ 2 helper classes (TipsLocalizer, CelebrationLocalizer)
3. ✅ 3 screens actualizadas
4. ✅ App soporta 5 idiomas
5. ✅ Reporte: TRANSLATIONS_INTEGRATION_COMPLETE.md

**REPORTE DEBE INCLUIR**:
- Screenshots de cada idioma
- Lista de strings integradas (89 × 4 = 356)
- Instrucciones para agregar nuevo idioma
- Known issues (si los hay)
```

---

## 🤖 AGENTE 3: DOCUMENTATION CONSOLIDATOR

### Prompt para Task tool:

```
Eres un especialista en organización de documentación técnica.

**CONTEXTO**:
El directorio root tiene 116 archivos .md, muchos duplicados o obsoletos.

**TU MISIÓN** (90 min):

**FASE 1: ANÁLISIS** (15 min)
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia

# Contar archivos
ls -1 *.md | wc -l

# Identificar categorías
ls -1 *.md | grep -i "MEGA" | wc -l
ls -1 *.md | grep -i "PLAN" | wc -l
ls -1 *.md | grep -i "REPORT" | wc -l
ls -1 *.md | grep -i "SUMMARY" | wc -l

# Encontrar más grandes
du -sh *.md | sort -rh | head -20
```

**FASE 2: CREAR ESTRUCTURA** (10 min)
```bash
mkdir -p .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION
mkdir -p .claude/ARCHIVE/2025_OCTOBER
mkdir -p .claude/TRANSLATIONS
mkdir -p .claude/PLANS/COMPLETED
```

**FASE 3: CATEGORIZAR Y MOVER** (45 min)

**MANTENER EN ROOT** (solo estos):
```bash
# Lista de archivos que DEBEN quedarse:
- README.md (si existe)
- CHANGELOG.md (si existe)
- QUICK_START_SIGUIENTE_SESION.md
- PLAN_MULTIAGENTE_REALISTA_OCT14_2025.md (el actual)
- AGENTES_EJECUTABLES_OCT14_2025.md (el actual)
```

**MOVER A COMPLETED_IMPLEMENTATIONS**:
```bash
mv MEGA_EXECUTION_*.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv *_IMPLEMENTATION_COMPLETE.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv *_COMPLETIONS_REPORT.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv INTEGRATION_MASTER_SUMMARY.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv BACKEND_RESILIENCE_REPORT.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv PRICING_*.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
mv GOAL_PLANNER_*.md .claude/12_COMPLETED_IMPLEMENTATIONS/2025_OCT_13-14_MEGA_EXECUTION/
```

**MOVER A TRANSLATIONS**:
```bash
mv COSMIC_GOALS_*_TRANSLATIONS.json .claude/TRANSLATIONS/
mv *TRANSLATION*.md .claude/TRANSLATIONS/
mv *TRADUZ*.md .claude/TRANSLATIONS/
mv CONSEGNA_*.md .claude/TRANSLATIONS/
mv RELATORIO_*.md .claude/TRANSLATIONS/
```

**MOVER A ARCHIVE** (obsoletos):
```bash
mv MASTER_PLAN_COMPLETE_OCT_2025.md .claude/ARCHIVE/2025_OCTOBER/
mv ANALISIS_COMPLETO_*.md .claude/ARCHIVE/2025_OCTOBER/
mv CLEANUP_*.md .claude/ARCHIVE/2025_OCTOBER/
mv PHASE*_COMPLETE*.md .claude/ARCHIVE/2025_OCTOBER/
mv *_OLD.md .claude/ARCHIVE/2025_OCTOBER/
mv *_BACKUP.md .claude/ARCHIVE/2025_OCTOBER/
```

**FASE 4: CREAR INDEX MAESTRO** (15 min)

Crear `.claude/12_COMPLETED_IMPLEMENTATIONS/INDEX.md`:
```markdown
# 📚 Completed Implementations - Index

## Mega Execution (Oct 13-14, 2025)

### Main Reports
- [Mega Execution Final Report](2025_OCT_13-14_MEGA_EXECUTION/MEGA_EXECUTION_FINAL_REPORT.md)
- [Integration Master Summary](2025_OCT_13-14_MEGA_EXECUTION/INTEGRATION_MASTER_SUMMARY.md)

### By Category

#### Goal Planner
- [Implementation Complete](2025_OCT_13-14_MEGA_EXECUTION/GOAL_PLANNER_IMPLEMENTATION_COMPLETE.md)
- [Models Report](2025_OCT_13-14_MEGA_EXECUTION/GOAL_PLANNER_MODELS_REPORT.md)
- [Service Report](2025_OCT_13-14_MEGA_EXECUTION/GOAL_PLANNER_SERVICE_REPORT.md)

#### Translations (4 languages)
- French: [Report](../../TRANSLATIONS/FRENCH_TRANSLATION_COMPLETE.md) | [JSON](../../TRANSLATIONS/COSMIC_GOALS_FRENCH_TRANSLATIONS.json)
- German: [JSON](../../TRANSLATIONS/COSMIC_GOALS_GERMAN_TRANSLATIONS.json)
- Italian: [Report](../../TRANSLATIONS/TRADUZIONE_ITALIANA_REPORT.md) | [JSON](../../TRANSLATIONS/COSMIC_GOALS_ITALIAN_TRANSLATIONS.json)
- Portuguese: [Report](../../TRANSLATIONS/RELATORIO_TRADUCAO_PORTUGUESA_COSMIC_GOALS.md) | [JSON](../../TRANSLATIONS/COSMIC_GOALS_PORTUGUESE_TRANSLATIONS.json)

#### Backend & Services
- [Backend Resilience](2025_OCT_13-14_MEGA_EXECUTION/BACKEND_RESILIENCE_REPORT.md)
- [Pricing Provider](2025_OCT_13-14_MEGA_EXECUTION/PRICING_PROVIDER_REPORT.md)
- [User ID Fix](2025_OCT_13-14_MEGA_EXECUTION/USER_ID_FIX_REPORT.md)

#### Quality & Cleanup
- [Print Cleanup](2025_OCT_13-14_MEGA_EXECUTION/PRINT_CLEANUP_REPORT.md)
- [TODOs Resolution](2025_OCT_13-14_MEGA_EXECUTION/TODOS_RESOLUTION_REPORT.md)

### Archived Reports
See: [Archive](../ARCHIVE/2025_OCTOBER/)
```

**FASE 5: ACTUALIZAR README ROOT** (5 min)

Crear/actualizar `/README.md`:
```markdown
# 🌟 Zodiac Life Coach

AI-powered astrology coaching app with personalized goals and insights.

## 📚 Documentation

- **Implementation Reports**: [.claude/12_COMPLETED_IMPLEMENTATIONS/INDEX.md](.claude/12_COMPLETED_IMPLEMENTATIONS/INDEX.md)
- **Quick Start**: [QUICK_START_SIGUIENTE_SESION.md](QUICK_START_SIGUIENTE_SESION.md)
- **Current Plan**: [PLAN_MULTIAGENTE_REALISTA_OCT14_2025.md](PLAN_MULTIAGENTE_REALISTA_OCT14_2025.md)

## 🚀 Getting Started

\`\`\`bash
cd zodiac_app
flutter pub get
flutter run
\`\`\`

## 🌍 Supported Languages

- English (EN)
- French (FR) - Integrated ✅
- German (DE) - Integrated ✅
- Italian (IT) - Integrated ✅
- Portuguese (PT) - Integrated ✅

## 📊 Production Readiness

**Score**: 99/100

---

For detailed history, see [Mega Execution Report](.claude/12_COMPLETED_IMPLEMENTATIONS/INDEX.md).
```

**ENTREGABLES**:
1. ✅ Root con <10 archivos .md
2. ✅ Documentación organizada en .claude/
3. ✅ INDEX.md maestro creado
4. ✅ README.md actualizado
5. ✅ Reporte: DOCUMENTATION_CONSOLIDATION_REPORT.md

**REPORTE DEBE INCLUIR**:
- Antes: 116 archivos
- Después: X archivos en root
- Archivos movidos por categoría
- Estructura final de directorios
- Rutas de acceso rápido
```

---

## 🤖 AGENTE 4: CODE DUPLICATION AUDITOR

### Prompt para Task tool:

```
Eres un especialista en análisis de código duplicado.

**CONTEXTO**:
Necesitamos identificar (NO arreglar) código duplicado en el proyecto Zodiac App.

**TU MISIÓN** (60 min):

**FASE 1: ANALIZAR SERVICES** (25 min)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# 1. Buscar métodos duplicados de error handling
grep -r "try {" lib/services/*.dart | wc -l
grep -r "catch (e)" lib/services/*.dart | wc -l
grep -r "AppLogger.error" lib/services/*.dart | wc -l

# 2. Buscar patrones de API calls
grep -r "http.get" lib/services/*.dart
grep -r "http.post" lib/services/*.dart
grep -r "dio.get" lib/services/*.dart

# 3. Buscar singleton patterns
grep -r "static final.*instance" lib/services/*.dart

# 4. Analizar cada archivo grande
find lib/services -name "*.dart" -exec wc -l {} \; | sort -rn | head -10
```

**FASE 2: ANALIZAR SCREENS** (25 min)

```bash
# 1. Buscar loading states duplicados
grep -r "CircularProgressIndicator" lib/features --include="*.dart" | wc -l
grep -r "isLoading" lib/features --include="*.dart" | wc -l

# 2. Buscar error widgets
grep -r "Error.*widget" lib/features --include="*.dart"
grep -r "ErrorScreen" lib/features --include="*.dart"
grep -r "Something went wrong" lib/features --include="*.dart"

# 3. Buscar AppBar duplicados
grep -r "AppBar(" lib/features --include="*.dart" | wc -l

# 4. Buscar ScaffoldState duplicados
grep -r "Scaffold(" lib/features --include="*.dart" | wc -l
```

**FASE 3: GENERAR REPORTE** (10 min)

Crear `CODIGO_DUPLICADO_AUDIT.md`:

```markdown
# Code Duplication Audit Report
**Date**: Oct 14, 2025
**Scope**: lib/services + lib/features

---

## 🔴 CRITICAL Duplications

### 1. Error Handling Pattern
**Occurrences**: [X encontrados]
**Location**: Multiple services
**Pattern**:
\`\`\`dart
try {
  // logic
} catch (e) {
  AppLogger.error('Error: $e');
  rethrow;
}
\`\`\`

**Recommendation**:
Create `lib/utils/error_handler.dart`:
\`\`\`dart
class ErrorHandler {
  static Future<T> handle<T>(Future<T> Function() operation) async {
    try {
      return await operation();
    } catch (e) {
      AppLogger.error('Error: $e');
      rethrow;
    }
  }
}
\`\`\`

---

### 2. Loading Indicator Widget
**Occurrences**: [X screens]
**Locations**: [lista de screens]

**Pattern**:
\`\`\`dart
if (isLoading) {
  return Center(
    child: CircularProgressIndicator(),
  );
}
\`\`\`

**Recommendation**:
Create `lib/widgets/common/loading_widget.dart`

---

## 🟡 MODERATE Duplications

### 3. API Client Configuration
**Occurrences**: [X services]
**Services**: [lista]

**Recommendation**:
Centralize in `lib/services/base_api_client.dart`

---

## 🟢 MINOR Duplications

### 4. AppBar Styles
**Occurrences**: [X screens]

**Recommendation**:
Create theme extension for AppBar

---

## 📊 Statistics

| Category | Duplications Found | Priority |
|----------|-------------------|----------|
| Error Handling | X | 🔴 High |
| Loading States | X | 🔴 High |
| Error Widgets | X | 🟡 Medium |
| API Clients | X | 🟡 Medium |
| AppBar Styles | X | 🟢 Low |

---

## 🎯 Recommended Refactorings

### Priority 1 (Week 1)
1. [ ] Create ErrorHandler utility
2. [ ] Create LoadingWidget component
3. [ ] Create ErrorWidget component

### Priority 2 (Week 2)
4. [ ] Centralize API client
5. [ ] Create BaseService class

### Priority 3 (Week 3)
6. [ ] Standardize AppBar styles
7. [ ] Extract common widgets

---

## 💡 Implementation Guide

For Priority 1 refactorings, see: `REFACTORING_GUIDE.md` (to be created)
```

**IMPORTANTE**:
- Solo REPORTA, NO hagas cambios
- Cuenta ocurrencias exactas
- Prioriza por impacto
- Sugiere soluciones concretas

**ENTREGABLES**:
1. ✅ Reporte: CODIGO_DUPLICADO_AUDIT.md
2. ✅ Lista priorizada de refactorings
3. ✅ Ejemplos de código duplicado
4. ✅ Recomendaciones de implementación
```

---

## 🚀 EJECUCIÓN EN PARALELO

### ⚡ Forma MÁS FÁCIL (recomendada):

**Solo di a Claude**:
```
Ejecuta los 4 agentes del archivo AGENTES_EJECUTABLES_OCT14_2025.md en paralelo
```

Claude hará todo automáticamente. ✨

---

### 📝 Forma Manual (si prefieres tener control):

**Copia SOLO los prompts de los 4 agentes** (líneas 32-693) y pega en Claude:

```
Ejecuta estos 4 agentes EN PARALELO usando Task tool (general-purpose):

[Aquí pegar los 4 prompts completos desde "Eres un especialista..." hasta el final de cada agente]
```

**Nota**: No copies las instrucciones, solo los prompts de los agentes

---

## 📊 TRACKING DE PROGRESO

Mientras los agentes trabajan, puedes:

```bash
# Ver archivos siendo creados
watch -n 5 'ls -lht | head -20'

# Monitorear reportes
watch -n 10 'ls -1 *REPORT*.md | tail -5'

# Ver cambios en git
watch -n 5 'git status --short'
```

---

## ✅ CHECKLIST DE COMPLETADO

### 📄 Reportes Generados (verificar que existen):

- [ ] `GOAL_MODEL_UNIFICATION_REPORT.md` - Agente 1
- [ ] `TRANSLATIONS_INTEGRATION_COMPLETE.md` - Agente 2
- [ ] `DOCUMENTATION_CONSOLIDATION_REPORT.md` - Agente 3
- [ ] `CODIGO_DUPLICADO_AUDIT.md` - Agente 4

### 🔍 Cambios en Código (verificar):

- [ ] Solo 1 modelo Goal existe (`lib/models/goal/goal.dart`)
- [ ] 5 archivos .arb creados en `zodiac_app/lib/l10n/`
- [ ] Root limpio (<15 archivos .md)
- [ ] Documentación en `.claude/` folders

### 🧪 Testing (ejecutar):

- [ ] App compila: `cd zodiac_app && flutter build apk --debug`
- [ ] Análisis pasa: `flutter analyze`
- [ ] Traducciones visibles en app (probar manualmente cambiar idioma)

---

## 🎯 RESULTADO ESPERADO

**Tiempo total**: 4-6 horas (en paralelo)

**Archivos generados**:
1. GOAL_MODEL_UNIFICATION_REPORT.md
2. TRANSLATIONS_INTEGRATION_COMPLETE.md
3. DOCUMENTATION_CONSOLIDATION_REPORT.md
4. CODIGO_DUPLICADO_AUDIT.md

**Estado final**:
- ✅ 1 modelo Goal (unificado)
- ✅ 5 idiomas soportados (EN/FR/DE/IT/PT)
- ✅ Documentación organizada
- ✅ Código duplicado auditado

---

**Creado**: 14 de Octubre 2025
**Versión**: 1.0 - EJECUTABLE
**Agentes**: 4 Task agents (general-purpose)
**Status**: ✅ LISTO PARA COPIAR Y PEGAR
