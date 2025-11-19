# 💎 PREMIUM TESTING CHECKLIST - Revenue Critical

**Objetivo**: Verificación exhaustiva de todos los flujos premium para garantizar 0% revenue loss
**Prioridad**: CRÍTICA - Cualquier error afecta directamente ingresos
**Última actualización**: 2025-10-05

---

## 🎯 FASE 1: Purchase Flows (Flujos de Compra)

### 1.1 Essential Tier Purchase ($4.99/mes)

#### Pre-compra
- [ ] Paywall se muestra correctamente con precio $4.99
- [ ] Descripción de features es clara y precisa
- [ ] Botón de compra está habilitado
- [ ] Loading state durante purchase request

#### Durante compra
- [ ] Sheet de pago de Apple/Google se abre
- [ ] Precio mostrado coincide: $4.99
- [ ] Método de pago se puede seleccionar
- [ ] Confirmación de compra funciona
- [ ] Loading indicator visible durante procesamiento

#### Post-compra
- [ ] Success message se muestra
- [ ] `isPremium` = true inmediatamente
- [ ] `getCurrentSubscriptionType()` = SubscriptionType.essential
- [ ] Subscription date registrada correctamente
- [ ] Features premium se desbloquean de inmediato
- [ ] UI actualiza para mostrar estado premium
- [ ] Analytics event `purchase_completed` disparado

**Revenue Validation**:
```dart
expect(SubscriptionService.subscriptionPrices[SubscriptionType.essential], 4.99);
expect(subscriptionService.isPremium, isTrue);
```

---

### 1.2 Advanced Tier Purchase ($9.99/mes)

#### Pre-compra
- [ ] Paywall muestra $9.99 correctamente
- [ ] Features adicionales vs Essential mostradas
- [ ] Badge "Most Popular" visible (si aplica)
- [ ] Upgrade desde Essential habilitado

#### Durante compra
- [ ] Apple/Google sheet con precio $9.99
- [ ] Purchase flow sin errores
- [ ] RevenueCat purchase request exitoso

#### Post-compra
- [ ] `getCurrentSubscriptionType()` = SubscriptionType.advanced
- [ ] Features de Essential + Advanced desbloqueadas
- [ ] Precio correcto en analytics: $9.99
- [ ] Si es upgrade: features previas se mantienen

**Upgrade Test**:
```dart
// Usuario con Essential upgrade a Advanced
expect(previousTier, SubscriptionType.essential);
expect(newTier, SubscriptionType.advanced);
expect(additionalRevenue, 5.00); // $9.99 - $4.99
```

---

### 1.3 Master Tier Purchase ($19.99/mes)

#### Pre-compra
- [ ] Precio $19.99 mostrado
- [ ] Features exclusivas de Master tier listadas
- [ ] AI Cosmic Coach incluido en features
- [ ] Upgrade path desde Advanced claro

#### Durante compra
- [ ] Sheet de pago muestra $19.99
- [ ] Purchase procesa correctamente
- [ ] Loading states apropiados

#### Post-compra
- [ ] Tier = SubscriptionType.master
- [ ] AI Cosmic Coach desbloqueado
- [ ] Todas las features previas + Master activas
- [ ] Analytics correctos

**Features Validation**:
- [ ] AI Cosmic Coach accessible
- [ ] Unlimited horoscopes
- [ ] Advanced compatibility
- [ ] Priority support visible

---

### 1.4 Cosmic VIP Tier Purchase ($49.99/mes)

#### Pre-compra
- [ ] Precio $49.99 destacado
- [ ] Features VIP exclusivas listadas
- [ ] "Astrologer Consultations" incluido
- [ ] Badge "Premium" visible

#### Durante compra
- [ ] Purchase flow para tier más alto
- [ ] Precio $49.99 en payment sheet
- [ ] Confirmación adicional (optional)

#### Post-compra
- [ ] Tier = SubscriptionType.cosmicVip
- [ ] Acceso a astrólogos desbloqueado
- [ ] Todas las features disponibles
- [ ] VIP badge en perfil

**VIP Features**:
- [ ] Astrologer consultations scheduling
- [ ] Personalized reports
- [ ] Priority AI coaching
- [ ] Exclusive content access

---

### 1.5 Lifetime Purchase ($199.99 one-time)

#### Pre-compra
- [ ] Precio $199.99 one-time mostrado
- [ ] "Lifetime Access" claramente indicado
- [ ] Value proposition vs monthly claro
- [ ] "One-time payment, forever access" visible

#### Durante compra
- [ ] Payment sheet muestra $199.99 one-time
- [ ] No subscription, compra única
- [ ] Terms of lifetime access claros

#### Post-compra
- [ ] Tier = SubscriptionType.lifetime
- [ ] `getDaysRemaining()` = -1 (unlimited)
- [ ] `isMonthlySubscriptionExpired()` = false (always)
- [ ] Lifetime badge en perfil
- [ ] Todas las features desbloqueadas permanentemente

**Lifetime Validation**:
```dart
expect(tier, SubscriptionType.lifetime);
expect(daysRemaining, -1); // Unlimited
expect(price, 199.99);
expect(isRecurring, false);
```

---

## 🔄 FASE 2: Restore Flows (Restauración)

### 2.1 Restore After Reinstall

#### Setup
1. Usuario con subscription activa
2. Desinstalar app completamente
3. Reinstalar app
4. Login con misma cuenta

#### Testing
- [ ] Botón "Restore Purchases" visible en paywall
- [ ] Tap en "Restore Purchases"
- [ ] RevenueCat fetch purchases ejecuta
- [ ] Premium status restaurado correctamente
- [ ] Tier correcto restaurado
- [ ] Features desbloqueadas inmediatamente
- [ ] UI actualiza a estado premium
- [ ] Subscription date preservada

**Validation**:
```dart
expect(restoredTier, originalTier);
expect(isPremium, isTrue);
expect(features, containsAll(originalFeatures));
```

---

### 2.2 Restore on New Device

#### Setup
1. Usuario con subscription en Device A
2. Login en Device B (nuevo)
3. App en estado free

#### Testing
- [ ] "Restore Purchases" disponible
- [ ] Restore ejecuta correctamente
- [ ] RevenueCat sincroniza desde servidor
- [ ] Premium status aplicado en Device B
- [ ] Same tier en ambos dispositivos
- [ ] Features sincronizadas
- [ ] Subscription info coherente

**Cross-Device Validation**:
- [ ] Device A: isPremium = true
- [ ] Device B: isPremium = true (after restore)
- [ ] Same expiry date en ambos
- [ ] Same features access

---

### 2.3 Restore with Expired Subscription

#### Setup
1. Subscription expirada (>30 días)
2. Usuario intenta restore

#### Testing
- [ ] Restore detecta subscription expirada
- [ ] Message claro: "Subscription expired"
- [ ] Option para renovar mostrada
- [ ] isPremium = false
- [ ] Features bloqueadas
- [ ] Prompt para re-subscribe

**Expected Behavior**:
```dart
expect(isExpired, isTrue);
expect(isPremium, isFalse);
expect(daysRemaining, 0);
expect(showRenewalPrompt, isTrue);
```

---

### 2.4 Restore with Active Subscription

#### Setup
1. Subscription activa (dentro de 30 días)
2. Usuario hace restore

#### Testing
- [ ] Restore exitoso
- [ ] Premium status activo
- [ ] Days remaining calculados correctamente
- [ ] No cobro adicional
- [ ] Features mantienen acceso
- [ ] Subscription date correcta

**Active Subscription Check**:
```dart
expect(isPremium, isTrue);
expect(daysRemaining, greaterThan(0));
expect(daysRemaining, lessThanOrEqualTo(30));
```

---

## 🆓 FASE 3: Free Trial Flows

### 3.1 Trial Activation (7 días)

#### Pre-trial
- [ ] Usuario nunca usó trial (`hasUsedTrial()` = false)
- [ ] `canActivateFreeTrial()` = true
- [ ] Banner de trial visible
- [ ] "Start 7-Day Free Trial" button habilitado

#### During activation
- [ ] Tap en "Start Trial"
- [ ] Loading state visible
- [ ] No payment required
- [ ] Trial activado instantáneamente

#### Post-activation
- [ ] `getCurrentSubscriptionType()` = SubscriptionType.trial
- [ ] `isPremium` = true
- [ ] `hasUsedTrial()` = true
- [ ] Trial start date registrada
- [ ] `getDaysRemaining()` = 6-7 días
- [ ] Premium features desbloqueadas
- [ ] Trial badge visible en UI
- [ ] Analytics event `trial_started` disparado

**Trial Validation**:
```dart
expect(tier, SubscriptionType.trial);
expect(isPremium, isTrue);
expect(daysRemaining, inInclusiveRange(6, 7));
expect(hasUsedTrial, isTrue);
```

---

### 3.2 Trial Expiration

#### Setup
1. Usuario con trial activo
2. Simular paso de 7 días

#### Testing
- [ ] `isTrialExpired()` = true después de 7 días
- [ ] `isPremium` = false automáticamente
- [ ] Features premium bloqueadas
- [ ] Prompt para subscribe mostrado
- [ ] "Your trial has ended" message claro
- [ ] CTA para purchase visible

**Expiration Check**:
```dart
expect(isTrialExpired, isTrue);
expect(isPremium, isFalse);
expect(daysRemaining, 0);
```

---

### 3.3 Trial to Paid Conversion

#### Setup
1. Usuario en trial (día 3-5)
2. Decide comprar subscription

#### Testing
- [ ] Purchase flow desde trial funciona
- [ ] Trial termina inmediatamente
- [ ] Paid subscription inicia
- [ ] `hasUsedTrial()` = true (preserved)
- [ ] New subscription date registrada
- [ ] Analytics: `trial_converted` disparado
- [ ] Conversion tracking preciso

**Conversion Validation**:
```dart
expect(previousTier, SubscriptionType.trial);
expect(newTier, SubscriptionType.essential); // o superior
expect(conversionRate, recorded);
```

---

### 3.4 Prevent Second Trial

#### Setup
1. Usuario ya usó trial (`hasUsedTrial()` = true)
2. Deactivate premium
3. Intenta activar trial de nuevo

#### Testing
- [ ] `canActivateFreeTrial()` = false
- [ ] "Start Trial" button disabled/hidden
- [ ] Message: "Trial already used"
- [ ] Solo option es paid subscription
- [ ] `activateFreeTrial()` retorna false
- [ ] Tier permanece en free

**Second Trial Prevention**:
```dart
expect(hasUsedTrial, isTrue);
expect(canActivateFreeTrial, isFalse);
expect(activateTrialResult, isFalse);
expect(tier, SubscriptionType.free);
```

---

## ⬆️ FASE 4: Upgrade/Downgrade Flows

### 4.1 Tier Upgrades

#### Essential → Advanced
- [ ] Upgrade option visible
- [ ] Precio diferencial mostrado: $5.00/mes
- [ ] "Upgrade to Advanced" CTA claro
- [ ] Purchase flow ejecuta
- [ ] Tier actualiza a Advanced
- [ ] Features adicionales desbloqueadas
- [ ] Revenue potential: +$5.00/mes

#### Advanced → Master
- [ ] Upgrade visible con features Master
- [ ] Precio diferencial: $10.00/mes
- [ ] AI Cosmic Coach preview mostrado
- [ ] Upgrade procesa correctamente
- [ ] Master tier activo
- [ ] Revenue: +$10.00/mes

#### Master → Cosmic VIP
- [ ] Upgrade a VIP visible
- [ ] Precio diferencial: $30.00/mes
- [ ] Astrologer access preview
- [ ] VIP tier se activa
- [ ] Todas las features VIP desbloqueadas
- [ ] Revenue: +$30.00/mes

**Upgrade Validation**:
```dart
final revenuePotential = getUpgradeRevenuePotential();
expect(revenuePotential, greaterThan(0));
expect(newTier.level, greaterThan(oldTier.level));
```

---

### 4.2 Tier Hierarchy

#### Testing
- [ ] Free (0) < Trial (1) < Essential (2) < Advanced (3) < Master (4) < Cosmic VIP (5) < Lifetime (6)
- [ ] `getTierLevel()` retorna valores correctos
- [ ] `canAccessTier(tier)` respeta jerarquía
- [ ] Features gating por tier funciona
- [ ] No downgrade automático sin usuario action

**Hierarchy Check**:
```dart
expect(getTierLevel(SubscriptionType.free), 0);
expect(getTierLevel(SubscriptionType.essential), 2);
expect(getTierLevel(SubscriptionType.lifetime), 6);
```

---

### 4.3 Next Tier Suggestions

#### Testing para cada tier
- [ ] Free user: suggested = Essential
- [ ] Essential user: suggested = Advanced
- [ ] Advanced user: suggested = Master
- [ ] Master user: suggested = Cosmic VIP
- [ ] Cosmic VIP user: suggested = Lifetime
- [ ] Lifetime user: suggested = null (no next tier)

**Upsell Logic**:
```dart
expect(getNextTier(free), SubscriptionType.essential);
expect(getNextTier(lifetime), isNull);
```

---

## 📊 FASE 5: Pricing & Revenue Validation

### 5.1 Price Accuracy

#### Tier Prices
- [ ] Free: $0.00 ✓
- [ ] Trial: $0.00 ✓
- [ ] Essential: $4.99 ✓
- [ ] Advanced: $9.99 ✓
- [ ] Master: $19.99 ✓
- [ ] Cosmic VIP: $49.99 ✓
- [ ] Lifetime: $199.99 ✓

**Price Validation**:
```dart
expect(prices[SubscriptionType.essential], 4.99);
expect(prices[SubscriptionType.advanced], 9.99);
expect(prices[SubscriptionType.master], 19.99);
expect(prices[SubscriptionType.cosmicVip], 49.99);
expect(prices[SubscriptionType.lifetime], 199.99);
```

---

### 5.2 Revenue Calculations

#### Upgrade Revenue Potential
- [ ] Essential → Advanced: $5.00
- [ ] Advanced → Master: $10.00
- [ ] Master → Cosmic VIP: $30.00
- [ ] Cálculos precisos al centavo

#### Lifetime Value (LTV)
- [ ] Essential: $4.99/mes → $59.88/año
- [ ] Advanced: $9.99/mes → $119.88/año
- [ ] Master: $19.99/mes → $239.88/año
- [ ] Cosmic VIP: $49.99/mes → $599.88/año
- [ ] Lifetime: $199.99 one-time

**Revenue Accuracy**:
```dart
expect(calculateUpgradeRevenue(Essential, Advanced), 5.00);
expect(calculateLTV(Essential, 12), 59.88);
```

---

### 5.3 Currency & Localization

#### Pricing Display
- [ ] USD: $4.99
- [ ] EUR: €4.99 (si aplica)
- [ ] GBP: £4.99 (si aplica)
- [ ] Símbolos de moneda correctos
- [ ] Formateo regional (decimal separator)

#### RevenueCat Currency
- [ ] Precio se obtiene de RevenueCat en moneda local
- [ ] Conversión automática si es necesario
- [ ] Display formateado según locale

---

## 🔒 FASE 6: Feature Gating & Access Control

### 6.1 Free Tier Features

#### Allowed
- [ ] Daily horoscope (1 per day)
- [ ] Basic compatibility check
- [ ] Zodiac sign info
- [ ] Basic profile

#### Blocked (Paywall shown)
- [ ] Weekly horoscopes
- [ ] Monthly horoscopes
- [ ] Advanced compatibility
- [ ] AI Cosmic Coach
- [ ] Unlimited horoscopes
- [ ] Astrologer consultations

**Feature Gate Check**:
```dart
expect(isFeatureAvailable('daily_horoscope'), isTrue);
expect(isFeatureAvailable('ai_cosmic_coach'), isFalse);
```

---

### 6.2 Essential Tier Features

#### Unlocked from Free
- [ ] Unlimited daily horoscopes
- [ ] Weekly horoscopes
- [ ] Monthly horoscopes
- [ ] Detailed compatibility reports
- [ ] No ads

#### Still Blocked
- [ ] AI Cosmic Coach (Master+)
- [ ] Astrologer consultations (Cosmic VIP+)
- [ ] Advanced predictions (Master+)

---

### 6.3 Advanced Tier Features

#### Additional vs Essential
- [ ] Enhanced compatibility insights
- [ ] Personalized daily insights
- [ ] Birth chart analysis
- [ ] Transit predictions

---

### 6.4 Master Tier Features

#### Exclusive Features
- [ ] AI Cosmic Coach full access
- [ ] Advanced astrological predictions
- [ ] Personalized coaching sessions
- [ ] Priority customer support

---

### 6.5 Cosmic VIP Features

#### VIP Exclusives
- [ ] 1-on-1 Astrologer consultations
- [ ] Personalized yearly reports
- [ ] VIP-only content
- [ ] Early access to new features
- [ ] Dedicated support line

---

### 6.6 Lifetime Features

#### All Features Forever
- [ ] Everything from all tiers
- [ ] No expiration
- [ ] Future features included (within reason)
- [ ] Lifetime VIP status

---

## 📱 FASE 7: Subscription Management

### 7.1 Expiry Detection

#### Monthly Subscriptions
- [ ] Detecta expiración después de 30 días
- [ ] `isMonthlySubscriptionExpired()` = true
- [ ] `isPremium` = false automáticamente
- [ ] `getDaysRemaining()` = 0
- [ ] Prompt para renovar mostrado

#### Active Window
- [ ] Subscription dentro de 30 días = activo
- [ ] Days remaining calculados correctamente
- [ ] Countdown visible en settings
- [ ] Renewal reminder 3 días antes

**Expiry Check**:
```dart
// Fresh subscription
expect(isExpired, isFalse);
expect(daysRemaining, greaterThan(25));

// 35-day old subscription
expect(isExpired, isTrue);
expect(daysRemaining, 0);
```

---

### 7.2 Cancellation Handling

#### User Cancels via App Store/Play Store
- [ ] RevenueCat webhook notifica cancellation
- [ ] Subscription permanece activa hasta final de período
- [ ] No immediate loss de acceso
- [ ] "Cancelled" badge visible
- [ ] Renewal prompt al acercarse fin
- [ ] Grace period si se re-subscribe

#### Immediate Cancellation (si aplica)
- [ ] Premium access termina inmediatamente
- [ ] Features bloqueadas
- [ ] Refund processing (si aplicable)

---

### 7.3 Subscription Info Display

#### Settings Screen
- [ ] Current tier mostrado claramente
- [ ] Monthly price visible
- [ ] Next billing date (si aplica)
- [ ] Days remaining countdown
- [ ] "Manage Subscription" link a App Store/Play Store
- [ ] "Cancel Subscription" option visible

**Info Validation**:
```dart
final info = getSubscriptionInfo();
expect(info['subscriptionType'], 'advanced');
expect(info['daysRemaining'], greaterThan(0));
expect(info['nextBillingDate'], isNotNull);
```

---

## 🧪 FASE 8: Edge Cases & Error Handling

### 8.1 Network Failures

#### During Purchase
- [ ] Network error durante purchase
- [ ] Error message claro al usuario
- [ ] Retry option disponible
- [ ] No phantom charges
- [ ] State revierte a pre-purchase

#### During Restore
- [ ] Network error durante restore
- [ ] "Cannot connect" message
- [ ] Offline mode activado
- [ ] Retry cuando network vuelve

---

### 8.2 RevenueCat Errors

#### API Errors
- [ ] 400 Bad Request: Message claro
- [ ] 401 Unauthorized: Re-auth prompt
- [ ] 500 Server Error: Retry logic
- [ ] Timeout: Loading con timeout message

#### Invalid Receipts
- [ ] Receipt inválido detectado
- [ ] No premium access otorgado
- [ ] User informado del issue
- [ ] Support contact mostrado

---

### 8.3 Concurrent Operations

#### Simultaneous Purchases
- [ ] Purchase lock previene duplicados
- [ ] Solo una purchase a la vez
- [ ] Queue si múltiples requests
- [ ] Final state consistente

#### Race Conditions
- [ ] Restore + Purchase simultáneo
- [ ] Multiple restore requests
- [ ] State consistency garantizada
- [ ] No corruption de datos

---

### 8.4 App Updates

#### After App Update
- [ ] Premium status preserved
- [ ] Tier correcto mantenido
- [ ] Features access intacto
- [ ] Subscription date preserved
- [ ] No re-authentication requerida

#### Migration Handling
- [ ] Data migration exitosa
- [ ] Backward compatibility
- [ ] No loss de subscription info

---

## 📊 FASE 9: Analytics & Tracking

### 9.1 Purchase Analytics

#### Events to Track
- [ ] `paywall_shown` (tier, context)
- [ ] `purchase_initiated` (tier, price)
- [ ] `purchase_completed` (tier, revenue)
- [ ] `purchase_failed` (tier, error)
- [ ] `purchase_cancelled` (tier, step)

#### Revenue Metrics
- [ ] Total revenue por tier
- [ ] Average revenue per user (ARPU)
- [ ] Lifetime value (LTV) por tier
- [ ] Conversion rate por tier
- [ ] Upgrade revenue tracking

---

### 9.2 Trial Analytics

#### Trial Events
- [ ] `trial_started`
- [ ] `trial_converted` (target_tier)
- [ ] `trial_expired`
- [ ] `trial_abandoned` (day)

#### Trial Metrics
- [ ] Trial activation rate
- [ ] Trial to paid conversion rate
- [ ] Average conversion day (1-7)
- [ ] Conversion by feature usage

---

### 9.3 User Journey Analytics

#### Funnel Tracking
- [ ] App install → Onboarding
- [ ] Onboarding → Paywall view
- [ ] Paywall view → Purchase
- [ ] Free → Trial → Paid

#### Drop-off Analysis
- [ ] Identify donde usuarios abandonan
- [ ] A/B test paywall variations
- [ ] Optimize conversion points

---

## ✅ Test Execution Protocol

### Pre-Test Setup
1. [ ] Clean app install
2. [ ] Fresh RevenueCat sandbox account
3. [ ] Valid test payment methods
4. [ ] Analytics monitoring active
5. [ ] Screen recording enabled

### During Testing
1. [ ] Check cada item en checklist
2. [ ] Screenshot de estados críticos
3. [ ] Log errors encontrados
4. [ ] Note performance issues
5. [ ] Validate analytics events

### Post-Test Validation
1. [ ] Review analytics data
2. [ ] Verify revenue calculations
3. [ ] Check for data leaks
4. [ ] Validate error handling
5. [ ] Document findings

---

## 🚨 Critical Issues - Immediate Fix Required

### Revenue Impact Issues
- ⛔ Purchase completa pero `isPremium` = false
- ⛔ Precio incorrecto mostrado/cobrado
- ⛔ Restore falla con subscription activa
- ⛔ Features premium accesibles sin pago
- ⛔ Phantom charges o double charging

### Data Integrity Issues
- ⚠️ Subscription date no se guarda
- ⚠️ Tier level inconsistente
- ⚠️ Features gating no funciona
- ⚠️ Analytics events no disparan

---

## 📈 Success Criteria

### Must Pass (100%)
- ✅ Todos los purchase flows funcionan
- ✅ Restore funciona en todos los escenarios
- ✅ Trial activation y expiry correctos
- ✅ Pricing exacto en todos los tiers
- ✅ Feature gating funciona perfectamente
- ✅ Revenue tracking preciso al centavo

### Should Pass (95%+)
- ✅ Error handling robusto
- ✅ Analytics completos
- ✅ Edge cases manejados
- ✅ Performance aceptable (<2s purchase)

---

## 📝 Test Report Template

```markdown
# Premium Testing Report
**Tester**: [Name]
**Date**: [Date]
**App Version**: [Version]
**Environment**: [Sandbox/Production]

## Test Results
- Purchase Flows: ✅/⚠️/❌
- Restore Flows: ✅/⚠️/❌
- Trial Flows: ✅/⚠️/❌
- Feature Gating: ✅/⚠️/❌
- Analytics: ✅/⚠️/❌

## Issues Found
1. [Issue description]
   - Severity: Critical/High/Medium/Low
   - Steps to reproduce
   - Expected vs Actual behavior
   - Screenshots/Logs

## Recommendations
- [Action items]
- [Priority fixes]
- [Future improvements]
```

---

**Status**: ⏳ PENDING EXECUTION
**Priority**: 🔴 CRITICAL - Revenue Impact
**Owner**: QA Team
**Est. Time**: 8-12 hours complete testing
