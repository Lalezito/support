# 🔔 Sistema de Notificaciones Diarias - Diagnóstico Completo

## 📊 **PROBLEMA IDENTIFICADO**

Las notificaciones diarias del horóscopo **NO se están enviando automáticamente** porque:

### 1. ✅ **Firebase & FCM - Configurado Correctamente**
- Firebase Cloud Messaging está inicializado ✅
- Token FCM se registra correctamente en el backend ✅
- Permisos de notificaciones en iOS configurados ✅
- `Info.plist` tiene `NSUserNotificationsUsageDescription` ✅
- Background modes configurados para `remote-notification` ✅

### 2. ✅ **UnifiedNotificationService - Implementado**
- Servicio de notificaciones completo en [unified_notification_service.dart](zodiac_app/lib/services/unified_notification_service.dart) ✅
- Método `sendDailyHoroscopeNotification()` existe (línea 538-564) ✅
- Método `scheduleNotification()` para programar notificaciones futuras ✅

### 3. ❌ **PROBLEMA CRÍTICO: No hay programación automática**
- **NO existe un sistema que programe notificaciones diarias automáticamente**
- **NO hay ningún código que llame a `scheduleDailyHoroscope()` diariamente**
- **NO hay WorkManager o scheduler configurado**

---

## 🔧 **SOLUCIÓN: Crear Sistema de Notificaciones Diarias**

Necesitas implementar un sistema que:

1. **Programe notificaciones locales diarias** para el horóscopo
2. **Permita al usuario configurar la hora** preferida para recibir notificaciones
3. **Re-programe automáticamente** cada día

---

## 📝 **PASOS PARA IMPLEMENTAR**

### **Paso 1: Crear DailyHoroscopeNotificationScheduler**

Crear archivo: `lib/services/daily_horoscope_notification_scheduler.dart`

```dart
import 'package:timezone/timezone.dart' as tz;
import 'package:zodiac_app/services/unified_notification_service.dart';
import 'package:zodiac_app/services/preferences_service.dart';
import 'package:zodiac_app/utils/app_logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// 🌅 Servicio para programar notificaciones diarias de horóscopo
class DailyHoroscopeNotificationScheduler {
  static final DailyHoroscopeNotificationScheduler _instance =
    DailyHoroscopeNotificationScheduler._internal();
  factory DailyHoroscopeNotificationScheduler() => _instance;
  DailyHoroscopeNotificationScheduler._internal();

  final UnifiedNotificationService _notificationService = UnifiedNotificationService.instance;

  // Preferencias por defecto
  static const String _notificationEnabledKey = 'daily_horoscope_notification_enabled';
  static const String _notificationTimeKey = 'daily_horoscope_notification_time';
  static const int _defaultHour = 9; // 9 AM por defecto
  static const int _defaultMinute = 0;

  bool _isInitialized = false;
  SharedPreferences? _prefs;

  /// Inicializar el scheduler
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      _prefs = await SharedPreferences.getInstance();

      // Inicializar servicio de notificaciones
      await _notificationService.initialize();

      // Programar notificaciones si están habilitadas
      final isEnabled = _prefs?.getBool(_notificationEnabledKey) ?? true;
      if (isEnabled) {
        await scheduleDaily();
      }

      _isInitialized = true;
      AppLogger.info('✅ DailyHoroscopeNotificationScheduler initialized');
    } catch (e) {
      AppLogger.error('Failed to initialize DailyHoroscopeNotificationScheduler', e);
    }
  }

  /// Programar notificación diaria
  Future<void> scheduleDaily() async {
    if (!_isInitialized) await initialize();

    try {
      // Cancelar notificaciones previas
      await _notificationService.cancelNotification('daily_horoscope');

      // Obtener hora configurada
      final scheduledHour = _prefs?.getInt('${_notificationTimeKey}_hour') ?? _defaultHour;
      final scheduledMinute = _prefs?.getInt('${_notificationTimeKey}_minute') ?? _defaultMinute;

      // Obtener signo zodiacal del usuario
      final prefsService = PreferencesService.instance;
      final zodiacSign = prefsService.userZodiacSign ?? 'Aries';
      final userId = prefsService.userId;

      // Calcular próxima hora de notificación
      final now = DateTime.now();
      DateTime scheduledTime = DateTime(
        now.year,
        now.month,
        now.day,
        scheduledHour,
        scheduledMinute,
      );

      // Si la hora ya pasó hoy, programar para mañana
      if (scheduledTime.isBefore(now)) {
        scheduledTime = scheduledTime.add(Duration(days: 1));
      }

      // Crear request de notificación
      final request = NotificationRequest(
        id: 'daily_horoscope',
        title: '🌟 Your Daily Horoscope is Ready!',
        body: 'Discover what the stars have in store for you today, $zodiacSign.',
        category: NotificationCategory.horoscope,
        priority: NotificationPriority.normal,
        scheduledTime: scheduledTime,
        payload: {
          'userId': userId,
          'zodiacSign': zodiacSign,
          'type': 'daily_horoscope',
        },
        actions: [
          NotificationAction(id: 'open_horoscope', title: 'Read Now'),
          NotificationAction(id: 'dismiss', title: 'Later'),
        ],
      );

      // Programar notificación
      final success = await _notificationService.scheduleNotification(request);

      if (success) {
        AppLogger.info('✅ Daily horoscope notification scheduled for $scheduledTime');
      } else {
        AppLogger.warning('⚠️ Failed to schedule daily horoscope notification');
      }

    } catch (e) {
      AppLogger.error('Error scheduling daily horoscope notification', e);
    }
  }

  /// Habilitar/deshabilitar notificaciones diarias
  Future<void> setEnabled(bool enabled) async {
    await _prefs?.setBool(_notificationEnabledKey, enabled);

    if (enabled) {
      await scheduleDaily();
    } else {
      await _notificationService.cancelNotification('daily_horoscope');
    }

    AppLogger.info('Daily horoscope notifications ${enabled ? "enabled" : "disabled"}');
  }

  /// Configurar hora de notificación
  Future<void> setNotificationTime(int hour, int minute) async {
    await _prefs?.setInt('${_notificationTimeKey}_hour', hour);
    await _prefs?.setInt('${_notificationTimeKey}_minute', minute);

    // Re-programar con nueva hora
    await scheduleDaily();

    AppLogger.info('Notification time updated to $hour:$minute');
  }

  /// Obtener si las notificaciones están habilitadas
  bool get isEnabled => _prefs?.getBool(_notificationEnabledKey) ?? true;

  /// Obtener hora configurada
  Map<String, int> get scheduledTime => {
    'hour': _prefs?.getInt('${_notificationTimeKey}_hour') ?? _defaultHour,
    'minute': _prefs?.getInt('${_notificationTimeKey}_minute') ?? _defaultMinute,
  };
}
```

---

### **Paso 2: Inicializar en main.dart**

Agregar en `main.dart` en la sección de inicialización:

```dart
// En la función de inicialización paralela, agregar:
await _initializeDailyNotifications(),

// Y crear la función:
Future<String> _initializeDailyNotifications() async {
  try {
    final scheduler = DailyHoroscopeNotificationScheduler();
    await scheduler.initialize();
    return '✅ Daily horoscope notifications scheduled';
  } catch (e) {
    return '⚠️ Daily notifications failed: $e';
  }
}
```

---

### **Paso 3: Agregar UI en Settings para configurar**

En `lib/screens/settings_screen.dart`, agregar sección de notificaciones:

```dart
// Agregar en la lista de settings
_buildNotificationSettings(),

// Y crear el método:
Widget _buildNotificationSettings() {
  final scheduler = DailyHoroscopeNotificationScheduler();
  final currentTime = scheduler.scheduledTime;

  return Column(
    children: [
      SwitchListTile(
        title: Text('📱 Daily Horoscope Notifications'),
        subtitle: Text('Receive your horoscope at ${currentTime['hour']}:${currentTime['minute'].toString().padLeft(2, '0')}'),
        value: scheduler.isEnabled,
        onChanged: (value) async {
          await scheduler.setEnabled(value);
          setState(() {});
        },
      ),
      ListTile(
        title: Text('⏰ Notification Time'),
        subtitle: Text('${currentTime['hour']}:${currentTime['minute'].toString().padLeft(2, '0')}'),
        trailing: Icon(Icons.chevron_right),
        onTap: () async {
          final time = await showTimePicker(
            context: context,
            initialTime: TimeOfDay(
              hour: currentTime['hour']!,
              minute: currentTime['minute']!,
            ),
          );

          if (time != null) {
            await scheduler.setNotificationTime(time.hour, time.minute);
            setState(() {});
          }
        },
      ),
    ],
  );
}
```

---

## 🧪 **TESTING**

### Test Manual Inmediato:
```dart
// Agregar botón temporal en Settings para probar:
ElevatedButton(
  onPressed: () async {
    final scheduler = DailyHoroscopeNotificationScheduler();
    // Programar para dentro de 1 minuto
    final now = DateTime.now().add(Duration(minutes: 1));
    await scheduler.setNotificationTime(now.hour, now.minute);
  },
  child: Text('🧪 Test Notification (1 min)'),
)
```

---

## 📋 **CHECKLIST DE VERIFICACIÓN**

- [ ] Crear `DailyHoroscopeNotificationScheduler`
- [ ] Agregar inicialización en `main.dart`
- [ ] Agregar UI en Settings
- [ ] Probar notificación de prueba (1 minuto)
- [ ] Verificar que aparezca la notificación
- [ ] Probar cambio de hora
- [ ] Probar habilitar/deshabilitar

---

## 🔍 **DIAGNÓSTICO ADICIONAL**

Si después de implementar esto NO funcionan las notificaciones, verificar:

1. **Permisos de iOS:**
   ```bash
   Settings → Zodiac Life Coach → Notifications
   # Verificar que están habilitados
   ```

2. **Logs en Xcode:**
   ```
   Window → Devices and Simulators → Open Console
   # Buscar errores de notificaciones
   ```

3. **Backend FCM:**
   - Verificar que el backend envía notificaciones push correctamente
   - Revisar logs de Railway

4. **Timezone:**
   ```dart
   import 'package:timezone/data/latest.dart' as tz;
   tz.initializeTimeZones(); // Ya está en main.dart línea 299
   ```

---

## 📊 **ARQUITECTURA ACTUAL vs NECESARIA**

### ❌ **Estado Actual:**
```
Usuario → App → Backend FCM Token ✅
                     ↓
                 (Nada más pasa)
```

### ✅ **Estado Necesario:**
```
Usuario → App → Scheduler → Notificaciones Locales Diarias
                                   ↓
                            (8:00 AM cada día)
                                   ↓
                            "Your Daily Horoscope!"
```

---

## 🎯 **RESULTADO ESPERADO**

Después de implementar:
1. Usuario abre Settings
2. Ve opción "Daily Horoscope Notifications" ✅
3. Puede configurar hora preferida ⏰
4. Cada día a esa hora recibe: **"🌟 Your Daily Horoscope is Ready!"**
5. Al tocar la notificación → Abre la app en HomeScreen

---

**Fecha de Diagnóstico:** 2025-11-18
**Estado:** Problema identificado, solución propuesta
**Prioridad:** Alta - Feature esperada por usuarios
