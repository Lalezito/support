# Plan Multi-Agente: Mejoras Sistema de Reviews

## Resumen Ejecutivo

**Estado Actual:** Sistema de reviews 60% implementado, 5 triggers integrados, 2 triggers sin integrar, 3 métodos de disqualificación sin conectar.

**Objetivo:** Completar 100% de integración usando 4 agentes en paralelo.

---

## Arquitectura Multi-Agente

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORQUESTADOR PRINCIPAL                        │
│                  (Claude Code - Coordinador)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   AGENTE 1    │    │   AGENTE 2    │    │   AGENTE 3    │
│  AI Rating    │    │ Disqualifiers │    │ Localization  │
│   + 30-Day    │    │  Integration  │    │  + Analytics  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ • Chat rating │    │ • recordCrash │    │ • i18n texts  │
│ • triggerAI   │    │ • recordSupp  │    │ • ARB files   │
│ • trigger30D  │    │ • recordCanc  │    │ • Analytics   │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## AGENTE 1: AI Rating + 30-Day User
**Prioridad:** 🔴 CRÍTICA | **Tiempo estimado:** 45 min

### Tareas:
1. **Crear widget de rating para mensajes del AI Coach**
   - Archivo: `lib/widgets/chat/ai_response_rating_widget.dart` (NUEVO)
   - 5 estrellas + thumbs up/down
   - Callback `onRated(int rating)`

2. **Integrar rating en chat bubbles**
   - Archivo: `lib/screens/cosmic_coach_chat_screen.dart`
   - Mostrar widget debajo de respuestas del AI
   - Al dar 5 estrellas → trigger review

3. **Integrar trigger 30-Day Active User**
   - Archivo: `lib/screens/home_screen.dart`
   - Verificar en `_loadHomeData()` después del streak check
   - Condición: `daysActive >= 30 && sessionCount >= 15`

### Código de referencia:

```dart
// ai_response_rating_widget.dart
class AiResponseRatingWidget extends StatefulWidget {
  final Function(int) onRated;
  final String messageId;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Was this helpful?'),
        ...List.generate(5, (i) => IconButton(
          icon: Icon(i < _rating ? Icons.star : Icons.star_border),
          onPressed: () => _handleRating(i + 1),
        )),
      ],
    );
  }

  void _handleRating(int rating) {
    widget.onRated(rating);
    if (rating == 5) {
      ReviewPromptService().triggerReviewPromptFlow(
        context: context,
        triggerId: ReviewPromptService.triggerAiResponseRated,
      );
    }
  }
}
```

```dart
// home_screen.dart - agregar después de streak check
// ⭐ REVIEW PROMPT: Check for 30-day active user milestone
unawaited(ReviewPromptService().checkAndTrigger30DayMilestone(context));
```

---

## AGENTE 2: Disqualifiers Integration
**Prioridad:** 🟠 ALTA | **Tiempo estimado:** 30 min

### Tareas:
1. **Integrar recordCrash() en error handlers**
   - Archivo: `lib/main.dart`
   - Ubicación: `FlutterError.onError` y `PlatformDispatcher.instance.onError`

2. **Integrar recordSupportContact() en settings**
   - Archivo: `lib/screens/settings_screen.dart`
   - Ubicación: Botón "Contact Support" / "Feedback"

3. **Integrar recordPremiumCancellation() en RevenueCat**
   - Archivo: `lib/services/revenuecat_service.dart`
   - Ubicación: Detección de cancelación de compra

### Código de referencia:

```dart
// main.dart - En FlutterError.onError
FlutterError.onError = (errorDetails) {
  FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
  // ✅ NEW: Disqualify from review prompts
  unawaited(ReviewPromptService().recordCrash());
};
```

```dart
// settings_screen.dart - En onPressed de Contact Support
onPressed: () async {
  await _launchSupportEmail();
  await ReviewPromptService().recordSupportContact();
}
```

```dart
// revenuecat_service.dart - En detección de cancelación
if (errorStr.contains('purchasecancellederror') ||
    errorStr.contains('user cancel')) {
  unawaited(ReviewPromptService().recordPremiumCancellation());
}
```

---

## AGENTE 3: Localization + Analytics
**Prioridad:** 🟡 MEDIA | **Tiempo estimado:** 40 min

### Tareas:
1. **Localizar textos del rating dialog**
   - Archivo: `lib/services/review_prompt_service.dart`
   - Método: `_getRatingText()` líneas 591-606
   - Usar: `AppLocalizations.of(context)`

2. **Localizar categorías de feedback**
   - Archivo: `lib/services/review_prompt_service.dart`
   - Variable: `_issueCategories` líneas 630-637
   - Usar keys existentes en ARB files

3. **Agregar constantes de analytics**
   - Archivo: `lib/utils/analytics_events.dart`
   - Agregar eventos de review system

4. **Actualizar review_prompt_service para usar constantes**
   - Reemplazar strings hardcodeados por `AnalyticsEvents.xxx`

### Código de referencia:

```dart
// analytics_events.dart - AGREGAR
// Review System Events
static const String reviewPromptShown = 'review_prompt_shown';
static const String reviewPromptDismissed = 'review_prompt_dismissed';
static const String inAppRatingGiven = 'in_app_rating_given';
static const String nativeReviewShown = 'native_review_shown';
static const String reviewFeedbackSubmitted = 'review_feedback_submitted';
static const String aiResponseRated = 'ai_response_rated';
static const String thirtyDayMilestone = 'thirty_day_milestone';

// Parameters
static const String paramRating = 'rating';
static const String paramTriggerId = 'trigger_id';
static const String paramFeedbackLength = 'feedback_length';
static const String paramIssueCategories = 'issue_categories';
```

```dart
// review_prompt_service.dart - _getRatingText() LOCALIZADO
String _getRatingText(BuildContext context, int rating) {
  final l10n = AppLocalizations.of(context);
  switch (rating) {
    case 1: return l10n?.reviewRatingVeryPoor ?? 'Very Poor';
    case 2: return l10n?.reviewRatingPoor ?? 'Poor';
    case 3: return l10n?.reviewRatingOkay ?? 'Okay';
    case 4: return l10n?.reviewRatingGood ?? 'Good';
    case 5: return l10n?.reviewRatingExcellent ?? 'Excellent!';
    default: return '';
  }
}
```

---

## Ejecución Paralela

### Comando de Ejecución:
```
Usuario: "dale con los 3 agentes"
```

### Diagrama de Tiempos:
```
Tiempo    0min    15min   30min   45min   60min
          │       │       │       │       │
AGENTE 1  ████████████████████████████████│
          │ Widget │ Chat  │ 30-Day│ Test │
          │       │       │       │       │
AGENTE 2  ████████████████████│           │
          │ Crash │Support│RevCat│        │
          │       │       │       │       │
AGENTE 3  ████████████████████████████│   │
          │ i18n  │Categs │Analytc│ ARB  │
          │       │       │       │       │
```

---

## Verificación Post-Implementación

### Checklist de Completitud:
```
□ triggerAiResponseRated integrado en cosmic_coach_chat_screen
□ trigger30DayActiveUser integrado en home_screen
□ recordCrash() llamado en main.dart error handlers
□ recordSupportContact() llamado en settings_screen
□ recordPremiumCancellation() llamado en revenuecat_service
□ _getRatingText() usando AppLocalizations
□ _issueCategories usando AppLocalizations
□ Analytics events definidos en analytics_events.dart
□ review_prompt_service usando constantes de AnalyticsEvents
□ flutter analyze sin errores
```

### Tests de Validación:
```bash
# Verificar compilación
cd zodiac_app && flutter analyze

# Verificar imports
grep -r "ReviewPromptService" lib/screens/ lib/main.dart

# Verificar localizaciones
flutter gen-l10n
```

---

## Dependencias entre Agentes

```
AGENTE 1 ──────────────────────────────────> NINGUNA
          (independiente)

AGENTE 2 ──────────────────────────────────> NINGUNA
          (independiente)

AGENTE 3 ──────────────────────────────────> PARCIAL
          (puede necesitar keys de ARB si no existen)
```

**Conclusión:** Los 3 agentes pueden ejecutarse en PARALELO ya que trabajan en archivos diferentes sin conflictos.

---

## Archivos Modificados por Agente

| Agente | Archivos | Tipo |
|--------|----------|------|
| 1 | `ai_response_rating_widget.dart` | CREAR |
| 1 | `cosmic_coach_chat_screen.dart` | MODIFICAR |
| 1 | `home_screen.dart` | MODIFICAR |
| 1 | `review_prompt_service.dart` | MODIFICAR (método nuevo) |
| 2 | `main.dart` | MODIFICAR |
| 2 | `settings_screen.dart` | MODIFICAR |
| 2 | `revenuecat_service.dart` | MODIFICAR |
| 3 | `review_prompt_service.dart` | MODIFICAR (localización) |
| 3 | `analytics_events.dart` | MODIFICAR |
| 3 | `app_*.arb` (si faltan keys) | MODIFICAR |

---

## Métricas de Éxito

| Métrica | Antes | Después |
|---------|-------|---------|
| Triggers integrados | 5/7 (71%) | 7/7 (100%) |
| Disqualifiers conectados | 0/3 (0%) | 3/3 (100%) |
| Textos localizados | 0% | 100% |
| Analytics coverage | 60% | 100% |

---

**Última actualización:** Noviembre 2025
**Autor:** Claude Code Multi-Agent System
