# 🚀 PLAN MULTIAGENTE FINAL: COSMIC COACH V2 COMPLETO

**Fecha:** 18 Noviembre 2025 - Noche
**Objetivo:** Completar las 3 features restantes del Plan Maestro V2
**Tiempo estimado:** 2-3 horas con 3 agentes en paralelo
**Estado actual:** Settings 100% funcional, faltan features avanzadas

---

## 📊 ESTADO ACTUAL vs OBJETIVO

### ✅ Ya completado (100%)
- Settings screen con persistencia completa
- 4 servicios backend (ConversationHistory, ChatCache, FavoriteMessage, Preferences extendido)
- 7 pantallas UI con dark mode
- 329 traducciones en 6 idiomas
- Widgets reutilizables
- Compilación sin errores

### 🎯 Por completar (3 features)
1. **Engine ↔ Modes Integration** - Que los modos quick/balanced/detailed cambien el comportamiento real
2. **Cosmic Status Panel** - Panel visual que muestre modo/personality/online status
3. **Cosmic Profile Service** - Perfiles prearmados (Starter/Power/Mystic)

---

## 🤖 ARQUITECTURA MULTIAGENTE (3 AGENTES EN PARALELO)

### AGENTE 1: Backend Engine Master
**Responsabilidad:** Conectar HoroscopeChatService con los modos configurados
**Duración estimada:** 2 horas
**Archivos a modificar:**
- `lib/services/horoscope_chat_service.dart`
- `lib/providers/horoscope_chat_provider.dart`

**Prompt recomendado:**
```
Ejecuta AGENTE 1: Backend Engine Master del plan
PLAN_MULTIAGENTE_FINAL_COSMIC_COACH_NOV18_NOCHE_2025.md

Objetivo: Modificar HoroscopeChatService para que respete los modos
quick/balanced/detailed configurados en PreferencesService.

Seguí el pseudocódigo exacto de la sección "AGENTE 1: BACKEND ENGINE MASTER".
```

---

### AGENTE 2: UI Cosmic Designer
**Responsabilidad:** Crear Cosmic Status Panel widget
**Duración estimada:** 1 hora
**Archivos a crear/modificar:**
- `lib/widgets/cosmic_coach/cosmic_status_panel.dart` (NUEVO)
- `lib/screens/cosmic_coach_chat_screen.dart` (modificar)
- `assets/l10n/app_*.arb` (agregar keys necesarias)

**Prompt recomendado:**
```
Ejecuta AGENTE 2: UI Cosmic Designer del plan
PLAN_MULTIAGENTE_FINAL_COSMIC_COACH_NOV18_NOCHE_2025.md

Objetivo: Crear widget CosmicStatusPanel que muestre modo/personality/status
en tiempo real.

Seguí el código completo de la sección "AGENTE 2: UI COSMIC DESIGNER".
```

---

### AGENTE 3: Profile System Architect
**Responsabilidad:** Crear sistema de perfiles cósmicos
**Duración estimada:** 2.5 horas
**Archivos a crear:**
- `lib/models/cosmic_profile.dart` (NUEVO)
- `lib/services/cosmic_profile_service.dart` (NUEVO)
- `lib/screens/cosmic_coach_settings_screen.dart` (agregar sección de perfiles)

**Prompt recomendado:**
```
Ejecuta AGENTE 3: Profile System Architect del plan
PLAN_MULTIAGENTE_FINAL_COSMIC_COACH_NOV18_NOCHE_2025.md

Objetivo: Crear sistema de perfiles Starter/Power User/Mystic con presets
y UI en settings.

Seguí el código completo de la sección "AGENTE 3: PROFILE SYSTEM ARCHITECT".
```

---

## 📋 AGENTE 1: BACKEND ENGINE MASTER

### Objetivo
Modificar `HoroscopeChatService` para que respete los modos configurados en `PreferencesService`.

### Lógica a implementar

#### Modo: QUICK (100% Local)
```dart
// QUICK MODE BEHAVIOR:
// - 0 llamadas a backend
// - Solo plantillas locales
// - Respuestas instantáneas (<1s)
// - Sin personalización avanzada
```

#### Modo: BALANCED (80% Local, 20% Backend)
```dart
// BALANCED MODE BEHAVIOR:
// - Mayoría plantillas locales
// - Backend solo para preguntas complejas
// - Detectar complejidad de pregunta
// - Si simple → local, si compleja → backend
```

#### Modo: DETAILED (50% Local, 50% Backend)
```dart
// DETAILED MODE BEHAVIOR:
// - Preferir backend cuando disponible
// - Respuestas más personalizadas
// - Usar contexto de conversación
// - Respetar daily limits
```

### Pseudocódigo de implementación

```dart
// En HoroscopeChatService

class HoroscopeChatService {
  final PreferencesService _prefsService;

  Future<ChatMessage> generateResponse(
    String userMessage,
    List<ChatMessage> conversationHistory,
  ) async {
    // 1. Leer modo configurado
    final mode = await _prefsService.getChatMode();

    // 2. Estrategia según modo
    switch (mode) {
      case 'quick':
        return _generateQuickResponse(userMessage);

      case 'balanced':
        return await _generateBalancedResponse(userMessage, conversationHistory);

      case 'detailed':
        return await _generateDetailedResponse(userMessage, conversationHistory);

      default:
        return _generateQuickResponse(userMessage);
    }
  }

  // QUICK: Solo templates
  ChatMessage _generateQuickResponse(String userMessage) {
    final category = _detectCategory(userMessage);
    final template = _getLocalTemplate(category);
    return ChatMessage(
      content: template,
      type: MessageType.assistant,
      timestamp: DateTime.now(),
    );
  }

  // BALANCED: Decidir según complejidad
  Future<ChatMessage> _generateBalancedResponse(
    String userMessage,
    List<ChatMessage> history,
  ) async {
    final complexity = _analyzeComplexity(userMessage);

    if (complexity == QuestionComplexity.simple) {
      // Usar local
      return _generateQuickResponse(userMessage);
    } else {
      // Intentar backend, fallback a local
      try {
        return await _generateBackendResponse(userMessage, history);
      } catch (e) {
        return _generateQuickResponse(userMessage);
      }
    }
  }

  // DETAILED: Preferir backend
  Future<ChatMessage> _generateDetailedResponse(
    String userMessage,
    List<ChatMessage> history,
  ) async {
    final preferBackend = await _prefsService.getPreferBackend();
    final isPremium = await _checkPremiumStatus();

    if (preferBackend && isPremium) {
      try {
        return await _generateBackendResponse(userMessage, history);
      } catch (e) {
        return _generateQuickResponse(userMessage);
      }
    } else {
      // Usar template enriquecido con contexto
      return _generateEnrichedLocalResponse(userMessage, history);
    }
  }

  // Helpers
  QuestionComplexity _analyzeComplexity(String message) {
    // Análisis simple por longitud y keywords
    if (message.length < 30) return QuestionComplexity.simple;
    if (message.contains('por qué') || message.contains('explica')) {
      return QuestionComplexity.complex;
    }
    return QuestionComplexity.medium;
  }
}

enum QuestionComplexity { simple, medium, complex }
```

### Testing checklist
- [ ] Modo Quick: 0 llamadas a backend
- [ ] Modo Balanced: Mix local/backend según complejidad
- [ ] Modo Detailed: Preferencia por backend cuando premium
- [ ] Fallback a local cuando backend falla
- [ ] Respeta daily limits en modo detailed

---

## 📋 AGENTE 2: UI COSMIC DESIGNER

### Objetivo
Crear widget `CosmicStatusPanel` que muestre el estado actual del coach de forma visual.

### Diseño del widget

```dart
// lib/widgets/cosmic_coach/cosmic_status_panel.dart

/// 🎨 COSMIC STATUS PANEL
/// =====================
/// Widget que muestra el estado actual del Cosmic Coach
///
/// Features:
/// - Modo activo (Quick/Balanced/Detailed)
/// - Personalidad (Friendly/Professional/Mystical)
/// - Estado de conexión (Online/Offline)
/// - Premium badge si aplica

class CosmicStatusPanel extends ConsumerWidget {
  const CosmicStatusPanel({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    final prefs = ref.watch(preferencesServiceProvider);

    return FutureBuilder(
      future: _loadSettings(prefs),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return SizedBox.shrink();

        final settings = snapshot.data as CosmicSettings;

        return Container(
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: isDarkMode
              ? Color(0xFF1A0B3E).withOpacity(0.8)
              : Colors.white.withOpacity(0.9),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: isDarkMode ? Colors.purple.shade700 : Colors.purple.shade200,
              width: 1,
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 1. Mode Badge
              _ModeBadge(mode: settings.mode),

              SizedBox(width: 8),

              // 2. Personality Icon
              _PersonalityIcon(personality: settings.personality),

              SizedBox(width: 8),

              // 3. Connection Status
              _ConnectionIndicator(isOnline: settings.isOnline),

              // 4. Premium Badge (si aplica)
              if (settings.isPremium) ...[
                SizedBox(width: 8),
                _PremiumBadge(),
              ],
            ],
          ),
        );
      },
    );
  }
}

// Sub-widgets

class _ModeBadge extends StatelessWidget {
  final String mode;

  @override
  Widget build(BuildContext context) {
    final config = _getModeConfig(mode);

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: config.color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(config.icon, size: 14, color: config.color),
          SizedBox(width: 4),
          Text(
            config.label,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: config.color,
            ),
          ),
        ],
      ),
    );
  }

  _ModeConfig _getModeConfig(String mode) {
    switch (mode) {
      case 'quick':
        return _ModeConfig(
          icon: Icons.flash_on,
          label: 'Quick',
          color: Colors.amber,
        );
      case 'balanced':
        return _ModeConfig(
          icon: Icons.balance,
          label: 'Balanced',
          color: Colors.blue,
        );
      case 'detailed':
        return _ModeConfig(
          icon: Icons.article,
          label: 'Detailed',
          color: Colors.purple,
        );
      default:
        return _ModeConfig(
          icon: Icons.help,
          label: mode,
          color: Colors.grey,
        );
    }
  }
}

class _PersonalityIcon extends StatelessWidget {
  final String personality;

  @override
  Widget build(BuildContext context) {
    final config = _getPersonalityConfig(personality);

    return Tooltip(
      message: config.label,
      child: Icon(
        config.icon,
        size: 20,
        color: config.color,
      ),
    );
  }

  _PersonalityConfig _getPersonalityConfig(String personality) {
    switch (personality) {
      case 'friendly':
        return _PersonalityConfig(
          icon: Icons.sentiment_very_satisfied,
          label: 'Friendly',
          color: Colors.green,
        );
      case 'professional':
        return _PersonalityConfig(
          icon: Icons.business_center,
          label: 'Professional',
          color: Colors.blue,
        );
      case 'mystical':
        return _PersonalityConfig(
          icon: Icons.auto_awesome,
          label: 'Mystical',
          color: Colors.purple,
        );
      default:
        return _PersonalityConfig(
          icon: Icons.face,
          label: personality,
          color: Colors.grey,
        );
    }
  }
}

class _ConnectionIndicator extends StatelessWidget {
  final bool isOnline;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 8,
      height: 8,
      decoration: BoxDecoration(
        color: isOnline ? Colors.green : Colors.red,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(
            color: (isOnline ? Colors.green : Colors.red).withOpacity(0.5),
            blurRadius: 4,
            spreadRadius: 1,
          ),
        ],
      ),
    );
  }
}

class _PremiumBadge extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.amber.shade400, Colors.amber.shade700],
        ),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.star, size: 12, color: Colors.white),
          SizedBox(width: 2),
          Text(
            'PRO',
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}

// Helper classes
class CosmicSettings {
  final String mode;
  final String personality;
  final bool isOnline;
  final bool isPremium;

  CosmicSettings({
    required this.mode,
    required this.personality,
    required this.isOnline,
    required this.isPremium,
  });
}

class _ModeConfig {
  final IconData icon;
  final String label;
  final Color color;

  _ModeConfig({
    required this.icon,
    required this.label,
    required this.color,
  });
}

class _PersonalityConfig {
  final IconData icon;
  final String label;
  final Color color;

  _PersonalityConfig({
    required this.icon,
    required this.label,
    required this.color,
  });
}
```

### Integración en CosmicCoachChatScreen

```dart
// Agregar en cosmic_coach_chat_screen.dart
// Después del AppBar, antes del chat

Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(...),
    body: Column(
      children: [
        // ✅ NUEVO: Status Panel
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Center(
            child: CosmicStatusPanel(),
          ),
        ),

        Divider(height: 1),

        // Chat messages
        Expanded(
          child: _buildMessageList(),
        ),

        // Input field
        _buildInputField(),
      ],
    ),
  );
}
```

### Traducciones necesarias

```json
// Agregar a app_en.arb
"cosmicStatusQuick": "Quick Mode",
"cosmicStatusBalanced": "Balanced Mode",
"cosmicStatusDetailed": "Detailed Mode",
"cosmicStatusOnline": "Online",
"cosmicStatusOffline": "Offline",
"cosmicStatusPremium": "Premium Active"

// Y equivalentes en ES, DE, FR, IT, PT
```

---

## 📋 AGENTE 3: PROFILE SYSTEM ARCHITECT

### Objetivo
Crear sistema de perfiles cósmicos con presets predefinidos.

### Modelo de datos

```dart
// lib/models/cosmic_profile.dart

/// 🌟 COSMIC PROFILE
/// =================
/// Representa un perfil de configuración del Cosmic Coach
///
/// Perfiles disponibles:
/// - Starter: Para usuarios nuevos, simple y rápido
/// - Power User: Para usuarios avanzados, balanceado
/// - Mystic: Para usuarios premium, máximo detalle

enum CosmicProfile {
  starter,
  powerUser,
  mystic,
  custom,
}

extension CosmicProfileExtension on CosmicProfile {
  String get name {
    switch (this) {
      case CosmicProfile.starter:
        return 'Starter';
      case CosmicProfile.powerUser:
        return 'Power User';
      case CosmicProfile.mystic:
        return 'Mystic';
      case CosmicProfile.custom:
        return 'Custom';
    }
  }

  String get description {
    switch (this) {
      case CosmicProfile.starter:
        return 'Quick responses, friendly tone. Perfect for beginners.';
      case CosmicProfile.powerUser:
        return 'Balanced responses, professional tone. For daily users.';
      case CosmicProfile.mystic:
        return 'Detailed responses, mystical tone. Maximum cosmic insight.';
      case CosmicProfile.custom:
        return 'Your personalized configuration.';
    }
  }

  IconData get icon {
    switch (this) {
      case CosmicProfile.starter:
        return Icons.rocket_launch;
      case CosmicProfile.powerUser:
        return Icons.bolt;
      case CosmicProfile.mystic:
        return Icons.auto_awesome;
      case CosmicProfile.custom:
        return Icons.tune;
    }
  }

  Color get color {
    switch (this) {
      case CosmicProfile.starter:
        return Colors.green;
      case CosmicProfile.powerUser:
        return Colors.blue;
      case CosmicProfile.mystic:
        return Colors.purple;
      case CosmicProfile.custom:
        return Colors.orange;
    }
  }
}

/// Preset de configuración para cada perfil
class CosmicProfilePreset {
  final CosmicProfile profile;
  final String chatMode;
  final String coachPersonality;
  final bool showQuickReplies;
  final bool autoSaveConversations;
  final bool preferBackendAI;
  final int dailyMessageLimit;

  const CosmicProfilePreset({
    required this.profile,
    required this.chatMode,
    required this.coachPersonality,
    required this.showQuickReplies,
    required this.autoSaveConversations,
    required this.preferBackendAI,
    required this.dailyMessageLimit,
  });

  /// Presets predefinidos
  static const starter = CosmicProfilePreset(
    profile: CosmicProfile.starter,
    chatMode: 'quick',
    coachPersonality: 'friendly',
    showQuickReplies: true,
    autoSaveConversations: false,
    preferBackendAI: false,
    dailyMessageLimit: 10,
  );

  static const powerUser = CosmicProfilePreset(
    profile: CosmicProfile.powerUser,
    chatMode: 'balanced',
    coachPersonality: 'professional',
    showQuickReplies: true,
    autoSaveConversations: true,
    preferBackendAI: false,
    dailyMessageLimit: 25,
  );

  static const mystic = CosmicProfilePreset(
    profile: CosmicProfile.mystic,
    chatMode: 'detailed',
    coachPersonality: 'mystical',
    showQuickReplies: false,
    autoSaveConversations: true,
    preferBackendAI: true,
    dailyMessageLimit: 50,
  );

  static CosmicProfilePreset getPreset(CosmicProfile profile) {
    switch (profile) {
      case CosmicProfile.starter:
        return starter;
      case CosmicProfile.powerUser:
        return powerUser;
      case CosmicProfile.mystic:
        return mystic;
      case CosmicProfile.custom:
        throw Exception('Custom profile has no preset');
    }
  }
}
```

### Servicio de perfiles

```dart
// lib/services/cosmic_profile_service.dart

/// 🎯 COSMIC PROFILE SERVICE
/// =========================
/// Gestiona los perfiles de configuración del Cosmic Coach
///
/// Responsabilidades:
/// - Detectar perfil actual del usuario
/// - Aplicar preset de perfil
/// - Cambiar entre perfiles
/// - Guardar perfil personalizado

class CosmicProfileService extends BaseSingletonService {
  static const _profileKey = 'cosmic_coach_profile';

  final PreferencesService _prefsService;

  CosmicProfileService(this._prefsService) : super('CosmicProfileService');

  /// Obtener perfil actual
  Future<CosmicProfile> getCurrentProfile() async {
    try {
      final profileName = await _prefsService.getString(_profileKey);

      if (profileName == null) {
        // Si no hay perfil guardado, detectar automáticamente
        return await _detectProfile();
      }

      return CosmicProfile.values.firstWhere(
        (p) => p.name.toLowerCase() == profileName.toLowerCase(),
        orElse: () => CosmicProfile.starter,
      );
    } catch (e) {
      logError('Error getting current profile', e);
      return CosmicProfile.starter;
    }
  }

  /// Aplicar preset de perfil
  Future<void> applyProfile(CosmicProfile profile) async {
    try {
      if (profile == CosmicProfile.custom) {
        logInfo('Cannot apply custom profile preset');
        return;
      }

      final preset = CosmicProfilePreset.getPreset(profile);

      // Aplicar todas las configuraciones del preset
      await _prefsService.setChatMode(preset.chatMode);
      await _prefsService.setCoachPersonality(preset.coachPersonality);
      await _prefsService.setShowQuickReplies(preset.showQuickReplies);
      await _prefsService.setAutoSaveConversations(preset.autoSaveConversations);
      await _prefsService.setPreferBackend(preset.preferBackendAI);
      await _prefsService.setDailyMessageLimit(preset.dailyMessageLimit);

      // Guardar perfil activo
      await _prefsService.setString(_profileKey, profile.name);

      logInfo('Applied profile: ${profile.name}');
    } catch (e) {
      logError('Error applying profile', e);
      rethrow;
    }
  }

  /// Detectar perfil apropiado según datos del usuario
  Future<CosmicProfile> _detectProfile() async {
    try {
      // Leer configuración actual
      final mode = await _prefsService.getChatMode();
      final personality = await _prefsService.getCoachPersonality();
      final isPremium = await _checkPremiumStatus();

      // Detectar perfil que más se parece
      if (mode == 'quick' && personality == 'friendly') {
        return CosmicProfile.starter;
      } else if (mode == 'detailed' && personality == 'mystical' && isPremium) {
        return CosmicProfile.mystic;
      } else if (mode == 'balanced' && personality == 'professional') {
        return CosmicProfile.powerUser;
      } else {
        return CosmicProfile.custom;
      }
    } catch (e) {
      logError('Error detecting profile', e);
      return CosmicProfile.starter;
    }
  }

  /// Verificar si configuración actual coincide con algún preset
  Future<bool> isUsingPreset() async {
    try {
      final currentProfile = await getCurrentProfile();

      if (currentProfile == CosmicProfile.custom) {
        return false;
      }

      final preset = CosmicProfilePreset.getPreset(currentProfile);

      // Comparar configuración actual con preset
      final mode = await _prefsService.getChatMode();
      final personality = await _prefsService.getCoachPersonality();
      final quickReplies = await _prefsService.getShowQuickReplies();
      final autoSave = await _prefsService.getAutoSaveConversations();

      return mode == preset.chatMode &&
          personality == preset.coachPersonality &&
          quickReplies == preset.showQuickReplies &&
          autoSave == preset.autoSaveConversations;
    } catch (e) {
      logError('Error checking preset match', e);
      return false;
    }
  }

  /// Marcar como perfil personalizado
  Future<void> markAsCustom() async {
    try {
      await _prefsService.setString(_profileKey, CosmicProfile.custom.name);
      logInfo('Marked profile as custom');
    } catch (e) {
      logError('Error marking as custom', e);
    }
  }

  Future<bool> _checkPremiumStatus() async {
    // TODO: Implementar check de premium real
    return false;
  }
}

/// Provider de CosmicProfileService
final cosmicProfileServiceProvider = Provider<CosmicProfileService>((ref) {
  final prefsService = ref.watch(preferencesServiceProvider);
  return CosmicProfileService(prefsService);
});
```

### UI: Sección de perfiles en Settings

```dart
// Agregar en cosmic_coach_settings_screen.dart

// Después de la sección BEHAVIOR, antes de INTERFACE

// ========== SECCIÓN: COSMIC PROFILES ==========
SettingSectionHeader(
  icon: Icons.person,
  title: 'Cosmic Profiles', // TODO: Add to l10n
  iconColor: _getAdaptiveColor(context, isPrimary: true),
),
const SizedBox(height: 12),

// Profile Selector
SettingCard(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(
        'Quick Setup', // TODO: Add to l10n
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
          fontWeight: FontWeight.w600,
        ),
      ),
      const SizedBox(height: 8),
      Text(
        'Choose a profile to quickly configure your coach', // TODO: Add to l10n
        style: Theme.of(context).textTheme.bodySmall,
      ),
      const SizedBox(height: 16),

      // Profile cards
      Row(
        children: [
          Expanded(
            child: _ProfileCard(
              profile: CosmicProfile.starter,
              isSelected: _currentProfile == CosmicProfile.starter,
              onTap: () => _applyProfile(CosmicProfile.starter),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: _ProfileCard(
              profile: CosmicProfile.powerUser,
              isSelected: _currentProfile == CosmicProfile.powerUser,
              onTap: () => _applyProfile(CosmicProfile.powerUser),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: _ProfileCard(
              profile: CosmicProfile.mystic,
              isSelected: _currentProfile == CosmicProfile.mystic,
              isLocked: !isPremium,
              onTap: () => _applyProfile(CosmicProfile.mystic),
            ),
          ),
        ],
      ),

      if (_currentProfile == CosmicProfile.custom) ...[
        const SizedBox(height: 12),
        Container(
          padding: EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.orange.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.orange.withOpacity(0.3)),
          ),
          child: Row(
            children: [
              Icon(Icons.tune, color: Colors.orange, size: 20),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Using custom configuration', // TODO: Add to l10n
                  style: TextStyle(
                    color: Colors.orange.shade700,
                    fontSize: 13,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    ],
  ),
),

const SizedBox(height: 24),
```

### Widget ProfileCard

```dart
class _ProfileCard extends StatelessWidget {
  final CosmicProfile profile;
  final bool isSelected;
  final bool isLocked;
  final VoidCallback onTap;

  const _ProfileCard({
    required this.profile,
    required this.isSelected,
    this.isLocked = false,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: isLocked ? null : onTap,
      child: Container(
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isSelected
              ? profile.color.withOpacity(0.2)
              : (isDarkMode ? Color(0xFF1A0B3E) : Colors.grey.shade100),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected
                ? profile.color
                : (isDarkMode ? Colors.purple.shade700 : Colors.grey.shade300),
            width: isSelected ? 2 : 1,
          ),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                Icon(
                  profile.icon,
                  size: 32,
                  color: isLocked
                      ? Colors.grey
                      : (isSelected ? profile.color : Colors.grey.shade600),
                ),
                if (isLocked)
                  Icon(Icons.lock, size: 16, color: Colors.grey),
              ],
            ),
            SizedBox(height: 8),
            Text(
              profile.name,
              style: TextStyle(
                fontSize: 12,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                color: isLocked
                    ? Colors.grey
                    : (isSelected ? profile.color : null),
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 🎯 ORDEN DE EJECUCIÓN

### Fase 1: Preparación (5 min)
1. Crear branches para cada agente (opcional)
2. Distribuir archivos a modificar
3. Sincronizar dependencias entre agentes

### Fase 2: Desarrollo paralelo (2-3 horas)
- **AGENTE 1**: Trabaja en `horoscope_chat_service.dart`
- **AGENTE 2**: Trabaja en `cosmic_status_panel.dart` + integración
- **AGENTE 3**: Trabaja en `cosmic_profile.dart` + service + UI

### Fase 3: Integración (30 min)
1. AGENTE 2 termina primero → integra en chat screen
2. AGENTE 1 termina segundo → testing de modos
3. AGENTE 3 termina tercero → integra en settings
4. Testing conjunto de las 3 features

### Fase 4: Testing final (30 min)
- Probar en iPhone físico
- Verificar interacción entre features
- Validar traducciones
- Verificar dark mode

---

## 📊 MÉTRICAS DE ÉXITO

### Feature 1: Engine Modes
- [ ] Quick mode: 0 llamadas backend
- [ ] Balanced mode: Mix inteligente local/backend
- [ ] Detailed mode: Preferencia backend cuando premium
- [ ] Fallback a local siempre funciona

### Feature 2: Status Panel
- [ ] Muestra modo actual correctamente
- [ ] Muestra personalidad correctamente
- [ ] Indicador online/offline funciona
- [ ] Premium badge aparece cuando corresponde
- [ ] Se actualiza cuando cambian settings

### Feature 3: Profile System
- [ ] 3 perfiles funcionan correctamente
- [ ] Aplicar perfil cambia todas las settings
- [ ] Detecta perfil custom cuando usuario modifica
- [ ] Mystic profile bloqueado para free users
- [ ] UI de perfiles responsive y clara

---

## 🚀 COMANDO DE INICIO

Una vez revisado el plan:

```
EJECUTAR PLAN MULTIAGENTE FINAL:
- AGENTE 1: Engine Master
- AGENTE 2: UI Designer
- AGENTE 3: Profile Architect

TIEMPO ESTIMADO: 2-3 horas
GO! 🚀
```

---

## 📝 NOTAS IMPORTANTES

### Dependencias entre agentes
- AGENTE 2 y 3 son 100% independientes (pueden correr en paralelo puro)
- AGENTE 1 puede afectar behavior del Status Panel de AGENTE 2 (pero no bloquea)
- Testing final requiere los 3 completos

### Prioridad si hay que elegir
1. **AGENTE 2** (Status Panel) - IMPACTO VISUAL INMEDIATO
2. **AGENTE 1** (Engine Modes) - MEJORA FUNCIONAL
3. **AGENTE 3** (Profiles) - NICE-TO-HAVE

### Rollback strategy
Cada agente trabaja en archivos separados, fácil rollback individual si algo falla.

---

**¿Listo para ejecutar?** 🎯

Responde con:
- **"GO"** → Ejecuto los 3 agentes ahora
- **"GO 1"** → Solo AGENTE 1 (Engine)
- **"GO 2"** → Solo AGENTE 2 (Status Panel)
- **"GO 3"** → Solo AGENTE 3 (Profiles)
- **"GO 2+3"** → AGENTE 2 y 3 en paralelo (más rápido, sin Engine)

