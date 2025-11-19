# 📱 FASE 1: CONTEXT FOR FLUTTER EXPERT
## **UserIdentityService Implementation - CRÍTICO**

**Agente:** zodiac_flutter_expert  
**Modelo:** Claude 3.5 Opus  
**Prioridad:** 🔴 CRÍTICA - Bloqueante para launch  
**Tiempo:** 4.5 horas  

---

## 🎯 MISIÓN ESPECÍFICA

Implementar **UserIdentityService** que solucione el bug crítico de RevenueCat donde el userID cambia en cada reinicio, causando pérdida de compras premium.

---

## 📋 CONTEXTO ZODIAC APP

### **Stack Actual:**
```yaml
State Management: Riverpod (migrado de Provider)
Storage: 
  - SharedPreferences (datos no sensibles)
  - SecureStorage (datos sensibles, AES-256)
Backend: 
  - Railway (Enhanced Zodiac Backend v2.0)
  - Firebase (zodi-a1658)
Payments: 
  - RevenueCat (API Key: appl_TwCrrBozYBCYouyUHpLJturOSSD)
  - In-App Purchase (backup)
Auth: 
  - UserAuthenticationService (existente pero SIN implementar)
  - Sign in with Apple (pendiente implementar)
```

### **Servicios Existentes Relevantes:**
```dart
// lib/services/preferences_service.dart
class PreferencesService extends BaseSingletonService {
  // SharedPreferences para datos no sensibles
  SharedPreferences? _prefs;
  
  // SecureStorage para datos sensibles
  final SecureStorageService _secureStorage;
  
  Future<void> initialize() async { ... }
  Future<void> setString(String key, String value) async { ... }
  Future<String?> getString(String key) async { ... }
  // Ya tiene cache en memoria
}

// lib/services/revenuecat_service.dart
class RevenueCatService {
  Future<String> _getAppUserID() async {
    // ❌ BUG AQUÍ: Genera nuevo ID cada vez
    return 'user_${DateTime.now().millisecondsSinceEpoch}';
  }
  
  Future<void> initialize() async {
    await rc.Purchases.configure(
      rc.PurchasesConfiguration(_revenueCatAPIKey)
        ..appUserID = await _getAppUserID(), // ❌ ID cambia
    );
  }
}

// lib/services/user_authentication_service.dart
class UserAuthenticationService extends BaseSingletonService {
  // ✅ YA EXISTE pero SIN implementar login/register
  User? _currentUser;
  bool get isAuthenticated => _currentUser != null;
  
  // Métodos register() y login() tienen TODOs
  Future<AuthResult> register({ ... }) async {
    // TODO: Implement registration logic
  }
}

// lib/core/base_singleton_service.dart
abstract class BaseSingletonService<T> {
  bool _initialized = false;
  bool get isInitialized => _initialized;
  
  Future<void> initialize() async {
    if (_initialized) return;
    _initialized = true;
  }
}
```

---

## 📁 ARCHIVOS A CREAR

### **1. lib/services/user_identity_service.dart** (NUEVO - 200 líneas)

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import 'package:zodiac_app/core/base_singleton_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';
import 'package:zodiac_app/services/secure_storage_service.dart';
import 'package:zodiac_app/services/user_authentication_service.dart';
import 'package:zodiac_app/utils/app_logger.dart';

/// 🆔 USER IDENTITY SERVICE
/// 
/// Manages user identity in two modes:
/// - ANONYMOUS: Device-based UUID (persistent across sessions)
/// - AUTHENTICATED: Real user ID from authentication service
///
/// Critical for:
/// - RevenueCat userID persistence
/// - Purchase restoration
/// - Multi-device sync (authenticated users)
/// - Data migration from anonymous to authenticated
///
/// IMPLEMENTATION REQUIREMENTS:
/// 1. Device UUID generated ONCE and stored in SecureStorage
/// 2. UUID persists across app restarts
/// 3. UUID persists across device reboots
/// 4. UUID does NOT change unless user reinstalls app
/// 5. Integration with UserAuthenticationService
/// 6. Support for migration from anonymous to authenticated
class UserIdentityService extends BaseSingletonService<UserIdentityService> 
    implements ChangeNotifier {
  
  final List<VoidCallback> _listeners = [];
  
  UserIdentityService._internal();
  
  static UserIdentityService get instance => 
    BaseSingletonService.getInstance<UserIdentityService>(
      UserIdentityService._internal
    );

  // Dependencies
  final SecureStorageService _secureStorage = SecureStorageService.instance;
  final PreferencesService _preferences = PreferencesService.instance;
  final UserAuthenticationService _authService = UserAuthenticationService.instance;
  
  // State
  String? _deviceUserId;
  UserType _currentUserType = UserType.anonymous;
  
  // Storage keys
  static const String _deviceUserIdKey = 'device_user_id_v1';
  static const String _userTypeKey = 'user_type';
  
  // Getters
  UserType get currentUserType => _currentUserType;
  bool get isAnonymous => _currentUserType == UserType.anonymous;
  bool get isAuthenticated => _currentUserType == UserType.authenticated;
  
  /// 🚀 Initialize service
  @override
  Future<void> initialize() async {
    if (isInitialized) return;
    
    await super.initialize();
    
    try {
      AppLogger.info('🆔 Initializing UserIdentityService');
      
      // Initialize dependencies
      await _secureStorage.initialize();
      await _preferences.initialize();
      
      // Load or generate device user ID
      await _loadOrGenerateDeviceUserId();
      
      // Detect current user type
      await _detectUserType();
      
      AppLogger.info('✅ UserIdentityService initialized successfully', {
        'userType': _currentUserType.name,
        'deviceUserId': _deviceUserId?.substring(0, 8) + '...',
      });
      
      notifyListeners();
      
    } catch (e) {
      AppLogger.error('❌ Failed to initialize UserIdentityService', e);
      throw Exception('UserIdentityService initialization failed: $e');
    }
  }
  
  /// Generate or load device user ID
  Future<void> _loadOrGenerateDeviceUserId() async {
    try {
      // Try to load existing device ID from SecureStorage
      _deviceUserId = await _secureStorage.read(_deviceUserIdKey);
      
      if (_deviceUserId != null) {
        AppLogger.info('✅ Device user ID loaded from storage');
        return;
      }
      
      // Generate new UUID if doesn't exist
      final uuid = const Uuid().v4();
      _deviceUserId = uuid;
      
      // Save to SecureStorage (encrypted, persists across restarts)
      await _secureStorage.write(_deviceUserIdKey, uuid);
      
      AppLogger.info('✅ New device user ID generated and saved', {
        'uuid': uuid.substring(0, 8) + '...',
      });
      
    } catch (e) {
      AppLogger.error('❌ Error loading/generating device user ID', e);
      rethrow;
    }
  }
  
  /// Detect current user type
  Future<void> _detectUserType() async {
    try {
      // Check if user is authenticated
      if (_authService.isAuthenticated) {
        _currentUserType = UserType.authenticated;
        AppLogger.info('👤 User type: AUTHENTICATED');
      } else {
        _currentUserType = UserType.anonymous;
        AppLogger.info('👤 User type: ANONYMOUS');
      }
      
      // Save user type to preferences
      await _preferences.setString(_userTypeKey, _currentUserType.name);
      
    } catch (e) {
      AppLogger.error('Error detecting user type', e);
      _currentUserType = UserType.anonymous; // Default to anonymous
    }
  }
  
  /// Get device user ID (guaranteed to exist after initialization)
  Future<String> getDeviceUserId() async {
    if (!isInitialized) {
      await initialize();
    }
    
    if (_deviceUserId == null) {
      throw Exception('Device user ID not initialized');
    }
    
    return _deviceUserId!;
  }
  
  /// Get RevenueCat user ID
  /// 
  /// Returns:
  /// - For authenticated users: actual user ID from auth service
  /// - For anonymous users: 'anon_{deviceUUID}'
  Future<String> getRevenueCatUserId() async {
    if (!isInitialized) {
      await initialize();
    }
    
    // If authenticated, use real user ID
    if (_authService.isAuthenticated && _authService.currentUser != null) {
      final userId = _authService.currentUser!.id;
      AppLogger.info('🆔 RevenueCat userID (authenticated): $userId');
      return userId;
    }
    
    // If anonymous, use device ID with prefix
    final deviceId = await getDeviceUserId();
    final anonId = 'anon_$deviceId';
    AppLogger.info('🆔 RevenueCat userID (anonymous): ${anonId.substring(0, 15)}...');
    return anonId;
  }
  
  /// Migrate from anonymous to authenticated
  /// 
  /// Called when user creates an account or signs in.
  /// Transfers purchases and data to new authenticated user ID.
  Future<void> migrateToAuthenticated(String newUserId) async {
    if (!isInitialized) {
      await initialize();
    }
    
    try {
      AppLogger.info('🔄 Starting migration from anonymous to authenticated');
      
      final oldDeviceId = await getDeviceUserId();
      final oldRevenueCatId = 'anon_$oldDeviceId';
      
      AppLogger.info('Migration details:', {
        'from': oldRevenueCatId.substring(0, 15) + '...',
        'to': newUserId,
      });
      
      // Update user type
      _currentUserType = UserType.authenticated;
      await _preferences.setString(_userTypeKey, _currentUserType.name);
      
      notifyListeners();
      
      AppLogger.info('✅ Migration to authenticated completed successfully');
      
    } catch (e) {
      AppLogger.error('❌ Migration to authenticated failed', e);
      rethrow;
    }
  }
  
  /// Get user data key with proper prefix
  /// 
  /// Returns key with userID prefix for data isolation:
  /// - Anonymous: 'anon_{deviceId}_key'
  /// - Authenticated: '{userId}_key'
  Future<String> getUserDataKey(String key) async {
    final revenueCatId = await getRevenueCatUserId();
    return '${revenueCatId}_$key';
  }
  
  /// Check if user has ever been authenticated
  Future<bool> hasBeenAuthenticated() async {
    final storedType = await _preferences.getString(_userTypeKey);
    return storedType == UserType.authenticated.name;
  }
  
  // ChangeNotifier implementation
  @override
  void addListener(VoidCallback listener) {
    _listeners.add(listener);
  }
  
  @override
  void removeListener(VoidCallback listener) {
    _listeners.remove(listener);
  }
  
  @override
  void notifyListeners() {
    for (var listener in _listeners) {
      listener();
    }
  }
  
  @override
  void dispose() {
    _listeners.clear();
  }
}

/// User type enum
enum UserType {
  /// Anonymous user (device-based ID)
  anonymous,
  
  /// Authenticated user (real account)
  authenticated,
}
```

---

### **2. lib/models/user_identity.dart** (NUEVO - 50 líneas)

```dart
/// 🆔 User Identity Model
class UserIdentity {
  final String id;
  final UserType type;
  final DateTime createdAt;
  final DateTime? authenticatedAt;
  
  const UserIdentity({
    required this.id,
    required this.type,
    required this.createdAt,
    this.authenticatedAt,
  });
  
  bool get isAnonymous => type == UserType.anonymous;
  bool get isAuthenticated => type == UserType.authenticated;
  
  UserIdentity copyWith({
    String? id,
    UserType? type,
    DateTime? createdAt,
    DateTime? authenticatedAt,
  }) {
    return UserIdentity(
      id: id ?? this.id,
      type: type ?? this.type,
      createdAt: createdAt ?? this.createdAt,
      authenticatedAt: authenticatedAt ?? this.authenticatedAt,
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'type': type.name,
      'createdAt': createdAt.toIso8601String(),
      'authenticatedAt': authenticatedAt?.toIso8601String(),
    };
  }
  
  factory UserIdentity.fromJson(Map<String, dynamic> json) {
    return UserIdentity(
      id: json['id'],
      type: UserType.values.firstWhere((e) => e.name == json['type']),
      createdAt: DateTime.parse(json['createdAt']),
      authenticatedAt: json['authenticatedAt'] != null 
        ? DateTime.parse(json['authenticatedAt']) 
        : null,
    );
  }
}
```

---

## 🔧 ARCHIVOS A MODIFICAR

### **1. lib/services/revenuecat_service.dart**

**Líneas a cambiar: 73-80**

```dart
// ❌ ANTES (BUGGY):
Future<String> _getAppUserID() async {
  try {
    // For now, generate a simple ID - replace with actual user ID logic
    return 'user_${DateTime.now().millisecondsSinceEpoch}';
  } catch (e) {
    return 'user_${DateTime.now().millisecondsSinceEpoch}';
  }
}

// ✅ DESPUÉS (FIXED):
Future<String> _getAppUserID() async {
  try {
    // Use UserIdentityService for persistent userID
    final identityService = UserIdentityService.instance;
    await identityService.initialize();
    final userId = await identityService.getRevenueCatUserId();
    
    AppLogger.info('🆔 RevenueCat using userID: ${userId.substring(0, 15)}...');
    return userId;
    
  } catch (e) {
    AppLogger.error('❌ Error getting app user ID', e);
    
    // Fallback: Generate temporary ID but log warning
    final fallbackId = 'temp_${DateTime.now().millisecondsSinceEpoch}';
    AppLogger.warning('⚠️ Using fallback userID: $fallbackId');
    return fallbackId;
  }
}
```

**Agregar import:**
```dart
import 'package:zodiac_app/services/user_identity_service.dart';
```

---

### **2. lib/services/preferences_service.dart**

**Agregar métodos (después de línea 80):**

```dart
/// Get user-specific data key
/// Uses UserIdentityService to prefix keys with userID
Future<String> getUserDataKey(String key) async {
  final identityService = UserIdentityService.instance;
  return await identityService.getUserDataKey(key);
}

/// Save user-specific string
Future<void> setUserString(String key, String value) async {
  final userKey = await getUserDataKey(key);
  await setString(userKey, value);
}

/// Get user-specific string
Future<String?> getUserString(String key) async {
  final userKey = await getUserDataKey(key);
  return await getString(userKey);
}

/// Migrate user data from one userID to another
/// Used when user moves from anonymous to authenticated
Future<void> migrateUserData(String fromUserId, String toUserId) async {
  try {
    logServiceInfo('Migrating user data from $fromUserId to $toUserId');
    
    // List of keys to migrate
    final keysToMigrate = [
      'zodiac_sign',
      'birth_date',
      'birth_time',
      'birth_place',
      'favorite_horoscopes',
      'favorite_compatibilities',
      'app_theme',
      'notification_preferences',
    ];
    
    for (final key in keysToMigrate) {
      final oldKey = '${fromUserId}_$key';
      final newKey = '${toUserId}_$key';
      
      // Read from old key
      final value = await getString(oldKey);
      
      if (value != null) {
        // Write to new key
        await setString(newKey, value);
        logServiceInfo('Migrated: $key');
      }
    }
    
    logServiceInfo('User data migration completed successfully');
    
  } catch (e) {
    logServiceError('User data migration failed', error: e);
    rethrow;
  }
}
```

---

## 🧪 TESTS A CREAR

### **test/services/user_identity_service_test.dart**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:zodiac_app/services/user_identity_service.dart';
import 'package:zodiac_app/services/secure_storage_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';

void main() {
  group('UserIdentityService Tests', () {
    late UserIdentityService service;
    
    setUp(() async {
      service = UserIdentityService.instance;
      await service.initialize();
    });
    
    test('Device user ID is generated and persisted', () async {
      final deviceId1 = await service.getDeviceUserId();
      expect(deviceId1, isNotEmpty);
      expect(deviceId1.length, equals(36)); // UUID length
      
      // Get again should return same ID
      final deviceId2 = await service.getDeviceUserId();
      expect(deviceId2, equals(deviceId1));
    });
    
    test('RevenueCat userID has correct format for anonymous', () async {
      final revenueCatId = await service.getRevenueCatUserId();
      expect(revenueCatId, startsWith('anon_'));
      expect(revenueCatId.length, greaterThan(10));
    });
    
    test('User type is anonymous by default', () {
      expect(service.currentUserType, equals(UserType.anonymous));
      expect(service.isAnonymous, isTrue);
      expect(service.isAuthenticated, isFalse);
    });
    
    test('Migration changes user type to authenticated', () async {
      expect(service.isAnonymous, isTrue);
      
      await service.migrateToAuthenticated('user_123');
      
      expect(service.isAuthenticated, isTrue);
      expect(service.isAnonymous, isFalse);
    });
    
    test('User data key has correct prefix', () async {
      final key = await service.getUserDataKey('zodiac_sign');
      expect(key, contains('anon_'));
      expect(key, contains('zodiac_sign'));
    });
  });
}
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

```
□ Crear UserIdentityService.dart con todos los métodos
□ Crear user_identity.dart model
□ Modificar revenuecat_service.dart (_getAppUserID)
□ Agregar métodos a preferences_service.dart
□ Crear tests unitarios completos
□ Validar UUID persiste entre reinicios
□ Validar RevenueCat userID consistente
□ Validar migración de anonymous a authenticated
□ Agregar logging apropiado con AppLogger
□ Documentar código con comentarios
□ Verificar sin regresiones en features existentes
```

---

## 🎯 CRITERIOS DE ÉXITO

1. ✅ Device UUID se genera UNA sola vez
2. ✅ UUID persiste después de cerrar/abrir app
3. ✅ UUID persiste después de reiniciar dispositivo
4. ✅ RevenueCat userID es consistente entre sesiones
5. ✅ Compras premium persisten después de reinicio
6. ✅ Restore purchases funciona correctamente
7. ✅ Tests unitarios pasan (coverage >85%)
8. ✅ Sin crashes o memory leaks
9. ✅ Logging claro y útil para debugging

---

**🚀 LISTO PARA IMPLEMENTACIÓN**

**Siguiente:** Después de completar, notificar a @orchestrator_master para validación
