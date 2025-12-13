# Plan de Mejoras: Sistema de Reviews/Rankings App Store

## Estado Actual

El `ReviewPromptService` está **85% completo pero 0% integrado**. El servicio está bien construido pero no se usa en ninguna pantalla.

---

## Fase 1: Integraciones Críticas (4-6 horas)
**Impacto: ALTO | Esfuerzo: BAJO**

### 1.1 Integrar en Compra Premium ⭐ PRIORIDAD MÁXIMA
**Archivo:** `lib/features/premium/controllers/premium_controller_v2.dart`
**Trigger:** `triggerFirstPremiumPurchase`

```dart
// Después de compra exitosa (~línea 207)
await ReviewPromptService().triggerReviewPromptFlow(
  context: context,
  triggerId: ReviewPromptService.triggerFirstPremiumPurchase,
);
```

**Por qué es crítico:** Los usuarios que pagan están más satisfechos = reviews de 5 estrellas.

---

### 1.2 Integrar en Goal Completion ⭐ PRIORIDAD MÁXIMA
**Archivo:** `lib/screens/goal_planner/goal_detail_screen.dart`
**Trigger:** `triggerGoalAchieved`

```dart
// Después de GoalCompletionCelebration.onDismiss()
if (goal.progress >= 100) {
  await ReviewPromptService().triggerReviewPromptFlow(
    context: context,
    triggerId: ReviewPromptService.triggerGoalAchieved,
  );
}
```

**Por qué es crítico:** Momento de máxima satisfacción = reviews positivos.

---

### 1.3 Integrar en Birth Chart ⭐ PRIORIDAD ALTA
**Archivo:** `lib/screens/birth_chart_visualization_screen.dart`
**Trigger:** `triggerBirthChartGenerated`

```dart
// Después de cargar carta natal exitosamente
await ReviewPromptService().triggerReviewPromptFlow(
  context: context,
  triggerId: ReviewPromptService.triggerBirthChartGenerated,
);
```

---

## Fase 2: Integraciones de Alto Impacto (6-10 horas)
**Impacto: ALTO | Esfuerzo: MEDIO**

### 2.1 Compatibilidad "Wow Moment"
**Archivo:** `lib/screens/compatibility_screen.dart`
**Trigger:** `triggerCompatibilityWow`

**Implementación:**
1. Detectar cuando el score >= 80%
2. Mostrar prompt después de que el usuario vea el resultado
3. Delay de 120 segundos

```dart
// Después de calcular compatibilidad
if (compatibilityResult.overallScore >= 80) {
  Future.delayed(Duration(seconds: 120), () {
    if (mounted) {
      ReviewPromptService().triggerReviewPromptFlow(
        context: context,
        triggerId: ReviewPromptService.triggerCompatibilityWow,
        customDelaySeconds: 0, // Ya esperamos 120s
      );
    }
  });
}
```

---

### 2.2 Streak de 7 Días
**Archivo:** `lib/screens/home_screen.dart`
**Trigger:** `triggerEngagementStreak`

**Implementación:**
1. Verificar días consecutivos al abrir home
2. Mostrar prompt cuando llegue a 7

```dart
// En initState o después de cargar horóscopo
final consecutiveDays = await ReviewPromptService()
    .getStatistics()['consecutive_days'];

if (consecutiveDays >= 7) {
  await ReviewPromptService().triggerReviewPromptFlow(
    context: context,
    triggerId: ReviewPromptService.triggerEngagementStreak,
  );
}
```

---

## Fase 3: Mejoras de UX/UI (8-12 horas)
**Impacto: MEDIO | Esfuerzo: ALTO**

### 3.1 Localizar Textos del Diálogo
**Problema:** Los textos del diálogo están hardcodeados en inglés.

**Solución:**
1. Usar las traducciones ya agregadas en los ARB
2. Actualizar `_InAppRatingDialog` y `_FeedbackFormDialog`

**Archivos a modificar:**
- `lib/services/review_prompt_service.dart`
- Regenerar localizaciones con `flutter gen-l10n`

---

### 3.2 Agregar Rating UI en Cosmic Coach
**Archivo:** `lib/screens/cosmic_coach_chat_screen.dart`
**Trigger:** `triggerAiResponseRated`

**Nueva funcionalidad:**
1. Crear widget `AiResponseRating` con 5 estrellas
2. Mostrar debajo de cada respuesta del coach
3. Al dar 5 estrellas → trigger review prompt

```dart
class AiResponseRating extends StatelessWidget {
  final Function(int) onRated;

  // Widget con 5 estrellas tapables
  // Al seleccionar 5 → onRated(5) → trigger review
}
```

---

## Fase 4: Mejoras Avanzadas (10-15 horas)
**Impacto: MEDIO | Esfuerzo: ALTO**

### 4.1 Crear ReviewTriggerManager
**Propósito:** Centralizar la lógica de triggers y escuchar eventos automáticamente.

```dart
// lib/services/review_trigger_manager.dart
class ReviewTriggerManager {
  static final instance = ReviewTriggerManager._();

  // Escucha eventos de analytics y auto-triggerea
  void onGoalCompleted(Goal goal, BuildContext context);
  void onCompatibilityCalculated(int score, BuildContext context);
  void onPurchaseCompleted(BuildContext context);
  void onBirthChartGenerated(BuildContext context);
  void onAiResponseRated(int rating, BuildContext context);
}
```

---

### 4.2 Mejorar Logging y Debug
**Problema:** Difícil debuggear por qué no se muestran prompts.

**Solución:**
```dart
Future<ReviewDecision> shouldShowReviewPromptWithReason(String triggerId) async {
  return ReviewDecision(
    shouldShow: true/false,
    reason: 'Already shown in last 90 days',
    daysUntilEligible: 45,
  );
}
```

---

### 4.3 A/B Testing Framework
**Variantes a probar:**
- **Timing:** 60s vs 90s vs 120s de delay
- **Mensaje:** "Rate us?" vs "How would you rate Zodiac Life?"
- **Visual:** Minimal vs con emoji vs con tema cósmico

---

## Fase 5: Analytics y Dashboard (5-8 horas)

### 5.1 Eventos de Analytics Adicionales
```dart
// Agregar estos eventos
'review_prompt_eligible' // Cuando califica pero no se muestra
'review_prompt_blocked_reason' // Por qué se bloqueó
'review_to_store_conversion' // Si dejó review en store
'feedback_issue_category' // Qué categoría seleccionó
```

### 5.2 Dashboard de Métricas
**KPIs a trackear:**
- Tasa de conversión: mostrado → rated → app store
- Rating promedio por trigger
- Tiempo promedio hasta primer review
- Categorías de feedback más comunes

---

## Cronograma Sugerido

| Fase | Descripción | Tiempo | Prioridad |
|------|-------------|--------|-----------|
| 1 | Integraciones Críticas | 4-6h | 🔴 CRÍTICO |
| 2 | Integraciones Alto Impacto | 6-10h | 🟠 ALTO |
| 3 | Mejoras UX/UI | 8-12h | 🟡 MEDIO |
| 4 | Mejoras Avanzadas | 10-15h | 🟢 BAJO |
| 5 | Analytics y Dashboard | 5-8h | 🟢 BAJO |

**Total estimado:** 33-51 horas

---

## Implementación Recomendada

### Sprint 1 (Esta semana) - CRÍTICO
- [ ] 1.1 Integrar en compra premium
- [ ] 1.2 Integrar en goal completion
- [ ] 1.3 Integrar en birth chart

### Sprint 2 (Próxima semana) - ALTO
- [ ] 2.1 Compatibilidad wow moment
- [ ] 2.2 Streak de 7 días
- [ ] 3.1 Localizar textos

### Sprint 3 (Semana 3) - MEDIO
- [ ] 3.2 Rating UI en Cosmic Coach
- [ ] 4.1 ReviewTriggerManager
- [ ] 4.2 Mejorar logging

### Sprint 4 (Semana 4) - BAJO
- [ ] 4.3 A/B Testing
- [ ] 5.1 Analytics adicionales
- [ ] 5.2 Dashboard métricas

---

## Métricas de Éxito

| Métrica | Objetivo 30 días | Objetivo 90 días |
|---------|------------------|------------------|
| Rating en App Store | 4.0+ estrellas | 4.5+ estrellas |
| Reviews por semana | 5+ | 15+ |
| % reviews 4-5 estrellas | 80%+ | 85%+ |
| Tasa conversión prompt→review | 30%+ | 40%+ |

---

## Notas Importantes

1. **Apple limita a 3 prompts/año por usuario** - El servicio ya lo respeta
2. **No pedir en las primeras 24h** - Ya implementado
3. **Pre-filtrar con rating in-app** - Ya implementado, previene reviews negativos
4. **Feedback de usuarios insatisfechos** - Ya implementado, captura problemas

---

**Última actualización:** Noviembre 2025
**Responsable:** Equipo de desarrollo
