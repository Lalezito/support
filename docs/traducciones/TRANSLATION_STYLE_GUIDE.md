# Translation Style Guide - Zodiac App

**Version:** 2.0
**Last Updated:** October 15, 2025
**Status:** Official Standard
**Supported Languages:** EN, ES, DE, FR, IT, PT

---

## Table of Contents

1. [Overview](#overview)
2. [Naming Conventions](#naming-conventions)
3. [Translation Best Practices](#translation-best-practices)
4. [Quality Standards](#quality-standards)
5. [Domain Organization](#domain-organization)
6. [Review Checklist](#review-checklist)
7. [Language-Specific Guidelines](#language-specific-guidelines)
8. [Examples](#examples)
9. [Quick Reference Card](#quick-reference-card)

---

## Overview

### Purpose

This style guide establishes standards for creating, managing, and maintaining translations in the Zodiac App across 6 languages. It ensures consistency, quality, and maintainability as the app scales.

### Key Principles

1. **Consistency**: Use standardized naming patterns across all keys
2. **Clarity**: Keys should be self-documenting and easy to understand
3. **Context**: Always provide sufficient context for translators
4. **Maintainability**: Structure keys for long-term sustainability
5. **Cultural Sensitivity**: Respect cultural differences in all languages

### Current State

- **Total Keys**: 1,376 translation keys
- **Languages**: 6 (EN, ES, DE, FR, IT, PT)
- **Coverage**: 90-100% across languages
- **Naming Mix**: 65.7% camelCase, 10.6% snake_case, 23.7% lowercase

---

## Naming Conventions

### 1. Official Standard: camelCase

**Rule**: ALL new translation keys MUST use camelCase.

```dart
// ✅ CORRECT
dailyHoroscope
premiumFeatures
compatibilityAnalysis
userProfileSettings

// ❌ INCORRECT
daily_horoscope
premium_features
compatibility_analysis
user-profile-settings
```

**Rationale**:
- Matches Dart/Flutter conventions
- Better IDE autocomplete
- Easier to read in code
- Consistent with 65%+ of existing keys

### 2. Prefix Patterns

Use domain prefixes to organize related keys logically.

#### Premium Features
```dart
premium{Feature}          // General pattern
premiumContent
premiumFeatures
premiumActivated
premiumAnalysis
premiumUpgradeButton
```

#### Error Messages
```dart
error{Context}            // General pattern
errorLoading
errorNetwork
errorPurchase
errorActivatingPremium
errorRestoringPurchases
```

#### Onboarding
```dart
onboarding{Section}{Element}    // General pattern
onboardingWelcomeTitle
onboardingWelcomeDescription
onboarding8dAnalysisTitle
onboardingCoachCompleteDescription
```

#### Settings
```dart
settings{Category}{Element}     // General pattern
settingsNotifications
settingsPrivacyPolicy
settingsDataBackup
settingsDarkMode
```

#### Compatibility
```dart
compatibility{Type}              // General pattern
compatibilityAnalysis
compatibilityScore
compatibilityLove
compatibilityFriendship
compatibility_aries_taurus_strength  // Exception for specific pairs
```

### 3. Suffix Patterns

Use consistent suffixes to indicate content type.

#### Titles
```dart
{domain}Title
welcomeTitle
premiumTitle
compatibilityTitle
```

#### Descriptions
```dart
{domain}Description
ariesDescription
premiumDescription
onboardingWelcomeDescription
```

#### Buttons
```dart
{action}Button
upgradeButton
saveButton
cancelButton
continueButton
```

#### Subtitles
```dart
{domain}Subtitle
selectSignSubtitle
welcomeSubtitle
```

#### Messages
```dart
{context}Message
successMessage
errorMessage
welcomeMessage
```

### 4. Generic vs. Specific Keys

#### Generic Keys (Use Sparingly)
Only use generic keys for truly universal terms:

```dart
// ✅ ACCEPTABLE
yes, no, ok, cancel, save, delete, edit, back, next

// ❌ AVOID - Too generic
error           → Use errorPurchase, errorNetwork
success         → Use successSaved, successPurchased
loading         → Use loadingHoroscope, loadingProducts
```

#### Specific Keys (Preferred)
Always add context to make keys self-documenting:

```dart
// ✅ PREFERRED
purchaseErrorInsufficientFunds
loadingHoroscopeData
savingUserPreferences
deletingAccountPermanently
```

### 5. Maximum Key Length

**Recommended**: 40 characters maximum
**Absolute Maximum**: 60 characters

```dart
// ✅ GOOD - 35 characters
compatibilityAnalysisLoading

// ⚠️ ACCEPTABLE - 52 characters
onboardingPredictiveCompleteDescription

// ❌ TOO LONG - 84 characters
thisWillPermanentlyDeleteAllYourBirthInformationAndPreferencesThisActionCannotBeUndone
// REFACTOR TO:
confirmPermanentDeleteWarning
```

### 6. Special Cases

#### Sign-Specific Combinations
```dart
compatibility_{sign1}_{sign2}_strength
compatibility_aries_taurus_strength
compatibility_leo_pisces_strength
```

#### Multi-word Zodiac References
```dart
// Use English names in keys, regardless of translation
aries, taurus, gemini, cancer, leo, virgo
libra, scorpio, sagittarius, capricorn, aquarius, pisces
```

#### Parameterized Keys
When a key requires dynamic content, use descriptive method names:

```dart
// ✅ GOOD
String compatibilityScoreDisplay(int score, String sign1, String sign2)
String signDescription(String signName)
String userGreeting(String userName)

// ❌ BAD
String text(Object x)
String msg(Object a, Object b)
```

---

## Translation Best Practices

### 1. Pluralization Handling

#### English (EN)
Use ICU format for plurals:

```json
"itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}"
```

#### Spanish (ES)
Gender and plural agreement:

```json
"compatibilityAnalysis": "Análisis de compatibilidad",
"compatibilityAnalyses": "Análisis de compatibilidad" // Same form
"horoscopeDaily": "Horóscopo diario",
"horoscopesDaily": "Horóscopos diarios"
```

#### German (DE)
Compound nouns and capitalization:

```json
"birthDate": "Geburtsdatum",
"birthDates": "Geburtsdaten"
```

#### French (FR)
Elision and gender:

```json
"theSun": "Le soleil" (masculine),
"theMoon": "La lune" (feminine),
"theAscendant": "L'ascendant" (vowel elision)
```

#### Italian (IT)
Gender agreement with articles:

```json
"theSign": "Il segno" (masculine),
"theCompatibility": "La compatibilità" (feminine)
```

#### Portuguese (PT)
Brazilian Portuguese standard:

```json
"youFormal": "Você" // Brazilian informal (not "Tu" or "Vossa Senhoria")
```

### 2. Gender Agreement Rules

#### Spanish (ES)
```json
// Masculine default for neutral/mixed
"premiumUser": "Usuario premium",
// Gender-neutral when possible
"person": "Persona" (grammatically feminine, but gender-neutral meaning)
```

#### German (DE)
```json
// Use gender-neutral forms
"user": "Benutzende" or "Benutzer*in" // Inclusive form
// Or traditional masculine as neutral
"user": "Benutzer"
```

#### French (FR)
```json
// Use masculine as neutral
"user": "Utilisateur",
// Or explicitly inclusive
"user": "Utilisateur/Utilisatrice"
```

#### Italian (IT)
```json
// Masculine as neutral
"user": "Utente" (already gender-neutral),
"friend": "Amico/a" // When necessary
```

#### Portuguese (PT)
```json
// Masculine as neutral
"user": "Usuário",
// Gender-neutral alternatives
"person": "Pessoa" (feminine grammatically, neutral in meaning)
```

### 3. Formal vs. Informal Tone

#### Zodiac App Standard: **Informal + Friendly**

| Language | Form | Pronoun | Example |
|----------|------|---------|---------|
| EN | Informal | you | "Unlock your cosmic potential" |
| ES | Informal | tú | "Desbloquea tu potencial cósmico" |
| DE | Informal | du | "Entdecke dein kosmisches Potenzial" |
| FR | Formal | vous | "Découvrez votre potentiel cosmique" |
| IT | Informal | tu | "Sblocca il tuo potenziale cosmico" |
| PT | Informal | você | "Desbloqueie seu potencial cósmico" |

**Exceptions**: Use formal tone for:
- Error messages
- Legal text (Terms of Service, Privacy Policy)
- Payment/subscription confirmations

### 4. Punctuation Guidelines

#### Exclamation Marks (!)
**Use for**:
- Celebration messages
- Success confirmations
- Welcome messages
- Call-to-action (sparingly)

```json
// ✅ GOOD
"premiumActivated": "Premium activated successfully!",
"welcomeTitle": "Welcome to Cosmic Coach!",

// ❌ OVERUSE
"dailyHoroscope": "Daily Horoscope!",
"settings": "Settings!"
```

#### Question Marks (?)
**Use for**:
- Direct questions
- Confirmation dialogs
- User prompts

```json
"whatsYourSign": "What's your sign?",
"areYouSure": "Are you sure?",
"deleteAccount": "Delete your account?"
```

#### Periods (.)
**Use for**:
- Complete sentences in descriptions
- Multi-sentence content
- Formal messages

**Omit for**:
- Titles and headings
- Button labels
- Short phrases

```json
// ✅ WITH PERIOD
"privacyDescription": "We protect your data with industry-standard encryption.",

// ✅ WITHOUT PERIOD
"privacyTitle": "Privacy Policy",
"saveButton": "Save"
```

### 5. Emoji Usage Guidelines

**Official Position**: Minimal and intentional

**When to use**:
- Premium/celebration contexts
- Couple/relationship features
- Specific cosmic events

**When NOT to use**:
- Error messages
- Settings/configuration
- Legal text
- Data-heavy screens

```json
// ✅ APPROPRIATE
"premiumActivated": "✅ Premium activated - Testing mode",
"coupleAdviceDefault": "Remember that open communication strengthens your connection 💕",

// ❌ INAPPROPRIATE
"errorNetwork": "❌ Network error",
"settings": "⚙️ Settings"
```

**Maximum**: 1 emoji per string
**Placement**: End of string preferred

---

## Quality Standards

### 1. Required Documentation Format

Every translation key should have a comment explaining:
1. **Purpose**: What it's for
2. **Context**: Where it appears
3. **Parameters** (if applicable): What they represent

```dart
/// Title for the premium upgrade modal
/// Used in: PremiumScreen, SettingsScreen, HoroscopeScreen
String get premiumUpgradeTitle => 'Unlock Premium Power';

/// Compatibility score display with dynamic values
/// @param score The compatibility percentage (0-100)
/// @param sign1 First zodiac sign name
/// @param sign2 Second zodiac sign name
String compatibilityScoreDisplay(int score, String sign1, String sign2) {
  return '$sign1 and $sign2: $score% compatible';
}
```

### 2. Cultural Difference Handling

#### Zodiac Sign Names
Always use localized names:

```json
// EN
"aries": "Aries"

// ES
"aries": "Aries"

// DE
"aries": "Widder"

// FR
"aries": "Bélier"

// IT
"aries": "Ariete"

// PT
"aries": "Áries"
```

#### Date Formats
Use locale-appropriate formats:

```dart
// EN: MM/DD/YYYY
"birthDateFormat": "MM/DD/YYYY"

// ES/FR/IT/PT/DE: DD/MM/YYYY
"birthDateFormat": "DD/MM/YYYY"
```

#### Color Associations
Be mindful of cultural color meanings:

```json
// Western: Red = passion, danger
// Eastern: Red = luck, prosperity

// Use context-specific translations
"luckyColorRed": "Rojo (suerte y pasión)" // ES
```

### 3. A/B Testing Translation Variants

**Naming Convention**: `{key}Variant{A|B|C}`

```dart
premiumUpgradeCTAVariantA = "Unlock Premium Now"
premiumUpgradeCTAVariantB = "Start Your Cosmic Journey"
premiumUpgradeCTAVariantC = "Upgrade to Premium"
```

**Documentation**:
```dart
/// A/B Test: Premium CTA - Experiment ID: EXP-2025-001
/// Variant A: Direct action-focused
/// Variant B: Emotional/aspirational
/// Variant C: Simple upgrade message
/// Started: 2025-10-15
/// Expected End: 2025-11-15
```

### 4. Accessibility Requirements

All translations must be **screen reader friendly**.

#### Guidelines

1. **Avoid Abbreviations**
```json
// ❌ BAD
"compatScore": "Compat. Score: 85%"

// ✅ GOOD
"compatibilityScore": "Compatibility Score: 85%"
```

2. **Provide Full Context**
```json
// ❌ BAD
"loading": "Loading..."

// ✅ GOOD
"loadingHoroscope": "Loading your daily horoscope..."
```

3. **Use Semantic Labels**
```json
// ❌ BAD
"button": "Click here"

// ✅ GOOD
"upgradeButton": "Upgrade to Premium"
```

4. **Avoid Emoji-Only Content**
```json
// ❌ BAD
"success": "✅"

// ✅ GOOD
"successPurchase": "✅ Purchase successful"
```

5. **Screen Reader Alternatives**
When using symbols, provide text alternatives:

```dart
// In ARB format
"premiumBadge": "💎",
"@premiumBadge": {
  "description": "Premium badge icon",
  "screen_reader": "Premium user"
}
```

### 5. Translation Memory & Consistency

Use consistent translations for repeated concepts:

| Concept | EN | ES | DE | FR | IT | PT |
|---------|----|----|----|----|----|----|
| Premium | Premium | Premium | Premium | Premium | Premium | Premium |
| Unlock | Unlock | Desbloquear | Freischalten | Débloquer | Sbloccare | Desbloquear |
| Compatibility | Compatibility | Compatibilidad | Kompatibilität | Compatibilité | Compatibilità | Compatibilidade |
| Horoscope | Horoscope | Horóscopo | Horoskop | Horoscope | Oroscopo | Horóscopo |
| Daily | Daily | Diario | Täglich | Quotidien | Quotidiano | Diário |

---

## Domain Organization

### 22 Official Categories

Based on comprehensive analysis, translations are organized into these domains:

#### 1. UI_NAVIGATION (79 keys)
Basic UI elements and navigation

**Placement**: Group at top of ARB file
**Prefix**: None (universal terms)

```json
"back", "next", "cancel", "save", "done", "continue"
```

#### 2. ACTIONS (34 keys)
User action verbs

**Placement**: After UI_NAVIGATION
**Prefix**: None (action verbs)

```json
"add", "edit", "delete", "share", "export", "import"
```

#### 3. HOROSCOPE (57 keys)
Core horoscope functionality

**Placement**: Early in file (core feature)
**Prefix**: `horoscope{Type}`

```json
"horoscopeDaily", "horoscopeWeekly", "horoscopeMonthly", "horoscopeYearly"
```

#### 4. ZODIAC_SIGNS (34 keys)
All zodiac signs and descriptions

**Placement**: After HOROSCOPE
**Prefix**: None (sign names are keys)

```json
"aries", "taurus", "gemini", "ariesDescription", "taurusDescription"
```

#### 5. ELEMENTS (19 keys)
Astrological elements

**Placement**: After ZODIAC_SIGNS
**Prefix**: None or `element{Name}`

```json
"fire", "earth", "air", "water", "fireActivities", "earthEnergyStable"
```

#### 6. PLANETS (16 keys)
Planetary references

**Placement**: After ELEMENTS
**Prefix**: None (planet names)

```json
"sun", "moon", "mercury", "venus", "mars", "jupiter"
```

#### 7. MOON_PHASES (8 keys)
Lunar cycle phases

**Placement**: After PLANETS
**Prefix**: None

```json
"newMoon", "fullMoon", "waxingCrescent", "waningGibbous"
```

#### 8. COMPATIBILITY (110 keys)
Compatibility analysis system

**Placement**: Major section after astrology basics
**Prefix**: `compatibility{Type}`

```json
"compatibilityAnalysis", "compatibilityScore", "compatibilityLove"
"compatibility_aries_taurus_strength"
```

#### 9. PREMIUM (73 keys)
Premium features and monetization

**Placement**: After COMPATIBILITY
**Prefix**: `premium{Feature}`

```json
"premiumFeatures", "premiumActivated", "premiumUpgradeButton"
```

#### 10. COSMIC_COACH (74 keys)
AI life coach features

**Placement**: After PREMIUM
**Prefix**: `cosmic{Feature}` or `ai{Feature}`

```json
"cosmicLifeCoach", "cosmicAdvice", "aiAnalysis"
```

#### 11. ONBOARDING (93 keys)
Onboarding flows

**Placement**: After core features
**Prefix**: `onboarding{Section}{Element}`

```json
"onboardingWelcomeTitle", "onboarding8dAnalysisDescription"
```

#### 12. SETTINGS (62 keys)
Settings and configuration

**Placement**: After onboarding
**Prefix**: `settings{Category}`

```json
"settingsNotifications", "settingsDarkMode", "settingsPrivacyPolicy"
```

#### 13. BIRTH_DATA (39 keys)
Birth information and personalization

**Placement**: After SETTINGS
**Prefix**: `birth{Type}` or `ascendant{Feature}`

```json
"birthDate", "birthTime", "ascendantSign", "calculateAscendant"
```

#### 14. ACCOUNT (34 keys)
Account management

**Placement**: After BIRTH_DATA
**Prefix**: `account{Feature}` or action verbs

```json
"signIn", "signOut", "accountBenefitsTitle", "deleteAccount"
```

#### 15. WELLNESS (24 keys)
Wellness and personal growth

**Placement**: After ACCOUNT
**Prefix**: `wellness{Category}` or `celebration{Theme}`

```json
"celebration_fitness_1", "wellness_Taurus", "mindfulness_Gemini"
```

#### 16. GOALS (4 keys)
Goal tracking system

**Placement**: After WELLNESS
**Prefix**: `goal{Feature}`

```json
"goals_empty_state", "createPrediction", "newPrediction"
```

#### 17. PREDICTIONS (5 keys)
Predictions tracking

**Placement**: After GOALS
**Prefix**: `prediction{State}` or no prefix

```json
"active", "pending", "verify", "noActivePredictions"
```

#### 18. STATUS_FEEDBACK (33 keys)
Loading, success, error states

**Placement**: Near end of file
**Prefix**: `loading{Context}`, `success{Context}`, `error{Context}`

```json
"loadingHoroscope", "successSaved", "errorNetwork"
```

#### 19. TIME_DATES (29 keys)
Time and date references

**Placement**: Near end
**Prefix**: None (day/month names)

```json
"today", "weekly", "january", "monday", "mondayShort"
```

#### 20. COUPLES (20 keys)
Couple-specific features

**Placement**: After COMPATIBILITY
**Prefix**: `couple{Feature}`

```json
"coupleChallenge.lunarCompatibility.title"
"coupleAdvice.aries"
```

#### 21. ANALYTICS (15 keys)
Analytics and tracking

**Placement**: After STATUS_FEEDBACK
**Prefix**: `analytics{Metric}` or `statistics{Metric}`

```json
"statistics_title", "current_streak_label", "success_rate_label"
```

#### 22. UNCATEGORIZED (287 keys)
Keys needing categorization

**Placement**: End of file
**Action Required**: Recategorize during refactor

---

## Review Checklist

### Pre-Commit Checklist for New Keys

Use this checklist BEFORE adding any new translation key:

```markdown
## New Translation Key Checklist

- [ ] **Naming Convention**
  - [ ] Uses camelCase (not snake_case or kebab-case)
  - [ ] Follows domain prefix pattern
  - [ ] Has appropriate suffix (Title, Description, Button, etc.)
  - [ ] Under 40 characters (60 max)

- [ ] **Uniqueness**
  - [ ] Key doesn't already exist
  - [ ] No similar keys with different casing
  - [ ] Checked for duplicates in all 6 language files

- [ ] **Documentation**
  - [ ] Added comment explaining purpose
  - [ ] Documented where it appears in app
  - [ ] Specified parameters (if applicable)

- [ ] **Translations**
  - [ ] English translation added
  - [ ] Spanish translation added
  - [ ] German translation added
  - [ ] French translation added
  - [ ] Italian translation added
  - [ ] Portuguese translation added

- [ ] **Quality**
  - [ ] Natural, conversational tone
  - [ ] Culturally appropriate for all languages
  - [ ] Screen reader friendly
  - [ ] No hardcoded emojis (unless intentional)
  - [ ] Punctuation follows guidelines

- [ ] **Context**
  - [ ] Not too generic (has sufficient context)
  - [ ] Placed in correct domain category
  - [ ] Alphabetically sorted within category

- [ ] **Testing**
  - [ ] JSON validates correctly
  - [ ] Tested in UI (all languages)
  - [ ] Tested with screen reader
  - [ ] Reviewed by native speaker (if possible)
```

### Translation Review Process

#### Phase 1: Self-Review
Translator/developer checks their own work:

1. **Spelling & Grammar**: Use language-specific spell checker
2. **Tone**: Matches app's informal, friendly voice
3. **Length**: Fits UI space constraints
4. **Context**: Makes sense without seeing code

#### Phase 2: Peer Review
Another team member reviews:

1. **Accuracy**: Meaning matches English source
2. **Naturalness**: Sounds like a native speaker wrote it
3. **Consistency**: Uses same terms as existing translations
4. **Cultural Fit**: Appropriate for target culture

#### Phase 3: Native Speaker Review
Native speaker validates:

1. **Idiomatic**: Uses natural expressions
2. **Cultural**: Respects cultural nuances
3. **Regional**: Appropriate for target region (e.g., PT-BR vs PT-PT)
4. **Professional**: Meets quality standards

#### Phase 4: QA Validation
QA team verifies:

1. **Functional**: Displays correctly in UI
2. **Layout**: Doesn't break design
3. **Responsive**: Works on all screen sizes
4. **Accessible**: Works with assistive technologies

### Regression Testing for Changed Translations

When updating existing translations:

```markdown
## Translation Update Checklist

- [ ] **Impact Analysis**
  - [ ] Identified all screens using this key
  - [ ] Checked if UI layout will break
  - [ ] Verified new length fits constraints

- [ ] **Backward Compatibility**
  - [ ] Old key deprecated (not deleted immediately)
  - [ ] Migration path documented
  - [ ] Timeline for removal set

- [ ] **Cross-Language Check**
  - [ ] Updated all 6 languages consistently
  - [ ] Meanings still aligned across languages

- [ ] **Testing**
  - [ ] Tested on smallest screen size
  - [ ] Tested with longest translation (usually DE or FR)
  - [ ] Screenshot comparisons (before/after)

- [ ] **Communication**
  - [ ] Notified affected team members
  - [ ] Updated design documentation
  - [ ] Added to release notes
```

---

## Language-Specific Guidelines

### English (EN) - Source Language

**Role**: Master reference for all translations

**Guidelines**:
1. Write for a global audience (avoid idioms)
2. Use American English spelling
3. Keep sentences short and clear
4. Avoid jargon unless necessary

**Example**:
```json
"premiumActivated": "Premium activated successfully!"
```

**Common Mistakes**:
- ❌ "Premium's been activated!" (Too casual/contracted)
- ❌ "Your premium subscription has been successfully activated and is now ready for use." (Too verbose)

---

### Spanish (ES) - Español

**Formality**: Informal (tú)
**Region**: Neutral (works for ES-MX, ES-ES, ES-AR)

**Guidelines**:
1. Use "tú" (informal you), not "usted"
2. Avoid regional slang
3. Gender-neutral when possible
4. Accents are mandatory (á, é, í, ó, ú, ñ)

**Gender Agreement**:
```json
// Masculine default for neutral
"premiumUser": "Usuario premium"

// But adapt when referring to user
"welcome": "Bienvenido/a" // Or use neutral constructions
```

**Pluralization**:
```json
"horoscope": "Horóscopo",
"horoscopes": "Horóscopos"
```

**Example**:
```json
"premiumActivated": "¡Premium activado con éxito!",
"whatsYourSign": "¿Cuál es tu signo?",
"dailyHoroscope": "Horóscopo diario"
```

**Common Mistakes**:
- ❌ "Horoscopo" (Missing accent)
- ❌ "¿Cuál es su signo?" (Too formal with "su")
- ❌ "Premium fue activado" (Unnatural construction)

---

### German (DE) - Deutsch

**Formality**: Informal (du)
**Region**: Standard High German (Hochdeutsch)

**Guidelines**:
1. Capitalize all nouns (Die Sonne, Der Mond)
2. Use compound words (Geburtstag + Datum = Geburtsdatum)
3. Use "du" (informal) for app tone
4. Respect umlauts (ä, ö, ü, ß)

**Compound Nouns**:
```json
"birthDate": "Geburtsdatum" // Geburt + Datum
"compatibility": "Kompatibilität"
```

**Word Order**:
German word order differs from English - work with native speakers.

**Example**:
```json
"premiumActivated": "Premium erfolgreich aktiviert!",
"whatsYourSign": "Was ist dein Sternzeichen?",
"dailyHoroscope": "Tageshoroskop"
```

**Common Mistakes**:
- ❌ "Geburts Datum" (Don't separate compound nouns)
- ❌ "Was ist Ihr Zeichen?" (Too formal with "Ihr")
- ❌ "tageshoroskop" (Nouns must be capitalized)

---

### French (FR) - Français

**Formality**: Formal (vous)
**Region**: Standard French (works for FR-FR, FR-CA)

**Guidelines**:
1. Use "vous" (formal you) for respectful tone
2. Apply elision (le/la → l' before vowels)
3. Gender agreement is strict
4. Accents are mandatory (é, è, ê, à, ç)

**Elision**:
```json
"theAscendant": "L'ascendant" // Not "Le ascendant"
"theAnalysis": "L'analyse"
```

**Gender**:
```json
"theSun": "Le soleil" // Masculine
"theMoon": "La lune" // Feminine
```

**Example**:
```json
"premiumActivated": "Premium activé avec succès !",
"whatsYourSign": "Quel est votre signe ?",
"dailyHoroscope": "Horoscope quotidien"
```

**Common Mistakes**:
- ❌ "Quel est ton signe ?" (Too informal with "ton")
- ❌ "Horoscope journalier" (Unnatural adjective)
- ❌ "Premium active" (Wrong gender agreement)

---

### Italian (IT) - Italiano

**Formality**: Informal (tu)
**Region**: Standard Italian

**Guidelines**:
1. Use "tu" (informal you)
2. Gender agreement with articles (il/la)
3. Apostrophe for vowel elision
4. Accents on final vowels (à, è, é, ì, ò, ù)

**Gender Agreement**:
```json
"theSign": "Il segno" // Masculine
"theCompatibility": "La compatibilità" // Feminine
```

**Elision**:
```json
"theAscendant": "L'ascendente"
"theFriend": "L'amico"
```

**Example**:
```json
"premiumActivated": "Premium attivato con successo!",
"whatsYourSign": "Qual è il tuo segno?",
"dailyHoroscope": "Oroscopo giornaliero"
```

**Common Mistakes**:
- ❌ "Qual e il tuo segno?" (Missing accent on "è")
- ❌ "La oroscopo" (Wrong gender - "oroscopo" is masculine)
- ❌ "Premium attivata" (Wrong gender - "premium" is masculine)

---

### Portuguese (PT) - Português

**Formality**: Informal (você)
**Region**: Brazilian Portuguese (PT-BR)

**Guidelines**:
1. Use "você" (Brazilian informal, not "tu" or "vós")
2. Use Brazilian spelling (not European Portuguese)
3. Gender agreement required
4. Special characters: ã, õ, ç, á, é, í, ó, ú

**Brazilian vs European**:
```json
// Brazilian (✅ USE THIS)
"screen": "Tela"
"train": "Treinar"

// European (❌ DON'T USE)
"screen": "Ecrã"
"train": "Treinar"
```

**Gender**:
```json
"premiumUser": "Usuário premium" // Masculine default
"activatedFeminine": "Ativada" // When subject is feminine
```

**Example**:
```json
"premiumActivated": "Premium ativado com sucesso!",
"whatsYourSign": "Qual é o seu signo?",
"dailyHoroscope": "Horóscopo diário"
```

**Common Mistakes**:
- ❌ "Qual é teu signo?" (Too informal even for PT-BR)
- ❌ "Horóscopo quotidiano" (European Portuguese spelling)
- ❌ "Premium ativada" (Wrong gender - "premium" is masculine)

---

## Examples

### Good Translation Key Examples

#### ✅ Example 1: Premium Feature
```dart
// KEY STRUCTURE: premium{Feature}{Element}

premiumUpgradeTitle
premiumUpgradeDescription
premiumUpgradeButton
premiumUpgradePrice
premiumUpgradeBenefits
```

**Why it's good**:
- Consistent prefix (`premium`)
- Clear hierarchy (Upgrade → Title/Description/Button)
- Self-documenting
- Easy to find with autocomplete

#### ✅ Example 2: Compatibility Analysis
```dart
// KEY STRUCTURE: compatibility{Type}{Element}

compatibilityLoveTitle
compatibilityLoveScore
compatibilityLoveStrengths
compatibilityLoveChallenges
compatibilityLoveAdvice
```

**Why it's good**:
- Domain-specific prefix
- Type specification (Love)
- Logical element naming
- Parallel structure

#### ✅ Example 3: Error Messages
```dart
// KEY STRUCTURE: error{Context}{Detail}

errorNetworkConnection
errorNetworkTimeout
errorPurchaseInsufficientFunds
errorPurchaseCanceled
errorAccountInvalidCredentials
```

**Why it's good**:
- Clear error prefix
- Context specified (Network/Purchase/Account)
- Specific detail
- Actionable for debugging

---

### Bad Translation Key Examples

#### ❌ Example 1: Too Generic
```dart
// BAD
error
success
message
text
data

// GOOD ALTERNATIVES
errorLoadingHoroscope
successPurchaseCompleted
messageWelcomeNew
textCompatibilityDescription
dataUserBirthInformation
```

**Why it's bad**:
- No context
- Not self-documenting
- Likely to cause confusion
- Hard to search/maintain

#### ❌ Example 2: Inconsistent Naming
```dart
// BAD - Mixed conventions
premium_features
PremiumContent
premiumuser
Premium-Benefits

// GOOD - Consistent camelCase
premiumFeatures
premiumContent
premiumUser
premiumBenefits
```

**Why it's bad**:
- Mixes snake_case, PascalCase, lowercase, kebab-case
- Inconsistent with codebase
- Harder to autocomplete
- Looks unprofessional

#### ❌ Example 3: Overly Long Keys
```dart
// BAD
thisMessageWillBeDisplayedToUsersWhenTheyAttemptToDeleteTheirAccountPermanently

// GOOD
confirmAccountDeletionWarning
```

**Why it's bad**:
- 84 characters (way over 40-60 limit)
- Reads like a sentence, not a key
- Hard to type and remember
- Difficult to maintain

---

### Before/After Refactoring Examples

#### Refactor 1: Generic Feature Keys

**BEFORE**:
```dart
feature1 = "Unlimited horoscopes"
feature2 = "Ad-free experience"
feature3 = "Advanced AI insights"
feature4 = "Detailed compatibility"
```

**AFTER**:
```dart
premiumFeatureUnlimitedHoroscopes = "Unlimited horoscopes"
premiumFeatureAdFree = "Ad-free experience"
premiumFeatureAdvancedAI = "Advanced AI insights"
premiumFeatureDetailedCompatibility = "Detailed compatibility"
```

**Improvements**:
- Self-documenting keys
- Clear domain (premium)
- Searchable and maintainable
- No magic numbers

---

#### Refactor 2: Error Messages

**BEFORE**:
```dart
error = "Error"
purchaseError = "Purchase error"
errorActivatingPremium = "Error activating premium"
```

**AFTER**:
```dart
errorGeneric = "An error occurred"
errorPurchaseGeneral = "Purchase error"
errorPurchaseInsufficientFunds = "Insufficient funds"
errorPurchaseCanceled = "Purchase canceled"
errorPremiumActivation = "Error activating premium"
errorPremiumRestoration = "Error restoring purchases"
```

**Improvements**:
- Specific error contexts
- Consistent prefix pattern
- Actionable for users
- Better debugging

---

#### Refactor 3: Onboarding Flow

**BEFORE**:
```dart
onboarding1Title = "Welcome"
onboarding1Desc = "Your cosmic journey begins"
onboarding2Title = "Features"
onboarding2Desc = "Explore all features"
```

**AFTER**:
```dart
onboardingWelcomeTitle = "Welcome to Cosmic Coach"
onboardingWelcomeDescription = "Your cosmic journey begins"
onboardingFeaturesTitle = "Discover Features"
onboardingFeaturesDescription = "Explore horoscopes, compatibility, and AI coaching"
```

**Improvements**:
- Descriptive section names (not numbers)
- Consistent Title/Description pattern
- Self-documenting
- Easier to reorder without breaking

---

#### Refactor 4: Compatibility Keys

**BEFORE**:
```dart
compat1 = "Love"
compat2 = "Friendship"
compat3 = "Business"
compatScore = "Score"
```

**AFTER**:
```dart
compatibilityTypeLove = "Love Compatibility"
compatibilityTypeFriendship = "Friendship Compatibility"
compatibilityTypeBusiness = "Business Compatibility"
compatibilityOverallScore = "Overall Compatibility Score"
compatibilityLoveScore = "Love Score"
compatibilityFriendshipScore = "Friendship Score"
```

**Improvements**:
- Full context in each key
- Type clearly specified
- Domain prefix consistent
- No ambiguity

---

## Quick Reference Card

**Print this page and keep it visible while coding!**

---

### Translation Quick Reference

#### Naming Convention
✅ **USE**: `camelCase`
❌ **AVOID**: `snake_case`, `kebab-case`, `PascalCase`

#### Key Structure
```
{domain}{Type}{Element}

Examples:
premiumUpgradeButton
compatibilityLoveScore
onboardingWelcomeTitle
errorNetworkConnection
```

#### Common Prefixes
| Domain | Prefix | Example |
|--------|--------|---------|
| Premium | `premium` | `premiumFeatures` |
| Error | `error` | `errorNetwork` |
| Onboarding | `onboarding` | `onboardingWelcome` |
| Settings | `settings` | `settingsPrivacy` |
| Compatibility | `compatibility` | `compatibilityLove` |

#### Common Suffixes
| Type | Suffix | Example |
|------|--------|---------|
| Title | `Title` | `welcomeTitle` |
| Description | `Description` | `premiumDescription` |
| Button | `Button` | `upgradeButton` |
| Message | `Message` | `successMessage` |

#### Tone by Language
| Language | Form | Pronoun |
|----------|------|---------|
| EN | Informal | you |
| ES | Informal | tú |
| DE | Informal | du |
| FR | Formal | vous |
| IT | Informal | tu |
| PT | Informal | você |

#### Punctuation Rules
| Use | For | Example |
|-----|-----|---------|
| ! | Success, celebration | `"Premium activated!"` |
| ? | Questions, confirmations | `"Delete account?"` |
| . | Complete sentences | `"We protect your data."` |
| None | Titles, buttons, labels | `"Settings"` |

#### Emoji Guidelines
✅ **OK**: Premium, couples, celebrations
❌ **NO**: Errors, settings, legal

**Max**: 1 emoji per string
**Place**: End of string

#### Key Length
✅ **Ideal**: ≤ 40 characters
⚠️ **Max**: ≤ 60 characters
❌ **Too long**: > 60 characters

#### Pre-Commit Checklist
- [ ] camelCase naming
- [ ] All 6 languages added
- [ ] Documented (comment)
- [ ] Tested in UI
- [ ] Screen reader friendly
- [ ] No duplicates

#### Common Mistakes
❌ Generic keys (`error`, `success`)
❌ Mixed conventions
❌ Missing context
❌ Too long (> 60 chars)
❌ No documentation
❌ Hardcoded values in UI

#### Golden Rules
1. **Be Specific**: Add context to every key
2. **Be Consistent**: Follow naming patterns
3. **Be Clear**: Self-documenting names
4. **Be Complete**: All 6 languages
5. **Be Accessible**: Screen reader friendly

---

### Translation Template

Use this template for every new translation:

```json
{
  "keyNameInCamelCase": "English translation here",
  "@keyNameInCamelCase": {
    "description": "Purpose and context of this translation",
    "placeholders": {
      "paramName": {
        "type": "String",
        "example": "example value"
      }
    }
  }
}
```

---

**End of Style Guide**

---

## Appendix A: Validation Commands

### Check for Naming Convention Violations
```bash
# Find snake_case keys in ARB files
grep -E '"[a-z]+_[a-z_]+"' zodiac_app/assets/l10n/*.arb

# Find PascalCase keys
grep -E '"[A-Z][a-zA-Z]+"' zodiac_app/assets/l10n/*.arb

# Find overly long keys (>60 chars)
grep -oE '"[^"]{61,}"' zodiac_app/assets/l10n/app_en.arb
```

### Check Translation Coverage
```bash
# Count keys per language
for file in zodiac_app/assets/l10n/app_*.arb; do
  echo "$file: $(grep -c '^  "[a-zA-Z]' $file) keys"
done

# Find missing keys in Spanish
comm -13 \
  <(grep -oE '^  "[^"]+"' zodiac_app/assets/l10n/app_es.arb | sort) \
  <(grep -oE '^  "[^"]+"' zodiac_app/assets/l10n/app_en.arb | sort)
```

### Validate JSON Syntax
```bash
# Validate all ARB files
for file in zodiac_app/assets/l10n/*.arb; do
  echo "Validating $file..."
  python3 -m json.tool $file > /dev/null && echo "✅ Valid" || echo "❌ Invalid"
done
```

---

## Appendix B: Migration Script Template

Use this template to migrate old keys to new naming convention:

```bash
#!/bin/bash
# migrate_translation_keys.sh

OLD_KEY="feature1"
NEW_KEY="premiumFeatureUnlimitedHoroscopes"

# Update all ARB files
for file in zodiac_app/assets/l10n/app_*.arb; do
  sed -i '' "s/\"$OLD_KEY\"/\"$NEW_KEY\"/g" "$file"
  echo "Updated $file"
done

# Update all Dart files
find zodiac_app/lib -name "*.dart" -exec sed -i '' "s/$OLD_KEY/$NEW_KEY/g" {} +

echo "Migration complete. Please test thoroughly!"
```

---

## Appendix C: Contributing

### How to Contribute Translations

1. **Fork** the repository
2. **Create** a feature branch: `feature/translation-{language}-{feature}`
3. **Follow** this style guide
4. **Test** translations in the app
5. **Submit** a pull request

### Translation Review SLA

- **Minor fixes** (typos, punctuation): 24 hours
- **New features** (10-50 keys): 3-5 days
- **Major updates** (100+ keys): 1-2 weeks

### Need Help?

- **Slack**: #translations
- **Email**: translations@zodiacapp.com
- **Docs**: https://docs.zodiacapp.com/translations

---

**Document Version**: 2.0
**Last Updated**: October 15, 2025
**Next Review**: January 15, 2026
**Maintained By**: Zodiac App Translation Team
