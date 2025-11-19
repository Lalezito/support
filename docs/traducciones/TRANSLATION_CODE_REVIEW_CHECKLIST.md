# Translation Code Review Checklist

Use this checklist when reviewing Pull Requests that add or modify translations.

---

## Quick Links

- **Style Guide**: `/TRANSLATION_STYLE_GUIDE.md`
- **Key Template**: `/TRANSLATION_KEY_TEMPLATE.md`
- **Quick Reference**: See end of this document

---

## PR Reviewer Checklist

### 1. Naming Conventions ✅

- [ ] **All new keys use camelCase**
  ```
  ✅ dailyHoroscope
  ❌ daily_horoscope
  ```

- [ ] **Keys follow domain prefix pattern**
  ```
  ✅ premiumFeatures, errorNetwork, settingsPrivacy
  ❌ features, network, privacy
  ```

- [ ] **Keys have appropriate suffixes**
  ```
  ✅ premiumUpgradeTitle, premiumUpgradeDescription, premiumUpgradeButton
  ❌ premiumUpgrade1, premiumUpgrade2, premiumUpgrade3
  ```

- [ ] **Keys are specific, not generic**
  ```
  ✅ errorLoadingHoroscope, successPurchaseComplete
  ❌ error, success
  ```

- [ ] **Key length is reasonable (≤60 characters)**
  ```
  ✅ compatibilityAnalysisLoading (26 chars)
  ❌ thisWillPermanentlyDeleteAllYourData... (84 chars)
  ```

---

### 2. Coverage & Completeness ✅

- [ ] **All 6 languages included**
  - [ ] English (EN)
  - [ ] Spanish (ES)
  - [ ] German (DE)
  - [ ] French (FR)
  - [ ] Italian (IT)
  - [ ] Portuguese (PT)

- [ ] **No keys missing in any language**
  ```bash
  # Run this command to check
  ./scripts/check_translation_coverage.sh
  ```

- [ ] **Metadata (@key) annotations present in EN file**
  ```json
  "@premiumUpgradeTitle": {
    "description": "...",
    "screen": "..."
  }
  ```

---

### 3. Translation Quality ✅

#### English (EN)
- [ ] Natural, conversational tone
- [ ] American English spelling
- [ ] Clear and concise
- [ ] No jargon unless necessary

#### Spanish (ES)
- [ ] Uses "tú" (informal), not "usted"
- [ ] Neutral Spanish (not region-specific slang)
- [ ] All accents present (á, é, í, ó, ú, ñ)
- [ ] Gender agreement correct

#### German (DE)
- [ ] Uses "du" (informal), not "Sie"
- [ ] All nouns capitalized
- [ ] Umlauts correct (ä, ö, ü, ß)
- [ ] Compound nouns properly formed

#### French (FR)
- [ ] Uses "vous" (formal)
- [ ] All accents present (é, è, ê, à, ç)
- [ ] Elision applied correctly (l' before vowels)
- [ ] Gender agreement correct

#### Italian (IT)
- [ ] Uses "tu" (informal)
- [ ] All accents present (à, è, é, ì, ò, ù)
- [ ] Gender agreement correct
- [ ] Elision applied correctly

#### Portuguese (PT)
- [ ] Brazilian Portuguese (PT-BR)
- [ ] Uses "você" (informal Brazilian)
- [ ] All special characters present (ã, õ, ç)
- [ ] Not European Portuguese spelling

---

### 4. Code Quality ✅

- [ ] **JSON syntax is valid**
  ```bash
  python3 -m json.tool zodiac_app/assets/l10n/app_en.arb
  ```

- [ ] **No duplicate keys**
  ```bash
  # Check for duplicates
  grep -o '"[^"]*":' app_en.arb | sort | uniq -d
  ```

- [ ] **Keys alphabetically sorted within domain**
  ```json
  // ✅ GOOD
  "premiumActivated": "...",
  "premiumFeatures": "...",
  "premiumUpgrade": "..."

  // ❌ BAD - not sorted
  "premiumFeatures": "...",
  "premiumUpgrade": "...",
  "premiumActivated": "..."
  ```

- [ ] **Parameterized translations properly formatted**
  ```json
  // ✅ GOOD
  "welcomeUser": "Welcome, {userName}!",
  "@welcomeUser": {
    "placeholders": {
      "userName": { "type": "String" }
    }
  }
  ```

---

### 5. Documentation ✅

- [ ] **All new keys have comments**
  ```dart
  /// Title for the premium upgrade modal
  /// Used in: PremiumScreen, SettingsScreen
  String get premiumUpgradeTitle => 'Unlock Premium Power';
  ```

- [ ] **Complex translations explained**
  ```dart
  /// Displays compatibility between two signs with score
  /// @param sign1 First zodiac sign
  /// @param sign2 Second zodiac sign
  /// @param score Percentage 0-100
  String compatibilityDisplay(String sign1, String sign2, int score);
  ```

- [ ] **CHANGELOG.md updated** (if significant changes)

- [ ] **Migration notes added** (if breaking changes)

---

### 6. UI/UX Considerations ✅

- [ ] **Tested on smallest screen size**
  - iPhone SE (375x667)
  - Tested in all languages

- [ ] **No text overflow**
  - Especially for German and French (typically longest)

- [ ] **Punctuation appropriate**
  - Titles: No period
  - Descriptions: Period if complete sentence
  - Buttons: No period
  - Success: Exclamation mark OK
  - Errors: Period preferred

- [ ] **Emoji usage appropriate**
  - ✅ Premium features, celebrations
  - ❌ Error messages, settings

- [ ] **Screen reader tested**
  - VoiceOver (iOS)
  - TalkBack (Android)

---

### 7. Accessibility ✅

- [ ] **No emoji-only content**
  ```json
  ❌ "success": "✅"
  ✅ "successPurchase": "✅ Purchase successful"
  ```

- [ ] **Abbreviations avoided**
  ```json
  ❌ "compatScore": "Compat. Score"
  ✅ "compatibilityScore": "Compatibility Score"
  ```

- [ ] **Semantic labels present**
  ```json
  ❌ "button": "Click"
  ✅ "upgradeButton": "Upgrade to Premium"
  ```

- [ ] **Screen reader alternatives documented**
  ```json
  "@premiumBadge": {
    "description": "Premium badge icon",
    "screen_reader": "Premium user"
  }
  ```

---

### 8. Performance ✅

- [ ] **No excessively long translations**
  - Max recommended: 200 characters for descriptions

- [ ] **Parameterized where appropriate**
  ```json
  // ✅ GOOD - one key with parameters
  "itemCount": "{count, plural, =0{No items} other{{count} items}}"

  // ❌ BAD - multiple keys for same concept
  "noItems": "No items"
  "oneItem": "1 item"
  "manyItems": "{count} items"
  ```

---

### 9. Cultural Sensitivity ✅

- [ ] **No culturally insensitive content**
  - Check color meanings
  - Check number significance
  - Check symbol interpretations

- [ ] **Zodiac sign names localized**
  ```
  EN: Aries → ES: Aries → DE: Widder → FR: Bélier
  ```

- [ ] **Date formats appropriate**
  ```
  EN: MM/DD/YYYY
  Others: DD/MM/YYYY
  ```

- [ ] **Currency formatted correctly** (if applicable)
  ```
  EN: $9.99
  ES: 9,99 €
  DE: 9,99 €
  ```

---

### 10. Testing ✅

- [ ] **Manual testing completed**
  - [ ] Tested in all 6 languages
  - [ ] Tested on iOS
  - [ ] Tested on Android
  - [ ] Tested with dynamic type sizes

- [ ] **Automated tests pass**
  ```bash
  flutter test test/translations_test.dart
  ```

- [ ] **Screenshot comparisons**
  - Before/After for changed translations
  - All languages documented

- [ ] **Edge cases tested**
  - Very long user names
  - Empty states
  - Error states

---

## Specific Checks by Change Type

### Adding New Feature

- [ ] All UI strings have translation keys
- [ ] Empty states translated
- [ ] Error messages translated
- [ ] Loading states translated
- [ ] Success messages translated
- [ ] Help text translated
- [ ] Tooltips translated (if any)

### Modifying Existing Translations

- [ ] Impact analysis completed
  - List all screens affected
  - Document layout changes

- [ ] Backward compatibility considered
  - Old key deprecated (not deleted)
  - Migration path documented

- [ ] All usages updated
  ```bash
  # Find all usages of a key
  grep -r "oldKeyName" zodiac_app/lib/
  ```

### Refactoring Translation Keys

- [ ] Migration script created
- [ ] All references updated
- [ ] Deprecated keys marked
- [ ] Timeline for removal set
- [ ] CHANGELOG.md updated

---

## Review Comments Templates

Use these templates when requesting changes:

### Naming Convention Issue
```markdown
**Naming Convention**: Please use camelCase instead of snake_case.

Current: `premium_features`
Expected: `premiumFeatures`

See: [Style Guide - Naming Conventions](/TRANSLATION_STYLE_GUIDE.md#naming-conventions)
```

### Missing Translation
```markdown
**Missing Translation**: Portuguese (PT) translation is missing for this key.

Please add to: `zodiac_app/assets/l10n/app_pt.arb`

See: [Template](/TRANSLATION_KEY_TEMPLATE.md)
```

### Too Generic
```markdown
**Too Generic**: This key needs more context.

Current: `error`
Suggested: `errorLoadingHoroscope` or `errorNetworkConnection`

See: [Style Guide - Generic vs Specific Keys](/TRANSLATION_STYLE_GUIDE.md#generic-vs-specific-keys)
```

### Missing Documentation
```markdown
**Missing Documentation**: Please add a comment explaining what this key is for.

Example:
\`\`\`dart
/// Title for the premium upgrade modal
/// Used in: PremiumScreen, SettingsScreen
String get premiumUpgradeTitle => 'Unlock Premium Power';
\`\`\`
```

### Cultural Issue
```markdown
**Cultural Consideration**: This translation may not be appropriate for {language}.

Reason: {explanation}

Suggested alternative: {suggestion}

Please consult with a native speaker.
```

### Accessibility Issue
```markdown
**Accessibility**: This translation is not screen reader friendly.

Issue: {problem}

Suggested fix: {solution}

See: [Style Guide - Accessibility Requirements](/TRANSLATION_STYLE_GUIDE.md#accessibility-requirements)
```

---

## Approval Criteria

✅ **Approve** if:
- All checklist items are checked
- All automated tests pass
- Manual testing completed in all languages
- No cultural or accessibility concerns
- Documentation complete

⚠️ **Request Changes** if:
- Any critical items are missing
- Translation quality is poor
- Accessibility issues present
- Documentation incomplete

🛑 **Block** if:
- Breaking changes without migration plan
- Security concerns
- Legal/compliance issues
- Cultural insensitivity

---

## Quick Reference

### Naming Convention
✅ `camelCase` ❌ `snake_case`

### Common Prefixes
- `premium` - Premium features
- `error` - Error messages
- `onboarding` - Onboarding flows
- `settings` - Settings
- `compatibility` - Compatibility

### Common Suffixes
- `Title` - Screen/section titles
- `Description` - Explanatory text
- `Button` - Button labels
- `Message` - User messages

### Tone by Language
| Language | Form | Pronoun |
|----------|------|---------|
| EN | Informal | you |
| ES | Informal | tú |
| DE | Informal | du |
| FR | Formal | vous |
| IT | Informal | tu |
| PT | Informal | você |

### Punctuation
- Titles: No period
- Descriptions: Period if complete sentence
- Buttons: No period
- Success: ! OK
- Errors: . preferred

### Key Length
- Ideal: ≤ 40 characters
- Max: ≤ 60 characters

---

## Validation Commands

### Check JSON syntax
```bash
python3 -m json.tool zodiac_app/assets/l10n/app_en.arb > /dev/null
```

### Find duplicate keys
```bash
grep -o '"[^"]*":' app_en.arb | sort | uniq -d
```

### Count keys per language
```bash
grep -c '^  "[a-zA-Z]' zodiac_app/assets/l10n/app_*.arb
```

### Find snake_case keys
```bash
grep -E '"[a-z]+_[a-z_]+"' zodiac_app/assets/l10n/*.arb
```

### Generate localization files
```bash
flutter gen-l10n
```

---

## Resources

- **Style Guide**: `/TRANSLATION_STYLE_GUIDE.md`
- **Key Template**: `/TRANSLATION_KEY_TEMPLATE.md`
- **ARB Files**: `/zodiac_app/assets/l10n/`
- **Flutter Docs**: https://docs.flutter.dev/development/accessibility-and-localization/internationalization

---

## Reviewer Notes Section

Use this section to leave notes for other reviewers:

```markdown
## Reviewer Notes

**Reviewed By**: {Your Name}
**Date**: {Date}

**Summary**: {Brief summary of changes}

**Testing**:
- [ ] Tested on iOS
- [ ] Tested on Android
- [ ] Tested all 6 languages
- [ ] Tested with VoiceOver/TalkBack

**Concerns**:
- {Any concerns or questions}

**Recommendations**:
- {Any recommendations for future improvements}
```

---

**Checklist Version**: 1.0
**Last Updated**: October 15, 2025
**Maintained By**: Zodiac App Translation Team
