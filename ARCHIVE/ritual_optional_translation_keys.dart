// ============================================================================
// OPTIONAL TRANSLATION KEYS FOR RITUAL GOALS
// ============================================================================
//
// NOTE: These keys are NOT currently needed in the codebase.
// They are provided for future enhancement if "rituals" become a first-class
// feature with special UI elements or functionality.
//
// Current Status: Ritual goals work through normal goal completion flow.
// No special "perform ritual" button or functionality exists.
//
// Add these to app_localizations_en.dart and app_localizations_es.dart
// only if you decide to enhance ritual goals with special features.
// ============================================================================

// ===================
// ENGLISH TRANSLATIONS
// ===================
// Add to: lib/l10n/app_localizations_en.dart

class RitualTranslationsEN {
  // Basic ritual labels
  static const String ritualGoal = 'Ritual Goal';
  static const String ritual = 'Ritual';
  static const String rituals = 'Rituals';

  // Actions
  static const String performRitual = 'Perform Ritual';
  static const String startRitual = 'Start Ritual';
  static const String completeRitual = 'Complete Ritual';

  // Status
  static const String ritualCompleted = 'Ritual Completed';
  static const String ritualInProgress = 'Ritual in Progress';
  static const String ritualNotStarted = 'Ritual Not Started';

  // Descriptions
  static const String ritualDescription = 'A transformative practice for your zodiac sign';
  static const String ritualGoalDescription = 'Complete this goal with a cosmic ritual';
  static const String ritualCompletionMessage = 'Congratulations! You\'ve completed your cosmic ritual.';

  // Specific ritual types
  static const String selfCareRitual = 'Self-Care Ritual';
  static const String gratitudeRitual = 'Gratitude Ritual';
  static const String releaseRitual = 'Release Ritual';
  static const String healingRitual = 'Healing Ritual';
  static const String manifestationRitual = 'Manifestation Ritual';
  static const String connectionRitual = 'Connection Ritual';

  // Categories
  static const String wellnessRituals = 'Wellness Rituals';
  static const String spiritualRituals = 'Spiritual Rituals';
  static const String emotionalRituals = 'Emotional Rituals';
  static const String physicalRituals = 'Physical Rituals';

  // Instructions
  static const String ritualInstructions = 'Follow these steps to complete your ritual:';
  static const String ritualPrepare = 'Prepare a quiet space';
  static const String ritualFocus = 'Focus on your intention';
  static const String ritualReflect = 'Reflect on your experience';

  // Badge/Labels
  static const String ritualBadge = 'RITUAL';
  static const String cosmicRitual = 'Cosmic Ritual';
  static const String zodiacRitual = 'Zodiac Ritual';

  // Time-based
  static const String dailyRitual = 'Daily Ritual';
  static const String weeklyRitual = 'Weekly Ritual';
  static const String monthlyRitual = 'Monthly Ritual';
  static const String lunarRitual = 'Lunar Ritual';
  static const String fullMoonRitual = 'Full Moon Ritual';
  static const String newMoonRitual = 'New Moon Ritual';

  // Completion messages
  static const String ritualCompletedTitle = 'Ritual Complete!';
  static const String ritualCompletedSubtitle = 'You\'ve honored your cosmic journey';
  static const String ritualReward = 'You\'ve earned cosmic energy for completing this ritual';
}

// ===================
// SPANISH TRANSLATIONS
// ===================
// Add to: lib/l10n/app_localizations_es.dart

class RitualTranslationsES {
  // Etiquetas básicas de ritual
  static const String ritualGoal = 'Meta Ritual';
  static const String ritual = 'Ritual';
  static const String rituals = 'Rituales';

  // Acciones
  static const String performRitual = 'Realizar Ritual';
  static const String startRitual = 'Comenzar Ritual';
  static const String completeRitual = 'Completar Ritual';

  // Estado
  static const String ritualCompleted = 'Ritual Completado';
  static const String ritualInProgress = 'Ritual en Progreso';
  static const String ritualNotStarted = 'Ritual No Iniciado';

  // Descripciones
  static const String ritualDescription = 'Una práctica transformadora para tu signo zodiacal';
  static const String ritualGoalDescription = 'Completa esta meta con un ritual cósmico';
  static const String ritualCompletionMessage = '¡Felicitaciones! Has completado tu ritual cósmico.';

  // Tipos específicos de ritual
  static const String selfCareRitual = 'Ritual de Auto-Cuidado';
  static const String gratitudeRitual = 'Ritual de Gratitud';
  static const String releaseRitual = 'Ritual de Liberación';
  static const String healingRitual = 'Ritual de Sanación';
  static const String manifestationRitual = 'Ritual de Manifestación';
  static const String connectionRitual = 'Ritual de Conexión';

  // Categorías
  static const String wellnessRituals = 'Rituales de Bienestar';
  static const String spiritualRituals = 'Rituales Espirituales';
  static const String emotionalRituals = 'Rituales Emocionales';
  static const String physicalRituals = 'Rituales Físicos';

  // Instrucciones
  static const String ritualInstructions = 'Sigue estos pasos para completar tu ritual:';
  static const String ritualPrepare = 'Prepara un espacio tranquilo';
  static const String ritualFocus = 'Enfócate en tu intención';
  static const String ritualReflect = 'Reflexiona sobre tu experiencia';

  // Insignias/Etiquetas
  static const String ritualBadge = 'RITUAL';
  static const String cosmicRitual = 'Ritual Cósmico';
  static const String zodiacRitual = 'Ritual Zodiacal';

  // Basado en tiempo
  static const String dailyRitual = 'Ritual Diario';
  static const String weeklyRitual = 'Ritual Semanal';
  static const String monthlyRitual = 'Ritual Mensual';
  static const String lunarRitual = 'Ritual Lunar';
  static const String fullMoonRitual = 'Ritual de Luna Llena';
  static const String newMoonRitual = 'Ritual de Luna Nueva';

  // Mensajes de completitud
  static const String ritualCompletedTitle = '¡Ritual Completado!';
  static const String ritualCompletedSubtitle = 'Has honrado tu viaje cósmico';
  static const String ritualReward = 'Has ganado energía cósmica por completar este ritual';
}

// ============================================================================
// USAGE EXAMPLE (if implemented in future)
// ============================================================================

/*
// In goal_detail_screen.dart
if (goal.title.toLowerCase().contains('ritual')) {
  // Show ritual badge
  Container(
    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
    decoration: BoxDecoration(
      color: Colors.purple,
      borderRadius: BorderRadius.circular(12),
    ),
    child: Text(
      AppLocalizations.of(context)!.ritualBadge,
      style: TextStyle(color: Colors.white, fontSize: 10),
    ),
  )
}

// Special ritual completion button
ElevatedButton(
  onPressed: () => _showRitualCompletionDialog(),
  child: Text(AppLocalizations.of(context)!.performRitual),
)

// Ritual completion dialog
void _showRitualCompletionDialog() {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(AppLocalizations.of(context)!.ritualCompletedTitle),
      content: Text(AppLocalizations.of(context)!.ritualCompletedSubtitle),
      actions: [
        ElevatedButton(
          onPressed: () {
            _completeGoal();
            Navigator.pop(context);
          },
          child: Text(AppLocalizations.of(context)!.completeRitual),
        ),
      ],
    ),
  );
}
*/

// ============================================================================
// INTEGRATION INSTRUCTIONS
// ============================================================================

/*
To add these translations to the app:

1. Open lib/l10n/app_localizations_en.dart
2. Add the English translations as getter methods:

  @override
  String get ritualGoal => 'Ritual Goal';

  @override
  String get performRitual => 'Perform Ritual';

  // ... etc

3. Open lib/l10n/app_localizations_es.dart
4. Add the Spanish translations:

  @override
  String get ritualGoal => 'Meta Ritual';

  @override
  String get performRitual => 'Realizar Ritual';

  // ... etc

5. Update assets/l10n/app_en.arb:

  "ritualGoal": "Ritual Goal",
  "@ritualGoal": {
    "description": "Label for ritual-type goals"
  },
  "performRitual": "Perform Ritual",
  "@performRitual": {
    "description": "Action to perform a ritual"
  },

6. Update assets/l10n/app_es.arb:

  "ritualGoal": "Meta Ritual",
  "@ritualGoal": {
    "description": "Etiqueta para metas tipo ritual"
  },
  "performRitual": "Realizar Ritual",
  "@performRitual": {
    "description": "Acción para realizar un ritual"
  },

7. Run: flutter pub run intl_utils:generate

8. Restart the app
*/
