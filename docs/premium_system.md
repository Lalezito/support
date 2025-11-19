# Premium System Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: ✅ Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Tier System](#tier-system)
3. [Architecture](#architecture)
4. [RevenueCat Integration](#revenuecat-integration)
5. [Feature Gating](#feature-gating)
6. [Purchase Flows](#purchase-flows)
7. [Testing](#testing)
8. [Analytics](#analytics)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Zodiac Life Coach premium system provides a 6-tier subscription model integrated with RevenueCat for cross-platform subscription management.

### Key Features

✅ 6 subscription tiers (Free → Lifetime)
✅ RevenueCat integration for subscription management
✅ Cross-platform purchase synchronization
✅ 7-day free trial
✅ Restore purchases functionality
✅ Feature gating per tier
✅ Revenue analytics tracking
✅ Upgrade/downgrade flows

---

## Tier System

### Subscription Tiers

| Tier | Price | Billing | Features | Target User |
|------|-------|---------|----------|-------------|
| **Free** | $0 | - | Basic horoscopes, zodiac info | New users, casual explorers |
| **Trial** | $0 | 7 days | All Advanced features | Trial converters |
| **Essential** | $4.99 | Monthly | AI Coach (basic), detailed horoscopes, compatibility | Regular users |
| **Advanced** | $9.99 | Monthly | Everything in Essential + journaling, predictions | Engaged users |
| **Master** | $19.99 | Monthly | Everything in Advanced + premium insights, priority support | Power users |
| **Cosmic VIP** | $49.99 | Monthly | Everything in Master + 1-on-1 sessions, exclusive content | VIP users |
| **Lifetime** | $199.99 | One-time | Everything in Cosmic VIP, forever | Committed users |

---

### Feature Matrix

| Feature | Free | Trial | Essential | Advanced | Master | Cosmic VIP | Lifetime |
|---------|------|-------|-----------|----------|--------|------------|----------|
| Daily Horoscope | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Weekly Horoscope | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Monthly Horoscope | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Compatibility Analysis | Basic | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Birth Chart | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI Cosmic Coach | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Smart Journaling | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Predictions | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Premium Insights | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Priority Support | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| 1-on-1 Sessions | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Exclusive Content | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │   Paywall   │  │   Settings  │  │   Feature    │   │
│  │   Screen    │  │   Screen    │  │   Screens    │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         PremiumSubscriptionManager               │  │
│  │  - Subscription state management                 │  │
│  │  - Purchase orchestration                        │  │
│  │  - Trial management                              │  │
│  └────────┬─────────────────────────────────────────┘  │
│           │                                             │
│  ┌────────▼─────────┐  ┌───────────────────────────┐  │
│  │ SubscriptionServ│  │   FeatureGatingService    │  │
│  │  - Purchase API  │  │  - Feature availability   │  │
│  │  - Restore       │  │  - Tier checking          │  │
│  └──────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│                  Integration Layer                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │                RevenueCat SDK                    │  │
│  │  - Purchase handling                             │  │
│  │  - Receipt validation                            │  │
│  │  - Cross-platform sync                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## RevenueCat Integration

### Setup

```dart
// lib/services/subscription_service.dart
import 'package:purchases_flutter/purchases_flutter.dart';

class SubscriptionService {
  static Future<void> initialize() async {
    await Purchases.setDebugLogsEnabled(kDebugMode);

    final configuration = PurchasesConfiguration(
      Platform.isIOS
        ? 'appl_YOUR_IOS_KEY'
        : 'goog_YOUR_ANDROID_KEY',
    );

    await Purchases.configure(configuration);
  }

  Future<void> identifyUser(String userId) async {
    await Purchases.logIn(userId);
  }
}
```

---

### Product IDs

| Tier | iOS Product ID | Android Product ID |
|------|----------------|-------------------|
| Trial | `zodiac_trial_7day` | `zodiac_trial_7day` |
| Essential | `zodiac_essential_monthly` | `zodiac_essential_monthly` |
| Advanced | `zodiac_advanced_monthly` | `zodiac_advanced_monthly` |
| Master | `zodiac_master_monthly` | `zodiac_master_monthly` |
| Cosmic VIP | `zodiac_vip_monthly` | `zodiac_vip_monthly` |
| Lifetime | `zodiac_lifetime` | `zodiac_lifetime` |

---

### Fetching Offerings

```dart
class SubscriptionService {
  Future<List<Package>> getAvailablePackages() async {
    try {
      final offerings = await Purchases.getOfferings();

      if (offerings.current != null) {
        return offerings.current!.availablePackages;
      }

      return [];
    } catch (e, stack) {
      SecureLoggingService().error(
        'Failed to fetch offerings',
        error: e,
        stackTrace: stack,
      );
      return [];
    }
  }

  Package? getPackageForTier(
    List<Package> packages,
    SubscriptionType tier,
  ) {
    final productId = _getProductIdForTier(tier);
    return packages.firstWhereOrNull(
      (package) => package.storeProduct.identifier == productId,
    );
  }
}
```

---

### Making a Purchase

```dart
class SubscriptionService {
  Future<bool> purchaseTier(SubscriptionType tier) async {
    analytics.logEvent('purchase_initiated', {
      'tier': tier.name,
      'price': tier.price,
    });

    try {
      final packages = await getAvailablePackages();
      final package = getPackageForTier(packages, tier);

      if (package == null) {
        throw Exception('Package not found for tier: ${tier.name}');
      }

      final purchaserInfo = await Purchases.purchasePackage(package);

      if (purchaserInfo.entitlements.active.isNotEmpty) {
        // Purchase successful!
        await _activatePremium(tier);

        analytics.logEvent('purchase_completed', {
          'tier': tier.name,
          'revenue': tier.price,
          'transaction_id': purchaserInfo.originalAppUserId,
        });

        return true;
      }

      return false;

    } on PlatformException catch (e) {
      final errorCode = PurchasesErrorHelper.getErrorCode(e);

      if (errorCode == PurchasesErrorCode.purchaseCancelledError) {
        analytics.logEvent('purchase_cancelled', {'tier': tier.name});
      } else {
        analytics.logEvent('purchase_failed', {
          'tier': tier.name,
          'error': e.message,
          'error_code': errorCode.toString(),
        });

        SecureLoggingService().error(
          'Purchase failed',
          error: e,
          stackTrace: StackTrace.current,
        );
      }

      return false;
    }
  }
}
```

---

### Restoring Purchases

```dart
class SubscriptionService {
  Future<bool> restorePurchases() async {
    analytics.logEvent('restore_purchases_initiated');

    try {
      final purchaserInfo = await Purchases.restorePurchases();

      if (purchaserInfo.entitlements.active.isNotEmpty) {
        // Find active subscription
        final activeTier = _determineActiveT ier(purchaserInfo);

        await _activatePremium(activeTier);

        analytics.logEvent('restore_purchases_success', {
          'tier': activeTier.name,
        });

        return true;
      } else {
        // No active subscriptions
        analytics.logEvent('restore_purchases_none_found');
        return false;
      }

    } catch (e, stack) {
      analytics.logEvent('restore_purchases_failed', {
        'error': e.toString(),
      });

      SecureLoggingService().error(
        'Restore purchases failed',
        error: e,
        stackTrace: stack,
      );

      return false;
    }
  }

  SubscriptionType _determineActiveTier(PurchaserInfo info) {
    // Check entitlements in priority order
    if (info.entitlements.active.containsKey('lifetime')) {
      return SubscriptionType.lifetime;
    } else if (info.entitlements.active.containsKey('cosmic_vip')) {
      return SubscriptionType.cosmicVip;
    } else if (info.entitlements.active.containsKey('master')) {
      return SubscriptionType.master;
    } else if (info.entitlements.active.containsKey('advanced')) {
      return SubscriptionType.advanced;
    } else if (info.entitlements.active.containsKey('essential')) {
      return SubscriptionType.essential;
    }

    return SubscriptionType.free;
  }
}
```

---

## Feature Gating

### Checking Feature Availability

```dart
class FeatureGatingService {
  final PremiumProvider _premiumProvider;

  bool isFeatureAvailable(String featureName) {
    final currentTier = _premiumProvider.getCurrentSubscriptionType();
    return _featureMatrix[featureName]?.contains(currentTier) ?? false;
  }

  static final Map<String, List<SubscriptionType>> _featureMatrix = {
    'daily_horoscope': [
      SubscriptionType.free,
      SubscriptionType.trial,
      SubscriptionType.essential,
      SubscriptionType.advanced,
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'weekly_horoscope': [
      SubscriptionType.trial,
      SubscriptionType.essential,
      SubscriptionType.advanced,
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'ai_coach': [
      SubscriptionType.trial,
      SubscriptionType.essential,
      SubscriptionType.advanced,
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'smart_journaling': [
      SubscriptionType.advanced,
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'predictions': [
      SubscriptionType.advanced,
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'premium_insights': [
      SubscriptionType.master,
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
    'one_on_one_sessions': [
      SubscriptionType.cosmicVip,
      SubscriptionType.lifetime,
    ],
  };
}
```

---

### Feature Gating in UI

```dart
class AICoachScreen extends StatelessWidget {
  final FeatureGatingService _featureGating = FeatureGatingService();

  @override
  Widget build(BuildContext context) {
    if (!_featureGating.isFeatureAvailable('ai_coach')) {
      return _buildLockedScreen(context);
    }

    return _buildCoachInterface();
  }

  Widget _buildLockedScreen(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Cosmic Coach')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.lock, size: 80, color: Colors.grey),
            SizedBox(height: 24),
            Text(
              'AI Cosmic Coach is a premium feature',
              style: Theme.of(context).textTheme.headline6,
            ),
            SizedBox(height: 16),
            Text(
              'Upgrade to Essential tier to unlock',
              style: Theme.of(context).textTheme.bodyText2,
            ),
            SizedBox(height: 32),
            ElevatedButton(
              onPressed: () => _showPaywall(context),
              child: Text('View Plans'),
            ),
          ],
        ),
      ),
    );
  }

  void _showPaywall(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PaywallScreen(
          lockedFeature: 'ai_coach',
          recommendedTier: SubscriptionType.essential,
        ),
      ),
    );
  }
}
```

---

## Purchase Flows

### Flow 1: Paywall → Purchase → Activate

```dart
class PaywallScreen extends StatefulWidget {
  final String? lockedFeature;
  final SubscriptionType? recommendedTier;

  @override
  _PaywallScreenState createState() => _PaywallScreenState();
}

class _PaywallScreenState extends State<PaywallScreen> {
  bool _isLoading = false;
  List<Package> _packages = [];

  @override
  void initState() {
    super.initState();
    _loadPackages();

    // Analytics
    analytics.logEvent('paywall_shown', {
      'locked_feature': widget.lockedFeature,
      'recommended_tier': widget.recommendedTier?.name,
    });
  }

  Future<void> _loadPackages() async {
    final packages = await subscriptionService.getAvailablePackages();
    setState(() => _packages = packages);
  }

  Future<void> _purchaseTier(SubscriptionType tier) async {
    setState(() => _isLoading = true);

    final success = await subscriptionService.purchaseTier(tier);

    setState(() => _isLoading = false);

    if (success) {
      // Show success message
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Welcome to ${tier.displayName}! ✨'),
          backgroundColor: Colors.green,
        ),
      );

      // Close paywall
      Navigator.pop(context, true);
    } else {
      // Show error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Purchase failed. Please try again.'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Choose Your Cosmic Journey')),
      body: _isLoading
        ? Center(child: CircularProgressIndicator())
        : _buildTierList(),
    );
  }

  Widget _buildTierList() {
    return ListView.builder(
      itemCount: _packages.length,
      itemBuilder: (context, index) {
        final package = _packages[index];
        final tier = _getTierFromPackage(package);

        return TierCard(
          tier: tier,
          package: package,
          isRecommended: tier == widget.recommendedTier,
          onPurchase: () => _purchaseTier(tier),
        );
      },
    );
  }
}
```

---

### Flow 2: Trial Activation

```dart
class TrialService {
  Future<bool> activateFreeTrial() async {
    // Check if trial already used
    if (await hasUsedTrial()) {
      return false;
    }

    analytics.logEvent('trial_started', {
      'duration_days': 7,
    });

    try {
      // Purchase trial package through RevenueCat
      final success = await subscriptionService.purchaseTier(
        SubscriptionType.trial,
      );

      if (success) {
        // Mark trial as used
        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('trial_used', true);
        await prefs.setString(
          'trial_start_date',
          DateTime.now().toIso8601String(),
        );

        return true;
      }

      return false;

    } catch (e, stack) {
      SecureLoggingService().error(
        'Trial activation failed',
        error: e,
        stackTrace: stack,
      );
      return false;
    }
  }

  Future<bool> hasUsedTrial() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('trial_used') ?? false;
  }

  Future<int> getDaysRemaining() async {
    final prefs = await SharedPreferences.getInstance();
    final startDateStr = prefs.getString('trial_start_date');

    if (startDateStr == null) return 0;

    final startDate = DateTime.parse(startDateStr);
    final endDate = startDate.add(Duration(days: 7));
    final now = DateTime.now();

    if (now.isAfter(endDate)) return 0;

    return endDate.difference(now).inDays;
  }
}
```

---

## Testing

See [PREMIUM_TESTING_CHECKLIST.md](./.claude/04_TESTING/PREMIUM_TESTING_CHECKLIST.md) for comprehensive testing guide.

### Quick Test Checklist

- [ ] Purchase Essential tier
- [ ] Features unlock immediately
- [ ] Restore purchases after reinstall
- [ ] Trial activation works
- [ ] Trial expiration handled correctly
- [ ] Upgrade from Essential → Advanced
- [ ] Downgrade from Advanced → Essential
- [ ] Lifetime purchase works
- [ ] Cross-platform sync (iOS ↔ Android)

---

## Analytics

### Key Events to Track

```dart
// Revenue events
analytics.logEvent('purchase_completed', {
  'tier': tier.name,
  'revenue': tier.price,
  'is_upgrade': isUpgrade,
});

analytics.logEvent('trial_converted', {
  'target_tier': tier.name,
  'conversion_day': dayNumber,
});

analytics.logEvent('subscription_cancelled', {
  'tier': tier.name,
  'reason': cancellationReason,
  'lifetime_value': lifetimeValue,
});

// Feature usage by tier
analytics.logEvent('feature_accessed', {
  'feature': featureName,
  'tier': currentTier.name,
  'is_gated': wasGated,
});
```

---

## Troubleshooting

### Issue: Purchase not activating

**Solution**:
```dart
// Check RevenueCat dashboard for transaction
// Verify product IDs match
// Test restore purchases
await subscriptionService.restorePurchases();

// Check entitlements
final info = await Purchases.getCustomerInfo();
print('Active entitlements: ${info.entitlements.active}');
```

---

### Issue: Features not unlocking after purchase

**Solution**:
```dart
// Force refresh subscription state
await premiumProvider.refreshSubscriptionStatus();

// Verify feature matrix
print('Feature available: ${featureGating.isFeatureAvailable("ai_coach")}');

// Check tier state
print('Current tier: ${premiumProvider.getCurrentSubscriptionType()}');
```

---

**For support**: Contact dev team
**For bugs**: See GitHub issues
**For revenue questions**: See business team
