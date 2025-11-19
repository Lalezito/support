# 🧪 UNIT TEST COVERAGE PLAN

**Objetivo**: Alcanzar 80%+ coverage en servicios críticos
**Prioridad**: CRÍTICA
**Fecha**: 2025-10-05

---

## 📊 Coverage Targets

### Overall Target
- **General Coverage**: 75% minimum
- **Critical Services**: 90% minimum
- **Business Logic**: 85% minimum
- **Utilities**: 80% minimum

---

## 🎯 Service Coverage Targets

### Tier 1: Critical Services (90%+ coverage required)

#### 1. CoreCompatibilityService
**Location**: `lib/services/consolidated_compatibility/core_compatibility_service.dart`

**Test Coverage Required**:
```dart
// test/services/compatibility/core_compatibility_service_test.dart

✅ Basic Compatibility Analysis
- [ ] analyzeCompatibility() with valid signs
- [ ] analyzeCompatibility() with invalid signs
- [ ] analyzeCompatibility() with null parameters
- [ ] Score calculation accuracy (0-100)
- [ ] Relationship type variations (romantic, friendship, business)

✅ Caching Behavior
- [ ] First call caches result
- [ ] Second call returns cached result
- [ ] Cache expiration after TTL
- [ ] Cache invalidation works

✅ Analytics Integration
- [ ] Logs compatibility_analyzed event
- [ ] Includes correct parameters (sign1, sign2, score)
- [ ] User ID included in analytics
- [ ] Handles analytics failures gracefully

✅ Error Handling
- [ ] Backend API failure
- [ ] Network timeout
- [ ] Invalid response format
- [ ] Fallback to cached data
```

**Target**: 90%+ coverage

---

#### 2. PremiumSubscriptionManager
**Location**: `lib/services/premium_subscription_manager.dart`

**Test Coverage Required**:
```dart
// test/services/premium_subscription_manager_test.dart

✅ Subscription State Management
- [ ] getCurrentSubscriptionType() returns correct tier
- [ ] isPremium() returns true for paid tiers
- [ ] isPremium() returns false for free tier
- [ ] Trial counts as premium
- [ ] Lifetime counts as premium

✅ Purchase Flow
- [ ] activatePremium() updates state
- [ ] activatePremium() persists to storage
- [ ] activatePremium() triggers analytics
- [ ] Purchase fails gracefully
- [ ] Handles RevenueCat errors

✅ Trial Management
- [ ] activateFreeTrial() works for new users
- [ ] activateFreeTrial() fails if trial already used
- [ ] getDaysRemaining() calculates correctly
- [ ] Trial expiration handled properly

✅ Restore Purchases
- [ ] restorePurchases() activates correct tier
- [ ] restorePurchases() handles no purchases
- [ ] restorePurchases() handles multiple purchases
- [ ] Syncs with RevenueCat correctly
```

**Target**: 95%+ coverage (revenue-critical)

---

#### 3. UnifiedNotificationService
**Location**: `lib/services/unified_notification_service.dart`

**Test Coverage Required**:
```dart
// test/services/notification/unified_notification_service_test.dart

✅ Initialization
- [ ] initialize() sets up platform channels
- [ ] initialize() requests permissions
- [ ] initialize() handles iOS vs Android differences

✅ Permission Handling
- [ ] requestPermission() returns true when granted
- [ ] requestPermission() returns false when denied
- [ ] hasPermission() reflects actual state

✅ Scheduling
- [ ] scheduleDailyNotification() creates notification
- [ ] Notification persists across restarts
- [ ] cancelNotification() removes notification
- [ ] cancelAllNotifications() clears all

✅ Deep Linking
- [ ] Notification tap triggers callback
- [ ] Payload passed correctly
- [ ] App launch from notification works
```

**Target**: 90%+ coverage

---

#### 4. OfflineModeService
**Location**: `lib/services/offline_mode_service.dart`

**Test Coverage Required**:
```dart
// test/services/offline/offline_mode_service_test.dart

✅ Connectivity Detection
- [ ] isOnline returns true when connected
- [ ] isOnline returns false when offline
- [ ] Detects connectivity changes
- [ ] Triggers sync on reconnect

✅ Cache Management
- [ ] Caches data when online
- [ ] Returns cached data when offline
- [ ] Respects cache expiration
- [ ] Clears cache correctly

✅ Synchronization
- [ ] Auto-sync on connectivity restore
- [ ] Manual sync via refresh
- [ ] Sync queue management
- [ ] Conflict resolution
```

**Target**: 90%+ coverage

---

#### 5. UserIdentityService
**Location**: `lib/services/user_identity_service.dart`

**Test Coverage Required**:
```dart
// test/services/user_identity_service_test.dart

✅ User ID Management
- [ ] getUserId() returns consistent ID
- [ ] getUserId() generates ID if not exists
- [ ] getUserId() persists across restarts
- [ ] setUserId() updates ID correctly

✅ Analytics Integration
- [ ] User ID sent to analytics (hashed)
- [ ] User properties set correctly
- [ ] Anonymous users handled
```

**Target**: 90%+ coverage

---

### Tier 2: Business Logic (85%+ coverage required)

#### 6. PremiumProvider
**Location**: `lib/providers/premium_provider.dart`

**Test Coverage Required**:
```dart
// test/providers/premium_provider_test.dart

✅ State Management
- [ ] notifyListeners() called on tier change
- [ ] getCurrentSubscriptionType() reflects state
- [ ] isPremium reflects state changes

✅ Feature Gating
- [ ] Feature availability by tier
- [ ] Tier upgrades unlock features
- [ ] Tier downgrades lock features
```

**Target**: 85%+ coverage

---

#### 7. SubscriptionService
**Location**: `lib/services/subscription_service.dart`

**Test Coverage Required**:
```dart
// test/services/subscription_service_test.dart

✅ Purchase Operations
- [ ] purchaseTier() completes successfully
- [ ] purchaseTier() handles cancellation
- [ ] purchaseTier() handles errors
- [ ] Analytics logged for all outcomes

✅ Restore Operations
- [ ] restorePurchases() restores active subscription
- [ ] restorePurchases() handles expired subscription
- [ ] restorePurchases() handles no purchases
```

**Target**: 85%+ coverage

---

#### 8. SmartJournalingService
**Location**: `lib/services/smart_journaling_service.dart`

**Test Coverage Required**:
```dart
// test/services/journaling/smart_journaling_service_test.dart

✅ Entry Creation
- [ ] createEntry() saves entry
- [ ] createEntry() analyzes emotions
- [ ] createEntry() persists to storage

✅ Emotional Analysis
- [ ] Detects positive emotions
- [ ] Detects negative emotions
- [ ] Crisis detection works
- [ ] Pattern analysis over time
```

**Target**: 85%+ coverage

---

### Tier 3: Utilities (80%+ coverage required)

#### 9. SecureLoggingService
**Location**: `lib/services/secure_logging_service.dart`

**Test Coverage Required**:
```dart
// test/services/logging/secure_logging_service_test.dart

✅ Log Levels
- [ ] debug() logs in development
- [ ] info() logs in all environments
- [ ] error() logs and reports to Crashlytics
- [ ] critical() triggers alerts

✅ Sensitive Data Protection
- [ ] Passwords redacted
- [ ] Emails redacted
- [ ] Tokens redacted
- [ ] User IDs hashed
```

**Target**: 80%+ coverage

---

#### 10. PerformanceMonitoringService
**Location**: `lib/services/performance_monitoring_service.dart`

**Test Coverage Required**:
```dart
// test/services/performance/performance_monitoring_service_test.dart

✅ Metrics Collection
- [ ] App startup time tracked
- [ ] Screen load time tracked
- [ ] API latency tracked
- [ ] Metrics persisted

✅ Performance Budgets
- [ ] Budget violations detected
- [ ] Alerts triggered on violations
```

**Target**: 80%+ coverage

---

## 🔧 Commands & Setup

### Generate Coverage Report

```bash
# Run all tests with coverage
flutter test --coverage

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html

# Open report in browser
open coverage/html/index.html  # macOS
# or
xdg-open coverage/html/index.html  # Linux
# or
start coverage/html/index.html  # Windows
```

---

### Run Tests by Category

```bash
# Core services only
flutter test test/services/

# Providers only
flutter test test/providers/

# Widgets only
flutter test test/widgets/

# Specific service
flutter test test/services/compatibility/core_compatibility_service_test.dart
```

---

### Coverage Filtering

```bash
# Exclude generated files from coverage
flutter test --coverage \
  --coverage-exclude='**/*.g.dart' \
  --coverage-exclude='**/*.freezed.dart' \
  --coverage-exclude='**/l10n/**'
```

---

## 📊 Coverage Analysis

### View Coverage by File

```bash
# Install lcov tools
# macOS: brew install lcov
# Ubuntu: sudo apt-get install lcov

# Generate summary
lcov --summary coverage/lcov.info

# Generate detailed report
lcov --list coverage/lcov.info
```

---

### Coverage Report Example

```
Reading tracefile coverage/lcov.info
Summary coverage rate:
  lines......: 78.3% (2345 of 2995 lines)
  functions..: 85.1% (456 of 536 functions)
  branches...: 72.4% (678 of 936 branches)

Files with low coverage:
  lib/services/compatibility_service.dart: 65.2%
  lib/services/journaling_service.dart: 58.7%
  lib/providers/theme_provider.dart: 70.1%
```

---

## 🎯 Action Plan to Reach Targets

### Week 1: Critical Services (90%+ coverage)
```markdown
Day 1-2: CoreCompatibilityService
- [ ] Write 20 unit tests covering all paths
- [ ] Mock analytics service
- [ ] Mock cache service
- [ ] Test error scenarios

Day 3-4: PremiumSubscriptionManager
- [ ] Write 25 unit tests (revenue-critical)
- [ ] Mock RevenueCat
- [ ] Test all purchase flows
- [ ] Test trial activation

Day 5: UnifiedNotificationService
- [ ] Write 15 unit tests
- [ ] Mock platform channels
- [ ] Test permission flows
```

### Week 2: Business Logic (85%+ coverage)
```markdown
Day 1: PremiumProvider
- [ ] Write 12 unit tests
- [ ] Test state changes
- [ ] Test feature gating

Day 2-3: SubscriptionService & SmartJournalingService
- [ ] Write 20 unit tests combined
- [ ] Test business logic thoroughly
```

### Week 3: Utilities (80%+ coverage)
```markdown
Day 1: SecureLoggingService
- [ ] Write 10 unit tests
- [ ] Test PII protection

Day 2: PerformanceMonitoringService
- [ ] Write 8 unit tests
- [ ] Test metrics collection
```

---

## 🧪 Testing Best Practices

### 1. Use Mocks for External Dependencies

```dart
class MockAnalyticsService extends Mock implements CoreAnalyticsService {}
class MockCacheService extends Mock implements CacheService {}

void main() {
  late CompatibilityService service;
  late MockAnalyticsService mockAnalytics;

  setUp(() {
    mockAnalytics = MockAnalyticsService();
    service = CompatibilityService(analytics: mockAnalytics);
  });

  test('logs analytics event on compatibility check', () async {
    await service.analyzeCompatibility('Aries', 'Leo');

    verify(mockAnalytics.logEvent('compatibility_analyzed', any)).called(1);
  });
}
```

---

### 2. Test Edge Cases

```dart
test('handles null sign gracefully', () async {
  expect(
    () => service.analyzeCompatibility(null, 'Leo'),
    throwsA(isA<ArgumentError>()),
  );
});

test('handles empty sign', () async {
  final result = await service.analyzeCompatibility('', 'Leo');
  expect(result.isValid, isFalse);
});
```

---

### 3. Test Async Operations

```dart
test('caches result asynchronously', () async {
  final result = await service.analyzeCompatibility('Aries', 'Leo');

  // Wait for cache operation to complete
  await Future.delayed(Duration(milliseconds: 100));

  verify(mockCache.set(any, result)).called(1);
});
```

---

### 4. Group Related Tests

```dart
group('CompatibilityService', () {
  group('analyzeCompatibility', () {
    test('returns valid result for valid signs', () { });
    test('throws error for invalid signs', () { });
  });

  group('caching', () {
    test('caches first result', () { });
    test('returns cached result on second call', () { });
  });
});
```

---

## 📈 Coverage Metrics Dashboard

### Target vs Actual

| Service | Target | Current | Gap | Priority |
|---------|--------|---------|-----|----------|
| CoreCompatibilityService | 90% | TBD | TBD | 🔴 High |
| PremiumSubscriptionManager | 95% | TBD | TBD | 🔴 Critical |
| UnifiedNotificationService | 90% | TBD | TBD | 🔴 High |
| OfflineModeService | 90% | TBD | TBD | 🔴 High |
| UserIdentityService | 90% | TBD | TBD | 🔴 High |
| PremiumProvider | 85% | TBD | TBD | 🟡 Medium |
| SubscriptionService | 85% | TBD | TBD | 🟡 Medium |
| SmartJournalingService | 85% | TBD | TBD | 🟡 Medium |
| SecureLoggingService | 80% | TBD | TBD | 🟢 Low |
| PerformanceMonitoring | 80% | TBD | TBD | 🟢 Low |

---

## ✅ Success Criteria

**Must Have**:
- [ ] All Tier 1 services: 90%+ coverage
- [ ] All Tier 2 services: 85%+ coverage
- [ ] All Tier 3 services: 80%+ coverage
- [ ] Overall coverage: 75%+
- [ ] Zero untested revenue-critical paths

**Nice to Have**:
- [ ] Overall coverage: 80%+
- [ ] All services: 85%+
- [ ] Widget tests: 70%+
- [ ] Integration tests passing

---

## 🔄 Continuous Monitoring

### CI/CD Integration

```yaml
# .github/workflows/test_coverage.yml
name: Test Coverage

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test --coverage
      - name: Check coverage
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 75" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 75% threshold"
            exit 1
          fi
```

---

**Status**: 📝 PLAN READY
**Priority**: 🔴 CRITICAL
**Est. Time**: 2-3 weeks for full implementation
**Next Steps**: Start with Tier 1 services
