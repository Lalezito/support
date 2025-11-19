# 🛒 PLAN SUPER COMPLETO: Verificación y Arreglo de Compras RevenueCat

**Fecha**: 7 de octubre de 2025
**Objetivo**: Diagnosticar y solucionar cualquier problema con las compras in-app
**Tiempo estimado**: 2-3 horas

---

## 🎯 FASE 1: DIAGNÓSTICO RÁPIDO (15 min)

### 1.1 Verificar Estado de RevenueCat Dashboard

**Ir a**: https://app.revenuecat.com/

**Checklist**:
- [ ] ✅ Proyecto "Zodiac Life Coach" existe
- [ ] ✅ API Keys configuradas (iOS + Android)
- [ ] ✅ Products configurados:
  - `zodiac_stellar_monthly` ($19.99)
  - `zodiac_stellar_annual` ($199.99)
- [ ] ✅ Entitlements configurados:
  - `stellar_features`
- [ ] ✅ Offerings configurado:
  - `default` offering con ambos productos

**Si algo falta**: Seguir la sección "Configuración de RevenueCat Dashboard"

---

### 1.2 Verificar Configuración en App Store Connect

**Ir a**: https://appstoreconnect.apple.com/

**Checklist**:
- [ ] ✅ In-App Purchases creados y aprobados
- [ ] ✅ IDs coinciden:
  - `zodiac_stellar_monthly`
  - `zodiac_stellar_annual`
- [ ] ✅ Precios configurados ($19.99 / $199.99)
- [ ] ✅ Cleared for Sale = YES
- [ ] ✅ Sandbox testers creados y activos

**Si algo falta**: Seguir la sección "Configuración de App Store Connect"

---

### 1.3 Verificar Código Flutter

**Archivos clave**:
```bash
# Ver configuración de RevenueCat
cat zodiac_app/lib/main.dart | grep -A 10 "Purchases.configure"

# Ver implementación del servicio
cat zodiac_app/lib/services/revenue_cat_service.dart | grep -A 5 "class RevenueCatService"

# Ver pantalla de premium
cat zodiac_app/lib/features/premium/screens/premium_subscription_screen.dart | grep -A 5 "purchasePackage"
```

**Checklist**:
- [ ] ✅ API Key correcta en `main.dart`
- [ ] ✅ `RevenueCatService` inicializado
- [ ] ✅ Premium screen usa `RevenueCatService.purchasePackage()`
- [ ] ✅ No hay hardcoded user IDs (debe usar `UserIdentityService`)

---

## 🔧 FASE 2: TESTING EN SIMULADOR (30 min)

### 2.1 Preparar Entorno de Testing

```bash
cd zodiac_app

# Limpiar build anterior
flutter clean
flutter pub get

# Verificar que iOS esté configurado
cat ios/Runner.xcodeproj/project.pbxproj | grep PRODUCT_BUNDLE_IDENTIFIER

# Debe mostrar: com.yourcompany.zodiaclifecoach (o tu bundle ID)
```

### 2.2 Ejecutar App en Simulador

```bash
# Verificar simuladores disponibles
xcrun simctl list devices | grep iPhone

# Ejecutar en iPhone 16 (iOS 18.2)
flutter run -d "iPhone 16"
```

### 2.3 Prueba Manual en App

**Pasos**:
1. Abrir app en simulador
2. Ir a "Premium Features" o "Upgrade to Stellar"
3. Hacer clic en un plan (Monthly o Annual)
4. **Observar comportamiento**:
   - ❌ Error? → Copiar mensaje de error completo
   - ⏳ Loading infinito? → Revisar logs
   - ✅ Payment sheet aparece? → Continuar con sandbox test

**Logs a revisar**:
```bash
# En otra terminal, ver logs en tiempo real
flutter logs | grep -i "revenue\|purchase\|subscription"
```

---

## 🐛 FASE 3: DEBUGGING COMÚN (1 hora)

### Problema 1: "No offerings found"

**Síntomas**:
- Premium screen vacía
- Error: "No offerings available"

**Solución**:
```bash
# Verificar configuración de RevenueCat
cat zodiac_app/lib/services/revenue_cat_service.dart
```

**Verificar que exista**:
```dart
Future<List<Package>> getAvailablePackages() async {
  try {
    final offerings = await Purchases.getOfferings();
    if (offerings.current != null) {
      return offerings.current!.availablePackages;
    }
    return [];
  } catch (e) {
    print('Error getting offerings: $e');
    return [];
  }
}
```

**Fix si falta**:
1. Ir a RevenueCat Dashboard
2. Products → Verify "zodiac_stellar_monthly" y "annual" existen
3. Entitlements → Verify "stellar_features" existe
4. Offerings → Verify "default" offering tiene ambos productos

---

### Problema 2: "API Key inválida"

**Síntomas**:
- Error: "Invalid API key"
- Purchases.configure falla

**Solución**:
```bash
# Verificar API Key
cat zodiac_app/lib/main.dart | grep "PurchasesConfiguration"
```

**Debe verse así**:
```dart
await Purchases.configure(
  PurchasesConfiguration('appl_xxxxxxxxxxxxxxxxx') // iOS key
    ..appUserID = null // Let RevenueCat generate
);
```

**Fix**:
1. Ir a RevenueCat Dashboard → API Keys
2. Copiar "Apple App Store" key (empieza con `appl_`)
3. Reemplazar en `main.dart`

---

### Problema 3: "User ID anónimo"

**Síntomas**:
- Compras no se asocian al usuario correcto
- Al reinstalar, compras desaparecen

**Solución**:
```bash
# Buscar hardcoded 'anonymous'
grep -r "anonymous" zodiac_app/lib/services/revenue_cat_service.dart
grep -r "anonymous" zodiac_app/lib/features/premium/
```

**Fix**:
```dart
// BEFORE (MAL):
await Purchases.logIn('anonymous');

// AFTER (BIEN):
final userId = await UserIdentityService.getRevenueCatUserId();
await Purchases.logIn(userId);
```

**Archivos a revisar**:
- `lib/services/revenue_cat_service.dart`
- `lib/providers/premium_provider.dart`
- `lib/features/premium/screens/premium_subscription_screen.dart`

---

### Problema 4: "StoreKit Configuration falta"

**Síntomas**:
- Error: "No StoreKit configuration file found"
- Solo en simulador iOS 15+

**Solución**:
```bash
# Verificar si existe StoreKit config
ls -la zodiac_app/ios/Runner/Configuration.storekit

# Si no existe, crear:
cat > zodiac_app/ios/Runner/Configuration.storekit << 'EOF'
{
  "identifier" : "Configuration",
  "nonRenewingSubscriptions" : [],
  "products" : [
    {
      "displayPrice" : "19.99",
      "familyShareable" : false,
      "internalID" : "stellar_monthly_test",
      "localizations" : [],
      "productID" : "zodiac_stellar_monthly",
      "referenceName" : "Stellar Monthly",
      "type" : "NonConsumable"
    },
    {
      "displayPrice" : "199.99",
      "familyShareable" : false,
      "internalID" : "stellar_annual_test",
      "localizations" : [],
      "productID" : "zodiac_stellar_annual",
      "referenceName" : "Stellar Annual",
      "type" : "NonConsumable"
    }
  ],
  "settings" : {
    "locale" : "en_US"
  },
  "subscriptionGroups" : [],
  "version" : {
    "major" : 1,
    "minor" : 0
  }
}
EOF
```

**Luego en Xcode**:
1. Abrir `ios/Runner.xcworkspace`
2. Runner → Edit Scheme → Run → Options
3. StoreKit Configuration → Seleccionar "Configuration.storekit"

---

### Problema 5: "Purchase sheet no aparece"

**Síntomas**:
- Click en "Subscribe" no hace nada
- No aparece el payment sheet de iOS

**Solución**:
```bash
# Verificar implementación de purchasePackage
cat zodiac_app/lib/services/revenue_cat_service.dart | grep -A 20 "purchasePackage"
```

**Debe verse así**:
```dart
Future<CustomerInfo> purchasePackage(Package package) async {
  try {
    final purchaseResult = await Purchases.purchasePackage(package);
    return purchaseResult.customerInfo;
  } on PlatformException catch (e) {
    final errorCode = PurchasesErrorHelper.getErrorCode(e);
    if (errorCode == PurchasesErrorCode.purchaseCancelledError) {
      throw PurchaseCancelledException();
    } else if (errorCode == PurchasesErrorCode.paymentPendingError) {
      throw PaymentPendingException();
    }
    rethrow;
  }
}
```

**Fix si falta manejo de errores**: Agregar try-catch completo

---

## 🧪 FASE 4: TESTING CON SANDBOX (30 min)

### 4.1 Crear Sandbox Tester

**App Store Connect**:
1. Users and Access → Sandbox Testers
2. Click "+" para crear nuevo tester
3. Email: `test.zodiac1@icloud.com` (usar email único)
4. Password: `TestZodiac123!`
5. Country: United States
6. Save

### 4.2 Configurar iPhone/Simulador

**En dispositivo físico**:
1. Settings → App Store → Sandbox Account
2. Sign in con sandbox tester

**En simulador**:
1. Settings → App Store → Sandbox Account
2. Sign in con sandbox tester

### 4.3 Prueba Completa

**Pasos**:
1. Abrir app
2. Ir a Premium/Upgrade screen
3. Seleccionar "Stellar Monthly ($19.99)"
4. Payment sheet debe aparecer
5. Touch ID/Face ID para confirmar (o contraseña de sandbox)
6. **Esperar confirmación**
7. Verificar que features premium se desbloqueen

**Verificar en RevenueCat Dashboard**:
1. Customers → Buscar por userID
2. Debe aparecer compra activa
3. Entitlement "stellar_features" = active

---

## 📱 FASE 5: TESTING EN DISPOSITIVO FÍSICO (30 min)

### 5.1 Preparar iPhone

```bash
# Verificar iPhone conectado
flutter devices

# Ejecutar en iPhone
flutter run -d "Alejandro's iPhone" --release
```

### 5.2 Configurar Sandbox

**En iPhone**:
1. Ajustes → App Store → Cuenta Sandbox
2. Iniciar sesión con sandbox tester
3. **IMPORTANTE**: No usar Apple ID real para compras de prueba

### 5.3 Prueba Real

**Pasos**:
1. Abrir app en iPhone físico
2. Navegar a Premium
3. Intentar compra
4. Verificar todo el flujo

**Diferencias vs Simulador**:
- Touch ID/Face ID real
- Network real (no mock)
- StoreKit real (no configuration file)

---

## 🔍 FASE 6: LOGS Y DEBUGGING AVANZADO (30 min)

### 6.1 Habilitar Debug Logging

**Agregar a `main.dart`**:
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Enable RevenueCat debug logs
  await Purchases.setLogLevel(LogLevel.debug);

  await Purchases.configure(
    PurchasesConfiguration('appl_xxxxxxxxx')
  );

  runApp(MyApp());
}
```

### 6.2 Ver Logs Detallados

```bash
# En terminal, filtrar logs de RevenueCat
flutter logs | grep -E "Purchases|RevenueCat|StoreKit"

# Guardar logs a archivo para análisis
flutter logs > purchase_debug.log
```

### 6.3 Common Error Codes

| Error Code | Significado | Solución |
|------------|-------------|----------|
| `PURCHASE_CANCELLED` | Usuario canceló | Normal, no hacer nada |
| `STORE_PROBLEM` | App Store issue | Verificar sandbox/network |
| `PURCHASE_NOT_ALLOWED` | Restrictions enabled | Settings → Screen Time |
| `PURCHASE_INVALID` | Product ID wrong | Verificar IDs en Dashboard |
| `UNKNOWN_ERROR` | Generic error | Ver logs detallados |

---

## 🛠️ FIXES RÁPIDOS

### Fix 1: Resetear RevenueCat Cache

```dart
// En development/debug
await Purchases.invalidateCustomerInfoCache();
```

### Fix 2: Limpiar App State

```bash
# En simulador
xcrun simctl uninstall booted com.yourcompany.zodiaclifecoach
flutter clean
flutter run
```

### Fix 3: Verificar Network

```dart
// Agregar a revenue_cat_service.dart
Future<bool> checkConnection() async {
  try {
    final result = await InternetAddress.lookup('api.revenuecat.com');
    return result.isNotEmpty && result[0].rawAddress.isNotEmpty;
  } catch (_) {
    return false;
  }
}
```

---

## 📊 CHECKLIST FINAL

### Configuración
- [ ] RevenueCat Dashboard configurado (Products, Entitlements, Offerings)
- [ ] App Store Connect configurado (In-App Purchases aprobados)
- [ ] API Keys correctas en código
- [ ] StoreKit Configuration creado (para simulador)

### Código
- [ ] `RevenueCatService` implementado correctamente
- [ ] User ID usa `UserIdentityService` (no hardcoded)
- [ ] Error handling completo
- [ ] Debug logging habilitado

### Testing
- [ ] Simulador: Compra exitosa
- [ ] Dispositivo físico: Compra exitosa
- [ ] RevenueCat Dashboard muestra compra
- [ ] Features premium se desbloquean
- [ ] Restore purchases funciona

### Production Readiness
- [ ] Remover debug logging
- [ ] Sandbox tester documentado
- [ ] Screenshots de compra para App Store Review
- [ ] Privacy Policy menciona compras

---

## 🚨 SI TODO FALLA: CHECKLIST NUCLEAR

1. **Eliminar RevenueCat completamente**:
```bash
flutter pub remove purchases_flutter
flutter clean
```

2. **Reinstalar desde cero**:
```bash
flutter pub add purchases_flutter
flutter pub get
```

3. **Verificar versión**:
```bash
flutter pub deps | grep purchases_flutter
# Debe ser >= 6.0.0
```

4. **Re-configurar todo siguiendo**:
   - `REVENUECAT_CONFIGURACION_COMPLETA_FINAL.md`
   - `SOLUCION_REVENUECAT_PASO_A_PASO.md`

---

## 📞 RECURSOS DE AYUDA

### Documentación
- **RevenueCat Docs**: https://docs.revenuecat.com/
- **Flutter Plugin**: https://pub.dev/packages/purchases_flutter
- **Error Codes**: https://docs.revenuecat.com/docs/errors

### Archivos de Referencia (ya creados)
- `REVENUECAT_CONFIGURACION_COMPLETA_FINAL.md` - Setup completo
- `SOLUCION_REVENUECAT_PASO_A_PASO.md` - Troubleshooting
- `ESTADO_FINAL_REVENUECAT.md` - Estado actual
- `TEST_REVENUECAT_IPHONE_FISICO.md` - Testing en dispositivo

### Commands Útiles
```bash
# Ver estado de RevenueCat
grep -r "Purchases" zodiac_app/lib/ --include="*.dart"

# Verificar productos configurados
cat zodiac_app/lib/services/revenue_cat_service.dart | grep productIdentifier

# Ver logs de compra
flutter logs | grep -i purchase

# Limpiar completamente
flutter clean && rm -rf ios/Pods && cd ios && pod install && cd ..
```

---

## ✅ CRITERIOS DE ÉXITO

**La compra está funcionando SI**:
1. ✅ Premium screen muestra productos con precios correctos
2. ✅ Click en "Subscribe" abre payment sheet de iOS
3. ✅ Confirmación de compra exitosa
4. ✅ Features premium se desbloquean inmediatamente
5. ✅ RevenueCat Dashboard muestra la transacción
6. ✅ Cerrar/abrir app mantiene estado premium
7. ✅ "Restore purchases" funciona

---

**Creado**: 7 de octubre de 2025
**Para**: Verificación de compras RevenueCat
**Prioridad**: Alta (bloqueador para App Store submission)
**Tiempo estimado**: 2-3 horas
**Siguiente paso**: Ejecutar FASE 1 - Diagnóstico Rápido

---

🎯 **TIP PRO**: Empieza por FASE 1 (15 min). Si todo está verde ahí, el problema es probablemente en FASE 2 (testing). Si FASE 1 tiene issues, arregla configuración antes de continuar.
