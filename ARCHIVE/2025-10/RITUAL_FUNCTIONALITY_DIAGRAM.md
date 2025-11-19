# Ritual Functionality - Visual Flow Diagram

## Current Implementation (What Actually Exists)

```
┌─────────────────────────────────────────────────────────────┐
│                    COSMIC COACH                             │
│                  Goal Generator Service                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Generates goals based on:
                     │ - User's zodiac sign
                     │ - Lunar phase
                     │ - Date/season
                     │
                     ▼
      ┌──────────────────────────────────────┐
      │   GOAL TEMPLATES (Hardcoded)         │
      ├──────────────────────────────────────┤
      │ Taurus Goals:                        │
      │  ✓ "Ritual de Auto-Cuidado"         │
      │  ✓ "Build Financial Habit"          │
      │                                      │
      │ Cancer Goals:                        │
      │  ✓ "Ritual de Gratitud Familiar"    │
      │  ✓ "Cook with Love"                 │
      │                                      │
      │ Full Moon Goals:                     │
      │  ✓ "Ritual de Liberación"           │
      └──────────────┬───────────────────────┘
                     │
                     │ User selects goal
                     │
                     ▼
      ┌──────────────────────────────────────┐
      │      GOAL PLANNER SCREEN             │
      ├──────────────────────────────────────┤
      │                                      │
      │  📋 Goal: "Ritual de Gratitud       │
      │            Familiar"                 │
      │                                      │
      │  Status: Active                      │
      │  Progress: 45%                       │
      │                                      │
      │  [Record Check-in] ← Only button    │
      │                                      │
      └──────────────┬───────────────────────┘
                     │
                     │ User clicks check-in
                     │
                     ▼
      ┌──────────────────────────────────────┐
      │    GOAL CHECK-IN SCREEN              │
      ├──────────────────────────────────────┤
      │  What did you do today?              │
      │  ┌────────────────────────────────┐  │
      │  │ Called mom and told her I      │  │
      │  │ love her                       │  │
      │  └────────────────────────────────┘  │
      │                                      │
      │  [Submit Check-in]                   │
      └──────────────┬───────────────────────┘
                     │
                     │ Progress tracked
                     │
                     ▼
      ┌──────────────────────────────────────┐
      │   GOAL COMPLETED (Eventually)        │
      │                                      │
      │   🎉 Goal Complete!                  │
      │   "Ritual de Gratitud Familiar"      │
      │                                      │
      │   [OK]                               │
      └──────────────────────────────────────┘
```

---

## What Users MIGHT Think Exists (But Doesn't)

```
❌ THIS DOES NOT EXIST ❌

┌─────────────────────────────────────────┐
│      GOAL DETAIL SCREEN                 │
├─────────────────────────────────────────┤
│                                         │
│  Goal: "Ritual de Gratitud Familiar"   │
│                                         │
│  [Realizar Ritual] ← DOESN'T EXIST     │
│  [Record Check-in]                      │
│                                         │
└─────────────────────────────────────────┘
            │
            │ User clicks "Realizar Ritual"
            │
            ▼
┌─────────────────────────────────────────┐
│   RITUAL PERFORMANCE SCREEN             │
│                                         │
│   ✨ Special Animation ✨              │
│   🌙 Cosmic Ceremony 🌙                │
│                                         │
│   THIS SCREEN DOESN'T EXIST            │
└─────────────────────────────────────────┘
```

---

## Code Architecture - Where "Ritual" Appears

```
zodiac_app/
├── lib/
│   ├── services/
│   │   └── cosmic_coach_goal_generator.dart
│   │       │
│   │       └── Contains goal templates ✅
│   │           ├── Line 84: "Ritual de Auto-Cuidado Sensorial"
│   │           ├── Line 126: "Ritual de Gratitud Familiar"
│   │           └── Line 348: "Ritual de Liberación"
│   │
│   ├── screens/
│   │   ├── goal_planner/
│   │   │   ├── goal_planner_home_screen.dart
│   │   │   │   └── Shows list of goals ✅
│   │   │   │       (No ritual-specific code)
│   │   │   │
│   │   │   ├── goal_detail_screen.dart
│   │   │   │   └── Shows goal details ✅
│   │   │   │       Actions:
│   │   │   │       - Record Check-in
│   │   │   │       - Pause Goal
│   │   │   │       - Complete Goal
│   │   │   │       - Delete Goal
│   │   │   │       ❌ NO "Perform Ritual" button
│   │   │   │
│   │   │   └── goal_checkin_screen.dart
│   │   │       └── Records progress ✅
│   │   │           (No ritual-specific code)
│   │   │
│   │   └── cosmic_coach_screen.dart
│   │       └── Suggests goals ✅
│   │           (Uses goal_generator templates)
│   │
│   └── models/
│       └── cosmic_goal_unified.dart
│           └── Goal data model ✅
│               Properties:
│               - id
│               - title ← "Ritual de..." appears here
│               - description
│               - category
│               - difficulty
│               - progress
│               ❌ NO ritual-specific properties
```

---

## Translation Architecture

```
Current State (✅ Working):

cosmic_coach_goal_generator.dart
    │
    └── Hardcoded bilingual templates
        │
        ├── English: "Sensory Self-Care Ritual"
        └── Spanish: "Ritual de Auto-Cuidado Sensorial"
        │
        │ Directly stored in code
        │ No localization files needed
        │
        ▼
    Goal object created with correct language
    based on user's locale


Alternative Approach (Not currently used):

cosmic_coach_goal_generator.dart
    │
    └── Uses translation keys
        │
        ├── Key: 'taurus_self_care_ritual'
        │
        ▼
    app_localizations.dart
        │
        ├── EN: "Sensory Self-Care Ritual"
        └── ES: "Ritual de Auto-Cuidado Sensorial"
```

---

## What "Ritual" Means in Different Contexts

| Context | What "Ritual" Is | Example |
|---------|------------------|---------|
| **Goal Title** | Descriptive word | "Ritual de Gratitud Familiar" |
| **Category** | Type of activity | Wellness ritual, spiritual ritual |
| **Action** | ❌ DOESN'T EXIST | "Perform Ritual" button |
| **Feature** | ❌ DOESN'T EXIST | Special ritual completion flow |

---

## User Journey Comparison

### What Actually Happens:
```
1. User sees suggested goal: "Ritual de Gratitud Familiar"
2. User accepts goal
3. User records check-ins over several days
4. User marks goal complete
5. Goal shows as completed
```

### What User Might Expect (Based on Name):
```
1. User sees goal: "Ritual de Gratitud Familiar"
2. User clicks "Realizar Ritual" button ← DOESN'T EXIST
3. Special ritual screen appears ← DOESN'T EXIST
4. User performs guided ritual ← DOESN'T EXIST
5. Goal automatically completes ← DOESN'T HAPPEN
```

---

## Data Flow

```
┌──────────────────────────────────────────────────────────┐
│              cosmic_coach_goal_generator.dart            │
│                                                          │
│  zodiacGoals = {                                         │
│    'Taurus': [                                          │
│      {                                                  │
│        'es': {                                          │
│          'title': 'Ritual de Auto-Cuidado Sensorial',  │
│          'description': 'Conecta con tus 5 sentidos'   │
│        },                                               │
│        'en': {                                          │
│          'title': 'Sensory Self-Care Ritual',          │
│          'description': 'Connect with your 5 senses'   │
│        },                                               │
│        'category': 'wellness',                          │
│        'difficulty': 'easy'                             │
│      }                                                  │
│    ]                                                    │
│  }                                                      │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ Template data
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│              CosmicGoalUnified Model                     │
│                                                          │
│  CosmicGoalUnified(                                     │
│    title: "Ritual de Auto-Cuidado Sensorial",          │
│    description: "Conecta con tus 5 sentidos...",       │
│    category: "wellness",                                │
│    difficulty: "easy",                                  │
│    progress: 0.0,                                       │
│    suggestedBy: "Cosmic Coach"                         │
│  )                                                      │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ Goal object
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│                 Goal Planner Screen                      │
│                                                          │
│  Displays:                                              │
│  - Title: "Ritual de Auto-Cuidado Sensorial"           │
│  - Description                                          │
│  - Progress bar                                         │
│  - Check-in button                                      │
│                                                          │
│  ❌ NO special "ritual" UI elements                     │
└──────────────────────────────────────────────────────────┘
```

---

## The Confusion Explained

```
User sees this in Spanish:
┌─────────────────────────────────┐
│  📋 Ritual de Gratitud Familiar │
│                                 │
│  [Record Check-in]              │
└─────────────────────────────────┘

User thinks:
"'Ritual de...' = There must be a 'Realizar Ritual' button!"

Reality:
"Ritual de Gratitud Familiar" is just the GOAL NAME.
Like "Morning Jog" or "Read a Book" - it's descriptive.
No special ritual functionality exists.
```

---

## Summary Table

| Element | Exists? | Location | Purpose |
|---------|---------|----------|---------|
| "Ritual" in goal titles | ✅ Yes | goal_generator.dart | Descriptive name |
| Bilingual translations | ✅ Yes | goal_generator.dart | EN/ES support |
| "Perform Ritual" button | ❌ No | N/A | Doesn't exist |
| Ritual completion flow | ❌ No | N/A | Doesn't exist |
| Special ritual properties | ❌ No | N/A | Not in model |
| Ritual-specific tracking | ❌ No | N/A | Uses normal tracking |

---

## Conclusion

The word "ritual" is purely **descriptive** and appears in goal titles.
It does NOT represent a separate feature or functionality.

Users complete ritual-themed goals the same way as any other goal:
through regular check-ins and progress tracking.
