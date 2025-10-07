# 🚀 REVENUECAT PRODUCTION DEPLOYMENT GUIDE

## CRITICAL SECURITY IMPLEMENTATION COMPLETE

This guide provides step-by-step instructions for securely deploying RevenueCat in production for the Zodiac App.

## ⚠️ SECURITY SUMMARY

**FIXED ISSUES:**
- ✅ Removed hardcoded API keys from source code
- ✅ Implemented secure environment variable configuration
- ✅ Added production/sandbox environment detection
- ✅ Integrated with existing SecureConfigService
- ✅ Added comprehensive validation and error handling

---

## 📋 PRODUCTION SETUP CHECKLIST

### 1. REVENUCAT ACCOUNT SETUP

#### Create Production RevenueCat Project
- [ ] Sign up for RevenueCat account at [app.revenuecat.com](https://app.revenuecat.com)
- [ ] Create new project: "Zodiac App"
- [ ] Choose appropriate pricing plan (Starter is free up to $10k MRR)

#### Configure iOS App
- [ ] Add iOS app in RevenueCat dashboard
- [ ] Bundle ID: `com.zodiac.app.zodiacApp`
- [ ] Upload App Store Connect API Key or Shared Secret
- [ ] Copy the **iOS API Key** (starts with `appl_`)

#### Configure Android App
- [ ] Add Android app in RevenueCat dashboard
- [ ] Package Name: `com.zodiac.app.zodiac_app`
- [ ] Upload Google Play Service Account JSON
- [ ] Copy the **Android API Key** (starts with `goog_`)

### 2. APP STORE CONNECT CONFIGURATION

#### iOS Products Setup
- [ ] Log into App Store Connect
- [ ] Navigate to your app → Features → In-App Purchases
- [ ] Create Auto-Renewable Subscription:
  - **Product ID**: `zodiac_premium_monthly_trial`
  - **Reference Name**: "Zodiac Premium Monthly with Trial"
  - **Price**: $4.99/month
  - **Free Trial**: 7 days
  - **Subscription Group**: "Zodiac Premium"

#### Configure Subscription Details
- [ ] **Display Name**: "Zodiac Premium"
- [ ] **Description**: "Unlock premium horoscopes, compatibility analysis, and personalized insights"
- [ ] **Promotional Text**: "7-day free trial, then $4.99/month"
- [ ] Add localized descriptions for target markets

### 3. GOOGLE PLAY CONSOLE CONFIGURATION

#### Android Products Setup
- [ ] Log into Google Play Console
- [ ] Navigate to your app → Monetize → Products → Subscriptions
- [ ] Create subscription:
  - **Product ID**: `zodiac.premium.monthly.trial`
  - **Name**: "Zodiac Premium Monthly"
  - **Price**: $4.99/month
  - **Free Trial**: 7 days

#### Configure Subscription Details
- [ ] Set up promotional pricing if needed
- [ ] Configure grace periods and account hold
- [ ] Add appropriate tax settings

### 4. SECURE ENVIRONMENT CONFIGURATION

#### Development Environment Variables
Add to your `.env.development` file:
```bash
# RevenueCat Development/Sandbox Keys
REVENUECAT_IOS_API_KEY=appl_your_development_ios_key_here
REVENUECAT_ANDROID_API_KEY=goog_your_development_android_key_here

# Product IDs (same for both environments)
REVENUECAT_PREMIUM_MONTHLY_IOS=zodiac_premium_monthly_trial
REVENUECAT_PREMIUM_MONTHLY_ANDROID=zodiac.premium.monthly.trial
REVENUECAT_ENTITLEMENT_ID=zodiac_premium_access

# Environment
ENVIRONMENT=development
```

#### Production Environment Variables
For production builds, set these environment variables:
```bash
# RevenueCat Production Keys
REVENUECAT_IOS_API_KEY=appl_your_production_ios_key_here
REVENUECAT_ANDROID_API_KEY=goog_your_production_android_key_here

# Product IDs
REVENUECAT_PREMIUM_MONTHLY_IOS=zodiac_premium_monthly_trial
REVENUECAT_PREMIUM_MONTHLY_ANDROID=zodiac.premium.monthly.trial
REVENUECAT_ENTITLEMENT_ID=zodiac_premium_access

# Environment
ENVIRONMENT=production
```

### 5. BUILD CONFIGURATION

#### Flutter Build Commands

**Development Build:**
```bash
flutter build ios --flavor development --dart-define=ENVIRONMENT=development
flutter build apk --flavor development --dart-define=ENVIRONMENT=development
```

**Production Build:**
```bash
flutter build ios --release --dart-define=ENVIRONMENT=production --dart-define=REVENUECAT_IOS_API_KEY=appl_your_production_key
flutter build apk --release --dart-define=ENVIRONMENT=production --dart-define=REVENUECAT_ANDROID_API_KEY=goog_your_production_key
```

#### CI/CD Environment Variables
Set these in your CI/CD system (GitHub Actions, Firebase App Distribution, etc.):

```yaml
# Production secrets
REVENUECAT_IOS_API_KEY: ${{ secrets.REVENUECAT_IOS_API_KEY }}
REVENUECAT_ANDROID_API_KEY: ${{ secrets.REVENUECAT_ANDROID_API_KEY }}
ENVIRONMENT: production
```

### 6. REVENUCAT DASHBOARD CONFIGURATION

#### Create Entitlement
- [ ] Go to RevenueCat Dashboard → Entitlements
- [ ] Create entitlement: `zodiac_premium_access`
- [ ] Attach iOS product: `zodiac_premium_monthly_trial`
- [ ] Attach Android product: `zodiac.premium.monthly.trial`

#### Configure Offerings
- [ ] Go to Offerings section
- [ ] Create offering: "Premium"
- [ ] Add monthly package with 7-day trial
- [ ] Set as default offering

#### Configure Webhooks (Optional)
- [ ] Set up webhook endpoint for subscription events
- [ ] Configure webhook URL in RevenueCat dashboard
- [ ] Test webhook delivery

### 7. TESTING CHECKLIST

#### Development Testing
- [ ] Test subscription purchase flow
- [ ] Test free trial activation
- [ ] Test restore purchases functionality
- [ ] Test subscription expiry handling
- [ ] Test offline mode behavior

#### Sandbox Testing (iOS)
- [ ] Create sandbox test accounts
- [ ] Test complete purchase flow
- [ ] Test subscription renewal
- [ ] Test subscription cancellation
- [ ] Test receipt validation

#### Google Play Testing (Android)
- [ ] Set up internal testing track
- [ ] Upload signed APK
- [ ] Test with licensed test accounts
- [ ] Test subscription lifecycle
- [ ] Test Google Play billing

### 8. PRODUCTION VALIDATION

#### Pre-Launch Validation
- [ ] Verify API keys are correctly configured
- [ ] Confirm product IDs match store configuration
- [ ] Test builds with production configuration
- [ ] Validate certificate pinning (if configured)
- [ ] Perform security audit

#### Launch Day Checklist
- [ ] Monitor RevenueCat dashboard for events
- [ ] Watch for subscription purchase notifications
- [ ] Monitor app crash reports
- [ ] Check revenue analytics
- [ ] Monitor customer support channels

---

## 🔐 SECURITY BEST PRACTICES

### API Key Security
1. **Never commit API keys to version control**
2. **Use environment variables for all builds**
3. **Rotate keys regularly (quarterly recommended)**
4. **Use different keys for development and production**
5. **Monitor key usage in RevenueCat dashboard**

### Configuration Validation
The app now includes automatic validation that:
- ✅ Ensures API keys are properly formatted
- ✅ Validates product IDs are configured
- ✅ Prevents production builds with invalid config
- ✅ Uses secure configuration service

### Environment Detection
The app automatically detects:
- ✅ Debug vs Release builds
- ✅ Development vs Production environment
- ✅ Sandbox vs Production RevenueCat environment

---

## 🚨 CRITICAL SECURITY WARNINGS

1. **NEVER hardcode production API keys in source code**
2. **Always use HTTPS for all API communications**
3. **Validate all subscription receipts server-side**
4. **Monitor for suspicious purchase patterns**
5. **Implement proper error handling for payment failures**

---

## 📊 MONITORING & ANALYTICS

### RevenueCat Dashboard Monitoring
- Monitor Monthly Recurring Revenue (MRR)
- Track conversion rates from trial to paid
- Monitor churn rates and retention
- Watch for refund patterns

### App Analytics Integration
The secure configuration supports:
- Firebase Analytics integration
- Custom subscription events
- Trial conversion tracking
- Revenue attribution

---

## 🛠️ TROUBLESHOOTING

### Common Issues

**"RevenueCat API key not configured"**
- Verify environment variables are set correctly
- Check build command includes necessary --dart-define flags
- Confirm API key format (iOS: appl_, Android: goog_)

**"Product ID not found"**
- Verify product IDs match exactly in stores
- Ensure products are approved and active
- Check RevenueCat entitlement configuration

**"Receipt validation failed"**
- Verify App Store Connect API key or shared secret
- Check Google Play service account permissions
- Ensure products are live in production

### Support Resources
- RevenueCat Documentation: [docs.revenuecat.com](https://docs.revenuecat.com)
- RevenueCat Support: support@revenuecat.com
- Community Discord: [discord.gg/revenuecat](https://discord.gg/revenuecat)

---

## ✅ DEPLOYMENT READY CONFIRMATION

When all items above are completed:

- [ ] All API keys configured securely
- [ ] Products created and approved in both stores
- [ ] RevenueCat entitlements configured
- [ ] Testing completed in all environments
- [ ] Production builds validated
- [ ] Monitoring setup complete

**The app is now ready for production deployment with secure RevenueCat integration!**

---

*Generated with secure configuration best practices for Zodiac App production deployment.*