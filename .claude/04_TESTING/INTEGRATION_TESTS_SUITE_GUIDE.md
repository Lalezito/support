# 🔗 INTEGRATION TESTS SUITE GUIDE

**Objetivo**: Suite completa de tests de integración end-to-end
**Prioridad**: ALTA
**Fecha**: 2025-10-05

---

## 📊 Integration Test Overview

Integration tests verify that multiple components work together correctly in real-world scenarios.

### Test Categories

1. **End-to-End User Journeys** (8 tests)
2. **Cross-Service Integration** (6 tests)
3. **Error Recovery & Resilience** (4 tests)

**Total**: 18 integration tests

---

## 🎯 End-to-End User Journeys

### 1. Onboarding to Premium Purchase Flow

**File**: `integration_test/flows/onboarding_to_premium_test.dart`

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:zodiac_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Onboarding to Premium Purchase Flow', () {
    testWidgets('Complete user journey from first launch to premium',
      (WidgetTester tester) async {
      // Launch app
      app.main();
      await tester.pumpAndSettle();

      // Step 1: Welcome screen
      expect(find.text('Welcome to Zodiac Life Coach'), findsOneWidget);
      await tester.tap(find.text('Get Started'));
      await tester.pumpAndSettle();

      // Step 2: Enter birth data
      expect(find.text('Enter Your Birth Details'), findsOneWidget);

      await tester.enterText(find.byKey(Key('birth_date_field')), '01/01/1990');
      await tester.enterText(find.byKey(Key('birth_time_field')), '12:00 PM');
      await tester.enterText(find.byKey(Key('birth_location_field')), 'New York');

      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Step 3: Birth chart calculated
      expect(find.text('Your Cosmic Profile'), findsOneWidget);
      expect(find.textContaining('Sun:'), findsOneWidget);
      expect(find.textContaining('Moon:'), findsOneWidget);

      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Step 4: View first horoscope (free)
      expect(find.text('Daily Horoscope'), findsOneWidget);
      await tester.pumpAndSettle();

      // Step 5: Try to access premium feature (AI Coach)
      await tester.tap(find.byIcon(Icons.psychology));
      await tester.pumpAndSettle();

      // Step 6: Paywall appears
      expect(find.text('Unlock AI Cosmic Coach'), findsOneWidget);
      expect(find.text('Essential - $4.99/month'), findsOneWidget);

      // Step 7: Select Essential tier
      await tester.tap(find.text('Choose Essential'));
      await tester.pumpAndSettle();

      // Step 8: Purchase flow (mocked in test environment)
      // Note: In integration tests, we mock the actual purchase
      await tester.tap(find.text('Subscribe'));
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Step 9: Premium activated
      expect(find.text('Welcome to Premium!'), findsOneWidget);

      // Step 10: AI Coach now accessible
      await tester.tap(find.text('Start Using'));
      await tester.pumpAndSettle();

      expect(find.text('AI Cosmic Coach'), findsOneWidget);
      expect(find.textContaining('Ask me anything'), findsOneWidget);

      // Verify analytics events were logged
      // (This would require a mock analytics service)
      // expect(analyticsEvents).toContain('purchase_completed');
    });
  });
}
```

**Expected Duration**: 15-20 seconds
**Assertions**: 15+
**Coverage**: Onboarding, birth data, paywall, purchase, feature unlock

---

### 2. Free Trial Activation and Conversion

**File**: `integration_test/flows/trial_conversion_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Free Trial to Paid Conversion', () {
    testWidgets('User activates trial and converts to paid',
      (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Skip onboarding (assume existing user)
      await _skipOnboarding(tester);

      // Step 1: User hits feature limit (e.g., weekly horoscope locked)
      await tester.tap(find.text('Weekly Horoscope'));
      await tester.pumpAndSettle();

      expect(find.text('Try 7-Day Free Trial'), findsOneWidget);

      // Step 2: Activate trial
      await tester.tap(find.text('Start Free Trial'));
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Step 3: Trial activated
      expect(find.text('Trial Active'), findsOneWidget);
      expect(find.textContaining('7 days remaining'), findsOneWidget);

      // Step 4: Access premium features during trial
      await tester.tap(find.text('AI Cosmic Coach'));
      await tester.pumpAndSettle();

      expect(find.text('Ask me anything'), findsOneWidget);

      // Step 5: Simulate trial nearing expiration (day 5)
      // (This would use a test clock or mock)
      await _simulateTimeAdvance(days: 5, tester: tester);

      // Step 6: Trial expiring notification appears
      expect(find.text('2 days left in your trial'), findsOneWidget);

      // Step 7: Convert to paid Essential tier
      await tester.tap(find.text('Continue with Essential'));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Subscribe Now'));
      await tester.pumpAndSettle(Duration(seconds: 2));

      // Step 8: Conversion successful
      expect(find.text('Welcome to Essential!'), findsOneWidget);
      expect(find.textContaining('Trial'), findsNothing);

      // Verify analytics
      // expect(analyticsEvents).toContain('trial_converted');
    });
  });
}

Future<void> _skipOnboarding(WidgetTester tester) async {
  // Implementation to skip onboarding
}

Future<void> _simulateTimeAdvance({required int days, required WidgetTester tester}) async {
  // Implementation to advance time in tests
}
```

**Expected Duration**: 12-15 seconds
**Assertions**: 10+
**Coverage**: Trial activation, feature access, conversion

---

### 3. Offline Mode Usage and Sync

**File**: `integration_test/flows/offline_sync_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Offline Mode and Sync', () {
    testWidgets('User goes offline, uses app, then syncs when online',
      (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      await _skipOnboarding(tester);

      // Step 1: Load horoscope while online (caches it)
      await tester.tap(find.text('Daily Horoscope'));
      await tester.pumpAndSettle();

      expect(find.textContaining('Aries'), findsOneWidget);

      // Step 2: Simulate going offline
      await _setNetworkConnectivity(false);
      await tester.pumpAndSettle();

      // Step 3: Offline indicator appears
      expect(find.text('Offline Mode'), findsOneWidget);

      // Step 4: Navigate away and back to horoscope
      await tester.tap(find.byIcon(Icons.home));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Daily Horoscope'));
      await tester.pumpAndSettle();

      // Step 5: Cached horoscope displayed
      expect(find.textContaining('Aries'), findsOneWidget);
      expect(find.text('Cached'), findsOneWidget);

      // Step 6: Create journal entry while offline
      await tester.tap(find.text('Journal'));
      await tester.pumpAndSettle();

      await tester.tap(find.byIcon(Icons.add));
      await tester.pumpAndSettle();

      await tester.enterText(
        find.byKey(Key('journal_content')),
        'Offline test entry'
      );

      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      // Step 7: Entry saved locally
      expect(find.text('Saved locally'), findsOneWidget);
      expect(find.text('Will sync when online'), findsOneWidget);

      // Step 8: Restore connectivity
      await _setNetworkConnectivity(true);
      await tester.pumpAndSettle();

      // Step 9: Auto-sync triggers
      expect(find.text('Syncing...'), findsOneWidget);
      await tester.pumpAndSettle(Duration(seconds: 3));

      // Step 10: Sync complete
      expect(find.text('Synced'), findsOneWidget);
      expect(find.text('Offline Mode'), findsNothing);

      // Step 11: Refresh horoscope (gets fresh data)
      await tester.drag(
        find.byType(RefreshIndicator),
        Offset(0, 300),
      );
      await tester.pumpAndSettle();

      expect(find.text('Cached'), findsNothing);
    });
  });
}

Future<void> _setNetworkConnectivity(bool online) async {
  // Mock network connectivity
}
```

**Expected Duration**: 18-22 seconds
**Assertions**: 12+
**Coverage**: Offline detection, cache usage, sync, conflict resolution

---

### 4. Notification Scheduling and Delivery

**File**: `integration_test/flows/notification_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Notification Scheduling', () {
    testWidgets('User enables notifications and receives them',
      (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      await _skipOnboarding(tester);

      // Step 1: Go to settings
      await tester.tap(find.byIcon(Icons.settings));
      await tester.pumpAndSettle();

      // Step 2: Enable notifications
      expect(find.text('Daily Horoscope Notifications'), findsOneWidget);

      final notificationSwitch = find.byKey(Key('notification_toggle'));
      await tester.tap(notificationSwitch);
      await tester.pumpAndSettle();

      // Step 3: Permission dialog appears
      // (In integration tests, this is simulated)
      expect(find.text('Allow Notifications'), findsOneWidget);

      await tester.tap(find.text('Allow'));
      await tester.pumpAndSettle();

      // Step 4: Select notification time
      await tester.tap(find.text('9:00 AM'));
      await tester.pumpAndSettle();

      final timePicker = find.byType(TimePickerDialog);
      expect(timePicker, findsOneWidget);

      // Select 10:00 AM
      await tester.tap(find.text('10'));
      await tester.tap(find.text('00'));
      await tester.tap(find.text('OK'));
      await tester.pumpAndSettle();

      // Step 5: Notification scheduled
      expect(find.text('10:00 AM'), findsOneWidget);
      expect(find.text('Daily notifications enabled'), findsOneWidget);

      // Step 6: Verify notification was scheduled
      // (This would check the notification service)
      final pendingNotifications = await _getPendingNotifications();
      expect(pendingNotifications.length, 1);
      expect(pendingNotifications.first.hour, 10);
      expect(pendingNotifications.first.minute, 0);

      // Step 7: Simulate notification delivery
      await _triggerScheduledNotification(pendingNotifications.first);
      await tester.pumpAndSettle();

      // Step 8: Tap notification (deep link)
      await _tapNotification();
      await tester.pumpAndSettle();

      // Step 9: App opens to horoscope screen
      expect(find.text('Daily Horoscope'), findsOneWidget);
    });
  });
}

Future<List<PendingNotificationRequest>> _getPendingNotifications() async {
  // Implementation
}

Future<void> _triggerScheduledNotification(PendingNotificationRequest notification) async {
  // Implementation
}

Future<void> _tapNotification() async {
  // Implementation
}
```

**Expected Duration**: 10-12 seconds
**Assertions**: 8+
**Coverage**: Permission request, scheduling, delivery, deep linking

---

## 🔄 Cross-Service Integration Tests

### 5. Premium Feature Gating Across Tiers

**File**: `integration_test/integration/feature_gating_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Feature Gating', () {
    testWidgets('Features unlock correctly for each tier',
      (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Test Free Tier
      await _setUserTier(SubscriptionType.free);
      await tester.pumpAndSettle();

      // Free user: AI Coach locked
      await tester.tap(find.text('AI Coach'));
      await tester.pumpAndSettle();
      expect(find.text('Premium Feature'), findsOneWidget);

      // Upgrade to Essential
      await _setUserTier(SubscriptionType.essential);
      await tester.pumpAndSettle();

      // Essential user: AI Coach unlocked
      await tester.tap(find.text('AI Coach'));
      await tester.pumpAndSettle();
      expect(find.text('Ask me anything'), findsOneWidget);

      // Essential user: Smart Journaling locked
      await tester.tap(find.text('Smart Journal'));
      await tester.pumpAndSettle();
      expect(find.text('Premium Feature'), findsOneWidget);

      // Upgrade to Advanced
      await _setUserTier(SubscriptionType.advanced);
      await tester.pumpAndSettle();

      // Advanced user: Smart Journaling unlocked
      await tester.tap(find.text('Smart Journal'));
      await tester.pumpAndSettle();
      expect(find.text('Write your thoughts'), findsOneWidget);
    });
  });
}

Future<void> _setUserTier(SubscriptionType tier) async {
  // Mock tier change
}
```

**Assertions**: 6+
**Coverage**: Feature gating, tier validation

---

### 6. Analytics Tracking Throughout User Journey

**File**: `integration_test/integration/analytics_tracking_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Analytics Tracking', () {
    testWidgets('All critical events logged correctly',
      (WidgetTester tester) async {
      final mockAnalytics = MockAnalyticsService();

      app.main(analyticsService: mockAnalytics);
      await tester.pumpAndSettle();

      // Complete user journey
      await _completeOnboarding(tester);
      await _viewHoroscope(tester);
      await _checkCompatibility(tester);
      await _purchasePremium(tester);

      // Verify events
      final events = mockAnalytics.getLoggedEvents();

      expect(events.where((e) => e.name == 'app_opened'), hasLength(1));
      expect(events.where((e) => e.name == 'onboarding_completed'), hasLength(1));
      expect(events.where((e) => e.name == 'horoscope_viewed'), hasLength(1));
      expect(events.where((e) => e.name == 'compatibility_analyzed'), hasLength(1));
      expect(events.where((e) => e.name == 'purchase_completed'), hasLength(1));

      // Verify event parameters
      final purchaseEvent = events.firstWhere((e) => e.name == 'purchase_completed');
      expect(purchaseEvent.parameters['tier'], 'essential');
      expect(purchaseEvent.parameters['revenue'], 4.99);
    });
  });
}
```

**Assertions**: 7+
**Coverage**: Analytics integration, event logging

---

## 🚨 Error Recovery Tests

### 7. Handle Network Failures Gracefully

**File**: `integration_test/error_recovery/network_failure_test.dart`

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Network Failure Recovery', () {
    testWidgets('App handles API failures gracefully',
      (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      await _skipOnboarding(tester);

      // Step 1: Simulate API failure
      await _setAPIResponse(500, error: true);

      // Step 2: Try to fetch horoscope
      await tester.tap(find.text('Daily Horoscope'));
      await tester.pumpAndSettle();

      // Step 3: Error handled gracefully
      expect(find.text('Unable to fetch latest horoscope'), findsOneWidget);
      expect(find.text('Showing cached version'), findsOneWidget);

      // Step 4: Retry button available
      expect(find.text('Retry'), findsOneWidget);

      // Step 5: Restore API
      await _setAPIResponse(200, error: false);

      // Step 6: Tap retry
      await tester.tap(find.text('Retry'));
      await tester.pumpAndSettle();

      // Step 7: Fresh data loaded
      expect(find.text('Unable to fetch'), findsNothing);
      expect(find.textContaining('Today'), findsOneWidget);
    });
  });
}

Future<void> _setAPIResponse(int statusCode, {required bool error}) async {
  // Mock API response
}
```

**Assertions**: 5+
**Coverage**: Error handling, retry logic, fallback strategies

---

## 🛠️ Test Setup & Configuration

### Integration Test Dependencies

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

---

### Test Runner Script

**File**: `scripts/run_integration_tests.sh`

```bash
#!/bin/bash

echo "🧪 Running Integration Tests..."

# Clean build
flutter clean
flutter pub get

# Run integration tests
flutter test integration_test/ \
  --reporter expanded \
  --timeout 120s

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ All integration tests passed!"
else
  echo "❌ Integration tests failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
```

Make executable:
```bash
chmod +x scripts/run_integration_tests.sh
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/integration_tests.yml`

```yaml
name: Integration Tests

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  integration-tests:
    runs-on: macos-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.29.2'
          channel: 'stable'

      - name: Install dependencies
        run: flutter pub get

      - name: Run integration tests
        run: flutter test integration_test/ --reporter expanded

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: integration-test-results
          path: |
            integration_test/screenshots/
            integration_test/logs/
```

---

## ✅ Success Criteria

**Must Pass**:
- [ ] All 18 integration tests pass
- [ ] Tests complete in <3 minutes total
- [ ] Zero flaky tests (pass 100% of time)
- [ ] All critical user journeys covered

**Quality Metrics**:
- [ ] Test coverage across all major flows
- [ ] Error scenarios handled
- [ ] Performance within acceptable ranges
- [ ] Analytics events verified

---

**Status**: 📝 GUIDE READY
**Priority**: 🔴 HIGH
**Total Tests**: 18 integration tests
**Est. Execution Time**: 2-3 minutes
**Next Steps**: Implement tests incrementally
