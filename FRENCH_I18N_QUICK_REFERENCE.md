# French Internationalization - Quick Reference Guide

## New Translation Keys Added (Dec 10, 2025)

### Key: `evaluationIn8KeyCategories`
Use this for: Subtitle describing 8-category evaluation in compatibility analysis

**Usage:**
```dart
Text(AppLocalizations.of(context)!.evaluationIn8KeyCategories)
```

**Translations:**
- 🇬🇧 EN: "Evaluation in 8 key categories"
- 🇪🇸 ES: "Evaluación en 8 categorías clave"
- 🇫🇷 FR: "Évaluation en 8 catégories clés"
- 🇩🇪 DE: "Bewertung in 8 Schlüsselkategorien"
- 🇮🇹 IT: "Valutazione in 8 categorie chiave"
- 🇵🇹 PT: "Avaliação em 8 categorias-chave"

---

### Key: `analyzingUpTo5People`
Use this for: Description of group compatibility feature

**Usage:**
```dart
Text(AppLocalizations.of(context)!.analyzingUpTo5People)
```

**Translations:**
- 🇬🇧 EN: "Analyze up to 5 people simultaneously"
- 🇪🇸 ES: "Analiza hasta 5 personas simultáneamente"
- 🇫🇷 FR: "Analysez jusqu'à 5 personnes simultanément"
- 🇩🇪 DE: "Analysieren Sie bis zu 5 Personen gleichzeitig"
- 🇮🇹 IT: "Analizza fino a 5 persone contemporaneamente"
- 🇵🇹 PT: "Analise até 5 pessoas simultaneamente"

---

## Already Existing Keys (Referenced)

### Key: `elements`
Tab label for elements in compatibility screen
```dart
Text(AppLocalizations.of(context)!.elements)
```

### Key: `multidimensionalAnalysis`
Header for 8D analysis section
```dart
Text(AppLocalizations.of(context)!.multidimensionalAnalysis)
```

---

## How to Add New Translations

### Step 1: Add to English ARB
File: `assets/l10n/app_en.arb`
```json
"yourNewKey": "Your English text",
```

### Step 2: Add to All Other Languages
Repeat for: `app_es.arb`, `app_fr.arb`, `app_de.arb`, `app_it.arb`, `app_pt.arb`

### Step 3: Regenerate
```bash
flutter gen-l10n
```

### Step 4: Use in Code
```dart
Text(AppLocalizations.of(context)!.yourNewKey)
```

---

## Common Mistakes to Avoid

❌ **DON'T:**
```dart
Text('Analyse Multidimensionnelle')  // Hardcoded French
```

✅ **DO:**
```dart
Text(AppLocalizations.of(context)!.multidimensionalAnalysis)
```

❌ **DON'T:**
```dart
// Mixing languages in switch statements outside helper classes
switch (locale) {
  case 'fr': return 'Erreur';
  // ...in regular widget code
}
```

✅ **DO:**
```dart
// Use AppLocalizations in widgets
Text(AppLocalizations.of(context)!.error)

// OR create a dedicated i18n helper class (like premium_error_i18n.dart)
```

---

## When to Use Helper Classes vs ARB Files

### Use ARB Files (Preferred):
- ✅ UI text that appears in widgets
- ✅ User-facing messages
- ✅ Navigation labels
- ✅ Button text
- ✅ Error messages shown in UI

### Use Helper Classes (Special Cases):
- ✅ Complex conditional translations
- ✅ Error messages that need context-free access
- ✅ Dynamic template generation
- ✅ Service-level translations without BuildContext

**Example Helper Class:**
```dart
class MyI18nHelper {
  String getError(String locale) {
    switch (locale) {
      case 'es': return 'Error';
      case 'fr': return 'Erreur';
      // ...
    }
  }
}
```

---

## Translation Verification Checklist

Before committing translations:

- [ ] Added key to `app_en.arb`
- [ ] Added key to `app_es.arb`
- [ ] Added key to `app_fr.arb`
- [ ] Added key to `app_de.arb`
- [ ] Added key to `app_it.arb`
- [ ] Added key to `app_pt.arb`
- [ ] Ran `flutter gen-l10n`
- [ ] Tested in all 6 languages
- [ ] No hardcoded strings remain
- [ ] Flutter analyze passes

---

## Search Commands

### Find hardcoded French:
```bash
grep -r "Analyse\|Compatibilité\|Éléments" lib/ \
  --exclude-dir=l10n \
  --include="*.dart" \
  | grep -v "translations" \
  | grep -v "i18n"
```

### Find missing translations:
```bash
python3 assets/l10n/comparar_idiomas.py
```

---

## Resources

- **ARB Files Location:** `assets/l10n/`
- **Generated Files:** `lib/l10n/`
- **I18n Config:** `l10n.yaml`
- **Helper Classes:** `lib/features/premium/helpers/`, `lib/utils/`

---

**Last Updated:** December 10, 2025
**Status:** ✅ All hardcoded French texts fixed
