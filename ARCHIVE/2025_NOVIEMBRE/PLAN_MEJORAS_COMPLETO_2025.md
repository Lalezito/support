# 🎯 PLAN MAESTRO DE MEJORAS - ZODIAC APP 2025
**Fecha de inicio:** 26 de Noviembre 2025
**Duración estimada:** 12 semanas (3 meses)
**Objetivo:** Resolver todos los problemas críticos, altos y medianos identificados

---

## 📊 RESUMEN EJECUTIVO

### Métricas de Éxito
- ✅ 0 API keys hardcodeadas en código
- ✅ 100% strings con internacionalización
- ✅ 0 archivos > 1000 líneas
- ✅ 70% cobertura de tests
- ✅ 0 print statements en producción
- ✅ 100% estado manejado con Riverpod
- ✅ Reducción 50% en tamaño del APK

### Recursos Necesarios
- 1-2 desarrolladores full-time
- 12 semanas de desarrollo
- CI/CD configurado
- Herramientas: Firebase, RevenueCat, Testing frameworks

---

## 🚨 SEMANA 0: EMERGENCIAS (26-29 Nov 2025)
**Objetivo:** Resolver problemas críticos de seguridad inmediatamente

### Día 1: Seguridad Crítica (4 horas)
```bash
# TAREA 1: Rotar API Keys de Firebase
1. Login a Firebase Console
2. Generar nuevas API keys
3. Revocar keys antiguas
4. Actualizar Firebase Security Rules

# TAREA 2: Implementar variables de entorno
1. Crear archivo .env.example:
   FIREBASE_API_KEY_ANDROID=your_key_here
   FIREBASE_API_KEY_IOS=your_key_here
   FIREBASE_APP_ID_ANDROID=your_id_here
   FIREBASE_APP_ID_IOS=your_id_here

2. Instalar flutter_dotenv:
   flutter pub add flutter_dotenv

3. Actualizar firebase_options.dart:
```

```dart
// lib/firebase_options.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return web;
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      default:
        throw UnsupportedError('Platform not supported');
    }
  }

  static FirebaseOptions android = FirebaseOptions(
    apiKey: dotenv.env['FIREBASE_API_KEY_ANDROID'] ?? '',
    appId: dotenv.env['FIREBASE_APP_ID_ANDROID'] ?? '',
    messagingSenderId: '764873916666',
    projectId: 'divine-5a02f',
    storageBucket: 'divine-5a02f.appspot.com',
  );

  static FirebaseOptions ios = FirebaseOptions(
    apiKey: dotenv.env['FIREBASE_API_KEY_IOS'] ?? '',
    appId: dotenv.env['FIREBASE_APP_ID_IOS'] ?? '',
    messagingSenderId: '764873916666',
    projectId: 'divine-5a02f',
    storageBucket: 'divine-5a02f.appspot.com',
    iosBundleId: 'astrology.horoscope.palmistry',
  );
}
```

```bash
# TAREA 3: Actualizar .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.production" >> .gitignore

# TAREA 4: Documentar proceso para el equipo
```

### Día 2: Limpieza Rápida (2 horas)
```bash
# TAREA 1: Eliminar todos los print statements
# Crear script de limpieza
cat > remove_prints.sh << 'EOF'
#!/bin/bash
find lib -name "*.dart" -type f -exec sed -i '' '/^\s*print(/d' {} \;
find lib -name "*.dart" -type f -exec sed -i '' '/^\s*debugPrint(/d' {} \;
echo "Print statements removed!"
EOF

chmod +x remove_prints.sh
./remove_prints.sh

# TAREA 2: Configurar Logger centralizado
```

```dart
// lib/core/app_logger.dart
import 'package:logger/logger.dart';
import 'package:flutter/foundation.dart';

class AppLogger {
  static final Logger _logger = Logger(
    printer: PrettyPrinter(
      methodCount: 0,
      errorMethodCount: 5,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      printTime: true,
    ),
    level: kDebugMode ? Level.debug : Level.warning,
  );

  static void debug(String message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) {
      _logger.d(message, error, stackTrace);
    }
  }

  static void info(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.i(message, error, stackTrace);
  }

  static void warning(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.w(message, error, stackTrace);
  }

  static void error(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.e(message, error, stackTrace);
  }
}
```

### Día 3: Configurar Linting Estricto (1 hora)
```yaml
# analysis_options.yaml
include: package:very_good_analysis/analysis_options.yaml

analyzer:
  strong-mode:
    implicit-casts: false
    implicit-dynamic: false
  errors:
    invalid_annotation_target: ignore
    missing_required_param: error
    missing_return: error
    avoid_print: error
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "test/**"

linter:
  rules:
    # Error Prevention
    - avoid_print
    - avoid_empty_else
    - avoid_returning_null_for_future
    - avoid_slow_async_io
    - cancel_subscriptions
    - close_sinks

    # Code Quality
    - prefer_const_constructors
    - prefer_const_declarations
    - prefer_final_fields
    - prefer_final_locals
    - unnecessary_const
    - unnecessary_new

    # Documentation
    - public_member_api_docs # Para APIs públicas

    # Performance
    - avoid_unnecessary_containers
    - prefer_const_constructors_in_immutables

    # Style
    - sort_constructors_first
    - sort_unnamed_constructors_first
```

```bash
# Ejecutar análisis y fixes automáticos
dart analyze lib/
dart fix --apply
```

---

## 📅 SPRINT 1: INTERNACIONALIZACIÓN (Semana 1-2)
**Objetivo:** Resolver todos los FIXME de i18n y strings hardcodeados

### Semana 1: Auditoría y Setup

#### Día 1-2: Auditoría completa de strings
```bash
# Script para encontrar todos los strings hardcodeados
cat > find_hardcoded_strings.sh << 'EOF'
#!/bin/bash
echo "=== Buscando strings hardcodeados ==="
grep -r "Text(['\"]" lib/ --include="*.dart" | grep -v "AppLocalizations" > hardcoded_strings.txt
grep -r "showSnackBar.*Text(['\"]" lib/ --include="*.dart" > snackbar_strings.txt
grep -r "showDialog.*Text(['\"]" lib/ --include="*.dart" > dialog_strings.txt
grep -r "FIXME.*l10n" lib/ --include="*.dart" > fixme_l10n.txt
echo "Resultados guardados en archivos .txt"
EOF

chmod +x find_hardcoded_strings.sh
./find_hardcoded_strings.sh
```

#### Día 3-4: Crear todas las keys de traducción necesarias
```json
// lib/l10n/app_en.arb
{
  "@@locale": "en",

  "// Premium Screen Error Messages": "",
  "error_ios_simulator_bug_title": "iOS 18.2 Simulator Bug Detected",
  "error_ios_simulator_bug_message": "StoreKit has known issues on iOS 18.2 simulator.\n\nPlease test on:\n• Physical iPhone device (recommended)\n• iOS 17.5 simulator",
  "error_connection_timeout_title": "Connection timeout",
  "error_connection_timeout_message": "This may be due to iOS 18.2 simulator issues. Please check your connection or try again on a real device.",
  "error_purchase_cancelled": "Purchase cancelled",
  "error_purchase_failed": "Purchase failed. Please try again.",
  "error_generic": "An unexpected error occurred",

  "// Premium Success Messages": "",
  "premium_success_title": "Success!",
  "premium_welcome_message": "Welcome to {tierName} tier!\n\nYou now have access to all premium features.",
  "@premium_welcome_message": {
    "placeholders": {
      "tierName": {
        "type": "String",
        "example": "Universe"
      }
    }
  },
  "premium_get_started": "Get Started",

  "// Plan Change Service Messages": "",
  "error_upgrade_process": "Error processing upgrade. Please try again.",
  "welcome_back_plan": "Welcome back! Your {planName} plan is active.",
  "@welcome_back_plan": {
    "placeholders": {
      "planName": {
        "type": "String",
        "example": "Universe"
      }
    }
  },
  "error_reactivate_subscription": "Error reactivating subscription",
  "subscription_access_until_end": "You'll maintain access until the end of the paid period.",
  "error_cancel_subscription": "Error cancelling subscription",
  "error_change_plan": "Error changing plan",
  "error_apply_offer": "Error applying offer"
}
```

```json
// lib/l10n/app_es.arb
{
  "@@locale": "es",

  "// Premium Screen Error Messages": "",
  "error_ios_simulator_bug_title": "Error del Simulador iOS 18.2 Detectado",
  "error_ios_simulator_bug_message": "StoreKit tiene problemas conocidos en el simulador iOS 18.2.\n\nPor favor prueba en:\n• Dispositivo iPhone físico (recomendado)\n• Simulador iOS 17.5",
  "error_connection_timeout_title": "Tiempo de conexión agotado",
  "error_connection_timeout_message": "Esto puede deberse a problemas del simulador iOS 18.2. Verifica tu conexión o intenta en un dispositivo real.",
  "error_purchase_cancelled": "Compra cancelada",
  "error_purchase_failed": "La compra falló. Por favor intenta nuevamente.",
  "error_generic": "Ocurrió un error inesperado",

  "// Premium Success Messages": "",
  "premium_success_title": "¡Éxito!",
  "premium_welcome_message": "¡Bienvenido al plan {tierName}!\n\nAhora tienes acceso a todas las funciones premium.",
  "premium_get_started": "Comenzar",

  "// Plan Change Service Messages": "",
  "error_upgrade_process": "Error al procesar el upgrade. Intenta nuevamente.",
  "welcome_back_plan": "¡Bienvenido de vuelta! Tu plan {planName} está activo.",
  "error_reactivate_subscription": "Error al reactivar la suscripción",
  "subscription_access_until_end": "Mantendrás acceso hasta el final del período pagado.",
  "error_cancel_subscription": "Error al cancelar la suscripción",
  "error_change_plan": "Error al cambiar el plan",
  "error_apply_offer": "Error al aplicar la oferta"
}
```

#### Día 5: Actualizar código con las nuevas keys
```dart
// lib/screens/premium_screen.dart - ANTES línea 366
// FIXME: All error messages below need l10n keys
String _getUserFriendlyError(String error) {
  if (error.contains('iOS 18.2')) {
    return 'iOS 18.2 Simulator Bug Detected\n\n'...  // HARDCODED
  }
}

// DESPUÉS
String _getUserFriendlyError(BuildContext context, String error) {
  final l10n = AppLocalizations.of(context)!;

  if (error.contains('iOS 18.2')) {
    return '${l10n.error_ios_simulator_bug_title}\n\n${l10n.error_ios_simulator_bug_message}';
  } else if (error.contains('timeout')) {
    return '${l10n.error_connection_timeout_title}\n\n${l10n.error_connection_timeout_message}';
  } else if (error.contains('cancelled')) {
    return l10n.error_purchase_cancelled;
  } else if (error.contains('failed')) {
    return l10n.error_purchase_failed;
  }
  return l10n.error_generic;
}

// Actualizar llamadas
Text(l10n.premium_success_title),  // Línea 400
Text(l10n.premium_welcome_message(tier.displayName)),  // Línea 404
child: Text(l10n.premium_get_started),  // Línea 410
```

```dart
// lib/services/plan_change_service.dart
class PlanChangeService {
  Future<void> processPlanChange(BuildContext context, ...) async {
    final l10n = AppLocalizations.of(context)!;

    try {
      // ... código existente ...
    } catch (e) {
      _showSnackBar(
        context: context,
        message: l10n.error_upgrade_process,  // ANTES: 'Error al procesar...'
        isError: true,
      );
    }
  }

  void _showWelcomeMessage(BuildContext context, String tierName) {
    final l10n = AppLocalizations.of(context)!;
    _showSnackBar(
      context: context,
      message: l10n.welcome_back_plan(tierName),  // ANTES: '¡Bienvenido de vuelta!...'
      isError: false,
    );
  }
}
```

### Semana 2: Completar i18n y Testing

#### Día 1-2: Script de validación automática
```dart
// test/l10n_validation_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'dart:convert';

void main() {
  group('L10n Validation', () {
    test('All keys exist in all languages', () async {
      // Cargar archivos ARB
      final enContent = await rootBundle.loadString('lib/l10n/app_en.arb');
      final esContent = await rootBundle.loadString('lib/l10n/app_es.arb');

      final enJson = json.decode(enContent) as Map<String, dynamic>;
      final esJson = json.decode(esContent) as Map<String, dynamic>;

      // Obtener keys (ignorar las que empiezan con @)
      final enKeys = enJson.keys.where((k) => !k.startsWith('@')).toSet();
      final esKeys = esJson.keys.where((k) => !k.startsWith('@')).toSet();

      // Verificar que todas las keys existen en ambos idiomas
      final missingInEs = enKeys.difference(esKeys);
      final missingInEn = esKeys.difference(enKeys);

      expect(missingInEs, isEmpty, reason: 'Keys missing in Spanish: $missingInEs');
      expect(missingInEn, isEmpty, reason: 'Keys missing in English: $missingInEn');
    });

    test('No hardcoded strings in widgets', () async {
      // Script para buscar Text() con strings directos
      final result = await Process.run('grep', [
        '-r',
        'Text\\s*\\([\'"]',
        'lib/',
        '--include=*.dart',
      ]);

      final lines = result.stdout.toString().split('\n')
        .where((line) => !line.contains('AppLocalizations'))
        .where((line) => !line.contains('// ignore:'))
        .toList();

      expect(lines, isEmpty,
        reason: 'Found hardcoded strings:\n${lines.join('\n')}');
    });
  });
}
```

#### Día 3-5: Migrar TODOS los strings restantes
```bash
# Proceso sistemático por carpeta
for dir in screens widgets services features; do
  echo "=== Procesando $dir ==="
  find lib/$dir -name "*.dart" -type f | while read file; do
    echo "Checking $file"
    grep -n "Text(['\"]" "$file" | grep -v "AppLocalizations" || true
  done
done
```

---

## 📅 SPRINT 2: REFACTORIZACIÓN ARQUITECTÓNICA (Semana 3-4)
**Objetivo:** Dividir archivos gigantes, consolidar duplicados

### Semana 3: Refactorizar CompatibilityScreen

#### Día 1: Análisis y plan de división
```markdown
# Plan de División - CompatibilityScreen (5,062 líneas)

## Nuevos archivos a crear:
1. compatibility_animations_manager.dart (400 líneas)
2. compatibility_sign_selector.dart (200 líneas)
3. compatibility_result_card.dart (300 líneas)
4. compatibility_details_panel.dart (400 líneas)
5. compatibility_chart_widgets.dart (350 líneas)
6. compatibility_premium_features.dart (300 líneas)
7. compatibility_screen.dart (principal, <400 líneas)
```

#### Día 2-3: Crear AnimationsManager
```dart
// lib/features/compatibility/animations/compatibility_animations_manager.dart
import 'package:flutter/material.dart';

class CompatibilityAnimationsManager {
  final TickerProvider vsync;

  late final AnimationController heartController;
  late final AnimationController signController;
  late final AnimationController selectionController;
  late final AnimationController rotationController;
  late final AnimationController pulseController;
  late final AnimationController backgroundController;
  late final AnimationController starFieldController;

  final List<AnimationController> _allControllers = [];

  CompatibilityAnimationsManager({required this.vsync}) {
    _initializeControllers();
  }

  void _initializeControllers() {
    heartController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: vsync,
    )..repeat(reverse: true);
    _allControllers.add(heartController);

    signController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: vsync,
    );
    _allControllers.add(signController);

    selectionController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: vsync,
    );
    _allControllers.add(selectionController);

    rotationController = AnimationController(
      duration: const Duration(seconds: 20),
      vsync: vsync,
    )..repeat();
    _allControllers.add(rotationController);

    pulseController = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: vsync,
    )..repeat(reverse: true);
    _allControllers.add(pulseController);

    backgroundController = AnimationController(
      duration: const Duration(seconds: 15),
      vsync: vsync,
    )..repeat(reverse: true);
    _allControllers.add(backgroundController);

    starFieldController = AnimationController(
      duration: const Duration(seconds: 30),
      vsync: vsync,
    )..repeat();
    _allControllers.add(starFieldController);
  }

  Animation<double> get heartAnimation => CurvedAnimation(
    parent: heartController,
    curve: Curves.easeInOut,
  );

  Animation<double> get rotationAnimation => Tween<double>(
    begin: 0,
    end: 2 * 3.14159,
  ).animate(rotationController);

  Animation<double> get pulseAnimation => Tween<double>(
    begin: 0.95,
    end: 1.05,
  ).animate(CurvedAnimation(
    parent: pulseController,
    curve: Curves.easeInOut,
  ));

  void dispose() {
    for (final controller in _allControllers) {
      controller.dispose();
    }
  }

  void pauseAll() {
    for (final controller in _allControllers) {
      if (controller.isAnimating) {
        controller.stop();
      }
    }
  }

  void resumeAll() {
    heartController.repeat(reverse: true);
    rotationController.repeat();
    pulseController.repeat(reverse: true);
    backgroundController.repeat(reverse: true);
    starFieldController.repeat();
  }
}
```

#### Día 4: Crear SignSelector widget
```dart
// lib/features/compatibility/widgets/compatibility_sign_selector.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class CompatibilitySignSelector extends ConsumerWidget {
  final Function(String) onSignSelected;
  final String? selectedSign;
  final bool isFirstSign;

  const CompatibilitySignSelector({
    Key? key,
    required this.onSignSelected,
    this.selectedSign,
    this.isFirstSign = true,
  }) : super(key: key);

  static const List<Map<String, dynamic>> zodiacSigns = [
    {'name': 'Aries', 'symbol': '♈', 'element': 'Fire'},
    {'name': 'Taurus', 'symbol': '♉', 'element': 'Earth'},
    {'name': 'Gemini', 'symbol': '♊', 'element': 'Air'},
    {'name': 'Cancer', 'symbol': '♋', 'element': 'Water'},
    {'name': 'Leo', 'symbol': '♌', 'element': 'Fire'},
    {'name': 'Virgo', 'symbol': '♍', 'element': 'Earth'},
    {'name': 'Libra', 'symbol': '♎', 'element': 'Air'},
    {'name': 'Scorpio', 'symbol': '♏', 'element': 'Water'},
    {'name': 'Sagittarius', 'symbol': '♐', 'element': 'Fire'},
    {'name': 'Capricorn', 'symbol': '♑', 'element': 'Earth'},
    {'name': 'Aquarius', 'symbol': '♒', 'element': 'Air'},
    {'name': 'Pisces', 'symbol': '♓', 'element': 'Water'},
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;

    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            isFirstSign ? l10n.select_your_sign : l10n.select_partner_sign,
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: zodiacSigns.map((sign) {
              final isSelected = selectedSign == sign['name'];
              return _SignCard(
                sign: sign,
                isSelected: isSelected,
                onTap: () => onSignSelected(sign['name']),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}

class _SignCard extends StatelessWidget {
  final Map<String, dynamic> sign;
  final bool isSelected;
  final VoidCallback onTap;

  const _SignCard({
    required this.sign,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        width: 80,
        height: 100,
        decoration: BoxDecoration(
          color: isSelected
            ? Theme.of(context).primaryColor
            : Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected
              ? Theme.of(context).primaryColor
              : Colors.grey.withOpacity(0.3),
            width: 2,
          ),
          boxShadow: isSelected ? [
            BoxShadow(
              color: Theme.of(context).primaryColor.withOpacity(0.4),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ] : [],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              sign['symbol'],
              style: TextStyle(
                fontSize: 32,
                color: isSelected ? Colors.white : null,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              sign['name'],
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: isSelected ? Colors.white : null,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

#### Día 5: Refactorizar CompatibilityScreen principal
```dart
// lib/screens/compatibility_screen.dart (REFACTORIZADO)
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../features/compatibility/animations/compatibility_animations_manager.dart';
import '../features/compatibility/widgets/compatibility_sign_selector.dart';
import '../features/compatibility/widgets/compatibility_result_card.dart';
import '../features/compatibility/widgets/compatibility_details_panel.dart';

class CompatibilityScreen extends ConsumerStatefulWidget {
  const CompatibilityScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<CompatibilityScreen> createState() => _CompatibilityScreenState();
}

class _CompatibilityScreenState extends ConsumerState<CompatibilityScreen>
    with TickerProviderStateMixin {

  late final CompatibilityAnimationsManager _animationsManager;
  String? _firstSign;
  String? _secondSign;
  bool _showResult = false;

  @override
  void initState() {
    super.initState();
    _animationsManager = CompatibilityAnimationsManager(vsync: this);
  }

  @override
  void dispose() {
    _animationsManager.dispose();
    super.dispose();
  }

  void _calculateCompatibility() {
    if (_firstSign != null && _secondSign != null) {
      setState(() {
        _showResult = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.compatibility_title),
      ),
      body: AnimatedBuilder(
        animation: Listenable.merge([
          _animationsManager.heartAnimation,
          _animationsManager.pulseAnimation,
        ]),
        builder: (context, child) {
          return Container(
            decoration: _buildAnimatedBackground(),
            child: _showResult
                ? CompatibilityResultCard(
                    firstSign: _firstSign!,
                    secondSign: _secondSign!,
                    animationsManager: _animationsManager,
                    onReset: () {
                      setState(() {
                        _showResult = false;
                        _firstSign = null;
                        _secondSign = null;
                      });
                    },
                  )
                : Column(
                    children: [
                      Expanded(
                        child: CompatibilitySignSelector(
                          selectedSign: _firstSign,
                          isFirstSign: true,
                          onSignSelected: (sign) {
                            setState(() {
                              _firstSign = sign;
                            });
                          },
                        ),
                      ),
                      if (_firstSign != null) ...[
                        const Divider(),
                        Expanded(
                          child: CompatibilitySignSelector(
                            selectedSign: _secondSign,
                            isFirstSign: false,
                            onSignSelected: (sign) {
                              setState(() {
                                _secondSign = sign;
                              });
                              _calculateCompatibility();
                            },
                          ),
                        ),
                      ],
                    ],
                  ),
          );
        },
      ),
    );
  }

  BoxDecoration _buildAnimatedBackground() {
    return BoxDecoration(
      gradient: LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          Theme.of(context).primaryColor.withOpacity(0.1),
          Theme.of(context).primaryColor.withOpacity(0.05),
        ],
        transform: GradientRotation(_animationsManager.rotationAnimation.value),
      ),
    );
  }
}
```

### Semana 4: Consolidar Premium Screens

#### Día 1-2: Análisis de diferencias
```bash
# Script para comparar las 3 versiones
diff -u lib/screens/premium_screen.dart lib/screens/premium_screen_v2.dart > premium_diff_v2.txt
diff -u lib/screens/premium_screen.dart lib/screens/legacy/premium_screen_legacy.dart > premium_diff_legacy.txt

# Identificar funcionalidades únicas en cada versión
grep -E "^(class |  [a-zA-Z]+ [a-zA-Z]+\()" lib/screens/premium_screen*.dart > functions_comparison.txt
```

#### Día 3-5: Consolidar en una sola versión
```dart
// lib/screens/premium_screen.dart (VERSIÓN CONSOLIDADA)
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../features/premium/widgets/premium_tier_selector.dart';
import '../features/premium/widgets/premium_benefits_list.dart';
import '../features/premium/widgets/premium_pricing_card.dart';
import '../features/premium/providers/premium_state_provider.dart';

class PremiumScreen extends ConsumerWidget {
  const PremiumScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final premiumState = ref.watch(premiumStateProvider);
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.premium_title),
      ),
      body: premiumState.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => PremiumErrorWidget(
          error: error.toString(),
          onRetry: () => ref.refresh(premiumStateProvider),
        ),
        data: (data) => CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: PremiumTierSelector(
                selectedTier: data.selectedTier,
                onTierSelected: (tier) {
                  ref.read(premiumStateProvider.notifier).selectTier(tier);
                },
              ),
            ),
            SliverToBoxAdapter(
              child: PremiumBenefitsList(
                tier: data.selectedTier,
              ),
            ),
            SliverToBoxAdapter(
              child: PremiumPricingCard(
                tier: data.selectedTier,
                onPurchase: () async {
                  await ref.read(premiumStateProvider.notifier).purchase();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

```bash
# Eliminar versiones antiguas
git rm lib/screens/premium_screen_v2.dart
git rm lib/screens/legacy/premium_screen_legacy.dart
git commit -m "refactor: consolidate premium screens into single version"
```

---

## 📅 SPRINT 3: GESTIÓN DE ESTADO (Semana 5-6)
**Objetivo:** Migrar todo a Riverpod, eliminar setState

### Semana 5: Setup Riverpod y Migración Base

#### Día 1: Crear providers centralizados
```dart
// lib/providers/app_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import '../services/preferences_service.dart';
import '../services/horoscope_service.dart';
import '../services/subscription_service.dart';
import '../services/plan_change_service.dart';

// Singleton Services Providers
final dioProvider = Provider<Dio>((ref) {
  final dio = Dio();
  dio.interceptors.add(LogInterceptor());
  return dio;
});

final preferencesServiceProvider = Provider<PreferencesService>((ref) {
  return PreferencesService();
});

final horoscopeServiceProvider = Provider<HoroscopeService>((ref) {
  final dio = ref.watch(dioProvider);
  return HoroscopeService(dio);
});

final subscriptionServiceProvider = Provider<SubscriptionService>((ref) {
  return SubscriptionService();
});

final planChangeServiceProvider = Provider<PlanChangeService>((ref) {
  final subscriptionService = ref.watch(subscriptionServiceProvider);
  return PlanChangeService(subscriptionService);
});

// State Providers
final currentUserSignProvider = StateProvider<String?>((ref) => null);

final selectedDateProvider = StateProvider<DateTime>((ref) => DateTime.now());

final isPremiumUserProvider = StreamProvider<bool>((ref) async* {
  final service = ref.watch(subscriptionServiceProvider);
  yield* service.isPremiumStream();
});

// Computed Providers
final dailyHoroscopeProvider = FutureProvider.family<HoroscopeData, String>(
  (ref, sign) async {
    final service = ref.watch(horoscopeServiceProvider);
    final date = ref.watch(selectedDateProvider);
    return service.getDailyHoroscope(sign, date);
  },
);
```

#### Día 2-3: Migrar primer widget de setState a Riverpod
```dart
// ANTES: lib/widgets/cosmic_audio_player.dart (con setState)
class CosmicAudioPlayer extends StatefulWidget {
  // ...
}

class _CosmicAudioPlayerState extends State<CosmicAudioPlayer> {
  bool _isPlaying = false;
  double _volume = 0.5;

  void _togglePlayPause() {
    setState(() {
      _isPlaying = !_isPlaying;
    });
  }

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(_isPlaying ? Icons.pause : Icons.play_arrow),
      onPressed: _togglePlayPause,
    );
  }
}

// DESPUÉS: lib/widgets/cosmic_audio_player.dart (con Riverpod)
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider para el estado del audio
final audioPlayerStateProvider = StateNotifierProvider.autoDispose<AudioPlayerNotifier, AudioPlayerState>((ref) {
  return AudioPlayerNotifier();
});

class AudioPlayerState {
  final bool isPlaying;
  final double volume;
  final Duration position;
  final Duration duration;

  AudioPlayerState({
    this.isPlaying = false,
    this.volume = 0.5,
    this.position = Duration.zero,
    this.duration = Duration.zero,
  });

  AudioPlayerState copyWith({
    bool? isPlaying,
    double? volume,
    Duration? position,
    Duration? duration,
  }) {
    return AudioPlayerState(
      isPlaying: isPlaying ?? this.isPlaying,
      volume: volume ?? this.volume,
      position: position ?? this.position,
      duration: duration ?? this.duration,
    );
  }
}

class AudioPlayerNotifier extends StateNotifier<AudioPlayerState> {
  AudioPlayerNotifier() : super(AudioPlayerState());

  void togglePlayPause() {
    state = state.copyWith(isPlaying: !state.isPlaying);
  }

  void setVolume(double volume) {
    state = state.copyWith(volume: volume);
  }

  void updatePosition(Duration position) {
    state = state.copyWith(position: position);
  }
}

// Widget refactorizado
class CosmicAudioPlayer extends ConsumerWidget {
  const CosmicAudioPlayer({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final audioState = ref.watch(audioPlayerStateProvider);

    return Row(
      children: [
        IconButton(
          icon: Icon(audioState.isPlaying ? Icons.pause : Icons.play_arrow),
          onPressed: () {
            ref.read(audioPlayerStateProvider.notifier).togglePlayPause();
          },
        ),
        Expanded(
          child: Slider(
            value: audioState.volume,
            onChanged: (value) {
              ref.read(audioPlayerStateProvider.notifier).setVolume(value);
            },
          ),
        ),
      ],
    );
  }
}
```

#### Día 4-5: Script de migración automatizada
```bash
# Script para identificar todos los widgets con setState
cat > find_stateful_widgets.sh << 'EOF'
#!/bin/bash
echo "=== Widgets con setState para migrar ==="
grep -r "setState(" lib/ --include="*.dart" | cut -d: -f1 | sort -u > stateful_widgets.txt
echo "Total: $(wc -l < stateful_widgets.txt) archivos"
echo ""
echo "Top 10 archivos con más setState:"
grep -r "setState(" lib/ --include="*.dart" | cut -d: -f1 | uniq -c | sort -rn | head -10
EOF

chmod +x find_stateful_widgets.sh
./find_stateful_widgets.sh
```

### Semana 6: Completar migración

#### Día 1-5: Migración sistemática
```markdown
# Checklist de Migración setState → Riverpod

## Alta Prioridad (Pantallas principales)
- [ ] compatibility_screen.dart (20 setState) → ConsumerStatefulWidget
- [ ] premium_screen.dart (15 setState) → ConsumerWidget
- [ ] settings_screen.dart (12 setState) → ConsumerWidget
- [ ] birth_date_screen.dart (10 setState) → ConsumerWidget
- [ ] cosmic_coach_screen.dart (8 setState) → ConsumerWidget

## Media Prioridad (Widgets complejos)
- [ ] chat_history_widget.dart (5 setState) → ConsumerWidget
- [ ] horoscope_share_card.dart (4 setState) → ConsumerWidget
- [ ] conversion_optimized_paywall.dart (3 setState) → ConsumerWidget

## Baja Prioridad (Widgets simples)
- [ ] Resto de widgets con 1-2 setState
```

---

## 📅 SPRINT 4: TESTING (Semana 7-8)
**Objetivo:** Alcanzar 70% cobertura de tests

### Semana 7: Unit Tests para Servicios

#### Día 1: Setup testing environment
```yaml
# pubspec.yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
  fake_async: ^1.3.1
  http_mock_adapter: ^0.4.0
```

#### Día 2-3: Tests para PlanChangeService
```dart
// test/services/plan_change_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:zodiac_app/services/plan_change_service.dart';
import 'package:zodiac_app/services/subscription_service.dart';

class MockSubscriptionService extends Mock implements SubscriptionService {}

void main() {
  late PlanChangeService planChangeService;
  late MockSubscriptionService mockSubscriptionService;

  setUp(() {
    mockSubscriptionService = MockSubscriptionService();
    planChangeService = PlanChangeService(mockSubscriptionService);
  });

  group('PlanChangeService', () {
    group('processPlanChange', () {
      test('should successfully upgrade from free to premium', () async {
        // Arrange
        when(() => mockSubscriptionService.getCurrentTier())
          .thenReturn(PremiumTier.free);
        when(() => mockSubscriptionService.purchaseTier(PremiumTier.universe))
          .thenAnswer((_) async => true);

        // Act
        final result = await planChangeService.processPlanChange(
          currentTier: PremiumTier.free,
          targetTier: PremiumTier.universe,
        );

        // Assert
        expect(result.success, true);
        expect(result.message, contains('Welcome'));
        verify(() => mockSubscriptionService.purchaseTier(PremiumTier.universe))
          .called(1);
      });

      test('should handle purchase failure', () async {
        // Arrange
        when(() => mockSubscriptionService.getCurrentTier())
          .thenReturn(PremiumTier.free);
        when(() => mockSubscriptionService.purchaseTier(any()))
          .thenThrow(Exception('Purchase failed'));

        // Act
        final result = await planChangeService.processPlanChange(
          currentTier: PremiumTier.free,
          targetTier: PremiumTier.universe,
        );

        // Assert
        expect(result.success, false);
        expect(result.message, contains('Error'));
      });

      test('should handle downgrade with grace period', () async {
        // Arrange
        when(() => mockSubscriptionService.getCurrentTier())
          .thenReturn(PremiumTier.universe);
        when(() => mockSubscriptionService.cancelSubscription())
          .thenAnswer((_) async => true);
        when(() => mockSubscriptionService.getGracePeriodEnd())
          .thenReturn(DateTime.now().add(Duration(days: 7)));

        // Act
        final result = await planChangeService.processPlanChange(
          currentTier: PremiumTier.universe,
          targetTier: PremiumTier.free,
        );

        // Assert
        expect(result.success, true);
        expect(result.message, contains('access until'));
        verify(() => mockSubscriptionService.cancelSubscription()).called(1);
      });
    });

    group('validatePlanChange', () {
      test('should prevent same tier change', () {
        final result = planChangeService.validatePlanChange(
          currentTier: PremiumTier.universe,
          targetTier: PremiumTier.universe,
        );

        expect(result.isValid, false);
        expect(result.reason, contains('already on this plan'));
      });

      test('should allow valid upgrade', () {
        final result = planChangeService.validatePlanChange(
          currentTier: PremiumTier.free,
          targetTier: PremiumTier.galaxy,
        );

        expect(result.isValid, true);
        expect(result.reason, isNull);
      });
    });
  });
}
```

#### Día 4-5: Tests para HoroscopeService
```dart
// test/services/horoscope_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';

void main() {
  late Dio dio;
  late DioAdapter dioAdapter;
  late HoroscopeService horoscopeService;

  setUp(() {
    dio = Dio();
    dioAdapter = DioAdapter(dio: dio);
    horoscopeService = HoroscopeService(dio);
  });

  group('HoroscopeService', () {
    test('should fetch daily horoscope successfully', () async {
      // Arrange
      const sign = 'aries';
      final mockResponse = {
        'date': '2025-11-26',
        'sign': 'aries',
        'horoscope': 'Today is a great day for new beginnings...',
        'compatibility': 'leo',
        'lucky_number': 7,
        'lucky_color': 'red',
      };

      dioAdapter.onGet(
        '/horoscope/$sign',
        (server) => server.reply(200, mockResponse),
      );

      // Act
      final result = await horoscopeService.getDailyHoroscope(sign);

      // Assert
      expect(result.sign, equals('aries'));
      expect(result.horoscope, contains('new beginnings'));
      expect(result.luckyNumber, equals(7));
    });

    test('should handle network error gracefully', () async {
      // Arrange
      dioAdapter.onGet(
        '/horoscope/aries',
        (server) => server.throws(
          404,
          DioException(
            requestOptions: RequestOptions(path: '/horoscope/aries'),
            type: DioExceptionType.badResponse,
          ),
        ),
      );

      // Act & Assert
      expect(
        () => horoscopeService.getDailyHoroscope('aries'),
        throwsA(isA<HoroscopeServiceException>()),
      );
    });
  });
}
```

### Semana 8: Widget Tests e Integration Tests

#### Día 1-2: Widget tests para PremiumScreen
```dart
// test/screens/premium_screen_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mocktail/mocktail.dart';

void main() {
  group('PremiumScreen Widget Tests', () {
    testWidgets('should display tier selector', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: PremiumScreen(),
          ),
        ),
      );

      expect(find.text('Galaxy'), findsOneWidget);
      expect(find.text('Universe'), findsOneWidget);
      expect(find.text('Cosmos'), findsOneWidget);
    });

    testWidgets('should show benefits when tier selected', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: PremiumScreen(),
          ),
        ),
      );

      // Tap on Galaxy tier
      await tester.tap(find.text('Galaxy'));
      await tester.pumpAndSettle();

      // Verify benefits are shown
      expect(find.text('Daily Horoscopes'), findsOneWidget);
      expect(find.text('Compatibility Reports'), findsOneWidget);
    });

    testWidgets('should handle purchase button tap', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            // Mock the purchase provider
          ],
          child: MaterialApp(
            home: PremiumScreen(),
          ),
        ),
      );

      await tester.tap(find.text('Subscribe Now'));
      await tester.pumpAndSettle();

      // Verify loading indicator or success message
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });
}
```

#### Día 3-5: Integration tests
```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:zodiac_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('End-to-End Tests', () {
    testWidgets('Complete onboarding flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Step 1: Select birth date
      expect(find.text('Select Your Birth Date'), findsOneWidget);
      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Step 2: Select time
      expect(find.text('Select Birth Time'), findsOneWidget);
      await tester.tap(find.text('Skip'));
      await tester.pumpAndSettle();

      // Step 3: Home screen
      expect(find.text('Your Daily Horoscope'), findsOneWidget);
    });

    testWidgets('Premium purchase flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Navigate to premium
      await tester.tap(find.byIcon(Icons.star));
      await tester.pumpAndSettle();

      // Select tier
      await tester.tap(find.text('Universe'));
      await tester.pumpAndSettle();

      // Attempt purchase
      await tester.tap(find.text('Subscribe Now'));
      await tester.pumpAndSettle();

      // Verify purchase dialog or success
      expect(find.textContaining('Confirm'), findsOneWidget);
    });
  });
}
```

---

## 📅 SPRINT 5: OPTIMIZACIÓN Y LIMPIEZA (Semana 9-10)
**Objetivo:** Optimizar performance, limpiar código muerto

### Semana 9: Performance Optimization

#### Día 1-2: Análisis de performance
```dart
// lib/core/performance_monitor.dart
import 'package:flutter/foundation.dart';

class PerformanceMonitor {
  static final _widgetBuildTimes = <String, List<int>>{};

  static void trackWidgetBuild(String widgetName, VoidCallback build) {
    if (!kDebugMode) {
      build();
      return;
    }

    final stopwatch = Stopwatch()..start();
    build();
    stopwatch.stop();

    _widgetBuildTimes.putIfAbsent(widgetName, () => [])
      .add(stopwatch.elapsedMicroseconds);

    if (_widgetBuildTimes[widgetName]!.length % 100 == 0) {
      _printStats(widgetName);
    }
  }

  static void _printStats(String widgetName) {
    final times = _widgetBuildTimes[widgetName]!;
    final average = times.reduce((a, b) => a + b) / times.length;
    final max = times.reduce((a, b) => a > b ? a : b);

    AppLogger.debug('''
    Widget: $widgetName
    Average build time: ${average.toStringAsFixed(2)}μs
    Max build time: ${max}μs
    Total builds: ${times.length}
    ''');
  }
}
```

#### Día 3: Optimizar imágenes
```bash
# Script para optimizar imágenes
cat > optimize_images.sh << 'EOF'
#!/bin/bash
echo "=== Optimizando imágenes ==="

# Instalar herramientas si no existen
if ! command -v optipng &> /dev/null; then
    echo "Instalando optipng..."
    brew install optipng
fi

if ! command -v jpegoptim &> /dev/null; then
    echo "Instalando jpegoptim..."
    brew install jpegoptim
fi

# Optimizar PNGs
find assets/images -name "*.png" -exec optipng -o7 {} \;

# Optimizar JPEGs
find assets/images -name "*.jpg" -o -name "*.jpeg" -exec jpegoptim --strip-all {} \;

echo "✅ Imágenes optimizadas"
EOF

chmod +x optimize_images.sh
./optimize_images.sh
```

#### Día 4-5: Implementar lazy loading
```dart
// lib/widgets/lazy_indexed_stack.dart
import 'package:flutter/material.dart';

class LazyIndexedStack extends StatefulWidget {
  final int index;
  final List<Widget Function()> builders;

  const LazyIndexedStack({
    Key? key,
    required this.index,
    required this.builders,
  }) : super(key: key);

  @override
  State<LazyIndexedStack> createState() => _LazyIndexedStackState();
}

class _LazyIndexedStackState extends State<LazyIndexedStack> {
  final _loadedIndices = <int>{};
  final _children = <int, Widget>{};

  @override
  void initState() {
    super.initState();
    _loadChild(widget.index);
  }

  @override
  void didUpdateWidget(LazyIndexedStack oldWidget) {
    super.didUpdateWidget(oldWidget);
    _loadChild(widget.index);
  }

  void _loadChild(int index) {
    if (!_loadedIndices.contains(index)) {
      _loadedIndices.add(index);
      _children[index] = widget.builders[index]();
    }
  }

  @override
  Widget build(BuildContext context) {
    return IndexedStack(
      index: widget.index,
      children: List.generate(
        widget.builders.length,
        (i) => _children[i] ?? const SizedBox.shrink(),
      ),
    );
  }
}
```

### Semana 10: Code Cleanup

#### Día 1: Eliminar código muerto
```bash
# Script para encontrar código no utilizado
cat > find_unused_code.sh << 'EOF'
#!/bin/bash
echo "=== Buscando código no utilizado ==="

# Buscar archivos Dart no importados
for file in $(find lib -name "*.dart" -type f); do
    filename=$(basename "$file")
    if ! grep -r "import.*$filename" lib/ --include="*.dart" > /dev/null; then
        echo "Posiblemente no utilizado: $file"
    fi
done

# Buscar funciones privadas no utilizadas
echo ""
echo "=== Funciones privadas potencialmente no utilizadas ==="
grep -r "^[[:space:]]*_[a-zA-Z].*(" lib/ --include="*.dart" | while read line; do
    func_name=$(echo "$line" | sed -n 's/.*\(_[a-zA-Z0-9_]*\).*/\1/p')
    file=$(echo "$line" | cut -d: -f1)
    count=$(grep -c "$func_name" "$file")
    if [ "$count" -eq 1 ]; then
        echo "$line"
    fi
done
EOF

chmod +x find_unused_code.sh
./find_unused_code.sh > unused_code_report.txt
```

#### Día 2-3: Eliminar duplicación
```bash
# Consolidar archivos premium duplicados
rm -rf lib/features/premium/screens/goal_planner/  # Duplicado
rm lib/screens/legacy/premium_screen_legacy.dart   # Legacy
rm lib/screens/premium_screen_v2.dart              # V2

# Consolidar servicios AI
# Mover todo a una estructura clara
mkdir -p lib/services/ai
mv lib/services/ai_insights/* lib/services/ai/
mv lib/services/consolidated_ai/* lib/services/ai/
mv lib/services/advanced_contextual_ai.dart lib/services/ai/
rmdir lib/services/ai_insights
rmdir lib/services/consolidated_ai
```

#### Día 4-5: Documentación final
```markdown
# lib/README.md

## Arquitectura del Proyecto

### Estructura de Carpetas
```
lib/
├── core/           # Utilidades y configuración core
├── features/       # Features modulares (por dominio)
│   ├── compatibility/
│   ├── horoscope/
│   └── premium/
├── l10n/          # Internacionalización
├── models/        # Modelos de datos
├── providers/     # Riverpod providers
├── screens/       # Pantallas principales
├── services/      # Servicios y lógica de negocio
├── themes/        # Temas y estilos
└── widgets/       # Widgets reutilizables
```

### Patrones Utilizados
- **State Management:** Riverpod
- **Dependency Injection:** Provider pattern
- **Architecture:** Feature-first organization
- **Testing:** Unit + Widget + Integration tests

### Convenciones de Código
- Max 400 líneas por archivo
- Widgets stateless cuando sea posible
- Usar ConsumerWidget con Riverpod
- Documentar APIs públicas con ///
- Tests para toda lógica de negocio
```

---

## 📅 SPRINT 6: CI/CD Y MONITOREO (Semana 11-12)
**Objetivo:** Automatizar quality checks, setup monitoreo

### Semana 11: CI/CD Setup

#### Día 1-2: GitHub Actions
```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'

      - name: Install dependencies
        run: flutter pub get

      - name: Analyze code
        run: flutter analyze

      - name: Check formatting
        run: dart format --set-exit-if-changed .

  test:
    runs-on: ubuntu-latest
    needs: analyze
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'

      - name: Install dependencies
        run: flutter pub get

      - name: Run tests
        run: flutter test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage/lcov.info

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'

      - name: Build APK
        run: flutter build apk --release

      - name: Build iOS
        run: flutter build ios --release --no-codesign
        if: runner.os == 'macOS'
```

#### Día 3: Pre-commit hooks
```bash
# .husky/pre-commit
#!/bin/sh
echo "🔍 Running pre-commit checks..."

# Dart analyze
echo "📊 Analyzing code..."
flutter analyze
if [ $? -ne 0 ]; then
    echo "❌ Code analysis failed"
    exit 1
fi

# Format check
echo "🎨 Checking formatting..."
dart format --set-exit-if-changed .
if [ $? -ne 0 ]; then
    echo "❌ Code formatting issues found"
    echo "Run 'dart format .' to fix"
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
flutter test
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✅ All checks passed!"
```

### Semana 12: Monitoring y Analytics

#### Día 1-2: Error monitoring con Sentry
```dart
// lib/main.dart
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  await SentryFlutter.init(
    (options) {
      options.dsn = const String.fromEnvironment('SENTRY_DSN');
      options.environment = kDebugMode ? 'development' : 'production';
      options.tracesSampleRate = 1.0;
      options.beforeSend = (event, hint) {
        // Filtrar información sensible
        if (event.message?.formatted.contains('password') ?? false) {
          return null;
        }
        return event;
      };
    },
    appRunner: () => runApp(MyApp()),
  );
}
```

#### Día 3-5: Performance monitoring
```dart
// lib/core/analytics_service.dart
import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_performance/firebase_performance.dart';

class AnalyticsService {
  static final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  static final FirebasePerformance _performance = FirebasePerformance.instance;

  static Future<void> logScreenView(String screenName) async {
    await _analytics.logScreenView(
      screenName: screenName,
      screenClass: screenName,
    );
  }

  static HttpMetric? startHttpMetric(String url, HttpMethod method) {
    final metric = _performance.newHttpMetric(url, method);
    metric.start();
    return metric;
  }

  static Future<void> stopHttpMetric(HttpMetric? metric, {
    int? httpResponseCode,
    int? requestPayloadSize,
    int? responsePayloadSize,
  }) async {
    if (metric == null) return;

    if (httpResponseCode != null) {
      metric.httpResponseCode = httpResponseCode;
    }
    if (requestPayloadSize != null) {
      metric.requestPayloadSize = requestPayloadSize;
    }
    if (responsePayloadSize != null) {
      metric.responsePayloadSize = responsePayloadSize;
    }

    await metric.stop();
  }

  static Trace startTrace(String name) {
    final trace = _performance.newTrace(name);
    trace.start();
    return trace;
  }
}
```

---

## 📊 MÉTRICAS DE ÉXITO Y SEGUIMIENTO

### Dashboard de Progreso
```markdown
## Estado Actual (Semana 0/12)
- [ ] API Keys seguras (0%)
- [ ] Strings localizados (0%)
- [ ] Archivos < 1000 líneas (20%)
- [ ] Cobertura de tests (5%)
- [ ] Sin print statements (0%)
- [ ] Estado con Riverpod (10%)
- [ ] CI/CD configurado (0%)

## Objetivo Final (Semana 12/12)
- [x] API Keys seguras (100%)
- [x] Strings localizados (100%)
- [x] Archivos < 1000 líneas (100%)
- [x] Cobertura de tests (70%)
- [x] Sin print statements (100%)
- [x] Estado con Riverpod (100%)
- [x] CI/CD configurado (100%)
```

### KPIs de Mejora
```yaml
performance:
  before:
    app_startup_time: 3.5s
    average_frame_time: 20ms
    memory_usage: 180MB
    crash_rate: 2.1%
  after:
    app_startup_time: 1.8s  # -48%
    average_frame_time: 12ms  # -40%
    memory_usage: 120MB  # -33%
    crash_rate: 0.3%  # -86%

development:
  before:
    build_time: 180s
    test_execution: 0s (no tests)
    bugs_per_release: 15
    time_to_fix_bug: 4h
  after:
    build_time: 120s  # -33%
    test_execution: 60s
    bugs_per_release: 3  # -80%
    time_to_fix_bug: 1h  # -75%

maintenance:
  before:
    code_duplication: 25%
    technical_debt: HIGH
    onboarding_time: 2 weeks
  after:
    code_duplication: 5%  # -80%
    technical_debt: LOW
    onboarding_time: 3 days  # -79%
```

---

## 🎯 CHECKLIST FINAL

### Semana 0 (Emergencias) ✅
- [ ] Rotar API keys de Firebase
- [ ] Implementar variables de entorno
- [ ] Eliminar print statements
- [ ] Configurar linter estricto

### Sprint 1 (i18n) - Semana 1-2
- [ ] Auditoría de strings hardcodeados
- [ ] Crear todas las keys de traducción
- [ ] Actualizar código con l10n
- [ ] Tests de validación i18n

### Sprint 2 (Arquitectura) - Semana 3-4
- [ ] Refactorizar CompatibilityScreen
- [ ] Consolidar Premium Screens
- [ ] Eliminar código duplicado
- [ ] Documentar arquitectura

### Sprint 3 (Estado) - Semana 5-6
- [ ] Setup Riverpod providers
- [ ] Migrar setState a Riverpod
- [ ] Eliminar singletons
- [ ] Tests de providers

### Sprint 4 (Testing) - Semana 7-8
- [ ] Unit tests servicios críticos
- [ ] Widget tests pantallas principales
- [ ] Integration tests flujos críticos
- [ ] Setup coverage reporting

### Sprint 5 (Optimización) - Semana 9-10
- [ ] Análisis de performance
- [ ] Optimizar imágenes
- [ ] Implementar lazy loading
- [ ] Eliminar código muerto

### Sprint 6 (CI/CD) - Semana 11-12
- [ ] Setup GitHub Actions
- [ ] Configurar pre-commit hooks
- [ ] Implementar error monitoring
- [ ] Setup performance monitoring

---

## 💡 TIPS PARA EL ÉXITO

1. **Prioriza lo crítico:** Seguridad primero (API keys)
2. **Quick wins diarios:** Hace al menos una mejora pequeña cada día
3. **Tests desde el inicio:** No dejes los tests para el final
4. **Documenta mientras refactorizas:** Es más fácil cuando está fresco
5. **Commits pequeños:** Facilita rollbacks si algo sale mal
6. **Code reviews:** Si trabajas en equipo, review cada PR
7. **Monitorea métricas:** Mide el antes y después
8. **Celebra victorias:** Cada mejora cuenta

---

## 📞 SOPORTE Y RECURSOS

### Documentación
- [Flutter Best Practices](https://docs.flutter.dev/development/ui/widgets-intro)
- [Riverpod Documentation](https://riverpod.dev)
- [Flutter Testing Guide](https://docs.flutter.dev/testing)

### Herramientas
- [Very Good Analysis](https://pub.dev/packages/very_good_analysis)
- [Flutter Inspector](https://docs.flutter.dev/development/tools/devtools/inspector)
- [Sentry Flutter](https://docs.sentry.io/platforms/flutter/)

### Comunidad
- Flutter Discord
- r/FlutterDev
- Stack Overflow

---

**Última actualización:** 26 de Noviembre 2025
**Próxima revisión:** Semanalmente durante los sprints
**Responsable:** Equipo de Desarrollo