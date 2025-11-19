# Logging Best Practices - Zodiac App
## Quick Reference Guide for Developers

**Status:** ✅ ALREADY IMPLEMENTED - This guide documents current practices

---

## Current Logging Infrastructure

### 1. AppLogger (Primary Logging Service)

**Location:** `lib/utils/app_logger.dart`

#### Usage Examples:

```dart
import 'package:zodiac_app/utils/app_logger.dart';
import 'package:flutter/foundation.dart';

// ✅ DEBUG logging (development only)
if (kDebugMode) {
  AppLogger.debug('Debug message: $variable');
}

// ✅ INFO logging
AppLogger.info('Operation completed successfully');

// ✅ WARNING logging
AppLogger.warning('Potential issue detected', error);

// ✅ ERROR logging (with Crashlytics in production)
AppLogger.error('Error occurred', error, stackTrace);

// ✅ PERFORMANCE logging
final stopwatch = Stopwatch()..start();
// ... operation ...
stopwatch.stop();
AppLogger.performance('operation_name', stopwatch.elapsedMilliseconds);
```

### 2. SecureLoggingService (Security-Sensitive Operations)

**Location:** `lib/services/logging/secure_logging_service.dart`

#### Usage Examples:

```dart
import 'package:zodiac_app/services/logging/secure_logging_service.dart';

// ✅ Secure logging (PII sanitization)
SecureLoggingService.logSecureInfo(
  'User operation completed',
  metadata: {'user_id': userId},
);

// ✅ Secure error logging
SecureLoggingService.logSecureError(
  'Authentication failed',
  error: error,
);
```

### 3. Domain-Specific Logging Functions

**Location:** Various service files (e.g., `certificate_pinning_service.dart`)

```dart
// ✅ Domain-specific logging
logDebug('Debug information');
logInfo('Information message');
logWarning('Warning message', error: error);
logError('Error occurred', error: error);
```

---

## What NOT to Do

### ❌ NEVER use print() in production code

```dart
// ❌ BAD - Console spam, not production-safe
print('Debug info: $data');

// ✅ GOOD - Proper logging with automatic production safety
if (kDebugMode) {
  AppLogger.debug('Debug info: $data');
}
```

### ❌ NEVER log without debug guards in production

```dart
// ❌ BAD - Will log in production
AppLogger.debug('Debug info');

// ✅ GOOD - Only logs in debug mode
if (kDebugMode) {
  AppLogger.debug('Debug info');
}
```

### ❌ NEVER log sensitive information

```dart
// ❌ BAD - Leaks PII
AppLogger.debug('User email: ${user.email}');

// ✅ GOOD - Use SecureLoggingService (auto-sanitizes)
SecureLoggingService.logSecureInfo(
  'User operation',
  metadata: {'user_id': user.id}, // ID only, no email
);
```

---

## Decision Tree: Which Logger to Use?

```
Is this debug-only information?
├─ YES → Use AppLogger.debug() with kDebugMode guard
└─ NO ↓

Does it contain sensitive user data?
├─ YES → Use SecureLoggingService
└─ NO ↓

Is this an error?
├─ YES → Use AppLogger.error() (auto-reports to Crashlytics)
└─ NO ↓

Is this a warning?
├─ YES → Use AppLogger.warning()
└─ NO ↓

Is this performance monitoring?
├─ YES → Use AppLogger.performance()
└─ NO ↓

General information → Use AppLogger.info()
```

---

## File-Specific Guidelines

### Debug Files (lib/debug/*)
```dart
// ✅ Use AppLogger or debugPrint with kDebugMode
if (kDebugMode) {
  debugPrint('Debug panel info');
}
// or
AppLogger.debug('Debug diagnostics');
```

### Test Files (test_*.dart, *_test.dart)
```dart
// ✅ debugPrint is acceptable in test files
if (kDebugMode) {
  debugPrint('Test output');
}
```

### Production Services (lib/services/*)
```dart
// ✅ Always use AppLogger
AppLogger.error('Service error', error, stackTrace);
```

### Production Providers (lib/providers/*)
```dart
// ✅ Debug info with guards
if (kDebugMode) {
  AppLogger.debug('Provider state: $state');
}
```

---

## Log Levels Explained

### DEBUG (Development Only)
- **When:** Detailed debugging information
- **Production:** Automatically disabled
- **Example:** Variable values, method calls, state changes

### INFO
- **When:** General informational messages
- **Production:** Enabled (but minimal)
- **Example:** Operation completed, service initialized

### WARNING
- **When:** Potential issues that don't prevent operation
- **Production:** Enabled
- **Example:** Deprecated API usage, fallback activated

### ERROR
- **When:** Errors that should be tracked and fixed
- **Production:** Enabled + sent to Crashlytics
- **Example:** API failures, exceptions, critical issues

### PERFORMANCE
- **When:** Timing and performance metrics
- **Production:** Disabled (debug only)
- **Example:** Operation duration, slow operations

---

## Production Safety Checklist

Before deploying:

- [ ] No `print()` statements in lib/ directory
- [ ] All `AppLogger.debug()` calls wrapped in `if (kDebugMode)`
- [ ] Sensitive data logged via SecureLoggingService
- [ ] Error logging includes proper error and stackTrace
- [ ] Flutter analyze shows 0 avoid_print warnings

Current Status: ✅ ALL CHECKS PASS

---

## Code Examples from Zodiac App

### Example 1: Premium Provider (lib/providers/premium_provider.dart)

```dart
/// Track feature usage
void trackFeatureUsage(PremiumFeature feature) async {
  try {
    await _analytics.trackPremiumFeatureUsage(
      feature: feature,
      userId: 'current_user',
      context: {/* ... */},
    );
  } catch (e) {
    // ✅ Proper debug logging with guard
    if (kDebugMode) AppLogger.debug('Error tracking feature view: $e');
  }
}
```

### Example 2: Launch Optimization Service

```dart
Future<void> initialize() async {
  try {
    await _conductMarketResearch();
    await _analyzeCompetitors();
    
    // ✅ Proper debug logging with guard
    if (kDebugMode) {
      AppLogger.debug('✅ Launch Optimization Service initialized');
    }
  } catch (e) {
    // ✅ Proper debug logging with guard
    if (kDebugMode) {
      AppLogger.debug('Error initializing launch service: $e');
    }
  }
}
```

### Example 3: Certificate Pinning Service

```dart
Future<void> initialize() async {
  if (_initialized) return;

  try {
    _secureHttpClient = Dio();
    _secureHttpClient.interceptors.add(/* ... */);
    _configureSecureClient();
    _initialized = true;
    
    // ✅ Proper logging function
    logInfo('Certificate pinning service initialized');
  } catch (e) {
    // ✅ Proper error logging
    logError('Error occurred', error: e);
    _initializeFallbackClient();
  }
}
```

### Example 4: User Authentication Service

```dart
Future<void> initialize() async {
  try {
    await _apiService.initialize();
    await _secureStorage.initialize();
    await _restoreSession();
    
    // ✅ Proper secure logging
    SecureLoggingService.logSecureInfo(
      'User Authentication Service initialized',
      metadata: {
        'auth_state': _authState.name,
        'has_user': _currentUser != null,
      },
    );
  } catch (e) {
    // ✅ Proper secure error logging
    SecureLoggingService.logSecureError(
      'Failed to initialize User Authentication Service',
      error: e,
    );
  }
}
```

---

## Testing Your Logging

### Manual Testing:
1. Run app in debug mode → Should see debug logs
2. Build release version → Should see NO debug logs
3. Trigger error → Should appear in Crashlytics

### Automated Testing:
```bash
# Check for print statements
grep -r "print(" lib/ --include="*.dart"
# Expected: 0 results (or only in comments)

# Check for avoid_print warnings
flutter analyze | grep -i "avoid_print"
# Expected: 0 warnings

# Verify AppLogger usage
grep -r "AppLogger\." lib/ --include="*.dart" | wc -l
# Expected: High number (100+)
```

---

## Quick Commands

```bash
# Check print statement count
grep -r "^\s*print(" lib/ --include="*.dart" | wc -l

# Count AppLogger usage
grep -r "AppLogger\." lib/ --include="*.dart" | wc -l

# Count kDebugMode guards
grep -r "if (kDebugMode)" lib/ --include="*.dart" | wc -l

# Run flutter analyze
flutter analyze | grep -i "avoid_print"
```

---

## References

- **AppLogger Implementation:** `lib/utils/app_logger.dart`
- **SecureLoggingService:** `lib/services/logging/secure_logging_service.dart`
- **Debug Tools:** `lib/debug/`
- **Current Status:** See `PRINT_CLEANUP_REPORT.md`

---

**Document Version:** 1.0
**Last Updated:** October 13, 2025
**Status:** ✅ Current practices documented
**Compliance:** 100% across codebase
