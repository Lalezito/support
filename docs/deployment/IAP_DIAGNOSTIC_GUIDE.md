# 🔍 Guía de Diagnóstico - IAP (In-App Purchases)

## Problema Reportado
**Síntoma:** Tras confirmar la suscripción en la sheet de App Store, la app no desbloquea los beneficios premium.

## Arquitectura del Sistema IAP

```
App Store / RevenueCat
        ↓
RevenueCatService (revenuecat_service.dart)
        ↓
RevenueCatIntegration (revenuecat_integration.dart)
        ↓
PremiumSubscriptionManager
        ↓
PreferencesService
        ↓
UI (Premium Features)
```

## Puntos de Verificación

### 1. ✅ Inicialización de RevenueCat

**Archivo:** `revenuecat_integration.dart:36-61`

**Verificar:**
```dart
// Debe ejecutarse al inicio de la app
await RevenueCatIntegration().initialize();
```

**Logs esperados:**
```
🔗 Initializing RevenueCat Integration
✅ RevenueCatService initialized successfully - Ready for purchases!
✅ RevenueCat Integration initialized successfully
```

**Si falla:** La compra no podrá procesar. Verificar API key en `revenuecat_service.dart`.

---

### 2. 🔑 Configuración de Entitlements en RevenueCat Dashboard

**Archivo:** `revenuecat_service.dart:142-148`

Los entitlements deben estar configurados EXACTAMENTE con estos IDs:
- `cosmic` → PremiumTier.cosmic
- `stellar` → PremiumTier.stellar
- `universe` → PremiumTier.universe

**Cómo verificar:**
1. Ir a RevenueCat Dashboard
2. Projects → [Tu App] → Entitlements
3. Verificar que existan entitlements con estos IDs EXACTOS

**Si no coinciden:** El mapeo en `revenuecat_service.dart:131-150` fallará y no se activará premium.

---

### 3. 💳 Flujo de Compra

**Archivo:** `revenuecat_integration.dart:94-189`

**Pasos:**
1. Usuario toca "Comprar"
2. `purchaseSubscription()` se ejecuta con timeout de 45s
3. RevenueCat SDK muestra sheet nativa de App Store
4. Usuario confirma compra
5. RevenueCat valida el receipt con App Store
6. RevenueCat actualiza `CustomerInfo` con entitlements activos
7. `_syncSubscriptionState()` se ejecuta (línea 124)

**Logs esperados:**
```
💳 Attempting to purchase: Cosmic Premium
✅ Purchase completed: Cosmic Premium
🔄 Syncing subscription state: Cosmic Premium
✅ Subscription state synced successfully
```

**Si falla en paso 6:**
- Error común: "Purchase completed but no active entitlements" (línea 132)
- **Causa:** Entitlements no configurados correctamente en RevenueCat

---

### 4. 🔄 Sincronización de Estado

**Archivo:** `revenuecat_integration.dart:64-91`

**Proceso:**
```dart
_syncSubscriptionState() {
  1. Lee currentTier de RevenueCat
  2. Actualiza PremiumSubscriptionManager.updateTier()
  3. Actualiza PreferencesService.setPremium(true)
}
```

**Verificar:**
```dart
// Después de compra exitosa
final tier = RevenueCatIntegration().currentTier;
final hasActive = RevenueCatIntegration().hasActiveSubscription;

print('Current tier: ${tier.displayName}');  // Debe ser 'Cosmic Premium', 'Stellar Premium', etc.
print('Has active: $hasActive');  // Debe ser true
```

---

### 5. 🎯 Verificación de Premium en UI

**Archivo:** Cualquier widget que use `isPremiumProvider`

**Ejemplo:**
```dart
// En build()
final isPremium = ref.watch(isPremiumProvider);

// Debe reflejar el estado correcto inmediatamente después de compra
```

**Si falla:** Verificar que `consolidated_providers.dart` esté leyendo de `PreferencesService` correctamente.

---

## Comandos de Diagnóstico

### Verificar estado actual de suscripción
```dart
// En cualquier parte de la app
final integration = RevenueCatIntegration();
print('Is initialized: ${integration.isInitialized}');
print('Current tier: ${integration.currentTier.displayName}');
print('Has active sub: ${integration.hasActiveSubscription}');
print('Expiration: ${integration.subscriptionExpirationDate}');
```

### Forzar sincronización manual
```dart
await RevenueCatIntegration().manualSync(
  preferencesService: ref.read(preferencesServiceProvider)
);
```

### Ver info detallada
```dart
final info = RevenueCatIntegration().getSubscriptionInfo();
print('Subscription info: $info');
```

---

## Causas Comunes y Soluciones

### ❌ Problema: "Purchase completed but no active entitlements"

**Causa:** Entitlements no configurados en RevenueCat Dashboard

**Solución:**
1. Ir a RevenueCat Dashboard
2. Configurar Products
3. Asociar Products a Entitlements
4. Verificar que los Entitlement IDs sean: `cosmic`, `stellar`, `universe`

---

### ❌ Problema: Compra exitosa pero UI no actualiza

**Causa:** `_syncSubscriptionState()` no se ejecutó

**Solución:**
```dart
// Agregar debugging
await _syncSubscriptionState(preferencesService);
print('✅ Sync completed');

// Verificar que PreferencesService persista el cambio
final prefs = await SharedPreferences.getInstance();
final isPremium = prefs.getBool('isPremium') ?? false;
print('Stored isPremium: $isPremium');
```

---

### ❌ Problema: Initialization nunca completa

**Causa:** API key incorrecta o problema de red

**Solución:**
```dart
// Verificar API key en revenuecat_service.dart
static const String _apiKey = 'YOUR_API_KEY_HERE';

// Debe coincidir con el key en RevenueCat Dashboard
```

---

## Testing en Sandbox

### Configurar cuenta de prueba
1. Settings → App Store → Sandbox Account
2. Crear cuenta de prueba en App Store Connect
3. Cerrar sesión de App Store en dispositivo
4. Iniciar compra en app
5. Usar cuenta sandbox cuando solicite

### Verificar compra sandbox
- La compra se completa inmediatamente
- No se cobra dinero real
- Receipt debe validar correctamente

---

## Logs Clave para Debugging

Buscar estos logs en consola después de intentar compra:

```
✅ Customer info retrieved: cosmic, stellar, universe
🔍 Active entitlements: [cosmic]
💳 Attempting to purchase: Cosmic Premium
✅ Purchase completed: Cosmic Premium
🔄 Syncing subscription state: Cosmic Premium
✅ Subscription state synced successfully
```

Si alguno falta, hay un problema en ese punto del flujo.

---

## Próximos Pasos Recomendados

1. **Verificar configuración RevenueCat:**
   - Products configurados correctamente
   - Entitlements con IDs correctos
   - App Bundle ID coincide

2. **Probar flujo completo en sandbox:**
   - Compra → Ver logs → Verificar UI actualiza
   - Reiniciar app → Verificar estado persiste
   - Restore purchases → Verificar funciona

3. **Agregar telemetría adicional:**
   - Log cada paso del flujo de compra
   - Capturar estados antes/después de sync
   - Monitorear `CustomerInfo` changes

---

## Código de Ejemplo para Testing

```dart
// En un botón de debug
ElevatedButton(
  onPressed: () async {
    final integration = RevenueCatIntegration();

    // Verificar inicialización
    if (!integration.isInitialized) {
      print('❌ Not initialized!');
      return;
    }

    // Mostrar estado actual
    print('📊 Current Status:');
    print('  Tier: ${integration.currentTier.displayName}');
    print('  Active: ${integration.hasActiveSubscription}');
    print('  Expires: ${integration.subscriptionExpirationDate}');

    // Intentar compra
    try {
      final success = await integration.purchaseSubscription(
        PremiumTier.cosmic,
        preferencesService: ref.read(preferencesServiceProvider),
      );

      if (success) {
        print('✅ Purchase succeeded!');
        // Verificar UI
        final isPremium = ref.read(isPremiumProvider);
        print('  UI shows premium: $isPremium');
      } else {
        print('❌ Purchase failed!');
      }
    } catch (e) {
      print('❌ Error: $e');
    }
  },
  child: Text('Test Purchase'),
)
```

---

## Checklist de Resolución

- [ ] RevenueCat API key configurada correctamente
- [ ] Entitlements creados en Dashboard con IDs correctos (`cosmic`, `stellar`, `universe`)
- [ ] Products vinculados a Entitlements en RevenueCat
- [ ] App Bundle ID coincide entre Xcode, RevenueCat y App Store Connect
- [ ] `initialize()` se ejecuta al inicio de la app
- [ ] Logs muestran "Customer info retrieved" con entitlements
- [ ] Compra sandbox completa sin errores
- [ ] `_syncSubscriptionState()` se ejecuta después de compra
- [ ] `isPremiumProvider` refleja el estado correcto
- [ ] Estado persiste después de reiniciar app

---

## Contacto para Soporte

Si el problema persiste después de verificar todos los puntos:

1. Capturar logs completos del flujo de compra
2. Screenshot de configuración de RevenueCat Dashboard
3. Verificar que la versión de `purchases_flutter` sea reciente
4. Comprobar que los certificados de App Store Connect estén válidos

---

_Generado: $(date)_
_Versión: 1.0_
