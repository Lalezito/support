# Translation Quick Reference Card

**Print this page and keep it visible while coding!**

---

## 📋 Naming Convention

### Standard: camelCase Only

```
✅ dailyHoroscope
✅ premiumFeatures
✅ errorNetwork
❌ daily_horoscope
❌ premium-features
❌ ErrorNetwork
```

---

## 🏷️ Key Structure Pattern

```
{domain}{Type}{Element}

Examples:
premiumUpgradeButton        (domain: premium)
compatibilityLoveScore      (domain: compatibility, type: love)
onboardingWelcomeTitle      (domain: onboarding)
errorNetworkConnection      (domain: error, type: network)
```

---

## 📌 Common Prefixes

| Domain | Prefix | Example |
|--------|--------|---------|
| **Premium** | `premium` | `premiumFeatures` |
| **Error** | `error` | `errorNetwork` |
| **Onboarding** | `onboarding` | `onboardingWelcome` |
| **Settings** | `settings` | `settingsPrivacy` |
| **Compatibility** | `compatibility` | `compatibilityLove` |
| **Horoscope** | `horoscope` | `horoscopeDaily` |
| **Cosmic Coach** | `cosmic` or `ai` | `cosmicAdvice` |

---

## 📝 Common Suffixes

| Content Type | Suffix | Example |
|--------------|--------|---------|
| **Title** | `Title` | `premiumUpgradeTitle` |
| **Description** | `Description` | `featureDescription` |
| **Button** | `Button` | `upgradeButton` |
| **Subtitle** | `Subtitle` | `welcomeSubtitle` |
| **Message** | `Message` | `successMessage` |
| **Error** | `Error` | `loadingError` |

---

## 🌍 Tone by Language

| Language | Code | Formality | Pronoun | Example |
|----------|------|-----------|---------|---------|
| English | EN | Informal | you | "Unlock your potential" |
| Spanish | ES | Informal | tú | "Desbloquea tu potencial" |
| German | DE | Informal | du | "Entdecke dein Potenzial" |
| French | FR | Formal | vous | "Découvrez votre potentiel" |
| Italian | IT | Informal | tu | "Sblocca il tuo potenziale" |
| Portuguese | PT | Informal | você | "Desbloqueie seu potencial" |

---

## ✏️ Punctuation Rules

| Use | For | Example |
|-----|-----|---------|
| **!** | Success, celebration | `"Premium activated!"` |
| **?** | Questions | `"Delete account?"` |
| **.** | Complete sentences | `"We protect your data."` |
| **None** | Titles, buttons | `"Settings"` |

---

## 😀 Emoji Guidelines

**✅ Use For:**
- Premium features
- Celebrations
- Couple features

**❌ Avoid In:**
- Error messages
- Settings
- Legal text

**Rules:**
- Max 1 emoji per string
- Place at end
- Always include text

```
✅ "Premium activated! ✅"
❌ "⚙️ Settings"
❌ "❌ Error"
```

---

## 📏 Key Length

| | Characters | Recommendation |
|---|-----------|----------------|
| **Ideal** | ≤ 40 | Aim for this |
| **Maximum** | ≤ 60 | Hard limit |
| **Too Long** | > 60 | Must refactor |

```
✅ compatibilityAnalysis (22 chars)
⚠️ onboardingPredictiveCompleteDescription (42 chars)
❌ thisWillPermanentlyDeleteAllYourData... (84 chars)
```

---

## ✅ Pre-Commit Checklist

Quick check before adding a new key:

```
□ camelCase naming
□ Domain prefix (if applicable)
□ Appropriate suffix
□ Under 60 characters
□ Self-documenting
□ No duplicates
□ All 6 languages added
□ Documented (comment)
□ Tested in UI
```

---

## 🚫 Common Mistakes

| ❌ Mistake | ✅ Fix |
|-----------|--------|
| `error` | `errorLoadingHoroscope` |
| `success` | `successPurchaseComplete` |
| `button` | `upgradeButton` |
| `premium_features` | `premiumFeatures` |
| `Premium-Content` | `premiumContent` |
| `feature1` | `premiumFeatureUnlimitedHoroscopes` |

---

## 🎯 Golden Rules

1. **Be Specific** - Add context to every key
2. **Be Consistent** - Follow naming patterns
3. **Be Clear** - Use self-documenting names
4. **Be Complete** - Translate all 6 languages
5. **Be Accessible** - Screen reader friendly

---

## 🔍 Quick Examples

### Good Key Names
```dart
// ✅ GOOD
premiumUpgradeButton
compatibilityLoveScore
errorNetworkConnection
loadingHoroscopeData
successPurchaseComplete
onboardingWelcomeTitle
settingsPrivacyPolicy
```

### Bad Key Names
```dart
// ❌ BAD
error                    // Too generic
premium_upgrade          // Wrong case
Button                   // Missing context
feature1                 // Not descriptive
settings_privacy_policy  // Wrong case
```

---

## 📦 Template (Copy & Paste)

```json
{
  "keyNameInCamelCase": "English translation",
  "@keyNameInCamelCase": {
    "description": "What this is for and where it appears",
    "screen": "ScreenName"
  }
}
```

---

## 🛠️ Validation Commands

```bash
# Validate JSON
python3 -m json.tool zodiac_app/assets/l10n/app_en.arb

# Count keys
grep -c '^  "[a-zA-Z]' app_en.arb

# Find duplicates
grep -o '"[^"]*":' app_en.arb | sort | uniq -d

# Generate localizations
flutter gen-l10n
```

---

## 📚 Full Documentation

- **Complete Style Guide**: `/TRANSLATION_STYLE_GUIDE.md`
- **Key Template**: `/TRANSLATION_KEY_TEMPLATE.md`
- **Review Checklist**: `/TRANSLATION_CODE_REVIEW_CHECKLIST.md`

---

## 💡 Need Help?

**Can't find the right name?** Ask yourself:
1. What domain? (premium, error, settings...)
2. What type? (title, button, message...)
3. What context? (upgrade, network, privacy...)

Combine: `{domain}{Type}{Context}`

Example: `premiumUpgradeButton`

---

## 🌟 Special Characters by Language

| Language | Special Characters | Example |
|----------|-------------------|---------|
| **ES** | á é í ó ú ñ ü ¿ ¡ | "¿Cuál es tu signo?" |
| **DE** | ä ö ü ß | "Glück" |
| **FR** | é è ê à ç | "Être" |
| **IT** | à è é ì ò ù | "Perché" |
| **PT** | ã õ ç á é í ó ú | "Atenção" |

---

## 📋 Domain Categories (22 Total)

1. UI_NAVIGATION - Basic UI elements
2. ACTIONS - User actions
3. HOROSCOPE - Horoscope content
4. ZODIAC_SIGNS - Signs & descriptions
5. ELEMENTS - Fire, Earth, Air, Water
6. PLANETS - Sun, Moon, Mercury...
7. MOON_PHASES - New Moon, Full Moon...
8. COMPATIBILITY - Compatibility system
9. PREMIUM - Premium features
10. COSMIC_COACH - AI life coach
11. ONBOARDING - Onboarding flows
12. SETTINGS - Settings & config
13. BIRTH_DATA - Birth info & ascendant
14. ACCOUNT - Account management
15. WELLNESS - Wellness & growth
16. GOALS - Goal tracking
17. PREDICTIONS - Predictions system
18. STATUS_FEEDBACK - Loading/success/error
19. TIME_DATES - Time & date refs
20. COUPLES - Couple features
21. ANALYTICS - Analytics & tracking
22. UNCATEGORIZED - Needs categorization

---

## ⚡ Quick Decision Tree

**Adding a new translation?**

```
Is it generic? (error, button, text)
  YES → Add context (errorNetwork, upgradeButton)
  NO → ↓

Does it fit an existing domain?
  YES → Use domain prefix
  NO → Create new domain (discuss with team)

Does it need parameters?
  YES → Use method with clear param names
  NO → Use simple getter

Is it under 40 characters?
  YES → ✅ Good to go!
  NO → Can you shorten it? If not, keep under 60.
```

---

**Version**: 1.0 | **Updated**: Oct 15, 2025 | **Team**: Zodiac App Translations
