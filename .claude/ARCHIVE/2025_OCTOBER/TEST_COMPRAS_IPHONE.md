# 🧪 PLAN DE TESTING - COMPRAS PREMIUM EN IPHONE

**Fecha:** Octubre 13, 2025
**Dispositivo:** Alejandro Caceres's iPhone (ID: 00008150-0015244A2288401C)

---

## 🎯 OBJETIVO

Testear el sistema completo de compras premium en dispositivo físico antes del lanzamiento a la App Store.

---

## ✅ PRE-REQUISITOS

- [x] RevenueCat configurado (API Key: `appl_TwCrrBozYBCYouyUHpLJturOSSD`)
- [x] 3 productos creados en App Store Connect
- [x] Código de compras implementado
- [ ] iPhone conectado por cable USB
- [ ] iPhone desbloqueado
- [ ] Developer Mode activado en iPhone

---

## 📋 CHECKLIST DE TESTING

### 1️⃣ PREPARACIÓN (5 min)

**Conectar iPhone:**
```bash
# 1. Conectar iPhone por cable USB
# 2. Desbloquear iPhone
# 3. Si aparece "Trust this computer?" → Trust
# 4. Verificar conexión
flutter devices
```

**Resultado esperado:**
```
✅ Alejandro Caceres's iPhone (mobile) • 00008150-0015244A2288401C • ios
```

---

### 2️⃣ EJECUTAR APP EN IPHONE (2 min)

```bash
cd "/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"

# Ejecutar en iPhone
flutter run -d 00008150-0015244A2288401C
```

**Esperar a que:**
- ✅ Compile la app (~30-60 segundos)
- ✅ Instale en iPhone
- ✅ App abra automáticamente

---

### 3️⃣ NAVEGACIÓN A PREMIUM (1 min)

**En el iPhone:**
1. Abrir la app Zodiac
2. Navegar a **Settings** o **Profile**
3. Buscar botón **"Upgrade to Premium"** o **"Premium Features"**
4. Hacer tap

---

### 4️⃣ VERIFICAR PRODUCTOS (CRÍTICO ✅)

**Deberías ver:**

```
╔════════════════════════════════════╗
║      ZODIAC PREMIUM TIERS         ║
╠════════════════════════════════════╣
║                                    ║
║  🌟 COSMIC TIER                    ║
║     $6.99 / month                  ║
║     [Subscribe]                    ║
║                                    ║
║  ✨ STELLAR TIER                   ║
║     $19.99 / month                 ║
║     [Subscribe]                    ║
║                                    ║
║  🌌 UNIVERSE LIFETIME              ║
║     $49.99 one-time                ║
║     [Purchase]                     ║
║                                    ║
╚════════════════════════════════════╝
```

**✅ VERIFICAR:**
- [ ] Se muestran los 3 tiers
- [ ] Precios correctos: $6.99, $19.99, $49.99
- [ ] Botones son clicables
- [ ] No hay errores en pantalla

**❌ SI NO SE MUESTRAN:**
- Ver logs en la terminal de Flutter
- Buscar errores como "PlatformException" o "No products found"
- Verificar conexión a internet del iPhone

---

### 5️⃣ PROBAR COMPRA - TIER 1 (COSMIC)

**Pasos:**
1. Tap en **"Subscribe"** del Cosmic tier ($6.99)
2. Aparece **StoreKit Payment Sheet** de Apple
3. Verás: "Zodiac Life Coach - Cosmic Monthly - $6.99"
4. **Tap "Subscribe"** (o "Confirm")
5. Completar Touch ID / Face ID

**✅ Resultado esperado:**
```
✅ Purchase successful!
✅ Welcome to Cosmic tier!
```

**Verificar:**
- [ ] Compra completó sin errores
- [ ] Mensaje de éxito apareció
- [ ] Pantalla premium se cerró o actualizó
- [ ] Badge/icono de premium aparece

**En RevenueCat Dashboard:**
- Ir a: https://app.revenuecat.com
- **Customers** → Buscar el email/ID del test user
- Verificar que aparezca: `Active Entitlement: zodiac_premium_access`

---

### 6️⃣ VERIFICAR FUNCIONES PREMIUM

**Navegar a funciones premium:**

**Deberían estar desbloqueadas:**
- [ ] Daily Horoscope (versión extendida)
- [ ] Compatibility Reports (ilimitados)
- [ ] Personalized AI readings
- [ ] Cosmic Coach features
- [ ] No ads / Premium badge visible

**Prueba específica:**
1. Ir a **Compatibility** screen
2. Seleccionar dos signos zodiacales
3. Ver reporte de compatibilidad
4. **Verificar:** Se muestra reporte completo sin paywall

---

### 7️⃣ PROBAR RESTORE PURCHASES

**Caso de uso:** Usuario reinstala la app o cambia de dispositivo

**Pasos:**
1. Cerrar la app completamente (swipe up)
2. Reabrir la app
3. Ir a Premium screen
4. Buscar botón **"Restore Purchases"**
5. Tap en "Restore Purchases"

**✅ Resultado esperado:**
```
✅ Purchases restored successfully!
✅ Cosmic tier activated
```

**Verificar:**
- [ ] Premium status se restauró
- [ ] Funciones premium siguen activas
- [ ] No pidió pagar de nuevo

---

### 8️⃣ PROBAR CANCELACIÓN DE COMPRA

**Caso de uso:** Usuario abre payment sheet pero cambia de opinión

**Pasos:**
1. Ir a Premium screen
2. Tap en **Stellar tier** ($19.99)
3. Aparece StoreKit Payment Sheet
4. **Tap "Cancel"** (botón X o Cancel)

**✅ Resultado esperado:**
```
(Sin mensaje de error)
(Vuelve a pantalla premium)
```

**Verificar:**
- [ ] NO apareció mensaje de error
- [ ] App no crasheó
- [ ] Simplemente volvió a la pantalla anterior

---

### 9️⃣ PROBAR COMPRA - LIFETIME

**Pasos:**
1. Tap en **"Purchase"** del Universe Lifetime ($49.99)
2. Aparece StoreKit Payment Sheet
3. Verás: "Zodiac Life Coach - Universe Lifetime - $49.99"
4. **Tap "Buy"**
5. Completar Touch ID / Face ID

**✅ Resultado esperado:**
```
✅ Purchase successful!
✅ Universe lifetime access activated!
```

**Verificar:**
- [ ] Compra completó
- [ ] Mensaje de éxito
- [ ] Premium features activadas
- [ ] Badge cambia a "Lifetime Member"

---

### 🔟 PROBAR UPGRADE (TIER 1 → TIER 2)

**Solo si ya compraste Tier 1:**

**Pasos:**
1. Siendo usuario de Cosmic ($6.99)
2. Tap en **"Upgrade to Stellar"** ($19.99)
3. Apple muestra: "Upgrade subscription?"
4. Confirmar upgrade

**✅ Resultado esperado:**
```
✅ Upgraded to Stellar tier!
✅ GPT features now unlocked
```

**Verificar:**
- [ ] Upgrade completó
- [ ] Nuevas features desbloqueadas
- [ ] RevenueCat refleja el cambio

---

## 🐛 TROUBLESHOOTING

### Problema: "No products available"

**Causa:** RevenueCat no puede conectarse o productos no sincronizados

**Solución:**
1. Verificar internet del iPhone
2. Ver logs en terminal Flutter
3. Verificar en App Store Connect que productos estén "Ready to Submit"
4. Reiniciar la app

---

### Problema: "Purchase failed" sin razón clara

**Causa:** Issue con Apple Sandbox o configuración

**Solución:**
1. Ir a iPhone → **Settings** → **App Store**
2. **Sign Out** de cuenta sandbox
3. **Sign In** nuevamente con cuenta sandbox
4. Reintentar compra

---

### Problema: Compra exitosa pero premium no se activa

**Causa:** Entitlements no configurados en RevenueCat

**Solución:**
1. Ir a RevenueCat Dashboard
2. **Products** → Verificar que cada producto tenga:
   - `tier1_subscription` → `zodiac_premium_access` ✅
   - `tier2_subscription` → `zodiac_premium_access` ✅
   - `lifetime_tier1_purchase` → `zodiac_premium_access` ✅
3. Si falta, agregar el entitlement
4. Probar nuevamente

---

### Problema: Logs muestran "PlatformException code 23"

**Causa:** Bug conocido de iOS simulators (NO aplica a iPhone físico)

**Solución:**
- Ignorar si estás en simulador
- En iPhone físico, esto NO debería pasar
- Si pasa en iPhone físico, verificar App Store Connect

---

## 📊 LOGS ESPERADOS

### Logs exitosos:
```
🔧 [RevenueCat] Initializing with API key: appl_TwC...
✅ [RevenueCat] SDK initialized successfully
📡 Fetching offerings from RevenueCat...
📦 Available packages (3): tier1_subscription, tier2_subscription, lifetime_tier1_purchase
💳 Initiating purchase: tier1_subscription ($6.99)
✅ Purchase successful: Cosmic
   Active entitlements: zodiac_premium_access
```

### Logs de cancelación (normal):
```
💳 Initiating purchase: tier2_subscription ($19.99)
ℹ️ User cancelled the purchase
```

### Logs de error (investigar):
```
❌ Purchase failed: [descripción del error]
❌ RevenueCat error: [código y mensaje]
```

---

## ✅ CHECKLIST FINAL

Después de testing completo:

- [ ] 3 productos se muestran correctamente
- [ ] Precios son exactos ($6.99, $19.99, $49.99)
- [ ] Compra de Tier 1 funciona
- [ ] Compra de Tier 2 funciona
- [ ] Compra de Lifetime funciona
- [ ] Cancelación no muestra error
- [ ] Restore purchases funciona
- [ ] Premium features se desbloquean
- [ ] RevenueCat dashboard refleja compras
- [ ] App no crashea en ningún flujo

---

## 🚀 DESPUÉS DEL TESTING

Si todo funciona:

✅ **Tu integración de compras está lista para producción**

**Próximos pasos:**
1. Crear screenshots para App Store
2. Preparar descripción de productos premium
3. Submit a App Store Review
4. **¡Lanzar y empezar a generar revenue!** 💰

**Proyección de revenue:**
- 1,000 descargas/mes
- 3% conversión = 30 premium users
- $13 promedio por usuario
- **~$400/mes** 🎯

---

## 📞 REFERENCIAS

- **RevenueCat Dashboard:** https://app.revenuecat.com
- **App Store Connect:** https://appstoreconnect.apple.com
- **RevenueCat Docs:** https://docs.revenuecat.com
- **Documentación local:**
  - `REVENUECAT_CONFIGURACION_COMPLETA_FINAL.md`
  - `SOLUCION_REVENUECAT_PASO_A_PASO.md`
  - `PURCHASE_ERROR_FIX_SUMMARY.md`

---

**🎉 ¡Buena suerte con el testing! Todo está configurado perfectamente.**
