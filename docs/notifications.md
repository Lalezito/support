# Notification System Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: ✅ Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [API Reference](#api-reference)
4. [Usage Examples](#usage-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Overview

The Zodiac Life Coach notification system provides intelligent, personalized notifications for daily horoscopes and cosmic predictions. The system is built on two main services:

- **UnifiedNotificationService**: Core notification scheduling and management
- **PredictionNotificationService**: Prediction-based notifications with cosmic timing

### Key Features

✅ Daily horoscope notifications with customizable timing
✅ Prediction-based notifications with optimal cosmic windows
✅ Deep linking to specific app sections
✅ Timezone-aware scheduling
✅ Persistent notification preferences
✅ Full permission handling flow
✅ iOS and Android support

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────┐
│           User Interface Layer                   │
│  ┌─────────────┐      ┌──────────────────┐     │
│  │  Settings   │      │  Notification    │     │
│  │   Screen    │      │    Handler       │     │
│  └──────┬──────┘      └────────┬─────────┘     │
│         │                      │               │
└─────────┼──────────────────────┼───────────────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────────────┐
│        Service Layer                             │
│  ┌──────────────────────────────────────────┐  │
│  │  UnifiedNotificationService              │  │
│  │  - Schedule management                   │  │
│  │  - Permission handling                   │  │
│  │  - Deep linking                          │  │
│  └──────────────┬───────────────────────────┘  │
│                 │                               │
│  ┌──────────────▼───────────────────────────┐  │
│  │  PredictionNotificationService           │  │
│  │  - Cosmic timing calculation             │  │
│  │  - Prediction-based scheduling           │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│        Platform Layer                            │
│  ┌─────────────────┐  ┌──────────────────────┐ │
│  │  flutter_local  │  │  Permission Handler  │ │
│  │  _notifications │  │                      │ │
│  └─────────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction** → Settings screen enables notifications
2. **Permission Request** → UnifiedNotificationService requests OS permission
3. **Schedule Creation** → Service schedules notification with platform
4. **Persistence** → Preferences saved to SharedPreferences
5. **Delivery** → OS delivers notification at scheduled time
6. **Deep Link** → User taps notification → Opens specific app section

---

## API Reference

### UnifiedNotificationService

The main service for notification management.

#### Methods

##### `initialize()`

Initializes the notification system with configuration.

```dart
Future<void> initialize()
```

**Returns**: `Future<void>`

**Example**:
```dart
final notificationService = UnifiedNotificationService();
await notificationService.initialize();
```

---

##### `requestPermission()`

Requests notification permission from the user. Modern API.

```dart
Future<bool> requestPermission()
```

**Returns**: `Future<bool>` - `true` if permission granted, `false` otherwise

**Example**:
```dart
final granted = await notificationService.requestPermission();
if (granted) {
  print('Notifications enabled!');
} else {
  print('User denied notifications');
}
```

**Platform Notes**:
- iOS: Shows system permission dialog
- Android: Permissions granted by default on API <33, requires explicit grant on API 33+

---

##### `scheduleDailyNotification()`

Schedules a daily repeating notification for horoscope updates.

```dart
Future<void> scheduleDailyNotification({
  required int hour,
  required int minute,
  String? customMessage,
})
```

**Parameters**:
- `hour` (int, required): Hour in 24-hour format (0-23)
- `minute` (int, required): Minute (0-59)
- `customMessage` (String?, optional): Custom notification message

**Example**:
```dart
// Schedule daily horoscope at 9:00 AM
await notificationService.scheduleDailyNotification(
  hour: 9,
  minute: 0,
  customMessage: 'Your cosmic guidance awaits! ✨',
);
```

**Behavior**:
- Creates a daily repeating notification
- Respects timezone changes
- Persists across app restarts
- Notification ID: 0 (daily notification ID)

---

##### `cancelNotification()`

Cancels a specific notification by ID.

```dart
Future<void> cancelNotification(int id)
```

**Parameters**:
- `id` (int, required): Notification ID to cancel

**Example**:
```dart
// Cancel daily notification
await notificationService.cancelNotification(0);
```

---

##### `cancelAllNotifications()`

Cancels all scheduled notifications.

```dart
Future<void> cancelAllNotifications()
```

**Example**:
```dart
await notificationService.cancelAllNotifications();
```

---

##### `getPendingNotifications()`

Gets all pending notification requests.

```dart
Future<List<PendingNotificationRequest>> getPendingNotifications()
```

**Returns**: `Future<List<PendingNotificationRequest>>`

**Example**:
```dart
final pending = await notificationService.getPendingNotifications();
print('You have ${pending.length} pending notifications');
```

---

### PredictionNotificationService

Service for prediction-based notifications with cosmic timing.

#### Methods

##### `schedulePredictionNotification()`

Schedules a notification for a cosmic prediction.

```dart
Future<void> schedulePredictionNotification({
  required String predictionId,
  required DateTime idealTime,
  required String title,
  required String body,
  String? payload,
})
```

**Parameters**:
- `predictionId` (String, required): Unique identifier for the prediction
- `idealTime` (DateTime, required): Cosmically optimal time to deliver
- `title` (String, required): Notification title
- `body` (String, required): Notification body text
- `payload` (String?, optional): Deep link payload

**Example**:
```dart
final predictionService = PredictionNotificationService();

await predictionService.schedulePredictionNotification(
  predictionId: 'full_moon_ritual_2025_10',
  idealTime: DateTime(2025, 10, 15, 22, 30), // 10:30 PM on full moon
  title: 'Full Moon Ritual Reminder',
  body: 'The cosmic energy is perfect for your manifestation ritual',
  payload: 'zodiac://predictions/full_moon_ritual',
);
```

---

## Usage Examples

### Example 1: Enable Daily Horoscope Notifications

```dart
class NotificationSettingsScreen extends StatefulWidget {
  @override
  _NotificationSettingsScreenState createState() =>
    _NotificationSettingsScreenState();
}

class _NotificationSettingsScreenState extends State<NotificationSettingsScreen> {
  final _notificationService = UnifiedNotificationService();
  bool _notificationsEnabled = false;
  TimeOfDay _selectedTime = TimeOfDay(hour: 9, minute: 0);

  @override
  void initState() {
    super.initState();
    _initNotifications();
  }

  Future<void> _initNotifications() async {
    await _notificationService.initialize();
    // Load saved preferences
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _notificationsEnabled = prefs.getBool('notifications_enabled') ?? false;
    });
  }

  Future<void> _toggleNotifications(bool enabled) async {
    if (enabled) {
      // Request permission
      final granted = await _notificationService.requestPermission();

      if (granted) {
        // Schedule daily notification
        await _notificationService.scheduleDailyNotification(
          hour: _selectedTime.hour,
          minute: _selectedTime.minute,
        );

        // Save preference
        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('notifications_enabled', true);

        setState(() => _notificationsEnabled = true);
      } else {
        // Show permission denied dialog
        _showPermissionDeniedDialog();
      }
    } else {
      // Disable notifications
      await _notificationService.cancelAllNotifications();

      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('notifications_enabled', false);

      setState(() => _notificationsEnabled = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Notification Settings')),
      body: Column(
        children: [
          SwitchListTile(
            title: Text('Daily Horoscope'),
            subtitle: Text('Receive your daily cosmic guidance'),
            value: _notificationsEnabled,
            onChanged: _toggleNotifications,
          ),
          if (_notificationsEnabled)
            ListTile(
              title: Text('Notification Time'),
              subtitle: Text('${_selectedTime.format(context)}'),
              onTap: _selectTime,
            ),
        ],
      ),
    );
  }

  Future<void> _selectTime() async {
    final picked = await showTimePicker(
      context: context,
      initialTime: _selectedTime,
    );

    if (picked != null) {
      setState(() => _selectedTime = picked);

      // Update notification schedule
      await _notificationService.scheduleDailyNotification(
        hour: picked.hour,
        minute: picked.minute,
      );
    }
  }

  void _showPermissionDeniedDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Permission Required'),
        content: Text(
          'Please enable notifications in your device settings to receive daily horoscopes.'
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // Open app settings
              // Note: Requires permission_handler package
            },
            child: Text('Settings'),
          ),
        ],
      ),
    );
  }
}
```

---

### Example 2: Handle Notification Tap (Deep Linking)

```dart
class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _notificationService = UnifiedNotificationService();

  @override
  void initState() {
    super.initState();
    _setupNotificationHandling();
  }

  Future<void> _setupNotificationHandling() async {
    await _notificationService.initialize();

    // Handle notification tap when app is in foreground/background
    _notificationService.onNotificationTap((payload) {
      if (payload != null) {
        _handleDeepLink(payload);
      }
    });

    // Handle notification tap when app was terminated
    final launchDetails = await _notificationService.getNotificationAppLaunchDetails();
    if (launchDetails?.didNotificationLaunchApp ?? false) {
      final payload = launchDetails!.notificationResponse?.payload;
      if (payload != null) {
        _handleDeepLink(payload);
      }
    }
  }

  void _handleDeepLink(String payload) {
    // Parse payload
    final uri = Uri.parse(payload);

    switch (uri.host) {
      case 'horoscope':
        // Navigate to horoscope screen
        Navigator.pushNamed(context, '/horoscope');
        break;

      case 'predictions':
        // Navigate to specific prediction
        final predictionId = uri.pathSegments.first;
        Navigator.pushNamed(
          context,
          '/predictions/$predictionId',
        );
        break;

      case 'coach':
        // Navigate to AI cosmic coach
        Navigator.pushNamed(context, '/coach');
        break;

      default:
        // Navigate to home
        Navigator.pushNamed(context, '/home');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Your app configuration
    );
  }
}
```

---

## Best Practices

### 1. Permission Handling

Always check and request permission before scheduling notifications:

```dart
// ✅ Good
final granted = await notificationService.requestPermission();
if (granted) {
  await notificationService.scheduleDailyNotification(...);
}

// ❌ Bad - Will fail silently if permission not granted
await notificationService.scheduleDailyNotification(...);
```

### 2. Persistence

Always persist notification preferences:

```dart
// ✅ Good
final prefs = await SharedPreferences.getInstance();
await prefs.setBool('notifications_enabled', true);
await prefs.setInt('notification_hour', 9);
await prefs.setInt('notification_minute', 0);

// ❌ Bad - Settings lost on app restart
// No persistence
```

### 3. User Feedback

Provide clear feedback when notifications are enabled/disabled:

```dart
// ✅ Good
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text('Daily horoscope notifications enabled!')),
);

// ❌ Bad - No user feedback
// Silent enable/disable
```

### 4. Timezone Handling

The system automatically handles timezone changes, but test edge cases:

```dart
// Test scenarios:
// - User travels to different timezone
// - Daylight saving time transitions
// - System timezone change
```

### 5. Notification Content

Keep notifications concise and actionable:

```dart
// ✅ Good
title: 'Your Daily Horoscope',
body: 'Cosmic guidance for Aries awaits! ✨'

// ❌ Bad - Too long
title: 'Your personalized astrological guidance based on your zodiac sign',
body: 'We have calculated your daily horoscope based on the current planetary alignments and cosmic energies specific to your sun sign...'
```

---

## Troubleshooting

### Issue: Notifications not appearing

**Possible causes**:
1. Permission not granted
2. Notification cancelled
3. System notification settings disabled

**Solution**:
```dart
// Check permission
final granted = await notificationService.requestPermission();
print('Permission granted: $granted');

// Check pending notifications
final pending = await notificationService.getPendingNotifications();
print('Pending notifications: ${pending.length}');

// Check system settings
// Guide user to Settings → Notifications → Zodiac Life Coach
```

---

### Issue: Notifications fire at wrong time

**Possible causes**:
1. Timezone mismatch
2. 12-hour vs 24-hour format confusion
3. Notification rescheduled incorrectly

**Solution**:
```dart
// Always use 24-hour format
await notificationService.scheduleDailyNotification(
  hour: 21, // 9 PM (not 9)
  minute: 0,
);

// Verify scheduled time
final pending = await notificationService.getPendingNotifications();
for (final notification in pending) {
  print('Scheduled: ${notification.id} at ${notification.scheduledDate}');
}
```

---

### Issue: Deep links not working

**Possible causes**:
1. Payload not set
2. Deep link handler not initialized
3. Invalid URI format

**Solution**:
```dart
// Ensure payload is set
await notificationService.scheduleDailyNotification(
  hour: 9,
  minute: 0,
  payload: 'zodiac://horoscope/daily', // ✅
);

// Validate URI format
final uri = Uri.parse(payload);
print('Host: ${uri.host}, Path: ${uri.path}');

// Initialize handler early
@override
void initState() {
  super.initState();
  _setupNotificationHandling(); // Call this ASAP
}
```

---

### Issue: Notifications disappear after app update

**Possible causes**:
1. Notification ID changed
2. Preferences not migrated
3. Notification system reinitialized

**Solution**:
```dart
// Use consistent notification IDs
static const int DAILY_NOTIFICATION_ID = 0;
static const int PREDICTION_NOTIFICATION_BASE_ID = 1000;

// Migrate preferences on app update
Future<void> migrateNotificationPreferences() async {
  final prefs = await SharedPreferences.getInstance();
  final version = prefs.getInt('app_version') ?? 0;

  if (version < 2) {
    // Reschedule all notifications with new system
    await _rescheduleAllNotifications();
    await prefs.setInt('app_version', 2);
  }
}
```

---

## Performance Considerations

- **Scheduling overhead**: ~10ms per notification
- **Permission request**: User interaction required (can be slow)
- **Deep link handling**: <50ms typical
- **Battery impact**: Minimal (system-managed)

---

## Platform-Specific Notes

### iOS
- Requires notification permission request
- Supports rich notifications with images
- Can customize notification sounds
- Provisional authorization available

### Android
- Permissions auto-granted on API <33
- Notification channels required (API 26+)
- Can create notification importance levels
- Battery optimization may affect delivery

---

**For support**: Contact dev team
**For bugs**: See GitHub issues
**For features**: See product roadmap
