# Translation System Implementation Checklist
## Zodiac App - Phased Rollout Plan with Time Estimates

**Version:** 1.0
**Date:** October 15, 2025
**Estimated Total Time:** 3-4 weeks (or 1.5 hours for MVP)

---

## Quick Reference

### Phase Priority Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  🔴 CRITICAL (Must Do)        🟡 HIGH (Should Do)                  │
│  ├─ Phase 1: Malformed Keys   ├─ Phase 2: IAP Messages            │
│  └─ Phase 3: Consolidation    └─ Phase 4: Remove Unused           │
│                                                                     │
│  🟢 MEDIUM (Nice to Have)                                          │
│  └─ Phase 5: Hardcoded Strings                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Time Estimates Summary

| Phase | Priority | Estimated Time | Dependencies |
|-------|----------|----------------|--------------|
| Phase 1 | 🔴 CRITICAL | 15 minutes | None |
| Phase 2 | 🟡 HIGH | 30 minutes | Phase 1 |
| Phase 3 | 🔴 CRITICAL | 45 minutes | Phase 1, 2 |
| Phase 4 | 🟢 MEDIUM | 30 minutes | Phase 3 |
| Phase 5 | 🟢 MEDIUM | 1-2 hours | Phase 3 |
| **Testing** | 🔴 CRITICAL | 2-4 hours | All phases |
| **Total (Full)** | - | **5-8 hours** | - |
| **MVP** | - | **1.5 hours** | Phases 1-3 only |

---

## Phase 1: Critical Fixes (Malformed Keys)

### Priority: 🔴 CRITICAL
### Estimated Time: 15 minutes
### Dependencies: None

### Tasks:

#### 1.1 Setup & Backup
- [ ] **Time:** 2 minutes
- [ ] Create migration branch: `git checkout -b feature/translation-migration`
- [ ] Verify Python 3.8+ installed: `python3 --version`
- [ ] Navigate to project: `cd /Users/alejandrocaceres/Desktop/appstore.zodia`
- [ ] Review current state: `ls -la zodiac_app/assets/l10n/`

#### 1.2 Run Automation Script (Dry Run)
- [ ] **Time:** 2 minutes
- [ ] Execute: `python3 scripts/fix_translations_automated.py --dry-run`
- [ ] Review proposed changes in terminal output
- [ ] Verify backup directory will be created
- [ ] Check for any error messages

#### 1.3 Apply Fixes
- [ ] **Time:** 2 minutes
- [ ] Execute: `python3 scripts/fix_translations_automated.py`
- [ ] Verify backup created in `backups/translations_YYYYMMDD_HHMMSS/`
- [ ] Check that all 6 `.arb` files were modified
- [ ] Review git diff: `git diff zodiac_app/assets/l10n/`

#### 1.4 Update Dart Code References
- [ ] **Time:** 5 minutes
- [ ] Find usages: `grep -r "active_activepredictionslength" zodiac_app/lib/`
- [ ] Find usages: `grep -r "pending_pendingpredictionslength" zodiac_app/lib/`
- [ ] Find usages: `grep -r "history_verifiedpredictionslength" zodiac_app/lib/`
- [ ] Replace in VS Code:
  - `active_activepredictionslength` → `active_activePredictionsLength`
  - `pending_pendingpredictionslength` → `pending_pendingPredictionsLength`
  - `history_verifiedpredictionslength` → `history_verifiedPredictionsLength`

#### 1.5 Regenerate & Test
- [ ] **Time:** 4 minutes
- [ ] `cd zodiac_app`
- [ ] `flutter pub get`
- [ ] `flutter gen-l10n`
- [ ] `flutter analyze` (should show no new errors)
- [ ] `flutter test` (basic smoke test)

#### 1.6 Commit
- [ ] **Time:** 1 minute
- [ ] `git add .`
- [ ] `git commit -m "Phase 1: Fix malformed translation keys"`
- [ ] `git push origin feature/translation-migration`

### Success Criteria:
✅ All spacing issues fixed in `.arb` files
✅ Code references updated
✅ `flutter gen-l10n` runs without errors
✅ No new analyzer warnings
✅ Changes committed to git

### Rollback Plan:
```bash
git reset --hard HEAD~1
cp backups/translations_*/app_*.arb zodiac_app/assets/l10n/
```

---

## Phase 2: Add Missing IAP Messages

### Priority: 🟡 HIGH
### Estimated Time: 30 minutes
### Dependencies: Phase 1 completed

### Tasks:

#### 2.1 Verify Missing Keys
- [ ] **Time:** 2 minutes
- [ ] Review list of 8 missing IAP keys in migration guide
- [ ] Check current `app_en.arb` to confirm they're missing
- [ ] Note: Script already added them with placeholders

#### 2.2 Add English Translations
- [ ] **Time:** 5 minutes
- [ ] Open `zodiac_app/assets/l10n/app_en.arb`
- [ ] Verify these keys exist (added by script):
  ```json
  "iap_error_connection": "Unable to connect to the store. Please check your internet connection.",
  "iap_error_cancelled": "Purchase was cancelled.",
  "iap_error_payment_invalid": "Payment method is invalid.",
  "iap_error_payment_not_allowed": "Payment is not allowed on this device.",
  "iap_error_product_not_available": "This product is not available.",
  "iap_error_already_owned": "You already own this product.",
  "iap_error_restoration_failed": "Failed to restore purchases. Please try again.",
  "iap_error_unknown": "An unknown error occurred. Please try again."
  ```

#### 2.3 Translate to Spanish
- [ ] **Time:** 5 minutes
- [ ] Open `zodiac_app/assets/l10n/app_es.arb`
- [ ] Replace `[TRANSLATE]` placeholders with Spanish translations (see migration guide)
- [ ] Double-check spelling and grammar

#### 2.4 Translate to Other Languages
- [ ] **Time:** 15 minutes (3 min per language)
- [ ] German (DE): Translate all 8 keys
- [ ] French (FR): Translate all 8 keys
- [ ] Italian (IT): Translate all 8 keys
- [ ] Portuguese (PT): Translate all 8 keys
- [ ] Use migration guide for reference translations

#### 2.5 Update IAP Error Handling Code
- [ ] **Time:** 3 minutes
- [ ] Locate IAP service file (e.g., `lib/services/revenuecat_service.dart`)
- [ ] Add error message mapping function (see migration guide)
- [ ] Replace generic error messages with localized keys

#### 2.6 Test & Commit
- [ ] **Time:** 5 minutes
- [ ] `flutter gen-l10n`
- [ ] `flutter analyze`
- [ ] Test IAP error scenarios (if possible)
- [ ] `git add .`
- [ ] `git commit -m "Phase 2: Add missing IAP error message keys"`
- [ ] `git push`

### Success Criteria:
✅ All 8 IAP error keys added to all 6 languages
✅ Translations are accurate and natural
✅ IAP error handling code updated
✅ No placeholder text remains
✅ Errors display correctly in all languages

### Rollback Plan:
```bash
git reset --hard HEAD~1
# Or remove only the IAP keys manually
```

---

## Phase 3: Consolidate Duplicates

### Priority: 🔴 CRITICAL
### Estimated Time: 45 minutes
### Dependencies: Phases 1 & 2 completed

### Tasks:

#### 3.1 Review Consolidation Map
- [ ] **Time:** 3 minutes
- [ ] Review duplicate key mappings in migration guide
- [ ] Note feature keys (feature1-15) renaming strategy
- [ ] Understand camelCase standardization approach

#### 3.2 Run Consolidation Script
- [ ] **Time:** 2 minutes
- [ ] The Python script already did this in Phase 1
- [ ] Verify changes: `git diff zodiac_app/assets/l10n/app_en.arb`
- [ ] Check that old keys are removed, new keys exist

#### 3.3 Find Code References
- [ ] **Time:** 5 minutes
- [ ] `grep -r "\.feature[0-9]" zodiac_app/lib/` (find feature keys)
- [ ] `grep -r "update_available" zodiac_app/lib/`
- [ ] `grep -r "coming_soon" zodiac_app/lib/`
- [ ] `grep -r "keyWords" zodiac_app/lib/`
- [ ] Document all findings in notepad

#### 3.4 Update Feature Key References
- [ ] **Time:** 20 minutes
- [ ] Open files with `feature1`-`feature15` references
- [ ] Replace each with descriptive name (use mapping table):
  - `feature1` → `premium_feature_unlimitedHoroscopes`
  - `feature2` → `premium_feature_advancedAI`
  - `feature3` → `premium_feature_extendedTracking`
  - (etc. - see full mapping in migration guide)
- [ ] Use VS Code Find & Replace for efficiency
- [ ] Test premium screen after each batch of changes

#### 3.5 Update Other Duplicate References
- [ ] **Time:** 10 minutes
- [ ] Replace `update_available` → `updateAvailable`
- [ ] Replace `coming_soon` → `comingSoon`
- [ ] Replace `keyWords` → `keywords`
- [ ] Check for any dynamic string construction that might break

#### 3.6 Regenerate & Test
- [ ] **Time:** 5 minutes
- [ ] `flutter gen-l10n`
- [ ] `flutter analyze`
- [ ] `flutter test`
- [ ] Visual check: Launch app and verify Premium screen
- [ ] Check all renamed features display correctly

#### 3.7 Commit
- [ ] **Time:** 2 minutes
- [ ] `git add .`
- [ ] `git commit -m "Phase 3: Consolidate duplicate translation keys"`
- [ ] `git push`

### Success Criteria:
✅ All duplicate keys removed
✅ Feature keys use descriptive names
✅ All code references updated
✅ No broken UI elements
✅ Premium screen displays correctly
✅ Naming convention standardized

### Rollback Plan:
```bash
git reset --hard HEAD~1
# Or keep backup of old keys temporarily
```

---

## Phase 4: Remove Unused Keys

### Priority: 🟢 MEDIUM
### Estimated Time: 30 minutes
### Dependencies: Phase 3 completed

### Tasks:

#### 4.1 Identify Unused Keys
- [ ] **Time:** 10 minutes
- [ ] Run unused key detection script:
  ```bash
  cd zodiac_app
  python3 << 'EOF'
  import json
  import subprocess

  with open('assets/l10n/app_en.arb', 'r') as f:
      data = json.load(f)

  unused = []
  for key in data.keys():
      if key.startswith('@'):
          continue
      result = subprocess.run(['grep', '-r', key, 'lib/'], capture_output=True, text=True)
      if not result.stdout:
          unused.append(key)

  print(f"Potentially unused: {len(unused)}")
  for k in unused[:20]:
      print(f"  - {k}")
  EOF
  ```
- [ ] Save output to file: `unused_keys.txt`

#### 4.2 Manual Verification
- [ ] **Time:** 15 minutes
- [ ] Review each unused key in context
- [ ] Check if used dynamically (string interpolation)
- [ ] Check if planned for future features
- [ ] Check API/backend references
- [ ] Create three categories:
  - ✅ **Safe to remove:** Confirmed unused
  - ⚠️ **Deprecated:** Mark but keep for now
  - ❌ **Keep:** Used or planned

#### 4.3 Mark or Remove Keys
- [ ] **Time:** 5 minutes
- [ ] For "Safe to remove": Delete from all 6 `.arb` files
- [ ] For "Deprecated": Add comment in English file:
  ```json
  "@deprecated_keys": {
    "description": "Keys marked for removal in next major version"
  },
  "oldKeyName": "Old Value",
  "@oldKeyName": {
    "description": "DEPRECATED: Use newKeyName instead"
  }
  ```
- [ ] Document removal plan in separate file

#### 4.4 Test & Commit
- [ ] **Time:** 5 minutes
- [ ] `flutter gen-l10n`
- [ ] `flutter analyze`
- [ ] `flutter test`
- [ ] `git add .`
- [ ] `git commit -m "Phase 4: Remove unused translation keys"`
- [ ] `git push`

### Success Criteria:
✅ Unused keys identified
✅ Safe removals made
✅ Deprecated keys documented
✅ No functionality broken
✅ Code still compiles and runs

### Rollback Plan:
```bash
git reset --hard HEAD~1
# Unused key removal is low-risk, easy to restore
```

---

## Phase 5: Fix Hardcoded Strings

### Priority: 🟢 MEDIUM
### Estimated Time: 1-2 hours
### Dependencies: Phase 3 completed

### Tasks:

#### 5.1 Find Hardcoded Strings
- [ ] **Time:** 15 minutes
- [ ] Find hardcoded Text widgets:
  ```bash
  grep -r "Text('" zodiac_app/lib/ | grep -v "AppLocalizations" > hardcoded.txt
  grep -r 'Text("' zodiac_app/lib/ | grep -v "AppLocalizations" >> hardcoded.txt
  ```
- [ ] Find hardcoded SnackBar messages
- [ ] Find hardcoded AlertDialog content
- [ ] Find hardcoded error messages
- [ ] Prioritize user-facing strings

#### 5.2 Create New Translation Keys
- [ ] **Time:** 20 minutes
- [ ] For each hardcoded string, create appropriate key
- [ ] Add to `app_en.arb` with descriptive key name
- [ ] Group by category (errors, dialogs, labels, etc.)
- [ ] Follow naming convention: camelCase

#### 5.3 Update Code - Text Widgets
- [ ] **Time:** 20 minutes
- [ ] Replace hardcoded Text widgets:
  ```dart
  // Before
  Text('Loading...')

  // After
  Text(AppLocalizations.of(context).loading)
  ```
- [ ] Work through one file at a time
- [ ] Test after each file

#### 5.4 Update Code - SnackBars & Dialogs
- [ ] **Time:** 15 minutes
- [ ] Replace hardcoded SnackBar messages
- [ ] Replace hardcoded AlertDialog content
- [ ] Replace hardcoded error messages
- [ ] Add translation keys as needed

#### 5.5 Translate New Keys
- [ ] **Time:** 20 minutes
- [ ] Translate all new keys to Spanish (ES)
- [ ] Translate to German (DE)
- [ ] Translate to French (FR)
- [ ] Translate to Italian (IT)
- [ ] Translate to Portuguese (PT)

#### 5.6 Test All Languages
- [ ] **Time:** 15 minutes
- [ ] Launch app in English
- [ ] Switch to each language and verify
- [ ] Check for UI overflow/truncation
- [ ] Verify all screens load correctly

#### 5.7 Commit
- [ ] **Time:** 2 minutes
- [ ] `git add .`
- [ ] `git commit -m "Phase 5: Replace hardcoded strings with translations"`
- [ ] `git push`

### Success Criteria:
✅ All user-facing hardcoded strings replaced
✅ New translation keys added to all languages
✅ App works correctly in all 6 languages
✅ No English-only UI elements in production

### Rollback Plan:
```bash
git reset --hard HEAD~1
# This phase is incremental, can rollback specific commits
```

---

## Testing & Validation Phase

### Priority: 🔴 CRITICAL
### Estimated Time: 2-4 hours
### Dependencies: All phases completed

### Tasks:

#### T.1 Automated Validation
- [ ] **Time:** 10 minutes
- [ ] Run Dart validation script:
  ```bash
  dart run scripts/validate_translations.dart --verbose
  ```
- [ ] Review output for errors/warnings
- [ ] Run with strict mode:
  ```bash
  dart run scripts/validate_translations.dart --strict
  ```
- [ ] Fix any issues found

#### T.2 Analyzer & Tests
- [ ] **Time:** 15 minutes
- [ ] `flutter analyze` (must pass with 0 errors)
- [ ] `flutter test` (all tests must pass)
- [ ] `flutter test integration_test/` (if exists)
- [ ] Review coverage report

#### T.3 Language Switching Test
- [ ] **Time:** 30 minutes
- [ ] Test each language:
  - [ ] English (EN)
  - [ ] Spanish (ES)
  - [ ] German (DE)
  - [ ] French (FR)
  - [ ] Italian (IT)
  - [ ] Portuguese (PT)
- [ ] For each language:
  - [ ] Home screen displays correctly
  - [ ] Premium screen shows features
  - [ ] Settings screen is translated
  - [ ] Error messages appear in correct language

#### T.4 Feature Testing
- [ ] **Time:** 45 minutes
- [ ] Test Premium flows:
  - [ ] Premium screen displays all features with new names
  - [ ] IAP error messages work (simulate errors if possible)
  - [ ] Purchase flow text is translated
- [ ] Test Horoscope screens:
  - [ ] Daily, Weekly, Monthly tabs
  - [ ] Horoscope content loads
  - [ ] All labels translated
- [ ] Test Settings:
  - [ ] All options translated
  - [ ] Language switching works
  - [ ] Preferences save correctly

#### T.5 UI/UX Testing
- [ ] **Time:** 30 minutes
- [ ] Check for text overflow in all languages
- [ ] Verify button text fits on all screen sizes
- [ ] Test on different devices (iOS & Android)
- [ ] Check dark mode translations
- [ ] Verify accessibility (screen reader)

#### T.6 Edge Cases
- [ ] **Time:** 20 minutes
- [ ] Test very long translations (German typically longest)
- [ ] Test special characters (accents, umlauts)
- [ ] Test plural forms (if implemented)
- [ ] Test date/time formatting
- [ ] Test currency formatting (if applicable)

#### T.7 Performance Testing
- [ ] **Time:** 15 minutes
- [ ] Build profile version: `flutter build apk --profile`
- [ ] Run and profile: `flutter run --profile`
- [ ] Check language switching performance (should be < 100ms)
- [ ] Monitor memory usage
- [ ] Check for translation loading lag

#### T.8 Build Testing
- [ ] **Time:** 30 minutes
- [ ] Build Android release: `flutter build apk --release`
- [ ] Build iOS release: `flutter build ios --release`
- [ ] Install and test on real devices
- [ ] Verify app size didn't increase significantly
- [ ] Test app startup time

### Success Criteria:
✅ All automated tests pass
✅ 0 analyzer errors
✅ All 6 languages work correctly
✅ No UI overflow or truncation
✅ IAP errors display properly
✅ Performance is acceptable
✅ Production builds work

---

## Final Deployment Checklist

### Priority: 🔴 CRITICAL
### Estimated Time: 1-2 hours
### Dependencies: All testing passed

### Tasks:

#### D.1 Documentation
- [ ] **Time:** 15 minutes
- [ ] Update README with new key naming conventions
- [ ] Document new IAP error keys
- [ ] Update CHANGELOG.md
- [ ] Create release notes

#### D.2 Code Review
- [ ] **Time:** 30 minutes
- [ ] Create pull request
- [ ] Request code review from team
- [ ] Address review comments
- [ ] Get approval

#### D.3 Pre-Release Checks
- [ ] **Time:** 15 minutes
- [ ] Verify version number updated
- [ ] Check all `.arb` files committed
- [ ] Ensure no debug code left
- [ ] Verify backups exist

#### D.4 Merge & Deploy
- [ ] **Time:** 10 minutes
- [ ] Merge to main/master branch
- [ ] Tag release: `git tag v1.x.x`
- [ ] Push tags: `git push --tags`
- [ ] Trigger CI/CD pipeline (if configured)

#### D.5 Monitor
- [ ] **Time:** Ongoing
- [ ] Monitor crash reports (Firebase Crashlytics)
- [ ] Check analytics for errors
- [ ] Monitor user feedback
- [ ] Prepare hotfix plan if needed

### Success Criteria:
✅ Code reviewed and approved
✅ Documentation updated
✅ Version tagged and deployed
✅ Monitoring in place
✅ Rollback plan ready

---

## MVP (Minimum Viable Product) Checklist

If you need to launch quickly, do only these tasks:

### MVP Phase 1: Critical Fixes (15 min)
- [x] Run automation script
- [x] Fix malformed keys
- [x] Update code references
- [x] Regenerate localization
- [x] Commit

### MVP Phase 2: IAP Messages (30 min)
- [x] Add IAP error keys (English only acceptable for MVP)
- [x] Update IAP error handling code
- [x] Test purchase error flows
- [x] Commit

### MVP Phase 3: Consolidate (45 min)
- [x] Rename feature keys to descriptive names
- [x] Update premium screen code
- [x] Remove obvious duplicates
- [x] Test premium features
- [x] Commit

### MVP Testing (30 min)
- [x] `flutter analyze` passes
- [x] `flutter test` passes
- [x] Premium screen works
- [x] IAP errors display

**MVP Total Time:** ~2 hours
**MVP Can Ship:** ✅ Yes, but plan to complete Phases 4-5 in next sprint

---

## Progress Tracking

### Phase Completion Status

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Phase 1: Critical Fixes          [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Testing           │
│                                    [ ] Completed         │
│                                                          │
│  Phase 2: IAP Messages             [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Testing           │
│                                    [ ] Completed         │
│                                                          │
│  Phase 3: Consolidation            [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Testing           │
│                                    [ ] Completed         │
│                                                          │
│  Phase 4: Remove Unused            [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Testing           │
│                                    [ ] Completed         │
│                                                          │
│  Phase 5: Hardcoded Strings        [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Testing           │
│                                    [ ] Completed         │
│                                                          │
│  Testing & Validation              [ ] Not Started       │
│                                    [ ] In Progress       │
│                                    [ ] Completed         │
│                                                          │
│  Deployment                        [ ] Not Started       │
│                                    [ ] Completed         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Completion Percentage

```
Overall Progress: [░░░░░░░░░░░░░░░░░░░░] 0%

Phase 1:  [░░░░░░░░░░░░░░░░░░░░] 0%
Phase 2:  [░░░░░░░░░░░░░░░░░░░░] 0%
Phase 3:  [░░░░░░░░░░░░░░░░░░░░] 0%
Phase 4:  [░░░░░░░░░░░░░░░░░░░░] 0%
Phase 5:  [░░░░░░░░░░░░░░░░░░░░] 0%
Testing:  [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## Time Tracking

### Estimated vs Actual

| Phase | Estimated | Actual | Variance | Notes |
|-------|-----------|--------|----------|-------|
| Phase 1 | 15 min | ___ min | ___ | |
| Phase 2 | 30 min | ___ min | ___ | |
| Phase 3 | 45 min | ___ min | ___ | |
| Phase 4 | 30 min | ___ min | ___ | |
| Phase 5 | 1-2 hrs | ___ hrs | ___ | |
| Testing | 2-4 hrs | ___ hrs | ___ | |
| **Total** | **5-8 hrs** | **___ hrs** | **___** | |

---

## Risk Assessment

### High Risk Items:
⚠️ **Breaking code references during consolidation**
- Mitigation: Thorough grep search, test frequently
- Rollback: Git revert to previous commit

⚠️ **Missing dynamically constructed keys**
- Mitigation: Manual code review, search for string interpolation
- Rollback: Keep old keys as aliases temporarily

⚠️ **Translation quality issues**
- Mitigation: Native speaker review (or professional translation)
- Rollback: Accept placeholders, fix in next release

### Medium Risk Items:
⚠️ **UI overflow with longer translations**
- Mitigation: Test all languages, use flexible layouts
- Fix: Adjust UI constraints as needed

⚠️ **Performance impact**
- Mitigation: Profile before/after, monitor metrics
- Fix: Optimize localization loading if needed

### Low Risk Items:
✅ Malformed key fixes (low impact, easy to test)
✅ Adding new keys (won't break existing code)
✅ Removing truly unused keys (no references)

---

## Support & Escalation

### If You Get Stuck:

1. **Check documentation:**
   - Migration guide: `scripts/TRANSLATION_MIGRATION_GUIDE.md`
   - Analysis report: `TRANSLATION_KEYS_ANALYSIS_REPORT.md`

2. **Run diagnostics:**
   ```bash
   dart run scripts/validate_translations.dart --verbose
   flutter analyze
   flutter doctor
   ```

3. **Review backup:**
   ```bash
   ls -la backups/translations_*/
   ```

4. **Rollback if needed:**
   ```bash
   git reset --hard HEAD~1
   # Or restore from backup
   ```

5. **Ask for help:**
   - Create GitHub issue with error details
   - Include phase number and task
   - Attach relevant logs/screenshots

---

## Post-Migration Review

After completing all phases, schedule a review meeting to:

- [ ] Review completion times vs estimates
- [ ] Discuss challenges encountered
- [ ] Document lessons learned
- [ ] Plan improvements for next migration
- [ ] Update this checklist based on experience

---

**Checklist Version:** 1.0
**Last Updated:** October 15, 2025
**Next Review:** After migration completion

---

**Ready to begin? Start with Phase 1, Task 1.1** ✅
