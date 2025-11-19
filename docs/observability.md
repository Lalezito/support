# Observability & Monitoring Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: ✅ Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Analytics System](#analytics-system)
3. [Logging System](#logging-system)
4. [Performance Monitoring](#performance-monitoring)
5. [Event Catalog](#event-catalog)
6. [Privacy & Compliance](#privacy--compliance)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The Zodiac Life Coach observability system provides comprehensive insight into app performance, user behavior, and business metrics through three main pillars:

1. **Analytics**: User behavior and business intelligence
2. **Logging**: Debugging and error tracking
3. **Performance Monitoring**: App health and optimization

---

## Analytics System

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Application Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │   Screens   │  │   Services  │  │   Providers  │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│              CoreAnalyticsService                        │
│  - Event validation                                      │
│  - PII protection                                        │
│  - Event batching                                        │
│  - Retry logic                                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Firebase Analytics                          │
│  - Event storage                                         │
│  - Funnel analysis                                       │
│  - Audience building                                     │
│  - BigQuery export                                       │
└─────────────────────────────────────────────────────────┘
```

---

### CoreAnalyticsService API

#### `logEvent()`

Logs an analytics event with optional parameters.

```dart
Future<void> logEvent(
  String name,
  [Map<String, dynamic>? parameters]
)
```

**Parameters**:
- `name` (String): Event name (max 40 chars, alphanumeric + underscore)
- `parameters` (Map?, optional): Event parameters (max 25, max 100 chars per value)

**Example**:
```dart
final analytics = CoreAnalyticsService();

await analytics.logEvent('purchase_completed', {
  'tier': 'essential',
  'revenue': 4.99,
  'currency': 'USD',
  'transaction_id': 'txn_123456',
});
```

---

#### `setUserId()`

Sets the user ID for analytics.

```dart
Future<void> setUserId(String userId)
```

**Note**: User ID is automatically hashed for privacy.

**Example**:
```dart
await analytics.setUserId('user_abc123');
// Stored as hashed ID: '7f8a9b2c...'
```

---

#### `setUserProperty()`

Sets a user property for segmentation.

```dart
Future<void> setUserProperty(String name, String value)
```

**Example**:
```dart
await analytics.setUserProperty('zodiac_sign', 'Aries');
await analytics.setUserProperty('subscription_tier', 'essential');
```

---

### Event Categories

#### 1. User Journey Events

Track user progression through the app:

```dart
// App lifecycle
await analytics.logEvent('app_opened');
await analytics.logEvent('app_closed', {
  'session_duration': sessionDuration.inSeconds,
});

// Onboarding
await analytics.logEvent('onboarding_started');
await analytics.logEvent('onboarding_step_completed', {
  'step': stepNumber,
  'step_name': stepName,
});
await analytics.logEvent('onboarding_completed', {
  'total_time': duration.inSeconds,
});

// Birth data
await analytics.logEvent('birth_data_entered', {
  'has_birth_time': birthTime != null,
  'has_location': location != null,
});
```

---

#### 2. Monetization Events (CRITICAL)

Revenue-critical events that must be tracked:

```dart
// Paywall
await analytics.logEvent('paywall_shown', {
  'tier': tier.name,
  'context': context, // e.g., 'feature_limit', 'upgrade_prompt'
  'trigger': trigger, // e.g., 'ai_coach_locked'
});

// Purchase flow
await analytics.logEvent('purchase_initiated', {
  'tier': tier.name,
  'price': price,
  'currency': 'USD',
  'from_trial': isTrialUser,
});

await analytics.logEvent('purchase_completed', {
  'tier': tier.name,
  'revenue': price,
  'transaction_id': transactionId,
  'is_upgrade': isUpgrade,
  'previous_tier': previousTier?.name,
});

await analytics.logEvent('purchase_failed', {
  'tier': tier.name,
  'error': errorMessage,
  'error_code': errorCode,
});

// Trial
await analytics.logEvent('trial_started', {
  'duration_days': 7,
  'trigger': trigger,
});

await analytics.logEvent('trial_converted', {
  'target_tier': tier.name,
  'conversion_day': dayNumber, // 1-7
  'trial_duration_used': daysUsed,
});

// Subscription management
await analytics.logEvent('subscription_cancelled', {
  'tier': tier.name,
  'reason': cancellationReason,
  'lifetime_value': lifetimeValue,
  'days_subscribed': daysSubscribed,
});
```

---

#### 3. Feature Usage Events

Track how users interact with features:

```dart
// Horoscope
await analytics.logEvent('horoscope_viewed', {
  'type': 'daily', // or 'weekly', 'monthly'
  'sign': zodiacSign,
  'source': 'home', // or 'notification', 'tab'
});

// Compatibility
await analytics.logEvent('compatibility_analyzed', {
  'sign1': sign1,
  'sign2': sign2,
  'compatibility_score': score,
  'relationship_type': type, // 'romantic', 'friendship', 'business'
});

// AI Coach
await analytics.logEvent('coach_chat_started', {
  'user_tier': tier.name,
  'context': context,
});

await analytics.logEvent('coach_message_sent', {
  'message_length': message.length,
  'topic': detectedTopic,
});

// Journaling
await analytics.logEvent('journal_entry_created', {
  'word_count': wordCount,
  'has_mood': mood != null,
  'emotional_tags': emotionalTags,
});
```

---

#### 4. Performance Metrics

Track app performance:

```dart
// API calls
await analytics.logEvent('api_call_completed', {
  'endpoint': endpoint,
  'duration_ms': duration.inMilliseconds,
  'success': success,
  'status_code': statusCode,
});

// Cache performance
await analytics.logEvent('cache_hit', {
  'service': serviceName,
  'cache_key': key,
});

// Screen performance
await analytics.logEvent('screen_load_time', {
  'screen': screenName,
  'duration_ms': loadTime.inMilliseconds,
  'widgets_rendered': widgetCount,
});
```

---

### Event Naming Convention

**Format**: `{category}_{action}_{object}`

**Examples**:
```
purchase_completed_essential
horoscope_viewed_daily
coach_chat_started_main
notification_opened_prediction
```

**Categories**:
- `app_*` - App lifecycle
- `purchase_*` - Monetization
- `trial_*` - Trial management
- `horoscope_*` - Horoscope features
- `coach_*` - AI Coach
- `journal_*` - Journaling
- `notification_*` - Notifications
- `error_*` - Errors

---

## Logging System

### Log Levels

| Level | Value | When to Use | Production |
|-------|-------|-------------|------------|
| DEBUG | 0 | Development debugging | ❌ Hidden |
| INFO | 1 | Important events | ✅ Shown |
| WARNING | 2 | Potential issues | ✅ Shown |
| ERROR | 3 | Recoverable errors | ✅ Shown |
| CRITICAL | 4 | App-breaking errors | ✅ Shown + Crashlytics |

---

### SecureLoggingService API

#### `debug()`

Log debugging information (development only).

```dart
void debug(String message, {Map<String, dynamic>? context})
```

**Example**:
```dart
logger.debug('Fetching horoscope', context: {
  'sign': sign,
  'user_id': SafeDataLogger.safeUserId(userId),
});
```

---

#### `info()`

Log important events.

```dart
void info(String message, {Map<String, dynamic>? context})
```

**Example**:
```dart
logger.info('Purchase completed', context: {
  'tier': tier.name,
  'revenue': tier.price,
});
```

---

#### `warning()`

Log warnings about potential issues.

```dart
void warning(String message, {Map<String, dynamic>? context})
```

**Example**:
```dart
logger.warning('API response slow', context: {
  'endpoint': endpoint,
  'duration_ms': duration.inMilliseconds,
});
```

---

#### `error()`

Log recoverable errors.

```dart
void error(String message, {dynamic error, StackTrace? stackTrace})
```

**Example**:
```dart
try {
  await fetchData();
} catch (e, stack) {
  logger.error('Failed to fetch data', error: e, stackTrace: stack);
}
```

---

#### `critical()`

Log critical errors that may crash the app.

```dart
void critical(String message, {dynamic error, StackTrace? stackTrace})
```

**Example**:
```dart
logger.critical('Database corrupted', error: e, stackTrace: stack);
// Automatically sent to Firebase Crashlytics
```

---

### Sensitive Data Protection

**Never log**:
- Passwords
- API keys/tokens
- Credit card numbers
- Email addresses (use hashed versions)
- Phone numbers
- Precise GPS locations
- Full birth dates
- IP addresses

**Automatic sanitization**:
```dart
// ❌ Bad
logger.info('User login: email@example.com, password: secret123');

// ✅ Good (automatically sanitized)
logger.info('User login: [EMAIL_REDACTED], password: [REDACTED]');
```

**Safe logging practices**:
```dart
// Use safe wrappers
logger.info('User action', context: {
  'user_id': SafeDataLogger.safeUserId(userId), // Hashed
  'sign': sign, // OK - not PII
  'timestamp': SafeDataLogger.safeTimestamp(),
});
```

---

### Log Persistence

- **Local storage**: Up to 7 days
- **Max file size**: 10 MB per file
- **Rotation**: Automatic when file size exceeded
- **Remote logging**: ERROR and CRITICAL only (production)
- **Cleanup**: Auto-delete logs older than 7 days

---

## Performance Monitoring

### App Performance Metrics

#### Startup Time

```dart
class PerformanceMonitoringService {
  final Stopwatch _startupStopwatch = Stopwatch();

  void startAppStartup() {
    _startupStopwatch.start();
  }

  void markInteractive() {
    final duration = _startupStopwatch.elapsed;

    analytics.logEvent('app_startup_performance', {
      'interactive_ms': duration.inMilliseconds,
      'platform': Platform.operatingSystem,
    });

    if (duration.inMilliseconds > 2000) {
      logger.warning('Slow app startup: ${duration.inMilliseconds}ms');
    }
  }
}
```

**Target**: <2000ms
**Alert threshold**: >3000ms

---

#### Screen Load Time

```dart
class ScreenPerformanceTracker {
  static void trackScreenLoad(String screenName, VoidCallback builder) {
    final stopwatch = Stopwatch()..start();

    builder();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      stopwatch.stop();

      analytics.logEvent('screen_load_time', {
        'screen': screenName,
        'duration_ms': stopwatch.elapsedMilliseconds,
      });
    });
  }
}
```

**Target**: <1000ms
**Alert threshold**: >3000ms

---

#### Frame Rate

```dart
class FrameRateMonitor {
  static void initialize() {
    WidgetsBinding.instance.addTimingsCallback((timings) {
      for (final timing in timings) {
        final frameDuration = timing.totalSpan;

        // Frame budget: 16.67ms for 60fps
        if (frameDuration.inMilliseconds > 16) {
          analytics.logEvent('frame_drop', {
            'duration_ms': frameDuration.inMilliseconds,
          });
        }
      }
    });
  }
}
```

**Target**: 60fps (16.67ms per frame)
**Alert threshold**: <50fps (>20ms per frame)

---

### Network Performance

#### API Latency

```dart
class BackendService {
  Future<T> _performRequest<T>(
    String endpoint,
    Future<T> Function() request,
  ) async {
    final stopwatch = Stopwatch()..start();

    try {
      final result = await request();
      stopwatch.stop();

      analytics.logEvent('api_call_completed', {
        'endpoint': endpoint,
        'duration_ms': stopwatch.elapsedMilliseconds,
        'success': true,
      });

      return result;
    } catch (e) {
      stopwatch.stop();

      analytics.logEvent('api_call_completed', {
        'endpoint': endpoint,
        'duration_ms': stopwatch.elapsedMilliseconds,
        'success': false,
      });

      rethrow;
    }
  }
}
```

**Target**: <2000ms
**Alert threshold**: >5000ms

---

### Performance Budgets

```dart
class PerformanceBudgets {
  // App startup
  static const maxStartupTime = Duration(seconds: 2);
  static const maxTimeToInteractive = Duration(seconds: 3);

  // Screens
  static const maxScreenLoadTime = Duration(milliseconds: 1000);

  // Network
  static const maxApiLatency = Duration(milliseconds: 2000);
  static const minSuccessRate = 99.0; // percent

  // Cache
  static const minCacheHitRate = 80.0; // percent

  // Resources
  static const maxMemoryUsage = 200; // MB
}
```

---

## Event Catalog

See [ANALYTICS_IMPLEMENTATION_GUIDE.md](../.claude/06_DEPLOYMENT/ANALYTICS_IMPLEMENTATION_GUIDE.md) for complete event catalog (100+ events).

### Critical Events Summary

**Revenue (Must Track)**:
1. `paywall_shown`
2. `purchase_initiated`
3. `purchase_completed`
4. `purchase_failed`
5. `trial_started`
6. `trial_converted`
7. `subscription_cancelled`

**User Journey**:
8. `app_opened`
9. `onboarding_completed`
10. `birth_chart_calculated`

**Feature Usage**:
11. `horoscope_viewed`
12. `compatibility_analyzed`
13. `coach_chat_started`

**Performance**:
14. `app_startup_performance`
15. `screen_load_time`
16. `api_call_completed`

---

## Privacy & Compliance

### GDPR Compliance

✅ **User consent**: Analytics only after consent
✅ **Data minimization**: Only collect necessary data
✅ **Right to be forgotten**: Can delete user data
✅ **Data portability**: Can export user data
✅ **Privacy by design**: PII protection built-in

### PII Protection

**Automatic redaction**:
```dart
class SensitiveDataFilter {
  static const prohibited = [
    'password', 'token', 'api_key', 'secret',
    'credit_card', 'email', 'phone', 'birth_date',
  ];

  static String sanitize(String message) {
    var sanitized = message;

    // Redact passwords
    sanitized = sanitized.replaceAllMapped(
      RegExp(r'password[:\s]*[^\s,}]+', caseSensitive: false),
      (match) => 'password: [REDACTED]',
    );

    // Redact emails
    sanitized = sanitized.replaceAllMapped(
      RegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
      (match) => '[EMAIL_REDACTED]',
    );

    return sanitized;
  }
}
```

---

## Troubleshooting

### Issue: Events not appearing in Firebase

**Solution**:
```dart
// Check debug mode
await FirebaseAnalytics.instance.setAnalyticsCollectionEnabled(true);

// Verify event name
// - Max 40 characters
// - Alphanumeric + underscore only
// - No spaces

// Check parameter count
// - Max 25 parameters per event

// Verify parameter values
// - Max 100 characters per value
```

---

### Issue: Logs not writing to file

**Solution**:
```dart
// Check initialization
await SecureLoggingService().initialize();

// Verify storage permissions
// Check available disk space

// Manual flush
await SecureLoggingService()._flush();

// Check log directory
final directory = await getApplicationDocumentsDirectory();
final logDir = Directory('${directory.path}/logs');
print('Log files: ${logDir.listSync()}');
```

---

### Issue: Performance metrics inaccurate

**Solution**:
```dart
// Use Stopwatch, not DateTime difference
final stopwatch = Stopwatch()..start();
// ... operation ...
stopwatch.stop();
final duration = stopwatch.elapsed;

// Measure in correct units
analytics.logEvent('operation_time', {
  'duration_ms': stopwatch.elapsedMilliseconds, // ✅
  'duration': stopwatch.elapsed.toString(), // ❌ Not comparable
});
```

---

## Best Practices

1. **Analytics**
   - Always use event naming convention
   - Track revenue events religiously
   - Keep parameter count reasonable (<10)
   - Test events in debug mode first

2. **Logging**
   - Use appropriate log levels
   - Never log PII
   - Include context in logs
   - Don't over-log in production

3. **Performance**
   - Monitor critical paths only
   - Set realistic budgets
   - Alert on budget violations
   - Regular performance reviews

4. **Privacy**
   - Hash all user IDs
   - Redact sensitive data automatically
   - Respect user consent
   - Document data collection

---

**For support**: Contact dev team
**For data questions**: See privacy policy
**For analytics dashboard**: Firebase Console
