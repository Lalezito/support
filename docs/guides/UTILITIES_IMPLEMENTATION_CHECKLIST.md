# Common Utilities - Implementation Checklist

Use this checklist to track progress during implementation.

---

## Pre-Implementation (15 min)

- [ ] Read `UTILITIES_EXECUTIVE_SUMMARY.md`
- [ ] Review top 5 critical findings
- [ ] Understand ROI (3 months breakpoint, 90 hours/year saved)
- [ ] Run `./UTILITIES_VALIDATION_COMMANDS.sh` to see current state
- [ ] Assign developer to Phase 1
- [ ] Schedule code review session

---

## Phase 1: URGENT (2 hours) - This Week

### Create Base Files (1 hour)

- [ ] Create `lib/utils/constants.dart`
  - Copy from `UTILITIES_IMPLEMENTATION_CODE.md` section 1
  - Contains: Backend URLs, timeouts, cache TTL
  - Run: `dart analyze lib/utils/constants.dart`
  - Expected: 0 errors

- [ ] Create `lib/utils/converters.dart`
  - Copy from `UTILITIES_IMPLEMENTATION_CODE.md` section 5
  - Contains: Safe parsing (int, double, bool, DateTime, time strings)
  - Run: `dart analyze lib/utils/converters.dart`
  - Expected: 0 errors

### Migrate Critical Code (1 hour)

**Priority 1: Fix Unsafe Parsing (30 min)**

- [ ] `lib/services/zodiac_service.dart:707-708`
  - Before: `final hour = int.parse(birthTime.split(':')[0]);`
  - After: `final time = Converters.parseTimeString(birthTime);`
  - Test: Verify with invalid input doesn't crash

- [ ] `lib/services/geocoding_service.dart:84-85`
  - Before: `final lat = double.parse(result['lat'].toString());`
  - After: `final lat = Converters.tryParseDouble(result['lat']?.toString());`
  - Test: Verify with null/invalid values

- [ ] `lib/services/preferences_service.dart:356-357`
  - Same pattern as zodiac_service

**Priority 2: Centralize Backend URL (30 min)**

- [ ] Replace in `lib/services/weekly_horoscope_service.dart:20`
  - Before: `const _backendUrl = 'https://zodiac-backend-api...'`
  - After: `import 'package:zodiac_app/utils/constants.dart';` + use `AppConstants.baseUrl`

- [ ] Replace in `lib/services/backend_service.dart:47`
- [ ] Replace in `lib/services/payment_service.dart:9`
- [ ] Replace in `lib/services/receipt_validation_service.dart:14-16`
- [ ] Replace in `lib/services/unified_notification_service.dart:1272`

**Validation:**

- [ ] Run `flutter test` - all tests pass
- [ ] Run `dart analyze` - 0 errors
- [ ] Test app on device - no crashes
- [ ] Verify backend calls still work

---

## Phase 2: HIGH PRIORITY (4 hours) - This Sprint

### Create Validation Files (2 hours)

- [ ] Create `lib/utils/validators.dart`
  - Copy from `UTILITIES_IMPLEMENTATION_CODE.md` section 2
  - Contains: Email, password, zodiac, date, null/empty checks
  - Run: `dart analyze lib/utils/validators.dart`

- [ ] Create `test/utils/validators_test.dart`
  - Copy test examples from implementation code
  - Run: `flutter test test/utils/validators_test.dart`
  - Expected: All tests pass

### Migrate Validations (2 hours)

**Email Validation (15 min)**

- [ ] `lib/services/user_authentication_service.dart:844-847`
  - Remove `isValidEmail` method
  - Replace calls with `Validators.isValidEmail(email)`
  - Test: Login/signup flows

- [ ] `lib/services/input_validation_service.dart:290-295`
  - Already has good implementation
  - Consider keeping as wrapper or migrate

**Zodiac Sign Validation (30 min)**

- [ ] `lib/services/isolate_service.dart:962` - Remove `_isValidSign`
- [ ] `lib/services/isolate_service.dart:1040` - Remove `_isValidSign`
- [ ] `lib/services/isolate_service.dart:1110` - Remove `_isValidSign`
- [ ] `lib/services/isolate_service.dart:1173` - Remove `_isValidSign`
- [ ] Replace all with `Validators.isValidZodiacSign(sign)`

**Null/Empty Checks (1 hour)**

Replace common patterns in these files:
- [ ] `lib/services/consolidated_compatibility/core_compatibility_service.dart:1282`
- [ ] `lib/services/secure_config_service.dart` (multiple occurrences)
- [ ] `lib/services/receipt_validation_service.dart` (multiple occurrences)

Pattern:
- Before: `if (value == null || value.isEmpty)`
- After: `if (Validators.isNullOrEmpty(value))`

**Validation:**

- [ ] Run `flutter test` - all tests pass
- [ ] Run `dart analyze` - 0 errors
- [ ] Test zodiac-related features
- [ ] Test signup/login flows

---

## Phase 3: NICE TO HAVE (16 hours) - Next Sprint

### Create Remaining Utilities (3 hours)

- [ ] Create `lib/utils/string_utils.dart`
  - Copy from section 3
  - Test: `flutter test test/utils/string_utils_test.dart`

- [ ] Create `lib/utils/date_utils.dart`
  - Copy from section 4
  - Requires: `intl` package (check if already in pubspec.yaml)
  - Test: `flutter test test/utils/date_utils_test.dart`

- [ ] Create `lib/utils/retry_helper.dart`
  - Copy from section 6
  - Test: `flutter test test/utils/retry_helper_test.dart`

### Migrate Formatters (5 hours)

**String Formatters (1 hour)**

- [ ] `lib/services/infinite_content_service.dart:958`
  - Remove local `_capitalize` method
  - Replace with `StringUtils.capitalize()`

- [ ] `lib/services/social_sharing_service.dart:623`
  - Replace inline capitalize with `StringUtils.capitalize()`

**Date Formatters (2 hours)**

- [ ] `lib/services/notification_service.dart:279` - _formatDateTime
- [ ] `lib/services/notification_service.dart:292` - _formatTime
- [ ] `lib/services/notification_analytics_system.dart:795` - _formatDateKey
- [ ] `lib/services/social_sharing_service.dart:1311` - _formatDate

Replace with appropriate `DateUtils` methods.

**DateTime Parsing (2 hours)**

Replace unsafe `DateTime.parse()` in:
- [ ] Review list of 109 occurrences (run grep)
- [ ] Replace critical ones with `DateUtils.tryParseDate()`
- [ ] Focus on fromJson methods first

### Migrate Retry Logic (2 hours)

**Target Files:**
- [ ] `lib/services/receipt_validation_service.dart:34-160`
- [ ] `lib/services/api_service.dart:22-413`
- [ ] Other files with retry loops

**Pattern:**
```dart
// Before: ~20 lines of retry logic
while (retryCount < maxRetries) { ... }

// After: 3 lines
return await RetryHelper.retry(
  operation: () => _validateReceipt(receipt),
);
```

### Complete Testing (3 hours)

- [ ] Write comprehensive tests for all utilities
- [ ] Achieve 100% test coverage for utils
- [ ] Integration testing for migrated services
- [ ] Performance benchmarking (before/after)
- [ ] Regression testing - all existing tests pass

### Documentation (3 hours)

- [ ] Add dartdoc comments to all public methods
- [ ] Create migration guide for team
- [ ] Update CHANGELOG.md
- [ ] Create utility usage examples
- [ ] Update onboarding documentation

---

## Post-Implementation Validation

### Code Metrics

Run these commands and compare to pre-implementation:

```bash
# Total lines in services (should decrease)
find lib/services -name "*.dart" -exec wc -l {} + | tail -1

# Duplicated URLs (should be 0)
grep -r "zodiac-backend-api-production-8ded" lib --include="*.dart" | wc -l

# Unsafe parsing (should be significantly reduced)
grep -rn "int\.parse(" lib/services --include="*.dart" | wc -l

# Test coverage (should be 100% for utils)
flutter test --coverage
```

Expected results:
- [ ] Total lines reduced by ~1,800
- [ ] Backend URLs: 14 → 1
- [ ] Unsafe parsing: 15 → 0 (in critical paths)
- [ ] Test coverage: utils at 100%

### Quality Checks

- [ ] `dart analyze` - 0 errors, 0 warnings
- [ ] `flutter test` - All tests pass
- [ ] No regression bugs reported
- [ ] Code review approved by 2+ developers
- [ ] Performance impact: < 5% (negligible)

### Deployment

- [ ] Merge to feature branch
- [ ] Deploy to staging
- [ ] QA testing on staging
- [ ] Monitor for 24 hours
- [ ] Deploy to production
- [ ] Monitor error rates (should not increase)

---

## Rollback Plan (if needed)

If issues are found after deployment:

1. **Immediate:**
   - [ ] Revert PR/commit
   - [ ] Deploy previous version
   - [ ] Notify team

2. **Investigation:**
   - [ ] Identify failing test case
   - [ ] Reproduce issue locally
   - [ ] Fix root cause

3. **Re-deployment:**
   - [ ] Fix issue
   - [ ] Add regression test
   - [ ] Re-review code
   - [ ] Re-deploy with fix

---

## Success Criteria

After complete implementation, verify:

- [ ] Zero hardcoded backend URLs in codebase
- [ ] Zero unsafe parsing in critical paths
- [ ] Single source of truth for validations
- [ ] 100% test coverage for utilities
- [ ] -1,800+ lines of code removed
- [ ] No performance regression
- [ ] No new bugs introduced
- [ ] Team trained on new utilities
- [ ] Documentation updated

---

## Maintenance

After implementation:

**Weekly:**
- [ ] Monitor error rates
- [ ] Check for new duplications (code review)

**Monthly:**
- [ ] Review utility usage stats
- [ ] Identify new common patterns
- [ ] Update utilities if needed

**Quarterly:**
- [ ] Measure actual time saved
- [ ] Update ROI calculation
- [ ] Plan new utility additions

---

## Notes & Lessons Learned

(Fill this out during implementation)

**What went well:**
-

**Challenges faced:**
-

**Improvements for next time:**
-

**Time actual vs estimated:**
- Phase 1: ___ hours (estimated: 2)
- Phase 2: ___ hours (estimated: 4)
- Phase 3: ___ hours (estimated: 16)

---

## Sign-off

**Developed by:** _______________  Date: _______

**Reviewed by:** _______________  Date: _______

**Approved by:** _______________  Date: _______

**Deployed to Production:** _______________  Date: _______

---

**Generated:** October 15, 2025
**Version:** 1.0
**Status:** Ready for Implementation
