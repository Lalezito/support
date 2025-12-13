# 🔧 USER ID TEMPORAL FIX - Sesión de Debugging

**Fecha**: 21 de octubre 2025 - 22:30+
**Problema**: User ID temporal impide persistencia de compras
**Prioridad**: 🔴 CRÍTICA

---

## 🎯 OBJETIVO

Arreglar el sistema de User ID para que:
1. Use UUID persistente en lugar de `temp_XXXXX`
2. Las compras persistan entre sesiones de app
3. Restore Purchases funcione correctamente

---

## 📋 ACCIONES REALIZADAS

### 1. Logging Detallado Agregado

**Archivo**: `lib/services/revenuecat_service.dart`
**Método**: `_getAppUserID()` (líneas 120-151)

**Logging agregado**:
```dart
print('🔍 [_getAppUserID] Step 1: Getting UserIdentityService instance');
print('🔍 [_getAppUserID] Step 2: Initializing UserIdentityService');
print('🔍 [_getAppUserID] Step 3: Getting RevenueCat user ID');
print('🔍 [_getAppUserID] Step 4: SUCCESS - Got userID: ...');

// En caso de error:
print('🚨🚨🚨 CRITICAL ERROR in _getAppUserID:');
print('Error Type: ${e.runtimeType}');
print('Error Message: $e');
print('Stack Trace: $stackTrace');
print('⚠️ Using TEMPORARY fallback ID: $fallbackId');
```

**Propósito**: Identificar en qué paso exacto falla UserIdentityService

---

## 🔍 DIAGNÓSTICO ESPERADO

### Escenario A: Falla en Step 1 (Getting instance)
```
🔍 Step 1: Getting UserIdentityService instance
🚨🚨🚨 CRITICAL ERROR
Error Type: ...
```
**Causa probable**: BaseSingletonService tiene un problema

### Escenario B: Falla en Step 2 (Initialize)
```
🔍 Step 1: Getting UserIdentityService instance
🔍 Step 2: Initializing UserIdentityService
🚨🚨🚨 CRITICAL ERROR
Error Type: ...
```
**Causa probable**: SecureStorageService.initialize() falla

### Escenario C: Falla en Step 3 (Get User ID)
```
🔍 Step 1: Getting UserIdentityService instance
🔍 Step 2: Initializing UserIdentityService
🔍 Step 3: Getting RevenueCat user ID
🚨🚨🚨 CRITICAL ERROR
Error Type: ...
```
**Causa probable**: getRevenueCatUserId() tiene un problema

---

## 🧪 TESTING PLAN

### Test 1: Verificar Logs en Consola
Después de compilar y correr la app:

1. Buscar en logs los mensajes que empiezan con `🔍 [_getAppUserID]`
2. Ver en qué Step se detiene
3. Capturar el error exacto mostrado

### Test 2: Verificar Debug Banner
En la pantalla de Premium, el debug banner mostrará:

**Si el fix funciona**:
```
User ID: anon_XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

**Si sigue fallando**:
```
User ID: temp_1761041078121
```

---

## 🔧 FIXES POTENCIALES BASADOS EN ERROR

### Si el error es: "SecureStorage not initialized"
**Fix**: Asegurar que SecureStorage se inicializa ANTES de UserIdentityService
```dart
// En main.dart o app initialization
await SecureStorageService.instance.initialize();
await UserIdentityService.instance.initialize();
```

### Si el error es: "Keychain access denied"
**Fix**: Verificar entitlements de iOS
```xml
<!-- ios/Runner/Runner.entitlements -->
<key>keychain-access-groups</key>
<array>
  <string>$(AppIdentifierPrefix)com.zodia.zodiacapp</string>
</array>
```

### Si el error es: "UUID package not found"
**Fix**: Verificar que el package uuid está en pubspec.yaml
```yaml
dependencies:
  uuid: ^3.0.0  # o versión actual
```

### Si el error es: "Device ID is null"
**Fix**: Usar fallback a SharedPreferences si SecureStorage falla
```dart
// En UserIdentityService._loadOrGenerateDeviceUserId()
try {
  _deviceUserId = await _secureStorage.read(_deviceUserIdKey);
} catch (e) {
  // Fallback to SharedPreferences
  _deviceUserId = await _preferences.getString(_deviceUserIdKey);
}
```

---

## 📊 ESTADO ACTUAL

**Compilación**: En progreso (background process 738d10)
**Logs guardados en**: `/tmp/flutter_final_debug.log`
**Próximo paso**: Analizar logs cuando la app arranque

---

## ⏭️ PRÓXIMOS PASOS

1. ✅ Agregar logging detallado
2. 🔄 Compilar app (en progreso)
3. ⏳ Esperar que app se instale en iPhone
4. ⏳ Revisar logs para identificar error exacto
5. ⏳ Implementar fix basado en error encontrado
6. ⏳ Probar que User ID persiste correctamente
7. ⏳ Documentar solución final

---

## 📝 NOTAS IMPORTANTES

- Este es el problema MÁS crítico porque afecta TODAS las compras
- Sin un User ID persistente, las compras se pierden al reiniciar la app
- Esto explica por qué "Restore Purchases" no funciona
- Una vez arreglado, las compras persistirán correctamente

---

**Actualizado**: 21 oct 2025 - 22:35
**Status**: Compilando con logging mejorado
**Next**: Analizar error en logs
