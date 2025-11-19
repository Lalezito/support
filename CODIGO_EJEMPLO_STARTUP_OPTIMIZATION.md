# Código Ejemplo - Startup Optimization

## Implementación Lista para Usar

Este documento contiene el código completo y listo para copiar-pegar de la optimización de startup.

---

## 1. Lazy Service Manager

```dart
// lib/core/lazy_service_manager.dart

import 'dart:async';
import 'package:zodiac_app/utils/app_logger.dart';

/// Gestiona la inicialización lazy de servicios pesados
///
/// Uso:
/// ```dart
/// // Registrar servicio
/// LazyServiceManager().register<AdService>(
///   AdService.instance,
///   () => AdService.instance.initialize(),
/// );
///
/// // Obtener servicio (inicializa automáticamente si es necesario)
/// final adService = await LazyServiceManager().get<AdService>();
/// ```
class LazyServiceManager {
  static final LazyServiceManager _instance = LazyServiceManager._internal();
  factory LazyServiceManager() => _instance;
  LazyServiceManager._internal();

  final Map<Type, Future<void>?> _initializationFutures = {};
  final Map<Type, bool> _initialized = {};
  final Map<Type, dynamic> _services = {};
  final Map<Type, Future<void> Function()> _initializers = {};

  /// Registrar un servicio lazy
  void register<T>(T service, Future<void> Function() initializer) {
    _services[T] = service;
    _initializers[T] = initializer;
    _initialized[T] = false;

    AppLogger.debug('📦 Registered lazy service: ${T.toString()}');
  }

  /// Obtener servicio (inicializa si es necesario)
  Future<T> get<T>() async {
    // Si ya está inicializado, devolver inmediatamente
    if (_initialized[T] == true) {
      return _services[T] as T;
    }

    // Si está inicializándose, esperar la inicialización en curso
    if (_initializationFutures[T] != null) {
      await _initializationFutures[T];
      return _services[T] as T;
    }

    // Inicializar por primera vez
    final initFuture = _initializeService<T>();
    _initializationFutures[T] = initFuture;

    try {
      await initFuture;
      _initialized[T] = true;
    } finally {
      _initializationFutures[T] = null;
    }

    return _services[T] as T;
  }

  Future<void> _initializeService<T>() async {
    final stopwatch = Stopwatch()..start();

    try {
      AppLogger.info('🔵 Lazy loading: ${T.toString()}...');

      final initializer = _initializers[T];
      if (initializer != null) {
        await initializer();
      }

      stopwatch.stop();
      AppLogger.info('✅ Lazy loaded: ${T.toString()} (${stopwatch.elapsedMilliseconds}ms)');

    } catch (e, stack) {
      stopwatch.stop();
      AppLogger.error('❌ Lazy loading failed: ${T.toString()}', e, stack);
      rethrow;
    }
  }

  /// Pre-warm: Inicializar servicio en background sin bloquear
  void prewarm<T>() {
    if (_initialized[T] != true && _initializationFutures[T] == null) {
      Future.microtask(() => get<T>());
      AppLogger.debug('🔥 Pre-warming service: ${T.toString()}');
    }
  }

  /// Verificar si un servicio está inicializado
  bool isInitialized<T>() => _initialized[T] == true;

  /// Obtener todos los servicios inicializados
  List<Type> getInitializedServices() {
    return _initialized.entries
        .where((entry) => entry.value == true)
        .map((entry) => entry.key)
        .toList();
  }

  /// Reset (útil para testing)
  void reset() {
    _initializationFutures.clear();
    _initialized.clear();
    _services.clear();
    _initializers.clear();
  }
}

/// Interface para servicios lazy-loadable
abstract class LazyInitializable {
  Future<void> initialize();
  bool get isInitialized;
}
```

---

## 2. Phase Manager

```dart
// lib/core/phase_manager.dart

import 'dart:async';
import 'package:zodiac_app/utils/app_logger.dart';

/// Fases de inicialización de la app
enum InitializationPhase {
  critical,   // <500ms - Mostrar UI
  important,  // 500-1000ms - Navegación habilitada
  deferred,   // 1-3s - Background
  lazy,       // On-demand - Cuando se necesite
}

/// Registro de servicio con su fase
class ServiceRegistration {
  final String name;
  final InitializationPhase phase;
  final Future<String> Function() initializer;
  final List<Type> dependencies;
  final bool required;

  ServiceRegistration({
    required this.name,
    required this.phase,
    required this.initializer,
    this.dependencies = const [],
    this.required = true,
  });
}

/// Gestiona la inicialización de servicios por fases
class PhaseManager {
  static final List<ServiceRegistration> _services = [];
  static final Map<InitializationPhase, bool> _phaseCompleted = {
    InitializationPhase.critical: false,
    InitializationPhase.important: false,
    InitializationPhase.deferred: false,
  };
  static final Map<InitializationPhase, List<String>> _phaseResults = {};

  /// Registrar un servicio
  static void register(ServiceRegistration service) {
    _services.add(service);
    AppLogger.debug('📝 Registered service: ${service.name} (${service.phase.name})');
  }

  /// Inicializar una fase completa
  static Future<List<String>> initializePhase(InitializationPhase phase) async {
    if (_phaseCompleted[phase] == true) {
      AppLogger.warning('⚠️ Phase ${phase.name} already completed, skipping');
      return _phaseResults[phase] ?? [];
    }

    final stopwatch = Stopwatch()..start();
    final servicesInPhase = _services.where((s) => s.phase == phase).toList();

    AppLogger.info('🚀 Initializing ${phase.name} phase (${servicesInPhase.length} services)');

    // Inicializar servicios en paralelo
    final results = await Future.wait(
      servicesInPhase.map((service) => _initializeService(service)),
      eagerError: false,
    );

    stopwatch.stop();

    // Log resultados
    for (var result in results) {
      AppLogger.info('  $result');
    }

    _phaseCompleted[phase] = true;
    _phaseResults[phase] = results;

    AppLogger.info('✅ Phase ${phase.name} completed in ${stopwatch.elapsedMilliseconds}ms');

    return results;
  }

  static Future<String> _initializeService(ServiceRegistration service) async {
    final stopwatch = Stopwatch()..start();

    try {
      final result = await service.initializer();
      stopwatch.stop();

      return '${result} (${stopwatch.elapsedMilliseconds}ms)';

    } catch (e, stack) {
      stopwatch.stop();

      if (service.required) {
        AppLogger.error('❌ CRITICAL: ${service.name} failed', e, stack);
        return '❌ ${service.name} FAILED: $e (${stopwatch.elapsedMilliseconds}ms)';
      } else {
        AppLogger.warning('⚠️ Optional service ${service.name} failed: $e');
        return '⚠️ ${service.name} failed (non-critical): $e (${stopwatch.elapsedMilliseconds}ms)';
      }
    }
  }

  /// Verificar si una fase está completa
  static bool isPhaseComplete(InitializationPhase phase) {
    return _phaseCompleted[phase] == true;
  }

  /// Obtener resultados de una fase
  static List<String> getPhaseResults(InitializationPhase phase) {
    return _phaseResults[phase] ?? [];
  }

  /// Reset (útil para testing)
  static void reset() {
    _services.clear();
    _phaseCompleted.clear();
    _phaseResults.clear();
  }

  /// Obtener servicios por fase
  static List<ServiceRegistration> getServicesByPhase(InitializationPhase phase) {
    return _services.where((s) => s.phase == phase).toList();
  }
}
```

---

## 3. Startup Metrics

```dart
// lib/core/startup_metrics.dart

import 'dart:async';
import 'package:zodiac_app/utils/app_logger.dart';
import 'package:zodiac_app/services/analytics_service.dart';

/// Sistema de métricas de arranque
class StartupMetrics {
  static final Stopwatch _appStartTime = Stopwatch();
  static final Map<String, int> _milestones = {};
  static bool _started = false;
  static bool _reported = false;

  /// Iniciar tracking de métricas
  static void start() {
    if (_started) return;
    _appStartTime.start();
    _started = true;
    AppLogger.info('📊 Startup metrics tracking started');
  }

  /// Marcar un milestone
  static void markMilestone(String name) {
    if (!_started) start();

    final elapsed = _appStartTime.elapsedMilliseconds;
    _milestones[name] = elapsed;

    AppLogger.info('⏱️ Milestone: $name at ${elapsed}ms');
  }

  /// Obtener tiempo de un milestone
  static int? getMilestone(String name) {
    return _milestones[name];
  }

  /// Obtener todos los milestones
  static Map<String, int> getAllMilestones() {
    return Map.from(_milestones);
  }

  /// Calcular duración entre dos milestones
  static int? getDuration(String from, String to) {
    final fromTime = _milestones[from];
    final toTime = _milestones[to];

    if (fromTime == null || toTime == null) return null;

    return toTime - fromTime;
  }

  /// Reportar métricas a Analytics
  static Future<void> reportMetrics() async {
    if (_reported) return;

    try {
      final metrics = {
        'time_to_critical': _milestones['critical_ready'],
        'time_to_important': _milestones['important_ready'],
        'time_to_first_frame': _milestones['first_frame'],
        'time_to_interactive': _milestones['first_navigation'],
        'time_to_complete': _milestones['fully_initialized'],
        'total_startup_time': _appStartTime.elapsedMilliseconds,
      };

      // Enviar a Analytics
      await AnalyticsService.logEvent('app_startup_performance', metrics);

      // Log local
      AppLogger.info('📊 Startup Metrics Report:');
      metrics.forEach((key, value) {
        if (value != null) {
          AppLogger.info('  - $key: ${value}ms');
        }
      });

      _reported = true;

    } catch (e, stack) {
      AppLogger.error('Failed to report startup metrics', e, stack);
    }
  }

  /// Generar reporte visual
  static String generateReport() {
    final buffer = StringBuffer();
    buffer.writeln('═══════════════════════════════════════');
    buffer.writeln('    STARTUP PERFORMANCE REPORT');
    buffer.writeln('═══════════════════════════════════════');

    final sortedMilestones = _milestones.entries.toList()
      ..sort((a, b) => a.value.compareTo(b.value));

    for (final entry in sortedMilestones) {
      final bar = '█' * (entry.value ~/ 50);
      buffer.writeln('${entry.key.padRight(25)} ${entry.value.toString().padLeft(5)}ms $bar');
    }

    buffer.writeln('═══════════════════════════════════════');
    buffer.writeln('Total: ${_appStartTime.elapsedMilliseconds}ms');
    buffer.writeln('═══════════════════════════════════════');

    return buffer.toString();
  }

  /// Reset (útil para testing)
  static void reset() {
    _appStartTime.reset();
    _milestones.clear();
    _started = false;
    _reported = false;
  }
}
```

---

## 4. Service Registry

```dart
// lib/core/service_registry.dart

import 'package:zodiac_app/core/phase_manager.dart';
import 'package:zodiac_app/core/lazy_service_manager.dart';

// Importar servicios
import 'package:zodiac_app/services/ad_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';
import 'package:zodiac_app/services/user_identity_service.dart';
import 'package:zodiac_app/services/revenuecat_integration.dart';
import 'package:zodiac_app/services/crash_reporting_service.dart';
import 'package:zodiac_app/services/consolidated_analytics/core_analytics_service.dart';
import 'package:zodiac_app/services/premium_features_service.dart';
import 'package:zodiac_app/services/data_migration_service.dart';
import 'package:zodiac_app/services/birth_data_service.dart';
import 'package:zodiac_app/services/unified_notification_service.dart';
import 'package:zodiac_app/services/daily_horoscope_notification_scheduler.dart';
import 'package:zodiac_app/services/consolidated_compatibility/core_compatibility_service.dart';
import 'package:zodiac_app/services/user_authentication_service.dart';

/// Registrar todos los servicios con sus fases
void registerAllServices() {

  // ========================================
  // FASE CRÍTICA - <500ms
  // ========================================

  PhaseManager.register(ServiceRegistration(
    name: 'Preferences Service (Basic)',
    phase: InitializationPhase.critical,
    initializer: () async {
      await PreferencesService.instance.initialize();
      return '✅ Preferences initialized';
    },
    required: true,
  ));

  // ========================================
  // FASE IMPORTANTE - 500-1000ms
  // ========================================

  PhaseManager.register(ServiceRegistration(
    name: 'User Identity Service',
    phase: InitializationPhase.important,
    initializer: () async {
      await UserIdentityService.instance.initialize();
      final userId = await UserIdentityService.instance.getRevenueCatUserId();
      return '✅ User Identity (${userId.substring(0, 15)}...)';
    },
    required: true,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'RevenueCat Integration',
    phase: InitializationPhase.important,
    initializer: () async {
      final integration = RevenueCatIntegration();
      await integration.initialize(
        preferencesService: PreferencesService.instance,
      );
      return '✅ RevenueCat initialized';
    },
    dependencies: [UserIdentityService],
    required: true,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Crashlytics',
    phase: InitializationPhase.important,
    initializer: () async {
      await CrashReportingService.instance.initialize();
      return '✅ Crashlytics initialized';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Premium Features Service',
    phase: InitializationPhase.important,
    initializer: () async {
      await PremiumFeaturesService.instance.initialize();
      return '✅ Premium Features initialized';
    },
    required: true,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Analytics Service (Basic)',
    phase: InitializationPhase.important,
    initializer: () async {
      await CoreAnalyticsService.instance.initialize();
      return '✅ Analytics initialized';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Authentication Service',
    phase: InitializationPhase.important,
    initializer: () async {
      await UserAuthenticationService.instance.initialize();
      return '✅ Authentication initialized';
    },
    required: true,
  ));

  // ========================================
  // FASE DIFERIDA - 1-3s background
  // ========================================

  PhaseManager.register(ServiceRegistration(
    name: 'Data Migration Service',
    phase: InitializationPhase.deferred,
    initializer: () async {
      await DataMigrationService.instance.initialize();
      return '✅ Data Migration initialized';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Birth Data Service',
    phase: InitializationPhase.deferred,
    initializer: () async {
      await BirthDataService().initialize();
      return '✅ Birth Data initialized';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Notification Service',
    phase: InitializationPhase.deferred,
    initializer: () async {
      await UnifiedNotificationService.instance.initialize();
      return '✅ Notifications initialized';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Daily Notifications Scheduler',
    phase: InitializationPhase.deferred,
    initializer: () async {
      final scheduler = DailyHoroscopeNotificationScheduler();
      await scheduler.initialize();
      return '✅ Daily Notifications scheduled';
    },
    required: false,
  ));

  PhaseManager.register(ServiceRegistration(
    name: 'Compatibility Service',
    phase: InitializationPhase.deferred,
    initializer: () async {
      await CoreCompatibilityService.instance.initialize();
      return '✅ Compatibility Service initialized';
    },
    required: false,
  ));

  // ========================================
  // FASE LAZY - On-demand
  // ========================================

  // AdService - Solo para usuarios free
  LazyServiceManager().register<AdService>(
    AdService.instance,
    () => AdService.instance.initialize(),
  );
}
```

---

## 5. Main Optimizado

```dart
// lib/main_optimized.dart

import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

import 'package:zodiac_app/firebase_options.dart';
import 'package:zodiac_app/config/logger_config.dart';
import 'package:zodiac_app/utils/app_logger.dart';
import 'package:zodiac_app/core/phase_manager.dart';
import 'package:zodiac_app/core/service_registry.dart';
import 'package:zodiac_app/core/startup_metrics.dart';

// Tu app actual
import 'package:zodiac_app/main.dart' show MyApp, _setupDeviceConfiguration;

void main() async {
  // ==========================================
  // INICIO: Tracking de métricas
  // ==========================================
  StartupMetrics.start();

  await runZonedGuarded<Future<void>>(() async {

    // ==========================================
    // PRE-FLUTTER: Setup esencial
    // ==========================================
    WidgetsFlutterBinding.ensureInitialized();
    StartupMetrics.markMilestone('flutter_binding_ready');

    // Cargar variables de entorno
    await dotenv.load(fileName: ".env");
    StartupMetrics.markMilestone('env_loaded');

    // Inicializar logger
    LoggerConfig.initialize();
    AppLogger.info('🚀 Zodiac App - Optimized Startup Mode');
    StartupMetrics.markMilestone('logger_ready');

    // Configuración de dispositivo
    _setupDeviceConfiguration();
    StartupMetrics.markMilestone('device_config_ready');

    // Firebase Core
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    StartupMetrics.markMilestone('firebase_core_ready');

    // Setup error handlers
    FlutterError.onError = (errorDetails) {
      FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
    };

    PlatformDispatcher.instance.onError = (error, stack) {
      FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
      return true;
    };

    // ==========================================
    // FASE CRÍTICA: Solo servicios esenciales
    // ==========================================
    registerAllServices(); // Registrar todos los servicios

    await PhaseManager.initializePhase(InitializationPhase.critical);
    StartupMetrics.markMilestone('critical_ready');

    AppLogger.info('✅ Critical services ready - Launching UI');

    // ==========================================
    // LANZAR APP INMEDIATAMENTE
    // ==========================================
    runApp(const MyApp());
    StartupMetrics.markMilestone('first_frame');

    // ==========================================
    // POST-LAUNCH: Fases importantes y diferidas
    // ==========================================
    _initializePostLaunch();

  }, (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    AppLogger.error('Uncaught error in main', error, stack);
  });
}

/// Inicializar servicios después del launch
void _initializePostLaunch() {

  // FASE IMPORTANTE: Después del primer frame
  Future.microtask(() async {
    try {
      AppLogger.info('🔵 Starting important services phase...');

      await PhaseManager.initializePhase(InitializationPhase.important);
      StartupMetrics.markMilestone('important_ready');

      AppLogger.info('✅ Important services ready - Navigation enabled');

    } catch (e, stack) {
      AppLogger.error('Important phase initialization error', e, stack);
    }
  });

  // FASE DIFERIDA: Después del segundo frame
  WidgetsBinding.instance.addPostFrameCallback((_) async {
    try {
      AppLogger.info('🔵 Starting deferred services phase...');

      await PhaseManager.initializePhase(InitializationPhase.deferred);
      StartupMetrics.markMilestone('fully_initialized');

      AppLogger.info('✅ All services initialized');

      // Reportar métricas
      await StartupMetrics.reportMetrics();

      // Log reporte visual
      if (kDebugMode) {
        AppLogger.info('\n${StartupMetrics.generateReport()}');
      }

    } catch (e, stack) {
      AppLogger.error('Deferred phase initialization error', e, stack);
    }
  });
}
```

---

## 6. Ejemplo de Servicio Lazy

```dart
// lib/services/lazy/ad_service_lazy.dart

import 'package:zodiac_app/core/lazy_service_manager.dart';
import 'package:zodiac_app/services/ad_service.dart';
import 'package:zodiac_app/utils/app_logger.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

/// AdService con lazy loading
class AdServiceLazy implements LazyInitializable {
  static AdServiceLazy? _instance;
  static AdServiceLazy get instance => _instance ??= AdServiceLazy._();

  AdServiceLazy._();

  bool _isInitialized = false;

  @override
  bool get isInitialized => _isInitialized;

  @override
  Future<void> initialize() async {
    if (_isInitialized) return;

    AppLogger.info('🎯 Lazy loading AdService...');

    try {
      // Inicializar MobileAds
      await MobileAds.instance.initialize().timeout(
        const Duration(seconds: 5),
      );

      // Inicializar AdService
      await AdService.instance.initialize().timeout(
        const Duration(seconds: 3),
      );

      _isInitialized = true;
      AppLogger.info('✅ AdService lazy loaded successfully');

    } catch (e, stack) {
      AppLogger.error('❌ AdService lazy loading failed', e, stack);
      rethrow;
    }
  }

  /// Mostrar banner ad (lazy load si es necesario)
  Future<void> showBannerAd() async {
    if (!_isInitialized) {
      await initialize();
    }

    AdService.instance.createBannerAd();
  }

  /// Mostrar interstitial ad (lazy load si es necesario)
  Future<void> showInterstitialAd() async {
    if (!_isInitialized) {
      await initialize();
    }

    await AdService.instance.showInterstitialAd();
  }

  /// Pre-cargar ads en background
  void prewarmAds() {
    LazyServiceManager().prewarm<AdServiceLazy>();
  }
}

// Registrar en service_registry.dart:
// LazyServiceManager().register<AdServiceLazy>(
//   AdServiceLazy.instance,
//   () => AdServiceLazy.instance.initialize(),
// );
```

---

## 7. Widget para Mostrar Estado de Inicialización

```dart
// lib/widgets/initialization_status_indicator.dart

import 'package:flutter/material.dart';
import 'package:zodiac_app/core/phase_manager.dart';
import 'package:zodiac_app/core/lazy_service_manager.dart';

/// Widget que muestra el estado de inicialización (solo debug)
class InitializationStatusIndicator extends StatefulWidget {
  const InitializationStatusIndicator({super.key});

  @override
  State<InitializationStatusIndicator> createState() => _InitializationStatusIndicatorState();
}

class _InitializationStatusIndicatorState extends State<InitializationStatusIndicator> {
  @override
  void initState() {
    super.initState();
    // Actualizar cada 500ms
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) {
        setState(() {});
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final criticalDone = PhaseManager.isPhaseComplete(InitializationPhase.critical);
    final importantDone = PhaseManager.isPhaseComplete(InitializationPhase.important);
    final deferredDone = PhaseManager.isPhaseComplete(InitializationPhase.deferred);

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.black87,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Initialization Status',
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          _buildPhaseStatus('Critical', criticalDone),
          _buildPhaseStatus('Important', importantDone),
          _buildPhaseStatus('Deferred', deferredDone),
        ],
      ),
    );
  }

  Widget _buildPhaseStatus(String name, bool done) {
    return Row(
      children: [
        Icon(
          done ? Icons.check_circle : Icons.hourglass_empty,
          color: done ? Colors.green : Colors.orange,
          size: 16,
        ),
        const SizedBox(width: 8),
        Text(
          name,
          style: TextStyle(
            color: done ? Colors.green : Colors.orange,
          ),
        ),
      ],
    );
  }
}

// Usar en HomeScreen (solo debug):
// if (kDebugMode)
//   Positioned(
//     bottom: 16,
//     right: 16,
//     child: InitializationStatusIndicator(),
//   ),
```

---

## 8. Tests

```dart
// test/core/lazy_service_manager_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:zodiac_app/core/lazy_service_manager.dart';

class MockService implements LazyInitializable {
  bool _initialized = false;
  int initCallCount = 0;

  @override
  bool get isInitialized => _initialized;

  @override
  Future<void> initialize() async {
    await Future.delayed(const Duration(milliseconds: 100));
    _initialized = true;
    initCallCount++;
  }
}

void main() {
  setUp(() {
    LazyServiceManager().reset();
  });

  group('LazyServiceManager', () {

    test('service is not initialized on registration', () {
      final service = MockService();
      LazyServiceManager().register<MockService>(
        service,
        () => service.initialize(),
      );

      expect(LazyServiceManager().isInitialized<MockService>(), false);
      expect(service.initCallCount, 0);
    });

    test('service initializes on first get', () async {
      final service = MockService();
      LazyServiceManager().register<MockService>(
        service,
        () => service.initialize(),
      );

      final retrieved = await LazyServiceManager().get<MockService>();

      expect(retrieved, service);
      expect(service.initCallCount, 1);
      expect(LazyServiceManager().isInitialized<MockService>(), true);
    });

    test('service initializes only once on multiple gets', () async {
      final service = MockService();
      LazyServiceManager().register<MockService>(
        service,
        () => service.initialize(),
      );

      await LazyServiceManager().get<MockService>();
      await LazyServiceManager().get<MockService>();
      await LazyServiceManager().get<MockService>();

      expect(service.initCallCount, 1);
    });

    test('prewarm starts initialization in background', () async {
      final service = MockService();
      LazyServiceManager().register<MockService>(
        service,
        () => service.initialize(),
      );

      LazyServiceManager().prewarm<MockService>();

      // Dar tiempo para que inicie
      await Future.delayed(const Duration(milliseconds: 200));

      expect(LazyServiceManager().isInitialized<MockService>(), true);
      expect(service.initCallCount, 1);
    });

  });

  group('PhaseManager', () {

    test('critical phase services initialize', () async {
      PhaseManager.register(ServiceRegistration(
        name: 'Test Service',
        phase: InitializationPhase.critical,
        initializer: () async {
          return '✅ Test service initialized';
        },
      ));

      final results = await PhaseManager.initializePhase(
        InitializationPhase.critical,
      );

      expect(results.length, 1);
      expect(results[0], contains('Test service initialized'));
      expect(PhaseManager.isPhaseComplete(InitializationPhase.critical), true);
    });

    test('phase does not reinitialize if already complete', () async {
      int callCount = 0;

      PhaseManager.register(ServiceRegistration(
        name: 'Test Service',
        phase: InitializationPhase.critical,
        initializer: () async {
          callCount++;
          return '✅ Test';
        },
      ));

      await PhaseManager.initializePhase(InitializationPhase.critical);
      await PhaseManager.initializePhase(InitializationPhase.critical);

      expect(callCount, 1);
    });

  });
}
```

---

## 9. Cómo Migrar

### Paso 1: Copiar archivos core

```bash
# Crear directorio core si no existe
mkdir -p lib/core

# Copiar archivos
# - lazy_service_manager.dart
# - phase_manager.dart
# - startup_metrics.dart
# - service_registry.dart
```

### Paso 2: Actualizar main.dart

```dart
// Opción 1: Renombrar actual y usar optimizado
mv lib/main.dart lib/main_legacy.dart
# Copiar main_optimized.dart a main.dart

// Opción 2: Feature flag para A/B testing
const bool USE_OPTIMIZED_STARTUP = true; // Toggle aquí

void main() async {
  if (USE_OPTIMIZED_STARTUP) {
    return mainOptimized();
  } else {
    return mainLegacy();
  }
}
```

### Paso 3: Migrar servicios uno por uno

```dart
// Ejemplo: Migrar AdService

// ANTES (en main.dart):
await _initializeAds(), // Bloqueaba startup

// DESPUÉS (lazy loading):
LazyServiceManager().register<AdService>(
  AdService.instance,
  () => AdService.instance.initialize(),
);

// Usar cuando se necesite:
final adService = await LazyServiceManager().get<AdService>();
await adService.showInterstitialAd();
```

### Paso 4: Verificar resultados

```dart
// En HomeScreen, agregar (solo debug):
if (kDebugMode) {
  Future.delayed(Duration(seconds: 2), () {
    print(StartupMetrics.generateReport());
  });
}
```

---

## 10. Checklist de Migración

```
✅ FASE 1: INFRAESTRUCTURA
  [ ] Copiar lazy_service_manager.dart
  [ ] Copiar phase_manager.dart
  [ ] Copiar startup_metrics.dart
  [ ] Copiar service_registry.dart
  [ ] Ejecutar tests unitarios

✅ FASE 2: SERVICIOS PESADOS
  [ ] Migrar RevenueCat a init parcial
  [ ] Migrar AdService a lazy loading
  [ ] Migrar Firebase Messaging a deferred
  [ ] Migrar Analytics a basic+full
  [ ] Verificar tiempos individuales

✅ FASE 3: MAIN OPTIMIZADO
  [ ] Crear main_optimized.dart
  [ ] Implementar fases de inicialización
  [ ] Agregar StartupMetrics tracking
  [ ] Testing en dispositivos reales

✅ FASE 4: VALIDACIÓN
  [ ] A/B testing (legacy vs optimized)
  [ ] Monitorear Analytics
  [ ] Verificar <2s startup time
  [ ] Deploy a producción
```

---

**¡Todo listo para implementar! 🚀**

Estos archivos pueden copiarse directamente al proyecto y empezar a usarse de inmediato.
