# 🚀 PLAN DE MEJORAS COSMIC COACH - "CHAD 2.0"
## Sistema de Metas Personalizadas con Contexto Real

### 📌 OBJETIVOS PRINCIPALES

1. **Contexto Real del Usuario (80% sesiones completas)**
   - Capturar sueño, estado emocional y energía actual
   - Persistir datos para análisis longitudinal
   - Reducir dependencia de valores por defecto

2. **Telemetría Accionable (Dashboard de métricas)**
   - Tracking de éxito/fallo del adapter
   - Detección de fallbacks genéricos (-50% metas genéricas)
   - Análisis de patrones por idioma y signo

3. **Experiencia Guiada (100% datos requeridos)**
   - Alertas proactivas de datos faltantes
   - Textos motivacionales por idioma
   - Onboarding contextual

---

## 🏗️ ARQUITECTURA DE IMPLEMENTACIÓN

### FASE 1: CAPTURA DE CONTEXTO EN UI (3-4 días)

#### 1.1 Formulario de Contexto Rápido
```dart
// Ubicación: cosmic_coach_screen.dart (línea ~130)
// NUEVO: Widget de captura antes de generar metas
```

**Componentes a crear:**
- `ContextCaptureDialog` - Modal con 3 pasos:
  - Sueño: Slider (3-12 horas)
  - Estado emocional: Chips (energético/calmado/ansioso/motivado/cansado)
  - Nivel energía: Visual bars (bajo/medio/alto)

**Integración:**
- Mostrar ANTES de `generateNewGoals()` si no hay contexto reciente (<24h)
- Guardar en PreferencesService con timestamp
- Pasar datos al adapter sin defaults

#### 1.2 Persistencia en PreferencesService
```dart
// Nuevos métodos en preferences_service.dart
Future<void> saveUserContext(Map<String, dynamic> context)
Map<String, dynamic>? getLastUserContext()
bool hasRecentContext() // <24 horas
```

**Almacenamiento:**
- SecureStorage para datos sensibles
- Keys: `user_context_sleep`, `user_context_emotion`, `user_context_energy`
- Incluir timestamp para validación

#### 1.3 Provider Updates
```dart
// cosmic_goals_provider.dart línea ~77
// Modificar generateNewGoals para aceptar contexto
Future<void> generateNewGoals({
  // ... existing params
  double? sleepHours,
  String? emotionalState,
  String? energyLevel,
})
```

---

### FASE 2: MEJORAS EN ENHANCED COACH ADAPTER (2-3 días)

#### 2.1 Contexto Real vs Defaults
```dart
// enhanced_coach_adapter.dart línea ~37
// CAMBIO: Solo usar defaults si NO hay contexto
final context = UserContext(
  sleepHours: sleepHours ?? _getLastSleepOrNull(),
  emotionalState: emotionalState ?? _getLastEmotionOrNull(),
  energyLevel: energyLevel ?? _getLastEnergyOrNull(),
  hasRealData: sleepHours != null || emotionalState != null,
);
```

#### 2.2 Validaciones Proactivas
```dart
// Nuevo método en adapter
Map<String, dynamic> validateUserData() {
  return {
    'hasBirthDate': userPrefs.birthDate != null,
    'hasLanguage': languageCode != 'en',
    'hasContext': hasRecentContext(),
    'missingFields': [...],
  };
}
```

#### 2.3 Fallback Detection
```dart
// En generatePersonalizedGoals línea ~95
if (convertedGoals.isEmpty) {
  AppLogger.warning('FALLBACK: No goals generated', {
    'reason': 'empty_result',
    'userSign': userSign,
    'language': languageCode,
  });
  _trackFallbackUsage(userSign, languageCode);
  return _generateFallbackGoals(); // Con tracking
}
```

#### 2.4 Enhanced Logging
```dart
// Mejorar logs existentes con metadata
AppLogger.info('Goal generation attempt', {
  'userSign': userSign,
  'language': languageCode,
  'hasRealContext': context.hasRealData,
  'birthDatePresent': birthDate != null,
  'biorhythmPhases': _calculatePhases(birthDate),
});
```

---

### FASE 3: TELEMETRÍA Y OBSERVABILIDAD (2 días)

#### 3.1 Analytics Events
```dart
// analytics_service.dart - Nuevos eventos
class CosmicCoachEvents {
  static const GENERATION_SUCCESS = 'coach_goal_generation_success';
  static const GENERATION_FAILURE = 'coach_goal_generation_failure';
  static const FALLBACK_USED = 'coach_fallback_used';
  static const CONTEXT_CAPTURED = 'coach_context_captured';
  static const MISSING_DATA_SHOWN = 'coach_missing_data_alert';
}
```

**Payload estándar:**
```dart
{
  'user_sign': String,
  'language': String,
  'has_birthdate': bool,
  'has_context': bool,
  'goal_count': int,
  'is_fallback': bool,
  'error_type': String?, // Si aplica
  'biorhythm_phases': Map<String, double>?,
}
```

#### 3.2 Crash Reporting Integration
```dart
// crash_reporting_service.dart
// Agregar custom keys para Chad
void setChadUserContext(Map<String, dynamic> context) {
  Crashlytics.instance.setCustomKey('chad_language', context['language']);
  Crashlytics.instance.setCustomKey('chad_has_birthdate', context['hasBirthDate']);
  Crashlytics.instance.setCustomKey('chad_last_generation', DateTime.now().toIso8601String());
}
```

#### 3.3 Dashboard Queries (BigQuery)
```sql
-- Métricas clave de Chad
SELECT
  DATE(timestamp) as date,
  params.value.string_value as language,
  COUNT(*) as total_generations,
  SUM(CASE WHEN params.is_fallback THEN 1 ELSE 0 END) as fallback_count,
  AVG(params.goal_count) as avg_goals_generated
FROM `project.analytics.events`
WHERE event_name = 'coach_goal_generation_success'
GROUP BY date, language
```

---

### FASE 4: EXPERIENCIA DE USUARIO (2 días)

#### 4.1 Banner de Datos Faltantes
```dart
// cosmic_coach_screen.dart - Nuevo widget
Widget _buildMissingDataBanner() {
  final missingFields = ref.read(cosmicGoalsProvider).getMissingFields();
  if (missingFields.isEmpty) return SizedBox.shrink();

  return Card(
    color: Colors.amber.shade100,
    child: ListTile(
      leading: Icon(Icons.info_outline),
      title: Text(localizations.complete_profile_for_better_goals),
      subtitle: Text(missingFields.join(', ')),
      trailing: TextButton(
        onPressed: _navigateToProfile,
        child: Text(localizations.complete_now),
      ),
    ),
  );
}
```

#### 4.2 Mensajes Motivacionales Mejorados
```dart
// biorhythm_goal_generator.dart
// Agregar CTA y contexto por idioma
String _enhanceGoalDescription(String base, String language) {
  final motivationalSuffix = getLocalizedText(
    'motivational_cta',
    language,
    {
      'en': 'Start with just 5 minutes today!',
      'es': '¡Comienza con solo 5 minutos hoy!',
      'it': 'Inizia con soli 5 minuti oggi!',
      // ...
    }
  );
  return '$base\n\n💫 $motivationalSuffix';
}
```

#### 4.3 Onboarding Contextual
```dart
// Nuevo: coach_onboarding_dialog.dart
class CoachOnboardingDialog extends StatelessWidget {
  // Tutorial de 3 pasos:
  // 1. Por qué el contexto mejora las metas
  // 2. Cómo los biorritmos personalizan tu experiencia
  // 3. Tu primera meta del día
}
```

---

## 📅 CRONOGRAMA OPTIMIZADO

### Semana 1 (Implementación Core)
**Días 1-2: Captura de Contexto**
- [ ] Crear ContextCaptureDialog
- [ ] Integrar con PreferencesService
- [ ] Actualizar cosmic_goals_provider
- [ ] Tests unitarios de persistencia

**Días 3-4: Chad Adapter Mejorado**
- [ ] Eliminar defaults automáticos
- [ ] Implementar validaciones
- [ ] Mejorar logging con metadata
- [ ] Detectar y trackear fallbacks

**Día 5: Telemetría Básica**
- [ ] Definir eventos en AnalyticsService
- [ ] Integrar con Crashlytics
- [ ] Primer tracking en adapter

### Semana 2 (Polish & Monitoring)
**Días 6-7: UX Mejorada**
- [ ] Banner datos faltantes
- [ ] Mensajes motivacionales
- [ ] Onboarding contextual
- [ ] Localización completa

**Días 8-9: Dashboard & QA**
- [ ] Queries BigQuery
- [ ] Tests E2E
- [ ] Beta deployment
- [ ] Documentación

**Día 10: Rollout**
- [ ] Feature flag activation
- [ ] Monitor métricas
- [ ] Hotfixes si necesario

---

## 🎯 MÉTRICAS DE ÉXITO

### KPIs Principales
- **Contexto capturado:** ≥80% sesiones con datos reales
- **Reducción fallbacks:** -50% metas genéricas
- **Completitud datos:** 100% usuarios con birthDate antes de generar
- **Engagement:** +30% en completion rate de metas

### Métricas Secundarias
- Tiempo promedio captura contexto: <30 segundos
- CTR en banner datos faltantes: >15%
- Retención D7 usuarios con contexto: +20%

---

## 🔧 CONSIDERACIONES TÉCNICAS

### Dependencias Críticas
1. PreferencesService debe estar inicializado
2. SecureStorage para datos sensibles
3. AnalyticsService configurado con eventos
4. Localización completa para todos los idiomas

### Riesgos y Mitigaciones
- **Riesgo:** Fatiga del usuario por formulario
  - **Mitigación:** Hacer opcional, recordar última entrada

- **Riesgo:** Aumento de fallbacks sin birthDate
  - **Mitigación:** Generar fecha estimada por signo

- **Riesgo:** Datos incorrectos del usuario
  - **Mitigación:** Validación y rangos sensatos

### Testing Strategy
1. **Unit Tests:** Persistencia, validaciones, conversiones
2. **Integration:** Flow completo con/sin contexto
3. **E2E:** Usuario nuevo vs recurrente
4. **A/B Test:** Con/sin captura de contexto

---

## 📝 DOCUMENTACIÓN REQUERIDA

1. **API Docs:** Nuevos métodos en services
2. **Analytics Schema:** Eventos y payloads
3. **User Guide:** Cómo usar el contexto
4. **Dashboard Manual:** Queries y métricas

---

## ✅ CHECKLIST PRE-LAUNCH

- [ ] Todos los tests pasando
- [ ] Localización completa (7+ idiomas)
- [ ] Analytics events firing
- [ ] Crashlytics keys configuradas
- [ ] Feature flag creado
- [ ] Dashboard queries funcionando
- [ ] Documentación actualizada
- [ ] QA approval
- [ ] Beta feedback positivo
- [ ] Rollback plan listo

---

## 🚀 SIGUIENTES PASOS INMEDIATOS

1. **HOY:** Revisar y aprobar este plan
2. **MAÑANA:** Comenzar con ContextCaptureDialog
3. **Esta semana:** Completar Fase 1 y 2
4. **Próxima semana:** Polish, QA y rollout

---

*Documento creado: 27 Nov 2025*
*Última actualización: 27 Nov 2025*
*Versión: 1.0*