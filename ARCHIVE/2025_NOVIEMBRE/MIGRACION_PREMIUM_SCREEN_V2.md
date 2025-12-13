# 🔄 PLAN DE MIGRACIÓN - PREMIUM SCREEN V2
**Fecha:** 26 de Noviembre 2025
**Objetivo:** Activar PremiumScreenV2 con funcionalidad completa

---

## 📊 SITUACIÓN ACTUAL

### Estado de los Archivos

**PremiumScreenV2.dart** - `lib/screens/premium_screen_v2.dart`
- ✅ Existe y está bien diseñada visualmente
- ❌ Solo es un mock/preview
- ❌ NO está conectada en main.dart
- ❌ Botones de compra simulados (espera 2s y muestra "Próximamente")
- ❌ Precios hardcodeados ($6.99/$19.99)
- ❌ No restaura compras reales

**PremiumControllerV2.dart** - `lib/features/premium/controllers/premium_controller_v2.dart`
- ✅ Lógica de negocio completa y robusta
- ✅ Integración con RevenueCat
- ✅ Manejo de errores
- ✅ Soporte para todos los tiers
- ✅ Analytics integrado
- ❌ NO está siendo usado por ninguna UI

**Main.dart** - `lib/main.dart`
```dart
// PROBLEMA: Apunta a la versión antigua
GoRoute(
  path: '/premium',
  builder: (context, state) => const PremiumScreen(),  // ❌ Versión antigua
),
```

---

## 🎯 PLAN DE MIGRACIÓN (3 FASES)

### FASE 1: Conectar PremiumScreenV2 con PremiumControllerV2 (2-3 horas)

#### Paso 1.1: Refactorizar PremiumScreenV2

**Archivo:** `lib/screens/premium_screen_v2.dart`

**Cambios Necesarios:**

1. **Agregar Provider de Controller:**
```dart
// ANTES (línea ~25):
class PremiumScreenV2 extends StatefulWidget {
  const PremiumScreenV2({super.key});

  @override
  State<PremiumScreenV2> createState() => _PremiumScreenV2State();
}

// DESPUÉS:
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../features/premium/controllers/premium_controller_v2.dart';

class PremiumScreenV2 extends ConsumerStatefulWidget {  // ← Cambio
  const PremiumScreenV2({super.key});

  @override
  ConsumerState<PremiumScreenV2> createState() => _PremiumScreenV2State();
}

class _PremiumScreenV2State extends ConsumerState<PremiumScreenV2>  // ← Cambio
    with SingleTickerProviderStateMixin {
```

2. **Reemplazar Mock Purchase Logic:**
```dart
// ANTES (línea ~450-470 aprox):
void _handlePurchase(String tierName) {
  setState(() {
    _isProcessingPurchase = true;
  });

  // Simular compra
  Future.delayed(Duration(seconds: 2), () {
    if (mounted) {
      setState(() {
        _isProcessingPurchase = false;
      });
      _showComingSoonDialog();
    }
  });
}

// DESPUÉS:
Future<void> _handlePurchase(PremiumTier tier) async {
  setState(() {
    _isProcessingPurchase = true;
  });

  try {
    // Usar el controller REAL
    final controller = ref.read(premiumControllerV2Provider.notifier);
    await controller.purchaseTier(tier);

    if (mounted) {
      // Mostrar success
      _showSuccessDialog(tier);

      // Analytics
      AnalyticsService.logEvent('premium_purchase_success', parameters: {
        'tier': tier.name,
        'screen': 'premium_v2',
      });
    }
  } catch (e) {
    if (mounted) {
      // Mostrar error user-friendly
      _showErrorDialog(e.toString());

      // Analytics
      AnalyticsService.logEvent('premium_purchase_error', parameters: {
        'tier': tier.name,
        'error': e.toString(),
      });
    }
  } finally {
    if (mounted) {
      setState(() {
        _isProcessingPurchase = false;
      });
    }
  }
}
```

3. **Cargar Precios Reales:**
```dart
// ANTES (líneas ~100-120 aprox - precios hardcodeados):
final tiers = [
  {
    'name': 'Universe',
    'price': '\$6.99/month',  // ❌ Hardcoded
    'features': [...],
  },
  {
    'name': 'Cosmos',
    'price': '\$19.99/month',  // ❌ Hardcoded
    'features': [...],
  },
];

// DESPUÉS:
@override
void initState() {
  super.initState();
  // Cargar precios reales al iniciar
  WidgetsBinding.instance.addPostFrameCallback((_) {
    ref.read(premiumControllerV2Provider.notifier).loadProducts();
  });
}

// En el build:
@override
Widget build(BuildContext context) {
  final premiumState = ref.watch(premiumControllerV2Provider);

  return premiumState.when(
    loading: () => Center(child: CircularProgressIndicator()),
    error: (error, stack) => ErrorWidget(error: error),
    data: (state) {
      // Usar precios reales del state
      final tiers = state.availableTiers;

      return Scaffold(
        body: /* UI usando tiers reales */
      );
    },
  );
}
```

4. **Implementar Restore Purchases:**
```dart
// AGREGAR botón de restore:
TextButton(
  onPressed: _handleRestorePurchases,
  child: Text(AppLocalizations.of(context)!.restorePurchases),
)

// AGREGAR método:
Future<void> _handleRestorePurchases() async {
  try {
    setState(() => _isProcessingPurchase = true);

    final controller = ref.read(premiumControllerV2Provider.notifier);
    await controller.restorePurchases();

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(AppLocalizations.of(context)!.purchasesRestored),
          backgroundColor: Colors.green,
        ),
      );
    }
  } catch (e) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(AppLocalizations.of(context)!.restoreFailed),
          backgroundColor: Colors.red,
        ),
      );
    }
  } finally {
    if (mounted) {
      setState(() => _isProcessingPurchase = false);
    }
  }
}
```

5. **Mostrar Tier Actual del Usuario:**
```dart
// En el build, mostrar badge si ya es premium:
@override
Widget build(BuildContext context) {
  final premiumState = ref.watch(premiumControllerV2Provider);

  return premiumState.when(
    data: (state) {
      final currentTier = state.currentTier;

      return Column(
        children: [
          if (currentTier != PremiumTier.free)
            _buildCurrentTierBadge(currentTier),

          // Lista de tiers disponibles
          ...state.availableTiers.map((tier) {
            final isCurrent = tier == currentTier;
            return _buildTierCard(
              tier: tier,
              isCurrent: isCurrent,
              onPurchase: isCurrent ? null : () => _handlePurchase(tier),
            );
          }),
        ],
      );
    },
    // ... loading/error
  );
}
```

#### Paso 1.2: Actualizar Main.dart

**Archivo:** `lib/main.dart`

```dart
// ANTES:
GoRoute(
  path: '/premium',
  builder: (context, state) => const PremiumScreen(),  // ❌ Antigua
),

// DESPUÉS:
GoRoute(
  path: '/premium',
  builder: (context, state) => const PremiumScreenV2(),  // ✅ Nueva
),

// Y agregar el import:
import 'package:zodiac_app/screens/premium_screen_v2.dart';
```

#### Paso 1.3: Testing Manual

1. **Verificar que compila:**
```bash
flutter clean
flutter pub get
flutter run
```

2. **Probar flujos:**
   - [ ] Abrir screen premium
   - [ ] Ver precios reales cargados
   - [ ] Simular compra (sandbox)
   - [ ] Verificar estado actualizado
   - [ ] Probar restore purchases
   - [ ] Verificar analytics se envían

---

### FASE 2: Migrar Todos los Entry Points (1 hora)

**Archivos que referencian PremiumScreen antigua:**

Buscar y reemplazar en:
```bash
grep -r "PremiumScreen()" lib/ --include="*.dart"
```

**Entry points comunes:**
1. `lib/screens/home_screen.dart` - Botón "Upgrade"
2. `lib/widgets/premium_upsell_banner.dart` - Banner
3. `lib/screens/settings_screen.dart` - Enlace a premium
4. `lib/widgets/monetization/*.dart` - Paywalls

**Cambio en todos:**
```dart
// ANTES:
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => PremiumScreen()),
);

// DESPUÉS:
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => PremiumScreenV2()),
);

// O con GoRouter:
context.go('/premium');  // Ya apunta a V2 después de paso 1.2
```

---

### FASE 3: Cleanup y Deprecación (30 min)

#### Paso 3.1: Deprecar PremiumScreen Antigua

**Archivo:** `lib/screens/premium_screen.dart`

```dart
// Agregar al principio de la clase:
@Deprecated('Use PremiumScreenV2 instead. Will be removed in v2.0.0')
class PremiumScreen extends ConsumerStatefulWidget {
  // ... código existente
}
```

#### Paso 3.2: Renombrar Archivos (Opcional)

Si quieres que V2 sea la oficial:
```bash
cd lib/screens

# Backup de la antigua
mv premium_screen.dart premium_screen_legacy.dart

# V2 pasa a ser la oficial
mv premium_screen_v2.dart premium_screen.dart

# Actualizar imports en toda la app
find lib -name "*.dart" -type f -exec sed -i '' 's/premium_screen_v2/premium_screen/g' {} \;
```

#### Paso 3.3: Documentar Cambio

Crear `MIGRATION_PREMIUM_SCREEN.md`:
```markdown
# Premium Screen Migration

## What Changed
- PremiumScreen (old) → Deprecated
- PremiumScreenV2 → Active (now connected to PremiumControllerV2)

## Breaking Changes
None - route remains `/premium`

## For Developers
Use `PremiumScreenV2` for all new code.
Old `PremiumScreen` will be removed in v2.0.0.

## Testing Checklist
- [ ] Purchase flow works in sandbox
- [ ] Restore purchases works
- [ ] Analytics events fire
- [ ] Error handling shows user-friendly messages
- [ ] Loading states work
- [ ] All entry points updated
```

---

## 🧪 TESTING COMPLETO

### Testing en Sandbox

**iOS:**
```bash
# 1. Configurar Sandbox Tester en App Store Connect
# 2. Ejecutar en simulador/device
flutter run --flavor dev

# 3. Probar flujos:
# - Compra nueva
# - Restore purchases
# - Upgrade de tier
# - Downgrade
```

**Android:**
```bash
# 1. Configurar License Testing en Play Console
# 2. Ejecutar
flutter run --flavor dev

# 3. Probar flujos (igual que iOS)
```

### Testing Checklist

#### Flujos de Compra
- [ ] Compra Universe tier (new user)
- [ ] Compra Cosmos tier (new user)
- [ ] Upgrade de Universe → Cosmos
- [ ] Downgrade de Cosmos → Universe
- [ ] Cancelar compra (dismiss sheet)
- [ ] Compra fallida (tarjeta rechazada)

#### Restore Purchases
- [ ] Restore con compra activa
- [ ] Restore sin compras previas
- [ ] Restore después de reinstalar app

#### Edge Cases
- [ ] No internet durante compra
- [ ] App crash durante compra
- [ ] Purchase already owned
- [ ] Subscription expired
- [ ] Trial period

#### UI/UX
- [ ] Loading states durante fetch de productos
- [ ] Loading states durante compra
- [ ] Error messages son user-friendly
- [ ] Success feedback claro
- [ ] Animaciones suaves
- [ ] Tier actual bien marcado

#### Analytics
- [ ] `premium_screen_viewed` se dispara
- [ ] `premium_tier_selected` con tier correcto
- [ ] `premium_purchase_started`
- [ ] `premium_purchase_success`
- [ ] `premium_purchase_error` con error details
- [ ] `premium_restore_initiated`

---

## 📊 ROLLOUT PLAN

### Fase 1: Internal Testing (Día 1-2)
- Devs prueban todos los flujos
- QA team valida en sandbox
- Fix bugs encontrados

### Fase 2: Beta Testing (Día 3-5)
- Deploy a TestFlight/Play Console Internal Testing
- 10-20 beta testers
- Monitorear Crashlytics
- Validar analytics

### Fase 3: Staged Rollout (Día 6-10)
- 10% de usuarios (Play Store)
- Monitorear métricas:
  - Crash rate
  - Purchase success rate
  - Restore success rate
- Incrementar a 50% si todo OK
- 100% después de 3 días sin issues

### Fase 4: Cleanup (Día 11-14)
- Remover código deprecado
- Actualizar documentación
- Post-mortem meeting

---

## 🚨 ROLLBACK PLAN

Si algo falla en producción:

### Rollback Rápido (5 minutos)

```dart
// lib/main.dart
GoRoute(
  path: '/premium',
  builder: (context, state) => const PremiumScreen(),  // Volver a antigua
),
```

```bash
# Build emergency release
flutter build appbundle --release
flutter build ipa --release

# Upload a stores
fastlane ios emergency_release
fastlane android emergency_release
```

### Rollback con Feature Flag (Mejor)

Implementar feature flag para toggle:
```dart
// lib/core/feature_flags.dart
class FeatureFlags {
  static bool get usePremiumScreenV2 =>
    RemoteConfig.instance.getBool('use_premium_v2') ?? false;
}

// lib/main.dart
GoRoute(
  path: '/premium',
  builder: (context, state) => FeatureFlags.usePremiumScreenV2
    ? const PremiumScreenV2()
    : const PremiumScreen(),
),
```

Así puedes desactivar V2 remotamente sin rebuild.

---

## 📈 MÉTRICAS A MONITOREAR

### Pre-Launch (Baseline)
```
Purchase success rate: X%
Average purchase time: X segundos
Restore success rate: X%
Crashes relacionados a premium: X/semana
```

### Post-Launch (Comparar)
```
Purchase success rate: ¿Mejor/peor?
Average purchase time: ¿Más rápido?
Restore success rate: ¿Mejor?
Crashes: ¿Menos?
```

### KPIs Críticos
- **Purchase Conversion:** % usuarios que completan compra
- **Error Rate:** % compras que fallan
- **Time to Purchase:** Tiempo desde ver screen hasta completar
- **Restore Success:** % restores exitosos

---

## ✅ CHECKLIST FINAL

### Pre-Launch
- [ ] PremiumScreenV2 conectada a PremiumControllerV2
- [ ] Todos los entry points actualizados
- [ ] Testing completo en sandbox (iOS + Android)
- [ ] Analytics validados en staging
- [ ] Error handling testeado
- [ ] Rollback plan documentado
- [ ] Feature flag implementado (opcional)

### Launch
- [ ] Deploy a beta testers primero
- [ ] Monitorear métricas 24-48h
- [ ] Staged rollout (10% → 50% → 100%)
- [ ] Post-mortem después de 1 semana

### Post-Launch
- [ ] Deprecar código antiguo
- [ ] Remover PremiumScreen después 2 semanas sin issues
- [ ] Actualizar documentación
- [ ] Celebrar 🎉

---

## 🎯 ESTIMACIÓN TOTAL

| Fase | Tiempo |
|------|--------|
| Fase 1: Conectar V2 | 2-3 horas |
| Fase 2: Migrar entry points | 1 hora |
| Fase 3: Cleanup | 30 min |
| Testing completo | 2-3 horas |
| **TOTAL** | **6-8 horas** |

**Recomendación:** Hacerlo en 1 día completo con testing exhaustivo.

---

## 📞 CONTACTOS

**Si algo sale mal:**
- Tech Lead: [nombre]
- Backend Team: [contacto] (si issues con RevenueCat)
- iOS/Android Specialists: [contactos]

---

**Generado:** 26 de Noviembre 2025
**Última Actualización:** [fecha]
**Estado:** 📝 Draft - Pendiente de implementación