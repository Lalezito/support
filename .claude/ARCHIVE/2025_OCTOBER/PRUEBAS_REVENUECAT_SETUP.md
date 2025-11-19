# 🧪 CONFIGURACIÓN PRUEBAS REVENUECAT

## ⚠️ PROBLEMA DETECTADO

iOS 18.4 simulator tiene un **bug conocido** con RevenueCat/StoreKit que impide cargar productos:
```
PlatformException(23, None of the products could be fetched from App Store Connect)
This issue is widely reported by iOS 18.4 simulator users.
```

## ✅ SOLUCIÓN IMPLEMENTADA

### 1️⃣ StoreKit Configuration File Creado

He creado `/ios/ZodiacStoreKitConfig.storekit` con tus 3 productos:

- **tier1_subscription** - $6.99/mes (Cosmic)
- **tier2_subscription** - $19.99/mes (Stellar)
- **lifetime_tier1_purchase** - $49.99 (Universe)

### 2️⃣ CÓMO CONFIGURAR EN XCODE

**IMPORTANTE: Debes hacer esto manualmente** (no se puede automatizar):

1. **Abre Xcode**:
   ```bash
   open /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app/ios/Runner.xcworkspace
   ```

2. **Configura StoreKit en el Scheme**:
   - En Xcode, ve a: **Product → Scheme → Edit Scheme...**
   - Selecciona **Run** en el sidebar izquierdo
   - Ve a la pestaña **Options**
   - Busca **StoreKit Configuration**
   - Selecciona el archivo: `ZodiacStoreKitConfig.storekit`
   - Click **Close**

3. **Verifica que esté activado**:
   - El dropdown debe mostrar `ZodiacStoreKitConfig.storekit` ✅

### 3️⃣ MÉTODO ALTERNATIVO: USAR iOS 18.3

Si prefieres no configurar StoreKit, usa el simulador iOS 18.3:

```bash
# Boot el simulador correcto
xcrun simctl boot D5AEB9B1-60D9-4DFD-8F45-B739CF5BD851

# Run la app en iOS 18.3
cd /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app
flutter run -d D5AEB9B1-60D9-4DFD-8F45-B739CF5BD851 test_revenuecat_storekit.dart
```

## 🧪 CÓMO PROBAR LAS COMPRAS

Una vez configurado, ejecuta:

```bash
cd /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app
flutter run -d "iPhone 16 Pro iOS 18.3" test_revenuecat_storekit.dart
```

### Lo que deberías ver:

1. ✅ **RevenueCat Initialized** (verde)
2. ✅ **Customer info retrieved**
3. ✅ **Offerings fetched** con 3 productos:
   - tier1_subscription: $6.99
   - tier2_subscription: $19.99
   - lifetime_tier1_purchase: $49.99
4. 3 botones para probar cada compra

### Al hacer click en comprar:

- Se abrirá el **StoreKit Payment Sheet** (simulado)
- Podrás aprobar/cancelar la compra
- Verás logs en tiempo real del proceso

## 📊 VERIFICACIÓN EN REVENUECAT

Después de hacer una compra de prueba:

1. Ve a: https://app.revenuecat.com
2. Login con tu cuenta
3. Ve a **Customers → Search**
4. Busca el `test_user_XXXXXX` (verás el ID en los logs)
5. Deberías ver el **active entitlement**: `zodiac_premium_access`

## 🔍 TROUBLESHOOTING

### Error: "Products not found"
- Verifica que StoreKit Configuration esté seleccionado en Xcode
- Reinicia Xcode y vuelve a correr

### Error: "Platform Exception 23"
- Estás usando iOS 18.4 → Cambia a 18.3 o usa StoreKit Config

### No se abre el payment sheet
- Asegúrate de tener StoreKit Configuration activo
- Revisa que los Product IDs sean exactos

## ✅ CHECKLIST FINAL

- [ ] Archivo StoreKit creado: `ios/ZodiacStoreKitConfig.storekit`
- [ ] StoreKit Configuration seleccionado en Xcode Scheme
- [ ] Test app corriendo en iOS 18.3 o con StoreKit Config
- [ ] 3 productos cargando correctamente
- [ ] Payment sheet funcionando
- [ ] Entitlements activándose en RevenueCat

## 🎯 SIGUIENTE PASO

Una vez que veas los 3 productos cargando:
1. Prueba cada tipo de compra
2. Verifica que RevenueCat reciba los eventos
3. Confirma que los entitlements se activen

**Entonces estarás 100% listo para producción** ✅
