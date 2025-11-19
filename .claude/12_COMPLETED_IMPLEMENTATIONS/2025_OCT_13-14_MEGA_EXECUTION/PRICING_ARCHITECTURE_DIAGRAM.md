# Pricing System Architecture Diagram

**Visual Reference**: Understanding the Pricing Provider Flow

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                                │
│                         (Flutter Widgets / Screens)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │              Premium Screen Widget                         │              │
│  │                                                            │              │
│  │  Current:                                                 │              │
│  │    price: PricingConstants.TIER1_PRICE_FORMATTED ❌       │              │
│  │    (Hardcoded "$6.99")                                    │              │
│  │                                                            │              │
│  │  Should be:                                               │              │
│  │    final pricing = ref.watch(pricingInfoProvider) ✅      │              │
│  │    price: pricing['cosmic']['price'] ?? '$6.99'          │              │
│  │    (Dynamic from RevenueCat)                              │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ ref.watch()                                     │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       STATE MANAGEMENT LAYER                                 │
│                        (Riverpod Providers)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │        pricingInfoProvider (FutureProvider)                │              │
│  │        lib/providers/premium_provider.dart                 │              │
│  │        Lines: 82-85                                        │              │
│  │        Status: ✅ ACTIVE                                   │              │
│  │                                                            │              │
│  │  Returns: Future<Map<String, dynamic>?>                   │              │
│  │  {                                                         │              │
│  │    'cosmic': {                                             │              │
│  │      'price': '$6.99',                                    │              │
│  │      'period': 'month',                                   │              │
│  │      'productId': 'tier1_subscription'                    │              │
│  │    },                                                      │              │
│  │    'stellar': {...},                                       │              │
│  │    'universe': {...}                                       │              │
│  │  }                                                         │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ calls                                            │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                                      │
│                   (Subscription Manager)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │      PremiumSubscriptionManager                            │              │
│  │      lib/services/premium_subscription_manager.dart        │              │
│  │      Lines: 154-181                                        │              │
│  │      Status: ✅ IMPLEMENTED                                │              │
│  │                                                            │              │
│  │  Method: getPricingInfo()                                 │              │
│  │                                                            │              │
│  │  Flow:                                                     │              │
│  │  1. Check if RevenueCat integration available             │              │
│  │  2. Ensure initialization                                 │              │
│  │  3. Fetch offerings from integration                      │              │
│  │  4. Return pricing data                                   │              │
│  │  5. On error: return _getFallbackPricing()               │              │
│  │                                                            │              │
│  │  Error Handling: ✅ Comprehensive                         │              │
│  │  Logging: ✅ Detailed                                     │              │
│  │  Fallback: ✅ 4-layer system                              │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ uses                                             │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     INTEGRATION LAYER                                        │
│                  (RevenueCat Middleware)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │         RevenueCatIntegration                              │              │
│  │         lib/services/revenuecat_integration.dart           │              │
│  │         Lines: 264-272                                     │              │
│  │         Status: ✅ CONNECTED                               │              │
│  │                                                            │              │
│  │  Method: getOfferings()                                   │              │
│  │                                                            │              │
│  │  Responsibilities:                                         │              │
│  │  - Acts as middleware                                     │              │
│  │  - Logging with emojis (📦)                               │              │
│  │  - Error propagation                                      │              │
│  │  - Delegates to RevenueCatService                         │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ delegates to                                     │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       SERVICE LAYER                                          │
│                  (RevenueCat API Wrapper)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │          RevenueCatService                                 │              │
│  │          lib/services/revenuecat_service.dart              │              │
│  │          Lines: 394-451                                    │              │
│  │          Status: ✅ COMPLETE                               │              │
│  │                                                            │              │
│  │  Method: getOfferingsData()                               │              │
│  │                                                            │              │
│  │  Flow:                                                     │              │
│  │  1. Check initialization                                  │              │
│  │  2. Call Purchases.getOfferings()                         │              │
│  │  3. Extract availablePackages                             │              │
│  │  4. Map products to tier structure:                       │              │
│  │     - tier1_subscription → 'cosmic'                       │              │
│  │     - tier2_subscription → 'stellar'                      │              │
│  │     - lifetime_tier1_purchase → 'universe'                │              │
│  │  5. Extract pricing info:                                 │              │
│  │     - price (localized string)                            │              │
│  │     - priceAmount (number)                                │              │
│  │     - currencyCode                                        │              │
│  │     - period                                              │              │
│  │     - productId                                           │              │
│  │  6. Return structured data                                │              │
│  │  7. On error: return _getFallbackPricing()               │              │
│  │                                                            │              │
│  │  Features:                                                 │              │
│  │  ✅ Currency localization                                 │              │
│  │  ✅ Regional pricing                                      │              │
│  │  ✅ Detailed logging                                      │              │
│  │  ✅ Graceful error handling                               │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ uses                                             │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         SDK LAYER                                            │
│                    (RevenueCat Flutter SDK)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │         Purchases (RevenueCat SDK)                         │              │
│  │         Package: purchases_flutter                         │              │
│  │         Status: ✅ INITIALIZED                             │              │
│  │                                                            │              │
│  │  API: Purchases.getOfferings()                            │              │
│  │                                                            │              │
│  │  Returns: Offerings object with:                          │              │
│  │  - current offering                                       │              │
│  │  - availablePackages[]                                    │              │
│  │    - storeProduct                                         │              │
│  │      - identifier (product ID)                            │              │
│  │      - priceString (localized)                            │              │
│  │      - price (number)                                     │              │
│  │      - currencyCode                                       │              │
│  │      - description                                        │              │
│  │      - title                                              │              │
│  └───────────────────────────────────────────────────────────┘              │
│                            │                                                  │
│                            │ fetches from                                     │
│                            ↓                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL API LAYER                                        │
│              (Apple App Store / Google Play)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────┐              │
│  │       Apple App Store / Google Play Store                 │              │
│  │       Status: ✅ CONFIGURED                                │              │
│  │                                                            │              │
│  │  Products:                                                 │              │
│  │  - tier1_subscription ($6.99/month)                       │              │
│  │  - tier2_subscription ($19.99/month)                      │              │
│  │  - lifetime_tier1_purchase ($49.99)                       │              │
│  │                                                            │              │
│  │  Features:                                                 │              │
│  │  - Real-time pricing                                      │              │
│  │  - Currency conversion                                    │              │
│  │  - Regional pricing                                       │              │
│  │  - Auto-renewable subscriptions                           │              │
│  │  - Non-consumable purchases                               │              │
│  └───────────────────────────────────────────────────────────┘              │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Request Flow (User Opens Premium Screen)

```
┌──────────┐
│  User    │ Opens Premium Screen
└────┬─────┘
     │
     ↓
┌─────────────────────────────┐
│   Premium Screen Widget     │ Currently uses hardcoded prices ❌
│   (UI Layer)                │ Should use: ref.watch(pricingInfoProvider) ✅
└──────────┬──────────────────┘
           │
           │ ref.watch()
           ↓
┌─────────────────────────────┐
│  pricingInfoProvider        │ FutureProvider (Riverpod)
│  (State Management)         │ Status: ✅ ACTIVE
└──────────┬──────────────────┘
           │
           │ async call
           ↓
┌─────────────────────────────┐
│ PremiumSubscriptionManager  │ Business logic
│ getPricingInfo()            │ Status: ✅ IMPLEMENTED
└──────────┬──────────────────┘
           │
           │ checks initialization
           ↓
┌─────────────────────────────┐
│  RevenueCatIntegration      │ Middleware
│  getOfferings()             │ Status: ✅ CONNECTED
└──────────┬──────────────────┘
           │
           │ delegates to
           ↓
┌─────────────────────────────┐
│   RevenueCatService         │ API wrapper
│   getOfferingsData()        │ Status: ✅ COMPLETE
└──────────┬──────────────────┘
           │
           │ SDK call
           ↓
┌─────────────────────────────┐
│  Purchases.getOfferings()   │ RevenueCat SDK
│  (SDK Layer)                │ Status: ✅ INITIALIZED
└──────────┬──────────────────┘
           │
           │ API request
           ↓
┌─────────────────────────────┐
│  Apple App Store API        │ Store backend
│  Google Play API            │ Status: ✅ CONFIGURED
└─────────────────────────────┘
```

---

## Response Flow (Prices Returned)

```
┌─────────────────────────────┐
│  Apple App Store API        │ Returns product info with pricing
└──────────┬──────────────────┘
           │
           │ Response: StoreProduct[]
           ↓
┌─────────────────────────────┐
│  RevenueCat SDK             │ Parses store response
│  Returns: Offerings         │
└──────────┬──────────────────┘
           │
           │ Offerings object
           ↓
┌─────────────────────────────┐
│  RevenueCatService          │ Maps products to tiers
│  Extracts pricing info      │ cosmic/stellar/universe
└──────────┬──────────────────┘
           │
           │ Map<String, dynamic>
           ↓
┌─────────────────────────────┐
│  RevenueCatIntegration      │ Passes through
│  Logs with emoji 📦         │
└──────────┬──────────────────┘
           │
           │ Same map
           ↓
┌─────────────────────────────┐
│ PremiumSubscriptionManager  │ Returns to provider
│ Logs success ✅             │
└──────────┬──────────────────┘
           │
           │ Future completes
           ↓
┌─────────────────────────────┐
│  pricingInfoProvider        │ Notifies listeners
│  State: AsyncValue.data     │
└──────────┬──────────────────┘
           │
           │ Widget rebuild
           ↓
┌─────────────────────────────┐
│  Premium Screen Widget      │ Displays localized prices
│  UI updates with prices     │ $6.99 or €6.99 or £6.99
└─────────────────────────────┘
           │
           ↓
      ┌──────────┐
      │   User   │ Sees accurate pricing
      └──────────┘
```

---

## Error Flow (Network Failure)

```
┌─────────────────────────────┐
│  Apple App Store API        │ ❌ Network error / Timeout
└──────────┬──────────────────┘
           │
           │ Exception thrown
           ↓
┌─────────────────────────────┐
│  RevenueCat SDK             │ Catches error
│  Throws PurchasesError      │
└──────────┬──────────────────┘
           │
           │ Error propagates
           ↓
┌─────────────────────────────┐
│  RevenueCatService          │ Catches in try/catch
│  getOfferingsData()         │ Logs error ❌
│                             │ Returns: _getFallbackPricing()
└──────────┬──────────────────┘
           │
           │ Fallback Map (USD)
           ↓
┌─────────────────────────────┐
│  RevenueCatIntegration      │ Passes through
│  OR throws error            │
└──────────┬──────────────────┘
           │
           │ Fallback or error
           ↓
┌─────────────────────────────┐
│ PremiumSubscriptionManager  │ Catches error
│ getPricingInfo()            │ Logs warning ⚠️
│                             │ Returns: _getFallbackPricing()
└──────────┬──────────────────┘
           │
           │ Fallback Map (USD)
           ↓
┌─────────────────────────────┐
│  pricingInfoProvider        │ Returns fallback data
│  State: AsyncValue.data     │ OR AsyncValue.error
└──────────┬──────────────────┘
           │
           │ Widget rebuild
           ↓
┌─────────────────────────────┐
│  Premium Screen Widget      │ Shows fallback prices
│  .when(                     │ $6.99, $19.99, $49.99
│    data: (d) => prices,     │
│    error: (e, s) => fallback│ ✅ No crash, seamless UX
│  )                          │
└─────────────────────────────┘
           │
           ↓
      ┌──────────┐
      │   User   │ Sees USD fallback prices
      └──────────┘ (Better than no prices!)
```

---

## 4-Layer Fallback System

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: RevenueCat API (Real-time Pricing)            │
│  Status: ✅ Primary source                              │
│  Data: Store prices in user's currency                  │
│  Example: €6.99, £6.99, ¥699                            │
└────────────────┬────────────────────────────────────────┘
                 │ FAIL (network error)
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: RevenueCatService Fallback                    │
│  Status: ✅ Implemented                                 │
│  Data: Hardcoded USD prices                             │
│  Code: _getFallbackPricing() in revenuecat_service.dart│
│  Example: $6.99, $19.99, $49.99                         │
└────────────────┬────────────────────────────────────────┘
                 │ FAIL (service error)
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Manager Fallback                              │
│  Status: ✅ Implemented                                 │
│  Data: Hardcoded USD prices                             │
│  Code: _getFallbackPricing() in manager.dart            │
│  Example: $6.99, $19.99, $49.99                         │
└────────────────┬────────────────────────────────────────┘
                 │ FAIL (all fails)
                 ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: UI Constants (Last Resort)                    │
│  Status: ✅ Always available                            │
│  Data: PricingConstants static values                   │
│  Code: lib/core/pricing/pricing_constants.dart          │
│  Example: $6.99, $19.99, $49.99                         │
└─────────────────────────────────────────────────────────┘
                 │
                 ↓
            ✅ UI ALWAYS SHOWS PRICES
```

---

## Current vs Desired State

### Current Implementation (Hardcoded)

```
Premium Screen
      ↓
PricingConstants (static)
      ↓
Display: "$6.99"
```

**Issues**:
- ❌ No currency localization
- ❌ Cannot update without release
- ❌ May not match store prices

---

### Desired Implementation (Dynamic)

```
Premium Screen
      ↓
ref.watch(pricingInfoProvider)
      ↓
PremiumSubscriptionManager.getPricingInfo()
      ↓
RevenueCatIntegration.getOfferings()
      ↓
RevenueCatService.getOfferingsData()
      ↓
Purchases.getOfferings() (SDK)
      ↓
Apple App Store API
      ↓
Display: "€6.99" (localized!)
```

**Benefits**:
- ✅ Currency localization
- ✅ Always matches store
- ✅ Update via dashboard
- ✅ Regional pricing

---

## Integration Point

### Where the Gap Is

```
┌───────────────────────────────────────────────────────────┐
│                    Premium Screen                          │
│                  (Current Implementation)                  │
│                                                            │
│  Widget build(BuildContext context) {                     │
│    return Column(                                          │
│      children: [                                           │
│        _buildTierCard(                                     │
│          tier: PremiumTier.cosmic,                        │
│          price: PricingConstants.TIER1_PRICE_FORMATTED,   │ ← HARDCODED ❌
│          //              ↑                                 │
│          //              └─── Should be: pricingData?['cosmic']?['price']
│        ),                                                  │
│      ],                                                    │
│    );                                                      │
│  }                                                         │
└───────────────────────────────────────────────────────────┘
                            ↓ NEEDS TO CONNECT TO ↓
┌───────────────────────────────────────────────────────────┐
│              pricingInfoProvider (Already exists!)         │
│              Status: ✅ ACTIVE and WORKING                 │
│                                                            │
│  final pricingInfoProvider =                              │
│    FutureProvider<Map<String, dynamic>?>((ref) async {    │
│      final manager = ref.watch(...);                      │
│      return await manager.getPricingInfo();               │
│    });                                                     │
└───────────────────────────────────────────────────────────┘
```

---

## Product IDs Mapping

```
┌────────────────────────────────────────────────────────────────┐
│              App Store Connect Products                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  tier1_subscription          ($6.99/month)                     │
│  tier2_subscription          ($19.99/month)                    │
│  lifetime_tier1_purchase     ($49.99 one-time)                 │
│                                                                 │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ Configured in RevenueCat Dashboard
                 ↓
┌────────────────────────────────────────────────────────────────┐
│           RevenueCat Dashboard (Entitlements)                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Entitlement: "cosmic"    ← tier1_subscription                │
│  Entitlement: "stellar"   ← tier2_subscription                │
│  Entitlement: "universe"  ← lifetime_tier1_purchase           │
│                                                                 │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ Fetched via SDK
                 ↓
┌────────────────────────────────────────────────────────────────┐
│              RevenueCatService.getOfferingsData()              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Maps products to internal structure:                          │
│                                                                 │
│  if (productId == 'tier1_subscription')                        │
│    tierKey = 'cosmic'                                          │
│                                                                 │
│  if (productId == 'tier2_subscription')                        │
│    tierKey = 'stellar'                                         │
│                                                                 │
│  if (productId == 'lifetime_tier1_purchase')                   │
│    tierKey = 'universe'                                        │
│                                                                 │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 │ Returns structured map
                 ↓
┌────────────────────────────────────────────────────────────────┐
│                    Returned Data Structure                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {                                                              │
│    'cosmic': {                                                 │
│      'price': '$6.99',                                        │
│      'productId': 'tier1_subscription'                        │
│    },                                                          │
│    'stellar': {                                                │
│      'price': '$19.99',                                       │
│      'productId': 'tier2_subscription'                        │
│    },                                                          │
│    'universe': {                                               │
│      'price': '$49.99',                                       │
│      'productId': 'lifetime_tier1_purchase'                   │
│    }                                                           │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Testing Flow

```
┌───────────────────────────────────────────────────────────┐
│  Test 1: Online with Internet                             │
│  Expected: Prices from RevenueCat                         │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  1. User opens Premium Screen                             │
│     ↓                                                      │
│  2. pricingInfoProvider fetches from RevenueCat           │
│     ↓ (1-3 seconds)                                       │
│  3. Real prices loaded: €6.99, €19.99, €49.99            │
│     ↓                                                      │
│  4. UI displays localized prices                          │
│     ✅ SUCCESS                                            │
│                                                            │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  Test 2: Offline Mode (Airplane Mode)                     │
│  Expected: Fallback to USD prices                         │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  1. User enables Airplane Mode                            │
│     ↓                                                      │
│  2. User opens Premium Screen                             │
│     ↓                                                      │
│  3. RevenueCat fetch fails (network error)                │
│     ↓                                                      │
│  4. Fallback pricing returned: $6.99, $19.99, $49.99     │
│     ↓                                                      │
│  5. UI displays fallback prices immediately               │
│     ✅ SUCCESS (no crash, seamless UX)                    │
│                                                            │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  Test 3: Currency Localization                            │
│  Expected: Prices in user's currency                      │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  1. Change device region to EU                            │
│     ↓                                                      │
│  2. Restart app                                            │
│     ↓                                                      │
│  3. Open Premium Screen                                    │
│     ↓                                                      │
│  4. RevenueCat returns EUR prices                         │
│     ↓                                                      │
│  5. UI displays: €6.99, €19.99, €49.99                   │
│     ✅ SUCCESS (localized!)                               │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

---

## Legend

```
✅ = Implemented and working
⚠️ = Needs attention / integration gap
❌ = Not working / missing
📦 = RevenueCat operation
🔄 = Loading / async operation
💰 = Pricing related
🌍 = Localization / regional
```

---

**Architecture Diagram**
**Created**: 2025-10-13
**Version**: 1.0
**Status**: Complete
