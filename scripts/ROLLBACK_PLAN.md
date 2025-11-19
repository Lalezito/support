# Translation Migration Rollback Plan
## Emergency Recovery Procedures

**Version:** 1.0
**Date:** October 15, 2025
**Classification:** CRITICAL DOCUMENTATION

---

## Quick Reference

### Emergency Contacts & Resources

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🚨 EMERGENCY ROLLBACK COMMANDS                                │
│                                                                 │
│  Quick Rollback (Last Commit):                                 │
│  $ git reset --hard HEAD~1                                     │
│                                                                 │
│  Restore from Backup:                                          │
│  $ cp backups/translations_*/app_*.arb zodiac_app/assets/l10n/ │
│  $ cd zodiac_app && flutter gen-l10n                           │
│                                                                 │
│  Rollback Multiple Commits:                                    │
│  $ git reset --hard <commit-hash>                              │
│                                                                 │
│  Emergency Hotfix Branch:                                      │
│  $ git checkout -b hotfix/translation-emergency                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

1. [When to Rollback](#when-to-rollback)
2. [Rollback Decision Matrix](#rollback-decision-matrix)
3. [Phase-Specific Rollbacks](#phase-specific-rollbacks)
4. [Full System Rollback](#full-system-rollback)
5. [Partial Rollback Procedures](#partial-rollback-procedures)
6. [Emergency Hotfix Process](#emergency-hotfix-process)
7. [Data Recovery](#data-recovery)
8. [Testing After Rollback](#testing-after-rollback)
9. [Communication Plan](#communication-plan)
10. [Prevention Checklist](#prevention-checklist)

---

## When to Rollback

### Immediate Rollback Required 🔴

Roll back IMMEDIATELY if:

✗ **Critical Production Issues:**
- App crashes on launch
- Key features completely broken (premium, purchases)
- User data loss or corruption
- Security vulnerabilities exposed
- App Store rejection due to translation issues

✗ **Build Failures:**
- `flutter build` fails completely
- Cannot generate production builds
- Signing/certificate errors related to changes

✗ **Widespread Translation Failures:**
- Entire language files corrupted
- 50%+ of UI shows broken/missing translations
- Payment/legal text showing wrong language

### Rollback Recommended 🟡

Consider rolling back if:

⚠️ **Significant Issues:**
- 10-20% of translations incorrect/missing
- Multiple screens have UI overflow/truncation
- IAP error messages not working correctly
- Performance degradation (>30% slower)

⚠️ **Multiple Test Failures:**
- >30% of unit tests failing
- Critical integration tests broken
- Flutter analyze shows >10 new errors

⚠️ **User-Facing Problems:**
- Premium features not displaying correctly
- Confusing/incorrect error messages
- Language switching broken

### Monitor & Fix (No Rollback) 🟢

No rollback needed if:

✓ **Minor Issues:**
- <5% of translations need correction
- Cosmetic UI issues only
- Minor typos or grammar errors
- Non-critical features affected

✓ **Can be Fixed Forward:**
- Quick fix possible (<30 minutes)
- Only affects one language
- Only affects non-critical screens

---

## Rollback Decision Matrix

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  Severity   │  Scope      │  Time to Fix  │  Action              │
│  ──────────────────────────────────────────────────────────────── │
│  CRITICAL   │  Widespread │  Unknown      │  🔴 ROLLBACK NOW     │
│  CRITICAL   │  Isolated   │  <30 min      │  🟡 Fix Forward      │
│  CRITICAL   │  Isolated   │  >30 min      │  🔴 ROLLBACK NOW     │
│  HIGH       │  Widespread │  >1 hour      │  🔴 ROLLBACK NOW     │
│  HIGH       │  Isolated   │  <1 hour      │  🟡 Fix Forward      │
│  MEDIUM     │  Any        │  <2 hours     │  🟢 Fix Forward      │
│  LOW        │  Any        │  Any          │  🟢 Fix Forward      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Decision Tree

```
Is production affected?
    ├─ YES → Is app unusable?
    │         ├─ YES → 🔴 ROLLBACK IMMEDIATELY
    │         └─ NO → Can fix in <30 min?
    │                  ├─ YES → 🟡 Fix Forward
    │                  └─ NO → 🔴 ROLLBACK
    │
    └─ NO → Is development blocked?
              ├─ YES → Is it just one phase?
              │         ├─ YES → 🟡 Rollback that phase
              │         └─ NO → 🔴 Full rollback
              │
              └─ NO → 🟢 Continue, fix issues
```

---

## Phase-Specific Rollbacks

### Phase 1: Malformed Keys Rollback

**If Phase 1 causes issues:**

#### Quick Rollback (15 minutes):

```bash
# 1. Rollback git commit
cd /Users/alejandrocaceres/Desktop/appstore.zodia
git reset --hard HEAD~1

# 2. Restore from backup
cp backups/translations_*/app_*.arb zodiac_app/assets/l10n/

# 3. Revert Dart code changes
git checkout HEAD -- zodiac_app/lib/

# 4. Regenerate
cd zodiac_app
flutter clean
flutter pub get
flutter gen-l10n

# 5. Test
flutter analyze
flutter test

# 6. Rebuild
flutter build apk --debug
```

#### Verification:

- [ ] Old malformed keys restored (e.g., `active_activepredictionslength`)
- [ ] Dart code uses old keys again
- [ ] App builds without errors
- [ ] Predictions screen works

#### Alternative: Keep Changes, Fix Issues

If only small issues:

```bash
# Just fix the problematic keys manually
nano zodiac_app/assets/l10n/app_en.arb
# Revert specific keys to old names

flutter gen-l10n
```

---

### Phase 2: IAP Messages Rollback

**If Phase 2 causes issues:**

#### Quick Rollback (10 minutes):

```bash
# 1. Rollback git commit
git reset --hard HEAD~1

# 2. Or manually remove IAP keys
cd zodiac_app/assets/l10n

# Edit each .arb file and remove:
# - iap_error_connection
# - iap_error_cancelled
# - iap_error_payment_invalid
# - iap_error_payment_not_allowed
# - iap_error_product_not_available
# - iap_error_already_owned
# - iap_error_restoration_failed
# - iap_error_unknown

# 3. Revert IAP code changes
git checkout HEAD -- zodiac_app/lib/services/*revenuecat*

# 4. Regenerate
cd zodiac_app
flutter gen-l10n
flutter analyze
```

#### Verification:

- [ ] IAP error handling reverted to old generic messages
- [ ] Purchase flows still work
- [ ] No compilation errors
- [ ] Premium screen functional

#### Impact Assessment:

**Risk Level:** LOW
- IAP keys are additive (don't break existing functionality)
- Easy to remove without side effects
- Can re-add later after fixing issues

---

### Phase 3: Consolidation Rollback

**If Phase 3 causes issues:**

#### Quick Rollback (20 minutes):

```bash
# 1. This is the most complex rollback
git reset --hard HEAD~1

# 2. If partial rollback needed, restore backup
cp backups/translations_*/app_en.arb zodiac_app/assets/l10n/

# 3. Check what changed
git diff HEAD~1 HEAD -- zodiac_app/lib/

# 4. If needed, manually revert specific files
git checkout HEAD~1 -- zodiac_app/lib/screens/premium_screen.dart
git checkout HEAD~1 -- zodiac_app/lib/widgets/premium_feature_card.dart

# 5. Regenerate
cd zodiac_app
flutter clean
flutter pub get
flutter gen-l10n

# 6. Extensive testing
flutter test
flutter build apk --debug
```

#### Verification:

- [ ] Old feature keys restored (feature1-feature15)
- [ ] Duplicate keys back (update_available, coming_soon, etc.)
- [ ] All screens render correctly
- [ ] Premium features display with old keys
- [ ] No missing translations

#### Alternative: Partial Revert

Keep some consolidations, revert only problematic ones:

```bash
# Example: Keep feature renames, revert other duplicates
# Manually edit .arb files to restore:
# - update_available (alongside updateAvailable)
# - coming_soon (alongside comingSoon)
# Then gradually remove old versions
```

**Risk Level:** HIGH
- Many code changes across multiple files
- Complex dependencies
- High chance of missing references
- Recommend full testing after rollback

---

### Phase 4: Unused Keys Rollback

**If Phase 4 causes issues:**

#### Quick Rollback (5 minutes):

```bash
# 1. This is the EASIEST rollback
git reset --hard HEAD~1

# 2. Or restore removed keys from backup
cp backups/translations_*/app_*.arb zodiac_app/assets/l10n/

# 3. Regenerate
cd zodiac_app
flutter gen-l10n
```

#### Verification:

- [ ] Removed keys restored
- [ ] No compilation errors
- [ ] All features work

**Risk Level:** VERY LOW
- Removing unused keys shouldn't break anything
- Easy to restore
- Minimal impact on codebase

---

### Phase 5: Hardcoded Strings Rollback

**If Phase 5 causes issues:**

#### Quick Rollback (15 minutes):

```bash
# 1. Rollback commits (might be multiple)
git log --oneline  # Find the last commit before Phase 5
git reset --hard <commit-hash>

# 2. Or revert specific files
git checkout HEAD~1 -- zodiac_app/lib/screens/
git checkout HEAD~1 -- zodiac_app/lib/widgets/

# 3. Remove added translation keys (optional)
# Edit .arb files and remove newly added keys for hardcoded strings

# 4. Regenerate
cd zodiac_app
flutter gen-l10n
flutter analyze
```

#### Verification:

- [ ] Hardcoded strings back in place
- [ ] App displays correctly (even if not localized)
- [ ] No runtime errors
- [ ] All languages work

**Risk Level:** MEDIUM
- Changes spread across many files
- Easy to miss some changes
- But hardcoded strings still work (just not localized)
- Can rollback incrementally

---

## Full System Rollback

### When ALL phases need rollback:

#### Nuclear Option (30 minutes):

```bash
# 1. Find pre-migration commit
cd /Users/alejandrocaceres/Desktop/appstore.zodia
git log --oneline | grep "Pre-migration checkpoint"
# Note the commit hash

# 2. Reset to that commit
git reset --hard <pre-migration-commit-hash>

# 3. Force clean
cd zodiac_app
flutter clean
rm -rf .dart_tool
rm -rf build

# 4. Reinstall dependencies
flutter pub get

# 5. Regenerate localization
flutter gen-l10n

# 6. Full test suite
flutter analyze
flutter test
flutter test integration_test/

# 7. Rebuild everything
flutter build apk --debug
flutter build ios --debug

# 8. Test on devices
flutter run
```

#### Verification Checklist:

- [ ] Git history shows rollback to pre-migration state
- [ ] All .arb files match pre-migration state
- [ ] All Dart code reverted
- [ ] Flutter analyze: 0 errors
- [ ] All tests pass
- [ ] Builds succeed for both platforms
- [ ] App runs on real devices
- [ ] All features functional

#### Post-Rollback:

```bash
# 1. Document what went wrong
echo "Rollback Reason: [describe issue]" > ROLLBACK_NOTES.txt
echo "Date: $(date)" >> ROLLBACK_NOTES.txt
echo "Failed Phase: [phase number]" >> ROLLBACK_NOTES.txt

# 2. Create issue for investigation
# Create GitHub issue with rollback details

# 3. Clean up branches
git branch -D feature/translation-migration
git push origin --delete feature/translation-migration

# 4. Optionally keep backup branch
git checkout -b backup/translation-migration-failed
git push origin backup/translation-migration-failed
```

---

## Partial Rollback Procedures

### Rollback Single File:

```bash
# Rollback specific .arb file
git checkout HEAD~1 -- zodiac_app/assets/l10n/app_es.arb

# Rollback specific Dart file
git checkout HEAD~1 -- zodiac_app/lib/screens/premium_screen.dart

# Regenerate
cd zodiac_app
flutter gen-l10n
```

### Rollback Single Key:

```bash
# 1. Open .arb file
nano zodiac_app/assets/l10n/app_en.arb

# 2. Manually change key back:
# From: "premium_feature_unlimitedHoroscopes": "..."
# To:   "feature1": "..."

# 3. Update code reference:
# From: AppLocalizations.of(context).premium_feature_unlimitedHoroscopes
# To:   AppLocalizations.of(context).feature1

# 4. Regenerate
flutter gen-l10n
```

### Rollback Single Language:

```bash
# If only one language is broken, restore just that one:
cp backups/translations_*/app_de.arb zodiac_app/assets/l10n/

# Regenerate
cd zodiac_app
flutter gen-l10n
```

---

## Emergency Hotfix Process

### Production is Down Scenario:

#### Immediate Actions (5 minutes):

```bash
# 1. Create emergency hotfix branch
cd /Users/alejandrocaceres/Desktop/appstore.zodia
git checkout main
git pull origin main
git checkout -b hotfix/translation-emergency

# 2. Identify problematic commit
git log --oneline

# 3. Revert specific commit
git revert <bad-commit-hash>

# 4. Or restore from backup
cp backups/translations_LATEST/*.arb zodiac_app/assets/l10n/

# 5. Quick test
cd zodiac_app
flutter gen-l10n
flutter analyze
flutter build apk --release

# 6. Deploy immediately
git add .
git commit -m "HOTFIX: Revert translation migration due to production issue"
git push origin hotfix/translation-emergency

# 7. Create emergency PR
gh pr create --title "HOTFIX: Translation Rollback" --body "Emergency rollback due to production issue" --base main
```

#### Communication:

```
Subject: [URGENT] Translation Migration Rolled Back

Status: Production issue detected and fixed
Action: Rolled back translation migration
Impact: [describe user impact]
Resolution: [describe fix applied]
ETA: Live in [X] minutes
Next Steps: Investigation and root cause analysis

Details:
- Issue: [specific problem]
- Affected: [features/languages]
- Fix: [what was done]
- Tested: [verification performed]
```

---

## Data Recovery

### Recovering Lost Translation Data:

#### From Git History:

```bash
# Find when key existed
git log --all --full-history -- "**/app_en.arb" | grep -A 5 "yourKeyName"

# Show file at specific commit
git show <commit-hash>:zodiac_app/assets/l10n/app_en.arb > recovered_en.arb

# Extract specific key
grep "yourKeyName" recovered_en.arb
```

#### From Backups:

```bash
# List all backups
ls -la backups/

# Find specific backup
ls -la backups/translations_*/

# Compare backup with current
diff backups/translations_LATEST/app_en.arb zodiac_app/assets/l10n/app_en.arb

# Extract specific keys
grep "feature1" backups/translations_LATEST/app_en.arb
```

#### From Flutter Generated Files:

```bash
# Generated localization files might still have old data
cat zodiac_app/lib/l10n/app_localizations_en.dart | grep "feature1"

# Copy translations from there if needed
```

### Recovering Lost Code Changes:

```bash
# Find deleted/modified code
git log --diff-filter=D --summary | grep "premium_screen.dart"

# Recover deleted file
git checkout <commit-hash>~1 -- zodiac_app/lib/screens/premium_screen.dart

# Show what was changed
git show <commit-hash> -- zodiac_app/lib/screens/premium_screen.dart
```

---

## Testing After Rollback

### Critical Tests (15 minutes):

```bash
# 1. Clean build
cd zodiac_app
flutter clean
flutter pub get

# 2. Analyze
flutter analyze
# MUST show 0 errors

# 3. Unit tests
flutter test
# MUST all pass

# 4. Build
flutter build apk --debug
flutter build ios --debug
# MUST succeed

# 5. Run on device
flutter run
# MUST launch without errors
```

### Functional Tests (30 minutes):

- [ ] **Home Screen:**
  - Loads without errors
  - All translations display
  - Navigation works

- [ ] **Premium Screen:**
  - Feature list displays
  - Purchase buttons work
  - Feature descriptions show correctly

- [ ] **Settings:**
  - Language switching works
  - All options display
  - Preferences save

- [ ] **IAP Flows:**
  - Purchase attempt works
  - Error messages display
  - Restore purchases works

- [ ] **Language Test:**
  - Test all 6 languages
  - Verify no blank screens
  - Check for overflow

### Regression Tests (45 minutes):

```bash
# Run full test suite
flutter test --coverage

# Integration tests
flutter test integration_test/

# Build production
flutter build apk --release
flutter build ios --release

# Performance check
flutter run --profile
# Monitor memory and performance
```

---

## Communication Plan

### Internal Team Communication:

#### Rollback Decision Made:

```
To: Development Team
Subject: Translation Migration Rollback in Progress

The translation migration is being rolled back due to [issue].

Status: In progress
Expected completion: [time]
Impact: [describe]
Action required: [if any]

Will update when complete.
```

#### Rollback Complete:

```
To: Development Team
Subject: Translation Migration Rollback Complete

Rollback completed successfully.

What was rolled back: [phases]
Current state: [describe]
Next steps: [plan]

All systems verified working. Development can continue.
```

### External Communication (if production affected):

#### User Notification:

```
We've detected an issue with our latest update and have temporarily
reverted some changes. Your app may update automatically. We're working
on a permanent fix. Thank you for your patience.

- Zodiac App Team
```

#### App Store Update Notes:

```
v1.x.x (Emergency Update)

This update fixes critical issues from the previous release:
- Restored proper translations in all languages
- Fixed premium feature display issues
- Resolved purchase error message problems

We apologize for any inconvenience. Future updates will include
the improvements we attempted, properly tested.
```

---

## Prevention Checklist

### Before Starting Migration:

- [ ] Create detailed backup plan (you have this! ✓)
- [ ] Ensure git is clean and committed
- [ ] Create migration branch
- [ ] Document current state
- [ ] Test backup restoration procedure
- [ ] Identify rollback contacts/approvers

### During Migration:

- [ ] Commit after each phase
- [ ] Test thoroughly before next phase
- [ ] Keep detailed notes
- [ ] Monitor for errors continuously
- [ ] Don't skip verification steps

### Before Deploying:

- [ ] Complete all testing checklists
- [ ] Get code review approval
- [ ] Test on real devices (iOS & Android)
- [ ] Verify backups are accessible
- [ ] Have rollback plan ready
- [ ] Plan deployment during low-traffic hours

### After Deploying:

- [ ] Monitor crash reports closely
- [ ] Check analytics for errors
- [ ] Have team on standby
- [ ] Keep rollback window open (2-4 hours)
- [ ] Document any issues immediately

---

## Rollback Success Criteria

Rollback is successful when:

✅ **Build Success:**
- `flutter analyze` shows 0 errors
- `flutter build` succeeds for both platforms
- All tests pass

✅ **Functional:**
- App launches without crashes
- All screens load correctly
- Core features work (horoscope, premium, purchases)
- Language switching works

✅ **Data Integrity:**
- User preferences preserved
- Purchase history intact
- No data corruption

✅ **Performance:**
- App performance matches pre-migration baseline
- No memory leaks
- Startup time acceptable

✅ **User Experience:**
- No broken UI elements
- Translations display correctly (even if not all localized)
- Error messages work

---

## Post-Rollback Analysis

### Required Actions:

1. **Document Root Cause:**
   - What went wrong?
   - Why wasn't it caught in testing?
   - What was the trigger?

2. **Update Procedures:**
   - What should be added to testing?
   - What warning signs were missed?
   - How can this be prevented?

3. **Plan Retry:**
   - Fix identified issues
   - Add additional safety checks
   - Schedule new migration attempt

### Lessons Learned Template:

```markdown
# Translation Migration Rollback - Post-Mortem

## Date: [date]
## Phase Failed: [phase]

### What Happened:
[Describe the issue that caused rollback]

### Root Cause:
[Technical explanation]

### Impact:
- Users affected: [number/percentage]
- Downtime: [duration]
- Features impacted: [list]

### What Went Well:
- [Things that worked]

### What Didn't Go Well:
- [Problems encountered]

### Action Items:
1. [Action 1] - Owner: [name] - Due: [date]
2. [Action 2] - Owner: [name] - Due: [date]

### Prevention:
[Steps to prevent similar issues]

### Next Attempt:
[Plan for retry, if applicable]
```

---

## Emergency Contacts

### Rollback Authority:

| Role | Name | Decision Level |
|------|------|----------------|
| Tech Lead | [Name] | Can approve any rollback |
| Product Manager | [Name] | Must approve production rollback |
| DevOps | [Name] | Executes deployment rollback |
| QA Lead | [Name] | Verifies rollback success |

### Escalation Path:

```
Issue Detected
    ↓
Developer assesses severity
    ↓
If CRITICAL → Notify Tech Lead immediately
    ↓
Tech Lead approves rollback
    ↓
Execute rollback procedures
    ↓
Verify success
    ↓
Notify Product Manager
    ↓
Post-mortem analysis
```

---

## Quick Reference Commands

### Most Common Rollback Commands:

```bash
# Rollback last commit
git reset --hard HEAD~1

# Restore from backup
cp backups/translations_LATEST/*.arb zodiac_app/assets/l10n/

# Regenerate localization
cd zodiac_app && flutter gen-l10n

# Test
flutter analyze && flutter test

# Build
flutter build apk --debug
```

### Emergency Aliases (add to ~/.bashrc or ~/.zshrc):

```bash
alias trans-rollback='git reset --hard HEAD~1 && cd zodiac_app && flutter gen-l10n && flutter analyze'
alias trans-restore='cp backups/translations_LATEST/*.arb zodiac_app/assets/l10n/ && cd zodiac_app && flutter gen-l10n'
alias trans-test='cd zodiac_app && flutter analyze && flutter test && flutter build apk --debug'
```

---

## Checklist Summary

### Rollback Complete When:

- [ ] Git reverted to stable state
- [ ] Translation files restored
- [ ] Code references fixed
- [ ] Flutter analyze: 0 errors
- [ ] All tests pass
- [ ] Builds succeed
- [ ] App tested on devices
- [ ] Team notified
- [ ] Post-mortem scheduled
- [ ] Lessons documented

---

**Rollback Plan Version:** 1.0
**Last Updated:** October 15, 2025
**Next Review:** After any rollback event

---

**Remember:** It's always better to rollback quickly than to spend hours debugging in production. When in doubt, roll back first, fix later.

**This document should be readily accessible during migration. Print or bookmark it.**

---

## Appendix A: Common Rollback Scenarios

### Scenario 1: "flutter gen-l10n fails"

```bash
# Quick fix:
flutter clean
rm -rf .dart_tool
flutter pub get
flutter gen-l10n

# If still fails:
git checkout HEAD~1 -- zodiac_app/assets/l10n/
flutter gen-l10n
```

### Scenario 2: "App crashes on launch"

```bash
# Immediate rollback:
git reset --hard HEAD~1
cd zodiac_app
flutter clean
flutter pub get
flutter gen-l10n
flutter run

# Test on device immediately
```

### Scenario 3: "Premium screen broken"

```bash
# Rollback just premium-related changes:
git checkout HEAD~1 -- zodiac_app/lib/screens/premium_screen.dart
git checkout HEAD~1 -- zodiac_app/lib/widgets/premium_*
git checkout HEAD~1 -- zodiac_app/assets/l10n/ | grep premium_feature
flutter gen-l10n
```

### Scenario 4: "One language completely broken"

```bash
# Restore just that language:
cp backups/translations_LATEST/app_de.arb zodiac_app/assets/l10n/
flutter gen-l10n

# Or from git:
git checkout HEAD~1 -- zodiac_app/assets/l10n/app_de.arb
flutter gen-l10n
```

### Scenario 5: "Tests failing after migration"

```bash
# Check what changed in tests:
git diff HEAD~1 -- zodiac_app/test/

# Rollback test changes if needed:
git checkout HEAD~1 -- zodiac_app/test/

# Or fix tests to match new keys
```

---

**END OF ROLLBACK PLAN**

**Keep this document accessible during migration. Safety first!** 🛡️
