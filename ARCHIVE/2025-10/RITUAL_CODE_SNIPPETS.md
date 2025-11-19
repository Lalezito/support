# Ritual Functionality - Code Snippets Reference

This document shows the exact code locations where "ritual" appears in the codebase.

---

## File: cosmic_coach_goal_generator.dart

**Location:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/cosmic_coach_goal_generator.dart`

### Snippet 1: Taurus Ritual Goal (Lines 84-88)

```dart
'Taurus': [
  {
    'es': {'title': 'Ritual de Auto-Cuidado Sensorial', 'description': 'Conecta con tus 5 sentidos: baño aromático o masaje'},
    'en': {'title': 'Sensory Self-Care Ritual', 'description': 'Connect with your 5 senses: aromatic bath or massage'},
    'category': 'wellness',
    'difficulty': 'easy',
  },
  {
    'es': {'title': 'Construir Hábito Financiero', 'description': 'Revisa tus finanzas y ahorra 10% de tus ingresos'},
    'en': {'title': 'Build Financial Habit', 'description': 'Review finances and save 10% of your income'},
    'category': 'finance',
    'difficulty': 'medium',
  },
  // ... more Taurus goals
],
```

**Analysis:**
- ✅ Bilingual: Spanish and English both present
- ✅ Properly structured: Uses standard goal template format
- 📝 Note: "Ritual" is part of the title, not a special property

---

### Snippet 2: Cancer Ritual Goal (Lines 126-130)

```dart
'Cancer': [
  {
    'es': {'title': 'Ritual de Gratitud Familiar', 'description': 'Expresa amor a tu familia o amigos cercanos'},
    'en': {'title': 'Family Gratitude Ritual', 'description': 'Express love to your family or close friends'},
    'category': 'relationships',
    'difficulty': 'easy',
  },
  {
    'es': {'title': 'Sanación Emocional con Agua', 'description': 'Baño lunar, natación o meditación junto al agua'},
    'en': {'title': 'Emotional Healing with Water', 'description': 'Lunar bath, swimming, or meditation by water'},
    'category': 'wellness',
    'difficulty': 'easy',
  },
  // ... more Cancer goals
],
```

**Analysis:**
- ✅ Category: 'relationships' (not a special "ritual" category)
- ✅ Difficulty: 'easy' (standard difficulty level)
- 📝 Note: "Gratitud Familiar" goal happens to include ritual in title

---

### Snippet 3: Full Moon Ritual Goal (Lines 348-352)

```dart
'full_moon': [
  {
    'es': {'title': 'Ritual de Liberación', 'description': 'Luna Llena: suelta lo que ya no sirve'},
    'en': {'title': 'Release Ritual', 'description': 'Full Moon: let go of what no longer serves'},
    'category': 'healing',
    'difficulty': 'medium',
  },
],
```

**Analysis:**
- 🌙 Lunar phase trigger: Generated during full moon
- ✅ Category: 'healing' (not "ritual")
- 📝 Note: Most thematically "ritual-like" goal

---

## File: goal_detail_screen.dart

**Location:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/goal_planner/goal_detail_screen.dart`

### Snippet 4: Goal Actions Menu (Lines 534-571)

```dart
/// Muestra el menú de opciones
void _showOptionsMenu(BuildContext context) {
  showModalBottomSheet(
    context: context,
    builder: (context) {
      return SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.pause),
              title: const Text('Pausar Meta'),
              onTap: () {
                Navigator.pop(context);
                _pauseGoal();
              },
            ),
            ListTile(
              leading: const Icon(Icons.check, color: Colors.green),
              title: const Text('Marcar como Completada'),
              onTap: () {
                Navigator.pop(context);
                _completeGoal();
              },
            ),
            ListTile(
              leading: const Icon(Icons.delete, color: Colors.red),
              title: const Text('Eliminar Meta'),
              onTap: () {
                Navigator.pop(context);
                _showDeleteConfirmation();
              },
            ),
          ],
        ),
      );
    },
  );
}
```

**Analysis:**
- ❌ NO "Realizar Ritual" option
- ❌ NO "Perform Ritual" option
- ✅ Only standard goal actions:
  - Pause Goal
  - Mark as Completed
  - Delete Goal

---

### Snippet 5: Floating Action Button (Lines 74-79)

```dart
floatingActionButton: FloatingActionButton.extended(
  onPressed: () => _recordCheckIn(context),
  backgroundColor: CosmicColors.stellarGold,
  icon: const Icon(Icons.check_circle),
  label: const Text('Record Check-in'),
),
```

**Analysis:**
- ❌ NO "Perform Ritual" button
- ✅ Only "Record Check-in" button exists
- 📝 Note: Same button for ALL goals, including ritual-themed ones

---

## File: cosmic_goal_unified.dart

**Location:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/models/cosmic_goal_unified.dart`

### Snippet 6: Goal Model Properties (Lines 11-23)

```dart
class CosmicGoalUnified {
  final String id;
  final String title;
  final String description;
  final String category; // String: 'fitness', 'mindfulness', etc.
  final String difficulty; // String: 'easy', 'medium', 'hard'
  final double progress; // 0.0 to 1.0
  final String suggestedBy; // 'Cosmic Coach', 'Lunar Cycle', 'User'
  final DateTime createdAt;
  final DateTime? completedAt;
  final DateTime? targetDate;
  final bool isArchived;

  // ... constructor and methods
}
```

**Analysis:**
- ❌ NO `isRitual` property
- ❌ NO `ritualType` property
- ❌ NO ritual-specific fields
- 📝 Note: "Ritual de..." goals use the same model as all other goals

---

### Snippet 7: Goal Completion Method (Lines 218-224)

```dart
/// Marcar como completado
CosmicGoalUnified markCompleted() {
  return copyWith(
    progress: 1.0,
    completedAt: DateTime.now(),
  );
}
```

**Analysis:**
- ❌ NO special ritual completion logic
- ✅ Simple progress and timestamp update
- 📝 Note: Same completion method for all goals

---

## File: goal_planner_home_screen.dart (Premium version)

**Location:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/features/premium/screens/goal_planner/goal_planner_home_screen.dart`

### Snippet 8: Goal Card Display (Lines 432-578)

```dart
Widget _buildGoalCard(Goal goal) {
  final progress = _calculateProgress(goal);
  final statusColor = _getStatusColor(goal.status);
  final statusIcon = _getStatusIcon(goal.status);

  return Card(
    // ... card styling
    child: InkWell(
      onTap: () => _navigateToGoalDetail(goal),
      child: Container(
        child: Padding(
          child: Column(
            children: [
              // Header with goal title
              Text(
                goal.mainGoal.title, // ← "Ritual de..." appears here
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),

              // Progress bar
              LinearProgressIndicator(
                value: progress / 100,
                // ...
              ),

              // NO special ritual indicators
              // NO ritual badges
              // NO "perform ritual" button
            ],
          ),
        ),
      ),
    ),
  );
}
```

**Analysis:**
- ✅ Displays goal title (which may contain "ritual")
- ❌ NO special UI for ritual goals
- ❌ NO ritual badge or indicator
- 📝 Note: Ritual goals look identical to other goals

---

## Search Results: "performRitual" Method

```bash
$ grep -r "performRitual" zodiac_app/lib/
# No results found
```

**Analysis:**
- ❌ NO `performRitual()` method exists anywhere in codebase
- ❌ NO `realizarRitual()` method exists
- ❌ NO `startRitual()` method exists

---

## Search Results: "ritual" Property

```bash
$ grep -r "isRitual\|ritual:" zodiac_app/lib/models/
# No results found (except in comments and strings)
```

**Analysis:**
- ❌ NO boolean `isRitual` property in any model
- ❌ NO `ritualType` enum or property
- ❌ NO ritual-specific data structures

---

## Translation Files Check

### File: app_localizations_es.dart

```bash
$ grep -i "ritual" zodiac_app/lib/l10n/app_localizations_es.dart
# Result: Only "spirituality" = "Espiritualidad"
```

**Analysis:**
- ❌ NO "performRitual" translation key
- ❌ NO "realizarRitual" translation key
- ❌ NO ritual-specific translations
- 📝 Note: All ritual strings are hardcoded in goal_generator.dart

---

## Complete List of Files Containing "Ritual"

From our grep search, these files contain "ritual":

### 1. Goal Generation:
- ✅ `cosmic_coach_goal_generator.dart` - Contains goal templates

### 2. Localization (only "spirituality"):
- `app_localizations.dart`
- `app_localizations_en.dart`
- `app_localizations_es.dart`
- `app_localizations_pt.dart`
- `app_localizations_fr.dart`
- `app_localizations_de.dart`
- `app_localizations_it.dart`

### 3. ARB files (only "spirituality"):
- `app_en.arb`
- `app_es.arb`
- `app_pt.arb`
- `app_fr.arb`
- `app_de.arb`
- `app_it.arb`

### 4. Documentation:
- Various service files and documentation containing "spiritual" references

**Key Finding:** Only ONE file has actual "ritual" goal templates - the goal generator!

---

## Code That DOESN'T Exist (But Might Be Expected)

### ❌ This code does NOT exist:

```dart
// DOES NOT EXIST - Example of what ISN'T there

class GoalDetailScreen extends StatefulWidget {
  // ...

  void _performRitual() {  // ❌ DOESN'T EXIST
    showDialog(
      context: context,
      builder: (context) => RitualCompletionDialog(  // ❌ DOESN'T EXIST
        ritual: goal,
        onComplete: () {
          _completeGoal();
        },
      ),
    );
  }

  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // ...
          if (goal.isRitual) {  // ❌ PROPERTY DOESN'T EXIST
            ElevatedButton(
              onPressed: _performRitual,  // ❌ METHOD DOESN'T EXIST
              child: Text('Realizar Ritual'),  // ❌ BUTTON DOESN'T EXIST
            ),
          }
        ],
      ),
    );
  }
}
```

### ❌ This model property does NOT exist:

```dart
// DOES NOT EXIST - Example of what ISN'T there

class CosmicGoalUnified {
  final String id;
  final String title;
  final bool isRitual;  // ❌ DOESN'T EXIST
  final RitualType? ritualType;  // ❌ DOESN'T EXIST
  final String? ritualInstructions;  // ❌ DOESN'T EXIST

  // ...
}

enum RitualType {  // ❌ DOESN'T EXIST
  selfCare,
  gratitude,
  release,
  healing,
}
```

---

## Summary of Code Locations

| Feature | Exists? | File | Line(s) |
|---------|---------|------|---------|
| Taurus ritual goal | ✅ Yes | cosmic_coach_goal_generator.dart | 84-88 |
| Cancer ritual goal | ✅ Yes | cosmic_coach_goal_generator.dart | 126-130 |
| Full moon ritual goal | ✅ Yes | cosmic_coach_goal_generator.dart | 348-352 |
| performRitual() method | ❌ No | N/A | N/A |
| isRitual property | ❌ No | N/A | N/A |
| "Realizar Ritual" button | ❌ No | N/A | N/A |
| Ritual completion dialog | ❌ No | N/A | N/A |
| Ritual badge/indicator | ❌ No | N/A | N/A |
| Translation keys | ❌ No | N/A | N/A |

---

## Conclusion

**Only 3 occurrences of "ritual" in goal titles exist:**

1. Taurus: "Ritual de Auto-Cuidado Sensorial" / "Sensory Self-Care Ritual"
2. Cancer: "Ritual de Gratitud Familiar" / "Family Gratitude Ritual"
3. Full Moon: "Ritual de Liberación" / "Release Ritual"

**No ritual-specific code exists anywhere else in the codebase.**

The word "ritual" is purely descriptive text in goal titles, not a functional element.
