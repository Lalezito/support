# 🚀 DEPLOYMENT MASTER GUIDE

**Objetivo**: Deployment seguro y controlado a producción
**Prioridad**: CRÍTICA
**Fecha**: 2025-10-05

---

## 📋 Table of Contents

1. [Feature Flags System](#feature-flags-system)
2. [Data Migration Strategy](#data-migration-strategy)
3. [Backup Strategy](#backup-strategy)
4. [Deployment Checklist](#deployment-checklist)
5. [Rollback Plan](#rollback-plan)

---

## 🎚️ Feature Flags System

### Overview

Feature flags allow gradual rollout of new features and provide kill switches for emergency rollbacks.

### Implementation

**File**: `lib/services/feature_flag_service.dart`

```dart
import 'package:firebase_remote_config/firebase_remote_config.dart';

class FeatureFlags {
  static final FeatureFlags _instance = FeatureFlags._internal();
  factory FeatureFlags() => _instance;
  FeatureFlags._internal();

  late FirebaseRemoteConfig _remoteConfig;
  bool _initialized = false;

  // Local defaults (can be overridden by remote config)
  static const Map<String, bool> _defaults = {
    // Core features (stable)
    'enable_smart_journaling': true,
    'enable_offline_mode': true,
    'enable_enhanced_analytics': true,

    // Premium features
    'enable_cosmic_vip_tier': true,
    'enable_lifetime_purchase': true,

    // New features (gradual rollout)
    'enable_predictive_transits': false,
    'enable_ai_coach_v2': false,
    'enable_neural_compatibility': false,

    // Emergency kill switches
    'enable_purchase_flow': true,
    'enable_trial_activation': true,
    'enable_backend_api': true,
  };

  Future<void> initialize() async {
    if (_initialized) return;

    _remoteConfig = FirebaseRemoteConfig.instance;

    // Set defaults
    await _remoteConfig.setDefaults(_defaults);

    // Configure fetch settings
    await _remoteConfig.setConfigSettings(
      RemoteConfigSettings(
        fetchTimeout: Duration(seconds: 10),
        minimumFetchInterval: Duration(hours: 1),
      ),
    );

    // Fetch and activate
    await _remoteConfig.fetchAndActivate();

    _initialized = true;

    SecureLoggingService().info('Feature flags initialized', context: {
      'flags_count': _defaults.length,
      'remote_config_active': true,
    });
  }

  bool isEnabled(String feature) {
    if (!_initialized) {
      SecureLoggingService().warning(
        'Feature flags not initialized, using default'
      );
      return _defaults[feature] ?? false;
    }

    return _remoteConfig.getBool(feature);
  }

  // Typed getters for common features
  bool get smartJournalingEnabled => isEnabled('enable_smart_journaling');
  bool get offlineModeEnabled => isEnabled('enable_offline_mode');
  bool get aiCoachV2Enabled => isEnabled('enable_ai_coach_v2');
  bool get cosmicVipTierEnabled => isEnabled('enable_cosmic_vip_tier');
  bool get purchaseFlowEnabled => isEnabled('enable_purchase_flow');

  // Force refresh (for testing/debugging)
  Future<void> forceRefresh() async {
    await _remoteConfig.fetch();
    await _remoteConfig.activate();
  }
}
```

### Usage

```dart
// In features
if (FeatureFlags().smartJournalingEnabled) {
  // Show smart journaling feature
} else {
  // Show "coming soon" or hide feature
}

// Emergency kill switch
if (!FeatureFlags().purchaseFlowEnabled) {
  return Text('Purchases temporarily unavailable. Please try again later.');
}
```

### Firebase Remote Config Setup

**Dashboard**: Firebase Console → Remote Config

**Config Example**:
```json
{
  "enable_smart_journaling": true,
  "enable_ai_coach_v2": false,
  "enable_neural_compatibility": false,
  "enable_purchase_flow": true
}
```

**Conditions** for gradual rollout:
```
Name: beta_users
Condition: User in audiences → Beta Users
Value: enable_ai_coach_v2 = true

Name: gradual_rollout_25
Condition: User in random percentile → 0-25%
Value: enable_neural_compatibility = true
```

---

## 💾 Data Migration Strategy

### Overview

Migrations ensure smooth transitions between app versions without data loss.

### Implementation

**File**: `lib/services/migration_service.dart`

```dart
class MigrationService {
  static final MigrationService _instance = MigrationService._internal();
  factory MigrationService() => _instance;
  MigrationService._internal();

  static const String _versionKey = 'app_data_version';

  Future<void> runMigrations() async {
    final prefs = await SharedPreferences.getInstance();
    final currentVersion = prefs.getInt(_versionKey) ?? 0;
    final targetVersion = 3; // Increment with each schema change

    SecureLoggingService().info('Running migrations', context: {
      'current_version': currentVersion,
      'target_version': targetVersion,
    });

    if (currentVersion < targetVersion) {
      for (var version = currentVersion + 1; version <= targetVersion; version++) {
        await _runMigration(version);
      }

      await prefs.setInt(_versionKey, targetVersion);

      SecureLoggingService().info('Migrations completed', context: {
        'new_version': targetVersion,
      });
    }
  }

  Future<void> _runMigration(int version) async {
    SecureLoggingService().info('Running migration', context: {'version': version});

    switch (version) {
      case 1:
        await _migrateToV1();
        break;
      case 2:
        await _migrateToV2();
        break;
      case 3:
        await _migrateToV3();
        break;
      default:
        SecureLoggingService().warning('Unknown migration version: $version');
    }
  }

  // V1: Add user identity
  Future<void> _migrateToV1() async {
    final prefs = await SharedPreferences.getInstance();

    if (!prefs.containsKey('user_id')) {
      final userId = Uuid().v4();
      await prefs.setString('user_id', userId);

      analytics.logEvent('migration_v1_completed', {
        'user_id_created': true,
      });
    }
  }

  // V2: Migrate old cache format to new format
  Future<void> _migrateToV2() async {
    final prefs = await SharedPreferences.getInstance();

    // Old format: horoscope_Aries_20251005
    // New format: horoscope_daily_Aries_2025-10-05

    final keys = prefs.getKeys().where((key) => key.startsWith('horoscope_'));

    for (final oldKey in keys) {
      if (!oldKey.contains('_daily_') && !oldKey.contains('_weekly_')) {
        final value = prefs.get(oldKey);
        final parts = oldKey.split('_');

        if (parts.length == 3) {
          final sign = parts[1];
          final date = parts[2];
          final newKey = 'horoscope_daily_${sign}_$date';

          await prefs.setString(newKey, value.toString());
          await prefs.remove(oldKey);
        }
      }
    }

    analytics.logEvent('migration_v2_completed', {
      'cache_keys_migrated': keys.length,
    });
  }

  // V3: Migrate subscription data to RevenueCat format
  Future<void> _migrateToV3() async {
    final prefs = await SharedPreferences.getInstance();

    // Old format: premium_status, premium_tier
    // New format: subscription_type, subscription_active

    final oldStatus = prefs.getBool('premium_status');
    final oldTier = prefs.getString('premium_tier');

    if (oldStatus != null && oldTier != null) {
      // Map old tier names to new enum
      final tierMap = {
        'basic': 'essential',
        'pro': 'advanced',
        'premium': 'master',
      };

      final newTier = tierMap[oldTier] ?? oldTier;

      await prefs.setString('subscription_type', newTier);
      await prefs.setBool('subscription_active', oldStatus);

      // Remove old keys
      await prefs.remove('premium_status');
      await prefs.remove('premium_tier');

      analytics.logEvent('migration_v3_completed', {
        'old_tier': oldTier,
        'new_tier': newTier,
      });
    }
  }
}
```

### Migration Testing

```dart
// test/services/migration_service_test.dart

void main() {
  group('MigrationService', () {
    test('migrates from v0 to v3', () async {
      // Setup old data
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('premium_tier', 'basic');
      await prefs.setBool('premium_status', true);

      // Run migration
      await MigrationService().runMigrations();

      // Verify new data
      expect(prefs.getString('subscription_type'), 'essential');
      expect(prefs.getBool('subscription_active'), true);

      // Verify old data removed
      expect(prefs.getString('premium_tier'), isNull);
    });
  });
}
```

---

## 📦 Backup Strategy

### Overview

Automatic backups protect user data during migrations and provide restore capability.

### Implementation

**File**: `lib/services/backup_service.dart`

```dart
import 'dart:convert';
import 'package:path_provider/path_provider.dart';

class BackupManifest {
  final DateTime timestamp;
  final String version;
  final Map<String, dynamic> data;

  BackupManifest({
    required this.timestamp,
    required this.version,
    required this.data,
  });

  Map<String, dynamic> toJson() => {
    'timestamp': timestamp.toIso8601String(),
    'version': version,
    'data': data,
  };

  factory BackupManifest.fromJson(Map<String, dynamic> json) => BackupManifest(
    timestamp: DateTime.parse(json['timestamp']),
    version: json['version'],
    data: json['data'],
  );
}

class BackupService {
  static final BackupService _instance = BackupService._internal();
  factory BackupService() => _instance;
  BackupService._internal();

  Future<BackupManifest> createBackup() async {
    SecureLoggingService().info('Creating backup');

    final packageInfo = await PackageInfo.fromPlatform();

    final backup = BackupManifest(
      timestamp: DateTime.now(),
      version: packageInfo.version,
      data: {
        'preferences': await _backupPreferences(),
        'secure_storage': await _backupSecureStorage(),
        'databases': await _backupDatabases(),
      },
    );

    await _saveBackupToFile(backup);

    analytics.logEvent('backup_created', {
      'version': backup.version,
      'data_size_kb': jsonEncode(backup.data).length / 1024,
    });

    return backup;
  }

  Future<Map<String, dynamic>> _backupPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys();

    final backup = <String, dynamic>{};
    for (final key in keys) {
      final value = prefs.get(key);
      backup[key] = value;
    }

    return backup;
  }

  Future<Map<String, dynamic>> _backupSecureStorage() async {
    final storage = FlutterSecureStorage();

    final backup = <String, dynamic>{};
    final allValues = await storage.readAll();

    for (final entry in allValues.entries) {
      backup[entry.key] = entry.value;
    }

    return backup;
  }

  Future<Map<String, dynamic>> _backupDatabases() async {
    // Backup Hive boxes
    final boxes = Hive.openedBoxes;
    final backup = <String, dynamic>{};

    for (final box in boxes) {
      backup[box.name] = box.toMap();
    }

    return backup;
  }

  Future<void> _saveBackupToFile(BackupManifest backup) async {
    final directory = await getApplicationDocumentsDirectory();
    final backupDir = Directory('${directory.path}/backups');

    if (!await backupDir.exists()) {
      await backupDir.create(recursive: true);
    }

    final filename = 'backup_${backup.timestamp.millisecondsSinceEpoch}.json';
    final file = File('${backupDir.path}/$filename');

    await file.writeAsString(jsonEncode(backup.toJson()));

    SecureLoggingService().info('Backup saved', context: {
      'path': file.path,
      'size_kb': await file.length() / 1024,
    });

    // Cleanup old backups (keep last 5)
    await _cleanupOldBackups(backupDir);
  }

  Future<void> _cleanupOldBackups(Directory backupDir) async {
    final files = backupDir.listSync()
      .whereType<File>()
      .where((f) => f.path.endsWith('.json'))
      .toList();

    if (files.length > 5) {
      files.sort((a, b) => a.path.compareTo(b.path));

      for (var i = 0; i < files.length - 5; i++) {
        await files[i].delete();
      }
    }
  }

  Future<void> restoreFromBackup(BackupManifest backup) async {
    SecureLoggingService().info('Restoring from backup', context: {
      'backup_version': backup.version,
      'backup_timestamp': backup.timestamp.toIso8601String(),
    });

    try {
      // Restore preferences
      await _restorePreferences(backup.data['preferences']);

      // Restore secure storage
      await _restoreSecureStorage(backup.data['secure_storage']);

      // Restore databases
      await _restoreDatabases(backup.data['databases']);

      analytics.logEvent('backup_restored', {
        'version': backup.version,
        'success': true,
      });

      SecureLoggingService().info('Backup restored successfully');
    } catch (e, stack) {
      SecureLoggingService().error(
        'Failed to restore backup',
        error: e,
        stackTrace: stack,
      );

      analytics.logEvent('backup_restored', {
        'version': backup.version,
        'success': false,
        'error': e.toString(),
      });

      rethrow;
    }
  }

  Future<void> _restorePreferences(Map<String, dynamic> data) async {
    final prefs = await SharedPreferences.getInstance();

    for (final entry in data.entries) {
      if (entry.value is String) {
        await prefs.setString(entry.key, entry.value);
      } else if (entry.value is bool) {
        await prefs.setBool(entry.key, entry.value);
      } else if (entry.value is int) {
        await prefs.setInt(entry.key, entry.value);
      } else if (entry.value is double) {
        await prefs.setDouble(entry.key, entry.value);
      }
    }
  }

  Future<void> _restoreSecureStorage(Map<String, dynamic> data) async {
    final storage = FlutterSecureStorage();

    for (final entry in data.entries) {
      await storage.write(key: entry.key, value: entry.value.toString());
    }
  }

  Future<void> _restoreDatabases(Map<String, dynamic> data) async {
    for (final entry in data.entries) {
      final boxName = entry.key;
      final boxData = entry.value as Map<String, dynamic>;

      final box = await Hive.openBox(boxName);
      await box.clear();
      await box.putAll(boxData);
    }
  }
}
```

### Automatic Backup Before Migration

```dart
// In main.dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Create backup before migrations
  await BackupService().createBackup();

  // Run migrations
  try {
    await MigrationService().runMigrations();
  } catch (e, stack) {
    SecureLoggingService().critical(
      'Migration failed, attempting restore',
      error: e,
      stackTrace: stack,
    );

    // Restore from latest backup
    // (Implementation would load latest backup and restore)
  }

  runApp(MyApp());
}
```

---

## ✅ Deployment Checklist

### Pre-Deployment (1 day before)

#### Code Quality
- [ ] All Phases 1-8 completed and documented
- [ ] Zero critical bugs in issue tracker
- [ ] Code review completed and approved
- [ ] No TODO comments in production code

#### Testing
- [ ] Unit test coverage >= 75% (verified in CI)
- [ ] Integration tests passing 100%
- [ ] Regression tests passing 100%
- [ ] Manual QA testing completed
- [ ] Premium flows tested end-to-end
- [ ] Offline mode tested thoroughly

#### Performance
- [ ] App startup time <2s (measured)
- [ ] Screen load times <1s (measured)
- [ ] API latency <2s (monitored)
- [ ] Memory usage <200MB (profiled)
- [ ] No memory leaks detected

#### Security
- [ ] Security audit completed
- [ ] No PII in logs (verified)
- [ ] API keys rotated if needed
- [ ] SSL pinning active (if applicable)
- [ ] Input validation complete

#### Infrastructure
- [ ] Backup of current production data created
- [ ] Feature flags configured in Firebase Remote Config
- [ ] Remote Config defaults set
- [ ] Monitoring dashboards prepared (Firebase, RevenueCat)
- [ ] Alert thresholds configured

---

### Deployment Day

#### Build
```bash
# iOS
flutter build ios --release --no-codesign
# Xcode: Archive and upload to App Store Connect

# Android
flutter build appbundle --release
# Upload to Google Play Console
```

- [ ] iOS build successful
- [ ] Android build successful
- [ ] Code signing verified (iOS)
- [ ] App signing verified (Android)
- [ ] Build artifacts backed up

#### TestFlight / Internal Testing
- [ ] Upload to TestFlight (iOS)
- [ ] Upload to Internal Testing (Android)
- [ ] Beta testing with 5% users
  - Target: 50-100 beta users
  - Duration: 24 hours
  - Monitor: crashes, errors, performance

#### Monitoring (24h Beta Period)
- [ ] Zero crashes (Firebase Crashlytics)
- [ ] Error rate <0.5%
- [ ] Performance within budgets
- [ ] Analytics events firing correctly
- [ ] Purchase flows working (test purchases)

---

### Gradual Rollout

#### Phase 1: 25% Rollout
- [ ] Enable 25% rollout in Play Console / App Store Connect
- [ ] Monitor for 24 hours
- [ ] Check metrics:
  - Crash rate <0.1%
  - Error rate <1%
  - Revenue stable or growing
  - User engagement stable

#### Phase 2: 50% Rollout
- [ ] Enable 50% rollout
- [ ] Monitor for 24 hours
- [ ] Same metric checks as Phase 1

#### Phase 3: 100% Rollout
- [ ] Enable 100% rollout
- [ ] Monitor for 48 hours
- [ ] Full metric validation

---

### Post-Deployment (48h after 100% rollout)

#### Monitoring
- [ ] Analytics data looks normal
- [ ] Revenue tracking accurate
- [ ] No spike in support tickets
- [ ] User reviews positive (>4.0 stars)

#### Documentation
- [ ] Update CHANGELOG.md with release notes
- [ ] Document any issues encountered
- [ ] Update runbook with learnings
- [ ] Create postmortem if needed

#### Communication
- [ ] Notify team of successful deployment
- [ ] Send release notes to stakeholders
- [ ] Update marketing materials if needed

---

## ⏮️ Rollback Plan

### Rollback Triggers

**Automatic Rollback**:
- Crash rate > 1.0%
- Error rate > 5.0%
- Revenue drop > 20% (compared to previous period)
- Security incident detected

**Manual Rollback**:
- Critical bug discovered
- Data corruption detected
- Major feature not working
- Stakeholder decision

---

### Immediate Actions (<5 minutes)

1. **Activate Kill Switch**
```
Firebase Remote Config → Enable kill switches for problem features
```

2. **Halt Rollout**
```
App Store Connect / Play Console → Pause phased release
```

3. **Disable Features**
```dart
// Set via Remote Config
enable_purchase_flow: false
enable_problematic_feature: false
```

4. **Notify Stakeholders**
```
Slack: #critical-alerts
Email: team@zodiac.com
```

---

### Full Rollback Procedure (< 30 minutes)

#### Step 1: Stop the Bleeding
- [ ] Halt all rollouts (iOS & Android)
- [ ] Enable all kill switches
- [ ] Disable problematic features via Remote Config

#### Step 2: Assess Damage
- [ ] Count affected users
- [ ] Identify root cause
- [ ] Estimate fix time

#### Step 3: Revert or Fix Forward?

**If quick fix (<1 hour)**:
- Create hotfix
- Test thoroughly
- Deploy via emergency release

**If complex fix (>1 hour)**:
- Revert to previous version
- Submit expedited review to stores
- Fix in next release

#### Step 4: Revert Procedure

**iOS**:
```
App Store Connect → My Apps → Zodiac
→ App Store → Remove from Sale (temporary)
→ Submit previous version for expedited review
```

**Android**:
```
Play Console → Rollback to previous release
(Immediate, no review needed)
```

#### Step 5: Communication
- [ ] User notification (in-app message)
- [ ] Support team briefing
- [ ] Stakeholder update
- [ ] Public statement (if needed)

---

### Recovery Validation

Before declaring rollback complete:

- [ ] Crash rate back to baseline (<0.1%)
- [ ] Error rate normal (<0.5%)
- [ ] Revenue stable
- [ ] User feedback improving
- [ ] Support tickets decreasing

---

### Postmortem

Within 48h of rollback:

1. **Root Cause Analysis**
   - What went wrong?
   - Why did it happen?
   - Why wasn't it caught in testing?

2. **Action Items**
   - Add test coverage
   - Improve monitoring
   - Update deployment checklist
   - Enhance rollback procedures

3. **Documentation**
   - Document incident timeline
   - Share learnings with team
   - Update runbooks

---

## 📊 Deployment Metrics

### Success Criteria

| Metric | Target | Alert If |
|--------|--------|----------|
| Crash-free rate | >99.9% | <99.0% |
| Error rate | <0.5% | >1.0% |
| App startup time | <2s | >3s |
| API latency (p95) | <2s | >5s |
| Purchase success rate | >95% | <90% |
| Revenue (vs prev period) | +/- 10% | -20% |

---

**Status**: 📝 GUIDE READY
**Priority**: 🔴 CRITICAL
**Owner**: DevOps Team
**Review Frequency**: Before each major release
