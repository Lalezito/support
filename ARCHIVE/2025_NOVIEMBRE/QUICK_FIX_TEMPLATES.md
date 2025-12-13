# Quick Fix Templates for Pre-Existing Errors

**Priority Order:** Follow this exact sequence for fastest resolution

---

## 🔥 FIX #1: Define Missing Variables (5 minutes)

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/subscription_service.dart`

**Location:** Around line 142, right after `_stellarMonthly` definition

**Current Code (Lines 141-144):**
```dart
// Product IDs for App Store - Only monthly subscriptions
static const String _cosmicMonthly = 'tier1_subscription'; // Tier 1: Cosmic
static const String _stellarMonthly = 'tier2_subscription'; // Tier 2: Stellar

static const Set<String> _productIds = {_cosmicMonthly, _stellarMonthly};
```

**ADD THESE LINES:**
```dart
// Product IDs for App Store - Only monthly subscriptions
static const String _cosmicMonthly = 'tier1_subscription'; // Tier 1: Cosmic
static const String _stellarMonthly = 'tier2_subscription'; // Tier 2: Stellar

// ✅ BACKWARD COMPATIBILITY: Map old product IDs to new tier system
static const String _monthlyPremium = 'tier1_subscription'; // Maps to cosmic
static const String _lifetimePremium = 'tier2_subscription'; // Maps to stellar (no lifetime anymore)

static const Set<String> _productIds = {_cosmicMonthly, _stellarMonthly};
```

**This fixes:** 11 undefined variable errors in subscription_service.dart

---

## 🔥 FIX #2: Remove Universe from Test Mode (2 minutes)

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/subscription_service.dart`

**Location:** Lines 104-106

**BEFORE:**
```dart
case 'universe':
  developer.log('✅ Returning PremiumTier.universe from test mode', name: 'SubscriptionService');
  return PremiumTier.universe;
```

**AFTER:**
```dart
case 'universe':
  developer.log('⚠️ Universe tier deprecated, returning stellar instead', name: 'SubscriptionService');
  return PremiumTier.stellar; // Universe removed, map to highest tier
```

**Also fix Line 1107:**
```dart
// BEFORE:
newTier = PremiumTier.universe; // Updated to new universe tier

// AFTER:
newTier = PremiumTier.stellar; // Universe removed, highest tier is now stellar
```

---

## 🔥 FIX #3: Remove SubscriptionType.lifetime (5 minutes)

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/subscription_service.dart`

**Location:** Line 694

**BEFORE:**
```dart
if (isLifetime) return subscriptionPrices[SubscriptionType.lifetime] ?? 0.0;
```

**AFTER:**
```dart
// Lifetime subscription removed - return stellar tier price instead
if (isLifetime) return subscriptionPrices[SubscriptionType.cosmicVip] ?? 19.99;
```

**Location:** Line 1276

**BEFORE:**
```dart
case SubscriptionType.lifetime:
  // some logic here
```

**AFTER:**
```dart
case SubscriptionType.cosmicVip: // Lifetime removed, map to highest subscription
  // same logic here
```

---

## 🔧 FIX #4: Update revenuecat_service.dart (15 minutes)

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/revenuecat_service.dart`

### Line 158:
```dart
// BEFORE:
newTier = PremiumTier.universe;

// AFTER:
newTier = PremiumTier.stellar; // Universe tier removed
```

### Line 184:
```dart
// BEFORE:
return PremiumTier.universe;

// AFTER:
return PremiumTier.stellar; // Universe tier removed
```

### Line 211:
```dart
// BEFORE:
if (currentTier == PremiumTier.universe) {

// AFTER:
if (currentTier == PremiumTier.stellar) { // Universe tier removed
```

### Line 371:
```dart
// BEFORE:
case PremiumTier.universe:
  return 'Universe Tier'; // or whatever logic

// AFTER:
case PremiumTier.stellar:
  return 'Stellar Tier'; // Universe tier removed
```

### Line 410:
```dart
// BEFORE:
'isLifetime': currentTier == PremiumTier.universe,

// AFTER:
'isLifetime': false, // Lifetime tier removed from system
```

---

## 🔧 FIX #5: Update premium_tier_system.dart (10 minutes)

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/services/premium_tier_system.dart`

### Line 73:
```dart
// BEFORE:
return _currentTier.level >= PremiumTier.universe.level;

// AFTER:
return _currentTier.level >= PremiumTier.stellar.level; // Universe removed
```

### Line 87:
```dart
// BEFORE:
return PremiumTier.universe;

// AFTER:
return PremiumTier.stellar; // Universe removed
```

### Line 112:
```dart
// BEFORE:
case PremiumTier.universe:
  // some logic

// AFTER:
case PremiumTier.stellar: // Universe removed, merge with stellar logic
  // same logic or enhanced
```

---

## ⚡ FIX #6: Switch Statement Pattern (Use for all remaining files)

**Pattern:** Replace all switch case statements

**BEFORE:**
```dart
switch (tier) {
  case PremiumTier.free:
    return something;
  case PremiumTier.cosmic:
    return somethingElse;
  case PremiumTier.stellar:
    return anotherThing;
  case PremiumTier.universe: // ❌ ERROR
    return universeStuff;
}
```

**AFTER Option 1** (Merge with stellar):
```dart
switch (tier) {
  case PremiumTier.free:
    return something;
  case PremiumTier.cosmic:
    return somethingElse;
  case PremiumTier.stellar:
    return anotherThing; // Universe features now part of stellar
  // Universe case removed
}
```

**AFTER Option 2** (Just remove):
```dart
switch (tier) {
  case PremiumTier.free:
    return something;
  case PremiumTier.cosmic:
    return somethingElse;
  case PremiumTier.stellar:
    return anotherThing;
  default:
    return anotherThing; // Fallback for any unknown tiers
}
```

---

## ⚡ FIX #7: Map/Dictionary Pattern

**BEFORE:**
```dart
final Map<PremiumTier, double> values = {
  PremiumTier.free: 0.0,
  PremiumTier.cosmic: 0.25,
  PremiumTier.stellar: 0.45,
  PremiumTier.universe: 0.55, // ❌ ERROR
};
```

**AFTER:**
```dart
final Map<PremiumTier, double> values = {
  PremiumTier.free: 0.0,
  PremiumTier.cosmic: 0.25,
  PremiumTier.stellar: 0.55, // Universe value merged into stellar
};
```

---

## ⚡ FIX #8: Equality Comparison Pattern

**BEFORE:**
```dart
if (currentTier == PremiumTier.universe) {
  // special universe logic
}
```

**AFTER Option 1** (Change to stellar):
```dart
if (currentTier == PremiumTier.stellar) {
  // universe features now in stellar
}
```

**AFTER Option 2** (Remove entirely):
```dart
// Universe check removed - feature no longer exists
```

---

## 🗑️ DEPRECATION FIX: premium_screen_legacy.dart

**File:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/legacy/premium_screen_legacy.dart`

**Option 1:** Add deprecation notice at top of file:
```dart
// @deprecated This legacy premium screen is no longer maintained
// Use premium_screen.dart instead
// Universe tier has been removed - this file should not be used
@Deprecated('Use premium_screen.dart instead')
class PremiumScreenLegacy extends StatefulWidget {
  // existing code
}
```

**Option 2:** Delete entire file if not used:
```bash
# Check if file is imported anywhere
grep -r "premium_screen_legacy" /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib --include="*.dart"

# If no imports found, delete it:
# rm /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/legacy/premium_screen_legacy.dart
```

---

## 📋 Complete File List with Fix Strategy

### Critical (Fix Immediately):
1. ✅ subscription_service.dart - Add variables, fix test mode, fix lifetime refs
2. ✅ revenuecat_service.dart - Replace all universe with stellar
3. ✅ premium_tier_system.dart - Replace universe with stellar

### Legacy (Deprecate or Quick Fix):
4. 🗑️ premium_screen_legacy.dart - 13 errors - **DEPRECATE**
5. 🗑️ quantum_payment_engine.dart - 1 error - **DEPRECATE**
6. 🗑️ revenue_math_engine.dart - 4 errors - **DEPRECATE**
7. 🗑️ advanced_monetization_tactics.dart - 7 errors - **DEPRECATE**

### Support (Quick Fixes):
8. ⚡ debug_premium_panel.dart - Line 497 - Replace return value
9. ⚡ mock_revenuecat_service.dart - Lines 56, 264, 284 - Replace universe
10. ⚡ logging/premium_logging_framework.dart - Lines 881, 885 - Add cases or remove

### UI/Features (Medium Priority):
11. 🔧 goal_planner_home_screen.dart - Line 103 - Change comparison
12. 🔧 device_performance_adapter.dart - Lines 102, 103, 129, 316, 327 - Update maps
13. 🔧 accessibility files - Update theme mappings
14. 🔧 ai_memory_manager.dart - Update switch cases
15. 🔧 premium_service_factory.dart - Update factory cases
16. 🔧 premium_tier_service.dart - Update switch case

---

## ⏱️ Time Estimates by File

| File | Errors | Time | Priority |
|------|--------|------|----------|
| subscription_service.dart | 14 | 15 min | 🔥 HIGH |
| revenuecat_service.dart | 5 | 10 min | 🔥 HIGH |
| premium_tier_system.dart | 3 | 5 min | 🔥 HIGH |
| premium_screen_legacy.dart | 13 | 2 min | 🗑️ DEPRECATE |
| revenue_math_engine.dart | 4 | 2 min | 🗑️ DEPRECATE |
| advanced_monetization_tactics.dart | 7 | 2 min | 🗑️ DEPRECATE |
| quantum_payment_engine.dart | 1 | 1 min | 🗑️ DEPRECATE |
| All other files | 30 | 30 min | ⚡ LOW |

**TOTAL: ~1 hour for all fixes** (excluding deprecations)

---

## 🚀 Fastest Path to Success

1. **5 minutes:** Define `_monthlyPremium` and `_lifetimePremium` constants
2. **10 minutes:** Fix test mode and lifetime refs in subscription_service.dart
3. **10 minutes:** Fix revenuecat_service.dart (5 occurrences)
4. **5 minutes:** Fix premium_tier_system.dart (3 occurrences)
5. **2 minutes:** Add @Deprecated to legacy files
6. **30 minutes:** Fix remaining support files

**Total: 62 minutes to resolve all 77 errors**

---

Generated: November 20, 2025
Ready for implementation
