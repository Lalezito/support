# 🧪 TESTING GUIDE - Category Translations

## Quick Test Checklist

### Pre-Test Setup
1. ✅ Ensure app is compiled: `flutter clean && flutter pub get`
2. ✅ Build for device: `flutter build ios` or `flutter run`
3. ✅ Have test users with different language preferences

---

## Test Scenarios

### 📱 Test 1: Goal Cards Display Translated Categories

**Steps:**
1. Open the app
2. Navigate to **Cosmic Coach** section
3. View daily goals list
4. Check category labels on each goal card

**Expected Results:**

| Language | Fitness Goal Should Show | Wellness Goal Should Show |
|----------|--------------------------|---------------------------|
| English  | 🏋️ FITNESS              | 🧘 WELLNESS              |
| Spanish  | 🏋️ EJERCICIO            | 🧘 BIENESTAR             |
| Portuguese | 🏋️ EXERCÍCIO          | 🧘 BEM-ESTAR             |
| French   | 🏋️ FORME                | 🧘 BIEN-ÊTRE             |
| German   | 🏋️ FITNESS              | 🧘 WOHLBEFINDEN          |
| Italian  | 🏋️ FITNESS              | 🧘 BENESSERE             |

**Visual Location:**
```
┌──────────────────────────────────────┐
│  🏋️                         [HARD]  │
│  Complete 30-minute workout          │
│  🏋️ EJERCICIO  ← Check this label! │
│                                      │
│  Progress ▓▓▓▓▓░░░░░ 50%            │
└──────────────────────────────────────┘
```

**Pass Criteria:** ✅ Category label matches user's language

---

### 📊 Test 2: Statistics Show Translated Categories

**Steps:**
1. Complete at least 3 goals in different categories
2. Navigate to **Statistics** or **Cosmic Coach Stats**
3. Scroll to **"Your Best Categories"** section
4. Check the category names in the list

**Expected Results:**

| Language | Should Display |
|----------|----------------|
| English  | Your Top Categories<br>💪 FITNESS 5<br>🧘 WELLNESS 3<br>🎨 CREATIVITY 2 |
| Spanish  | Tus Mejores Categorías<br>💪 EJERCICIO 5<br>🧘 BIENESTAR 3<br>🎨 CREATIVIDAD 2 |
| Portuguese | Suas Melhores Categorias<br>💪 EXERCÍCIO 5<br>🧘 BEM-ESTAR 3<br>🎨 CRIATIVIDADE 2 |

**Visual Location:**
```
┌──────────────────────────────────────┐
│  📊 Your Statistics                  │
│  ─────────────────────────────────── │
│  Your Best Categories                │
│                                      │
│  💪 EJERCICIO            5 ← Check! │
│  🧘 BIENESTAR            3 ← Check! │
│  🎨 CREATIVIDAD          2 ← Check! │
└──────────────────────────────────────┘
```

**Pass Criteria:** ✅ All category names are translated and uppercase

---

### 🔄 Test 3: Language Switching (if supported)

**Steps:**
1. Start with English language
2. Note the category labels
3. Switch to Spanish in app settings
4. Force refresh or restart app
5. Check category labels again

**Expected Results:**
- ✅ Labels update from "FITNESS" → "EJERCICIO"
- ✅ Labels update from "WELLNESS" → "BIENESTAR"
- ✅ No crashes or errors
- ✅ Immediate update (no cache issues)

---

### 🌐 Test 4: All Categories Coverage

**Test Matrix:**

| Category | Emoji | EN | ES | PT | FR | DE | IT |
|----------|-------|----|----|----|----|----|----|
| fitness | 🏋️ | FITNESS | EJERCICIO | EXERCÍCIO | FORME | FITNESS | FITNESS |
| wellness | 🧘 | WELLNESS | BIENESTAR | BEM-ESTAR | BIEN-ÊTRE | WOHLBEFINDEN | BENESSERE |
| creativity | 🎨 | CREATIVITY | CREATIVIDAD | CRIATIVIDADE | CRÉATIVITÉ | KREATIVITÄT | CREATIVITÀ |
| productivity | 📊 | PRODUCTIVITY | PRODUCTIVIDAD | PRODUTIVIDADE | PRODUCTIVITÉ | PRODUKTIVITÄT | PRODUTTIVITÀ |
| action | ⚡ | ACTION | ACCIÓN | AÇÃO | ACTION | AKTION | AZIONE |

**How to Test:**
1. Generate goals of each category (use Cosmic Coach)
2. Verify each category label matches the table above
3. Test in at least 2 different languages

**Pass Criteria:** ✅ All 5 categories × 6 languages = 30 correct translations

---

## Automated Verification

### Static Analysis
```bash
cd /path/to/zodiac_app
flutter analyze lib/services/cosmic_coach/category_translations.dart
```
**Expected:** ✅ No issues found

### Code Review Checklist
- [ ] `category_translations.dart` contains all 5 categories
- [ ] Each category has all 6 language translations
- [ ] All translations are uppercase
- [ ] Special characters (É, Ê, Ü, etc.) are properly encoded
- [ ] `expandable_goal_card.dart` imports and uses `CategoryTranslations`
- [ ] `goal_statistics_card.dart` imports and uses `CategoryTranslations`
- [ ] No hardcoded English category names remain in widgets

---

## Regression Testing

### Ensure Nothing Broke:

#### Test 1: Goals Still Generate
- [ ] Daily goals appear
- [ ] Goals have titles
- [ ] Goals have descriptions
- [ ] Goals have categories
- [ ] Goals are completable

#### Test 2: Statistics Still Calculate
- [ ] Streak counter works
- [ ] Success rate calculates
- [ ] Top categories populate
- [ ] Counts are accurate

#### Test 3: UI Still Looks Good
- [ ] Category badges show correct colors
- [ ] Category icons appear
- [ ] Text doesn't overflow
- [ ] Cards are properly formatted
- [ ] No layout issues with longer translations

---

## Edge Cases to Test

### 1. Unknown Category
**Test:** Add a goal with category "unknown_test"
**Expected:** Shows "UNKNOWN TEST" (uppercase fallback)

### 2. Unknown Language
**Test:** Request category with languageCode "xx"
**Expected:** Shows English translation (EN fallback)

### 3. Empty Category
**Test:** Pass empty string as category
**Expected:** Returns empty string or handles gracefully

### 4. Case Variations
**Test:** Pass "FITNESS", "fitness", "FiTnEsS"
**Expected:** All return same translation (case-insensitive)

### 5. Underscores in Category
**Test:** Pass "physical_fitness"
**Expected:** Returns "PHYSICAL FITNESS" (underscores removed)

---

## Performance Testing

### Should Be Fast:
- [ ] Category label lookup < 1ms
- [ ] No noticeable UI lag
- [ ] Statistics page loads quickly
- [ ] Goal cards render smoothly

### Should Not Leak Memory:
- [ ] Create/destroy 100 goal cards
- [ ] Check memory usage remains stable
- [ ] No accumulation over time

---

## Accessibility Testing

### Screen Readers:
- [ ] Category labels are read aloud correctly
- [ ] Special characters (É, Ü, etc.) pronounce correctly
- [ ] Uppercase doesn't cause issues

### Font Scaling:
- [ ] Category labels don't overflow at 200% text size
- [ ] Labels remain readable at all sizes

---

## Bug Report Template

If you find issues, report with:

```markdown
**Bug:** Category label not translating

**Steps to Reproduce:**
1. Set language to [language]
2. Go to Cosmic Coach
3. View [goal type] goal

**Expected:** Category shows "[expected translation]"
**Actual:** Category shows "[actual text]"

**Device:** iPhone 14, iOS 17.0
**App Version:** 1.0.0
**Language:** Spanish (es)

**Screenshot:** [attach image]
```

---

## Success Criteria

### Minimum Requirements:
- ✅ All 5 categories translate in all 6 languages
- ✅ Goal cards show translated labels
- ✅ Statistics show translated labels
- ✅ No crashes or errors
- ✅ No visual regressions

### Ideal Results:
- ✅ Translations are natural and correct
- ✅ No UI overflow issues
- ✅ Fast and responsive
- ✅ Works across all devices
- ✅ Passes all edge case tests

---

## Sign-Off

### Developer Testing:
- [ ] All unit tests pass (if created)
- [ ] Static analysis clean
- [ ] Manual testing on simulator
- [ ] Code review completed

### QA Testing:
- [ ] Tested on physical device
- [ ] All 6 languages verified
- [ ] No regressions found
- [ ] Edge cases handled

### Product Approval:
- [ ] Translations are accurate
- [ ] UX is acceptable
- [ ] Ready for production

---

**Testing completed by:** _______________
**Date:** _______________
**Status:** [ ] PASS [ ] FAIL [ ] NEEDS WORK

**Notes:**
