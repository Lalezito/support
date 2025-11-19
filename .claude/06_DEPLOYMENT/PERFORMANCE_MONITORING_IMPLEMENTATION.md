# ⚡ PERFORMANCE MONITORING IMPLEMENTATION GUIDE

**Objetivo**: Sistema completo de monitoreo de performance y métricas UX
**Servicio**: PerformanceMonitoringService (expandido)
**Prioridad**: ALTA - User Experience & Optimization
**Fecha**: 2025-10-05

---

## 🎯 Performance Metrics Overview

### Metric Categories

| Category | Metrics | Target | Alert Threshold |
|----------|---------|--------|----------------|
| App Performance | Startup time, Frame rate | <2s, 60fps | >3s, <50fps |
| Network Performance | API latency, Success rate | <500ms, >99% | >2s, <95% |
| Storage Performance | Cache hit rate, Query time | >80%, <100ms | <60%, >500ms |
| UX Metrics | Time to content, Conversion | <1s, >5% | >3s, <2% |
| Resource Usage | Memory, CPU, Battery | <150MB, <30% | >300MB, >60% |

---

## 📱 App Performance Monitoring

### 1.1 App Startup Time

```dart
// lib/services/performance_monitoring_service.dart
class PerformanceMonitoringService {
  static final PerformanceMonitoringService _instance =
    PerformanceMonitoringService._internal();
  factory PerformanceMonitoringService() => _instance;
  PerformanceMonitoringService._internal();

  final Stopwatch _startupStopwatch = Stopwatch();
  final Map<String, Duration> _metrics = {};

  // Track app startup
  void startAppStartup() {
    _startupStopwatch.start();
    _logMetric('app_startup_initiated', DateTime.now());
  }

  void markFirstFrame() {
    final duration = _startupStopwatch.elapsed;
    _metrics['time_to_first_frame'] = duration;

    _logMetric('first_frame_rendered', duration);

    if (duration.inMilliseconds > 2000) {
      _alertSlowStartup(duration);
    }
  }

  void markInteractive() {
    final duration = _startupStopwatch.elapsed;
    _metrics['time_to_interactive'] = duration;
    _stopwatch.stop();

    _logMetric('app_interactive', duration);

    // Send to analytics
    analytics.logEvent('app_startup_performance', {
      'first_frame_ms': _metrics['time_to_first_frame']!.inMilliseconds,
      'interactive_ms': duration.inMilliseconds,
      'platform': Platform.operatingSystem,
    });
  }
}
```

### 1.2 Screen Transition Performance

```dart
class ScreenPerformanceTracker {
  static final Map<String, Stopwatch> _screenTimers = {};

  static void startScreenLoad(String screenName) {
    _screenTimers[screenName] = Stopwatch()..start();
  }

  static void endScreenLoad(String screenName) {
    final stopwatch = _screenTimers[screenName];
    if (stopwatch == null) return;

    stopwatch.stop();
    final duration = stopwatch.elapsedMilliseconds;

    // Log to analytics
    analytics.logEvent('screen_load_time', {
      'screen': screenName,
      'duration_ms': duration,
      'is_slow': duration > 1000,
    });

    // Alert if too slow
    if (duration > 3000) {
      SecureLoggingService().warning(
        'Slow screen load: $screenName took ${duration}ms'
      );
    }

    _screenTimers.remove(screenName);
  }
}

// Usage in screens
class HoroscopeScreen extends StatefulWidget {
  @override
  void initState() {
    super.initState();
    ScreenPerformanceTracker.startScreenLoad('horoscope');
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    // Mark as loaded when dependencies are ready
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScreenPerformanceTracker.endScreenLoad('horoscope');
    });
  }
}
```

### 1.3 Frame Rate Monitoring

```dart
class FrameRateMonitor {
  static int _droppedFrames = 0;
  static int _totalFrames = 0;
  static DateTime _monitoringStart = DateTime.now();

  static void initialize() {
    WidgetsBinding.instance.addTimingsCallback((timings) {
      for (final timing in timings) {
        _totalFrames++;

        // Frame budget: 16.67ms for 60fps
        const frameBudget = Duration(milliseconds: 16);
        final frameDuration = timing.totalSpan;

        if (frameDuration > frameBudget) {
          _droppedFrames++;

          // Log slow frame
          if (frameDuration.inMilliseconds > 100) {
            SecureLoggingService().debug(
              'Slow frame detected: ${frameDuration.inMilliseconds}ms'
            );
          }
        }
      }

      // Report every 5 minutes
      if (DateTime.now().difference(_monitoringStart).inMinutes >= 5) {
        _reportFrameStats();
        _resetStats();
      }
    });
  }

  static void _reportFrameStats() {
    final dropRate = (_droppedFrames / _totalFrames) * 100;

    analytics.logEvent('frame_performance', {
      'total_frames': _totalFrames,
      'dropped_frames': _droppedFrames,
      'drop_rate_percent': dropRate,
      'duration_minutes': 5,
    });

    if (dropRate > 5.0) {
      SecureLoggingService().warning(
        'High frame drop rate: ${dropRate.toStringAsFixed(2)}%'
      );
    }
  }

  static void _resetStats() {
    _droppedFrames = 0;
    _totalFrames = 0;
    _monitoringStart = DateTime.now();
  }
}
```

---

## 🌐 Network Performance Monitoring

### 2.1 API Call Performance

```dart
// lib/services/backend_service.dart
class BackendService {
  Future<T> _performRequest<T>(
    String endpoint,
    Future<T> Function() request,
  ) async {
    final stopwatch = Stopwatch()..start();
    final startTime = DateTime.now();

    try {
      final result = await request();
      stopwatch.stop();

      // Log successful request
      _logApiPerformance(
        endpoint: endpoint,
        duration: stopwatch.elapsed,
        success: true,
        statusCode: 200,
      );

      return result;

    } catch (e, stack) {
      stopwatch.stop();

      // Log failed request
      _logApiPerformance(
        endpoint: endpoint,
        duration: stopwatch.elapsed,
        success: false,
        error: e.toString(),
      );

      rethrow;
    }
  }

  void _logApiPerformance({
    required String endpoint,
    required Duration duration,
    required bool success,
    int? statusCode,
    String? error,
  }) {
    final durationMs = duration.inMilliseconds;

    // Analytics event
    analytics.logEvent('api_call_completed', {
      'endpoint': endpoint,
      'duration_ms': durationMs,
      'success': success,
      'status_code': statusCode,
      'is_slow': durationMs > 2000,
    });

    // Performance tracking
    PerformanceMonitoringService().trackApiCall(
      endpoint: endpoint,
      duration: duration,
      success: success,
    );

    // Alert on slow requests
    if (durationMs > 3000) {
      SecureLoggingService().warning(
        'Slow API call: $endpoint took ${durationMs}ms',
        error: error,
      );
    }
  }
}
```

### 2.2 Network Success Rate Tracking

```dart
class NetworkHealthMonitor {
  static int _successfulRequests = 0;
  static int _failedRequests = 0;
  static DateTime _windowStart = DateTime.now();

  static void recordSuccess(String endpoint) {
    _successfulRequests++;
    _checkAndReport();
  }

  static void recordFailure(String endpoint, dynamic error) {
    _failedRequests++;
    _checkAndReport();
  }

  static void _checkAndReport() {
    // Report every 100 requests or 5 minutes
    final total = _successfulRequests + _failedRequests;
    final elapsed = DateTime.now().difference(_windowStart);

    if (total >= 100 || elapsed.inMinutes >= 5) {
      _reportHealthMetrics();
      _reset();
    }
  }

  static void _reportHealthMetrics() {
    if (_successfulRequests + _failedRequests == 0) return;

    final successRate =
      (_successfulRequests / (_successfulRequests + _failedRequests)) * 100;

    analytics.logEvent('network_health', {
      'success_rate': successRate,
      'total_requests': _successfulRequests + _failedRequests,
      'failures': _failedRequests,
    });

    // Alert on low success rate
    if (successRate < 95.0) {
      SecureLoggingService().error(
        'Low network success rate: ${successRate.toStringAsFixed(2)}%'
      );
    }
  }

  static void _reset() {
    _successfulRequests = 0;
    _failedRequests = 0;
    _windowStart = DateTime.now();
  }
}
```

---

## 💾 Storage & Cache Performance

### 3.1 Cache Performance Tracking

```dart
// lib/services/cache_service.dart
class CachePerformanceTracker {
  static int _cacheHits = 0;
  static int _cacheMisses = 0;
  static final List<Duration> _accessTimes = [];

  static void recordCacheHit(String key, Duration accessTime) {
    _cacheHits++;
    _accessTimes.add(accessTime);

    if (accessTime.inMilliseconds > 100) {
      SecureLoggingService().debug(
        'Slow cache access: $key took ${accessTime.inMilliseconds}ms'
      );
    }
  }

  static void recordCacheMiss(String key) {
    _cacheMisses++;
  }

  static Map<String, dynamic> getStats() {
    final total = _cacheHits + _cacheMisses;
    if (total == 0) return {};

    final hitRate = (_cacheHits / total) * 100;
    final avgAccessTime = _accessTimes.isEmpty
      ? 0
      : _accessTimes.fold(0, (sum, d) => sum + d.inMilliseconds) / _accessTimes.length;

    return {
      'hit_rate': hitRate,
      'total_accesses': total,
      'avg_access_time_ms': avgAccessTime,
      'cache_hits': _cacheHits,
      'cache_misses': _cacheMisses,
    };
  }

  static void reportStats() {
    final stats = getStats();
    if (stats.isEmpty) return;

    analytics.logEvent('cache_performance', stats);

    // Alert on low hit rate
    if (stats['hit_rate'] < 60.0) {
      SecureLoggingService().warning(
        'Low cache hit rate: ${stats['hit_rate'].toStringAsFixed(2)}%'
      );
    }
  }
}
```

### 3.2 Database Query Performance

```dart
class DatabasePerformanceTracker {
  static Future<T> trackQuery<T>(
    String queryName,
    Future<T> Function() query,
  ) async {
    final stopwatch = Stopwatch()..start();

    try {
      final result = await query();
      stopwatch.stop();

      final durationMs = stopwatch.elapsedMilliseconds;

      analytics.logEvent('database_query', {
        'query': queryName,
        'duration_ms': durationMs,
        'success': true,
      });

      if (durationMs > 500) {
        SecureLoggingService().warning(
          'Slow database query: $queryName took ${durationMs}ms'
        );
      }

      return result;

    } catch (e, stack) {
      stopwatch.stop();

      analytics.logEvent('database_query', {
        'query': queryName,
        'duration_ms': stopwatch.elapsedMilliseconds,
        'success': false,
      });

      SecureLoggingService().error(
        'Database query failed: $queryName',
        error: e,
        stackTrace: stack,
      );

      rethrow;
    }
  }
}
```

---

## 🎨 UX Performance Metrics

### 4.1 Time to First Content

```dart
class ContentLoadingTracker {
  static final Map<String, Stopwatch> _contentTimers = {};

  static void startContentLoad(String contentType) {
    _contentTimers[contentType] = Stopwatch()..start();
  }

  static void endContentLoad(String contentType, {bool fromCache = false}) {
    final stopwatch = _contentTimers[contentType];
    if (stopwatch == null) return;

    stopwatch.stop();
    final durationMs = stopwatch.elapsedMilliseconds;

    analytics.logEvent('content_load_time', {
      'content_type': contentType,
      'duration_ms': durationMs,
      'from_cache': fromCache,
      'is_fast': durationMs < 1000,
    });

    _contentTimers.remove(contentType);
  }
}

// Usage
class HoroscopeService {
  Future<Horoscope> getDailyHoroscope(String sign) async {
    ContentLoadingTracker.startContentLoad('daily_horoscope');

    try {
      final horoscope = await _fetchHoroscope(sign);
      ContentLoadingTracker.endContentLoad('daily_horoscope');
      return horoscope;
    } catch (e) {
      ContentLoadingTracker.endContentLoad('daily_horoscope');
      rethrow;
    }
  }
}
```

### 4.2 User Interaction Latency

```dart
class InteractionPerformanceTracker {
  static void trackButtonPress(String buttonName, VoidCallback action) {
    final stopwatch = Stopwatch()..start();

    action();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      stopwatch.stop();

      analytics.logEvent('interaction_latency', {
        'interaction': buttonName,
        'latency_ms': stopwatch.elapsedMilliseconds,
      });
    });
  }
}

// Usage in widgets
ElevatedButton(
  onPressed: () => InteractionPerformanceTracker.trackButtonPress(
    'purchase_essential',
    () => _handlePurchase(),
  ),
  child: Text('Purchase'),
)
```

---

## 📊 Resource Usage Monitoring

### 5.1 Memory Monitoring

```dart
class MemoryMonitor {
  static Timer? _monitoringTimer;
  static final List<int> _memorySnapshots = [];

  static void startMonitoring() {
    _monitoringTimer = Timer.periodic(Duration(minutes: 1), (_) {
      _checkMemoryUsage();
    });
  }

  static void _checkMemoryUsage() {
    // Get current memory usage
    final info = ProcessInfo.currentRss;
    final memoryMB = info / (1024 * 1024);

    _memorySnapshots.add(memoryMB.toInt());

    // Keep last 10 snapshots
    if (_memorySnapshots.length > 10) {
      _memorySnapshots.removeAt(0);
    }

    // Report if high
    if (memoryMB > 300) {
      SecureLoggingService().warning(
        'High memory usage: ${memoryMB.toStringAsFixed(2)} MB'
      );

      analytics.logEvent('high_memory_usage', {
        'memory_mb': memoryMB,
        'snapshots': _memorySnapshots,
      });
    }

    // Detect memory leaks (consistently increasing)
    if (_memorySnapshots.length >= 5) {
      if (_isMemoryLeaking()) {
        SecureLoggingService().error(
          'Potential memory leak detected',
          error: 'Memory consistently increasing: $_memorySnapshots',
        );
      }
    }
  }

  static bool _isMemoryLeaking() {
    // Check if memory is consistently increasing
    for (int i = 1; i < _memorySnapshots.length; i++) {
      if (_memorySnapshots[i] < _memorySnapshots[i - 1]) {
        return false; // Not consistently increasing
      }
    }
    return true;
  }

  static void stopMonitoring() {
    _monitoringTimer?.cancel();
  }
}
```

### 5.2 Battery Impact Monitoring

```dart
class BatteryImpactMonitor {
  static void trackBackgroundTask(
    String taskName,
    Future<void> Function() task,
  ) async {
    final startTime = DateTime.now();

    try {
      await task();

      final duration = DateTime.now().difference(startTime);

      analytics.logEvent('background_task', {
        'task': taskName,
        'duration_ms': duration.inMilliseconds,
      });

      // Alert on long-running tasks
      if (duration.inMinutes > 5) {
        SecureLoggingService().warning(
          'Long-running background task: $taskName ran for ${duration.inMinutes}min'
        );
      }

    } catch (e, stack) {
      SecureLoggingService().error(
        'Background task failed: $taskName',
        error: e,
        stackTrace: stack,
      );
    }
  }
}
```

---

## 🎯 Performance Budgets

### Budget Configuration

```dart
class PerformanceBudgets {
  // App startup
  static const maxStartupTime = Duration(seconds: 2);
  static const maxTimeToInteractive = Duration(seconds: 3);

  // Screens
  static const maxScreenLoadTime = Duration(milliseconds: 1000);
  static const maxScreenTransitionTime = Duration(milliseconds: 300);

  // Network
  static const maxApiLatency = Duration(milliseconds: 2000);
  static const minSuccessRate = 99.0; // percent

  // Cache
  static const minCacheHitRate = 80.0; // percent
  static const maxCacheAccessTime = Duration(milliseconds: 100);

  // Resources
  static const maxMemoryUsage = 200; // MB
  static const maxCpuUsage = 40; // percent

  // UX
  static const maxTimeToFirstContent = Duration(seconds: 1);
  static const maxInteractionLatency = Duration(milliseconds: 100);
}
```

### Budget Enforcement

```dart
class BudgetEnforcer {
  static void checkBudget(String metric, dynamic value, dynamic budget) {
    bool exceeded = false;

    if (value is Duration && budget is Duration) {
      exceeded = value > budget;
    } else if (value is num && budget is num) {
      exceeded = value > budget;
    }

    if (exceeded) {
      SecureLoggingService().warning(
        'Performance budget exceeded: $metric = $value (budget: $budget)'
      );

      analytics.logEvent('budget_exceeded', {
        'metric': metric,
        'value': value.toString(),
        'budget': budget.toString(),
      });
    }
  }
}
```

---

## 📈 Performance Dashboard

### Real-Time Metrics

```dart
class PerformanceDashboard {
  static Map<String, dynamic> getCurrentMetrics() {
    return {
      'app_performance': {
        'startup_time_ms': PerformanceMonitoringService()
          ._metrics['time_to_interactive']?.inMilliseconds ?? 0,
        'frame_drop_rate': FrameRateMonitor._droppedFrames /
          (FrameRateMonitor._totalFrames + 1),
      },
      'network_performance': {
        'success_rate': NetworkHealthMonitor._successfulRequests /
          (NetworkHealthMonitor._successfulRequests +
           NetworkHealthMonitor._failedRequests + 1) * 100,
      },
      'cache_performance': CachePerformanceTracker.getStats(),
      'resource_usage': {
        'memory_mb': MemoryMonitor._memorySnapshots.isNotEmpty
          ? MemoryMonitor._memorySnapshots.last
          : 0,
      },
    };
  }

  static void reportDailyMetrics() {
    final metrics = getCurrentMetrics();

    analytics.logEvent('daily_performance_report', metrics);

    SecureLoggingService().info(
      'Daily performance report',
      context: metrics,
    );
  }
}
```

---

## 🚨 Performance Alerts

### Alert Configuration

```dart
class PerformanceAlerts {
  static void checkAndAlert() {
    final metrics = PerformanceDashboard.getCurrentMetrics();

    // Startup time alert
    final startupTime = metrics['app_performance']['startup_time_ms'];
    if (startupTime > 3000) {
      _sendAlert(
        'Slow App Startup',
        'App taking ${startupTime}ms to start (target: <2000ms)',
        severity: 'high',
      );
    }

    // Network success rate alert
    final successRate = metrics['network_performance']['success_rate'];
    if (successRate < 95.0) {
      _sendAlert(
        'Low Network Success Rate',
        'Network success rate at ${successRate.toStringAsFixed(2)}% (target: >99%)',
        severity: 'critical',
      );
    }

    // Cache hit rate alert
    final cacheHitRate = metrics['cache_performance']['hit_rate'];
    if (cacheHitRate < 60.0) {
      _sendAlert(
        'Low Cache Hit Rate',
        'Cache hit rate at ${cacheHitRate.toStringAsFixed(2)}% (target: >80%)',
        severity: 'medium',
      );
    }

    // Memory usage alert
    final memoryMB = metrics['resource_usage']['memory_mb'];
    if (memoryMB > 300) {
      _sendAlert(
        'High Memory Usage',
        'App using ${memoryMB}MB (target: <200MB)',
        severity: 'high',
      );
    }
  }

  static void _sendAlert(String title, String message, {String severity = 'medium'}) {
    SecureLoggingService().error(
      'PERFORMANCE ALERT: $title - $message'
    );

    analytics.logEvent('performance_alert', {
      'title': title,
      'message': message,
      'severity': severity,
    });

    // In production, send to monitoring service
    if (kReleaseMode) {
      FirebaseCrashlytics.instance.recordError(
        Exception('Performance Alert: $title'),
        StackTrace.current,
        reason: message,
      );
    }
  }
}
```

---

## ✅ Implementation Checklist

### Phase 1: Core Metrics
- [ ] App startup time tracking
- [ ] Screen load time tracking
- [ ] Frame rate monitoring
- [ ] API latency tracking

### Phase 2: Advanced Metrics
- [ ] Cache performance tracking
- [ ] Memory monitoring
- [ ] Network health tracking
- [ ] UX performance metrics

### Phase 3: Budgets & Alerts
- [ ] Define performance budgets
- [ ] Implement budget enforcement
- [ ] Configure alerts
- [ ] Setup daily reports

### Phase 4: Integration
- [ ] Integrate with all services
- [ ] Add to critical user flows
- [ ] Setup Firebase Performance
- [ ] Create performance dashboard

---

## 🎯 Success Criteria

- [ ] All critical paths monitored
- [ ] Performance budgets enforced
- [ ] Alerts firing correctly
- [ ] <1% performance overhead
- [ ] Daily reports generated
- [ ] No performance regressions

---

**Status**: 📝 IMPLEMENTATION GUIDE READY
**Priority**: 🟡 HIGH
**Performance Impact**: <1% overhead
**Est. Time**: 2-3 days full implementation
