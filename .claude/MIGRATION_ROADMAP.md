# 🗺️ MIGRATION ROADMAP - v2.0

**Purpose**: Roadmap for cleaning up deprecated code and completing migrations
**Timeline**: Post v1.0 launch
**Priority**: Tech debt reduction
**Owner**: Engineering Team

---

## 📊 Current State (Oct 6, 2025)

### ✅ Completed Migrations

| Item | Status | Date | Notes |
|------|--------|------|-------|
| RevenueCat Integration | ✅ Complete | Oct 6, 2025 | Production-ready |
| Storage Consolidation | ✅ Complete | Oct 6, 2025 | PreferencesService unified |
| AI Services Integration | ✅ Complete | Oct 6, 2025 | 3 services connected |
| Graceful Degradation | ✅ Complete | Oct 6, 2025 | Documented + monitored |
| Security Hardening | ✅ Complete | Oct 6, 2025 | AppCheck, mocks isolated |

### ⚠️ Pending Migrations

| Item | Affected Files | Priority | Estimated Effort |
|------|----------------|----------|------------------|
| Remove @Deprecated methods | preferences_service.dart, horoscope_service.dart | P2 | 2-4 hours |
| Rewrite premium tests | subscription_payment_test.dart | P1 | 8-12 hours |
| Asset directory cleanup | pubspec.yaml | P3 | 1 hour |
| Evaluate experimental features | 4 services | P2 | 4-6 hours |

---

## 🎯 Phase 1: Deprecated Methods Removal (v2.0)

### Target Date: 2-3 months post v1.0 launch

### Step 1.1: Identify All Usages

```bash
# Find all calls to deprecated methods
grep -r "getUserLanguage\|setSelectedLanguage\|getSelectedLanguage" lib/

# Find all @Deprecated annotations
grep -r "@Deprecated" lib/services/
```

**Expected**: 12 deprecated methods across 2 files

### Step 1.2: Update Callers

**preferences_service.dart** (10 methods):

| Deprecated Method | Replacement | Migration Complexity |
|-------------------|-------------|---------------------|
| `getUserLanguage()` | `userLanguage` getter | Low - direct replacement |
| `setSelectedLanguage()` | `setUserLanguage()` | Low - rename only |
| `getSelectedLanguage()` | `userLanguage` getter | Low - direct replacement |
| `isServiceInitialized()` | `isInitialized` getter | Low - direct replacement |
| `getPreference()` | Use specific getters | Medium - requires context |
| `hasData()` | `isInitialized` | Low - semantic change |
| `getAllData()` | N/A - internal only | Medium - refactor needed |
| `getUserZodiacSign()` | `userZodiacSign` getter | Low - direct replacement |
| `getLanguage()` | `userLanguage` getter | Low - direct replacement |
| `isPremiumUser()` | `isPremium` getter | Low - direct replacement |

**horoscope_service.dart** (2 methods):

| Deprecated Method | Replacement | Migration Complexity |
|-------------------|-------------|---------------------|
| `generateHybridHoroscope()` | `generateDailyHoroscope()` | Low - already delegates |
| `generateInfiniteDailyHoroscope()` | `generateDailyHoroscope()` | Low - already delegates |

### Step 1.3: Remove Deprecated Methods

**Action Plan**:
1. Verify 0 callers with grep
2. Remove method + @Deprecated annotation
3. Run tests
4. Commit per file

**Risk**: Low - all deprecated methods have migration guides

---

## 🧪 Phase 2: Premium Tests Rewrite (v2.0)

### Target Date: 1 month post v1.0 launch

### Current State

**File**: `test/premium/subscription_payment_test.dart`
- **Status**: Entire suite skipped (early return)
- **Reason**: Uses `activatePremium()`/`deactivatePremium()` (removed in RevenueCat migration)
- **Test Count**: 23 tests

### Migration Strategy

#### Option A: RevenueCat SDK Mocking (Recommended)

**Approach**:
1. Use `mockito` or `mocktail` to mock RevenueCat SDK
2. Mock `Purchases.getOfferings()`, `Purchases.purchasePackage()`, etc.
3. Simulate subscription states

**Example**:
```dart
import 'package:mocktail/mocktail.dart';
import 'package:purchases_flutter/purchases_flutter.dart';

class MockPurchases extends Mock implements Purchases {}

void main() {
  group('Premium Payment Processing', () {
    late MockPurchases mockPurchases;
    late SubscriptionService subscriptionService;

    setUp(() {
      mockPurchases = MockPurchases();
      subscriptionService = SubscriptionService();

      // Mock successful purchase
      when(() => mockPurchases.purchasePackage(any()))
          .thenAnswer((_) async => MockCustomerInfo(
                tier: PremiumTier.cosmic,
                isActive: true,
              ));
    });

    test('Should process Essential tier upgrade correctly', () async {
      // Test implementation using mocks
      final result = await subscriptionService.purchaseSubscription('cosmic_monthly');

      expect(result.status, PaymentStatus.completed);
      expect(subscriptionService.currentTier, PremiumTier.cosmic);
    });
  });
}
```

**Pros**:
- Tests real subscription flow
- Validates RevenueCat integration
- Industry-standard testing pattern

**Cons**:
- Requires RevenueCat SDK mocking setup
- More complex than old tests

**Effort**: 8-12 hours

#### Option B: Integration Tests with Sandbox

**Approach**:
1. Use RevenueCat Sandbox environment
2. Real purchases with test cards
3. Integration tests instead of unit tests

**Pros**:
- Tests actual payment flow
- Validates with Apple/Google sandboxes
- High confidence

**Cons**:
- Slower test execution
- Requires sandbox configuration
- Flaky if network issues

**Effort**: 12-16 hours

#### Recommendation: **Option A** (RevenueCat SDK Mocking)

---

## 🗂️ Phase 3: Asset Directory Cleanup (v2.1)

### Target Date: Low priority, anytime

### Current State

**File**: `pubspec.yaml`
- Commented out: `assets/images/`, `assets/icons/`, `assets/sounds/`
- Reason: Directories don't exist

### Options

**Option 1**: Create directories (if planning to use)
```bash
mkdir -p assets/images assets/icons assets/sounds
touch assets/images/.gitkeep
touch assets/icons/.gitkeep
touch assets/sounds/.gitkeep
```

**Option 2**: Remove from pubspec (if not needed)
```yaml
# Simply delete the commented lines
```

**Recommendation**: **Option 1** - Create directories with .gitkeep for future use

**Effort**: 5 minutes

---

## 🔬 Phase 4: Experimental Features Evaluation (v2.0)

### Target Date: 2 months post v1.0 launch

### Services to Evaluate

During audit, found 6 features/services requiring v2.0 backend implementation:

| Feature | Purpose | Current Status | Lines | v2.0 Requirement |
|---------|---------|----------------|-------|------------------|
| `personalized_ai_horoscope_service.dart` | AI-personalized horoscopes | 0 references in UI | ~400 | Complete or remove |
| `astrologer_booking_service.dart` | Book 1-on-1 astrologer | 0 references in UI | ~350 | Complete or remove |
| `crisis_monetization_engine.dart` | Crisis intervention upsells | 0 references in UI | ~280 | Complete or remove |
| `ethical_crisis_support.dart` | Mental health support | 0 references in UI | ~200 | Complete or remove |
| **Historical Timeline** | Personal horoscope history | Returns empty list | ~20 | Backend API: `GET /api/horoscopes/history` |
| **Real-time Compatibility** | Advanced couples analysis | Using basic fallback | ~50 | Backend API: `POST /api/compatibility/calculate` |

### Evaluation Criteria

For each service, answer:
1. **Product Fit**: Does this align with Zodiac Life Coach vision?
2. **User Demand**: Has anyone requested this feature?
3. **ROI**: Revenue potential vs development cost?
4. **Completion**: How much work to make production-ready?
5. **Maintenance**: Ongoing cost to maintain?

### Decision Matrix

| Score | Action |
|-------|--------|
| 4-5/5 | **Complete** - finish implementation and launch |
| 2-3/5 | **Defer** - keep code, revisit in 6 months |
| 0-1/5 | **Remove** - delete to reduce tech debt |

### Example Evaluation: personalized_ai_horoscope_service.dart

1. **Product Fit**: 5/5 - Personalization is core value prop
2. **User Demand**: 3/5 - No explicit requests, but aligns with market
3. **ROI**: 4/5 - Premium feature, high perceived value
4. **Completion**: 60% complete - needs UI integration, testing
5. **Maintenance**: 2/5 - Low ongoing cost (AI handles content)

**Score**: 3.8/5
**Recommendation**: **Complete** - Finish and launch in v2.1

**Effort per service**: 4-6 hours evaluation + variable completion time

---

### Backend API Contracts for v2.0

#### 1. Historical Timeline Endpoint

**Endpoint**: `GET /api/horoscopes/history`

**Query Parameters**:
```typescript
{
  sign: string;        // Zodiac sign (e.g., 'aries', 'taurus')
  days?: number;       // Number of days (default: 30, max: 90)
  language?: string;   // User language (default: 'es')
}
```

**Response**:
```typescript
{
  timeline: Array<{
    date: string;              // ISO 8601 date
    horoscope: string;         // Daily horoscope text
    energy_level: number;      // 0-100
    lucky_numbers: number[];   // Array of lucky numbers
    mood: string;              // Predicted mood
  }>;
  stats: {
    average_energy: number;
    total_days: number;
  };
}
```

**Storage Requirement**: Persistent daily horoscope storage with indexing by sign + date

---

#### 2. Real-time Compatibility Endpoint

**Endpoint**: `POST /api/compatibility/calculate`

**Request Body**:
```typescript
{
  user_sign: string;           // User's zodiac sign
  partner_sign: string;        // Partner's zodiac sign
  include_daily_factors: boolean; // Include today's planetary positions
  language?: string;           // Response language
}
```

**Response**:
```typescript
{
  compatibility_score: number;  // 0-100
  daily_harmony: number;        // Today's harmony level
  communication_flow: number;   // Communication quality
  energy_sync: number;          // Energy alignment
  challenges_today: string[];   // Array of challenge descriptions
  couple_advice: string[];      // Array of advice tips
  planetary_influences: {
    venus_aspect: string;       // Current Venus influence
    mars_aspect: string;        // Current Mars influence
  };
  calculation_timestamp: string; // ISO 8601 timestamp
}
```

**Processing Requirement**: Real-time planetary position calculations + sign compatibility matrix

---

## 📅 Suggested Timeline

### v1.0 Launch (Current)
- ✅ All migrations complete
- ✅ Graceful degradation documented
- ✅ Production-ready

### v1.1 (1 month post-launch)
- 📝 Analytics dashboard for fallback metrics
- 🧪 **Phase 2**: Rewrite premium tests with RevenueCat mocking
- 📊 Evaluate experimental features

### v2.0 (2-3 months post-launch)
- 🗑️ **Phase 1**: Remove 12 @Deprecated methods
- 🔬 **Phase 4**: Complete or remove 4 experimental services
- ♻️ Code quality improvements

### v2.1 (4-5 months post-launch)
- 🗂️ **Phase 3**: Asset directory cleanup
- 🚀 Launch completed experimental features
- 📈 Performance optimizations

---

## ⚠️ Migration Risks & Mitigation

### Risk 1: Breaking Changes

**Scenario**: Removing deprecated methods breaks hidden usages
**Probability**: Low
**Impact**: Medium
**Mitigation**:
- Run comprehensive grep before deletion
- Rely on compile-time errors to catch issues
- Deploy to staging first

### Risk 2: Test Coverage Gaps

**Scenario**: New tests miss edge cases old tests covered
**Probability**: Medium
**Impact**: High
**Mitigation**:
- Port test cases 1:1 from old to new
- Increase integration test coverage
- Beta testing before production

### Risk 3: Resource Constraints

**Scenario**: Team lacks time for v2.0 migrations
**Probability**: Medium
**Impact**: Low
**Mitigation**:
- Migrations are optional (v1.0 works without them)
- Spread work across multiple sprints
- Prioritize P1 items only

---

## 📋 Pre-Migration Checklist

Before starting any migration phase:

- [ ] v1.0 stable in production (0 critical bugs)
- [ ] Analytics dashboard shows <5% fallback usage
- [ ] User retention rate ≥ target
- [ ] Revenue goals met
- [ ] Team has bandwidth (not in crunch mode)
- [ ] Staging environment ready
- [ ] Rollback plan documented

**If any unchecked**: Defer migrations

---

## 📊 Success Metrics

### Phase 1: Deprecated Methods

- [ ] 0 @Deprecated annotations remaining
- [ ] 0 compiler warnings
- [ ] Tests: 100% passing
- [ ] Production: 0 regressions

### Phase 2: Premium Tests

- [ ] 23/23 tests passing
- [ ] Test coverage ≥ 80% for subscription_service.dart
- [ ] CI/CD: All tests run in <5 min
- [ ] RevenueCat mocking: Documented pattern

### Phase 3: Asset Cleanup

- [ ] 0 warnings from `flutter pub get`
- [ ] pubspec.yaml validated
- [ ] Directories exist or removed

### Phase 4: Experimental Features

- [ ] Decision matrix completed (4/4 services)
- [ ] Completed features: Launched or removed
- [ ] Tech debt: Reduced by X lines
- [ ] Documentation: Updated

---

## 🎯 North Star

**Goal**: By v2.0, have a codebase with:
- ✅ Zero deprecated methods
- ✅ 100% passing tests
- ✅ Zero experimental dead code
- ✅ Comprehensive documentation
- ✅ <5% fallback usage
- ✅ Industry-standard patterns

**Why**: Clean code → faster development → better features → happier users → more revenue

---

**Document Owner**: Engineering Lead
**Created**: October 6, 2025
**Last Updated**: October 6, 2025
**Next Review**: Post v1.0 launch (TBD)
**Status**: 📋 **PLANNING** - Execute after v1.0 stable
