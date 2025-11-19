# 🐛 Bug Report - Cosmic Coach & Analytics

**Fecha:** 13 de Noviembre 2025
**Reportado por:** Usuario
**Estado:** 🔍 **INVESTIGANDO**

---

## 🐛 Bug #1: Tareas completadas vuelven a "sin completar"

### **Descripción del Usuario:**
> "Cuando marco algo como 'completado' después voy para atrás o se va solo a veces. Vuelvo y está sin completar. Me lo suma arriba donde dice 'Tus mejores categorías: bienestar', pero aparece sin completar por hoy. Tendría que aparecer ya completado, o 'ya hecho', o 'ya hecho hoy'."

### **Síntomas:**
1. Usuario marca una tarea como completada
2. La tarea se suma a las estadísticas ("Tus mejores categorías: bienestar")
3. Al volver a la pantalla, la tarea aparece sin completar
4. El progreso se perdió

### **Ubicación del Código:**

#### **ExpandableGoalCard** (`lib/widgets/expandable_goal_card.dart`):
- Línea 364-366: Botón "Complete/Completar"
```dart
onTap: () {
  HapticFeedback.mediumImpact();
  widget.onComplete(); // ← Llama al callback
},
```

- Línea 403-435: Badge de "Completado"
```dart
if (isCompleted)  // isCompleted = widget.goal.progress >= 1.0
  Container(
    child: Text(
      widget.languageCode == 'es'
          ? '¡Completado! 🎉'
          : 'Completed! 🎉',
    ),
  ),
```

#### **CosmicGoalsProvider** (`lib/providers/cosmic_goals_provider.dart`):
- Línea 163-200: Método `completeGoal()`
```dart
Future<bool> completeGoal(String goalTitle) async {
  // 1. Find goal
  final goalIndex = _currentGoals.indexWhere((g) => g.title == goalTitle);

  // 2. Complete in persistence service
  final success = await _persistenceService.completeGoal(goal);

  if (success) {
    // 3. Update goal to 100% progress
    _currentGoals[goalIndex] = goal.copyWith(progress: 1.0);

    // 4. Save updated goals
    await _persistenceService.saveGoals(_currentGoals);

    // 5. Reload statistics
    await loadStatistics();

    notifyListeners();
    return true;
  }
  return false;
}
```

### **Análisis Inicial:**

#### **Posibles Causas:**

**1. La tarea NO se está marcando como completada en el día actual:**
```dart
// En goal_persistence_service.dart, línea ~110-130
Future<bool> completeGoal(CosmicGoalUnified goal) async {
  // Guarda en history
  // Actualiza stats
  // ¿PERO marca el goal como completedToday?
}
```

**Problema potencial:**
- El goal se completa (progress = 1.0)
- Se guarda en history
- Se actualiza stats
- PERO cuando se recarga la pantalla, el sistema podría estar:
  - Generando nuevos goals
  - O cargando goals sin el flag de "completedToday"

**2. El flag `completedToday` no existe en el modelo:**

Revisando `CosmicGoalUnified`:
```dart
class CosmicGoalUnified {
  final String title;
  final String description;
  final String category;
  final String difficulty;
  final String suggestedBy;
  final double progress;  // 0.0 - 1.0
  // ❌ NO HAY: bool completedToday
  // ❌ NO HAY: DateTime? completedAt
}
```

**3. Sistema de "refresh" borra el progreso:**

En `cosmic_goals_provider.dart`, línea 43-53:
```dart
Future<void> _initialize() async {
  await _persistenceService.initialize();

  // 🚨 PROBLEMA: Esto limpia TODOS los goals cada vez que se inicializa
  await _persistenceService.saveGoals([]); // Clear goals
  AppLogger.info('🧹 Cleared old goals - Enhanced Adapter will generate fresh ones');

  await loadStatistics();
}
```

**ESTE ES EL BUG:** Cada vez que se inicializa el provider (al abrir la pantalla), limpia todos los goals!

---

## 🐛 Bug #2: Analytics Dashboard - Números Fijos

### **Descripción del Usuario:**
> "Yo usé el Coach y sigue marcándome 23. Está fijo eso. Probé más compatibilidad y sigue marcándome 18. Está usando Mox o no está actualizándose."

### **Síntomas:**
1. Analytics muestra "23" para Coach sessions
2. Analytics muestra "18" para Compatibility checks
3. Los números NO cambian después de usar las features

### **Ubicación del Código:**

#### **AnalyticsDataProvider** (`lib/providers/analytics_data_provider.dart`):

Línea 112-119:
```dart
// Compatibility checks - from premium feature usage
final featureUsage = premiumReport?['feature_usage_breakdown'] as Map<String, dynamic>?;
final compatibilityChecks = (featureUsage?['PremiumFeature.compatibility'] as num?)?.toInt() ??
                              _getRandomSampleData(5, 20);  // ← FALLBACK a datos mock

// Coach sessions - from premium feature usage
final coachSessions = (featureUsage?['PremiumFeature.cosmicCoach'] as num?)?.toInt() ??
                      _getRandomSampleData(10, 30);  // ← FALLBACK a datos mock
```

Línea 240-245:
```dart
/// Generate random sample data (for features not yet tracked)
int _getRandomSampleData(int min, int max) {
  // 🚨 PROBLEMA: NO es random! Es basado en el día del mes
  final seed = DateTime.now().day % (max - min);
  return min + seed;
}
```

**Cálculo del Bug:**
```
Hoy es 13 de noviembre:
DateTime.now().day = 13

Coach sessions:
  seed = 13 % (30 - 10) = 13 % 20 = 13
  return 10 + 13 = 23  ← ¡SIEMPRE 23 hoy!

Compatibility checks:
  seed = 13 % (20 - 5) = 13 % 15 = 13
  return 5 + 13 = 18  ← ¡SIEMPRE 18 hoy!
```

**Por qué están "fijos":**
- El método `_getRandomSampleData()` usa el DÍA del mes como seed
- Siempre devuelve el mismo número durante todo el día
- Mañana (día 14) mostrará números diferentes, pero igual fijos

**Por qué se usan datos mock:**
- La condición `featureUsage?['PremiumFeature.cosmicCoach']` devuelve `null`
- Entonces se ejecuta el fallback: `?? _getRandomSampleData(10, 30)`
- Esto significa que `CoreAnalyticsService` NO está trackeando correctamente

---

## 🔍 Root Cause Analysis

### **Bug #1 - Root Cause:**

**Problema Principal:** Provider se resetea en cada inicialización

```dart
// cosmic_goals_provider.dart:43-53
Future<void> _initialize() async {
  await _persistenceService.initialize();

  // 🔥 BUG: Esto borra TODOS los goals cada vez
  await _persistenceService.saveGoals([]);  // ← AQUÍ

  await loadStatistics();
}
```

**Por qué pasa:**
1. Usuario completa una tarea → se guarda en history ✅
2. Usuario sale de Cosmic Coach
3. Usuario vuelve a entrar a Cosmic Coach
4. Provider se inicializa → llama `_initialize()`
5. `_initialize()` borra todos los goals → `saveGoals([])`
6. Usuario ve tareas sin completar ❌

**El comentario en el código:**
```dart
// 🔄 FORCE FRESH GOALS: Clear old goals to ensure Enhanced Adapter generates new ones
// This is a one-time migration to clear stale "acciones hacia tus metas" goals
```

Este fue un "migration" temporal que se quedó en el código!

### **Bug #2 - Root Cause:**

**Problema Principal:** CoreAnalyticsService no está trackeando features correctamente

```dart
// analytics_data_provider.dart:112-119
final featureUsage = premiumReport?['feature_usage_breakdown'] as Map<String, dynamic>?;
```

**Por qué `featureUsage` es null:**
1. `CoreAnalyticsService.getConsolidatedAnalyticsDashboard()` devuelve data
2. Pero `premium_analytics.feature_usage_breakdown` está vacío o null
3. Entonces `featureUsage` es null
4. Se ejecuta el fallback a datos mock

**Posibles razones:**
- CoreAnalyticsService no está trackeando Cosmic Coach usage
- CoreAnalyticsService no está trackeando Compatibility checks
- Los eventos de Firebase Analytics no se están enviando
- Los eventos se envían pero con nombres diferentes

---

## ✅ Soluciones Propuestas

### **Solución Bug #1: Remover el reset de goals**

#### **Opción A: Comentar el reset (Quick Fix)**
```dart
Future<void> _initialize() async {
  await _persistenceService.initialize();

  // 🔧 FIX: Don't clear goals on every init
  // This was a one-time migration that should be removed
  // await _persistenceService.saveGoals([]);

  await loadStatistics();
  await loadGoals();  // ← Cargar goals guardados
}
```

#### **Opción B: Agregar flag completedToday (Solución Completa)**

1. Agregar campo al modelo:
```dart
class CosmicGoalUnified {
  final String title;
  final String description;
  final String category;
  final String difficulty;
  final String suggestedBy;
  final double progress;
  final bool completedToday;  // ← NUEVO
  final DateTime? completedAt;  // ← NUEVO
}
```

2. Actualizar lógica de completado:
```dart
Future<bool> completeGoal(String goalTitle) async {
  // Mark as completed TODAY
  _currentGoals[goalIndex] = goal.copyWith(
    progress: 1.0,
    completedToday: true,  // ← NUEVO
    completedAt: DateTime.now(),  // ← NUEVO
  );

  await _persistenceService.saveGoals(_currentGoals);
}
```

3. Mostrar estado correcto en UI:
```dart
// En ExpandableGoalCard
if (widget.goal.completedToday)
  Container(
    child: Text('✅ Ya completado hoy'),
  )
else if (isCompleted)
  Container(
    child: Text('✅ Completado'),
  )
```

### **Solución Bug #2: Conectar a datos reales**

#### **Opción A: Verificar CoreAnalyticsService tracking**

1. Verificar que se estén enviando eventos:
```dart
// En cosmic_coach_chat_screen.dart
await CoreAnalyticsService.instance.trackFeatureUsage(
  'cosmic_coach_message_sent',
  metadata: {'type': 'user_message'},
);
```

2. Verificar que Compatibility screen envía eventos:
```dart
// En compatibility_screen.dart
await CoreAnalyticsService.instance.trackFeatureUsage(
  'compatibility_check_performed',
  metadata: {'signs': [sign1, sign2]},
);
```

#### **Opción B: Usar contador local (Quick Fix)**

```dart
// En analytics_data_provider.dart
Future<UserStats> _buildUserStats(...) async {
  // Try to get real data from SharedPreferences
  final prefs = await SharedPreferences.getInstance();
  final coachSessions = prefs.getInt('coach_sessions_count') ?? 0;
  final compatibilityChecks = prefs.getInt('compatibility_checks_count') ?? 0;

  return UserStats(
    coachSessions: coachSessions,
    compatibilityChecks: compatibilityChecks,
    // ...
  );
}
```

3. Incrementar contador cuando se usa:
```dart
// En cosmic_coach_chat_screen.dart
Future<void> _sendMessage() async {
  final prefs = await SharedPreferences.getInstance();
  final count = prefs.getInt('coach_sessions_count') ?? 0;
  await prefs.setInt('coach_sessions_count', count + 1);
}
```

---

## 🎯 Plan de Acción Recomendado

### **Prioridad Alta (Ahora):**

1. **Bug #1 - Quick Fix:**
   - Comentar línea que borra goals en `_initialize()`
   - Agregar `await loadGoals()` para cargar goals guardados
   - **Tiempo:** 2 minutos
   - **Impacto:** ✅ Arregla completamente el bug

2. **Bug #2 - Quick Fix:**
   - Reemplazar `_getRandomSampleData()` con contador local
   - Agregar tracking en screens relevantes
   - **Tiempo:** 15 minutos
   - **Impacto:** ✅ Muestra números reales

### **Prioridad Media (Después):**

3. **Bug #1 - Solución Completa:**
   - Agregar `completedToday` y `completedAt` al modelo
   - Actualizar lógica de UI
   - Mostrar "Ya completado hoy" en español
   - **Tiempo:** 30 minutos

4. **Bug #2 - Integración CoreAnalyticsService:**
   - Verificar que eventos se envían correctamente
   - Asegurar que `feature_usage_breakdown` se popula
   - **Tiempo:** 1 hora

---

## 📝 Testing Requerido

### **Para Bug #1:**
1. Completar una tarea
2. Salir de Cosmic Coach
3. Volver a entrar
4. ✅ Verificar que la tarea sigue completada

### **Para Bug #2:**
1. Ir a Analytics Dashboard → anotar números
2. Usar Cosmic Coach (enviar mensaje)
3. Volver a Analytics → verificar que el número subió
4. Usar Compatibility
5. Volver a Analytics → verificar que el número subió

---

## 🚀 ¿Quieres que lo arregle ahora?

Puedo implementar los **Quick Fixes** ahora mismo:
- Bug #1: Comentar el reset (2 min)
- Bug #2: Implementar contador local (15 min)

**Total tiempo:** ~20 minutos
**Resultado:** Ambos bugs arreglados

¿Procedo?
