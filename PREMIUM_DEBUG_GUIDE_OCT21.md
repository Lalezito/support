# 🔍 PREMIUM DEBUG GUIDE - 21 Octubre 2025

## PROBLEMA REPORTADO

Usuario reporta que después de los fixes:
- Analytics: Muestra "Premium: Suscripción activa, plan esencial" en lugar del dashboard
- Cosmic Coach: Sigue mostrando prompt premium abajo
- Ascendant: Pide fecha de nacimiento pero no guarda, vuelve a pedir

## ROOT CAUSE PROBABLE

`isPremiumUserProvider` está retornando **FALSE** a pesar de que el usuario tiene suscripción activa.

## TEORÍAS Y VERIFICACIONES

### Teoría 1: RevenueCat No Reconoce la Suscripción

**Verificación requerida:**
1. Abrir RevenueCat Dashboard (https://app.revenuecat.com)
2. Ir a Customers
3. Buscar tu usuario (por email o ID)
4. Verificar que aparezca con suscripción activa

**Si NO aparece:**
- La suscripción no está vinculada a RevenueCat
- Necesitas restaurar compras en la app

**Si SÍ aparece:**
- El problema está en el provider o la configuración

### Teoría 2: App Usa Suscripción de Sandbox vs Production

**Verificación:**
```dart
// En lib/providers/unified_premium_integration_provider.dart
// Buscar esta línea:
final customerInfo = await Purchases.getCustomerInfo();
```

**Debug necesario:**
Agregar logs para ver qué retorna RevenueCat.

### Teoría 3: Provider No Se Actualiza Después de Compra

**Problema conocido:**
Si compraste ANTES de instalar esta versión, el provider puede no actualizarse.

**Solución temporal:**
1. Desinstalar app del iPhone
2. Reinstalar
3. Abrir app
4. Ir a Premium screen
5. Tocar "Restore Purchases" (Restaurar compras)

## DIAGNÓSTICO PASO A PASO

### Paso 1: Verificar Estado del Provider

Necesito agregar código de debug al provider para ver qué está pasando:

```dart
// En lib/providers/unified_premium_integration_provider.dart
final isPremiumUserProvider = StreamProvider<bool>((ref) async* {
  try {
    print('🔍 [PREMIUM DEBUG] Checking RevenueCat status...');

    final customerInfo = await Purchases.getCustomerInfo();

    print('🔍 [PREMIUM DEBUG] CustomerInfo received:');
    print('   - Entitlements: ${customerInfo.entitlements.all.keys}');
    print('   - Active: ${customerInfo.entitlements.active.keys}');

    final hasEntitlement = customerInfo.entitlements.active.containsKey('premium');

    print('🔍 [PREMIUM DEBUG] Has premium entitlement: $hasEntitlement');

    yield hasEntitlement;

    // Listen for updates
    await for (final info in Purchases.customerInfoStream) {
      print('🔍 [PREMIUM DEBUG] CustomerInfo updated:');
      print('   - Active: ${info.entitlements.active.keys}');

      yield info.entitlements.active.containsKey('premium');
    }
  } catch (e, stack) {
    print('❌ [PREMIUM DEBUG] Error: $e');
    print('   Stack: $stack');
    yield false;
  }
});
```

### Paso 2: Verificar Configuración de RevenueCat

**Archivo:** `lib/main.dart`

Buscar la configuración de RevenueCat:

```dart
await Purchases.configure(
  PurchasesConfiguration('YOUR_API_KEY')
);
```

**Verificar:**
1. ¿La API key es correcta?
2. ¿Es la key de Production o Sandbox?
3. ¿Coincide con el entorno de la suscripción?

### Paso 3: Verificar Entitlement Name

**El problema más común:**

RevenueCat usa "entitlements" para verificar premium. El nombre del entitlement DEBE coincidir exactamente.

**En RevenueCat Dashboard:**
1. Ir a "Entitlements"
2. Verificar el nombre exacto (case-sensitive)
3. Debería ser: `premium` (minúsculas)

**En código:**
```dart
customerInfo.entitlements.active.containsKey('premium')
```

Si el entitlement se llama diferente (ej: `Premium`, `pro`, `cosmic`), el código falla.

## SOLUCIONES INMEDIATAS

### Solución 1: Restaurar Compras

**En la app:**
1. Ir a Premium Screen
2. Tocar "Restore Purchases"
3. Esperar confirmación
4. Reiniciar app
5. Probar Analytics de nuevo

### Solución 2: Agregar Logs de Debug

Modificar `isPremiumUserProvider` para agregar logs y ver qué retorna RevenueCat.

### Solución 3: Verificar ID de Usuario

**Posible problema:**
RevenueCat asocia suscripciones a un "App User ID". Si el ID cambió, la suscripción no se reconoce.

**Verificación:**
```dart
final appUserId = await Purchases.appUserID;
print('Current App User ID: $appUserId');
```

Comparar con el ID en RevenueCat Dashboard.

## ARCHIVOS A REVISAR

### 1. `lib/providers/unified_premium_integration_provider.dart`

**Líneas clave:**
- Línea ~40: Definición de `isPremiumUserProvider`
- Verificar que use `Purchases.getCustomerInfo()`
- Verificar que busque el entitlement correcto

### 2. `lib/main.dart`

**Buscar:**
- Configuración de RevenueCat
- API Key
- Initialization

### 3. `lib/screens/premium_screen.dart`

**Funcionalidad de Restore:**
- Verificar que exista botón "Restore Purchases"
- Verificar que llame a `Purchases.restorePurchases()`

## TESTING MANUAL REQUERIDO

Para determinar la causa exacta, necesito que hagas:

1. **Abrir la app**
2. **Ir a Premium screen**
3. **Tomar screenshot del estado actual**
4. **Tocar "Restore Purchases"** (si existe)
5. **Ver qué mensaje aparece**
6. **Volver a probar Analytics**

### Si Restore Purchases funciona:
✅ Problema: El provider no se actualizó después de la compra
✅ Solución: Agregar listener para actualizar automáticamente

### Si Restore Purchases NO funciona:
❌ Problema: Suscripción no está en RevenueCat
❌ Solución: Verificar RevenueCat Dashboard y configuración

## PRÓXIMOS PASOS

Basado en lo que reportaste, mi teoría principal es:

**`isPremiumUserProvider` retorna FALSE porque:**
1. RevenueCat no reconoce la suscripción, O
2. El entitlement name no coincide, O
3. El App User ID cambió

**Para confirmarlo necesito:**
1. Que me digas si existe botón "Restore Purchases" en Premium screen
2. Que lo toques y me digas qué pasa
3. Que me confirmes si en algún momento viste un mensaje de "Compra restaurada exitosamente"

## CÓDIGO TEMPORARIO PARA DEBUG

Si quieres que agregue logs de debug para ver exactamente qué está pasando, puedo modificar el provider así:

```dart
final isPremiumUserProvider = StreamProvider<bool>((ref) async* {
  print('🟢 [PREMIUM] Starting premium check...');

  try {
    final info = await Purchases.getCustomerInfo();

    print('🟢 [PREMIUM] Customer Info:');
    print('   Original App User ID: ${info.originalAppUserId}');
    print('   All Entitlements: ${info.entitlements.all.keys.toList()}');
    print('   Active Entitlements: ${info.entitlements.active.keys.toList()}');
    print('   Has premium: ${info.entitlements.active.containsKey("premium")}');

    yield info.entitlements.active.containsKey('premium');

    await for (final updated in Purchases.customerInfoStream) {
      print('🔄 [PREMIUM] Customer info updated');
      print('   Active: ${updated.entitlements.active.keys.toList()}');
      yield updated.entitlements.active.containsKey('premium');
    }
  } catch (e) {
    print('❌ [PREMIUM] Error: $e');
    yield false;
  }
});
```

Esto imprimirá en consola EXACTAMENTE qué ve el provider.

---

**Creado:** 2025-10-21
**Para:** Debugging premium issues post-fix
**Requiere:** Testing manual del usuario
