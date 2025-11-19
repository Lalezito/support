# 📊 ANALYTICS IMPLEMENTATION GUIDE

**Objetivo**: Instrumentar CoreAnalyticsService en todos los módulos
**Prioridad**: CRÍTICA - Business Intelligence
**Fecha**: 2025-10-05

---

## 🎯 Analytics Events Catalog

### 1. User Journey Events

#### App Lifecycle
```dart
// lib/main.dart
await analytics.logEvent('app_opened', {
  'timestamp': DateTime.now().toIso8601String(),
  'platform': Platform.operatingSystem,
  'app_version': packageInfo.version,
});

await analytics.logEvent('app_closed', {
  'session_duration': sessionDuration.inSeconds,
});
```

#### Onboarding
```dart
// lib/screens/onboarding_screen.dart
await analytics.logEvent('onboarding_started');

await analytics.logEvent('onboarding_step_completed', {
  'step': stepNumber,
  'step_name': stepName,
});

await analytics.logEvent('onboarding_completed', {
  'total_time': duration.inSeconds,
  'steps_completed': totalSteps,
});
```

#### Birth Data
```dart
// lib/screens/birth_data_collection_screen.dart
await analytics.logEvent('birth_data_entered', {
  'has_birth_time': birthTime != null,
  'has_location': location != null,
});

await analytics.logEvent('birth_chart_calculated', {
  'sun_sign': chart.sunSign,
  'moon_sign': chart.moonSign,
  'ascendant': chart.ascendant,
});
```

---

### 2. Monetization Events (CRITICAL)

#### Paywall
```dart
// lib/screens/paywall_screen.dart
await analytics.logEvent('paywall_shown', {
  'tier': tier.name,
  'context': context, // e.g., 'feature_limit', 'upgrade_prompt'
  'trigger': trigger, // e.g., 'ai_coach_locked'
});

await analytics.logEvent('paywall_dismissed', {
  'tier': tier.name,
  'time_viewed': viewDuration.inSeconds,
});
```

#### Purchase Flow
```dart
// lib/services/subscription_service.dart
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

await analytics.logEvent('purchase_cancelled', {
  'tier': tier.name,
  'step': purchaseStep, // e.g., 'payment_sheet', 'confirmation'
});
```

#### Trial
```dart
// lib/services/subscription_service.dart
await analytics.logEvent('trial_started', {
  'duration_days': 7,
  'trigger': trigger, // e.g., 'paywall', 'settings'
});

await analytics.logEvent('trial_converted', {
  'target_tier': tier.name,
  'conversion_day': dayNumber, // 1-7
  'trial_duration_used': daysUsed,
});

await analytics.logEvent('trial_expired', {
  'converted': false,
  'last_used_feature': lastFeature,
});
```

#### Subscription Management
```dart
await analytics.logEvent('subscription_cancelled', {
  'tier': tier.name,
  'reason': cancellationReason,
  'lifetime_value': lifetimeValue,
  'days_subscribed': daysSubscribed,
});

await analytics.logEvent('subscription_restored', {
  'tier': tier.name,
  'restore_source': 'button', // or 'auto'
});
```

---

### 3. Feature Usage Events

#### Horoscope
```dart
// lib/services/horoscope_service.dart
await analytics.logEvent('horoscope_viewed', {
  'type': 'daily', // or 'weekly', 'monthly'
  'sign': zodiacSign,
  'source': 'home', // or 'notification', 'tab'
});

await analytics.logEvent('horoscope_shared', {
  'type': 'daily',
  'sign': zodiacSign,
  'platform': 'whatsapp', // or 'instagram', etc.
});
```

#### Compatibility
```dart
// lib/services/consolidated_compatibility/core_compatibility_service.dart
await analytics.logEvent('compatibility_analyzed', {
  'sign1': sign1,
  'sign2': sign2,
  'compatibility_score': score,
  'relationship_type': type, // 'romantic', 'friendship', 'business'
});

await analytics.logEvent('compatibility_shared', {
  'sign1': sign1,
  'sign2': sign2,
  'score': score,
});
```

#### AI Cosmic Coach
```dart
// lib/services/consolidated_ai/coaching_ai_service.dart
await analytics.logEvent('coach_chat_started', {
  'user_tier': tier.name,
  'context': context, // e.g., 'main_screen', 'notification'
});

await analytics.logEvent('coach_message_sent', {
  'message_length': message.length,
  'topic': detectedTopic,
});

await analytics.logEvent('coach_response_received', {
  'response_time_ms': responseTime.inMilliseconds,
  'response_type': responseType, // 'guidance', 'insight', etc.
});
```

#### Journaling
```dart
// lib/services/smart_journaling_service.dart
await analytics.logEvent('journal_entry_created', {
  'word_count': wordCount,
  'has_mood': mood != null,
  'emotional_tags': emotionalTags,
});

await analytics.logEvent('journal_analysis_viewed', {
  'entry_count': totalEntries,
  'analysis_type': 'emotional_patterns',
});
```

#### Notifications
```dart
// lib/services/prediction_notification_service.dart
await analytics.logEvent('notification_scheduled', {
  'type': notificationType,
  'time': scheduledTime.toString(),
});

await analytics.logEvent('notification_delivered', {
  'type': notificationType,
  'time_actual': actualTime.toString(),
  'delay_seconds': delay.inSeconds,
});

await analytics.logEvent('notification_opened', {
  'type': notificationType,
  'time_opened': openTime.toString(),
  'time_to_open': timeToOpen.inSeconds,
});
```

#### Offline Mode
```dart
// lib/services/offline_mode_service.dart
await analytics.logEvent('offline_mode_activated', {
  'trigger': 'network_lost', // or 'manual'
  'cached_data_available': hasCachedData,
});

await analytics.logEvent('offline_sync_completed', {
  'duration_ms': duration.inMilliseconds,
  'items_synced': itemCount,
  'conflicts_resolved': conflictCount,
});
```

---

### 4. Performance Metrics

#### API Calls
```dart
// lib/services/backend_service.dart
await analytics.logEvent('api_call_completed', {
  'endpoint': endpoint,
  'duration_ms': duration.inMilliseconds,
  'success': success,
  'status_code': statusCode,
});
```

#### Cache Performance
```dart
// lib/services/cache_service.dart
await analytics.logEvent('cache_hit', {
  'service': serviceName,
  'cache_key': key,
});

await analytics.logEvent('cache_miss', {
  'service': serviceName,
  'cache_key': key,
  'fallback_used': usedFallback,
});
```

#### Screen Performance
```dart
// Use in key screens
await analytics.logEvent('screen_load_time', {
  'screen': screenName,
  'duration_ms': loadTime.inMilliseconds,
  'widgets_rendered': widgetCount,
});
```

---

### 5. Error Tracking

```dart
// Global error handler
await analytics.logEvent('error_occurred', {
  'service': serviceName,
  'error': error.toString(),
  'stack_trace': stackTrace.toString().substring(0, 500), // Truncate
  'severity': 'high', // or 'medium', 'low'
});

await analytics.logEvent('crash_detected', {
  'error': error.toString(),
  'platform': Platform.operatingSystem,
  'app_version': appVersion,
});
```

---

## 📈 Revenue Analytics (Special Tracking)

### Key Metrics to Track

```dart
class RevenueAnalytics {
  // Average Revenue Per User
  static Future<void> trackARPU() async {
    final arpu = totalRevenue / totalUsers;
    await analytics.setUserProperty('arpu', arpu.toString());
  }

  // Lifetime Value
  static Future<void> trackLTV(String userId, double value) async {
    await analytics.logEvent('ltv_updated', {
      'user_id': userId,
      'ltv': value,
      'tier': currentTier,
    });
  }

  // Conversion Rate
  static Future<void> trackConversion(String funnel, double rate) async {
    await analytics.logEvent('conversion_tracked', {
      'funnel': funnel, // e.g., 'free_to_trial', 'trial_to_paid'
      'conversion_rate': rate,
    });
  }

  // Churn
  static Future<void> trackChurn(String reason) async {
    await analytics.logEvent('user_churned', {
      'reason': reason,
      'tier_at_churn': tier,
      'lifetime_days': lifetimeDays,
      'lifetime_revenue': lifetimeRevenue,
    });
  }
}
```

---

## 🔐 Privacy & Compliance

### Data to NEVER Log

```dart
// ❌ PROHIBITED - Never log these
class ProhibitedData {
  static const prohibited = [
    'password',
    'payment_token',
    'credit_card_number',
    'full_name', // Use hashed ID instead
    'email', // Use hashed version
    'phone_number',
    'precise_location', // Use city-level only
    'birth_date', // Use year only if needed
    'ip_address',
  ];
}
```

### Safe Data Practices

```dart
// ✅ SAFE - Hash PII before logging
class SafeAnalytics {
  static String hashUserId(String userId) {
    return sha256.convert(utf8.encode(userId)).toString();
  }

  static Future<void> logWithPrivacy(String event, Map<String, dynamic> params) async {
    // Remove any PII
    final safeParams = params.map((key, value) {
      if (ProhibitedData.prohibited.contains(key)) {
        return MapEntry(key, '[REDACTED]');
      }
      return MapEntry(key, value);
    });

    await analytics.logEvent(event, safeParams);
  }
}
```

---

## 🔧 Implementation Checklist

### Phase 1: Core Events (Week 1)
- [ ] App lifecycle events
- [ ] Onboarding events
- [ ] Purchase flow events (CRITICAL)
- [ ] Error tracking

### Phase 2: Feature Events (Week 2)
- [ ] Horoscope events
- [ ] Compatibility events
- [ ] AI Coach events
- [ ] Journaling events

### Phase 3: Advanced (Week 3)
- [ ] Performance metrics
- [ ] Cache analytics
- [ ] Offline mode events
- [ ] Notification events

### Phase 4: Optimization (Week 4)
- [ ] Revenue analytics dashboard
- [ ] Conversion funnels
- [ ] Retention cohorts
- [ ] A/B testing framework

---

## 📊 Analytics Dashboard Setup

### Firebase Analytics Events

```dart
// lib/services/core_analytics_service.dart
import 'package:firebase_analytics/firebase_analytics.dart';

class CoreAnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  Future<void> logEvent(String name, [Map<String, dynamic>? parameters]) async {
    try {
      await _analytics.logEvent(
        name: name,
        parameters: parameters,
      );
    } catch (e) {
      // Log error but don't break app
      debugPrint('Analytics error: $e');
    }
  }

  Future<void> setUserId(String userId) async {
    await _analytics.setUserId(id: hashUserId(userId));
  }

  Future<void> setUserProperty(String name, String value) async {
    await _analytics.setUserProperty(name: name, value: value);
  }
}
```

### Custom Events Setup (Firebase Console)

1. **Monetization Events**:
   - purchase_completed (Revenue)
   - trial_started (Conversions)
   - subscription_cancelled (Churn)

2. **Engagement Events**:
   - horoscope_viewed (Daily Active Users)
   - coach_chat_started (Feature Usage)
   - journal_entry_created (Content Creation)

3. **Performance Events**:
   - api_call_completed (Backend Health)
   - screen_load_time (UX Performance)

---

## 🎯 Success Metrics

### Analytics Coverage
- [ ] 100% of revenue events tracked
- [ ] 95%+ of user journey events tracked
- [ ] All critical features instrumented
- [ ] Error tracking on all services

### Data Quality
- [ ] No PII in event params
- [ ] All events have required params
- [ ] Event names follow naming convention
- [ ] Data validation in place

### Business Intelligence
- [ ] Revenue dashboard functional
- [ ] Conversion funnels visible
- [ ] Retention metrics tracking
- [ ] A/B test capabilities ready

---

## 📝 Event Naming Convention

### Format
```
{category}_{action}_{object}
```

### Examples
```
purchase_completed_essential
horoscope_viewed_daily
coach_chat_started_main
notification_opened_prediction
```

### Categories
- `app_*` - App lifecycle
- `purchase_*` - Monetization
- `trial_*` - Trial management
- `horoscope_*` - Horoscope features
- `coach_*` - AI Coach
- `journal_*` - Journaling
- `notification_*` - Notifications
- `error_*` - Errors

---

## 🚀 Quick Start Guide

### 1. Initialize Analytics
```dart
// main.dart
final analytics = CoreAnalyticsService();
await analytics.initialize();
```

### 2. Add to Key Screens
```dart
// Example: PremiumScreen
class PremiumScreen extends StatefulWidget {
  @override
  void initState() {
    super.initState();
    analytics.logEvent('paywall_shown', {
      'tier': widget.tier.name,
      'context': widget.context,
    });
  }
}
```

### 3. Track Purchases
```dart
// subscription_service.dart
Future<bool> purchaseTier(SubscriptionType tier) async {
  analytics.logEvent('purchase_initiated', {'tier': tier.name});

  try {
    final result = await revenueCat.purchase(tier);

    analytics.logEvent('purchase_completed', {
      'tier': tier.name,
      'revenue': tier.price,
    });

    return true;
  } catch (e) {
    analytics.logEvent('purchase_failed', {
      'tier': tier.name,
      'error': e.toString(),
    });
    return false;
  }
}
```

### 4. Monitor Performance
```dart
// Wrap critical operations
final stopwatch = Stopwatch()..start();
final result = await expensiveOperation();
stopwatch.stop();

analytics.logEvent('operation_completed', {
  'operation': 'expensive_operation',
  'duration_ms': stopwatch.elapsedMilliseconds,
});
```

---

**Status**: 📝 IMPLEMENTATION GUIDE READY
**Priority**: 🔴 CRITICAL
**Next**: Implement in codebase
**Est. Time**: 2-3 days full implementation
