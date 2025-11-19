# 🏗️ Guía de Arquitectura del Sistema Premium - Zodiac App

**Última actualización**: Octubre 26, 2025
**Propósito**: Documentación completa de cómo funciona el sistema de tiers premium en cada archivo

---

## 📋 Índice

1. [Resumen del Sistema](#resumen-del-sistema)
2. [Modelos](#modelos)
3. [Servicios](#servicios)
4. [Providers](#providers)
5. [Pantallas](#pantallas)
6. [Widgets](#widgets)
7. [Flujo de Datos](#flujo-de-datos)

---

## 🎯 Resumen del Sistema

### Los 4 Tiers Premium:
```
FREE (0)      → Gratis, funciones básicas
COSMIC (1)    → $6.99/mes - Premium básico, 10 AI insights/día
STELLAR (2)   → $19.99/mes - Premium avanzado, AI ilimitado + Crisis AI
UNIVERSE (3)  → $49.99 one-time - Lifetime, todo incluido
```

### Stack Tecnológico:
- **State Management**: Riverpod
- **Payments**: RevenueCat
- **Backend**: SubscriptionService
- **Storage**: iOS Keychain via SecureStorage

---

## 📦 Modelos

### `lib/models/subscription_tier.dart`

**¿Qué hace este archivo?**
Define el enum `PremiumTier` con los 4 niveles de subscripción.

**Estructura:**
```dart
enum PremiumTier {
  free(0, 'Free Trial'),      // Usuario gratis
  cosmic(1, 'Cosmic'),        // $6.99/mes
  stellar(2, 'Stellar'),      // $19.99/mes
  universe(3, 'Universe'),    // $49.99 lifetime
}
```

**Propiedades:**
- `level: int` - Nivel jerárquico (0-3)
- `displayName: String` - Nombre para mostrar en UI

**Métodos útiles:**
```dart
bool isHigherThan(PremiumTier other) // Compara niveles
bool isAtLeast(PremiumTier other)    // Verifica si cumple tier mínimo
```

**¿Cuándo se usa?**
- En `SubscriptionService` para saber el tier actual del usuario
- En `currentTierProvider` para exponer el tier a la UI
- En cualquier lugar que necesite distinguir entre tiers específicos

---

## 🔧 Servicios

### `lib/services/subscription_service.dart`

**¿Qué hace este archivo?**
Servicio principal que gestiona el estado de subscripción del usuario. Es el "cerebro" del sistema premium.

**Responsabilidades:**
1. ✅ Leer el tier actual desde RevenueCat
2. ✅ Detectar cambios en subscripción
3. ✅ Proveer estado premium a toda la app
4. ✅ Sincronizar con backend

**Propiedades Clave:**

```dart
// Línea 87 - GETTER MÁS IMPORTANTE
PremiumTier get currentTier {
  // Lee el tier desde RevenueCatService
  // Este es el SINGLE SOURCE OF TRUTH
  return _revenueCatService.currentTier;
}

// Línea 695 - Derivados del tier
bool get isPremium => currentTier != PremiumTier.free;
bool get isLifetime => currentTier == PremiumTier.universe;
bool get isMonthly => currentTier == PremiumTier.cosmic;
bool get isFree => currentTier == PremiumTier.free;
```

**Flow de Datos:**
```
RevenueCat SDK
    ↓
RevenueCatService.currentTier (lee entitlements)
    ↓
SubscriptionService.currentTier (expone a la app)
    ↓
currentTierProvider (Riverpod provider)
    ↓
UI Screens (leen el tier)
```

**¿Cómo se inicializa?**
```dart
// Se inicializa automáticamente como singleton
final service = SubscriptionService.instance;
await service.initialize();
```

---

### `lib/services/revenuecat_service.dart`

**¿Qué hace este archivo?**
Wrapper de RevenueCat SDK. Maneja la comunicación directa con RevenueCat para detectar subscripciones.

**Responsabilidades:**
1. ✅ Configurar RevenueCat SDK
2. ✅ Leer `customerInfo` (entitlements)
3. ✅ Detectar qué tier tiene el usuario
4. ✅ Escuchar cambios en tiempo real

**Método Clave:**

```dart
// Línea 229 (aproximadamente) - GETTER CRÍTICO
PremiumTier get currentTier {
  final customerInfo = _customerInfo;
  if (customerInfo == null) return PremiumTier.free;

  // Revisa entitlements de RevenueCat
  final entitlements = customerInfo.entitlements.active;

  if (entitlements.containsKey('universe')) return PremiumTier.universe;
  if (entitlements.containsKey('stellar')) return PremiumTier.stellar;
  if (entitlements.containsKey('cosmic')) return PremiumTier.cosmic;

  return PremiumTier.free;
}
```

**¿Cuándo se actualiza?**
- Al abrir la app
- Cuando completas una compra
- Cada vez que RevenueCat notifica cambios
- Cuando se sincroniza manualmente

**⚠️ IMPORTANTE:**
Este servicio tiene los infames print statements que causaban freeze:
```dart
// ❌ EVITAR: Print statements en getters que se llaman 100x/segundo
print('🚨🚨🚨 CRITICAL DEBUG - currentTier getter - Entitlements: []');
```

---

## 🔌 Providers

### `lib/providers/unified_premium_integration_provider.dart`

**¿Qué hace este archivo?**
Hub central de providers de Riverpod. Conecta servicios con la UI.

**Providers Principales:**

#### 1. `currentTierProvider` (NUEVO - Oct 26, 2025)
```dart
// Línea 308
final currentTierProvider = Provider<PremiumTier>((ref) {
  final subscriptionService = ref.watch(subscriptionServiceProvider);
  return subscriptionService.currentTier;
});
```

**¿Qué devuelve?** `PremiumTier` enum (free/cosmic/stellar/universe)

**¿Cuándo usarlo?**
- Cuando necesites distinguir entre tiers específicos
- Para mostrar features exclusivas de Stellar o Universe
- Para limitar features según tier (ej: 10 vs ilimitado)

**Ejemplo de uso:**
```dart
final tier = ref.watch(currentTierProvider);

if (tier == PremiumTier.stellar || tier == PremiumTier.universe) {
  return UnlimitedAIWidget();
} else if (tier == PremiumTier.cosmic) {
  return LimitedAIWidget(limit: 10);
} else {
  return UpgradePromptWidget();
}
```

---

#### 2. `isPremiumUserProvider` (EXISTENTE)
```dart
// Línea 315
final isPremiumUserProvider = Provider<bool>((ref) {
  final subscriptionService = ref.watch(subscriptionServiceProvider);
  return subscriptionService.isPremium;
});
```

**¿Qué devuelve?** `bool` (true si tiene cualquier tier pago)

**¿Cuándo usarlo?**
- Cuando solo necesites saber "¿es premium o gratis?"
- Para mostrar/ocultar contenido premium genérico
- Cuando no importa si es Cosmic, Stellar o Universe

**Ejemplo de uso:**
```dart
final isPremium = ref.watch(isPremiumUserProvider);

if (isPremium) {
  return PremiumContentWidget();
} else {
  return FreeContentWidget();
}
```

---

#### 3. `subscriptionServiceProvider`
```dart
// En consolidated_providers.dart
final subscriptionServiceProvider = Provider((ref) {
  return SubscriptionService.instance;
});
```

**¿Qué devuelve?** Instancia del `SubscriptionService`

**¿Cuándo usarlo?**
- Cuando necesites acceso directo al servicio
- Para llamar métodos como `syncSubscriptionState()`
- Para leer propiedades específicas como `isLifetime`, `isMonthly`

---

### `lib/providers/consolidated_providers.dart`

**¿Qué hace este archivo?**
Agrupa todos los providers principales de la app en un solo lugar.

**Providers Premium relevantes:**
```dart
final subscriptionServiceProvider = Provider((ref) => SubscriptionService.instance);
final revenueCatIntegrationProvider = Provider((ref) => RevenueCatIntegration.instance);
final premiumControllerProvider = StateNotifierProvider(...);
```

---

## 📱 Pantallas

### `lib/screens/home_screen.dart`

**¿Qué hace este archivo?**
Pantalla principal de la app. Muestra horóscopo diario y navegación.

**Uso de Premium (línea 977):**
```dart
final bool shouldNavigateToAnalytics = ref.watch(isPremiumUserProvider);

if (shouldNavigateToAnalytics) {
  // Usuario premium puede acceder a analytics
  Navigator.pushNamed(context, '/analytics');
} else {
  // Usuario free ve upgrade prompt
  showUpgradeDialog();
}
```

**Decisión de diseño:**
Usa `isPremiumUserProvider` (bool) porque solo necesita saber si es premium o no. No importa si es Cosmic, Stellar o Universe para esta funcionalidad.

---

### `lib/screens/premium_screen.dart`

**¿Qué hace este archivo?**
Pantalla de suscripción/upgrade. Muestra planes premium y maneja compras.

**Uso de Premium (línea 3675):**
```dart
Consumer(
  builder: (context, ref, _) {
    final isPremium = ref.watch(isPremiumUserProvider);
    return Text(
      '🔍 isPremiumUserProvider: ${isPremium ? "TRUE ✅" : "FALSE ❌"}',
      style: TextStyle(
        color: isPremium ? Colors.green : Colors.red,
        fontSize: 11,
        fontWeight: FontWeight.bold,
      ),
    );
  },
),
```

**Propósito:**
Debug widget para mostrar el estado premium actual. Útil para verificar que RevenueCat está funcionando.

**Futuro:**
Esta pantalla debería usar `currentTierProvider` para mostrar exactamente QUÉ tier tiene el usuario y ofrecer upgrades específicos (ej: Cosmic → Stellar).

---

### `lib/screens/cosmic_coach_screen.dart`

**¿Qué hace este archivo?**
Pantalla de Cosmic Coach (AI coaching). Muestra guías personalizadas.

**Uso de Premium (línea 361):**
```dart
Consumer(
  builder: (context, ref, _) {
    final isPremium = ref.watch(isPremiumUserProvider);

    if (isPremium) {
      return _buildAdvancedCosmicCoachFeatures(languageCode);
    } else {
      return _buildCosmicCoachTeaser(languageCode);
    }
  },
),
```

**Lógica:**
- **Premium users** (Cosmic/Stellar/Universe): Ven features avanzadas
- **Free users**: Ven teaser con upgrade prompt

**Futuro mejorado:**
```dart
final tier = ref.watch(currentTierProvider);

switch (tier) {
  case PremiumTier.stellar:
  case PremiumTier.universe:
    return _buildUnlimitedAICoach();  // AI ilimitado

  case PremiumTier.cosmic:
    return _buildLimitedAICoach(limit: 10);  // 10 insights/día

  case PremiumTier.free:
    return _buildCoachTeaser();  // Upgrade prompt
}
```

---

## 🧩 Widgets

### `lib/widgets/monetization/premium_feature_gate.dart`

**¿Qué hace este archivo?**
Widget reutilizable que bloquea contenido premium. Muestra upgrade prompt para usuarios free.

**Uso típico:**
```dart
PremiumFeatureGate(
  child: AdvancedAstroChart(),  // Contenido premium
  fallback: UpgradePrompt(),    // Qué mostrar si no es premium
)
```

**Implementación interna:**
```dart
class PremiumFeatureGate extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isPremium = ref.watch(isPremiumUserProvider);

    if (isPremium) {
      return child;  // Mostrar contenido premium
    } else {
      return fallback ?? _defaultUpgradePrompt();
    }
  }
}
```

**⚠️ IMPORTANTE:**
Este widget tenía el print statement problemático que causaba freeze:
```dart
// ❌ EVITAR en build()
print('🚪 [PremiumFeatureGate] DEBUG BYPASS ENABLED - showing content');
```

---

## 🔄 Flujo de Datos Completo

### 1. **Al Iniciar la App**

```
1. main.dart
   ↓
2. RevenueCatService.initialize()
   ↓ (conecta con RevenueCat SDK)
3. RevenueCat SDK lee subscripciones del usuario
   ↓ (descarga customerInfo)
4. RevenueCatService.currentTier
   ↓ (detecta tier basado en entitlements)
5. SubscriptionService.currentTier
   ↓ (expone a providers)
6. currentTierProvider & isPremiumUserProvider
   ↓ (Riverpod notifica a listeners)
7. UI se actualiza automáticamente
```

### 2. **Cuando el Usuario Compra Premium**

```
1. Usuario hace tap en "Subscribe"
   ↓
2. premium_screen.dart llama RevenueCat.purchase()
   ↓
3. RevenueCat procesa pago con Apple
   ↓
4. RevenueCat notifica cambio en subscripción
   ↓
5. RevenueCatService._updateSubscriptionTier()
   ↓
6. SubscriptionService detecta nuevo tier
   ↓
7. Providers se actualizan (currentTierProvider, isPremiumUserProvider)
   ↓
8. UI reacciona automáticamente:
   - Premium gates se abren
   - Pantallas muestran contenido premium
   - Teaser prompts desaparecen
```

### 3. **Cuando la App Verifica Estado**

```
1. Usuario abre la app
   ↓
2. SubscriptionService.syncSubscriptionState()
   ↓
3. RevenueCat SDK verifica con servidor
   ↓
4. Si hay cambios:
   - Actualiza customerInfo
   - Notifica a listeners
   - Providers reactivos actualizan UI
```

---

## 🐛 Problemas Comunes y Soluciones

### Problema 1: "App se congela / corre lento"
**Causa**: Print statements en getters que se ejecutan cientos de veces por segundo

**Archivos afectados:**
- `revenuecat_service.dart` (línea 229)
- `premium_feature_gate.dart` (línea 40)

**Solución:**
```dart
// ❌ MAL - En getter que se llama frecuentemente
PremiumTier get currentTier {
  print('🚨 DEBUG - currentTier called');  // ← Ejecuta 100x/seg
  return _tier;
}

// ✅ BIEN - Solo en métodos que se llaman ocasionalmente
Future<void> syncSubscriptionState() async {
  print('🔄 Syncing subscription state');  // ← Ejecuta 1x/30min
  await _sync();
}
```

---

### Problema 2: "Provider devuelve bool pero necesito tier específico"
**Causa**: Usando `isPremiumUserProvider` cuando necesitas `currentTierProvider`

**Solución:**
```dart
// ❌ MAL - No puedo distinguir Cosmic vs Stellar
final isPremium = ref.watch(isPremiumUserProvider);
if (isPremium) {
  // ¿Pero cuál tier? No sé...
}

// ✅ BIEN - Puedo distinguir cada tier
final tier = ref.watch(currentTierProvider);
if (tier == PremiumTier.stellar || tier == PremiumTier.universe) {
  showUnlimitedFeature();
} else if (tier == PremiumTier.cosmic) {
  showLimitedFeature();
}
```

---

### Problema 3: "Errores de compilación después de git revert"
**Causa**: Archivos esperan `AsyncValue<bool>` pero provider devuelve `bool`

**Archivos afectados:**
- `home_screen.dart` (línea 977)
- `premium_screen.dart` (línea 3674)
- `cosmic_coach_screen.dart` (línea 363)

**Solución:**
Ver [TIER_SYSTEM_FIX_DOCUMENTATION.md](TIER_SYSTEM_FIX_DOCUMENTATION.md) para los cambios específicos.

---

## �� Glosario

**Terms:**

- **Tier**: Nivel de subscripción (free/cosmic/stellar/universe)
- **Entitlement**: Permiso de RevenueCat que indica qué compró el usuario
- **Provider**: Objeto de Riverpod que expone estado a la UI
- **customerInfo**: Objeto de RevenueCat con toda la info de subscripción del usuario
- **Single Source of Truth**: Un único lugar donde se almacena el dato oficial (RevenueCatService.currentTier)

---

## 🔗 Referencias Útiles

- **RevenueCat Docs**: https://docs.revenuecat.com/
- **Riverpod Docs**: https://riverpod.dev/
- **Pricing Constants**: Ver `lib/utils/pricing_constants.dart`
- **Subscription Models**: Ver `lib/models/subscription_tier.dart`

---

**Última actualización**: Octubre 26, 2025
**Mantenedor**: Claude Code
**Para preguntas**: Revisar esta guía primero, luego buscar en código