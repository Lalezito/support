# Translation Key Template

Use this template every time you add a new translation key to the Zodiac App.

---

## Template Usage

1. Copy the relevant template below
2. Fill in all placeholders `{...}`
3. Add to all 6 language files (EN, ES, DE, FR, IT, PT)
4. Test in UI before committing

---

## ARB File Template

### Basic Translation Key

```json
{
  "{keyNameInCamelCase}": "{English translation}",
  "@{keyNameInCamelCase}": {
    "description": "{Purpose and context - where this appears in the app}",
    "context": "{Additional context for translators}",
    "screen": "{Screen name where this is used}"
  }
}
```

**Example**:
```json
{
  "premiumUpgradeButton": "Upgrade to Premium",
  "@premiumUpgradeButton": {
    "description": "Call-to-action button to upgrade to premium subscription",
    "context": "Displayed in settings, horoscope screen, and compatibility screen",
    "screen": "PremiumScreen, SettingsScreen, HoroscopeScreen"
  }
}
```

---

### Parameterized Translation Key

```json
{
  "{keyNameInCamelCase}": "{Text with {placeholder} parameter}",
  "@{keyNameInCamelCase}": {
    "description": "{Purpose and context}",
    "placeholders": {
      "{parameterName}": {
        "type": "{String|int|double|DateTime}",
        "example": "{Example value}",
        "description": "{What this parameter represents}"
      }
    }
  }
}
```

**Example**:
```json
{
  "compatibilityScoreDisplay": "{sign1} and {sign2}: {score}% compatible",
  "@compatibilityScoreDisplay": {
    "description": "Displays compatibility score between two zodiac signs",
    "placeholders": {
      "sign1": {
        "type": "String",
        "example": "Aries",
        "description": "First zodiac sign name"
      },
      "sign2": {
        "type": "String",
        "example": "Taurus",
        "description": "Second zodiac sign name"
      },
      "score": {
        "type": "int",
        "example": "85",
        "description": "Compatibility percentage (0-100)"
      }
    }
  }
}
```

---

### Plural Translation Key

```json
{
  "{keyNameInCamelCase}": "{count, plural, =0{no items} =1{one item} other{{count} items}}",
  "@{keyNameInCamelCase}": {
    "description": "{Purpose and context}",
    "placeholders": {
      "count": {
        "type": "int",
        "format": "compact",
        "example": "42"
      }
    }
  }
}
```

**Example**:
```json
{
  "predictionCount": "{count, plural, =0{No predictions} =1{1 prediction} other{{count} predictions}}",
  "@predictionCount": {
    "description": "Displays the number of active predictions",
    "placeholders": {
      "count": {
        "type": "int",
        "format": "compact",
        "example": "5"
      }
    }
  }
}
```

---

## Dart Code Template

### Simple Getter

```dart
/// {Brief description of what this translation is for}
///
/// Used in: {ScreenName}, {OtherScreenName}
///
/// Example: "{Example text}"
String get {keyName} => '{English translation}';
```

**Example**:
```dart
/// Title for the premium upgrade modal
///
/// Used in: PremiumScreen, SettingsScreen, HoroscopeScreen
///
/// Example: "Unlock Premium Power"
String get premiumUpgradeTitle => 'Unlock Premium Power';
```

---

### Parameterized Method

```dart
/// {Brief description}
///
/// Parameters:
/// - [{paramName}]: {Description of parameter}
/// - [{paramName2}]: {Description of parameter 2}
///
/// Used in: {ScreenName}
///
/// Example: "{Example with sample values}"
String {methodName}({paramType} {paramName}, {paramType2} {paramName2}) {
  return '{Translation with $paramName and $paramName2}';
}
```

**Example**:
```dart
/// Displays compatibility score between two zodiac signs
///
/// Parameters:
/// - [score]: Compatibility percentage (0-100)
/// - [sign1]: First zodiac sign name
/// - [sign2]: Second zodiac sign name
///
/// Used in: CompatibilityScreen, CompatibilityCard
///
/// Example: "Aries and Taurus: 85% compatible"
String compatibilityScoreDisplay(int score, String sign1, String sign2) {
  return '$sign1 and $sign2: $score% compatible';
}
```

---

## Multi-Language Template

Use this when adding a new key to all 6 languages at once:

### English (EN)
```json
"{keyName}": "{English translation}"
```

### Spanish (ES)
```json
"{keyName}": "{Traducción en español}"
```

### German (DE)
```json
"{keyName}": "{Deutsche Übersetzung}"
```

### French (FR)
```json
"{keyName}": "{Traduction française}"
```

### Italian (IT)
```json
"{keyName}": "{Traduzione italiana}"
```

### Portuguese (PT)
```json
"{keyName}": "{Tradução em português}"
```

---

## Complete Example: Adding a New Feature

**Scenario**: Adding "Daily Affirmation" feature

### Step 1: Define Keys

```
dailyAffirmationTitle
dailyAffirmationDescription
dailyAffirmationButton
dailyAffirmationEmpty
dailyAffirmationLoading
dailyAffirmationError
```

### Step 2: Add to app_en.arb

```json
{
  "dailyAffirmationTitle": "Daily Cosmic Affirmation",
  "@dailyAffirmationTitle": {
    "description": "Title for the daily affirmation feature",
    "screen": "DailyAffirmationScreen"
  },

  "dailyAffirmationDescription": "Receive personalized affirmations based on your zodiac sign and current planetary positions",
  "@dailyAffirmationDescription": {
    "description": "Subtitle explaining the daily affirmation feature",
    "screen": "DailyAffirmationScreen"
  },

  "dailyAffirmationButton": "Get Today's Affirmation",
  "@dailyAffirmationButton": {
    "description": "Call-to-action button to generate daily affirmation",
    "screen": "DailyAffirmationScreen"
  },

  "dailyAffirmationEmpty": "Your cosmic affirmation will appear here. Tap the button to receive today's message.",
  "@dailyAffirmationEmpty": {
    "description": "Empty state message when no affirmation is loaded",
    "screen": "DailyAffirmationScreen"
  },

  "dailyAffirmationLoading": "Channeling cosmic wisdom...",
  "@dailyAffirmationLoading": {
    "description": "Loading message while generating affirmation",
    "screen": "DailyAffirmationScreen"
  },

  "dailyAffirmationError": "Unable to load today's affirmation. Please try again.",
  "@dailyAffirmationError": {
    "description": "Error message when affirmation fails to load",
    "screen": "DailyAffirmationScreen"
  }
}
```

### Step 3: Add to app_es.arb

```json
{
  "dailyAffirmationTitle": "Afirmación Cósmica Diaria",
  "dailyAffirmationDescription": "Recibe afirmaciones personalizadas basadas en tu signo zodiacal y las posiciones planetarias actuales",
  "dailyAffirmationButton": "Obtener Afirmación de Hoy",
  "dailyAffirmationEmpty": "Tu afirmación cósmica aparecerá aquí. Toca el botón para recibir el mensaje de hoy.",
  "dailyAffirmationLoading": "Canalizando sabiduría cósmica...",
  "dailyAffirmationError": "No se pudo cargar la afirmación de hoy. Por favor, inténtalo de nuevo."
}
```

### Step 4: Add to app_de.arb

```json
{
  "dailyAffirmationTitle": "Tägliche Kosmische Affirmation",
  "dailyAffirmationDescription": "Erhalte personalisierte Affirmationen basierend auf deinem Sternzeichen und den aktuellen Planetenständen",
  "dailyAffirmationButton": "Heutige Affirmation erhalten",
  "dailyAffirmationEmpty": "Deine kosmische Affirmation erscheint hier. Tippe auf den Button, um die heutige Nachricht zu erhalten.",
  "dailyAffirmationLoading": "Kosmische Weisheit wird kanalisiert...",
  "dailyAffirmationError": "Die heutige Affirmation konnte nicht geladen werden. Bitte versuche es erneut."
}
```

### Step 5: Add to app_fr.arb

```json
{
  "dailyAffirmationTitle": "Affirmation Cosmique Quotidienne",
  "dailyAffirmationDescription": "Recevez des affirmations personnalisées basées sur votre signe du zodiaque et les positions planétaires actuelles",
  "dailyAffirmationButton": "Obtenir l'Affirmation d'Aujourd'hui",
  "dailyAffirmationEmpty": "Votre affirmation cosmique apparaîtra ici. Appuyez sur le bouton pour recevoir le message d'aujourd'hui.",
  "dailyAffirmationLoading": "Canalisation de la sagesse cosmique...",
  "dailyAffirmationError": "Impossible de charger l'affirmation d'aujourd'hui. Veuillez réessayer."
}
```

### Step 6: Add to app_it.arb

```json
{
  "dailyAffirmationTitle": "Affermazione Cosmica Giornaliera",
  "dailyAffirmationDescription": "Ricevi affermazioni personalizzate basate sul tuo segno zodiacale e sulle posizioni planetarie attuali",
  "dailyAffirmationButton": "Ottieni l'Affermazione di Oggi",
  "dailyAffirmationEmpty": "La tua affermazione cosmica apparirà qui. Tocca il pulsante per ricevere il messaggio di oggi.",
  "dailyAffirmationLoading": "Incanalando saggezza cosmica...",
  "dailyAffirmationError": "Impossibile caricare l'affermazione di oggi. Per favore, riprova."
}
```

### Step 7: Add to app_pt.arb

```json
{
  "dailyAffirmationTitle": "Afirmação Cósmica Diária",
  "dailyAffirmationDescription": "Receba afirmações personalizadas baseadas no seu signo do zodíaco e nas posições planetárias atuais",
  "dailyAffirmationButton": "Obter Afirmação de Hoje",
  "dailyAffirmationEmpty": "Sua afirmação cósmica aparecerá aqui. Toque no botão para receber a mensagem de hoje.",
  "dailyAffirmationLoading": "Canalizando sabedoria cósmica...",
  "dailyAffirmationError": "Não foi possível carregar a afirmação de hoje. Por favor, tente novamente."
}
```

### Step 8: Test

```bash
# Validate JSON syntax
python3 -m json.tool zodiac_app/assets/l10n/app_en.arb > /dev/null
python3 -m json.tool zodiac_app/assets/l10n/app_es.arb > /dev/null
python3 -m json.tool zodiac_app/assets/l10n/app_de.arb > /dev/null
python3 -m json.tool zodiac_app/assets/l10n/app_fr.arb > /dev/null
python3 -m json.tool zodiac_app/assets/l10n/app_it.arb > /dev/null
python3 -m json.tool zodiac_app/assets/l10n/app_pt.arb > /dev/null

# Generate localization files
flutter gen-l10n

# Run the app and test in all languages
flutter run
```

---

## Naming Checklist

Before finalizing your key name, check:

- [ ] Uses camelCase (not snake_case or kebab-case)
- [ ] Has domain prefix if applicable (premium, error, settings, etc.)
- [ ] Has appropriate suffix (Title, Description, Button, etc.)
- [ ] Under 40 characters (60 max)
- [ ] Self-documenting (readable without context)
- [ ] No duplicate keys
- [ ] Specific enough (not too generic)
- [ ] Consistent with existing keys in same domain

---

## Translation Checklist

For each language translation:

- [ ] **Natural**: Sounds like a native speaker wrote it
- [ ] **Accurate**: Meaning matches English source
- [ ] **Tone**: Matches app's informal/friendly voice
- [ ] **Length**: Fits UI constraints (test on smallest screen)
- [ ] **Grammar**: Correct spelling and grammar
- [ ] **Special Chars**: All accents and special characters included
- [ ] **Gender**: Appropriate gender agreement (ES, DE, FR, IT, PT)
- [ ] **Formality**: Correct pronoun usage (tú/du/vous/tu/você)
- [ ] **Cultural**: Culturally appropriate
- [ ] **Punctuation**: Follows style guide rules

---

## Common Patterns

### Screen Title + Description
```json
"{screenName}Title": "{Title Text}",
"{screenName}Description": "{Description text}"
```

### Action Button
```json
"{action}{Object}Button": "{Action Text}"
// Example: "upgradePremiumButton": "Upgrade to Premium"
```

### Empty State
```json
"{feature}Empty": "{Empty state message}",
"{feature}EmptySubtitle": "{Additional context}"
```

### Loading State
```json
"loading{Feature}": "Loading {feature}..."
// Example: "loadingHoroscope": "Loading your horoscope..."
```

### Error State
```json
"error{Context}{Detail}": "{Error message}"
// Example: "errorNetworkConnection": "Network connection error"
```

### Success State
```json
"success{Action}": "{Success message}"
// Example: "successSaved": "Saved successfully"
```

---

## Version Control

When updating translation keys:

1. **Add new key** with `_v2` suffix if significantly different
2. **Deprecate old key** with comment: `// DEPRECATED: Use {newKey} instead`
3. **Migration timeline**: Allow 2-3 releases before removing
4. **Document in CHANGELOG.md**

**Example**:
```dart
// DEPRECATED: Use premiumUpgradeTitleV2 instead
// Will be removed in version 3.0.0
String get premiumUpgradeTitle => 'Unlock Premium';

/// New version with clearer messaging
String get premiumUpgradeTitleV2 => 'Unlock Your Cosmic Potential';
```

---

## Resources

- **Style Guide**: `/TRANSLATION_STYLE_GUIDE.md`
- **Review Checklist**: `/TRANSLATION_CODE_REVIEW_CHECKLIST.md`
- **Quick Reference**: See style guide Appendix
- **ARB Files**: `/zodiac_app/assets/l10n/`

---

**Template Version**: 1.0
**Last Updated**: October 15, 2025
**Maintained By**: Zodiac App Translation Team
