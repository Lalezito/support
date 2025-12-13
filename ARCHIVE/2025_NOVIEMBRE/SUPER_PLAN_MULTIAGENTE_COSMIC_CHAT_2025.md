# SUPER PLAN MULTI-AGENTE: COSMIC COACH CHAT 2.0

## Fecha: 28 Noviembre 2025
## Versión: 1.0
## Estado: APROBADO PARA EJECUCIÓN

---

## RESUMEN EJECUTIVO

Plan de mejoras del Cosmic Coach Chat con **8 agentes especializados** trabajando en paralelo para lograr:

| Métrica | Actual (Estimado) | Objetivo | Delta |
|---------|-------------------|----------|-------|
| Mensajes/sesión | ~3-4 | 5+ | +25% |
| Retención semanal | ~45% | 52%+ | +15% |
| NPS del módulo | ~35 | 45+ | +10pts |
| Errores backend/chat | ~3% | <1% | -66% |

---

## ARQUITECTURA MULTI-AGENTE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORQUESTADOR PRINCIPAL                                │
│                    (Coordina 8 agentes especializados)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   AGENTE 1    │          │   AGENTE 2    │          │   AGENTE 3    │
│   ANALYTICS   │          │   UX/INPUT    │          │   AI ENGINE   │
│   & METRICS   │          │   OPTIMIZER   │          │   ENHANCER    │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   AGENTE 4    │          │   AGENTE 5    │          │   AGENTE 6    │
│   PERSONAL-   │          │   OBSERVAB.   │          │   QUICK REPLY │
│   IZATION     │          │   & LOGS      │          │   SMART       │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐
│   AGENTE 7    │          │   AGENTE 8    │
│   HISTORY &   │          │   QA & L10N   │
│   FAVORITES   │          │   TESTING     │
└───────────────┘          └───────────────┘
```

---

## AGENTE 1: ANALYTICS & TELEMETRÍA

### Responsabilidad
Instrumentación de métricas y establecimiento de línea base.

### Archivos Objetivo
```
zodiac_app/lib/services/horoscope_chat_service.dart (líneas 23-69)
zodiac_app/lib/services/consolidated_analytics/core_analytics_service.dart
zodiac_app/lib/services/consolidated_analytics/user_analytics_service.dart
```

### Tareas

#### 1.1 Auditoría de Flujos Actuales
```dart
// Documentar KPIs existentes:
// - dailyUsage / dailyLimit (línea 240-329)
// - source tracking (template/cache/backend)
// - latencia (_recentLatencies, líneas 62-68)
```

#### 1.2 Nuevos Eventos de Telemetría
```dart
// Archivo: horoscope_chat_service.dart
// Agregar después de línea 69:

class ChatAnalyticsEvent {
  static const String chatOpened = 'cosmic_chat_opened';
  static const String messageSent = 'cosmic_chat_message_sent';
  static const String responseReceived = 'cosmic_chat_response_received';
  static const String quickReplyUsed = 'cosmic_chat_quick_reply_used';
  static const String sessionStarted = 'cosmic_chat_session_started';
  static const String errorOccurred = 'cosmic_chat_error';
}

// Implementar tracking en sendMessage():
void _trackMessageEvent({
  required String userId,
  required String zodiacSign,
  required String language,
  required String source, // template/cache/backend
  required String category,
  required int latencyMs,
  String? error,
}) {
  CoreAnalyticsService.instance.trackEvent(
    ChatAnalyticsEvent.messageSent,
    parameters: {
      'user_id': userId,
      'zodiac_sign': zodiacSign,
      'language': language,
      'response_source': source,
      'category': category,
      'latency_ms': latencyMs,
      'tier': _currentTier.name,
      'session_message_count': _sessionMessageCount,
      'timestamp': DateTime.now().toIso8601String(),
    },
  );
}
```

#### 1.3 Dashboard de Métricas
```dart
// Crear provider para estadísticas de chat
final chatStatsProvider = FutureProvider<ChatStats>((ref) async {
  final service = ref.watch(horoscopeChatServiceProvider);
  return ChatStats(
    totalMessages: service.state.messages.length,
    dailyUsage: service.state.dailyUsage,
    dailyLimit: service.state.dailyLimit,
    avgLatency: service._getAverageLatency(),
    cacheHitRate: service._getCacheHitRate(),
    backendSuccessRate: service._getBackendSuccessRate(),
  );
});
```

### Entregables
- [ ] Clase `ChatAnalyticsEvent` con constantes de eventos
- [ ] Método `_trackMessageEvent()` integrado en flujo
- [ ] Provider `chatStatsProvider` para dashboard
- [ ] Reporte de línea base (últimos 30 días)

### Dependencias
- CoreAnalyticsService.instance
- UserAnalyticsService.instance

---

## AGENTE 2: UX/INPUT OPTIMIZER

### Responsabilidad
Mejorar la experiencia de entrada de mensajes y sugerencias contextuales.

### Archivos Objetivo
```
zodiac_app/lib/screens/cosmic_coach_chat_screen.dart (líneas 599-755)
zodiac_app/lib/widgets/chat/chat_input_widget.dart
zodiac_app/lib/widgets/chat/smart_reply_chips.dart
```

### Tareas

#### 2.1 Input Contextual Inteligente
```dart
// Archivo: chat_input_widget.dart
// Nuevo widget con sugerencias adaptadas

class SmartChatInputWidget extends ConsumerStatefulWidget {
  final Function(String) onSendMessage;
  final HoroscopeChatState chatState;
  final String zodiacSign;
  final String? userMood; // Estado emocional opcional

  // Sugerencias dinámicas basadas en:
  // 1. Categoría del último mensaje
  // 2. Estado emocional del usuario
  // 3. Metas activas del usuario
  // 4. Fase lunar actual

  List<String> _getContextualSuggestions() {
    final lastCategory = _getLastMessageCategory();
    final mood = userMood ?? 'neutral';

    return switch (lastCategory) {
      HoroscopeQuestionCategory.dailyGuidance => [
        '¿Cómo puedo aprovechar mejor esta energía?',
        '¿Qué debo evitar hoy?',
        'Dame un consejo específico para mi trabajo',
      ],
      HoroscopeQuestionCategory.loveCompatibility => [
        '¿Qué puedo hacer para mejorar mi relación?',
        '¿Cuál es mi mejor momento para el amor hoy?',
        '¿Cómo puedo conectar mejor con mi pareja?',
      ],
      HoroscopeQuestionCategory.careerTiming => [
        '¿Es buen momento para pedir un aumento?',
        '¿Qué oportunidades debo buscar?',
        '¿Cómo puedo destacar en mi trabajo?',
      ],
      _ => _getDefaultSuggestions(),
    };
  }
}
```

#### 2.2 Selector de Modo de Conversación
```dart
// Archivo: cosmic_coach_chat_screen.dart
// Agregar después de línea 470

enum ConversationMode {
  general('General', Icons.auto_awesome),
  wellness('Bienestar', Icons.spa),
  career('Carrera', Icons.work),
  love('Amor', Icons.favorite),
  spirituality('Espiritualidad', Icons.self_improvement);

  final String label;
  final IconData icon;
  const ConversationMode(this.label, this.icon);
}

// Widget selector de modo
Widget _buildModeSelector(String languageCode) {
  return Consumer(
    builder: (context, ref, child) {
      final currentMode = ref.watch(conversationModeProvider);

      return Container(
        height: 40,
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: ConversationMode.values.length,
          itemBuilder: (context, index) {
            final mode = ConversationMode.values[index];
            final isSelected = mode == currentMode;

            return Padding(
              padding: EdgeInsets.only(right: 8),
              child: FilterChip(
                selected: isSelected,
                avatar: Icon(mode.icon, size: 16),
                label: Text(mode.label),
                onSelected: (selected) {
                  ref.read(conversationModeProvider.notifier).state = mode;
                },
              ),
            );
          },
        ),
      );
    },
  );
}

// Provider para el modo
final conversationModeProvider = StateProvider<ConversationMode>((ref) {
  return ConversationMode.general;
});
```

#### 2.3 Empty State Personalizado
```dart
// Archivo: chat_history_widget_riverpod.dart (líneas 516-579)
// Mejorar ChatEmptyState

class PersonalizedEmptyState extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final prefs = ref.watch(preferencesServiceProvider);
    final zodiacSign = prefs.userZodiacSign ?? 'Aries';
    final language = prefs.userLanguage;
    final lastGoal = prefs.lastActiveGoal; // Nuevo campo

    // Sugerencias personalizadas
    final suggestions = _getPersonalizedSuggestions(
      zodiacSign: zodiacSign,
      language: language,
      lastGoal: lastGoal,
    );

    return ChatEmptyState(
      title: _getPersonalizedTitle(zodiacSign, language),
      subtitle: _getPersonalizedSubtitle(language),
      suggestions: suggestions,
      onSuggestionTap: (suggestion) => _handleSuggestion(suggestion, ref),
    );
  }

  List<String> _getPersonalizedSuggestions({
    required String zodiacSign,
    required String language,
    String? lastGoal,
  }) {
    final base = [
      '¿Cómo será mi día como $zodiacSign?',
      '¿Qué energía cósmica me acompaña hoy?',
    ];

    if (lastGoal != null) {
      base.insert(0, '¿Cómo puedo avanzar en: $lastGoal?');
    }

    return base;
  }
}
```

### Entregables
- [ ] SmartChatInputWidget con sugerencias contextuales
- [ ] Selector de modo de conversación (ConversationMode)
- [ ] PersonalizedEmptyState basado en preferencias
- [ ] Animaciones de transición entre modos

### Dependencias
- PreferencesService
- HoroscopeChatService state

---

## AGENTE 3: AI ENGINE ENHANCER

### Responsabilidad
Mejorar el motor de IA y la generación de respuestas híbridas.

### Archivos Objetivo
```
zodiac_app/lib/services/horoscope_chat_service.dart (líneas 417-548, 218-299)
zodiac_app/lib/models/horoscope_chat_models.dart
```

### Tareas

#### 3.1 Unificación de Sesión con Reconexión
```dart
// Archivo: horoscope_chat_service.dart
// Refactorizar _startSession y _callBackend (líneas 417-548)

Future<HoroscopeResponse> _callBackendWithRetry({
  required String message,
  required String userId,
  required String zodiacSign,
  required String language,
  required HoroscopeQuestionCategory category,
  int maxRetries = 2,
}) async {
  int attempts = 0;
  Exception? lastError;

  while (attempts < maxRetries) {
    try {
      // Si la sesión expiró, crear una nueva
      if (_sessionExpired || _currentSessionId == null) {
        _currentSessionId = await _startSession(
          userId: userId,
          zodiacSign: zodiacSign,
          language: language,
        );
      }

      return await _callBackend(
        message: message,
        userId: userId,
        zodiacSign: zodiacSign,
        language: language,
        category: category,
      );

    } on SessionExpiredException {
      _log('🔄 Session expired, refreshing...');
      _currentSessionId = null;
      attempts++;
    } on TimeoutException catch (e) {
      _log('⏱️ Timeout on attempt $attempts: $e');
      lastError = e;
      attempts++;
      _adjustTimeoutOnFailure();
    } catch (e) {
      lastError = e as Exception;
      attempts++;
    }
  }

  throw lastError ?? Exception('Max retries exceeded');
}

// Verificar si la sesión expiró
bool get _sessionExpired {
  if (_sessionStartTime == null) return true;
  return DateTime.now().difference(_sessionStartTime!) > const Duration(hours: 1);
}
```

#### 3.2 Prompt Modular con Contexto Enriquecido
```dart
// Archivo: horoscope_chat_models.dart
// Nuevo modelo para contexto de prompt

class EnrichedContext extends HoroscopeContext {
  final String? currentMood;
  final List<String> activeGoals;
  final String? moonPhase;
  final int energyLevel; // 1-10
  final ConversationMode conversationMode;
  final List<String> previousTopics;

  const EnrichedContext({
    required super.userId,
    required super.zodiacSign,
    required super.language,
    this.currentMood,
    this.activeGoals = const [],
    this.moonPhase,
    this.energyLevel = 5,
    this.conversationMode = ConversationMode.general,
    this.previousTopics = const [],
    super.additionalData,
  });

  /// Generar prompt enriquecido para el backend
  String toPromptContext() {
    final buffer = StringBuffer();

    buffer.writeln('Usuario: Signo $zodiacSign');

    if (currentMood != null) {
      buffer.writeln('Estado emocional actual: $currentMood');
    }

    if (activeGoals.isNotEmpty) {
      buffer.writeln('Metas activas: ${activeGoals.join(", ")}');
    }

    if (moonPhase != null) {
      buffer.writeln('Fase lunar: $moonPhase');
    }

    buffer.writeln('Nivel de energía: $energyLevel/10');
    buffer.writeln('Modo de conversación: ${conversationMode.name}');

    if (previousTopics.isNotEmpty) {
      buffer.writeln('Temas previos: ${previousTopics.take(3).join(", ")}');
    }

    return buffer.toString();
  }
}
```

#### 3.3 Generación Híbrida Avanzada
```dart
// Archivo: horoscope_chat_service.dart
// Mejorar flujo híbrido (líneas 218-299)

Future<HoroscopeResponse> _generateHybridResponse({
  required String message,
  required CategoryMatch categoryMatch,
  required EnrichedContext context,
}) async {
  // 1. Obtener respuesta base del template (instantánea)
  final templateResponse = await _generateFromTemplate(
    categoryMatch.matchedTemplate ?? _getDefaultTemplate(),
    context,
  );

  // 2. Si la confianza es baja o el usuario es premium, enriquecer con AI
  final shouldEnrich = categoryMatch.confidence < 0.85 ||
                        _isPremiumUser ||
                        context.conversationMode != ConversationMode.general;

  if (!shouldEnrich) {
    return templateResponse;
  }

  try {
    // 3. Llamar al backend para enriquecer la respuesta
    final aiEnhancement = await _callBackendWithRetry(
      message: message,
      userId: context.userId,
      zodiacSign: context.zodiacSign,
      language: context.language,
      category: categoryMatch.category,
    );

    // 4. Mezclar respuestas: template abre, AI profundiza
    return _mergeResponses(templateResponse, aiEnhancement);

  } catch (e) {
    // Fallback al template si falla el backend
    _log('⚠️ AI enhancement failed, using template: $e');
    return templateResponse;
  }
}

HoroscopeResponse _mergeResponses(
  HoroscopeResponse template,
  HoroscopeResponse ai,
) {
  // Template provee estructura, AI provee profundidad
  final mergedContent = '''${template.content}

${ai.content}''';

  return HoroscopeResponse(
    content: mergedContent,
    category: ai.category,
    suggestedReplies: ai.suggestedReplies.isNotEmpty
        ? ai.suggestedReplies
        : template.suggestedReplies,
    relatedTopics: {...template.relatedTopics, ...ai.relatedTopics}.toList(),
    source: 'hybrid',
    timestamp: DateTime.now(),
    metadata: {
      ...?template.metadata,
      ...?ai.metadata,
      'hybrid': true,
    },
  );
}
```

### Entregables
- [ ] `_callBackendWithRetry()` con reconexión automática
- [ ] `EnrichedContext` con datos de perfil de usuario
- [ ] `_generateHybridResponse()` con mezcla template+AI
- [ ] Detección de sesión expirada

### Dependencias
- Backend API (Railway)
- PreferencesService (para datos de usuario)
- MoonPhase service (si existe)

---

## AGENTE 4: PERSONALIZATION ENGINE

### Responsabilidad
Integrar datos personales para enriquecer el contexto del chat.

### Archivos Objetivo
```
zodiac_app/lib/models/horoscope_chat_models.dart (líneas 296-318)
zodiac_app/lib/providers/consolidated_providers.dart (líneas 391-429)
zodiac_app/lib/services/preferences_service.dart
```

### Tareas

#### 4.1 Perfil de Usuario para Coaching
```dart
// Archivo: Nuevo - lib/models/coaching_profile.dart

import 'package:flutter/foundation.dart';

@immutable
class CoachingProfile {
  final String userId;
  final String zodiacSign;
  final DateTime? birthDate;
  final String? ascendant;
  final String? moonSign;

  // Estado emocional tracking
  final String? lastReportedMood;
  final DateTime? lastMoodUpdate;
  final List<String> moodHistory; // Últimos 7 días

  // Metas y progreso
  final List<ActiveGoal> activeGoals;
  final List<String> completedGoals;

  // Preferencias de coaching
  final CoachingStyle preferredStyle;
  final List<String> favoriteTopics;
  final bool receiveMotivationalReminders;

  // Estadísticas
  final int totalSessions;
  final int totalMessages;
  final DateTime? lastSessionDate;
  final double averageSessionLength; // en minutos

  const CoachingProfile({
    required this.userId,
    required this.zodiacSign,
    this.birthDate,
    this.ascendant,
    this.moonSign,
    this.lastReportedMood,
    this.lastMoodUpdate,
    this.moodHistory = const [],
    this.activeGoals = const [],
    this.completedGoals = const [],
    this.preferredStyle = CoachingStyle.balanced,
    this.favoriteTopics = const [],
    this.receiveMotivationalReminders = true,
    this.totalSessions = 0,
    this.totalMessages = 0,
    this.lastSessionDate,
    this.averageSessionLength = 0,
  });

  factory CoachingProfile.fromJson(Map<String, dynamic> json) {
    return CoachingProfile(
      userId: json['userId'] ?? '',
      zodiacSign: json['zodiacSign'] ?? 'Aries',
      birthDate: json['birthDate'] != null
          ? DateTime.parse(json['birthDate'])
          : null,
      ascendant: json['ascendant'],
      moonSign: json['moonSign'],
      lastReportedMood: json['lastReportedMood'],
      lastMoodUpdate: json['lastMoodUpdate'] != null
          ? DateTime.parse(json['lastMoodUpdate'])
          : null,
      moodHistory: List<String>.from(json['moodHistory'] ?? []),
      activeGoals: (json['activeGoals'] as List?)
          ?.map((g) => ActiveGoal.fromJson(g))
          .toList() ?? [],
      completedGoals: List<String>.from(json['completedGoals'] ?? []),
      preferredStyle: CoachingStyle.values.firstWhere(
        (s) => s.name == json['preferredStyle'],
        orElse: () => CoachingStyle.balanced,
      ),
      favoriteTopics: List<String>.from(json['favoriteTopics'] ?? []),
      receiveMotivationalReminders: json['receiveMotivationalReminders'] ?? true,
      totalSessions: json['totalSessions'] ?? 0,
      totalMessages: json['totalMessages'] ?? 0,
      lastSessionDate: json['lastSessionDate'] != null
          ? DateTime.parse(json['lastSessionDate'])
          : null,
      averageSessionLength: (json['averageSessionLength'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => {
    'userId': userId,
    'zodiacSign': zodiacSign,
    'birthDate': birthDate?.toIso8601String(),
    'ascendant': ascendant,
    'moonSign': moonSign,
    'lastReportedMood': lastReportedMood,
    'lastMoodUpdate': lastMoodUpdate?.toIso8601String(),
    'moodHistory': moodHistory,
    'activeGoals': activeGoals.map((g) => g.toJson()).toList(),
    'completedGoals': completedGoals,
    'preferredStyle': preferredStyle.name,
    'favoriteTopics': favoriteTopics,
    'receiveMotivationalReminders': receiveMotivationalReminders,
    'totalSessions': totalSessions,
    'totalMessages': totalMessages,
    'lastSessionDate': lastSessionDate?.toIso8601String(),
    'averageSessionLength': averageSessionLength,
  };

  CoachingProfile copyWith({
    String? userId,
    String? zodiacSign,
    DateTime? birthDate,
    String? ascendant,
    String? moonSign,
    String? lastReportedMood,
    DateTime? lastMoodUpdate,
    List<String>? moodHistory,
    List<ActiveGoal>? activeGoals,
    List<String>? completedGoals,
    CoachingStyle? preferredStyle,
    List<String>? favoriteTopics,
    bool? receiveMotivationalReminders,
    int? totalSessions,
    int? totalMessages,
    DateTime? lastSessionDate,
    double? averageSessionLength,
  }) {
    return CoachingProfile(
      userId: userId ?? this.userId,
      zodiacSign: zodiacSign ?? this.zodiacSign,
      birthDate: birthDate ?? this.birthDate,
      ascendant: ascendant ?? this.ascendant,
      moonSign: moonSign ?? this.moonSign,
      lastReportedMood: lastReportedMood ?? this.lastReportedMood,
      lastMoodUpdate: lastMoodUpdate ?? this.lastMoodUpdate,
      moodHistory: moodHistory ?? this.moodHistory,
      activeGoals: activeGoals ?? this.activeGoals,
      completedGoals: completedGoals ?? this.completedGoals,
      preferredStyle: preferredStyle ?? this.preferredStyle,
      favoriteTopics: favoriteTopics ?? this.favoriteTopics,
      receiveMotivationalReminders: receiveMotivationalReminders ?? this.receiveMotivationalReminders,
      totalSessions: totalSessions ?? this.totalSessions,
      totalMessages: totalMessages ?? this.totalMessages,
      lastSessionDate: lastSessionDate ?? this.lastSessionDate,
      averageSessionLength: averageSessionLength ?? this.averageSessionLength,
    );
  }
}

enum CoachingStyle {
  motivational,  // Enfocado en motivación y ánimo
  analytical,    // Enfocado en datos y análisis astrológico
  balanced,      // Mezcla equilibrada
  spiritual,     // Enfoque espiritual profundo
  practical,     // Consejos prácticos y accionables
}

@immutable
class ActiveGoal {
  final String id;
  final String title;
  final String category; // wellness, career, love, growth
  final DateTime createdAt;
  final DateTime? targetDate;
  final int progress; // 0-100
  final List<String> milestones;
  final int completedMilestones;

  const ActiveGoal({
    required this.id,
    required this.title,
    required this.category,
    required this.createdAt,
    this.targetDate,
    this.progress = 0,
    this.milestones = const [],
    this.completedMilestones = 0,
  });

  factory ActiveGoal.fromJson(Map<String, dynamic> json) {
    return ActiveGoal(
      id: json['id'] ?? '',
      title: json['title'] ?? '',
      category: json['category'] ?? 'growth',
      createdAt: DateTime.parse(json['createdAt'] ?? DateTime.now().toIso8601String()),
      targetDate: json['targetDate'] != null
          ? DateTime.parse(json['targetDate'])
          : null,
      progress: json['progress'] ?? 0,
      milestones: List<String>.from(json['milestones'] ?? []),
      completedMilestones: json['completedMilestones'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'title': title,
    'category': category,
    'createdAt': createdAt.toIso8601String(),
    'targetDate': targetDate?.toIso8601String(),
    'progress': progress,
    'milestones': milestones,
    'completedMilestones': completedMilestones,
  };
}
```

#### 4.2 Provider de Perfil de Coaching
```dart
// Archivo: consolidated_providers.dart
// Agregar después de línea 429

/// Provider para el perfil de coaching del usuario
final coachingProfileProvider = StateNotifierProvider<CoachingProfileNotifier, CoachingProfile?>((ref) {
  final prefs = ref.watch(preferencesServiceProvider);
  return CoachingProfileNotifier(prefs);
});

class CoachingProfileNotifier extends StateNotifier<CoachingProfile?> {
  final PreferencesService _prefs;

  CoachingProfileNotifier(this._prefs) : super(null) {
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    try {
      final json = await _prefs.getCoachingProfileJson();
      if (json != null) {
        state = CoachingProfile.fromJson(json);
      } else {
        // Crear perfil por defecto
        state = CoachingProfile(
          userId: _prefs.userId ?? 'anonymous',
          zodiacSign: _prefs.userZodiacSign ?? 'Aries',
          birthDate: _prefs.birthDate,
        );
      }
    } catch (e) {
      state = CoachingProfile(
        userId: 'anonymous',
        zodiacSign: 'Aries',
      );
    }
  }

  Future<void> updateMood(String mood) async {
    if (state == null) return;

    final newHistory = [...state!.moodHistory.take(6), mood];
    state = state!.copyWith(
      lastReportedMood: mood,
      lastMoodUpdate: DateTime.now(),
      moodHistory: newHistory,
    );

    await _saveProfile();
  }

  Future<void> addGoal(ActiveGoal goal) async {
    if (state == null) return;

    state = state!.copyWith(
      activeGoals: [...state!.activeGoals, goal],
    );

    await _saveProfile();
  }

  Future<void> updateGoalProgress(String goalId, int progress) async {
    if (state == null) return;

    final updatedGoals = state!.activeGoals.map((g) {
      if (g.id == goalId) {
        return ActiveGoal(
          id: g.id,
          title: g.title,
          category: g.category,
          createdAt: g.createdAt,
          targetDate: g.targetDate,
          progress: progress,
          milestones: g.milestones,
          completedMilestones: g.completedMilestones,
        );
      }
      return g;
    }).toList();

    state = state!.copyWith(activeGoals: updatedGoals);
    await _saveProfile();
  }

  Future<void> completeGoal(String goalId) async {
    if (state == null) return;

    final goal = state!.activeGoals.firstWhere((g) => g.id == goalId);
    final remaining = state!.activeGoals.where((g) => g.id != goalId).toList();

    state = state!.copyWith(
      activeGoals: remaining,
      completedGoals: [...state!.completedGoals, goal.title],
    );

    await _saveProfile();
  }

  Future<void> setPreferredStyle(CoachingStyle style) async {
    if (state == null) return;

    state = state!.copyWith(preferredStyle: style);
    await _saveProfile();
  }

  Future<void> incrementSessionStats() async {
    if (state == null) return;

    state = state!.copyWith(
      totalSessions: state!.totalSessions + 1,
      lastSessionDate: DateTime.now(),
    );

    await _saveProfile();
  }

  Future<void> _saveProfile() async {
    if (state == null) return;
    await _prefs.saveCoachingProfileJson(state!.toJson());
  }
}
```

#### 4.3 Categorizador Mejorado Multi-idioma
```dart
// Archivo: horoscope_chat_service.dart
// Mejorar _buildTemplates() con nuevos términos

// Agregar estos términos al template de carrerTiming:
final newCareerTerms = [
  // Español
  'burnout', 'trabajo remoto', 'home office', 'teletrabajo',
  'freelance', 'emprendimiento', 'startup', 'networking',
  'productividad', 'balance vida-trabajo', 'promoción',

  // English
  'remote work', 'side hustle', 'career change', 'job interview',
  'salary negotiation', 'professional growth', 'work-life balance',

  // German
  'homeoffice', 'beförderung', 'arbeit von zuhause',

  // French
  'télétravail', 'évolution professionnelle', 'reconversion',

  // Italian
  'lavoro da casa', 'crescita professionale',

  // Portuguese
  'trabalho remoto', 'crescimento profissional',
];

// Agregar nuevos términos de bienestar mental
final mentalWellnessTerms = [
  'ansiedad', 'estrés', 'meditación', 'mindfulness',
  'anxiety', 'stress', 'meditation', 'self-care',
  'angst', 'meditation', 'selbstfürsorge',
  'anxiété', 'méditation', 'bien-être',
  'ansia', 'meditazione', 'benessere',
  'ansiedade', 'meditação', 'bem-estar',
];
```

### Entregables
- [ ] Modelo `CoachingProfile` completo
- [ ] `CoachingProfileNotifier` con persistencia
- [ ] Provider `coachingProfileProvider`
- [ ] Términos nuevos para categorizador
- [ ] Integración con `EnrichedContext`

### Dependencias
- PreferencesService
- SharedPreferences

---

## AGENTE 5: OBSERVABILITY & RELIABILITY

### Responsabilidad
Implementar logging estructurado y trazabilidad end-to-end.

### Archivos Objetivo
```
zodiac_app/lib/services/horoscope_chat_service.dart (líneas 23-69)
zodiac_app/lib/utils/app_logger.dart
```

### Tareas

#### 5.1 Logging Estructurado Condicional
```dart
// Archivo: horoscope_chat_service.dart
// Mejorar sistema de logging

class StructuredChatLogger {
  final String sessionId;
  final String userId;
  final bool isEnabled;

  StructuredChatLogger({
    required this.sessionId,
    required this.userId,
    required this.isEnabled,
  });

  void logEvent(ChatLogEvent event) {
    if (!isEnabled) return;

    final logEntry = {
      'timestamp': DateTime.now().toIso8601String(),
      'session_id': sessionId,
      'user_id': userId,
      'event': event.type,
      'data': event.data,
      'latency_ms': event.latencyMs,
      'source': event.source,
    };

    // Log local (debug)
    if (kDebugMode) {
      debugPrint('[CosmicChat] ${jsonEncode(logEntry)}');
    }

    // Log remoto (producción)
    _sendToAnalytics(logEntry);
  }

  void logError(ChatLogEvent event, Object error, StackTrace? stack) {
    final errorEntry = {
      'timestamp': DateTime.now().toIso8601String(),
      'session_id': sessionId,
      'user_id': userId,
      'event': 'error',
      'error_type': error.runtimeType.toString(),
      'error_message': error.toString(),
      'stack_trace': stack?.toString().split('\n').take(5).join('\n'),
      'context': event.data,
    };

    // Siempre log errores
    debugPrint('[CosmicChat ERROR] ${jsonEncode(errorEntry)}');

    // Enviar a Crashlytics
    _sendToCrashlytics(errorEntry);
  }

  void _sendToAnalytics(Map<String, dynamic> entry) {
    CoreAnalyticsService.instance.trackEvent(
      'cosmic_chat_log',
      parameters: entry,
    );
  }

  void _sendToCrashlytics(Map<String, dynamic> entry) {
    // Integración con Firebase Crashlytics
    // FirebaseCrashlytics.instance.log(jsonEncode(entry));
  }
}

class ChatLogEvent {
  final String type;
  final Map<String, dynamic> data;
  final int? latencyMs;
  final String? source;

  const ChatLogEvent({
    required this.type,
    this.data = const {},
    this.latencyMs,
    this.source,
  });
}
```

#### 5.2 Tracing End-to-End
```dart
// Archivo: horoscope_chat_service.dart
// Agregar IDs de trazabilidad

class ChatTraceContext {
  final String traceId;      // ID único por mensaje
  final String sessionId;    // ID de sesión de chat
  final String spanId;       // ID de operación específica
  final DateTime startTime;

  ChatTraceContext({
    String? traceId,
    required this.sessionId,
    String? spanId,
  }) : traceId = traceId ?? _generateTraceId(),
       spanId = spanId ?? _generateSpanId(),
       startTime = DateTime.now();

  static String _generateTraceId() {
    return 'tr_${DateTime.now().millisecondsSinceEpoch}_${math.Random().nextInt(9999)}';
  }

  static String _generateSpanId() {
    return 'sp_${math.Random().nextInt(99999)}';
  }

  int get elapsedMs => DateTime.now().difference(startTime).inMilliseconds;

  Map<String, String> toHeaders() => {
    'X-Trace-Id': traceId,
    'X-Session-Id': sessionId,
    'X-Span-Id': spanId,
  };

  @override
  String toString() => '[$traceId/$spanId]';
}

// Uso en _callBackend:
Future<HoroscopeResponse> _callBackend({
  required String message,
  required String userId,
  required String zodiacSign,
  required String language,
  required HoroscopeQuestionCategory category,
}) async {
  final trace = ChatTraceContext(sessionId: _currentSessionId ?? 'unknown');

  _log('${trace} Starting backend call for category: ${category.name}');

  try {
    final response = await _httpClient.post(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...trace.toHeaders(), // Agregar headers de tracing
      },
      body: jsonEncode({
        'sessionId': _currentSessionId,
        'message': message,
        'traceId': trace.traceId, // Incluir en payload
        // ...
      }),
    ).timeout(_requestTimeout);

    _log('${trace} Backend response received in ${trace.elapsedMs}ms');

    // ... resto del código

  } catch (e, stack) {
    _logger.logError(
      ChatLogEvent(
        type: 'backend_error',
        data: {
          'trace_id': trace.traceId,
          'category': category.name,
          'latency_ms': trace.elapsedMs,
        },
      ),
      e,
      stack,
    );
    rethrow;
  }
}
```

#### 5.3 Configuración de Alertas
```dart
// Archivo: Nuevo - lib/services/chat_monitoring_service.dart

class ChatMonitoringService {
  static final instance = ChatMonitoringService._();
  ChatMonitoringService._();

  // Métricas en memoria para alertas
  final List<int> _recentLatencies = [];
  int _fallbackCount = 0;
  int _totalRequests = 0;
  DateTime? _windowStart;

  // Umbrales de alerta
  static const int latencyThresholdMs = 5000;
  static const double fallbackRateThreshold = 0.3; // 30%
  static const Duration monitoringWindow = Duration(minutes: 5);

  void recordRequest({
    required int latencyMs,
    required bool usedFallback,
    required String source,
  }) {
    _checkWindowReset();

    _recentLatencies.add(latencyMs);
    _totalRequests++;
    if (usedFallback) _fallbackCount++;

    // Verificar umbrales
    _checkAlerts();
  }

  void _checkWindowReset() {
    if (_windowStart == null ||
        DateTime.now().difference(_windowStart!) > monitoringWindow) {
      _windowStart = DateTime.now();
      _recentLatencies.clear();
      _fallbackCount = 0;
      _totalRequests = 0;
    }
  }

  void _checkAlerts() {
    // Alerta de latencia alta
    if (_recentLatencies.isNotEmpty) {
      final avgLatency = _recentLatencies.reduce((a, b) => a + b) / _recentLatencies.length;
      if (avgLatency > latencyThresholdMs) {
        _triggerAlert(AlertType.highLatency, {
          'avg_latency_ms': avgLatency,
          'sample_count': _recentLatencies.length,
        });
      }
    }

    // Alerta de tasa de fallback alta
    if (_totalRequests > 10) {
      final fallbackRate = _fallbackCount / _totalRequests;
      if (fallbackRate > fallbackRateThreshold) {
        _triggerAlert(AlertType.highFallbackRate, {
          'fallback_rate': fallbackRate,
          'fallback_count': _fallbackCount,
          'total_requests': _totalRequests,
        });
      }
    }
  }

  void _triggerAlert(AlertType type, Map<String, dynamic> data) {
    // Log crítico
    logError('🚨 ALERT: ${type.name} - $data');

    // Enviar a sistema de alertas (ej: Firebase, Sentry, etc.)
    CoreAnalyticsService.instance.trackEvent(
      'chat_alert_triggered',
      parameters: {
        'alert_type': type.name,
        ...data,
      },
    );
  }

  // Estadísticas para dashboard
  Map<String, dynamic> getStats() {
    return {
      'avg_latency_ms': _recentLatencies.isEmpty
          ? 0
          : _recentLatencies.reduce((a, b) => a + b) / _recentLatencies.length,
      'fallback_rate': _totalRequests == 0
          ? 0
          : _fallbackCount / _totalRequests,
      'total_requests': _totalRequests,
      'window_start': _windowStart?.toIso8601String(),
    };
  }
}

enum AlertType {
  highLatency,
  highFallbackRate,
  backendUnavailable,
  sessionErrors,
}
```

### Entregables
- [ ] `StructuredChatLogger` con logging condicional
- [ ] `ChatTraceContext` para trazabilidad
- [ ] `ChatMonitoringService` con alertas
- [ ] Headers de tracing en requests al backend
- [ ] Integración con Crashlytics

### Dependencias
- CoreAnalyticsService
- Firebase Crashlytics (opcional)

---

## AGENTE 6: QUICK REPLY SMART ENGINE

### Responsabilidad
Mejorar el sistema de quick replies con sugerencias personalizadas del backend.

### Archivos Objetivo
```
zodiac_app/lib/screens/cosmic_coach_chat_screen.dart (líneas 1586-1634)
zodiac_app/lib/services/horoscope_chat_service.dart (líneas 1098-1182)
```

### Tareas

#### 6.1 Quick Replies desde Backend
```dart
// Archivo: horoscope_chat_service.dart
// Mejorar _getSuggestedReplies

/// Sistema de quick replies inteligente con 3 fuentes:
/// 1. Backend AI (personalizado) - PRIORIDAD ALTA
/// 2. Contexto de conversación - PRIORIDAD MEDIA
/// 3. Pool local por categoría - FALLBACK
List<String> _getSmartQuickReplies({
  required HoroscopeQuestionCategory category,
  required String language,
  List<String>? backendSuggestions,
  List<ChatMessage>? conversationHistory,
  CoachingProfile? userProfile,
}) {
  final replies = <String>[];

  // 1. Sugerencias del backend (máximo 2)
  if (backendSuggestions != null && backendSuggestions.isNotEmpty) {
    replies.addAll(backendSuggestions.take(2));
  }

  // 2. Sugerencias contextuales basadas en perfil
  if (userProfile != null && replies.length < 3) {
    final contextualReplies = _getContextualReplies(
      category: category,
      language: language,
      profile: userProfile,
    );

    for (final reply in contextualReplies) {
      if (!replies.contains(reply) && replies.length < 3) {
        replies.add(reply);
      }
    }
  }

  // 3. Fallback al pool local
  if (replies.length < 3) {
    final localReplies = _getSuggestedReplies(category, language);
    for (final reply in localReplies) {
      if (!replies.contains(reply) && replies.length < 3) {
        replies.add(reply);
      }
    }
  }

  return replies;
}

List<String> _getContextualReplies({
  required HoroscopeQuestionCategory category,
  required String language,
  required CoachingProfile profile,
}) {
  final replies = <String>[];

  // Si tiene metas activas, sugerir preguntar sobre ellas
  if (profile.activeGoals.isNotEmpty) {
    final firstGoal = profile.activeGoals.first;
    replies.add(language == 'es'
        ? '¿Cómo va mi progreso en "${firstGoal.title}"?'
        : 'How is my progress on "${firstGoal.title}"?');
  }

  // Si reportó un mood recientemente, preguntar seguimiento
  if (profile.lastReportedMood != null &&
      profile.lastMoodUpdate != null &&
      DateTime.now().difference(profile.lastMoodUpdate!).inHours < 24) {
    replies.add(language == 'es'
        ? '¿Cómo puedo mejorar mi estado de ánimo hoy?'
        : 'How can I improve my mood today?');
  }

  // Basado en el estilo de coaching preferido
  switch (profile.preferredStyle) {
    case CoachingStyle.motivational:
      replies.add(language == 'es'
          ? 'Dame una afirmación poderosa para hoy'
          : 'Give me a powerful affirmation for today');
    case CoachingStyle.analytical:
      replies.add(language == 'es'
          ? '¿Qué dice mi carta natal sobre esto?'
          : 'What does my birth chart say about this?');
    case CoachingStyle.spiritual:
      replies.add(language == 'es'
          ? '¿Cómo puedo conectar con mi propósito?'
          : 'How can I connect with my purpose?');
    case CoachingStyle.practical:
      replies.add(language == 'es'
          ? 'Dame 3 acciones concretas para hoy'
          : 'Give me 3 concrete actions for today');
    default:
      break;
  }

  return replies;
}
```

#### 6.2 UI de Quick Replies Mejorada
```dart
// Archivo: cosmic_coach_chat_screen.dart
// Mejorar _getQuickRepliesFromState (líneas 1586-1634)

List<QuickReply> _getQuickRepliesFromState(
  HoroscopeChatState state,
  BuildContext context,
  CoachingProfile? profile,
) {
  if (state.messages.isEmpty) {
    return _getQuickReplies(context);
  }

  final lastAiMessage = state.messages.reversed.firstWhere(
    (msg) => msg.type == MessageType.ai,
    orElse: () => state.messages.last,
  );

  // Obtener sugerencias del backend
  final backendSuggestions = lastAiMessage.suggestedReplies;

  // Crear quick replies con metadata
  final quickReplies = <QuickReply>[];

  // Backend suggestions (con badge "AI")
  for (final suggestion in backendSuggestions.take(2)) {
    quickReplies.add(QuickReply(
      id: 'ai_${suggestion.hashCode}',
      text: suggestion,
      category: 'ai_suggested',
      badge: 'AI', // Badge especial
      priority: 1, // Alta prioridad
    ));
  }

  // Contextual suggestions (basadas en perfil)
  if (profile != null && quickReplies.length < 3) {
    final contextual = _getContextualQuickReplies(profile, context);
    for (final reply in contextual) {
      if (quickReplies.length < 4) {
        quickReplies.add(reply.copyWith(priority: 2));
      }
    }
  }

  // Local fallback
  if (quickReplies.length < 3) {
    final local = _getQuickReplies(context);
    for (final reply in local) {
      if (quickReplies.length < 4 &&
          !quickReplies.any((qr) => qr.text == reply.text)) {
        quickReplies.add(reply.copyWith(priority: 3));
      }
    }
  }

  // Ordenar por prioridad
  quickReplies.sort((a, b) => (a.priority ?? 3).compareTo(b.priority ?? 3));

  return quickReplies.take(4).toList();
}

// Widget mejorado para mostrar quick replies
Widget _buildSmartQuickReplyChip(QuickReply reply) {
  return Container(
    margin: EdgeInsets.only(right: 8),
    child: FilterChip(
      label: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (reply.badge != null) ...[
            Container(
              padding: EdgeInsets.symmetric(horizontal: 4, vertical: 1),
              decoration: BoxDecoration(
                color: Colors.purple.withOpacity(0.3),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                reply.badge!,
                style: TextStyle(
                  fontSize: 8,
                  fontWeight: FontWeight.bold,
                  color: Colors.purple.shade200,
                ),
              ),
            ),
            SizedBox(width: 4),
          ],
          Text(reply.text),
        ],
      ),
      onSelected: (_) => _handleQuickReply(reply),
      backgroundColor: reply.category == 'ai_suggested'
          ? Colors.purple.withOpacity(0.2)
          : Colors.white.withOpacity(0.1),
    ),
  );
}
```

#### 6.3 Modelo QuickReply Extendido
```dart
// Archivo: chat_models.dart (o crear nuevo archivo)

@immutable
class QuickReply {
  final String id;
  final String text;
  final String category;
  final String? badge; // "AI", "Goal", etc.
  final int? priority; // 1 = highest
  final IconData? icon;
  final Map<String, dynamic>? metadata;

  const QuickReply({
    required this.id,
    required this.text,
    required this.category,
    this.badge,
    this.priority,
    this.icon,
    this.metadata,
  });

  QuickReply copyWith({
    String? id,
    String? text,
    String? category,
    String? badge,
    int? priority,
    IconData? icon,
    Map<String, dynamic>? metadata,
  }) {
    return QuickReply(
      id: id ?? this.id,
      text: text ?? this.text,
      category: category ?? this.category,
      badge: badge ?? this.badge,
      priority: priority ?? this.priority,
      icon: icon ?? this.icon,
      metadata: metadata ?? this.metadata,
    );
  }
}
```

### Entregables
- [ ] `_getSmartQuickReplies()` con 3 fuentes
- [ ] `_getContextualReplies()` basado en perfil
- [ ] UI de chips con badges
- [ ] Modelo `QuickReply` extendido

### Dependencias
- CoachingProfile
- Backend quick replies API
- chat_models.dart

---

## AGENTE 7: HISTORY & FAVORITES

### Responsabilidad
Mejorar el historial de chat y sistema de favoritos.

### Archivos Objetivo
```
zodiac_app/lib/widgets/chat/chat_history_widget_riverpod.dart (líneas 189-264)
zodiac_app/lib/services/favorite_message_service.dart
zodiac_app/lib/screens/favorites_screen.dart
```

### Tareas

#### 7.1 Historial Enriquecido con Etiquetas
```dart
// Archivo: chat_history_widget_riverpod.dart
// Mejorar ChatMessageWidget

class EnrichedChatMessageWidget extends ConsumerWidget {
  final ChatMessage message;
  final bool showTimestamp;
  final bool showAvatar;
  final VoidCallback? onRetry;
  final Function(String)? onQuickReply;
  final VoidCallback? onFavorite;
  final VoidCallback? onShare;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Column(
      crossAxisAlignment: message.type == MessageType.user
          ? CrossAxisAlignment.end
          : CrossAxisAlignment.start,
      children: [
        // Timestamp (si aplica)
        if (showTimestamp) _buildTimestamp(),

        // Mensaje principal
        Row(
          mainAxisAlignment: message.type == MessageType.user
              ? MainAxisAlignment.end
              : MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (showAvatar && message.type == MessageType.ai)
              _buildAIAvatar(),

            Flexible(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Source badge (Template/AI/Cache)
                  if (message.type == MessageType.ai)
                    _buildSourceBadge(),

                  // Contenido del mensaje
                  _buildMessageContent(),

                  // Acciones (favorito, compartir, etc.)
                  if (message.type == MessageType.ai)
                    _buildMessageActions(context, ref),
                ],
              ),
            ),
          ],
        ),

        // Quick replies (si hay)
        if (message.suggestedReplies.isNotEmpty)
          _buildQuickReplies(),
      ],
    );
  }

  Widget _buildSourceBadge() {
    final source = message.metadata?['source'] as String? ?? 'unknown';

    final (label, color, icon) = switch (source) {
      'ai_backend' => ('AI', Colors.purple.shade300, Icons.auto_awesome),
      'template' => ('Local', Colors.blue.shade300, Icons.flash_on),
      'cache' => ('Cache', Colors.green.shade300, Icons.cached),
      'hybrid' => ('AI+', Colors.amber.shade300, Icons.psychology),
      _ => ('', Colors.grey, Icons.help_outline),
    };

    if (label.isEmpty) return SizedBox.shrink();

    return Container(
      margin: EdgeInsets.only(bottom: 4),
      padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 10, color: color),
          SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 9,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageActions(BuildContext context, WidgetRef ref) {
    final favoriteService = ref.watch(favoriteMessageServiceProvider);
    final isFavorite = favoriteService.isFavorite(message.id);

    return Padding(
      padding: EdgeInsets.only(top: 8),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Favorito
          IconButton(
            icon: Icon(
              isFavorite ? Icons.favorite : Icons.favorite_border,
              size: 16,
              color: isFavorite ? Colors.red.shade300 : Colors.white60,
            ),
            onPressed: () {
              if (isFavorite) {
                favoriteService.removeFavorite(message.id);
              } else {
                favoriteService.addFavorite(message);
              }
            },
            tooltip: isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos',
            constraints: BoxConstraints(minWidth: 32, minHeight: 32),
            padding: EdgeInsets.zero,
          ),

          // Copiar
          IconButton(
            icon: Icon(Icons.copy, size: 16, color: Colors.white60),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: message.content));
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Copiado al portapapeles')),
              );
            },
            tooltip: 'Copiar',
            constraints: BoxConstraints(minWidth: 32, minHeight: 32),
            padding: EdgeInsets.zero,
          ),

          // Compartir
          IconButton(
            icon: Icon(Icons.share, size: 16, color: Colors.white60),
            onPressed: () => _shareMessage(context),
            tooltip: 'Compartir',
            constraints: BoxConstraints(minWidth: 32, minHeight: 32),
            padding: EdgeInsets.zero,
          ),
        ],
      ),
    );
  }

  void _shareMessage(BuildContext context) {
    Share.share(
      'Cosmic Coach dice:\n\n${message.content}\n\n✨ Zodiac App',
      subject: 'Mensaje de Cosmic Coach',
    );
  }
}
```

#### 7.2 Servicio de Favoritos Mejorado
```dart
// Archivo: favorite_message_service.dart
// Agregar funcionalidades

class FavoriteMessageService extends ChangeNotifier {
  // ... código existente ...

  // Categorías de favoritos
  final Map<String, List<String>> _categories = {};

  /// Agregar a categoría
  Future<void> addToCategory(String messageId, String category) async {
    _categories.putIfAbsent(category, () => []);
    if (!_categories[category]!.contains(messageId)) {
      _categories[category]!.add(messageId);
      await _saveCategories();
      notifyListeners();
    }
  }

  /// Obtener favoritos por categoría
  List<ChatMessage> getFavoritesByCategory(String category) {
    final ids = _categories[category] ?? [];
    return _favorites.where((m) => ids.contains(m.id)).toList();
  }

  /// Buscar en favoritos
  List<ChatMessage> searchFavorites(String query) {
    final lowercaseQuery = query.toLowerCase();
    return _favorites.where((m) {
      return m.content.toLowerCase().contains(lowercaseQuery);
    }).toList();
  }

  /// Exportar favoritos
  Future<String> exportFavorites() async {
    final buffer = StringBuffer();
    buffer.writeln('# Mis Favoritos de Cosmic Coach\n');
    buffer.writeln('Exportado: ${DateTime.now().toString()}\n');
    buffer.writeln('---\n');

    for (final message in _favorites) {
      buffer.writeln('## ${message.timestamp.toString().split(' ')[0]}');
      buffer.writeln(message.content);
      buffer.writeln('\n---\n');
    }

    return buffer.toString();
  }

  // Estadísticas de favoritos
  Map<String, int> getFavoriteStats() {
    final stats = <String, int>{};
    for (final message in _favorites) {
      final category = message.metadata?['category'] as String? ?? 'general';
      stats[category] = (stats[category] ?? 0) + 1;
    }
    return stats;
  }
}
```

#### 7.3 Pantalla de Favoritos Mejorada
```dart
// Archivo: favorites_screen.dart
// Nueva UI con categorías y búsqueda

class FavoritesScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends ConsumerState<FavoritesScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String _searchQuery = '';

  final _categories = [
    ('all', 'Todos', Icons.star),
    ('daily_guidance', 'Guía Diaria', Icons.wb_sunny),
    ('love', 'Amor', Icons.favorite),
    ('career', 'Carrera', Icons.work),
    ('spiritual', 'Espiritual', Icons.self_improvement),
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: _categories.length, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    final favoriteService = ref.watch(favoriteMessageServiceProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('Mis Favoritos'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: _categories.map((c) => Tab(
            icon: Icon(c.$3, size: 18),
            text: c.$2,
          )).toList(),
        ),
        actions: [
          // Búsqueda
          IconButton(
            icon: Icon(Icons.search),
            onPressed: _showSearch,
          ),
          // Exportar
          IconButton(
            icon: Icon(Icons.file_download),
            onPressed: () => _exportFavorites(favoriteService),
          ),
        ],
      ),
      body: Column(
        children: [
          // Estadísticas rápidas
          _buildStatsBar(favoriteService),

          // Lista de favoritos
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: _categories.map((c) {
                final favorites = c.$1 == 'all'
                    ? favoriteService.favorites
                    : favoriteService.getFavoritesByCategory(c.$1);

                // Filtrar por búsqueda
                final filtered = _searchQuery.isEmpty
                    ? favorites
                    : favorites.where((m) =>
                        m.content.toLowerCase().contains(_searchQuery.toLowerCase())
                      ).toList();

                return _buildFavoritesList(filtered);
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatsBar(FavoriteMessageService service) {
    final stats = service.getFavoriteStats();

    return Container(
      height: 60,
      padding: EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatItem('Total', service.favorites.length.toString(), Icons.star),
          _buildStatItem('Guía', stats['daily_guidance']?.toString() ?? '0', Icons.wb_sunny),
          _buildStatItem('Amor', stats['love']?.toString() ?? '0', Icons.favorite),
          _buildStatItem('Carrera', stats['career']?.toString() ?? '0', Icons.work),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, String value, IconData icon) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, size: 20, color: Colors.purple.shade300),
        SizedBox(height: 4),
        Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        Text(label, style: TextStyle(fontSize: 11, color: Colors.white60)),
      ],
    );
  }

  Widget _buildFavoritesList(List<ChatMessage> favorites) {
    if (favorites.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.star_border, size: 64, color: Colors.white30),
            SizedBox(height: 16),
            Text('No hay favoritos en esta categoría'),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: EdgeInsets.all(16),
      itemCount: favorites.length,
      itemBuilder: (context, index) {
        return FavoriteMessageCard(
          message: favorites[index],
          onRemove: () {
            ref.read(favoriteMessageServiceProvider).removeFavorite(favorites[index].id);
          },
        );
      },
    );
  }

  Future<void> _exportFavorites(FavoriteMessageService service) async {
    final content = await service.exportFavorites();
    await Share.share(content, subject: 'Mis Favoritos de Cosmic Coach');
  }
}
```

### Entregables
- [ ] `EnrichedChatMessageWidget` con source badges
- [ ] Acciones de mensaje (favorito, copiar, compartir)
- [ ] `FavoriteMessageService` con categorías y búsqueda
- [ ] `FavoritesScreen` con tabs y estadísticas
- [ ] Funcionalidad de exportar favoritos

### Dependencias
- FavoriteMessageService
- share_plus package

---

## AGENTE 8: QA & LOCALIZATION

### Responsabilidad
Pruebas unitarias, integración, y validación de localización.

### Archivos Objetivo
```
zodiac_app/test/services/horoscope_chat_service_test.dart (crear)
zodiac_app/test/widgets/cosmic_coach_chat_test.dart (crear)
zodiac_app/lib/l10n/*.arb
```

### Tareas

#### 8.1 Tests Unitarios del Servicio
```dart
// Archivo: test/services/horoscope_chat_service_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;
import 'package:zodiac_app/services/horoscope_chat_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';

class MockPreferencesService extends Mock implements PreferencesService {}
class MockHttpClient extends Mock implements http.Client {}

void main() {
  late HoroscopeChatService service;
  late MockPreferencesService mockPrefs;
  late MockHttpClient mockHttpClient;

  setUp(() {
    mockPrefs = MockPreferencesService();
    mockHttpClient = MockHttpClient();
    service = HoroscopeChatService(mockPrefs, mockHttpClient);
  });

  group('HoroscopeChatService', () {
    group('sendMessage', () {
      test('should return cached response when available', () async {
        // Arrange
        when(mockPrefs.userId).thenReturn('test_user');
        // ... setup cache

        // Act
        final response = await service.sendMessage(
          message: 'test message',
          userId: 'test_user',
          zodiacSign: 'Aries',
          language: 'es',
        );

        // Assert
        expect(response.source, equals('cache'));
      });

      test('should return template response for high confidence match', () async {
        // Arrange
        when(mockPrefs.userId).thenReturn('test_user');

        // Act
        final response = await service.sendMessage(
          message: 'horóscopo de hoy',
          userId: 'test_user',
          zodiacSign: 'Aries',
          language: 'es',
        );

        // Assert
        expect(response.source, equals('template'));
        expect(response.category, equals(HoroscopeQuestionCategory.dailyGuidance));
      });

      test('should call backend for low confidence match', () async {
        // Arrange
        when(mockPrefs.userId).thenReturn('test_user');
        when(mockHttpClient.post(any, headers: anyNamed('headers'), body: anyNamed('body')))
            .thenAnswer((_) async => http.Response(
              '{"success": true, "content": "AI response"}',
              200,
            ));

        // Act
        final response = await service.sendMessage(
          message: 'pregunta compleja sin match claro',
          userId: 'test_user',
          zodiacSign: 'Aries',
          language: 'es',
        );

        // Assert
        expect(response.source, equals('ai_backend'));
      });

      test('should respect daily limit', () async {
        // Arrange
        when(mockPrefs.userId).thenReturn('test_user');
        // Simulate limit reached
        await service.initialize();
        for (var i = 0; i < 5; i++) {
          await service.sendMessage(
            message: 'test $i',
            userId: 'test_user',
            zodiacSign: 'Aries',
            language: 'es',
          );
        }

        // Act
        final response = await service.sendMessage(
          message: 'test beyond limit',
          userId: 'test_user',
          zodiacSign: 'Aries',
          language: 'es',
        );

        // Assert
        expect(response.source, equals('limit'));
      });

      test('should fallback to template on backend error', () async {
        // Arrange
        when(mockPrefs.userId).thenReturn('test_user');
        when(mockHttpClient.post(any, headers: anyNamed('headers'), body: anyNamed('body')))
            .thenThrow(Exception('Network error'));

        // Act
        final response = await service.sendMessage(
          message: 'pregunta que requiere backend',
          userId: 'test_user',
          zodiacSign: 'Aries',
          language: 'es',
        );

        // Assert
        expect(response.source, isIn(['template', 'emergency']));
      });
    });

    group('categorizeMessage', () {
      test('should categorize daily guidance questions correctly', () {
        final result = service.categorizeMessage('¿cómo está mi día?', 'es');
        expect(result.category, equals(HoroscopeQuestionCategory.dailyGuidance));
        expect(result.confidence, greaterThan(0.8));
      });

      test('should categorize love questions correctly', () {
        final result = service.categorizeMessage('¿soy compatible con Leo?', 'es');
        expect(result.category, equals(HoroscopeQuestionCategory.loveCompatibility));
      });

      test('should categorize career questions correctly', () {
        final result = service.categorizeMessage('¿es buen momento para cambiar de trabajo?', 'es');
        expect(result.category, equals(HoroscopeQuestionCategory.careerTiming));
      });

      test('should handle multiple languages', () {
        // Spanish
        var result = service.categorizeMessage('horóscopo de hoy', 'es');
        expect(result.category, equals(HoroscopeQuestionCategory.dailyGuidance));

        // English
        result = service.categorizeMessage('how is my day today', 'en');
        expect(result.category, equals(HoroscopeQuestionCategory.dailyGuidance));

        // German
        result = service.categorizeMessage('wie ist mein Tag heute', 'de');
        expect(result.category, equals(HoroscopeQuestionCategory.dailyGuidance));
      });
    });

    group('Quick Replies', () {
      test('should return personalized quick replies', () async {
        // Test que las quick replies cambian según contexto
      });

      test('should not repeat recent quick replies', () async {
        // Test de no repetición
      });
    });
  });
}
```

#### 8.2 Tests de Widget (Golden Tests)
```dart
// Archivo: test/widgets/cosmic_coach_chat_test.dart

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  group('CosmicCoachChatScreen Goldens', () {
    testGoldens('renders correctly in light mode', (tester) async {
      await loadAppFonts();

      await tester.pumpWidgetBuilder(
        ProviderScope(
          child: MaterialApp(
            theme: ThemeData.light(),
            home: CosmicCoachChatScreen(),
          ),
        ),
        surfaceSize: Size(375, 812), // iPhone X size
      );

      await screenMatchesGolden(tester, 'cosmic_coach_light');
    });

    testGoldens('renders correctly in dark mode', (tester) async {
      await loadAppFonts();

      await tester.pumpWidgetBuilder(
        ProviderScope(
          child: MaterialApp(
            theme: ThemeData.dark(),
            home: CosmicCoachChatScreen(),
          ),
        ),
        surfaceSize: Size(375, 812),
      );

      await screenMatchesGolden(tester, 'cosmic_coach_dark');
    });

    testGoldens('renders empty state correctly', (tester) async {
      await loadAppFonts();

      await tester.pumpWidgetBuilder(
        ProviderScope(
          overrides: [
            horoscopeChatStateStreamProvider.overrideWith(
              (ref) => Stream.value(HoroscopeChatState()),
            ),
          ],
          child: MaterialApp(
            theme: ThemeData.dark(),
            home: CosmicCoachChatScreen(),
          ),
        ),
        surfaceSize: Size(375, 812),
      );

      await screenMatchesGolden(tester, 'cosmic_coach_empty_state');
    });

    testGoldens('renders typing indicator correctly', (tester) async {
      await loadAppFonts();

      await tester.pumpWidgetBuilder(
        ProviderScope(
          overrides: [
            horoscopeChatStateStreamProvider.overrideWith(
              (ref) => Stream.value(HoroscopeChatState(isLoading: true)),
            ),
          ],
          child: MaterialApp(
            theme: ThemeData.dark(),
            home: CosmicCoachChatScreen(),
          ),
        ),
        surfaceSize: Size(375, 812),
      );

      await screenMatchesGolden(tester, 'cosmic_coach_typing');
    });

    testGoldens('renders Stellar tier correctly', (tester) async {
      // Test para tier Stellar
    });

    testGoldens('renders Cosmic tier with ads correctly', (tester) async {
      // Test para tier Cosmic con banner de ads
    });

    testGoldens('renders Free tier paywall correctly', (tester) async {
      // Test para paywall de Free tier
    });
  });
}
```

#### 8.3 Nuevas Claves de Localización
```json
// Archivo: lib/l10n/app_es.arb (agregar)
{
  "cosmicCoachModeGeneral": "General",
  "cosmicCoachModeWellness": "Bienestar",
  "cosmicCoachModeCareer": "Carrera",
  "cosmicCoachModeLove": "Amor",
  "cosmicCoachModeSpirituality": "Espiritualidad",

  "cosmicCoachSourceAI": "IA",
  "cosmicCoachSourceLocal": "Local",
  "cosmicCoachSourceCache": "Cache",
  "cosmicCoachSourceHybrid": "IA+",

  "cosmicCoachActionFavorite": "Agregar a favoritos",
  "cosmicCoachActionRemoveFavorite": "Quitar de favoritos",
  "cosmicCoachActionCopy": "Copiar",
  "cosmicCoachActionShare": "Compartir",

  "cosmicCoachFavoritesTitle": "Mis Favoritos",
  "cosmicCoachFavoritesEmpty": "No hay favoritos en esta categoría",
  "cosmicCoachFavoritesExport": "Exportar favoritos",
  "cosmicCoachFavoritesAll": "Todos",
  "cosmicCoachFavoritesDaily": "Guía Diaria",
  "cosmicCoachFavoritesLove": "Amor",
  "cosmicCoachFavoritesCareer": "Carrera",
  "cosmicCoachFavoritesSpiritual": "Espiritual",

  "cosmicCoachMoodQuestion": "¿Cómo te sientes hoy?",
  "cosmicCoachGoalProgress": "¿Cómo va mi progreso en \"{goal}\"?",
  "@cosmicCoachGoalProgress": {
    "placeholders": {
      "goal": {
        "type": "String"
      }
    }
  },

  "cosmicCoachUpgradeStellar": "Actualiza a Stellar para chat ilimitado sin anuncios",
  "cosmicCoachRateLimit": "Has alcanzado el límite de mensajes. Actualiza para continuar."
}

// Archivo: lib/l10n/app_en.arb (agregar)
{
  "cosmicCoachModeGeneral": "General",
  "cosmicCoachModeWellness": "Wellness",
  "cosmicCoachModeCareer": "Career",
  "cosmicCoachModeLove": "Love",
  "cosmicCoachModeSpirituality": "Spirituality",

  "cosmicCoachSourceAI": "AI",
  "cosmicCoachSourceLocal": "Local",
  "cosmicCoachSourceCache": "Cache",
  "cosmicCoachSourceHybrid": "AI+",

  "cosmicCoachActionFavorite": "Add to favorites",
  "cosmicCoachActionRemoveFavorite": "Remove from favorites",
  "cosmicCoachActionCopy": "Copy",
  "cosmicCoachActionShare": "Share",

  "cosmicCoachFavoritesTitle": "My Favorites",
  "cosmicCoachFavoritesEmpty": "No favorites in this category",
  "cosmicCoachFavoritesExport": "Export favorites",
  "cosmicCoachFavoritesAll": "All",
  "cosmicCoachFavoritesDaily": "Daily Guidance",
  "cosmicCoachFavoritesLove": "Love",
  "cosmicCoachFavoritesCareer": "Career",
  "cosmicCoachFavoritesSpiritual": "Spiritual",

  "cosmicCoachMoodQuestion": "How are you feeling today?",
  "cosmicCoachGoalProgress": "How is my progress on \"{goal}\"?",
  "@cosmicCoachGoalProgress": {
    "placeholders": {
      "goal": {
        "type": "String"
      }
    }
  },

  "cosmicCoachUpgradeStellar": "Upgrade to Stellar for unlimited ad-free chat",
  "cosmicCoachRateLimit": "You've reached the message limit. Upgrade to continue."
}
```

#### 8.4 Script de Validación de Localizaciones
```dart
// Archivo: tool/validate_l10n.dart

import 'dart:convert';
import 'dart:io';

void main() {
  final languages = ['es', 'en', 'de', 'fr', 'it', 'pt'];
  final baseFile = File('lib/l10n/app_en.arb');
  final baseJson = jsonDecode(baseFile.readAsStringSync()) as Map<String, dynamic>;

  // Obtener claves base (excluyendo metadata @)
  final baseKeys = baseJson.keys.where((k) => !k.startsWith('@')).toSet();

  for (final lang in languages) {
    if (lang == 'en') continue;

    final file = File('lib/l10n/app_$lang.arb');
    if (!file.existsSync()) {
      print('❌ Missing file: app_$lang.arb');
      continue;
    }

    final json = jsonDecode(file.readAsStringSync()) as Map<String, dynamic>;
    final keys = json.keys.where((k) => !k.startsWith('@')).toSet();

    // Claves faltantes
    final missing = baseKeys.difference(keys);
    if (missing.isNotEmpty) {
      print('⚠️ [$lang] Missing ${missing.length} keys:');
      for (final key in missing.take(10)) {
        print('   - $key');
      }
      if (missing.length > 10) {
        print('   ... and ${missing.length - 10} more');
      }
    }

    // Claves extra
    final extra = keys.difference(baseKeys);
    if (extra.isNotEmpty) {
      print('ℹ️ [$lang] Has ${extra.length} extra keys');
    }

    // Claves vacías
    final empty = json.entries
        .where((e) => !e.key.startsWith('@') && e.value.toString().isEmpty)
        .map((e) => e.key)
        .toList();
    if (empty.isNotEmpty) {
      print('❌ [$lang] Empty values for: ${empty.join(", ")}');
    }

    if (missing.isEmpty && empty.isEmpty) {
      print('✅ [$lang] All keys present and non-empty');
    }
  }
}
```

### Entregables
- [ ] Tests unitarios de `HoroscopeChatService`
- [ ] Golden tests para temas claro/oscuro
- [ ] Golden tests para diferentes tiers
- [ ] Nuevas claves de localización en 6 idiomas
- [ ] Script de validación de localizaciones
- [ ] Documentación de cobertura de tests

### Dependencias
- flutter_test
- mockito
- golden_toolkit

---

## CRONOGRAMA DE EJECUCIÓN

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SPRINT 1 (Días 1-3)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ AGENTE 1: Analytics Setup           │ AGENTE 5: Logging Setup              │
│ - ChatAnalyticsEvent                 │ - StructuredChatLogger               │
│ - _trackMessageEvent()               │ - ChatTraceContext                   │
│ - Reporte línea base                 │ - ChatMonitoringService              │
├─────────────────────────────────────────────────────────────────────────────┤
│                         SPRINT 2 (Días 4-7)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ AGENTE 2: UX Input                  │ AGENTE 4: Personalization            │
│ - SmartChatInputWidget              │ - CoachingProfile model              │
│ - ConversationMode selector         │ - CoachingProfileNotifier            │
│ - PersonalizedEmptyState            │ - Provider integration               │
├─────────────────────────────────────────────────────────────────────────────┤
│                         SPRINT 3 (Días 8-12)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ AGENTE 3: AI Engine                 │ AGENTE 6: Quick Replies              │
│ - _callBackendWithRetry()           │ - _getSmartQuickReplies()            │
│ - EnrichedContext                   │ - Contextual suggestions             │
│ - _generateHybridResponse()         │ - UI with badges                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                         SPRINT 4 (Días 13-17)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ AGENTE 7: History & Favorites       │ AGENTE 8: QA & L10N                  │
│ - EnrichedChatMessageWidget         │ - Unit tests                         │
│ - Message actions                   │ - Golden tests                       │
│ - FavoritesScreen enhanced          │ - Localization keys (6 langs)        │
├─────────────────────────────────────────────────────────────────────────────┤
│                         SPRINT 5 (Días 18-21)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                    INTEGRACIÓN Y TESTING FINAL                              │
│ - Integrar todos los cambios                                                │
│ - Tests de integración E2E                                                  │
│ - Beta cerrada (Stellar tier)                                               │
│ - Correcciones finales                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                         ROLLOUT (Días 22-25)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                    DESPLIEGUE PROGRESIVO                                    │
│ - 10% usuarios → 25% → 50% → 100%                                          │
│ - Monitoreo de métricas                                                     │
│ - Hotfixes si es necesario                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## MATRIZ DE DEPENDENCIAS

| Agente | Depende de | Es requerido por |
|--------|------------|------------------|
| 1 | - | 5, 8 |
| 2 | 4 | 6 |
| 3 | 4 | 2, 6 |
| 4 | - | 2, 3, 6 |
| 5 | 1 | 8 |
| 6 | 2, 3, 4 | 7 |
| 7 | 6 | 8 |
| 8 | 1, 5, 7 | - |

---

## RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Backend no responde | Media | Alto | Fallback robusto a templates |
| Latencia alta | Media | Medio | Timeout dinámico + cache |
| Rotura de localización | Baja | Medio | Script de validación automático |
| Regresión UI | Media | Medio | Golden tests obligatorios |
| Conflictos de merge | Alta | Bajo | Feature branches + PRs pequeños |

---

## MÉTRICAS DE ÉXITO

### Post-lanzamiento (Semana 1-2)
- [ ] Mensajes/sesión ≥ 4.5 (vs baseline)
- [ ] Errores backend < 2%
- [ ] Crash rate estable (no incremento)

### Post-lanzamiento (Semana 3-4)
- [ ] Mensajes/sesión ≥ 5.0
- [ ] Retención semanal +10%
- [ ] NPS ≥ 40

### Post-lanzamiento (Mes 2)
- [ ] Mensajes/sesión ≥ 5.5
- [ ] Retención semanal +15%
- [ ] NPS ≥ 45
- [ ] Errores < 1%

---

## CHECKLIST DE LANZAMIENTO

### Pre-Beta
- [ ] Todos los tests pasan
- [ ] Golden tests actualizados
- [ ] Localizaciones validadas
- [ ] Feature flags configurados
- [ ] Dashboards de métricas listos

### Beta (Stellar)
- [ ] 100 usuarios Stellar seleccionados
- [ ] Canal de feedback habilitado
- [ ] Monitoreo 24/7 activado
- [ ] Rollback plan preparado

### Producción
- [ ] Aprobación de QA
- [ ] Aprobación de Product
- [ ] Release notes documentadas
- [ ] Comunicación a soporte

---

## COMANDOS DE EJECUCIÓN

```bash
# Ejecutar todos los agentes en paralelo (simulación)
# En realidad, usar Claude Code multi-agente

# Validar localizaciones
dart run tool/validate_l10n.dart

# Ejecutar tests
flutter test --coverage

# Generar golden tests
flutter test --update-goldens

# Build de verificación
flutter build ios --release --no-codesign
flutter build appbundle --release
```

---

**Documento generado por Claude Code**
**Fecha: 2025-11-28**
**Versión del plan: 1.0**