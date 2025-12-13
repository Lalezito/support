# COMPREHENSIVE LOCALIZATION & TRANSLATION SYSTEM ANALYSIS
## Zodiac App - Complete i18n Review

**Analysis Date:** October 29, 2025  
**Analyst:** Claude Code Agent  
**Project:** Zodiac App (appstore.zodia)

---

## EXECUTIVE SUMMARY

This report provides a complete analysis of the Zodiac App's internationalization (i18n) and localization (l10n) system, covering translation completeness, hardcoded strings, RTL support, and recommendations for achieving full i18n coverage.

### Quick Stats
- **Languages Implemented:** 6 (English, Spanish, German, French, Italian, Portuguese)
- **Languages Missing:** 5 (Japanese, Chinese, Arabic, Hindi, Russian)
- **Total Translation Keys:** 1,616 (in English base)
- **Hardcoded Strings Found:** 528+ strings across 64 files
- **RTL Support:** Partial (infrastructure exists, but Arabic not configured)
- **Translation Completeness:** 91.3% - 100.4% across implemented languages

---

## 1. TRANSLATION COMPLETENESS BY LANGUAGE

### 1.1 Coverage Analysis

| Language | Keys | Coverage | Status |
|----------|------|----------|--------|
| **English (en)** | 1,616/1,616 | 100.0% | ✅ Base language |
| **Spanish (es)** | 1,622/1,616 | 100.4% | ✅ Complete (6 extra keys) |
| **German (de)** | 1,530/1,616 | 94.7% | ⚠️ Missing 163 keys |
| **French (fr)** | 1,475/1,616 | 91.3% | ⚠️ Missing 163 keys |
| **Italian (it)** | 1,516/1,616 | 93.8% | ⚠️ Missing 163 keys |
| **Portuguese (pt)** | 1,480/1,616 | 91.6% | ⚠️ Missing 163 keys |
| **Japanese (ja)** | 0/1,616 | 0% | ❌ Not implemented |
| **Chinese (zh)** | 0/1,616 | 0% | ❌ Not implemented |
| **Arabic (ar)** | 0/1,616 | 0% | ❌ Not implemented |
| **Hindi (hi)** | 0/1,616 | 0% | ❌ Not implemented |
| **Russian (ru)** | 0/1,616 | 0% | ❌ Not implemented |

### 1.2 Critical Missing Keys

**163 keys missing from ALL non-English languages (de, fr, it, pt):**

These are the most critical gaps affecting 4 out of 6 implemented languages:

#### Analytics Features (25 keys)
- `analyticsTitle`, `analyticsJourneyTitle`
- `analyticsReadingStreakTitle`, `analyticsWeeklyActivity`
- `analyticsPremiumFeaturesTitle`, `analyticsGoalsProgressTitle`
- `analyticsAdvancedChartsFeature`, `analyticsCosmicCoachFeature`
- `analyticsCompatibilityProFeature`, `analyticsCompatibilityLabel`
- And 15 more analytics-related keys

#### Goal Planner Features (18 keys)
- `generate_button`, `goals_empty_state`
- `goal_completed_success`, `new_goals_generated`
- `smart_goals_generated`, `completeGoalQuestion`
- `confirmCompleteGoal`, `confirmDeleteGoal`
- `deleteGoal`, `pauseGoal`
- And 8 more goal-related keys

#### Celebration Messages (42 keys)
- All `celebration_*` keys for various categories:
  - Adventure, Career, Creativity, Finance, Fitness
  - Growth, Healing, Leadership, Learning
  - Mindfulness, Nature, Relationships, Service, Wellness

#### Empty State Messages (32 keys)
- All `emptyState*` keys covering:
  - No birth data, No charts, No compatibility
  - No connection, No favorites, No history
  - No horoscopes, No notifications, No search results
  - Coming soon states

#### Motivational Content (20+ keys)
- Life area motivations: `adventure`, `career`, `creativity`, `finance`
- `fitness`, `growth`, `healing`, `leadership`
- `learning`, `mindfulness`, `nature`, `relationships`
- `service`, `wellness`
- Plus zodiac-specific variants (e.g., `adventure_Sagittarius`)

#### Statistics & Progress (8 keys)
- `statistics_title`, `current_streak_label`
- `success_rate_label`, `this_week_label`
- `total_completed_label`, `top_categories_label`

### 1.3 Translation Quality Metrics

| Language | Avg Length vs EN | Suspiciously Short | Suspiciously Long | Untranslated Strings |
|----------|------------------|--------------------|--------------------|---------------------|
| Spanish | 113.7% | 3 | 12 | 18 |
| German | 119.3% | 10 | 13 | 22 |
| French | 119.9% | 18 | 14 | 29 |
| Italian | 113.3% | 9 | 5 | 12 |
| Portuguese | 107.0% | 27 | 3 | 14 |

**Key Findings:**
- French and German translations tend to be ~20% longer than English (expected)
- Portuguese has 27 suspiciously short translations (needs review)
- French has 29 untranslated strings (identical to English)
- Spanish has the best overall quality with only 18 untranslated strings

### 1.4 Special Character Support

All implemented languages properly support special characters:

| Language | Accented Characters | Special Punctuation | Unicode Support |
|----------|---------------------|---------------------|-----------------|
| English | - | - | 179 chars |
| Spanish | 1,003 | 89 (¿¡) | 160 chars |
| German | 606 (äöüß) | - | 133 chars |
| French | 1,427 (éèêàç) | - | 125 chars |
| Italian | 224 | - | 74 chars |
| Portuguese | 1,318 (ãõç) | - | 81 chars |

✅ **Verdict:** All languages have proper encoding and special character support.

---

## 2. MISSING LANGUAGES ANALYSIS

### 2.1 Not Implemented (5 Languages)

The following languages mentioned in requirements are completely missing:

1. **Japanese (ja)** - 0% implemented
2. **Chinese (zh)** - 0% implemented  
3. **Arabic (ar)** - 0% implemented (RTL required)
4. **Hindi (hi)** - 0% implemented
5. **Russian (ru)** - 0% implemented

### 2.2 Implementation Requirements

To add these languages, you need:

#### For All Languages:
- Create `app_XX.arb` files with all 1,616 keys
- Add locale to `main.dart` supportedLocales
- Generate localizations: `flutter gen-l10n`
- Professional translation of all strings

#### Additional for Arabic (RTL):
- Configure RTL text direction support
- Test UI layouts for RTL compatibility
- Verify that all custom widgets support RTL
- Add Arabic-specific font support if needed

#### Estimated Effort:
- **Per language:** ~40-60 hours (professional translation + QA)
- **Arabic (with RTL):** +20 hours (RTL implementation and testing)
- **Total for 5 languages:** ~220-320 hours

---

## 3. HARDCODED STRINGS ANALYSIS

### 3.1 Overview

**Total Hardcoded Strings:** 528+  
**Files Affected:** 64 files  
**Critical Impact:** HIGH - These strings are not translatable

### 3.2 Breakdown by Category

| Category | Count | Severity | Priority |
|----------|-------|----------|----------|
| **Titles** | 314 | HIGH | P0 |
| **Descriptions** | 138 | HIGH | P0 |
| **Debug/Dev** | 25 | LOW | P3 |
| **Buttons** | 23 | HIGH | P0 |
| **Success Messages** | 19 | MEDIUM | P1 |
| **Error Messages** | 9 | MEDIUM | P1 |

### 3.3 High-Priority Hardcoded Strings

#### User-Facing UI (Top Priority)

**Example from compatibility_screen.dart:**
```dart
Text("Selecciona el signo de tu pareja")  // Spanish hardcoded!
Text("Analyse Multidimensionnelle")       // French hardcoded!
Text("Évaluation en 8 catégories clés")   // French hardcoded!
```

**Example from premium_screen.dart:**
```dart
Text("Success!")
Text("Get Started")
Text("Purchases Restored!")
```

**Example from ascendant_profile_screen.dart:**
```dart
Text("Calculating your rising sign...")
Text("Unable to load ascendant data")
Text("Please complete your birth data in Settings")
```

#### Goal Planner Features
```dart
Text("✅ Goal created successfully!")
Text("Create Goal")
Text("Focus Area")
Text("This Week")
Text("Key Actions:")
```

#### Empty States
```dart
Text("No goals yet. Generate some below!")
Text("Stellar Tier Required")
Text("Goal Planner is an exclusive feature for Stellar tier members.")
```

### 3.4 Files with Most Hardcoded Strings

1. **design_system/zodiac_implementation_guide.dart** - 37 strings
2. **services/ai_insights/ai_insights_generator_service.dart** - 34 strings
3. **screens/premium_screen.dart** - 33 strings
4. **screens/compatibility_screen.dart** - 26 strings (MIXED LANGUAGES!)
5. **debug/debug_premium_panel.dart** - 20 strings
6. **screens/personalization_onboarding_screen.dart** - 17 strings
7. **screens/ascendant_profile_screen.dart** - 15 strings

### 3.5 Critical Issue: Mixed Language Hardcoding

**SEVERE BUG FOUND:** `compatibility_screen.dart` contains hardcoded strings in MULTIPLE languages:
- Spanish: "Selecciona el signo de tu pareja"
- French: "Analyse Multidimensionnelle", "Évaluation en 8 catégories clés"

This means the app will show the wrong language regardless of user settings!

---

## 4. RTL (RIGHT-TO-LEFT) SUPPORT ANALYSIS

### 4.1 Current Status

**Infrastructure:** ✅ Partially implemented  
**Arabic Language:** ❌ Not configured  
**Testing:** ❌ No RTL testing done

### 4.2 RTL-Related Code

**Files with RTL support:** 30 files contain RTL-related code:
- `TextDirection` usage found in 30+ files
- `Directionality` widgets implemented
- Generated localization files include RTL support

**Example from codebase:**
```dart
// RTL support exists in accessibility components
TextDirection textDirection = ...
Directionality(
  textDirection: TextDirection.rtl,
  child: ...
)
```

### 4.3 Main Configuration Gap

**Critical Issue in main.dart:**
```dart
supportedLocales: const [
  Locale('en', 'US'),
  Locale('es', 'ES'),
  Locale('fr', 'FR'),
  Locale('de', 'DE'),
  Locale('it', 'IT'),
  Locale('pt', 'PT'),
],
```

❌ **Arabic (ar) locale is NOT in the list!**

### 4.4 RTL Implementation Checklist

To properly support Arabic:

- [ ] Create `app_ar.arb` with all 1,616 keys translated to Arabic
- [ ] Add `Locale('ar', 'SA')` to supportedLocales in main.dart
- [ ] Run `flutter gen-l10n` to generate Arabic localizations
- [ ] Test all screens in RTL mode
- [ ] Fix any UI layout issues (hardcoded alignment, padding issues)
- [ ] Test custom widgets for RTL compatibility
- [ ] Verify text input fields work correctly with RTL
- [ ] Test navigation animations with RTL
- [ ] Validate that icons and images flip appropriately
- [ ] Add Arabic font if default doesn't render well

**Estimated Effort:** 40-60 hours (translation) + 20 hours (RTL testing and fixes)

---

## 5. TRANSLATION GENERATION SCRIPTS

### 5.1 Available Tools

The project has excellent automation infrastructure:

#### 1. **fix_translations_automated.py**
- **Location:** `/scripts/fix_translations_automated.py`
- **Features:**
  - Fixes spacing issues in keys
  - Consolidates duplicate keys
  - Adds missing keys
  - Validates key consistency
  - Checks for English text in translations
- **Usage:** `python3 scripts/fix_translations_automated.py [--dry-run] [--backup]`

#### 2. **validate_translations.dart**
- **Location:** `/scripts/validate_translations.dart`
- **Features:**
  - Validates key parity across languages
  - Checks naming conventions
  - Detects English text in non-English files
  - Checks for [TRANSLATE] placeholders
  - Calculates translation quality scores
- **Usage:** `dart run scripts/validate_translations.dart [--verbose] [--strict]`

### 5.2 Translation Workflow

**Recommended workflow for adding new translations:**

1. **Update English base** (`app_en.arb`)
2. **Run fix script:** `python3 scripts/fix_translations_automated.py --backup`
3. **Translate missing keys** in other language files
4. **Validate:** `dart run scripts/validate_translations.dart --verbose`
5. **Fix any issues** reported by validation
6. **Test:** `flutter gen-l10n && flutter run`

---

## 6. CONSISTENCY ANALYSIS

### 6.1 Naming Conventions

**Analysis of English keys (app_en.arb):**

| Convention | Keys | Percentage |
|------------|------|------------|
| camelCase | Primary | ~85% |
| snake_case | Some | ~8% |
| mixed | Problem | ~5% |
| lowercase | Minimal | ~2% |

**Issues Found:**
- **Mixed naming:** Some keys use both camelCase AND snake_case (e.g., `celebration_adventure_1`)
- **Inconsistent prefixes:** Some categories use prefixes, others don't
- **Legacy keys:** Some old keys don't follow current conventions

**Recommendation:** Standardize on camelCase for all new keys.

### 6.2 Key Organization

**Current structure (by prefix analysis):**

| Category | Key Count | Examples |
|----------|-----------|----------|
| Compatibility | 171 | `compatibility_*`, `compatibilityScore` |
| Celebration | 42 | `celebration_adventure_1`, `celebration_career_1` |
| Analytics | 25 | `analyticsTitle`, `analyticsReadings` |
| Empty State | 32 | `emptyStateGenericTitle`, `emptyStateNoData` |
| Premium | 50+ | `premiumFeatures`, `premiumAnalysisTitle` |
| Goal Planner | 20+ | `completeGoalQuestion`, `pauseGoal` |
| Other | 1,356 | Various UI strings |

### 6.3 Duplicate Keys Across Languages

**Spanish (es)** has 6 extra keys not in English:
- `placeholders`
- `sign`, `sign1`, `sign2`
- `trialValidityWarning`
- `type`

**German (de)** has 77 extra keys including:
- Duplicate compatibility strings
- Old prediction-related keys

**French (fr)** has 22 extra keys
**Italian (it)** has 63 extra keys
**Portuguese (pt)** has 27 extra keys

**Recommendation:** Clean up extra keys - they should match English base exactly.

---

## 7. SPECIAL FORMATTING & PARAMETERS

### 7.1 Parameterized Strings

The system properly supports parameterized strings using ICU MessageFormat:

**Examples from app_en.arb:**
```json
"analyticsGoalsCompleted": "of {total} completed",
"new_goals_generated": "✨ New goals generated for {userSign}",
"smart_goals_generated": "🧠 Smart goals generated for {userSign}"
```

**Usage in code:**
```dart
AppLocalizations.of(context)!.new_goals_generated(userSign: 'Leo')
```

### 7.2 Plural Support

**Limited plural support found.** Most strings use simple substitution rather than proper plural forms.

**Recommendation:** Implement ICU plural syntax for better multilingual support:
```json
"daysCount": "{count, plural, =0{no days} =1{1 day} other{{count} days}}"
```

### 7.3 Emoji Usage

**Extensive emoji usage found** (~179 Unicode characters in English alone):
- ✅ Properly encoded in UTF-8
- ✅ Consistent across languages
- ⚠️ May not render identically on all platforms

**Examples:**
- Goal celebrations: 🎨, 🗺️, 💪, 🌟, ✨
- Analytics: 📊, 📈, 🏆
- Life areas: ❤️, 💰, 🧘, 🌿

---

## 8. LOCALIZATION SYSTEM GAPS

### 8.1 Critical Gaps (P0)

1. **Hardcoded Strings** (528+ strings)
   - Impact: Entire features not translatable
   - Effort: 40-60 hours to fix
   - Priority: IMMEDIATE

2. **Missing Languages** (5 languages)
   - Impact: Cannot serve users in Japan, China, Arabia, India, Russia
   - Effort: 220-320 hours total
   - Priority: HIGH

3. **Incomplete Translations** (163 keys missing from 4 languages)
   - Impact: Broken features in de, fr, it, pt
   - Effort: 20-30 hours
   - Priority: HIGH

### 8.2 Major Gaps (P1)

4. **RTL Support Not Configured**
   - Impact: Cannot support Arabic properly
   - Effort: 60-80 hours
   - Priority: MEDIUM-HIGH

5. **Mixed Language Hardcoding Bug**
   - Impact: Wrong language shown in compatibility screen
   - Effort: 2 hours
   - Priority: IMMEDIATE

6. **No Plural Forms**
   - Impact: Grammatically incorrect in many languages
   - Effort: 10-15 hours
   - Priority: MEDIUM

### 8.3 Minor Gaps (P2)

7. **Inconsistent Naming Conventions**
   - Impact: Developer confusion, harder maintenance
   - Effort: 5-10 hours
   - Priority: LOW

8. **Extra Keys in Non-English Files**
   - Impact: Confusion, potential bugs
   - Effort: 2-3 hours
   - Priority: LOW

9. **No Translation Memory/TM System**
   - Impact: Inefficient translation workflow
   - Effort: 8-12 hours (setup)
   - Priority: LOW

---

## 9. RECOMMENDATIONS FOR FULL i18n COVERAGE

### 9.1 Immediate Actions (This Sprint)

**1. Fix Critical Hardcoded Strings Bug (2 hours)**
- Fix `compatibility_screen.dart` mixed language bug
- Add proper localization keys
- Test in all 6 languages

**2. Complete Missing Keys in Existing Languages (20-30 hours)**
- Translate 163 missing keys to German, French, Italian, Portuguese
- Focus on: Analytics, Goal Planner, Empty States, Celebrations
- Use professional translator or AI with human review

**3. Fix Hardcoded Strings in Premium Features (10 hours)**
- Convert hardcoded strings in `premium_screen.dart`
- Fix `ascendant_profile_screen.dart`
- Fix goal planner screens

### 9.2 Short-term (Next 2-4 Weeks)

**4. Fix All Remaining Hardcoded Strings (40-60 hours)**
- Systematic pass through all 64 files
- Add localization keys to ARB files
- Replace hardcoded Text() with AppLocalizations
- Test thoroughly

**5. Add Missing Languages (200-250 hours)**
- Phase 1: Japanese and Chinese (Asian market)
- Phase 2: Arabic with RTL (Middle East)
- Phase 3: Hindi and Russian

**6. Implement Proper RTL Support (20-30 hours)**
- Configure Arabic locale
- Test all screens in RTL mode
- Fix layout issues
- Verify custom widgets

### 9.3 Medium-term (1-3 Months)

**7. Implement Advanced i18n Features (15-25 hours)**
- Add proper plural forms
- Implement gender-specific translations (where needed)
- Add date/time localization
- Add number formatting localization

**8. Quality Assurance (40-60 hours)**
- Native speaker review for all languages
- Cultural adaptation review
- Context verification
- Screenshot testing in all languages

**9. Translation Management System (8-15 hours)**
- Set up translation memory (TM)
- Implement continuous localization workflow
- Add translation review process
- Document translation guidelines

### 9.4 Long-term (3-6 Months)

**10. Advanced Features**
- Regional variants (e.g., es-MX vs es-ES)
- Locale-specific content
- A/B testing for translations
- User-contributed translations

**11. Maintenance**
- Regular translation updates
- Continuous quality monitoring
- Performance optimization for large translation files
- Automated translation suggestions

---

## 10. IMPLEMENTATION PRIORITY MATRIX

| Priority | Task | Impact | Effort | ROI |
|----------|------|--------|--------|-----|
| **P0** | Fix mixed language bug | HIGH | 2h | CRITICAL |
| **P0** | Complete missing 163 keys | HIGH | 25h | HIGH |
| **P0** | Fix premium hardcoded strings | HIGH | 10h | HIGH |
| **P1** | Fix all hardcoded strings | HIGH | 50h | HIGH |
| **P1** | Add Japanese & Chinese | HIGH | 100h | HIGH |
| **P2** | Add Arabic + RTL | MEDIUM | 80h | MEDIUM |
| **P2** | Add Hindi & Russian | MEDIUM | 100h | MEDIUM |
| **P2** | Implement plurals | MEDIUM | 15h | MEDIUM |
| **P3** | Clean up extra keys | LOW | 3h | LOW |
| **P3** | Standardize naming | LOW | 8h | LOW |

---

## 11. COST ESTIMATION

### 11.1 Internal Development Time

| Phase | Hours | @ $75/hr | Total |
|-------|-------|----------|-------|
| **Immediate (P0)** | 37h | $75 | $2,775 |
| **Short-term (P1)** | 370h | $75 | $27,750 |
| **Medium-term (P2)** | 240h | $75 | $18,000 |
| **Long-term (P3)** | 50h | $75 | $3,750 |
| **TOTAL** | 697h | - | **$52,275** |

### 11.2 External Translation Costs

| Language | Words | @ $0.10/word | Total |
|----------|-------|--------------|-------|
| Japanese | ~25,000 | $0.12 | $3,000 |
| Chinese | ~20,000 | $0.12 | $2,400 |
| Arabic | ~25,000 | $0.15 | $3,750 |
| Hindi | ~25,000 | $0.10 | $2,500 |
| Russian | ~25,000 | $0.10 | $2,500 |
| **TOTAL** | ~120,000 | - | **$14,150** |

### 11.3 Total Project Cost

**Development + Translation: $66,425**

**ROI Justification:**
- Opens app to 2+ billion additional users
- Required for app store approval in target markets
- Competitive advantage in Asian and Middle Eastern markets
- Better user retention through native language support

---

## 12. TESTING STRATEGY

### 12.1 Translation Testing

**Unit Tests:**
- Verify all keys exist in all language files
- Check for untranslated strings
- Validate parameterized string syntax

**Integration Tests:**
- Test language switching
- Verify correct translations load
- Check fallback behavior

**Manual Testing:**
- Native speaker review
- Context verification
- Screenshot comparison

### 12.2 RTL Testing

**Layout Tests:**
- All screens render correctly in RTL
- Text alignment is correct
- Icons and images flip appropriately
- Navigation flows right-to-left

**Input Tests:**
- Text fields work with RTL
- Cursor movement is correct
- Selection behavior is proper

### 12.3 Automation

**Recommended tools:**
- Flutter's integration test framework
- Screenshot testing (flutter_driver)
- Automated translation quality checks
- CI/CD integration for l10n validation

---

## 13. CONCLUSION

### 13.1 Current State Assessment

**Strengths:**
✅ Solid foundation with 6 languages implemented
✅ Good translation coverage (91-100%) for existing languages
✅ Excellent automation scripts in place
✅ Proper UTF-8 and special character support
✅ RTL infrastructure partially implemented

**Weaknesses:**
❌ 528+ hardcoded strings prevent full localization
❌ 5 major languages missing (ja, zh, ar, hi, ru)
❌ 163 keys missing from 4 implemented languages
❌ Critical bug: mixed language hardcoding
❌ RTL not configured for Arabic
❌ No plural forms implementation

### 13.2 Path to Full i18n Coverage

**Phase 1: Fix Critical Issues (1-2 weeks)**
- Fix mixed language bug
- Complete missing translations
- Fix premium features hardcoded strings

**Phase 2: Complete Localization (4-6 weeks)**
- Fix all hardcoded strings
- Add Japanese and Chinese
- Implement proper testing

**Phase 3: Advanced Support (8-12 weeks)**
- Add Arabic with RTL
- Add Hindi and Russian
- Implement advanced i18n features

**Phase 4: Quality & Maintenance (Ongoing)**
- Native speaker reviews
- Continuous translation updates
- Performance optimization

### 13.3 Success Criteria

- [ ] Zero hardcoded user-facing strings
- [ ] 100% translation coverage in all 11 languages
- [ ] Full RTL support for Arabic
- [ ] Proper plural forms
- [ ] Native speaker approved
- [ ] Automated translation validation in CI/CD
- [ ] <1% user-reported translation issues

---

## APPENDICES

### A. File Locations

**ARB Files:**
- `/zodiac_app/assets/l10n/app_en.arb` (1,616 keys)
- `/zodiac_app/assets/l10n/app_es.arb` (1,622 keys)
- `/zodiac_app/assets/l10n/app_de.arb` (1,530 keys)
- `/zodiac_app/assets/l10n/app_fr.arb` (1,475 keys)
- `/zodiac_app/assets/l10n/app_it.arb` (1,516 keys)
- `/zodiac_app/assets/l10n/app_pt.arb` (1,480 keys)

**Configuration:**
- `/zodiac_app/l10n.yaml` - Flutter localization config
- `/zodiac_app/lib/main.dart` - Locale configuration

**Scripts:**
- `/scripts/fix_translations_automated.py` - Translation automation
- `/scripts/validate_translations.dart` - Validation tool

**Documentation:**
- `/zodiac_app/assets/l10n/translation_keys_reference.md` - Key reference
- `/docs/traducciones/` - Translation documentation

### B. Key Statistics

- **Total files analyzed:** 500+ Dart files
- **Files with hardcoded strings:** 64 files
- **Translation keys in base:** 1,616 keys
- **Special characters supported:** Full UTF-8
- **ARB file sizes:** 89KB - 107KB per language

### C. Quick Reference Commands

```bash
# Validate translations
dart run scripts/validate_translations.dart --verbose

# Fix translation issues
python3 scripts/fix_translations_automated.py --backup

# Generate localizations
flutter gen-l10n

# Test specific language
flutter run --dart-define=LOCALE=es
```

---

**Report End**

For questions or clarifications, contact the development team.
