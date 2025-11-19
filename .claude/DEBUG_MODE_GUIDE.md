# 🔧 DEBUG MODE - TESTING GUIDE

**Date**: October 7, 2025
**Purpose**: Guide for testing premium features without subscription

---

## ✅ CHANGES MADE

### 1. Removed Test Picker Button

**Location**: `lib/screens/home_screen.dart`

**Changes**:
- ❌ Removed `FloatingActionButton` with "Test Pickers" label
- ❌ Removed from both error state and normal state

**Before**:
```dart
floatingActionButton: FloatingActionButton.extended(
  onPressed: () => Navigator.pushNamed(context, '/cosmic-pickers-demo'),
  icon: const Icon(Icons.auto_awesome),
  label: const Text('Test Pickers'),
  backgroundColor: const Color(0xFF3A86FF),
  foregroundColor: Colors.white,
),
```

**After**: Removed completely ✅

---

### 2. Created Debug Configuration System

**New File**: `lib/config/debug_config.dart`

**Features**:
- ✅ `bypassPremiumGate` - Access all premium features in debug mode
- ✅ `enableTestMode` - Enable test mode features
- ✅ `showPerformanceOverlay` - Display FPS counter
- ✅ `enableUITestHelpers` - Show layout boundaries
- ✅ `logNavigation` - Log all route changes
- ✅ `autoReloadContent` - Auto-refresh horoscopes
- ✅ `useTestPayments` - Use sandbox RevenueCat
- ✅ `forceLanguage` - Force specific language for testing
- ✅ `showHiddenFeatures` - Display features in development
- ✅ `simulateSubscriptionTier` - Simulate different tiers

**Key Configuration**:
```dart
class DebugConfig {
  /// 🔓 Bypass premium features for testing
  /// ⚠️ MUST BE FALSE IN PRODUCTION
  static const bool bypassPremiumGate = kDebugMode && true;

  /// 🧪 Enable test mode
  static const bool enableTestMode = kDebugMode && true;

  // ... other flags
}
```

**Safety Features**:
- ✅ All flags automatically FALSE in release builds (`kDebugMode` check)
- ✅ `assertProductionSafety()` - Throws error if debug flags enabled in release
- ✅ `getDebugSummary()` - Print current debug configuration
- ✅ `hasDebugFlagsEnabled` - Check if any debug flag is active

---

### 3. Updated Premium Feature Gate

**File**: `lib/widgets/monetization/premium_feature_gate.dart`

**Changes**:
```dart
import 'package:zodiac_app/config/debug_config.dart';

@override
Widget build(BuildContext context, WidgetRef ref) {
  // 🔓 DEBUG: Bypass premium gate for testing
  if (DebugConfig.bypassPremiumGate) {
    return child; // Show premium content directly
  }

  // Normal premium check
  final subscriptionService = ref.read(subscriptionServiceProvider);
  final isPremium = subscriptionService.isPremium;

  if (isPremium) {
    return child;
  }

  // Show premium gate
  return fallback ?? _buildPremiumGate(context);
}
```

**Affected Widgets** (all inherit from `PremiumFeatureGate`):
- ✅ `PremiumAnalysisGate`
- ✅ `PremiumCosmicCoachGate`
- ✅ `PremiumHoroscopeGate`

---

### 4. Added Debug Indicator

**Location**: `lib/screens/home_screen.dart` - AppBar actions

**Visual Indicator**:
```dart
if (DebugConfig.bypassPremiumGate)
  Tooltip(
    message: 'Debug Mode: Premium Bypass Active',
    child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.orange.withOpacity(0.2),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.orange, width: 1),
      ),
      child: Row(
        children: [
          Icon(Icons.bug_report, color: Colors.orange, size: 16),
          Text('TEST', style: TextStyle(color: Colors.orange)),
        ],
      ),
    ),
  ),
```

**Appearance**:
- 🐛 Orange bug icon + "TEST" badge in AppBar
- Only visible when `bypassPremiumGate = true`
- Tooltip shows "Debug Mode: Premium Bypass Active"

---

## 🚀 HOW TO USE

### For Testing Premium Features

**Current State**: ✅ **ENABLED BY DEFAULT IN DEBUG MODE**

1. ✅ **Already configured** - `bypassPremiumGate = kDebugMode && true`
2. ✅ Run app in debug mode: `flutter run`
3. ✅ All premium features unlocked automatically
4. ✅ Orange "TEST" badge visible in AppBar

**What you can test**:
- ✅ Cosmic Coach (unlimited access)
- ✅ Premium Analysis Card
- ✅ Advanced Compatibility
- ✅ Detailed Horoscopes
- ✅ All premium-gated features

---

### To Disable Premium Bypass

**If you want to test the actual premium gates**:

**Option 1: Change config file**
```dart
// File: lib/config/debug_config.dart
static const bool bypassPremiumGate = kDebugMode && false; // Changed to false
```

**Option 2: Test in release mode**
```bash
flutter run --release
```
- All debug flags automatically disabled in release mode
- Tests actual production behavior

---

### To Enable Other Debug Features

**Edit** `lib/config/debug_config.dart`:

```dart
class DebugConfig {
  // Show FPS counter and memory usage
  static const bool showPerformanceOverlay = true;

  // Display layout boundaries
  static const bool enableUITestHelpers = true;

  // Force Spanish language
  static const String? forceLanguage = 'es';

  // Simulate Cosmic tier subscription
  static const String? simulateSubscriptionTier = 'cosmic';
}
```

---

### Print Debug Summary

Add this to your app initialization:

```dart
// File: lib/main.dart
void main() {
  // Print debug configuration
  if (kDebugMode) {
    print(DebugConfig.getDebugSummary());
  }

  // Verify production safety
  DebugConfig.assertProductionSafety();

  runApp(MyApp());
}
```

**Output**:
```
🔧 DEBUG CONFIG STATUS:
━━━━━━━━━━━━━━━━━━━━━
Mode: DEBUG
Premium Bypass: ✅ ENABLED
Test Mode: ✅ ENABLED
Performance Overlay: ❌ OFF
UI Test Helpers: ❌ OFF
Navigation Logs: ✅ ON
Auto-reload Content: ❌ OFF
Test Payments: ✅ ON
Force Language: System
Hidden Features: ✅ VISIBLE
Simulate Tier: Actual subscription
━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚨 BEFORE PRODUCTION BUILD

### ⚠️ CRITICAL: Verify Debug Flags Are Disabled

**Automatic Safety**:
- ✅ All flags use `kDebugMode` check - automatically FALSE in release
- ✅ `assertProductionSafety()` throws error if any flag is TRUE in release

**Manual Verification**:
```bash
# 1. Check current config
grep "bypassPremiumGate" lib/config/debug_config.dart

# 2. Build release and test
flutter run --release

# 3. If any debug flags appear, build will fail (as designed)
```

**Expected in Release Mode**:
- ❌ No "TEST" badge in AppBar
- ❌ No premium bypass
- ❌ No debug logs
- ❌ No performance overlay
- ✅ Normal premium gates working

---

## 📋 TESTING CHECKLIST

### Before Testing Premium Features

- [ ] Verify debug mode: `flutter run` (not `flutter run --release`)
- [ ] Check for orange "TEST" badge in AppBar
- [ ] Try accessing Cosmic Coach → Should work without subscription
- [ ] Try accessing Premium Analysis → Should show content
- [ ] Check logs for "DEBUG: Premium Bypass Active"

### Testing Actual Premium Gates

- [ ] Set `bypassPremiumGate = false` in `debug_config.dart`
- [ ] Hot reload app
- [ ] Verify "TEST" badge disappears
- [ ] Try accessing Cosmic Coach → Should show upgrade prompt
- [ ] Purchase test subscription → Premium should unlock

### Before App Store Submission

- [ ] Build release: `flutter build ios --release`
- [ ] Verify no "TEST" badge appears
- [ ] Verify premium gates work correctly
- [ ] Test actual purchase flow
- [ ] Verify no debug logs in console
- [ ] Run `assertProductionSafety()` check

---

## 🎯 COMMON SCENARIOS

### Scenario 1: Testing Premium Features Daily
**Solution**: Leave `bypassPremiumGate = true` in `debug_config.dart`
- Always enabled in debug mode
- Automatically disabled in release builds

### Scenario 2: Testing Purchase Flow
**Solution**: Temporarily set `bypassPremiumGate = false`
- Test actual premium gates
- Test RevenueCat integration
- Change back to `true` after testing

### Scenario 3: Testing Specific Language
**Solution**: Set `forceLanguage = 'es'` in `debug_config.dart`
- Forces Spanish regardless of system language
- Test translations without changing device settings

### Scenario 4: Performance Testing
**Solution**: Enable `showPerformanceOverlay = true`
- See FPS counter
- Monitor memory usage
- Identify performance bottlenecks

---

## 🔍 DEBUG INDICATORS

When debug mode is active, you'll see:

**Visual Indicators**:
- 🐛 Orange "TEST" badge in AppBar (when premium bypass active)
- 🎨 Layout boundaries (if `enableUITestHelpers = true`)
- 📊 FPS counter (if `showPerformanceOverlay = true`)

**Console Logs**:
```
[DEBUG] Premium bypass active - showing premium content
[DEBUG] Navigation: /home → /cosmic-coach
[DEBUG] RevenueCat: Using sandbox environment
```

**Behavior Changes**:
- ✅ All premium features accessible
- ✅ No upgrade prompts
- ✅ Unlimited Cosmic Coach usage
- ✅ All advanced features unlocked

---

## 📚 FILES MODIFIED

1. ✅ `lib/screens/home_screen.dart`
   - Removed test picker button
   - Added debug indicator badge
   - Imported debug config

2. ✅ `lib/widgets/monetization/premium_feature_gate.dart`
   - Added premium bypass check
   - Imported debug config

3. ✅ `lib/config/debug_config.dart` (NEW)
   - Debug configuration system
   - Safety checks
   - Production verification

4. ✅ `.claude/DEBUG_MODE_GUIDE.md` (NEW)
   - This documentation file

---

## ⚡ QUICK REFERENCE

### Enable Premium Testing
```dart
// lib/config/debug_config.dart
static const bool bypassPremiumGate = kDebugMode && true; ✅
```

### Disable Premium Testing
```dart
// lib/config/debug_config.dart
static const bool bypassPremiumGate = kDebugMode && false; ❌
```

### Test Production Behavior
```bash
flutter run --release
```

### Check Debug Status
```dart
print(DebugConfig.getDebugSummary());
```

---

**Summary**:
✅ Test picker removed
✅ Premium bypass system implemented
✅ Debug indicators added
✅ Production safety guaranteed
✅ Full testing capability enabled

**Status**: ✅ **READY FOR TESTING**
