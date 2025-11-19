# 🔐 SECURE LOGGING IMPLEMENTATION GUIDE

**Objetivo**: Sistema de logs seguro sin exponer datos sensibles
**Servicio**: SecureLoggingService
**Prioridad**: ALTA - Security & Debugging
**Fecha**: 2025-10-05

---

## 🎯 Log Levels & Environment Configuration

### Log Level Hierarchy
```dart
enum LogLevel {
  debug(0),
  info(1),
  warning(2),
  error(3),
  critical(4);

  final int value;
  const LogLevel(this.value);
}
```

### Environment-Based Configuration
```dart
class LogConfig {
  static LogLevel get currentLevel {
    if (kDebugMode) return LogLevel.debug;
    if (kProfileMode) return LogLevel.info;
    if (kReleaseMode) return LogLevel.warning;
    return LogLevel.error;
  }

  static bool shouldLog(LogLevel level) {
    return level.value >= currentLevel.value;
  }
}
```

### Usage by Environment

| Environment | Debug | Info | Warning | Error | Critical |
|-------------|-------|------|---------|-------|----------|
| Development | ✅ | ✅ | ✅ | ✅ | ✅ |
| Staging | ❌ | ✅ | ✅ | ✅ | ✅ |
| Production | ❌ | ❌ | ✅ | ✅ | ✅ |

---

## 🔒 Sensitive Data Protection

### Prohibited Data (NEVER Log)

```dart
class SensitiveDataFilter {
  static const prohibited = [
    'password',
    'token',
    'api_key',
    'secret',
    'credit_card',
    'ssn',
    'birth_date', // Full date
    'birth_time',
    'email',
    'phone',
    'address',
    'location', // Precise GPS
  ];

  static String sanitize(String message) {
    var sanitized = message;

    // Redact passwords
    sanitized = sanitized.replaceAllMapped(
      RegExp(r'password[:\s]*[^\s,}]+', caseSensitive: false),
      (match) => 'password: [REDACTED]',
    );

    // Redact tokens
    sanitized = sanitized.replaceAllMapped(
      RegExp(r'token[:\s]*[^\s,}]+', caseSensitive: false),
      (match) => 'token: [REDACTED]',
    );

    // Redact emails
    sanitized = sanitized.replaceAllMapped(
      RegExp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
      (match) => '[EMAIL_REDACTED]',
    );

    return sanitized;
  }
}
```

### Safe Data to Log

```dart
class SafeDataLogger {
  // ✅ Safe: Hashed user IDs
  static String safeUserId(String userId) {
    return sha256.convert(utf8.encode(userId))
      .toString()
      .substring(0, 8);
  }

  // ✅ Safe: Sign names (not PII)
  static String safeSign(String sign) => sign; // OK

  // ✅ Safe: Error types (no stack with PII)
  static String safeError(dynamic error) {
    return error.runtimeType.toString();
  }

  // ✅ Safe: Timestamps
  static String safeTimestamp() {
    return DateTime.now().toIso8601String();
  }
}
```

---

## 📝 SecureLoggingService Implementation

### Core Service
```dart
// lib/services/secure_logging_service.dart
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class SecureLoggingService {
  static final SecureLoggingService _instance = SecureLoggingService._internal();
  factory SecureLoggingService() => _instance;
  SecureLoggingService._internal();

  final List<LogEntry> _buffer = [];
  static const int _maxBufferSize = 1000;
  static const int _maxFileSize = 10 * 1024 * 1024; // 10 MB
  static const int _maxLogAge = 7; // days

  File? _logFile;
  bool _initialized = false;

  // Initialize logging system
  Future<void> initialize() async {
    if (_initialized) return;

    try {
      final directory = await getApplicationDocumentsDirectory();
      final logDir = Directory('${directory.path}/logs');
      
      if (!await logDir.exists()) {
        await logDir.create(recursive: true);
      }

      _logFile = File('${logDir.path}/app_${DateTime.now().millisecondsSinceEpoch}.log');
      _initialized = true;

      // Start periodic flush
      _startPeriodicFlush();
      
      // Cleanup old logs
      await _cleanupOldLogs(logDir);
    } catch (e) {
      debugPrint('Failed to initialize logging: $e');
    }
  }

  // Log methods
  void debug(String message, {Map<String, dynamic>? context}) {
    _log(LogLevel.debug, message, context);
  }

  void info(String message, {Map<String, dynamic>? context}) {
    _log(LogLevel.info, message, context);
  }

  void warning(String message, {Map<String, dynamic>? context}) {
    _log(LogLevel.warning, message, context);
  }

  void error(String message, {dynamic error, StackTrace? stackTrace}) {
    _log(LogLevel.error, message, {
      'error': error?.toString(),
      'stack_trace': stackTrace?.toString().substring(0, 500),
    });
  }

  void critical(String message, {dynamic error, StackTrace? stackTrace}) {
    _log(LogLevel.critical, message, {
      'error': error?.toString(),
      'stack_trace': stackTrace?.toString(),
    });

    // Critical errors: send to remote immediately
    _sendToRemote(LogLevel.critical, message, error, stackTrace);
  }

  // Internal logging
  void _log(LogLevel level, String message, Map<String, dynamic>? context) {
    if (!LogConfig.shouldLog(level)) return;

    // Sanitize message
    final sanitized = SensitiveDataFilter.sanitize(message);

    final entry = LogEntry(
      level: level,
      message: sanitized,
      timestamp: DateTime.now(),
      context: context,
    );

    _buffer.add(entry);

    // Console output in development
    if (kDebugMode) {
      _printToConsole(entry);
    }

    // Flush if buffer full
    if (_buffer.length >= _maxBufferSize) {
      _flush();
    }
  }

  // Periodic flush (every 5 minutes)
  void _startPeriodicFlush() {
    Timer.periodic(Duration(minutes: 5), (_) {
      _flush();
    });
  }

  // Flush buffer to file
  Future<void> _flush() async {
    if (_buffer.isEmpty || _logFile == null) return;

    try {
      final logs = _buffer.map((e) => e.toJson()).join('\n');
      await _logFile!.writeAsString('$logs\n', mode: FileMode.append);
      _buffer.clear();

      // Check file size
      final fileSize = await _logFile!.length();
      if (fileSize > _maxFileSize) {
        await _rotateLogFile();
      }
    } catch (e) {
      debugPrint('Failed to flush logs: $e');
    }
  }

  // Rotate log file
  Future<void> _rotateLogFile() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final logDir = Directory('${directory.path}/logs');
      
      _logFile = File('${logDir.path}/app_${DateTime.now().millisecondsSinceEpoch}.log');
    } catch (e) {
      debugPrint('Failed to rotate log file: $e');
    }
  }

  // Cleanup old logs
  Future<void> _cleanupOldLogs(Directory logDir) async {
    try {
      final files = logDir.listSync();
      final cutoffDate = DateTime.now().subtract(Duration(days: _maxLogAge));

      for (final file in files) {
        if (file is File) {
          final stat = await file.stat();
          if (stat.modified.isBefore(cutoffDate)) {
            await file.delete();
          }
        }
      }
    } catch (e) {
      debugPrint('Failed to cleanup logs: $e');
    }
  }

  // Send critical errors to remote
  Future<void> _sendToRemote(
    LogLevel level,
    String message,
    dynamic error,
    StackTrace? stackTrace,
  ) async {
    if (!kReleaseMode) return;

    try {
      await FirebaseCrashlytics.instance.recordError(
        error,
        stackTrace,
        reason: message,
        fatal: level == LogLevel.critical,
      );
    } catch (e) {
      debugPrint('Failed to send to Crashlytics: $e');
    }
  }

  // Console output
  void _printToConsole(LogEntry entry) {
    final emoji = _levelEmoji(entry.level);
    final timestamp = entry.timestamp.toIso8601String();
    print('$emoji [$timestamp] ${entry.level.name.toUpperCase()}: ${entry.message}');
    
    if (entry.context != null) {
      print('   Context: ${entry.context}');
    }
  }

  String _levelEmoji(LogLevel level) {
    switch (level) {
      case LogLevel.debug: return '🔍';
      case LogLevel.info: return 'ℹ️';
      case LogLevel.warning: return '⚠️';
      case LogLevel.error: return '❌';
      case LogLevel.critical: return '🔥';
    }
  }
}
```

### Log Entry Model
```dart
class LogEntry {
  final LogLevel level;
  final String message;
  final DateTime timestamp;
  final Map<String, dynamic>? context;

  LogEntry({
    required this.level,
    required this.message,
    required this.timestamp,
    this.context,
  });

  String toJson() {
    return jsonEncode({
      'level': level.name,
      'message': message,
      'timestamp': timestamp.toIso8601String(),
      if (context != null) 'context': context,
    });
  }
}
```

---

## 🚀 Usage Examples

### Service Logging
```dart
// lib/services/horoscope_service.dart
class HoroscopeService {
  final logger = SecureLoggingService();

  Future<Horoscope> getDailyHoroscope(String sign) async {
    logger.debug('Fetching daily horoscope', context: {
      'sign': sign,
      'user_id': SafeDataLogger.safeUserId(userId),
    });

    try {
      final horoscope = await _fetchFromBackend(sign);
      
      logger.info('Horoscope fetched successfully', context: {
        'sign': sign,
        'cached': false,
      });

      return horoscope;
    } catch (e, stack) {
      logger.error('Failed to fetch horoscope', 
        error: e, 
        stackTrace: stack
      );
      
      // Try cache fallback
      return await _getFromCache(sign);
    }
  }
}
```

### Purchase Flow Logging
```dart
// lib/services/subscription_service.dart
class SubscriptionService {
  final logger = SecureLoggingService();

  Future<bool> purchaseTier(SubscriptionType tier) async {
    logger.info('Purchase initiated', context: {
      'tier': tier.name,
      'price': tier.price,
      'user_id': SafeDataLogger.safeUserId(userId),
    });

    try {
      final result = await revenueCat.purchase(tier.productId);

      logger.info('Purchase completed', context: {
        'tier': tier.name,
        'transaction_id': result.transactionId,
        'revenue': tier.price,
      });

      return true;
    } catch (e, stack) {
      logger.error('Purchase failed', error: e, stackTrace: stack);
      return false;
    }
  }
}
```

### Critical Error Logging
```dart
// Global error handler
void main() {
  FlutterError.onError = (details) {
    final logger = SecureLoggingService();
    
    logger.critical('Flutter error caught', 
      error: details.exception,
      stackTrace: details.stack,
    );
  };

  runZonedGuarded(() {
    runApp(MyApp());
  }, (error, stack) {
    final logger = SecureLoggingService();
    
    logger.critical('Uncaught error', 
      error: error,
      stackTrace: stack,
    );
  });
}
```

---

## 📊 Remote Logging (Production)

### Firebase Crashlytics Integration
```dart
class RemoteLogger {
  static Future<void> initialize() async {
    if (kReleaseMode) {
      await FirebaseCrashlytics.instance
        .setCrashlyticsCollectionEnabled(true);
    }
  }

  static Future<void> logError(
    String message,
    dynamic error,
    StackTrace? stackTrace, {
    bool fatal = false,
  }) async {
    if (!kReleaseMode) return;

    try {
      await FirebaseCrashlytics.instance.recordError(
        error,
        stackTrace,
        reason: message,
        fatal: fatal,
      );
    } catch (e) {
      debugPrint('Failed to log to Crashlytics: $e');
    }
  }

  static Future<void> setCustomKey(String key, dynamic value) async {
    if (!kReleaseMode) return;

    await FirebaseCrashlytics.instance.setCustomKey(key, value);
  }

  static Future<void> setUserId(String userId) async {
    if (!kReleaseMode) return;

    // Hash user ID before sending
    final hashedId = SafeDataLogger.safeUserId(userId);
    await FirebaseCrashlytics.instance.setUserIdentifier(hashedId);
  }
}
```

### Batched Remote Logging
```dart
class BatchedRemoteLogger {
  static final List<Map<String, dynamic>> _batch = [];
  static const int _batchSize = 50;
  static const Duration _batchInterval = Duration(minutes: 5);

  static void addLog(LogLevel level, String message, Map<String, dynamic>? context) {
    _batch.add({
      'level': level.name,
      'message': message,
      'timestamp': DateTime.now().toIso8601String(),
      'context': context,
    });

    if (_batch.length >= _batchSize) {
      _flush();
    }
  }

  static Future<void> _flush() async {
    if (_batch.isEmpty) return;

    try {
      // Send to your logging endpoint
      await http.post(
        Uri.parse('https://your-logging-endpoint.com/logs'),
        body: jsonEncode(_batch),
      );

      _batch.clear();
    } catch (e) {
      debugPrint('Failed to send log batch: $e');
    }
  }

  static void startPeriodicFlush() {
    Timer.periodic(_batchInterval, (_) => _flush());
  }
}
```

---

## 🛡️ Security Best Practices

### 1. Data Sanitization Checklist
- [ ] All user inputs sanitized before logging
- [ ] Passwords/tokens never logged
- [ ] Email addresses redacted
- [ ] Stack traces truncated (max 500 chars)
- [ ] User IDs hashed

### 2. Log Retention
- [ ] Local logs: Max 7 days
- [ ] Max file size: 10 MB per file
- [ ] Auto-rotation enabled
- [ ] Old logs auto-deleted

### 3. Remote Logging
- [ ] Only ERROR and CRITICAL in production
- [ ] Batch sending for efficiency
- [ ] Retry logic with exponential backoff
- [ ] Rate limiting (max 100 logs/min)

### 4. Access Control
- [ ] Log files in protected directory
- [ ] No logs in version control
- [ ] Production logs require auth
- [ ] Audit log access

---

## 📈 Monitoring & Alerts

### Error Rate Alerts
```dart
class ErrorRateMonitor {
  static int _errorCount = 0;
  static DateTime _windowStart = DateTime.now();
  static const Duration _window = Duration(minutes: 5);
  static const int _errorThreshold = 10;

  static void trackError() {
    final now = DateTime.now();
    
    if (now.difference(_windowStart) > _window) {
      _errorCount = 0;
      _windowStart = now;
    }

    _errorCount++;

    if (_errorCount > _errorThreshold) {
      _sendAlert('High error rate detected: $_errorCount errors in 5 minutes');
    }
  }

  static void _sendAlert(String message) {
    // Send to monitoring system
    // e.g., Sentry, DataDog, custom endpoint
  }
}
```

---

## ✅ Implementation Checklist

### Phase 1: Core Setup
- [ ] Create SecureLoggingService
- [ ] Implement log levels
- [ ] Add sensitive data filtering
- [ ] Setup log rotation

### Phase 2: Integration
- [ ] Add to all services
- [ ] Replace print() with logger
- [ ] Add context to all logs
- [ ] Test in all environments

### Phase 3: Remote Logging
- [ ] Setup Firebase Crashlytics
- [ ] Implement batch sending
- [ ] Add retry logic
- [ ] Configure alerts

### Phase 4: Monitoring
- [ ] Setup error rate monitoring
- [ ] Create logging dashboard
- [ ] Configure alert thresholds
- [ ] Document log analysis

---

## 🎯 Success Criteria

- [ ] Zero PII in logs
- [ ] All errors logged with context
- [ ] Log rotation working
- [ ] Remote logging functional
- [ ] Alerts firing correctly
- [ ] Performance impact <1%

---

**Status**: 📝 IMPLEMENTATION GUIDE READY
**Priority**: 🟡 HIGH
**Security**: 🔒 CRITICAL
**Est. Time**: 1-2 days
