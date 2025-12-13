# GERMAN BIORHYTHM TRANSLATION - IMPLEMENTATION GUIDE

**Specialist:** German Translation Expert
**Date:** November 13, 2025
**Priority:** CRITICAL
**Time Estimate:** 2-3 hours

---

## QUICK START

### The Problem
`biorhythm_goal_generator.dart` has **hardcoded English** strings in microHabits, successIndicators, zodiac messages, and science explanations. These need German (de) translations.

### The Solution
The translations ALREADY EXIST in `biorhythm_micro_habits_translations.dart`! We just need to USE them instead of hardcoding.

---

## IMPLEMENTATION GUIDE

### STEP 1: Add Import to biorhythm_goal_generator.dart

**Location:** Top of file (after line 8)

```dart
import 'biorhythm_micro_habits_translations.dart'; // ADD THIS LINE
```

---

### STEP 2: Refactor Physical Peak Goal (Lines 53-119)

**Before (Hardcoded):**
```dart
static Map<String, dynamic> _physicalPeakGoal(
  String zodiacSign,
  BiorhythmResult bio,
  String languageCode,
) {
  return {
    'title': BiorhythmTranslations.physicalPeakTitle(languageCode),
    'description': BiorhythmTranslations.physicalPeakDesc(
      languageCode,
      bio.dayInCycle,
      bio.cycleLength,
      bio.percentage.toInt(),
    ),
    'category': 'fitness',
    'difficulty': HabitDifficulty.hard,
    'biorhythmType': 'physical',
    'biorhythmPhase': 'peak',
    'microHabits': [  // ❌ HARDCODED ENGLISH
      {
        'habit': 'Set a personal record (weight, distance, or time)',
        'when': 'Today while physical energy is at peak',
        'why': '75% of Olympic records were broken during peak physical phase',
        'difficulty': 'hard',
      },
      // ... more hardcoded items
    ],
    'successIndicators': [  // ❌ HARDCODED ENGLISH
      'Achieved personal record or milestone',
      'Completed intense physical activity',
      'Felt strong and energized during workout',
      'No unusual fatigue or pain',
    ],
    // ...
  };
}
```

**After (Using Translation System):**
```dart
static Map<String, dynamic> _physicalPeakGoal(
  String zodiacSign,
  BiorhythmResult bio,
  String languageCode,
) {
  return {
    'title': BiorhythmTranslations.physicalPeakTitle(languageCode),
    'description': BiorhythmTranslations.physicalPeakDesc(
      languageCode,
      bio.dayInCycle,
      bio.cycleLength,
      bio.percentage.toInt(),
    ),
    'category': 'fitness',
    'difficulty': HabitDifficulty.hard,
    'biorhythmType': 'physical',
    'biorhythmPhase': 'peak',
    'microHabits': BiorhythmMicroHabitsTranslations.physicalPeakMicroHabits(languageCode), // ✅ TRANSLATED
    'successIndicators': BiorhythmMicroHabitsTranslations.physicalPeakSuccessIndicators(languageCode), // ✅ TRANSLATED
    'motivationalMessage': _getPhysicalPeakMessage(zodiacSign, languageCode), // ✅ ADD LANGUAGE PARAM
    'scienceBacked': true,
    'scienceExplanation': BiorhythmTranslations.physicalCycleScience(languageCode), // ✅ USE EXISTING TRANSLATION
  };
}
```

**German Result:**
```dart
// microHabits will now include:
{
  'habit': 'Stellen Sie einen persönlichen Rekord auf (Gewicht, Distanz oder Zeit)',
  'when': 'Heute, während Ihre körperliche Energie am höchsten ist',
  'why': '75% der olympischen Rekorde wurden während der körperlichen Spitzenphase gebrochen',
  'difficulty': 'hard',
}
```

---

### STEP 3: Refactor All Other Goals (SAME PATTERN)

Apply the same pattern to:

#### Physical Critical Goal (Lines 121-163)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.physicalCriticalMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.physicalCriticalSuccessIndicators(languageCode),
'scienceExplanation': BiorhythmTranslations.physicalCycleScience(languageCode),
```

#### Physical Recovery Goal (Lines 165-206)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.physicalRecoveryMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.physicalRecoverySuccessIndicators(languageCode),
```

#### Emotional Peak Goal (Lines 212-273)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.emotionalPeakMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.emotionalPeakSuccessIndicators(languageCode),
'scienceExplanation': BiorhythmTranslations.emotionalCycleScience(languageCode),
```

#### Emotional Critical Goal (Lines 275-317)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.emotionalCriticalMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.emotionalCriticalSuccessIndicators(languageCode),
```

#### Intellectual Peak Goal (Lines 323-384)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.intellectualPeakMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.intellectualPeakSuccessIndicators(languageCode),
'scienceExplanation': BiorhythmTranslations.intellectualCycleScience(languageCode),
```

#### Intellectual Critical Goal (Lines 386-427)
```dart
'microHabits': BiorhythmMicroHabitsTranslations.intellectualCriticalMicroHabits(languageCode),
'successIndicators': BiorhythmMicroHabitsTranslations.intellectualCriticalSuccessIndicators(languageCode),
```

---

### STEP 4: Update Zodiac Message Methods to Accept languageCode

**Before:**
```dart
static String _getPhysicalPeakMessage(String zodiacSign) {
  final messages = <String, String>{
    'aries': 'Your Mars + physical peak = unstoppable force today!',
    // ...
  };
  return messages[zodiacSign.toLowerCase()] ??
      'Your physical energy is at its peak. Use it wisely!';
}
```

**After:**
```dart
static String _getPhysicalPeakMessage(String zodiacSign, String languageCode) {
  final messages = <String, Map<String, String>>{
    'aries': {
      'en': 'Your Mars + physical peak = unstoppable force today!',
      'es': 'Tu Marte + pico físico = fuerza imparable hoy!',
      'pt': 'Seu Marte + pico físico = força imparável hoje!',
      'fr': 'Votre Mars + pic physique = force irrésistible aujourd\'hui!',
      'de': 'Dein Mars + körperlicher Höhepunkt = unaufhaltsame Kraft heute!',
      'it': 'Il tuo Marte + picco fisico = forza irresistibile oggi!',
    },
    'taurus': {
      'en': 'Your Earth energy + physical peak = grounded power.',
      'es': 'Tu energía Tierra + pico físico = poder fundamentado.',
      'pt': 'Sua energia Terra + pico físico = poder fundamentado.',
      'fr': 'Votre énergie Terre + pic physique = pouvoir enraciné.',
      'de': 'Deine Erdenergie + körperlicher Höhepunkt = grundierte Kraft.',
      'it': 'La tua energia Terra + picco fisico = potere radicato.',
    },
    'gemini': {
      'en': 'Your adaptability + physical peak = master any movement.',
      'es': 'Tu adaptabilidad + pico físico = domina cualquier movimiento.',
      'pt': 'Sua adaptabilidade + pico físico = domine qualquer movimento.',
      'fr': 'Votre adaptabilité + pic physique = maîtrise tout mouvement.',
      'de': 'Deine Anpassungsfähigkeit + körperlicher Höhepunkt = beherrsche jede Bewegung.',
      'it': 'La tua adattabilità + picco fisico = domina qualsiasi movimento.',
    },
    'cancer': {
      'en': 'Your Moon + physical peak = body wisdom at its highest.',
      'es': 'Tu Luna + pico físico = sabiduría corporal en su apogeo.',
      'pt': 'Sua Lua + pico físico = sabedoria corporal em seu auge.',
      'fr': 'Votre Lune + pic physique = sagesse corporelle à son apogée.',
      'de': 'Dein Mond + körperlicher Höhepunkt = körperliche Weisheit auf dem Höchsten.',
      'it': 'La tua Luna + picco fisico = saggezza corporale al suo apice.',
    },
    'leo': {
      'en': 'Your Sun + physical peak = radiate strength today.',
      'es': 'Tu Sol + pico físico = irradia fuerza hoy.',
      'pt': 'Seu Sol + pico físico = irradie força hoje.',
      'fr': 'Votre Soleil + pic physique = rayonnez la force aujourd\'hui.',
      'de': 'Deine Sonne + körperlicher Höhepunkt = strahle Kraft heute aus.',
      'it': 'Il tuo Sole + picco fisico = irradia forza oggi.',
    },
    'virgo': {
      'en': 'Your precision + physical peak = perfect form.',
      'es': 'Tu precisión + pico físico = forma perfecta.',
      'pt': 'Sua precisão + pico físico = forma perfeita.',
      'fr': 'Votre précision + pic physique = forme parfaite.',
      'de': 'Deine Präzision + körperlicher Höhepunkt = perfekte Form.',
      'it': 'La tua precisione + picco fisico = forma perfetta.',
    },
    'libra': {
      'en': 'Your Venus + physical peak = graceful power.',
      'es': 'Tu Venus + pico físico = poder elegante.',
      'pt': 'Sua Vênus + pico físico = poder gracioso.',
      'fr': 'Votre Vénus + pic physique = pouvoir gracieux.',
      'de': 'Deine Venus + körperlicher Höhepunkt = anmutige Kraft.',
      'it': 'La tua Venere + picco fisico = potere elegante.',
    },
    'scorpio': {
      'en': 'Your Pluto + physical peak = transformative strength.',
      'es': 'Tu Plutón + pico físico = fuerza transformadora.',
      'pt': 'Seu Plutão + pico físico = força transformadora.',
      'fr': 'Votre Pluton + pic physique = force transformatrice.',
      'de': 'Dein Pluto + körperlicher Höhepunkt = transformative Kraft.',
      'it': 'Il tuo Plutone + picco fisico = forza trasformativa.',
    },
    'sagittarius': {
      'en': 'Your Jupiter + physical peak = adventure awaits.',
      'es': 'Tu Júpiter + pico físico = la aventura te espera.',
      'pt': 'Seu Júpiter + pico físico = a aventura o aguarda.',
      'fr': 'Votre Jupiter + pic physique = l\'aventure vous attend.',
      'de': 'Dein Jupiter + körperlicher Höhepunkt = Abenteuer wartet.',
      'it': 'Il tuo Giove + picco fisico = l\'avventura ti aspetta.',
    },
    'capricorn': {
      'en': 'Your Saturn + physical peak = disciplined excellence.',
      'es': 'Tu Saturno + pico físico = excelencia disciplinada.',
      'pt': 'Seu Saturno + pico físico = excelência disciplinada.',
      'fr': 'Votre Saturne + pic physique = excellence disciplinée.',
      'de': 'Dein Saturn + körperlicher Höhepunkt = disziplinierte Exzellenz.',
      'it': 'Il tuo Saturno + picco fisico = eccellenza disciplinata.',
    },
    'aquarius': {
      'en': 'Your Uranus + physical peak = innovative movement.',
      'es': 'Tu Urano + pico físico = movimiento innovador.',
      'pt': 'Seu Urano + pico físico = movimento inovador.',
      'fr': 'Votre Uranus + pic physique = mouvement innovant.',
      'de': 'Dein Uranus + körperlicher Höhepunkt = innovative Bewegung.',
      'it': 'Il tuo Urano + picco fisico = movimento innovativo.',
    },
    'pisces': {
      'en': 'Your Neptune + physical peak = fluid strength.',
      'es': 'Tu Neptuno + pico físico = fuerza fluida.',
      'pt': 'Seu Netuno + pico físico = força fluida.',
      'fr': 'Votre Neptune + pic physique = force fluide.',
      'de': 'Dein Neptun + körperlicher Höhepunkt = fließende Kraft.',
      'it': 'Il tuo Nettuno + picco fisico = forza fluida.',
    },
  };

  final zodiacMessages = messages[zodiacSign.toLowerCase()];
  if (zodiacMessages == null) {
    return languageCode == 'de'
        ? 'Deine körperliche Energie ist auf ihrem Höhepunkt. Nutze sie weise!'
        : 'Your physical energy is at its peak. Use it wisely!';
  }

  return zodiacMessages[languageCode] ?? zodiacMessages['en']!;
}
```

---

### STEP 5: Complete Emotional Peak Messages

**Complete German translations:**
```dart
static String _getEmotionalPeakMessage(String zodiacSign, String languageCode) {
  final messages = <String, Map<String, String>>{
    'aries': {
      'en': 'Your passion + emotional peak = pure creative fire.',
      'es': 'Tu pasión + pico emocional = fuego creativo puro.',
      'pt': 'Sua paixão + pico emocional = fogo criativo puro.',
      'fr': 'Votre passion + pic émotionnel = feu créatif pur.',
      'de': 'Deine Leidenschaft + emotionaler Höhepunkt = reines kreatives Feuer.',
      'it': 'La tua passione + picco emozionale = fuoco creativo puro.',
    },
    'taurus': {
      'en': 'Your sensuality + emotional peak = artistic beauty.',
      'es': 'Tu sensualidad + pico emocional = belleza artística.',
      'pt': 'Sua sensualidade + pico emocional = beleza artística.',
      'fr': 'Votre sensualité + pic émotionnel = beauté artistique.',
      'de': 'Deine Sinnlichkeit + emotionaler Höhepunkt = künstlerische Schönheit.',
      'it': 'La tua sensualità + picco emozionale = bellezza artistica.',
    },
    'gemini': {
      'en': 'Your communication + emotional peak = powerful words.',
      'es': 'Tu comunicación + pico emocional = palabras poderosas.',
      'pt': 'Sua comunicação + pico emocional = palavras poderosas.',
      'fr': 'Votre communication + pic émotionnel = paroles puissantes.',
      'de': 'Deine Kommunikation + emotionaler Höhepunkt = mächtige Worte.',
      'it': 'La tua comunicazione + picco emozionale = parole potenti.',
    },
    'cancer': {
      'en': 'Your Moon + emotional peak = supreme emotional intelligence.',
      'es': 'Tu Luna + pico emocional = inteligencia emocional suprema.',
      'pt': 'Sua Lua + pico emocional = inteligência emocional suprema.',
      'fr': 'Votre Lune + pic émotionnel = intelligence émotionnelle suprême.',
      'de': 'Dein Mond + emotionaler Höhepunkt = höchste emotionale Intelligenz.',
      'it': 'La tua Luna + picco emozionale = intelligenza emotiva suprema.',
    },
    'leo': {
      'en': 'Your heart + emotional peak = radiant self-expression.',
      'es': 'Tu corazón + pico emocional = autoexpresión radiante.',
      'pt': 'Seu coração + pico emocional = auto-expressão radiante.',
      'fr': 'Votre cœur + pic émotionnel = auto-expression rayonnante.',
      'de': 'Dein Herz + emotionaler Höhepunkt = strahlender Selbstausdruck.',
      'it': 'Il tuo cuore + picco emozionale = auto-espressione radiante.',
    },
    'virgo': {
      'en': 'Your sensitivity + emotional peak = healing presence.',
      'es': 'Tu sensibilidad + pico emocional = presencia sanadora.',
      'pt': 'Sua sensibilidade + pico emocional = presença curadora.',
      'fr': 'Votre sensibilité + pic émotionnel = présence guérissante.',
      'de': 'Deine Sensibilität + emotionaler Höhepunkt = heilende Präsenz.',
      'it': 'La tua sensibilità + picco emozionale = presenza guaritrice.',
    },
    'libra': {
      'en': 'Your Venus + emotional peak = harmony and beauty.',
      'es': 'Tu Venus + pico emocional = armonía y belleza.',
      'pt': 'Sua Vênus + pico emocional = harmonia e beleza.',
      'fr': 'Votre Vénus + pic émotionnel = harmonie et beauté.',
      'de': 'Deine Venus + emotionaler Höhepunkt = Harmonie und Schönheit.',
      'it': 'La tua Venere + picco emozionale = armonia e bellezza.',
    },
    'scorpio': {
      'en': 'Your depth + emotional peak = transformative insights.',
      'es': 'Tu profundidad + pico emocional = insights transformadores.',
      'pt': 'Sua profundidade + pico emocional = insights transformadores.',
      'fr': 'Votre profondeur + pic émotionnel = perspectives transformatrices.',
      'de': 'Deine Tiefe + emotionaler Höhepunkt = transformative Einsichten.',
      'it': 'La tua profondità + picco emozionale = intuizioni trasformative.',
    },
    'sagittarius': {
      'en': 'Your optimism + emotional peak = contagious joy.',
      'es': 'Tu optimismo + pico emocional = alegría contagiosa.',
      'pt': 'Seu otimismo + pico emocional = alegria contagiosa.',
      'fr': 'Votre optimisme + pic émotionnel = joie contagieuse.',
      'de': 'Dein Optimismus + emotionaler Höhepunkt = ansteckende Freude.',
      'it': 'Il tuo ottimismo + picco emozionale = gioia contagiosa.',
    },
    'capricorn': {
      'en': 'Your wisdom + emotional peak = emotional mastery.',
      'es': 'Tu sabiduría + pico emocional = maestría emocional.',
      'pt': 'Sua sabedoria + pico emocional = maestria emocional.',
      'fr': 'Votre sagesse + pic émotionnel = maîtrise émotionnelle.',
      'de': 'Deine Weisheit + emotionaler Höhepunkt = emotionale Meisterschaft.',
      'it': 'La tua saggezza + picco emozionale = padronanza emotiva.',
    },
    'aquarius': {
      'en': 'Your vision + emotional peak = humanitarian creativity.',
      'es': 'Tu visión + pico emocional = creatividad humanitaria.',
      'pt': 'Sua visão + pico emocional = criatividade humanitária.',
      'fr': 'Votre vision + pic émotionnel = créativité humanitaire.',
      'de': 'Deine Vision + emotionaler Höhepunkt = humanitäre Kreativität.',
      'it': 'La tua visione + picco emozionale = creatività umanitaria.',
    },
    'pisces': {
      'en': 'Your empathy + emotional peak = artistic transcendence.',
      'es': 'Tu empatía + pico emocional = trascendencia artística.',
      'pt': 'Sua empatia + pico emocional = transcendência artística.',
      'fr': 'Votre empathie + pic émotionnel = transcendance artistique.',
      'de': 'Dein Mitgefühl + emotionaler Höhepunkt = künstlerische Transzendenz.',
      'it': 'La tua empatia + picco emozionale = trascendenza artistica.',
    },
  };

  final zodiacMessages = messages[zodiacSign.toLowerCase()];
  if (zodiacMessages == null) {
    return languageCode == 'de'
        ? 'Deine emotionale Energie ist auf ihrem Höhepunkt. Erschaffe etwas Schönes!'
        : 'Your emotional energy is at its peak. Create something beautiful!';
  }

  return zodiacMessages[languageCode] ?? zodiacMessages['en']!;
}
```

---

### STEP 6: Complete Intellectual Peak Messages

```dart
static String _getIntellectualPeakMessage(String zodiacSign, String languageCode) {
  final messages = <String, Map<String, String>>{
    'aries': {
      'en': 'Your initiative + intellectual peak = breakthrough ideas.',
      'es': 'Tu iniciativa + pico intelectual = ideas revolucionarias.',
      'pt': 'Sua iniciativa + pico intelectual = ideias inovadoras.',
      'fr': 'Votre initiative + pic intellectuel = idées révolutionnaires.',
      'de': 'Deine Initiative + intellektueller Höhepunkt = bahnbrechende Ideen.',
      'it': 'La tua iniziativa + picco intellettuale = idee rivoluzionarie.',
    },
    'taurus': {
      'en': 'Your practicality + intellectual peak = brilliant solutions.',
      'es': 'Tu practicidad + pico intelectual = soluciones brillantes.',
      'pt': 'Sua praticidade + pico intelectual = soluções brilhantes.',
      'fr': 'Votre pragmatisme + pic intellectuel = solutions brillantes.',
      'de': 'Deine Praktikalität + intellektueller Höhepunkt = brillante Lösungen.',
      'it': 'La tua praticità + picco intellettuale = soluzioni brillanti.',
    },
    'gemini': {
      'en': 'Your Mercury + intellectual peak = genius-level thinking.',
      'es': 'Tu Mercurio + pico intelectual = pensamiento a nivel de genio.',
      'pt': 'Seu Mercúrio + pico intelectual = pensamento de nível gênio.',
      'fr': 'Votre Mercure + pic intellectuel = pensée au niveau du génie.',
      'de': 'Dein Merkur + intellektueller Höhepunkt = Denken auf Genie-Niveau.',
      'it': 'Il tuo Mercurio + picco intellettuale = pensiero a livello di genio.',
    },
    'cancer': {
      'en': 'Your intuition + intellectual peak = emotional intelligence.',
      'es': 'Tu intuición + pico intelectual = inteligencia emocional.',
      'pt': 'Sua intuição + pico intelectual = inteligência emocional.',
      'fr': 'Votre intuition + pic intellectuel = intelligence émotionnelle.',
      'de': 'Deine Intuition + intellektueller Höhepunkt = emotionale Intelligenz.',
      'it': 'La tua intuizione + picco intellettuale = intelligenza emotiva.',
    },
    'leo': {
      'en': 'Your vision + intellectual peak = strategic brilliance.',
      'es': 'Tu visión + pico intelectual = brillantez estratégica.',
      'pt': 'Sua visão + pico intelectual = brilho estratégico.',
      'fr': 'Votre vision + pic intellectuel = brillance stratégique.',
      'de': 'Deine Vision + intellektueller Höhepunkt = strategische Brillanz.',
      'it': 'La tua visione + picco intellettuale = brillanza strategica.',
    },
    'virgo': {
      'en': 'Your Mercury + intellectual peak = analytical perfection.',
      'es': 'Tu Mercurio + pico intelectual = perfección analítica.',
      'pt': 'Seu Mercúrio + pico intelectual = perfeição analítica.',
      'fr': 'Votre Mercure + pic intellectuel = perfection analytique.',
      'de': 'Dein Merkur + intellektueller Höhepunkt = analytische Perfektion.',
      'it': 'Il tuo Mercurio + picco intellettuale = perfezione analitica.',
    },
    'libra': {
      'en': 'Your balance + intellectual peak = fair judgment.',
      'es': 'Tu balance + pico intelectual = juicio justo.',
      'pt': 'Seu equilíbrio + pico intelectual = julgamento justo.',
      'fr': 'Votre équilibre + pic intellectuel = jugement équitable.',
      'de': 'Dein Gleichgewicht + intellektueller Höhepunkt = gerechte Urteilskraft.',
      'it': 'Il tuo equilibrio + picco intellettuale = giudizio equo.',
    },
    'scorpio': {
      'en': 'Your research skills + intellectual peak = deep insights.',
      'es': 'Tus habilidades de investigación + pico intelectual = insights profundos.',
      'pt': 'Suas habilidades de pesquisa + pico intelectual = insights profundos.',
      'fr': 'Vos compétences en recherche + pic intellectuel = perspectives profondes.',
      'de': 'Deine Forschungsfähigkeiten + intellektueller Höhepunkt = tiefe Einsichten.',
      'it': 'Le tue abilità di ricerca + picco intellettuale = intuizioni profonde.',
    },
    'sagittarius': {
      'en': 'Your philosophy + intellectual peak = wisdom.',
      'es': 'Tu filosofía + pico intelectual = sabiduría.',
      'pt': 'Sua filosofia + pico intelectual = sabedoria.',
      'fr': 'Votre philosophie + pic intellectuel = sagesse.',
      'de': 'Deine Philosophie + intellektueller Höhepunkt = Weisheit.',
      'it': 'La tua filosofia + picco intellettuale = saggezza.',
    },
    'capricorn': {
      'en': 'Your strategy + intellectual peak = masterful planning.',
      'es': 'Tu estrategia + pico intelectual = planificación magistral.',
      'pt': 'Sua estratégia + pico intelectual = planejamento magistral.',
      'fr': 'Votre stratégie + pic intellectuel = planification magistrale.',
      'de': 'Deine Strategie + intellektueller Höhepunkt = meisterhaftes Planen.',
      'it': 'La tua strategia + picco intellettuale = pianificazione magistrale.',
    },
    'aquarius': {
      'en': 'Your innovation + intellectual peak = revolutionary ideas.',
      'es': 'Tu innovación + pico intelectual = ideas revolucionarias.',
      'pt': 'Sua inovação + pico intelectual = ideias revolucionárias.',
      'fr': 'Votre innovation + pic intellectuel = idées révolutionnaires.',
      'de': 'Deine Innovation + intellektueller Höhepunkt = revolutionäre Ideen.',
      'it': 'La tua innovazione + picco intellettuale = idee rivoluzionarie.',
    },
    'pisces': {
      'en': 'Your imagination + intellectual peak = creative genius.',
      'es': 'Tu imaginación + pico intelectual = genio creativo.',
      'pt': 'Sua imaginação + pico intelectual = gênio criativo.',
      'fr': 'Votre imagination + pic intellectuel = génie créatif.',
      'de': 'Deine Vorstellungskraft + intellektueller Höhepunkt = kreatives Genie.',
      'it': 'La tua immaginazione + picco intellettuale = genio creativo.',
    },
  };

  final zodiacMessages = messages[zodiacSign.toLowerCase()];
  if (zodiacMessages == null) {
    return languageCode == 'de'
        ? 'Deine intellektuelle Energie ist auf ihrem Höhepunkt. Denk groß!'
        : 'Your intellectual energy is at its peak. Think big!';
  }

  return zodiacMessages[languageCode] ?? zodiacMessages['en']!;
}
```

---

### STEP 7: Update Message Method Calls

**Before:**
```dart
'motivationalMessage': _getPhysicalPeakMessage(zodiacSign),
```

**After:**
```dart
'motivationalMessage': _getPhysicalPeakMessage(zodiacSign, languageCode),
```

Do this for all three message methods:
- `_getPhysicalPeakMessage(zodiacSign, languageCode)`
- `_getEmotionalPeakMessage(zodiacSign, languageCode)`
- `_getIntellectualPeakMessage(zodiacSign, languageCode)`

---

### STEP 8: Fix Other Motivational Messages (4 more strings)

**Lines 161, 204, 315, 425:**

```dart
// Line 161 - Physical Critical Goal
'motivationalMessage': languageCode == 'de'
    ? 'Deine $zodiacSign-Weisheit weiß: Ruhetage sind auch Trainingstage. Ehre deinen körperlichen Rhythmus.'
    : 'Your $zodiacSign wisdom knows: rest days are training days too. Honor your body\'s cycles.',

// Line 204 - Physical Recovery Goal
'motivationalMessage': languageCode == 'de'
    ? 'Dein $zodiacSign weiß: Wachstum passiert während der Erholung, nicht während des Handelns.'
    : 'Your $zodiacSign knows: growth happens during recovery, not during action.',

// Line 315 - Emotional Critical Goal
'motivationalMessage': languageCode == 'de'
    ? 'Deine $zodiacSign-Sensibilität ist ein Geschenk. Ehre deinen emotionalen Rhythmus.'
    : 'Your $zodiacSign sensitivity is a gift. Honor your emotional rhythms.',

// Line 425 - Intellectual Critical Goal
'motivationalMessage': languageCode == 'de'
    ? 'Dein $zodiacSign weiß: Nicht jeder Tag ist für Genie. Manche Tage sind zum Auftauchen.'
    : 'Your $zodiacSign knows: not every day is for genius. Some days are for showing up.',
```

---

### STEP 9: Update enhanced_coach_adapter.dart (Optional - UI Enhancement)

**Location:** Lines 143-203

Current code only handles Spanish and English. Add German support:

```dart
String _buildSuggestedByText(Map<String, dynamic> goalMap, String languageCode) {
  // Check if it's a biorhythm goal
  if (goalMap.containsKey('biorhythmType')) {
    final type = goalMap['biorhythmType'] as String;
    final phase = goalMap['biorhythmPhase'] as String;

    switch (languageCode) {
      case 'es':
        return 'Basado en tu ciclo $type ($phase)';
      case 'pt':
        return 'Baseado no seu ciclo $type ($phase)';
      case 'fr':
        return 'Basé sur votre cycle $type ($phase)';
      case 'de':
        return 'Basierend auf Ihrem $type-Zyklus ($phase)';  // ✅ ADD THIS
      case 'it':
        return 'Basato sul tuo ciclo $type ($phase)';
      default:
        return 'Based on your $type cycle ($phase)';
    }
  }

  // ... rest of method
}
```

**Also update writeSectionHeader calls:**

```dart
// Old:
writeSectionHeader('⚙️', 'Acciones recomendadas', 'Recommended actions');

// New (need to modify method signature first):
String _getLabel(String esText, String deText, String enText) {
  switch (languageCode) {
    case 'es': return esText;
    case 'de': return deText;
    default: return enText;
  }
}

// Then:
writeSectionHeader('⚙️', _getLabel('Acciones recomendadas', 'Empfohlene Maßnahmen', 'Recommended actions'));
writeSectionHeader('✅', _getLabel('Cómo medir el progreso', 'Fortschritt messen', 'How to measure progress'));
writeSectionHeader('🔬', _getLabel('Respaldo científico', 'Wissenschaftliche Erkenntnis', 'Science-backed insight'));
```

**And the When/Why labels:**

```dart
final whenLabel = languageCode == 'es' ? 'Cuándo'
    : languageCode == 'de' ? 'Wann'
    : languageCode == 'fr' ? 'Quand'
    : languageCode == 'pt' ? 'Quando'
    : languageCode == 'it' ? 'Quando'
    : 'When';

final whyLabel = languageCode == 'es' ? 'Por qué'
    : languageCode == 'de' ? 'Warum'
    : languageCode == 'fr' ? 'Pourquoi'
    : languageCode == 'pt' ? 'Por que'
    : languageCode == 'it' ? 'Perché'
    : 'Why';
```

---

## VERIFICATION CHECKLIST

After implementation, verify:

- [ ] German text appears when `languageCode = 'de'`
- [ ] All physical peak micro-habits translated
- [ ] All physical critical micro-habits translated
- [ ] All physical recovery micro-habits translated
- [ ] All emotional peak micro-habits translated
- [ ] All emotional critical micro-habits translated
- [ ] All intellectual peak micro-habits translated
- [ ] All intellectual critical micro-habits translated
- [ ] All success indicators translated
- [ ] All zodiac messages translated (36 for each of 3 types = 108 total)
- [ ] Science explanations translated
- [ ] UI labels in enhanced_coach_adapter translated
- [ ] No hardcoded English strings remain
- [ ] App builds without errors
- [ ] German localization file exists and is complete

---

## SUMMARY

**Total German Strings Added:** ~150+

**Files Modified:**
1. `biorhythm_goal_generator.dart` - Add import, refactor methods, add language params
2. `enhanced_coach_adapter.dart` - Add German language support (optional)

**Time Estimate:** 2-3 hours

**Difficulty:** Medium (repetitive but straightforward)

---

**Report Complete - Ready for Implementation**
