# App Store Testing Instructions

## Sandbox Testing - Subscription Flows

### Test Case 1: Stellar Tier Subscription ($19.99/month)

**Steps:**
1. Open app > Side menu > Premium
2. Select "Stellar Tier ($19.99/month + AI)" card
3. Verify popup shows free trial configured in App Store
4. Complete purchase with sandbox account

**Sandbox Credentials:**
- User: XXX@apple.com
- Password: XXXXX

---

### Test Case 2: Cosmic Premium Subscription ($6.99/month)

**Steps:**
1. Open app > Side menu > Premium
2. Select "Cosmic Premium ($6.99/month)"
3. StoreKit should display 7-day free trial period
4. Complete purchase with sandbox account

**Sandbox Credentials:**
- User: XXX@apple.com
- Password: XXXXX

---

## Subscription Products Configured

| Tier | Price | Features | Trial |
|------|-------|----------|-------|
| Cosmic | $6.99/month | Essential premium features | 7 days |
| Stellar | $19.99/month | Full AI coach access + advanced features | 7 days |

---

## Subscription Display Names & Descriptions by Language

### Stellar Premium ($19.99/month)

| Language | Display Name | Description |
|----------|------------|-------------|
| German | Stellar Premium | Cosmic + Krisen-KI, Geburtskarte, Coach Plus. |
| Spanish (Mexico) | Stellar Premium | Cosmic + Crisis IA, carta natal y coach avanzado. |
| French | Stellar Premium | Cosmic + IA de crise, thème natal, coach pro. |
| English (Australia) | Stellar Premium | Cosmic + Crisis AI, birth chart, advanced coach |
| Italian | Stellar Premium | Cosmic + IA crisi, carta natale, coach pro. |
| Portuguese (Brazil) | Stellar Premium | Cosmic + IA crise, mapa natal, coach avançado. |

### Cosmic Premium ($6.99/month)

| Language | Display Name | Description |
|----------|------------|-------------|
| German | Cosmic Premium | Unbegrenzte Horoskope, werbefrei, KI-Coach |
| Spanish (Mexico) | Cosmic Premium | Horóscopos ilimitados, sin anuncios y coach IA. |
| French | Cosmic Premium | Horoscopes illimités, sans pub, coach IA. |
| English (Australia) | Cosmic Premium | Unlimited horoscopes, ad-free, AI coach guide. |
| Italian | Cosmic Premium | Oroscopi illimitati, senza pub, coach IA. |
| Portuguese (Brazil) | Cosmic Premium | Horóscopos ilimitados, sem anúncios, coach IA. |

---

## Notes
- Subscriptions auto-renew in production
- In sandbox, subscriptions are accelerated (1 day = ~1 hour)
- Always use provided sandbox credentials for testing
