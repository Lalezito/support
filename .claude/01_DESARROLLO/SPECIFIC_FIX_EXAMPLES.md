# 🔧 SPECIFIC FIX EXAMPLES
## Critical Flutter Error Fixes with Before/After Code

### 1. NON-EXHAUSTIVE SWITCH STATEMENT FIX

**File:** `test/premium/ai_memory_test.dart:30`

**❌ BROKEN CODE (Missing PremiumTier.essential case):**
```dart
switch (_currentTier) {
  case PremiumTier.free:
    _currentMemoryUsage = 25 * 1024 * 1024; // 25MB
    break;
  case PremiumTier.cosmic:
    _currentMemoryUsage = 45 * 1024 * 1024; // 45MB
    break;
  case PremiumTier.stellar:
    _currentMemoryUsage = 120 * 1024 * 1024; // 120MB
    break;
  case PremiumTier.universe:
    _currentMemoryUsage = 200 * 1024 * 1024; // 200MB
    break;
  // Missing PremiumTier.essential case!
  // Missing deprecated aliases!
}
```

**✅ FIXED CODE (Complete switch with all cases):**
```dart
switch (_currentTier) {
  case PremiumTier.free:
    _currentMemoryUsage = 25 * 1024 * 1024; // 25MB
    break;
  case PremiumTier.cosmic:
  case PremiumTier.essential:  // Handle deprecated alias
    _currentMemoryUsage = 45 * 1024 * 1024; // 45MB
    break;
  case PremiumTier.stellar:
  case PremiumTier.advanced:   // Handle deprecated aliases
  case PremiumTier.master:
  case PremiumTier.cosmicVip:
    _currentMemoryUsage = 120 * 1024 * 1024; // 120MB
    break;
  case PremiumTier.universe:
  case PremiumTier.lifetime:   // Handle deprecated alias
    _currentMemoryUsage = 200 * 1024 * 1024; // 200MB
    break;
  case PremiumTier.hrProfessional:      // B2B tiers
  case PremiumTier.enterpriseSuite:     // map to stellar
  case PremiumTier.consultingPlatform:
    _currentMemoryUsage = 120 * 1024 * 1024; // Same as stellar
    break;
}
```

### 2. DUPLICATE SWITCH CASES FIX

**File:** `test/premium/ai_memory_test.dart:44-61`

**❌ BROKEN CODE (Unreachable duplicate cases):**
```dart
switch (_currentTier) {
  case PremiumTier.cosmic:
    _currentMemoryUsage = 45 * 1024 * 1024; // 45MB
    break;
  case PremiumTier.cosmic:  // DUPLICATE! Unreachable
    _currentMemoryUsage = 45 * 1024 * 1024; // 45MB
    break;
  case PremiumTier.stellar:
    _currentMemoryUsage = 75 * 1024 * 1024; // 75MB
    break;
  case PremiumTier.stellar:  // DUPLICATE! Unreachable
    _currentMemoryUsage = 120 * 1024 * 1024; // 120MB
    break;
  case PremiumTier.stellar:  // DUPLICATE! Unreachable
    _currentMemoryUsage = 180 * 1024 * 1024; // 180MB
    break;
}
```

**✅ FIXED CODE (Single cases with proper handling):**
```dart
switch (_currentTier) {
  case PremiumTier.cosmic:
  case PremiumTier.essential:
    _currentMemoryUsage = 45 * 1024 * 1024; // 45MB
    break;
  case PremiumTier.stellar:
  case PremiumTier.advanced:
  case PremiumTier.master:
  case PremiumTier.cosmicVip:
    _currentMemoryUsage = 120 * 1024 * 1024; // 120MB (unified value)
    break;
  case PremiumTier.universe:
  case PremiumTier.lifetime:
    _currentMemoryUsage = 200 * 1024 * 1024; // 200MB
    break;
}
```

### 3. UNDEFINED CLASS/IMPORT FIX

**File:** `lib/widgets/conversion_optimized_paywall.dart`

**❌ BROKEN CODE (Missing import):**
```dart
// Missing import!
class ConversionOptimizedPaywall extends StatefulWidget {
  final PremiumTier? recommendedTier;  // ❌ Undefined class 'PremiumTier'

  const ConversionOptimizedPaywall({
    Key? key,
    this.recommendedTier = PremiumTier.cosmic,  // ❌ Undefined name 'PremiumTier'
  }) : super(key: key);
}
```

**✅ FIXED CODE (With proper import):**
```dart
import '../models/subscription_tier.dart';  // ✅ Add this import

class ConversionOptimizedPaywall extends StatefulWidget {
  final PremiumTier? recommendedTier;  // ✅ Now defined

  const ConversionOptimizedPaywall({
    Key? key,
    this.recommendedTier = PremiumTier.cosmic,  // ✅ Now works
  }) : super(key: key);
}
```

### 4. REFERRAL SERVICE MISSING MEMBERS FIX

**File:** `lib/services/referral_service.dart`

**❌ BROKEN CODE (Missing class members):**
```dart
class ReferralService {
  // Missing all these members!

  Future<String> generateReferralCode() async {
    if (!_isInitialized) {  // ❌ Undefined name '_isInitialized'
      throw StateError('Service not initialized');
    }

    _referralCodes[_userId] = code;  // ❌ Undefined names
    await _prefs.setStringList(_referralCodesKey, codes);  // ❌ Undefined names

    return _userReferralCode;  // ❌ Undefined name
  }
}
```

**✅ FIXED CODE (With all required members):**
```dart
import 'package:shared_preferences/shared_preferences.dart';

class ReferralService {
  // ✅ Add all missing members
  late SharedPreferences _prefs;
  late String _userId;
  late String _userReferralCode;
  Map<String, dynamic> _referralCodes = {};
  List<Map<String, dynamic>> _referralEvents = [];
  Map<String, dynamic> _activeRewards = {};
  bool _isInitialized = false;

  static const String _referralCodesKey = 'referral_codes';
  static const String _referralEventsKey = 'referral_events';
  static const String _referralRewardsKey = 'referral_rewards';

  Future<String> generateReferralCode() async {
    if (!_isInitialized) {  // ✅ Now defined
      throw StateError('Service not initialized');
    }

    _referralCodes[_userId] = code;  // ✅ Now works
    await _prefs.setStringList(_referralCodesKey, codes);  // ✅ Now works

    return _userReferralCode;  // ✅ Now works
  }
}
```

### 5. SOCIAL SHARING UNDEFINED VARIABLES FIX

**File:** `lib/services/social_sharing_service.dart:431`

**❌ BROKEN CODE (Undefined variables):**
```dart
Future<String> shareHoroscope() async {
  final signName = translations.getSignName(sign);  // ❌ Undefined 'translations'
  final content = '${horoscope.content}';           // ❌ Undefined 'horoscope'

  return shareContent(content);
}
```

**✅ FIXED CODE (With proper context):**
```dart
Future<String> shareHoroscope(BuildContext context, HoroscopeData horoscope) async {
  final signName = context.translations.getSignName(sign);  // ✅ Use context
  final content = '${horoscope.content}';                   // ✅ Parameter passed

  return shareContent(content);
}
```

### 6. SYNTAX ERROR FIX

**File:** `lib/widgets/social_share_button.dart:583`

**❌ BROKEN CODE (Malformed syntax):**
```dart
final items = [
  'item1',
  'item2'[,  // ❌ Malformed array syntax
];
```

**✅ FIXED CODE (Corrected syntax):**
```dart
final items = [
  'item1',
  'item2',  // ✅ Proper comma placement
];
```

### 7. DUPLICATE MAP KEYS FIX

**File:** `test/business/business_logic_tests.dart:750`

**❌ BROKEN CODE (Duplicate keys):**
```dart
final testData = {
  'cosmic': cosmicFeatures,
  'cosmic': differentCosmicFeatures,  // ❌ Duplicate key!
  'stellar': stellarFeatures,
};
```

**✅ FIXED CODE (Unique keys):**
```dart
final testData = {
  'cosmic': cosmicFeatures,
  'cosmic_premium': differentCosmicFeatures,  // ✅ Unique key
  'stellar': stellarFeatures,
};
```

### 8. DEPRECATED ENUM USAGE FIX

**File:** `lib/core/device_performance_adapter.dart:99`

**❌ BROKEN CODE (Using deprecated enum):**
```dart
if (tier == PremiumTier.essential) {  // ❌ Deprecated
  return BasicPerformanceMode();
} else if (tier == PremiumTier.advanced) {  // ❌ Deprecated
  return AdvancedPerformanceMode();
}
```

**✅ FIXED CODE (Using new enum values):**
```dart
if (tier == PremiumTier.cosmic) {  // ✅ New enum value
  return BasicPerformanceMode();
} else if (tier == PremiumTier.stellar) {  // ✅ New enum value
  return AdvancedPerformanceMode();
}
```

### 9. PRINT STATEMENT REPLACEMENT

**❌ BROKEN CODE (Using print in production):**
```dart
void debugMemoryUsage() {
  print('Current memory: ${_currentMemoryUsage}');  // ❌ Don't use print
  print('Cleanup triggered: $_cleanupTriggered');   // ❌ in production
}
```

**✅ FIXED CODE (Using proper logging):**
```dart
import 'package:logging/logging.dart';

final _logger = Logger('AIMemoryManager');

void debugMemoryUsage() {
  _logger.info('Current memory: ${_currentMemoryUsage}');  // ✅ Proper logging
  _logger.info('Cleanup triggered: $_cleanupTriggered');   // ✅ Configurable
}
```

## 🚀 EXECUTION ORDER FOR FIXES

1. **Fix critical compilation errors first:**
   ```bash
   ./fix_critical_errors.sh
   flutter analyze  # Should show 0 errors
   ```

2. **Migrate deprecated enums:**
   ```bash
   ./fix_deprecated_enums.sh
   flutter analyze  # Should show no deprecated warnings
   ```

3. **Improve code quality:**
   ```bash
   ./fix_code_quality.sh
   flutter analyze  # Should show minimal warnings
   ```

4. **Verify build works:**
   ```bash
   flutter build apk --debug
   flutter test
   ```

These specific examples show exactly what needs to be fixed and how to fix it systematically across the entire codebase.