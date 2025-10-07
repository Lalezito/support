# 🍎 APP STORE CONNECT SETUP GUIDE - ZODIAC LIFE COACH

**FECHA**: 26 de Agosto 2025  
**VERSIÓN**: 1.0  
**OBJETIVO**: Resolver IAP Issues (Guideline 2.1) y configurar productos correctamente

---

## 📋 CHECKLIST CRÍTICO PARA APP STORE APPROVAL

### ✅ **FASE 1: PAID APPS AGREEMENT (CRÍTICO)**

1. **Navegar a App Store Connect**:
   - Ir a https://appstoreconnect.apple.com
   - Iniciar sesión con cuenta de desarrollador

2. **Acceder a Agreements, Tax, and Banking**:
   ```
   App Store Connect → Agreements, Tax, and Banking
   ```

3. **Firmar Paid Apps Agreement**:
   - Buscar "Paid Applications"
   - Status debe estar "Active"
   - Si no está firmado: Click "Request" → Completar formulario
   - **IMPORTANTE**: Sin esto firmado, NO se pueden cargar productos

4. **Configurar información fiscal**:
   - Completar Tax Information
   - Agregar Banking Information (para recibir pagos)
   - **NOTA**: Puede tomar 24-48 horas en activarse

---

## 2. 📱 IN-APP PURCHASE CONFIGURATION

### Setup Monthly Subscription ($4.99):
1. In App Store Connect → Your App → Features → In-App Purchases
2. Click **+** to create new subscription
3. Configure:
   - **Product ID**: `zodiac_pro_monthly`
   - **Reference Name**: Zodiac Premium Monthly
   - **Subscription Group**: Create new "Zodiac Premium"
   - **Duration**: 1 Month
   - **Price**: $4.99 USD
   - **Subscription Group Display Name**: Zodiac Premium Access
   - **App Store Review Information**: Add screenshot + review notes

### Setup Lifetime Purchase ($49.99):
1. Click **+** to create new in-app purchase
2. Configure:
   - **Type**: Non-Consumable
   - **Product ID**: `zodiac_premium_lifetime`
   - **Reference Name**: Zodiac Premium Lifetime
   - **Price**: $49.99 USD

### ⚠️ Required Content:
- Add localized descriptions for all supported languages
- Upload subscription screenshots showing premium features
- Configure auto-renewable subscription terms
- Set up promotional offers (optional)

---

## 3. 🧪 SANDBOX TESTING CONFIGURATION

### Create Test Accounts:
1. Go to **Users and Roles** → **Sandbox Testers**
2. Create test accounts:
   - US tester: test-us@zodiacapp.com
   - EU tester: test-eu@zodiacapp.com
   - Test different payment scenarios

### Test Scenarios Required:
- [ ] Successful monthly subscription purchase
- [ ] Successful lifetime purchase  
- [ ] Subscription cancellation
- [ ] Subscription restoration
- [ ] Failed payment handling
- [ ] Receipt validation
- [ ] Offline purchase restoration

---

## 4. 📋 APP REVIEW PREPARATION

### Required for Submission:
- [ ] All in-app purchases configured and approved
- [ ] Subscription terms clearly displayed in app
- [ ] Terms of Use and Privacy Policy accessible
- [ ] EULA included and linked
- [ ] Subscription management instructions provided
- [ ] Auto-renewal terms disclosed

### Review Notes Template:
```
This app offers premium astrology features through subscriptions:

MONTHLY SUBSCRIPTION ($4.99/month):
- Auto-renewable monthly subscription
- Advanced AI coaching features
- Full access to predictive astrology
- Smart journaling with pattern analysis

LIFETIME PURCHASE ($49.99):
- One-time purchase for permanent premium access
- All monthly features included forever

TESTING INSTRUCTIONS:
- Use sandbox test account: [test account email]
- Premium features are accessible after purchase
- Terms and Privacy Policy available in Premium screen
- Subscription management through iOS Settings

The app includes proper subscription disclosures and Terms of Use as required by App Store Guidelines 3.1.2.
```

---

## 5. 🔧 BACKEND REQUIREMENTS

### Receipt Validation Service:
Current implementation uses mock validation. For production:

1. **Set up server endpoint** for receipt validation
2. **Configure SSL certificate** for secure communication  
3. **Implement receipt verification** with Apple's servers
4. **Set up database** for purchase tracking
5. **Configure webhook** for subscription status updates

### Server Architecture:
```
iOS App → Your Backend → Apple Verification Server
    ↓         ↓              ↓
Receipt → Validation → Subscription Status
```

---

## 📞 SUPPORT INFORMATION

### Contact Details (Update before submission):
- **Support Email**: support@zodiaclifecoach.app
- **Privacy Policy URL**: https://zodiaclifecoach.app/privacy
- **Terms of Use URL**: https://zodiaclifecoach.app/terms
- **App Website**: https://zodiaclifecoach.app

---

## ✅ SUBMISSION CHECKLIST

Before submitting for review:
- [ ] Paid Apps Agreement active
- [ ] Banking and tax information complete  
- [ ] In-app purchases configured and approved
- [ ] Sandbox testing completed successfully
- [ ] EULA and Terms accessible in app
- [ ] Subscription management instructions provided
- [ ] Receipt validation service configured (if using server)
- [ ] All premium features working correctly
- [ ] App Store metadata updated with differentiation
- [ ] Screenshots showcase premium features

---

**⏰ ESTIMATED TIMELINE**: 3-5 business days for setup + 24-48 hours for Apple review of in-app purchases + 2-7 days for app review

**🚨 CRITICAL**: Do not submit app until all in-app purchases show "Ready to Submit" status in App Store Connect.