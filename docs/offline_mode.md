# Offline Mode Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: ✅ Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Cache Strategy](#cache-strategy)
4. [Synchronization](#synchronization)
5. [Conflict Resolution](#conflict-resolution)
6. [Performance Considerations](#performance-considerations)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The Zodiac Life Coach offline mode provides seamless app functionality even without internet connectivity. Users can access previously loaded content, create journal entries, and view cached data.

### Key Features

✅ Multi-layer caching (horoscopes, compatibility, birth charts)
✅ Automatic sync when connectivity restored
✅ Intelligent conflict resolution
✅ Cache cleanup with data preservation
✅ Offline indicators and user feedback
✅ Background sync support
✅ Data integrity guarantees

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │  Horoscope  │  │ Compatibility│  │   Journal    │   │
│  │   Screen    │  │    Screen    │  │   Screen     │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         OfflineModeService                       │  │
│  │  - Connectivity monitoring                       │  │
│  │  - Sync coordination                             │  │
│  │  - Cache management                              │  │
│  └────────┬─────────────────────────────────────────┘  │
│           │                                             │
│  ┌────────▼─────────┐  ┌───────────────────────────┐  │
│  │   CacheService   │  │   BackendService          │  │
│  │  - Read/Write    │  │  - API calls              │  │
│  │  - Expiration    │  │  - Data fetching          │  │
│  └──────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
          │                                │
          ▼                                ▼
┌─────────────────────────────────────────────────────────┐
│                  Storage Layer                           │
│  ┌──────────────────┐  ┌───────────────────────────┐   │
│  │ SharedPreferences│  │   Hive Database           │   │
│  │ - User prefs     │  │   - Structured data       │   │
│  │ - Simple cache   │  │   - Large datasets        │   │
│  └──────────────────┘  └───────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

#### Online Mode
```
User Request → Service → Backend API → Cache → Return Data
```

#### Offline Mode
```
User Request → Service → Cache Check → Return Cached Data
```

#### Sync Mode
```
Connectivity Restored → OfflineModeService → Sync Queue → Backend → Update Cache
```

---

## Cache Strategy

### Cache Types

#### 1. Horoscope Cache

**Daily Horoscopes**
- **Cache Key**: `horoscope_daily_{sign}_{date}`
- **TTL**: 24 hours
- **Storage**: SharedPreferences
- **Size**: ~2KB per sign

```dart
class HoroscopeCacheStrategy {
  static const String prefix = 'horoscope_daily_';
  static const Duration ttl = Duration(hours: 24);

  static String getCacheKey(String sign, DateTime date) {
    final dateStr = DateFormat('yyyy-MM-dd').format(date);
    return '${prefix}${sign}_$dateStr';
  }

  static bool isExpired(DateTime cachedTime) {
    return DateTime.now().difference(cachedTime) > ttl;
  }
}
```

**Weekly Horoscopes**
- **Cache Key**: `horoscope_weekly_{sign}_{week}`
- **TTL**: 7 days
- **Storage**: SharedPreferences
- **Size**: ~5KB per sign

**Monthly Horoscopes**
- **Cache Key**: `horoscope_monthly_{sign}_{month}`
- **TTL**: 30 days
- **Storage**: SharedPreferences
- **Size**: ~10KB per sign

---

#### 2. Compatibility Cache

**Compatibility Results**
- **Cache Key**: `compatibility_{sign1}_{sign2}`
- **TTL**: 12 hours (cosmic energies change)
- **Storage**: Hive Database
- **Size**: ~15KB per pair

```dart
class CompatibilityCacheStrategy {
  static String getCacheKey(String sign1, String sign2) {
    // Normalize order (Aries-Leo == Leo-Aries)
    final signs = [sign1, sign2]..sort();
    return 'compatibility_${signs[0]}_${signs[1]}';
  }

  static const Duration ttl = Duration(hours: 12);
}
```

---

#### 3. User Data Cache

**Birth Chart**
- **Cache Key**: `birth_chart_{userId}`
- **TTL**: No expiration (permanent)
- **Storage**: Hive Database
- **Size**: ~20KB

**Journal Entries**
- **Cache Key**: `journal_entries_{userId}`
- **TTL**: No expiration (permanent)
- **Storage**: Hive Database
- **Size**: Variable (10KB - 1MB)

**User Preferences**
- **Cache Key**: Various preference keys
- **TTL**: No expiration (permanent)
- **Storage**: SharedPreferences
- **Size**: ~5KB total

---

### Cache Invalidation

#### Time-Based Expiration

```dart
class CacheService {
  Future<bool> isCacheValid(String key) async {
    final prefs = await SharedPreferences.getInstance();
    final timestampStr = prefs.getString('${key}_timestamp');

    if (timestampStr == null) return false;

    final timestamp = DateTime.parse(timestampStr);
    final ttl = _getTTLForKey(key);

    return DateTime.now().difference(timestamp) < ttl;
  }

  Duration _getTTLForKey(String key) {
    if (key.startsWith('horoscope_daily_')) {
      return Duration(hours: 24);
    } else if (key.startsWith('horoscope_weekly_')) {
      return Duration(days: 7);
    } else if (key.startsWith('compatibility_')) {
      return Duration(hours: 12);
    }
    // No expiration for user data
    return Duration(days: 365 * 100);
  }
}
```

#### Manual Invalidation

```dart
// Clear specific cache
await cacheService.invalidate('horoscope_daily_Aries_2025-10-05');

// Clear all horoscopes
await cacheService.invalidateByPattern('horoscope_daily_*');

// Clear all cache (except user data)
await cacheService.clearAllCache(preserveUserData: true);
```

---

## Synchronization

### Connectivity Detection

```dart
class OfflineModeService {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<ConnectivityResult>? _subscription;

  bool _isOnline = true;
  bool get isOnline => _isOnline;

  void initialize() {
    // Check initial connectivity
    _checkConnectivity();

    // Listen for connectivity changes
    _subscription = _connectivity.onConnectivityChanged.listen((result) {
      _handleConnectivityChange(result);
    });
  }

  Future<void> _checkConnectivity() async {
    final result = await _connectivity.checkConnectivity();
    _isOnline = result != ConnectivityResult.none;
  }

  void _handleConnectivityChange(ConnectivityResult result) {
    final wasOffline = !_isOnline;
    _isOnline = result != ConnectivityResult.none;

    if (wasOffline && _isOnline) {
      // Connectivity restored!
      _triggerAutoSync();
    }
  }
}
```

---

### Auto-Sync on Connect

When connectivity is restored, the system automatically syncs pending data:

```dart
class SyncManager {
  Future<void> autoSync() async {
    try {
      // 1. Sync pending journal entries
      await _syncJournalEntries();

      // 2. Refresh expired caches
      await _refreshExpiredCaches();

      // 3. Upload pending analytics events
      await _syncAnalyticsEvents();

      // 4. Update user preferences
      await _syncUserPreferences();

      SecureLoggingService().info('Auto-sync completed successfully');
    } catch (e, stack) {
      SecureLoggingService().error(
        'Auto-sync failed',
        error: e,
        stackTrace: stack,
      );
    }
  }

  Future<void> _syncJournalEntries() async {
    final prefs = await SharedPreferences.getInstance();
    final pendingKeys = prefs.getKeys()
      .where((key) => key.startsWith('pending_journal_'));

    for (final key in pendingKeys) {
      final entryJson = prefs.getString(key);
      if (entryJson == null) continue;

      try {
        // Upload to backend
        await backendService.uploadJournalEntry(entryJson);

        // Remove from pending queue
        await prefs.remove(key);
      } catch (e) {
        // Will retry on next sync
        SecureLoggingService().warning('Failed to sync journal entry: $key');
      }
    }
  }
}
```

---

### Manual Sync

Users can trigger manual sync via pull-to-refresh:

```dart
class HoroscopeScreen extends StatefulWidget {
  @override
  _HoroscopeScreenState createState() => _HoroscopeScreenState();
}

class _HoroscopeScreenState extends State<HoroscopeScreen> {
  final _offlineService = OfflineModeService();
  bool _isSyncing = false;

  Future<void> _handleRefresh() async {
    if (!_offlineService.isOnline) {
      _showOfflineMessage();
      return;
    }

    setState(() => _isSyncing = true);

    try {
      // Force refresh from backend
      await horoscopeService.refreshHoroscope(forceRefresh: true);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Updated to latest horoscope ✨')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to refresh. Try again.')),
      );
    } finally {
      setState(() => _isSyncing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _handleRefresh,
      child: ListView(
        // Your content
      ),
    );
  }
}
```

---

## Conflict Resolution

### Conflict Types

#### 1. Journal Entry Conflicts

**Scenario**: User edits journal entry offline, but entry was modified on another device.

**Resolution**: Last-write-wins (LWW)

```dart
class JournalConflictResolver {
  Future<JournalEntry> resolveConflict(
    JournalEntry local,
    JournalEntry remote,
  ) async {
    // Use timestamp to determine winner
    if (local.modifiedAt.isAfter(remote.modifiedAt)) {
      // Local is newer
      await backendService.updateJournalEntry(local);
      return local;
    } else {
      // Remote is newer
      await cacheService.updateLocalJournal(remote);
      return remote;
    }
  }
}
```

---

#### 2. Preference Conflicts

**Scenario**: User changes notification time on device A, then changes it on device B while offline.

**Resolution**: Device-specific preferences + Server-side merge

```dart
class PreferenceConflictResolver {
  Future<void> resolvePreferences(
    Map<String, dynamic> local,
    Map<String, dynamic> remote,
  ) async {
    final merged = <String, dynamic>{};

    // Merge strategy: take newer value for each preference
    for (final key in {...local.keys, ...remote.keys}) {
      final localTimestamp = local['${key}_timestamp'] as int?;
      final remoteTimestamp = remote['${key}_timestamp'] as int?;

      if (localTimestamp == null) {
        merged[key] = remote[key];
      } else if (remoteTimestamp == null) {
        merged[key] = local[key];
      } else if (localTimestamp > remoteTimestamp) {
        merged[key] = local[key];
      } else {
        merged[key] = remote[key];
      }
    }

    // Save merged preferences
    await preferencesService.saveAll(merged);
  }
}
```

---

#### 3. Data Freshness Conflicts

**Scenario**: Cached horoscope is stale, but user is offline.

**Resolution**: Show cached data with staleness indicator

```dart
class HoroscopeService {
  Future<Horoscope> getDailyHoroscope(String sign) async {
    if (!offlineService.isOnline) {
      // Use cache (even if stale)
      final cached = await cacheService.getCachedHoroscope(sign);

      if (cached != null) {
        cached.isStale = cacheService.isExpired(cached.cachedAt);
        cached.cacheAge = DateTime.now().difference(cached.cachedAt);
        return cached;
      } else {
        throw OfflineException('No cached horoscope available');
      }
    }

    // Online: fetch fresh data
    return await _fetchFromBackend(sign);
  }
}

// In UI
Widget build(BuildContext context) {
  return Column(
    children: [
      if (horoscope.isStale)
        Banner(
          message: 'Cached ${_formatCacheAge(horoscope.cacheAge)}',
          color: Colors.orange,
        ),
      HoroscopeContent(horoscope: horoscope),
    ],
  );
}
```

---

## Performance Considerations

### Cache Size Management

```dart
class CacheSizeManager {
  static const int maxCacheSizeMB = 50;

  Future<void> enforceSizeLimit() async {
    final cacheSize = await _calculateCacheSize();

    if (cacheSize > maxCacheSizeMB * 1024 * 1024) {
      // Cache too large, cleanup
      await _performCleanup();
    }
  }

  Future<void> _performCleanup() async {
    // 1. Remove expired caches
    await cacheService.removeExpired();

    // 2. Remove oldest non-essential caches
    await cacheService.removeOldest(
      preserveKeys: [
        'birth_chart_*',
        'user_preferences_*',
        'journal_entries_*',
      ],
    );

    // 3. Compact database
    await hiveService.compact();
  }
}
```

---

### Read Performance

- **SharedPreferences**: <5ms typical
- **Hive Database**: <10ms typical
- **Cache hit**: <15ms end-to-end
- **Cache miss + API**: 500-2000ms

### Write Performance

- **SharedPreferences**: <10ms
- **Hive Database**: <20ms
- **Batch writes**: Prefer for multiple updates

---

## Offline Indicators

### Visual Feedback

```dart
class OfflineIndicator extends StatelessWidget {
  final bool isOnline;

  @override
  Widget build(BuildContext context) {
    if (isOnline) return SizedBox.shrink();

    return Container(
      color: Colors.orange,
      padding: EdgeInsets.all(8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.cloud_off, color: Colors.white, size: 16),
          SizedBox(width: 8),
          Text(
            'Offline Mode - Showing cached content',
            style: TextStyle(color: Colors.white, fontSize: 12),
          ),
        ],
      ),
    );
  }
}
```

---

## Troubleshooting

### Issue: Cache not updating after going online

**Solution**:
```dart
// Force cache refresh
await cacheService.invalidateAll();
await syncManager.autoSync();

// Check connectivity
print('Online: ${offlineService.isOnline}');

// Verify background sync enabled
// Settings → Background App Refresh → On
```

---

### Issue: "No cached data available" error

**Solution**:
```dart
// Ensure data was cached when online
if (offlineService.isOnline) {
  await horoscopeService.prewarmCache();
}

// Check cache size limits
final size = await cacheService.getCacheSize();
print('Cache size: $size MB');

// Verify storage permissions (Android)
```

---

### Issue: Sync conflicts causing data loss

**Solution**:
```dart
// Enable conflict logs
SecureLoggingService().debug('Conflict detected', context: {
  'local_modified': local.modifiedAt,
  'remote_modified': remote.modifiedAt,
});

// Use explicit conflict resolution
await conflictResolver.resolveWithUserInput(local, remote);

// Backup before sync
await backupService.createBackup();
```

---

## Best Practices

1. **Always check online status before API calls**
2. **Provide clear offline indicators to users**
3. **Cache essential data proactively**
4. **Handle offline errors gracefully**
5. **Sync as soon as connectivity restored**
6. **Use appropriate TTL for each data type**
7. **Monitor cache size regularly**
8. **Test offline scenarios thoroughly**

---

**For support**: Contact dev team
**For bugs**: See GitHub issues
**For features**: See product roadmap
