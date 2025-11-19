# Pricing Provider - Quick Implementation Guide

**Time Required**: 15 minutes
**Difficulty**: Easy
**Impact**: High (enables currency localization)

---

## Problem

Premium Screen shows hardcoded USD prices instead of real prices from RevenueCat.

**Current**:
```dart
price: PricingConstants.TIER1_PRICE_FORMATTED,  // Hardcoded "$6.99"
```

**Desired**:
```dart
price: pricingData?['cosmic']?['price'] ?? '\$6.99',  // Dynamic from RevenueCat
```

---

## Solution

### Step 1: Locate the Premium Screen File

**File**: `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/premium_screen.dart`

**Method**: `_buildPremiumTiers()` (around line 1240)

---

### Step 2: Add Pricing Provider Watch

**Add this at the beginning of `_buildPremiumTiers()` method**:

```dart
Widget _buildPremiumTiers() {
  final languageCode = Localizations.localeOf(context).languageCode;

  // ✅ ADD THIS: Watch pricing from RevenueCat
  final pricingAsyncValue = ref.watch(pricingInfoProvider);

  return pricingAsyncValue.when(
    // SUCCESS: Use real prices from RevenueCat
    data: (pricingData) => _buildTiersWithPricing(pricingData, languageCode),

    // LOADING: Show loading state with fallback prices
    loading: () => _buildTiersWithFallback(languageCode),

    // ERROR: Show fallback prices and log error
    error: (error, stackTrace) {
      AppLogger.warning('Failed to load pricing, using fallback: $error');
      return _buildTiersWithFallback(languageCode);
    },
  );
}
```

---

### Step 3: Create Helper Method for Real Pricing

**Add this new method**:

```dart
Widget _buildTiersWithPricing(Map<String, dynamic>? pricingData, String languageCode) {
  // Extract prices from RevenueCat with fallback to constants
  final cosmicPrice = pricingData?['cosmic']?['price'] ?? PricingConstants.TIER1_PRICE_FORMATTED;
  final stellarPrice = pricingData?['stellar']?['price'] ?? PricingConstants.TIER2_PRICE_FORMATTED;
  final universePrice = pricingData?['universe']?['price'] ?? PricingConstants.LIFETIME_PRICE_FORMATTED;

  return Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      // Header section (existing code)
      Container(
        padding: const EdgeInsets.symmetric(vertical: 24),
        child: Column(
          children: [
            Text(
              AppLocalizations.of(context)!.choosePremiumTier,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              AppLocalizations.of(context)!.unlockFullPotential,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.white70,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
      SizedBox(height: 20),

      // TIER 1 - Cosmic Tier
      _buildTierCard(
        tier: PremiumTier.cosmic,
        title: AppLocalizations.of(context)!.cosmicTier,
        price: cosmicPrice,  // ✅ DYNAMIC PRICING
        period: AppLocalizations.of(context)!.perMonth,
        description: '${PremiumFeaturesTranslations.getCosmicDescription(languageCode)}\n\n🎁 Incluye período de prueba gratuito',
        isRecommended: false,
        hasTrial: true,
      ),

      SizedBox(height: 16),

      // TIER 2 - Stellar Tier
      _buildTierCard(
        tier: PremiumTier.stellar,
        title: AppLocalizations.of(context)!.stellarTier,
        price: stellarPrice,  // ✅ DYNAMIC PRICING
        period: '${AppLocalizations.of(context)!.perMonth} ${AppLocalizations.of(context)!.withAI}',
        description: '${PremiumFeaturesTranslations.getStellarDescription(languageCode)}\n\n🎁 Incluye período de prueba gratuito',
        isRecommended: true,
        hasTrial: true,
      ),

      SizedBox(height: 16),

      // LIFETIME TIER 1 - Universe Tier
      _buildTierCard(
        tier: PremiumTier.universe,
        title: AppLocalizations.of(context)!.universeTier,
        price: universePrice,  // ✅ DYNAMIC PRICING
        period: ' (${AppLocalizations.of(context)!.oneTimePayment})',
        description: '${PremiumFeaturesTranslations.getUniverseDescription(languageCode)}\n\n🎁 Incluye período de prueba gratuito',
        isRecommended: false,
        hasTrial: true,
      ),
    ],
  );
}
```

---

### Step 4: Create Helper Method for Fallback

**Add this new method**:

```dart
Widget _buildTiersWithFallback(String languageCode) {
  // Use hardcoded constants as fallback
  return _buildTiersWithPricing(null, languageCode);
}
```

---

### Step 5: Required Imports

**Add at the top of the file if not already present**:

```dart
import 'package:zodiac_app/providers/premium_provider.dart';
import 'package:zodiac_app/utils/app_logger.dart';
```

---

## Expected Behavior

### Before (Hardcoded)

```
Premium Screen
  Cosmic Tier: $6.99/month  ← Always USD
  Stellar Tier: $19.99/month  ← Always USD
  Universe Tier: $49.99 (lifetime)  ← Always USD
```

### After (Dynamic)

```
Premium Screen (US user)
  Cosmic Tier: $6.99/month  ← From App Store

Premium Screen (EU user)
  Cosmic Tier: €6.99/month  ← Localized!

Premium Screen (UK user)
  Cosmic Tier: £6.99/month  ← Localized!

Premium Screen (Offline)
  Cosmic Tier: $6.99/month  ← Fallback to USD
```

---

## Testing

### Test 1: Online with Internet

1. Open Premium Screen
2. Verify prices load (may take 1-3 seconds)
3. Check prices match your region
4. Look for logs:
   ```
   [INFO] Fetching pricing information from RevenueCat
   [INFO] Successfully fetched pricing info with 3 tiers
   ```

### Test 2: Offline Mode

1. Enable Airplane Mode
2. Open Premium Screen
3. Verify fallback prices shown immediately
4. Check logs:
   ```
   [WARNING] RevenueCat integration not available, using fallback pricing
   ```

### Test 3: Currency Localization

1. Change device region to EU
2. Restart app
3. Open Premium Screen
4. Verify prices in EUR (€6.99, €19.99, €49.99)

---

## Troubleshooting

### Issue: Prices show as null

**Cause**: RevenueCat not initialized

**Fix**:
```dart
// Ensure fallback is used
final cosmicPrice = pricingData?['cosmic']?['price'] ?? PricingConstants.TIER1_PRICE_FORMATTED;
```

### Issue: Takes too long to load

**Cause**: Network timeout

**Solution**: Already handled by `loading:` state in `pricingAsyncValue.when()`

### Issue: Wrong currency displayed

**Cause**: App Store Connect pricing not configured for that region

**Fix**: Add regional pricing in App Store Connect

---

## Rollback Plan

If something goes wrong, simply revert to:

```dart
Widget _buildPremiumTiers() {
  final languageCode = Localizations.localeOf(context).languageCode;

  // Original implementation (hardcoded prices)
  return Column(
    children: [
      _buildTierCard(
        tier: PremiumTier.cosmic,
        price: PricingConstants.TIER1_PRICE_FORMATTED,  // Hardcoded
        // ... rest of params
      ),
      // ... other tiers
    ],
  );
}
```

---

## Benefits

1. ✅ **Currency Localization**: Prices in user's currency
2. ✅ **Accuracy**: Matches App Store exactly
3. ✅ **Flexibility**: Update via RevenueCat dashboard
4. ✅ **Regional Pricing**: Different prices per country
5. ✅ **Compliance**: App Store guidelines
6. ✅ **Graceful Degradation**: Falls back on error

---

## Code Diff Summary

**Changes**:
- Modified: `_buildPremiumTiers()` method
- Added: `_buildTiersWithPricing()` method
- Added: `_buildTiersWithFallback()` method
- Added: `ref.watch(pricingInfoProvider)`

**Lines Changed**: ~50-70 lines
**New Methods**: 2
**Imports Added**: 0 (already exist)

---

## Verification Checklist

- [ ] Code compiles without errors
- [ ] Prices load from RevenueCat when online
- [ ] Fallback prices shown when offline
- [ ] No crashes or exceptions
- [ ] Currency localization works
- [ ] UI matches previous design
- [ ] Free trial text still displays
- [ ] All tiers show correctly

---

## Performance Impact

**Before**:
- Instant display (hardcoded values)

**After**:
- First load: 1-3 seconds (fetch from RevenueCat)
- Cached: Instant (provider caches result)
- Offline: Instant (fallback)
- Error: Instant (fallback)

**Net Impact**: +1-3 seconds on first load, worth it for accuracy

---

## Questions?

- Check `PRICING_PROVIDER_REPORT.md` for full details
- Review `lib/providers/premium_provider.dart` for provider code
- See `lib/services/revenuecat_service.dart` for API implementation

---

**Quick Fix Guide**
**Last Updated**: 2025-10-13
**Status**: Ready to implement
