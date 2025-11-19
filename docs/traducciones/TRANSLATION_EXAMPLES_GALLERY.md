# Translation Examples Gallery

Real-world examples from the Zodiac App showing good and bad translation practices.

---

## Table of Contents

1. [Naming Convention Examples](#naming-convention-examples)
2. [Before/After Refactoring](#beforeafter-refactoring)
3. [Language-Specific Examples](#language-specific-examples)
4. [Common Patterns](#common-patterns)
5. [Error Message Examples](#error-message-examples)
6. [Premium Feature Examples](#premium-feature-examples)
7. [Accessibility Examples](#accessibility-examples)
8. [Cultural Adaptation Examples](#cultural-adaptation-examples)

---

## Naming Convention Examples

### ✅ Good Examples

#### Premium Features
```dart
// Clear, consistent, self-documenting
premiumFeatures
premiumContent
premiumActivated
premiumUpgradeTitle
premiumUpgradeDescription
premiumUpgradeButton
premiumMonthlyPrice
premiumLifetimePrice
premiumBenefitsList
```

#### Compatibility System
```dart
// Well-structured hierarchy
compatibilityAnalysis
compatibilityScore
compatibilityOverall
compatibilityLove
compatibilityFriendship
compatibilityBusiness
compatibilityStrengths
compatibilityChallenges
compatibilityAdvice
```

#### Settings
```dart
// Logical grouping
settingsTitle
settingsNotifications
settingsNotificationTime
settingsNotificationDaily
settingsPrivacyPolicy
settingsDataBackup
settingsDarkMode
settingsLanguage
```

---

### ❌ Bad Examples

#### Too Generic
```dart
// ❌ BAD - No context
error
success
loading
button
title
message

// ✅ GOOD - With context
errorLoadingHoroscope
successPurchaseComplete
loadingCompatibilityAnalysis
upgradeButton
premiumUpgradeTitle
welcomeMessage
```

#### Inconsistent Naming
```dart
// ❌ BAD - Mixed conventions
premium_features        // snake_case
PremiumContent         // PascalCase
premiumUser            // camelCase
Premium-Benefits       // kebab-case

// ✅ GOOD - Consistent camelCase
premiumFeatures
premiumContent
premiumUser
premiumBenefits
```

#### Non-Descriptive
```dart
// ❌ BAD - Generic numbering
feature1
feature2
feature3
screen1Title
button1
button2

// ✅ GOOD - Descriptive names
premiumFeatureUnlimitedHoroscopes
premiumFeatureAdFree
premiumFeatureAdvancedAI
onboardingWelcomeTitle
upgradeButton
cancelButton
```

---

## Before/After Refactoring

### Example 1: Generic Feature Keys

**BEFORE** ❌
```dart
// Non-descriptive, hard to maintain
feature1 = "Unlimited horoscopes"
feature2 = "Ad-free experience"
feature3 = "Advanced AI insights"
feature4 = "Detailed compatibility"
feature5 = "Custom birth chart"
feature6 = "Premium support"
feature7 = "Extended forecasts"
feature8 = "Relationship advice"
feature9 = "Cosmic coach access"
feature10 = "Priority content"
```

**AFTER** ✅
```dart
// Self-documenting, searchable, maintainable
premiumFeatureUnlimitedHoroscopes = "Unlimited horoscopes"
premiumFeatureAdFree = "Ad-free experience"
premiumFeatureAdvancedAI = "Advanced AI insights"
premiumFeatureDetailedCompatibility = "Detailed compatibility"
premiumFeatureCustomBirthChart = "Custom birth chart"
premiumFeaturePrioritySupport = "Premium support"
premiumFeatureExtendedForecasts = "Extended forecasts"
premiumFeatureRelationshipAdvice = "Relationship advice"
premiumFeatureCosmicCoach = "Cosmic coach access"
premiumFeaturePriorityContent = "Priority content"
```

**Impact**:
- 🔍 **Searchability**: Easy to find with IDE autocomplete
- 📖 **Readability**: Understand purpose without looking up
- 🛠️ **Maintainability**: Clear what each feature represents
- 🎯 **No Magic Numbers**: No need to remember which number is which

---

### Example 2: Error Messages

**BEFORE** ❌
```dart
// Too generic, not actionable
error = "Error"
purchaseError = "Purchase error"
errorActivatingPremium = "Error activating premium"
networkError = "Network error"
```

**AFTER** ✅
```dart
// Specific, actionable, consistent
errorGeneral = "An unexpected error occurred"
errorPurchaseGeneral = "Unable to complete purchase"
errorPurchaseInsufficientFunds = "Insufficient funds in your account"
errorPurchaseCanceled = "Purchase was canceled"
errorPurchaseNotAvailable = "This product is not available"
errorPremiumActivation = "Unable to activate premium features"
errorPremiumRestoration = "Unable to restore purchases"
errorNetworkConnection = "No internet connection"
errorNetworkTimeout = "Request timed out"
errorNetworkServerUnavailable = "Server is temporarily unavailable"
```

**Impact**:
- 🎯 **User-Friendly**: Users understand what went wrong
- 🐛 **Debugging**: Developers can quickly identify issues
- 📊 **Analytics**: Better error tracking and categorization
- 🌍 **Translation**: Easier for translators to understand context

---

### Example 3: Onboarding Flow

**BEFORE** ❌
```dart
// Numbered, hard to reorder
onboarding1Title = "Welcome"
onboarding1Desc = "Your cosmic journey begins"
onboarding2Title = "Features"
onboarding2Desc = "Explore all features"
onboarding3Title = "Premium"
onboarding3Desc = "Unlock premium features"
onboarding4Title = "Get Started"
onboarding4Desc = "Start your journey"
```

**AFTER** ✅
```dart
// Semantic, flexible, descriptive
onboardingWelcomeTitle = "Welcome to Cosmic Coach"
onboardingWelcomeDescription = "Your personal AI-powered astrological companion"
onboardingFeaturesTitle = "Discover Your Tools"
onboardingFeaturesDescription = "Explore horoscopes, compatibility, and cosmic wisdom"
onboardingPremiumTitle = "Unlock Your Potential"
onboardingPremiumDescription = "Get unlimited access to advanced features"
onboardingStartTitle = "You're All Set!"
onboardingStartDescription = "Begin your cosmic journey with personalized insights"
```

**Impact**:
- 🔄 **Flexible**: Can reorder screens without renaming keys
- 📝 **Self-Documenting**: Clear what each screen is about
- 🎨 **Designer-Friendly**: Easy to reference in design docs
- 🧪 **A/B Testing**: Can easily test different flows

---

### Example 4: Compatibility Analysis

**BEFORE** ❌
```dart
// Inconsistent, abbreviated
compat1 = "Love"
compat2 = "Friendship"
compat3 = "Business"
compatScore = "Score"
compatAnalysis = "Analysis"
compatResult = "Result"
```

**AFTER** ✅
```dart
// Complete, consistent, hierarchical
compatibilityTitle = "Compatibility Analysis"
compatibilityOverallTitle = "Overall Compatibility"
compatibilityOverallScore = "Overall Score"
compatibilityLoveTitle = "Love Compatibility"
compatibilityLoveScore = "Love Score"
compatibilityLoveDescription = "Romantic connection potential"
compatibilityFriendshipTitle = "Friendship Compatibility"
compatibilityFriendshipScore = "Friendship Score"
compatibilityFriendshipDescription = "Social bond strength"
compatibilityBusinessTitle = "Business Compatibility"
compatibilityBusinessScore = "Business Score"
compatibilityBusinessDescription = "Professional collaboration potential"
```

**Impact**:
- 🎯 **Clarity**: No ambiguity about what each key represents
- 🔍 **Searchable**: Easy to find related keys
- 📊 **Scalable**: Easy to add new compatibility types
- 🌍 **Translation**: Translators understand full context

---

## Language-Specific Examples

### Spanish (ES) - Tone & Formality

**CORRECT** ✅
```json
{
  "whatsYourSign": "¿Cuál es tu signo?",
  "premiumUpgradeTitle": "Desbloquea tu potencial cósmico",
  "dailyHoroscope": "Horóscopo diario",
  "yourCompatibility": "Tu compatibilidad",
  "saveSettings": "Guardar configuración"
}
```

**INCORRECT** ❌
```json
{
  "whatsYourSign": "¿Cuál es su signo?",          // Too formal (su)
  "premiumUpgradeTitle": "Desbloquee su potencial", // Too formal (usted)
  "dailyHoroscope": "Horoscopo diario",            // Missing accent
  "yourCompatibility": "Su compatibilidad",        // Too formal
  "saveSettings": "Guardar ajustes"                // Inconsistent terminology
}
```

**Notes**:
- Use "tú" (informal), not "usted" (formal)
- Always include accents (á, é, í, ó, ú, ñ)
- Be consistent with terminology (configuración vs ajustes)

---

### German (DE) - Capitalization & Compounds

**CORRECT** ✅
```json
{
  "birthDate": "Geburtsdatum",
  "dailyHoroscope": "Tageshoroskop",
  "compatibility": "Kompatibilität",
  "settings": "Einstellungen",
  "premiumUser": "Premium-Benutzer"
}
```

**INCORRECT** ❌
```json
{
  "birthDate": "geburts datum",        // Not capitalized, separated
  "dailyHoroscope": "tageshoroskop",   // Not capitalized
  "compatibility": "Kompatibilitat",   // Missing umlaut
  "settings": "einstellungen",         // Not capitalized
  "premiumUser": "premium benutzer"    // Not capitalized, separated
}
```

**Notes**:
- All nouns MUST be capitalized
- Compound words written as one word (Geburtsdatum, not Geburts Datum)
- Umlauts are mandatory (ä, ö, ü, ß)
- Use hyphens for certain compounds (Premium-Benutzer)

---

### French (FR) - Elision & Gender

**CORRECT** ✅
```json
{
  "theAscendant": "L'ascendant",
  "theSun": "Le soleil",
  "theMoon": "La lune",
  "theCompatibility": "La compatibilité",
  "yourHoroscope": "Votre horoscope",
  "dailyAdvice": "Conseil quotidien"
}
```

**INCORRECT** ❌
```json
{
  "theAscendant": "Le ascendant",           // No elision
  "theSun": "La soleil",                    // Wrong gender
  "theMoon": "Le lune",                     // Wrong gender
  "theCompatibility": "Le compatibilité",   // Wrong gender
  "yourHoroscope": "Ton horoscope",         // Too informal
  "dailyAdvice": "Conseil journalier"       // Unnatural
}
```

**Notes**:
- Apply elision: le/la → l' before vowels
- Gender agreement is strict (le/la)
- Use "vous" (formal), not "tu" (informal)
- Use "quotidien" for "daily" (not "journalier")

---

### Portuguese (PT) - Brazilian vs European

**CORRECT** ✅ (Brazilian Portuguese)
```json
{
  "screen": "Tela",
  "train": "Treinar",
  "download": "Baixar",
  "youFormal": "Você",
  "cellPhone": "Celular",
  "email": "E-mail"
}
```

**INCORRECT** ❌ (European Portuguese)
```json
{
  "screen": "Ecrã",               // European spelling
  "train": "Treinar",             // Same in both
  "download": "Descarregar",      // European term
  "youFormal": "O senhor",        // Too formal
  "cellPhone": "Telemóvel",       // European term
  "email": "Correio eletrónico"   // European term
}
```

**Notes**:
- Use Brazilian Portuguese (PT-BR), not European (PT-PT)
- Use "você" (informal Brazilian), not "o senhor" or "tu"
- Be aware of vocabulary differences (tela vs ecrã)

---

## Common Patterns

### Pattern 1: Screen Title + Description + Button

```json
{
  "{screenName}Title": "Screen Title",
  "{screenName}Description": "Detailed description of what this screen does",
  "{screenName}Button": "Primary Action"
}
```

**Example - Premium Upgrade**:
```json
{
  "premiumUpgradeTitle": "Unlock Your Cosmic Potential",
  "premiumUpgradeDescription": "Get unlimited access to advanced horoscopes, AI-powered insights, and personalized compatibility analysis",
  "premiumUpgradeButton": "Upgrade to Premium"
}
```

**Translations**:

**Spanish**:
```json
{
  "premiumUpgradeTitle": "Desbloquea tu potencial cósmico",
  "premiumUpgradeDescription": "Obtén acceso ilimitado a horóscopos avanzados, insights impulsados por IA y análisis de compatibilidad personalizado",
  "premiumUpgradeButton": "Actualizar a Premium"
}
```

**German**:
```json
{
  "premiumUpgradeTitle": "Entdecke dein kosmisches Potenzial",
  "premiumUpgradeDescription": "Erhalte unbegrenzten Zugang zu erweiterten Horoskopen, KI-gestützten Einblicken und personalisierten Kompatibilitätsanalysen",
  "premiumUpgradeButton": "Auf Premium upgraden"
}
```

**French**:
```json
{
  "premiumUpgradeTitle": "Découvrez votre potentiel cosmique",
  "premiumUpgradeDescription": "Obtenez un accès illimité aux horoscopes avancés, aux insights alimentés par l'IA et à l'analyse de compatibilité personnalisée",
  "premiumUpgradeButton": "Passer à Premium"
}
```

---

### Pattern 2: Empty State + Call to Action

```json
{
  "{feature}Empty": "No {items} yet",
  "{feature}EmptySubtitle": "Encouraging message to take action",
  "{feature}EmptyButton": "Create First {Item}"
}
```

**Example - Predictions**:
```json
{
  "predictionsEmpty": "No Active Predictions",
  "predictionsEmptySubtitle": "Start tracking your cosmic predictions to see how accurate they are over time",
  "predictionsEmptyButton": "Create First Prediction"
}
```

**Translations**:

**Spanish**:
```json
{
  "predictionsEmpty": "No hay predicciones activas",
  "predictionsEmptySubtitle": "Comienza a rastrear tus predicciones cósmicas para ver qué tan precisas son con el tiempo",
  "predictionsEmptyButton": "Crear primera predicción"
}
```

**Italian**:
```json
{
  "predictionsEmpty": "Nessuna previsione attiva",
  "predictionsEmptySubtitle": "Inizia a tracciare le tue previsioni cosmiche per vedere quanto sono accurate nel tempo",
  "predictionsEmptyButton": "Crea prima previsione"
}
```

---

### Pattern 3: Loading + Success + Error

```json
{
  "loading{Feature}": "Loading {feature}...",
  "success{Action}": "{Action} successful!",
  "error{Context}": "Unable to {action}. Please try again."
}
```

**Example - Purchase Flow**:
```json
{
  "loadingPurchase": "Processing your purchase...",
  "successPurchase": "Purchase completed successfully!",
  "errorPurchaseGeneral": "Unable to complete purchase. Please try again.",
  "errorPurchaseInsufficientFunds": "Insufficient funds in your account",
  "errorPurchaseCanceled": "Purchase was canceled"
}
```

---

## Error Message Examples

### Clear & Actionable Errors

**GOOD** ✅
```json
{
  "errorNetworkConnection": "No internet connection. Please check your network settings and try again.",
  "errorPurchaseInsufficientFunds": "Your payment method has insufficient funds. Please update your payment information.",
  "errorAccountInvalidCredentials": "Invalid email or password. Please check your credentials and try again.",
  "errorBirthDateInvalid": "Please enter a valid birth date in MM/DD/YYYY format.",
  "errorLocationNotFound": "Location not found. Please try a different search term."
}
```

**BAD** ❌
```json
{
  "error": "Error",
  "errorGeneral": "Something went wrong",
  "errorPurchase": "Purchase error",
  "errorAccount": "Account error",
  "errorBirthDate": "Invalid input"
}
```

**Why the good examples are better**:
- 🎯 **Specific**: User knows exactly what went wrong
- 🛠️ **Actionable**: Suggests how to fix the problem
- 📖 **Clear**: No technical jargon
- 🌍 **Translatable**: Provides full context for translators

---

### Technical vs User-Friendly Errors

**TECHNICAL** ❌ (Too technical for users)
```json
{
  "errorNetwork": "HTTP 500 Internal Server Error",
  "errorPurchase": "SKU not found in RevenueCat catalog",
  "errorAuth": "JWT token expired at 1634567890"
}
```

**USER-FRIENDLY** ✅
```json
{
  "errorNetwork": "Our servers are currently unavailable. Please try again in a few minutes.",
  "errorPurchase": "This product is currently unavailable. Please try again later.",
  "errorAuth": "Your session has expired. Please sign in again."
}
```

---

## Premium Feature Examples

### Feature List

**Structured & Consistent**:
```json
{
  "premiumFeatureUnlimitedHoroscopes": "Unlimited daily, weekly, and monthly horoscopes",
  "premiumFeatureAdFree": "Ad-free experience across the entire app",
  "premiumFeatureAdvancedAI": "Advanced AI-powered cosmic insights",
  "premiumFeatureDetailedCompatibility": "In-depth compatibility analysis for all signs",
  "premiumFeatureCustomBirthChart": "Personalized birth chart with ascendant analysis",
  "premiumFeaturePrioritySupport": "Priority customer support",
  "premiumFeatureExtendedForecasts": "Extended 30-day and yearly forecasts",
  "premiumFeatureRelationshipAdvice": "AI-powered relationship advice and tips",
  "premiumFeatureCosmicCoach": "24/7 access to your AI Cosmic Life Coach",
  "premiumFeaturePriorityContent": "Early access to new features and content"
}
```

**All 6 Languages**:

**English**:
```json
"premiumFeatureUnlimitedHoroscopes": "Unlimited daily, weekly, and monthly horoscopes"
```

**Spanish**:
```json
"premiumFeatureUnlimitedHoroscopes": "Horóscopos diarios, semanales y mensuales ilimitados"
```

**German**:
```json
"premiumFeatureUnlimitedHoroscopes": "Unbegrenzte tägliche, wöchentliche und monatliche Horoskope"
```

**French**:
```json
"premiumFeatureUnlimitedHoroscopes": "Horoscopes quotidiens, hebdomadaires et mensuels illimités"
```

**Italian**:
```json
"premiumFeatureUnlimitedHoroscopes": "Oroscopi giornalieri, settimanali e mensili illimitati"
```

**Portuguese**:
```json
"premiumFeatureUnlimitedHoroscopes": "Horóscopos diários, semanais e mensais ilimitados"
```

---

## Accessibility Examples

### Screen Reader Friendly

**BAD** ❌ (Not accessible)
```json
{
  "upgradeButton": "→",
  "closeButton": "×",
  "premiumBadge": "💎",
  "loading": "..."
}
```

**GOOD** ✅ (Accessible)
```json
{
  "upgradeButton": "Upgrade to Premium",
  "closeButton": "Close",
  "premiumBadge": "💎 Premium",
  "loading": "Loading your horoscope..."
}
```

**With ARB Metadata**:
```json
{
  "premiumBadge": "💎",
  "@premiumBadge": {
    "description": "Premium badge icon",
    "screen_reader": "Premium user badge"
  }
}
```

---

### Abbreviations Avoided

**BAD** ❌
```json
{
  "compatScore": "Compat. Score: 85%",
  "birthDate": "DOB: 01/15/1990",
  "premiumSub": "Premium Sub.",
  "notifSettings": "Notif. Settings"
}
```

**GOOD** ✅
```json
{
  "compatibilityScore": "Compatibility Score: 85%",
  "birthDate": "Birth Date: January 15, 1990",
  "premiumSubscription": "Premium Subscription",
  "notificationSettings": "Notification Settings"
}
```

---

## Cultural Adaptation Examples

### Zodiac Sign Names

**Localized Properly**:

| English | Spanish | German | French | Italian | Portuguese |
|---------|---------|--------|--------|---------|------------|
| Aries | Aries | Widder | Bélier | Ariete | Áries |
| Taurus | Tauro | Stier | Taureau | Toro | Touro |
| Gemini | Géminis | Zwillinge | Gémeaux | Gemelli | Gêmeos |
| Cancer | Cáncer | Krebs | Cancer | Cancro | Câncer |
| Leo | Leo | Löwe | Lion | Leone | Leão |
| Virgo | Virgo | Jungfrau | Vierge | Vergine | Virgem |
| Libra | Libra | Waage | Balance | Bilancia | Libra |
| Scorpio | Escorpio | Skorpion | Scorpion | Scorpione | Escorpião |
| Sagittarius | Sagitario | Schütze | Sagittaire | Sagittario | Sagitário |
| Capricorn | Capricornio | Steinbock | Capricorne | Capricorno | Capricórnio |
| Aquarius | Acuario | Wassermann | Verseau | Acquario | Aquário |
| Pisces | Piscis | Fische | Poissons | Pesci | Peixes |

---

### Date Formats

**English (US)**:
```
MM/DD/YYYY
01/15/2025
```

**Spanish/German/French/Italian/Portuguese**:
```
DD/MM/YYYY
15/01/2025
```

**In Code**:
```dart
// Don't hardcode formats
String formatDate(DateTime date, String locale) {
  if (locale == 'en') {
    return '${date.month}/${date.day}/${date.year}';
  } else {
    return '${date.day}/${date.month}/${date.year}';
  }
}
```

---

### Color Meanings

Be aware that colors have different cultural meanings:

**Red**:
- Western: Passion, danger, love
- Eastern: Luck, prosperity, celebration

**White**:
- Western: Purity, peace, innocence
- Eastern: Mourning, death

**Example - Lucky Color**:
```json
{
  "luckyColorRed": "Red - Passion and energy",
  "@luckyColorRed": {
    "context": "Western interpretation of red as lucky color"
  }
}
```

**Spanish (neutral)**:
```json
"luckyColorRed": "Rojo - Pasión y energía"
```

---

## Real Zodiac App Examples

### From Actual Codebase

#### Good Example: Compatibility Strengths

```dart
// From app_en.arb (well-structured)
"compatibility_aries_taurus_strength": "Aries' passion ignites Taurus' sensuality, creating a powerful physical connection"
"compatibility_gemini_libra_strength": "Both air signs share intellectual compatibility and love for social connections"
"compatibility_cancer_scorpio_strength": "Deep emotional understanding and intuitive connection between water signs"
```

**Why it's good**:
- Consistent pattern: `compatibility_{sign1}_{sign2}_strength`
- Self-documenting
- Easy to generate programmatically
- Clear what each key represents

---

#### Refactored Example: Premium Tiers

**BEFORE** (from old codebase):
```dart
tier1 = "Cosmic"
tier2 = "Stellar"
tier3 = "Universe"
desc1 = "Basic premium features"
desc2 = "Advanced AI features"
desc3 = "Lifetime access"
```

**AFTER** (current best practice):
```dart
premiumTierCosmicName = "Cosmic Tier"
premiumTierCosmicDescription = "Access to all basic premium features"
premiumTierStellarName = "Stellar Tier"
premiumTierStellarDescription = "Everything from Cosmic Tier + Advanced Astrological AI"
premiumTierUniverseName = "Universe Tier"
premiumTierUniverseDescription = "All Cosmic Tier features forever"
```

---

## Summary Checklist

When creating translations, ensure:

- [ ] **Naming**: camelCase, domain prefix, appropriate suffix
- [ ] **Length**: Under 60 characters
- [ ] **Context**: Specific, not generic
- [ ] **Coverage**: All 6 languages
- [ ] **Quality**: Natural, accurate, appropriate tone
- [ ] **Documentation**: Commented and explained
- [ ] **Testing**: Tested in UI, all languages
- [ ] **Accessibility**: Screen reader friendly
- [ ] **Cultural**: Appropriate for all cultures

---

**Document Version**: 1.0
**Last Updated**: October 15, 2025
**Maintained By**: Zodiac App Translation Team
