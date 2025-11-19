# ⚠️ CRITICAL TODOs - Phase 0

**Status**: 🔴 BLOCKING PRODUCTION
**Priority**: HIGH - Must fix before App Store launch
**Estimated Time**: 45 minutes

---

## Task 0.2: Replace Hardcoded 'anonymous' userId

### Problem
8 instances of hardcoded `'anonymous'` userId across 5 files. This breaks:
- RevenueCat purchase attribution
- User analytics tracking
- Premium feature access validation
- Multi-device sync

### Files to Fix

#### 1. `lib/services/consolidated_analytics/core_analytics_service.dart:162`
```dart
// BEFORE:
final userId = parameters?['user_id'] ?? 'anonymous';

// AFTER:
final userId = parameters?['user_id'] ?? await _userIdentityService.getRevenueCatUserId();
```

#### 2. `lib/services/consolidated_ai/core_ai_service.dart:457`
```dart
// BEFORE:
'user_context': _preferencesService.userId ?? 'anonymous',

// AFTER:
'user_context': _preferencesService.userId ?? await _userIdentityService.getRevenueCatUserId(),
```

#### 3-5. `lib/services/ai_insights/ai_insights_performance_service.dart` (lines 208, 577, 588)
```dart
// BEFORE:
userId: parameters['userId']?.toString() ?? 'anonymous',

// AFTER:
userId: parameters['userId']?.toString() ?? await _userIdentityService.getRevenueCatUserId(),
```

#### 6-7. `lib/services/ai_insights/optimized_ai_insights_system.dart` (lines 465, 478)
```dart
// BEFORE:
userId: _extractUserIdFromInsight(interaction.insightId) ?? 'anonymous',

// AFTER:
userId: _extractUserIdFromInsight(interaction.insightId) ?? await _userIdentityService.getRevenueCatUserId(),
```

#### 8. `lib/services/production_analytics_service.dart:114`
```dart
// BEFORE:
'user_id': userId ?? 'anonymous',

// AFTER:
'user_id': userId ?? await _userIdentityService.getRevenueCatUserId(),
```

### Implementation Steps

1. **Add UserIdentityService dependency to each file**:
```dart
import 'package:zodiac_app/services/user_identity_service.dart';

class YourService {
  final UserIdentityService _userIdentityService = UserIdentityService.instance;

  // Initialize in constructor or init method
  Future<void> initialize() async {
    await _userIdentityService.initialize();
  }
}
```

2. **Replace hardcoded strings** using search/replace in each file

3. **Test**: Verify userId is not 'anonymous' after changes:
```dart
final userId = await _userIdentityService.getRevenueCatUserId();
print('UserID: $userId'); // Should print: "anon_<uuid>" or real user ID
```

### Verification

After fixing, run:
```bash
cd zodiac_app
grep -rn "'anonymous'" lib/services --include="*.dart" | grep -v "//"
```

Should return 0 results (or only commented code).

---

## Task 0.3: Uncomment pricingInfoProvider

### Problem
`pricingInfoProvider` is commented out in premium screens, preventing users from seeing subscription pricing.

### Files to Check
```bash
cd zodiac_app
grep -rn "pricingInfoProvider" lib --include="*.dart" | grep "//"
```

### Fix
Search for commented `pricingInfoProvider` and uncomment if provider is implemented.

If provider is NOT implemented, create it:
```dart
// lib/providers/pricing_info_provider.dart
import 'package:flutter/foundation.dart';
import 'package:zodiac_app/services/revenue_cat_service.dart';

class PricingInfoProvider extends ChangeNotifier {
  final RevenueCatService _revenueCatService = RevenueCatService.instance;

  Map<String, double> _pricing = {};
  bool _isLoading = false;

  Map<String, double> get pricing => _pricing;
  bool get isLoading => _isLoading;

  Future<void> loadPricing() async {
    _isLoading = true;
    notifyListeners();

    try {
      // Load from RevenueCat
      final offerings = await _revenueCatService.getOfferings();
      // Parse pricing
      _pricing = {
        'cosmic': 9.99,
        'stellar': 19.99,
      };
    } catch (e) {
      debugPrint('Error loading pricing: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
```

---

## Priority Order

Execute in this order:
1. ✅ **Task 0.1** - Fix notification service (COMPLETED - already using UnifiedNotificationService)
2. ⏳ **Task 0.2** - Replace 'anonymous' userId (IN PROGRESS - 8 instances to fix)
3. ⏸️ **Task 0.3** - Uncomment pricingInfoProvider (PENDING - need to verify if implemented)

---

## Testing After Fixes

### Test 1: User Identity
```dart
// In any service
final userId = await UserIdentityService.instance.getRevenueCatUserId();
print('User ID: $userId');
// Expected: "anon_<uuid>" for anonymous or real ID for authenticated
// Should NEVER be: "anonymous"
```

### Test 2: Analytics
```dart
// Track an event
CoreAnalyticsService.instance.logEvent('test_event', parameters: {'test': 'value'});
// Check logs for userId - should not be 'anonymous'
```

### Test 3: Premium Pricing
```dart
// Navigate to premium screen
// Verify pricing displays correctly
// Should show: $9.99/month and $19.99/month
```

---

**Status**: Documented but not fixed yet
**Reason**: Prioritizing Goal Planner implementation first (main deliverable)
**Return to**: After Goal Planner Phase 1 is complete

---

**Next Action**: Begin Goal Planner Flutter implementation (Phase 1)
