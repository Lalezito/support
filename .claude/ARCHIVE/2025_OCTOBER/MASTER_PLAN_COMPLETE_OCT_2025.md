# 🎯 MASTER PLAN COMPLETO - Zodiac App + Backend
## Octubre 2025 - Plan Integral de Ejecución

**Última actualización**: Octubre 8, 2025
**Status**: Goal Planner ✅ LIVE | TODOs Pendientes | Features Roadmap

---

## 📊 RESUMEN EJECUTIVO

### ✅ Completado Recientemente
- **Goal Planner Backend**: Deployado y funcionando en producción
- **OpenAI Integration**: GPT-4 conectado y operativo
- **Database Schema**: premium_goals + goal_check_ins creadas
- **API Endpoints**: 6 endpoints funcionando en Railway

### 🔄 En Progreso
- Flutter Goal Planner UI (no iniciado)
- TODOs críticos del análisis anterior
- Features premium pendientes

### 📈 Prioridades
1. **INMEDIATO**: TODOs críticos (blocking production)
2. **SEMANA 1**: Goal Planner Flutter integration
3. **SEMANA 2-3**: Features premium roadmap
4. **SEMANA 4+**: Optimizaciones y Phase 2

---

## 🔴 FASE 0: CRÍTICOS (HACER PRIMERO - BLOCKING PRODUCTION)

### 0.1 🔴 Notificaciones Reales [CRÍTICO]
**Archivo**: `lib/services/prediction_notification_service.dart`
**Tiempo**: 45 minutos
**Prioridad**: MÁXIMA

**Problema**:
- TODOs en líneas 143, 149, 155, 245, 258, 270
- Mock notifications no funcionan
- Bloquea feature de predicciones

**Solución**:
```dart
// lib/services/prediction_notification_service.dart

// Agregar import
import 'package:zodiac_app/services/unified_notification_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';

// Reemplazar TODOs
Future<void> scheduleNotification() async {
  // Línea 143
  await UnifiedNotificationService().scheduleNotification(
    id: notificationId,
    title: title,
    body: body,
    scheduledDate: scheduledDate,
    payload: payload,
  );
}

Future<void> cancelAllNotifications() async {
  // Línea 149
  await UnifiedNotificationService().cancelAllNotifications();
}

Future<void> _sendNotification() async {
  // Línea 155
  await UnifiedNotificationService().sendNotification(
    title: title,
    body: body,
    payload: payload,
  );
}

Future<void> _loadPreferences() async {
  // Línea 245
  final prefs = PreferencesService.instance;
  final json = await prefs.getString('prediction_notification_prefs');
  if (json != null) {
    // Parse and load settings
  }
}

Future<void> _savePreferences() async {
  // Líneas 258, 270
  final prefs = PreferencesService.instance;
  await prefs.setString('prediction_notification_prefs', jsonEncode(settings));
}
```

**Testing**:
```bash
cd zodiac_app
flutter test test/services/prediction_notification_service_test.dart
```

---

### 0.2 🔴 UserID Anónimo [CRÍTICO]
**Archivos**: 8 servicios
**Tiempo**: 30 minutos
**Prioridad**: MÁXIMA

**Problema**:
- `userId: 'anonymous'` hardcoded en 8 archivos
- Analytics no trackea usuarios reales
- Bloquea métricas de conversión

**Archivos a actualizar**:
1. `lib/services/consolidated_compatibility/core_compatibility_service.dart`
2. `lib/services/production_analytics_service.dart`
3. `lib/services/consolidated_analytics/core_analytics_service.dart`
4. `lib/services/compatibility_analytics_service.dart`
5. `lib/services/ai_insights/optimized_ai_insights_system.dart`
6. `lib/services/ai_insights/ai_insights_performance_service.dart`
7. `lib/services/consolidated_ai/core_ai_service.dart`
8. `lib/services/payment/enterprise_payment_orchestrator.dart`

**Solución** (aplicar a TODOS):
```dart
// Agregar import
import 'package:zodiac_app/services/user_identity_service.dart';

// En el constructor o método init
class ServiceName {
  final UserIdentityService _userIdentity;

  ServiceName() : _userIdentity = UserIdentityService();

  // En métodos que usan userId
  Future<void> someMethod() async {
    final userId = _userIdentity.getUserId(); // En vez de 'anonymous'

    // Usar userId real
    await analytics.track(userId: userId, ...);
  }
}
```

**Verificar** en `lib/main.dart`:
```dart
void main() async {
  // Asegurar que UserIdentityService se inicializa
  await UserIdentityService().initialize();
  // ...
}
```

---

### 0.3 🔴 Pricing Provider [CRÍTICO]
**Archivo**: `lib/providers/premium_provider.dart`
**Tiempo**: 20 minutos
**Prioridad**: MÁXIMA

**Problema**:
- `pricingInfoProvider` comentado (línea 77-80)
- No muestra precios reales en premium screen
- Afecta conversión

**Solución**:
```dart
// lib/providers/premium_provider.dart

// Descomentar líneas 77-80
final pricingInfoProvider = FutureProvider<SubscriptionPricingInfo?>((ref) async {
  final manager = ref.watch(premiumSubscriptionManagerProvider);
  return await manager.getPricingInfo();
});

// Implementar en lib/services/premium_subscription_manager.dart
Future<SubscriptionPricingInfo> getPricingInfo() async {
  try {
    final offerings = await RevenueCatIntegration.getOfferings();

    return SubscriptionPricingInfo(
      monthlyPrice: offerings.current?.monthly?.product.priceString ?? '\$6.99',
      yearlyPrice: offerings.current?.annual?.product.priceString ?? '\$49.99',
      lifetimePrice: offerings.current?.lifetime?.product.priceString ?? '\$49.99',
      currency: offerings.current?.monthly?.product.currencyCode ?? 'USD',
    );
  } catch (e) {
    // Fallback a precios default
    return SubscriptionPricingInfo.defaults();
  }
}
```

**Testing**:
```dart
// test/providers/premium_provider_test.dart
test('pricingInfoProvider returns real prices', () async {
  final container = ProviderContainer();
  final pricing = await container.read(pricingInfoProvider.future);

  expect(pricing, isNotNull);
  expect(pricing!.monthlyPrice, isNot('TODO'));
});
```

---

## 🟠 FASE 1: GOAL PLANNER FLUTTER (SEMANA 1)

### 1.1 Backend Validation ✅
**Status**: COMPLETADO
- ✅ Backend deployed
- ✅ Endpoints funcionando
- ✅ OpenAI integrado
- ✅ Database schema creada

### 1.2 Flutter Models
**Tiempo**: 30 minutos

**Crear archivos**:

**`lib/models/goal.dart`**:
```dart
class Goal {
  final String goalId;
  final String userId;
  final ZodiacSign zodiacSign;
  final FocusArea focusArea;
  final String objective;
  final MainGoal mainGoal;
  final WeeklyFocus weeklyFocus;
  final List<MicroHabit> microHabits;
  final List<String> successIndicators;
  final List<Obstacle> potentialObstacles;
  final String motivationalMessage;
  final GoalStatus status;
  final DateTime createdAt;

  Goal({
    required this.goalId,
    required this.userId,
    required this.zodiacSign,
    required this.focusArea,
    required this.objective,
    required this.mainGoal,
    required this.weeklyFocus,
    required this.microHabits,
    required this.successIndicators,
    required this.potentialObstacles,
    required this.motivationalMessage,
    required this.status,
    required this.createdAt,
  });

  factory Goal.fromJson(Map<String, dynamic> json) {
    return Goal(
      goalId: json['goalId'] ?? json['goal_id'],
      userId: json['userId'] ?? json['user_id'],
      zodiacSign: ZodiacSign.values.firstWhere(
        (s) => s.name == (json['zodiacSign'] ?? json['zodiac_sign']),
      ),
      focusArea: FocusArea.values.firstWhere(
        (f) => f.name == (json['focusArea'] ?? json['focus_area']),
      ),
      objective: json['objective'],
      mainGoal: MainGoal.fromJson(json['mainGoal'] ?? json['main_goal']),
      weeklyFocus: WeeklyFocus.fromJson(json['weeklyFocus'] ?? json['weekly_focus']),
      microHabits: (json['microHabits'] ?? json['micro_habits'] as List)
          .map((h) => MicroHabit.fromJson(h))
          .toList(),
      successIndicators: List<String>.from(
        json['successIndicators'] ?? json['success_indicators'] ?? [],
      ),
      potentialObstacles: (json['potentialObstacles'] ?? json['potential_obstacles'] as List)
          .map((o) => Obstacle.fromJson(o))
          .toList(),
      motivationalMessage: json['motivationalMessage'] ?? json['motivational_message'],
      status: GoalStatus.values.firstWhere(
        (s) => s.name == json['status'],
        orElse: () => GoalStatus.active,
      ),
      createdAt: DateTime.parse(json['createdAt'] ?? json['created_at']),
    );
  }
}

enum FocusArea {
  career,
  relationships,
  wellness,
  personal_growth,
}

enum GoalStatus {
  active,
  completed,
  archived,
}

class MainGoal {
  final String title;
  final String why;
  final String specific;
  final String measurable;
  final String achievable;
  final String relevant;
  final String timeBound;

  MainGoal({
    required this.title,
    required this.why,
    required this.specific,
    required this.measurable,
    required this.achievable,
    required this.relevant,
    required this.timeBound,
  });

  factory MainGoal.fromJson(Map<String, dynamic> json) {
    return MainGoal(
      title: json['title'],
      why: json['why'],
      specific: json['specific'],
      measurable: json['measurable'],
      achievable: json['achievable'],
      relevant: json['relevant'],
      timeBound: json['timeBound'] ?? json['time_bound'],
    );
  }
}

class WeeklyFocus {
  final String theme;
  final List<String> keyActions;
  final String astroTiming;

  WeeklyFocus({
    required this.theme,
    required this.keyActions,
    required this.astroTiming,
  });

  factory WeeklyFocus.fromJson(Map<String, dynamic> json) {
    return WeeklyFocus(
      theme: json['theme'],
      keyActions: List<String>.from(json['keyActions'] ?? json['key_actions'] ?? []),
      astroTiming: json['astroTiming'] ?? json['astro_timing'],
    );
  }
}

class MicroHabit {
  final String habit;
  final String when;
  final String why;
  final String difficulty;

  MicroHabit({
    required this.habit,
    required this.when,
    required this.why,
    required this.difficulty,
  });

  factory MicroHabit.fromJson(Map<String, dynamic> json) {
    return MicroHabit(
      habit: json['habit'],
      when: json['when'],
      why: json['why'],
      difficulty: json['difficulty'],
    );
  }
}

class Obstacle {
  final String obstacle;
  final String solution;

  Obstacle({
    required this.obstacle,
    required this.solution,
  });

  factory Obstacle.fromJson(Map<String, dynamic> json) {
    return Obstacle(
      obstacle: json['obstacle'],
      solution: json['solution'],
    );
  }
}
```

---

### 1.3 Flutter Service
**Tiempo**: 45 minutos

**`lib/services/goal_planner_service.dart`**:
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:zodiac_app/models/goal.dart';
import 'package:zodiac_app/models/app_enums.dart';
import 'package:zodiac_app/utils/app_logger.dart';

class GoalPlannerService {
  static const String _baseUrl = 'https://zodiac-backend-api-production-8ded.up.railway.app';

  static GoalPlannerService? _instance;
  static GoalPlannerService get instance => _instance ??= GoalPlannerService._internal();

  GoalPlannerService._internal();

  /// Generate a new SMART goal using AI
  Future<Goal> generateGoal({
    required String userId,
    required ZodiacSign zodiacSign,
    required String objective,
    required FocusArea focusArea,
    String emotionalState = 'motivated',
    String timeframe = 'monthly',
    String languageCode = 'en',
  }) async {
    try {
      AppLogger.info('Generating goal for user $userId');

      final response = await http.post(
        Uri.parse('$_baseUrl/api/ai/goals'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'userId': userId,
          'zodiacSign': zodiacSign.name,
          'objective': objective,
          'emotionalState': emotionalState,
          'focusArea': focusArea.name,
          'timeframe': timeframe,
          'languageCode': languageCode,
        }),
      ).timeout(const Duration(seconds: 30));

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return Goal.fromJson(data['goal']);
      } else if (response.statusCode == 403) {
        throw Exception('Premium Stellar subscription required');
      } else {
        throw Exception('Failed to generate goal: ${response.body}');
      }
    } catch (e) {
      AppLogger.error('Error generating goal', e);
      rethrow;
    }
  }

  /// Get user's goals
  Future<List<Goal>> getUserGoals({
    required String userId,
    GoalStatus status = GoalStatus.active,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/ai/goals/$userId?status=${status.name}'),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return (data['goals'] as List)
            .map((g) => Goal.fromJson(g))
            .toList();
      } else {
        throw Exception('Failed to get goals: ${response.body}');
      }
    } catch (e) {
      AppLogger.error('Error getting goals', e);
      return [];
    }
  }

  /// Record a check-in
  Future<void> recordCheckIn({
    required String goalId,
    required String userId,
    required int progress,
    String? feedback,
    String? mood,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/ai/goals/$goalId/checkin'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'userId': userId,
          'progress': progress,
          'feedback': feedback,
          'mood': mood,
        }),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode != 200) {
        throw Exception('Failed to record check-in: ${response.body}');
      }
    } catch (e) {
      AppLogger.error('Error recording check-in', e);
      rethrow;
    }
  }

  /// Get goal analytics
  Future<Map<String, dynamic>> getAnalytics({
    required String userId,
    String timeframe = '30d',
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/ai/goals/$userId/analytics?timeframe=$timeframe'),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get analytics: ${response.body}');
      }
    } catch (e) {
      AppLogger.error('Error getting analytics', e);
      return {};
    }
  }

  /// Check service health
  Future<bool> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/ai/goals/health'),
      ).timeout(const Duration(seconds: 5));

      return response.statusCode == 200;
    } catch (e) {
      AppLogger.error('Goal Planner service unhealthy', e);
      return false;
    }
  }
}
```

---

### 1.4 Flutter UI Screens
**Tiempo**: 2-3 horas

**Crear archivos**:
1. `lib/screens/goal_planner/goal_planner_home_screen.dart` - Lista de metas
2. `lib/screens/goal_planner/goal_creation_wizard_screen.dart` - Wizard de creación
3. `lib/screens/goal_planner/goal_detail_screen.dart` - Detalle de meta
4. `lib/screens/goal_planner/goal_checkin_dialog.dart` - Check-in dialog
5. `lib/widgets/goal_card.dart` - Card para lista
6. `lib/widgets/progress_chart.dart` - Gráfico de progreso

**Ejemplo: Goal Planner Home Screen**:
```dart
// lib/screens/goal_planner/goal_planner_home_screen.dart

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:zodiac_app/services/goal_planner_service.dart';
import 'package:zodiac_app/services/user_identity_service.dart';
import 'package:zodiac_app/models/goal.dart';
import 'package:zodiac_app/widgets/goal_card.dart';

class GoalPlannerHomeScreen extends ConsumerStatefulWidget {
  const GoalPlannerHomeScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<GoalPlannerHomeScreen> createState() => _GoalPlannerHomeScreenState();
}

class _GoalPlannerHomeScreenState extends ConsumerState<GoalPlannerHomeScreen> {
  final _goalService = GoalPlannerService.instance;
  final _userIdentity = UserIdentityService();

  List<Goal> _goals = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadGoals();
  }

  Future<void> _loadGoals() async {
    setState(() => _loading = true);

    final userId = _userIdentity.getUserId();
    final goals = await _goalService.getUserGoals(userId: userId);

    setState(() {
      _goals = goals;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🎯 Goal Planner'),
        subtitle: const Text('Stellar Premium'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _goals.isEmpty
              ? _buildEmptyState()
              : _buildGoalsList(),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _navigateToCreateGoal(),
        icon: const Icon(Icons.add),
        label: const Text('New Goal'),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.track_changes, size: 80, color: Colors.grey),
          const SizedBox(height: 16),
          const Text('No goals yet', style: TextStyle(fontSize: 24)),
          const SizedBox(height: 8),
          const Text('Create your first SMART goal'),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () => _navigateToCreateGoal(),
            child: const Text('Create Goal'),
          ),
        ],
      ),
    );
  }

  Widget _buildGoalsList() {
    return RefreshIndicator(
      onRefresh: _loadGoals,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _goals.length,
        itemBuilder: (context, index) {
          return GoalCard(
            goal: _goals[index],
            onTap: () => _navigateToGoalDetail(_goals[index]),
          );
        },
      ),
    );
  }

  void _navigateToCreateGoal() {
    Navigator.pushNamed(context, '/goal-planner/create')
        .then((_) => _loadGoals());
  }

  void _navigateToGoalDetail(Goal goal) {
    Navigator.pushNamed(
      context,
      '/goal-planner/detail',
      arguments: goal,
    ).then((_) => _loadGoals());
  }
}
```

---

### 1.5 Premium Gate Integration
**Tiempo**: 20 minutos

**Agregar en `lib/screens/premium_screen.dart`**:
```dart
// Agregar botón de Goal Planner para usuarios Stellar

if (premiumTier == PremiumTier.stellar) {
  ListTile(
    leading: const Icon(Icons.track_changes, color: Colors.purple),
    title: const Text('🎯 Goal Planner'),
    subtitle: const Text('AI-powered SMART goals personalized to your sign'),
    trailing: const Icon(Icons.arrow_forward_ios),
    onTap: () {
      Navigator.pushNamed(context, '/goal-planner');
    },
  ),
}
```

**Agregar routes en `lib/main.dart`**:
```dart
routes: {
  '/goal-planner': (context) => const GoalPlannerHomeScreen(),
  '/goal-planner/create': (context) => const GoalCreationWizardScreen(),
  '/goal-planner/detail': (context) => const GoalDetailScreen(),
  // ...
}
```

---

### 1.6 Testing
**Tiempo**: 30 minutos

```bash
# Test service
flutter test test/services/goal_planner_service_test.dart

# Test models
flutter test test/models/goal_test.dart

# Integration test
flutter test integration_test/goal_planner_flow_test.dart
```

---

## 🟡 FASE 2: BACKEND CONSOLIDATION (SEMANA 1-2)

### 2.1 Backend Horoscope Service
**Archivos**: `backend_service.dart`, `horoscope_service.dart`
**Tiempo**: 60 minutos

**Problema**:
- TODOs en métodos híbridos (Railway + caché)
- Fallback no implementado

**Solución**:
```dart
// lib/services/backend_service.dart

Future<Horoscope> getDailyHoroscope(ZodiacSign sign) async {
  try {
    // 1. Try Railway API first
    final response = await http.get(
      Uri.parse('$_railwayUrl/api/coaching/getDailyHoroscope?sign=${sign.name}'),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final horoscope = Horoscope.fromJson(data);

      // Cache result
      await _cacheHoroscope(sign, horoscope);

      return horoscope;
    }
  } catch (e) {
    AppLogger.warning('Railway API failed, using cache', e);
  }

  // 2. Fallback to cache
  final cached = await _getCachedHoroscope(sign);
  if (cached != null && _isCacheValid(cached)) {
    return cached;
  }

  // 3. Last resort: Local generation
  return _generateLocalHoroscope(sign);
}

Future<void> _cacheHoroscope(ZodiacSign sign, Horoscope horoscope) async {
  final prefs = PreferencesService.instance;
  await prefs.setString(
    'horoscope_${sign.name}_${DateTime.now().toString().substring(0, 10)}',
    jsonEncode(horoscope.toJson()),
  );
}

Future<Horoscope?> _getCachedHoroscope(ZodiacSign sign) async {
  final prefs = PreferencesService.instance;
  final key = 'horoscope_${sign.name}_${DateTime.now().toString().substring(0, 10)}';
  final json = await prefs.getString(key);

  if (json != null) {
    return Horoscope.fromJson(jsonDecode(json));
  }
  return null;
}

bool _isCacheValid(Horoscope horoscope) {
  final now = DateTime.now();
  final horoscopeDate = DateTime.parse(horoscope.date);

  return now.difference(horoscopeDate).inHours < 24;
}

Horoscope _generateLocalHoroscope(ZodiacSign sign) {
  // Fallback básico con mensajes genéricos
  return Horoscope(
    sign: sign,
    date: DateTime.now().toString(),
    content: 'Today is a day of reflection and growth for ${sign.name}...',
    luckyNumbers: [7, 14, 21],
    luckyColor: 'Blue',
  );
}
```

---

### 2.2 Offline Mode Service
**Archivo**: `lib/services/offline_mode_service.dart`
**Tiempo**: 40 minutos

**Completar método**:
```dart
Future<void> _clearAllCaches() async {
  final prefs = PreferencesService.instance;

  // Clear horoscope caches
  final keys = await prefs.getAllKeys();
  for (final key in keys) {
    if (key.startsWith('horoscope_') ||
        key.startsWith('weekly_') ||
        key.startsWith('compatibility_')) {
      await prefs.remove(key);
    }
  }

  AppLogger.info('All caches cleared');
}

Future<void> syncWhenOnline() async {
  if (!await _isOnline()) return;

  // Sync pending actions
  final pendingActions = await _getPendingActions();

  for (final action in pendingActions) {
    try {
      await _executeAction(action);
      await _removePendingAction(action);
    } catch (e) {
      AppLogger.error('Failed to sync action', e);
    }
  }
}
```

---

## 🟢 FASE 3: FEATURES PREMIUM ROADMAP (SEMANA 2-3)

### 3.1 Astrological Timing for Goals
**Tiempo**: 90 minutos

**Backend**: Agregar timing service
```javascript
// backend/src/services/astrologicalTimingForGoals.js

class AstrologicalTimingForGoals {
  getBestDaysForAction(zodiacSign, focusArea, startDate, endDate) {
    // Calcular tránsitos planetarios
    const transits = this.calculateTransits(startDate, endDate);

    // Filtrar por signo y área
    const relevantTransits = transits.filter(t =>
      this.isRelevantFor(t, zodiacSign, focusArea)
    );

    // Retornar mejores días con score
    return relevantTransits.map(t => ({
      date: t.date,
      planet: t.planet,
      aspect: t.aspect,
      score: t.favorability,
      reason: this.generateReason(t, focusArea)
    }));
  }
}
```

**Flutter**: Mostrar en Goal Detail
```dart
// Agregar widget de timing
class AstroTimingWidget extends StatelessWidget {
  final WeeklyFocus weeklyFocus;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('⭐ Cosmic Timing', style: TextStyle(fontSize: 18)),
            const SizedBox(height: 8),
            Text(weeklyFocus.astroTiming),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _showDetailedTiming(),
              child: const Text('View Detailed Timing'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

### 3.2 PDF Report Generation
**Tiempo**: 2 horas

**Backend**: Agregar PDF service
```javascript
// backend/src/services/pdfReportService.js

const PDFDocument = require('pdfkit');

class PDFReportService {
  async generateWeeklyReport(userId, goalId) {
    const goal = await this.getGoal(goalId);
    const checkIns = await this.getCheckIns(goalId);

    const doc = new PDFDocument();

    // Header
    doc.fontSize(20).text('Weekly Goal Report', { align: 'center' });
    doc.moveDown();

    // Goal summary
    doc.fontSize(16).text('Goal: ' + goal.mainGoal.title);
    doc.fontSize(12).text('Progress: ' + this.calculateProgress(checkIns) + '%');

    // Charts
    await this.addProgressChart(doc, checkIns);

    // Recommendations
    doc.addPage();
    doc.fontSize(14).text('Astrological Recommendations');
    doc.fontSize(12).text(goal.weeklyFocus.astroTiming);

    return doc;
  }
}
```

---

### 3.3 Push Notifications for Micro-Habits
**Tiempo**: 90 minutos

**Implementar scheduler**:
```dart
// lib/services/goal_notification_scheduler.dart

class GoalNotificationScheduler {
  Future<void> scheduleMicroHabitReminders(Goal goal) async {
    final notificationService = UnifiedNotificationService();

    for (var i = 0; i < goal.microHabits.length; i++) {
      final habit = goal.microHabits[i];

      // Schedule based on "when" trigger
      final scheduledTime = _parseWhenToTime(habit.when);

      await notificationService.scheduleNotification(
        id: '${goal.goalId}_habit_$i'.hashCode,
        title: '🎯 Micro-Habit Reminder',
        body: habit.habit,
        scheduledDate: scheduledTime,
        payload: jsonEncode({
          'type': 'micro_habit',
          'goalId': goal.goalId,
          'habitIndex': i,
        }),
      );
    }
  }

  DateTime _parseWhenToTime(String when) {
    // Parse "First thing every morning" → 8:00 AM
    // Parse "End of each workday" → 6:00 PM
    // etc.

    if (when.contains('morning')) {
      return DateTime.now().add(const Duration(days: 1)).copyWith(hour: 8, minute: 0);
    } else if (when.contains('workday') || when.contains('end of day')) {
      return DateTime.now().add(const Duration(days: 1)).copyWith(hour: 18, minute: 0);
    }

    // Default: tomorrow at 9 AM
    return DateTime.now().add(const Duration(days: 1)).copyWith(hour: 9, minute: 0);
  }
}
```

---

## 🔵 FASE 4: OPTIMIZATIONS (SEMANA 3-4)

### 4.1 Redis Caching for Goals
**Backend**: Agregar Redis layer
```javascript
// backend/src/services/goalPlannerService.js

async generateGoals(params) {
  const cacheKey = `goal_${params.userId}_${params.focusArea}_${params.zodiacSign}`;

  // Check cache first
  const cached = await redisService.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Generate with OpenAI
  const goal = await this._generateWithAI(params);

  // Cache for 7 days
  await redisService.setex(cacheKey, 7 * 24 * 60 * 60, JSON.stringify(goal));

  return goal;
}
```

---

### 4.2 A/B Testing for Prompts
**Backend**: Track prompt performance
```javascript
// backend/src/services/goalPlannerService.js

_buildGoalPrompt(params) {
  // A/B test: 50% get version A, 50% get version B
  const promptVersion = Math.random() > 0.5 ? 'A' : 'B';

  const prompt = promptVersion === 'A'
    ? this._buildPromptV1(params)
    : this._buildPromptV2(params);

  // Track which version was used
  this._trackPromptVersion(params.userId, promptVersion);

  return prompt;
}
```

---

## 📅 TIMELINE & PRIORITIES

### Semana 1 (Oct 8-14)
**Día 1-2**: CRÍTICOS (Fase 0)
- [ ] Notificaciones reales
- [ ] UserID anónimo fix
- [ ] Pricing provider

**Día 3-5**: Goal Planner Flutter
- [ ] Models y service
- [ ] UI screens básicas
- [ ] Integration testing

### Semana 2 (Oct 15-21)
**Día 1-3**: Backend consolidation
- [ ] Horoscope service fallbacks
- [ ] Offline mode complete

**Día 4-5**: Goal Planner enhancements
- [ ] Astrological timing
- [ ] Notifications

### Semana 3 (Oct 22-28)
**Día 1-3**: Premium features
- [ ] PDF reports
- [ ] Analytics dashboard

**Día 4-5**: Testing & polish
- [ ] E2E testing
- [ ] Performance optimization

### Semana 4 (Oct 29+)
**Maintenance & monitoring**
- [ ] Monitor KPIs
- [ ] User feedback iteration
- [ ] Bug fixes

---

## 📊 SUCCESS METRICS

### Goal Planner KPIs
- **Activation**: 40% de usuarios Stellar crean goal en 7 días
- **Engagement**: 4+ check-ins promedio por usuario en 14 días
- **Conversion**: 15% Cosmic → Stellar atribuido a Goal Planner
- **Satisfaction**: NPS > 70

### Technical KPIs
- **Uptime**: > 99.5%
- **API Response Time**: < 3s para goal generation
- **Error Rate**: < 0.1%
- **OpenAI Cost**: < $50/mes

### App Store KPIs
- **Crash-free sessions**: > 99.9%
- **ANR rate**: < 0.1%
- **Startup time**: < 2s
- **Rating**: > 4.5 stars

---

## 🔧 TOOLS & COMMANDS

### Testing
```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/services/goal_planner_service_test.dart

# Integration tests
flutter test integration_test/

# Coverage report
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

### Backend
```bash
# Local backend
cd backend/flutter-horoscope-backend
npm start

# Test Goal Planner
node test-goal-planner.js

# Railway logs
railway logs

# Railway redeploy
railway redeploy --service zodiac-backend-api --yes
```

### Flutter Build
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

---

## 📚 DOCUMENTATION REFERENCE

### Existing Docs
- `DEPLOYMENT_SUCCESS.md` - Goal Planner deployment
- `GOAL_PLANNER_IMPLEMENTATION.md` - Technical details
- `TODO_EXECUTION_PLAN_OPTIMIZED.md` - Original TODOs
- `APP_STORE_SUBMISSION_READY.md` - App Store checklist

### Code Reference
- Backend: `backend/flutter-horoscope-backend/`
- Flutter: `zodiac_app/lib/`
- Models: `zodiac_app/lib/models/`
- Services: `zodiac_app/lib/services/`

---

## ✅ DAILY CHECKLIST

### Morning (9:00 AM)
- [ ] Check Railway health
- [ ] Review error logs
- [ ] Triage new issues

### Work Session
- [ ] Pick task from current phase
- [ ] Write test first
- [ ] Implement feature
- [ ] Run tests
- [ ] Commit with descriptive message

### Evening (6:00 PM)
- [ ] Deploy if needed
- [ ] Update this plan
- [ ] Document blockers
- [ ] Plan tomorrow

---

**Este plan está vivo y debe actualizarse diariamente.**
**Prioridad: Fase 0 (Críticos) PRIMERO, luego Goal Planner Flutter.**

🎯 **Next Action**: Empezar con 0.1 (Notificaciones Reales)
