# Backend Resilience Quick Reference Guide

**For**: Developers maintaining Zodiac App backend integration
**Last Updated**: October 13, 2025

---

## 🎯 Quick Summary

The Zodiac App uses a **3-level fallback cascade** to ensure users always get horoscope content:

```
Railway API (2-3s) → Local Cache (<100ms) → Local Generation (<500ms)
```

**Status**: ✅ Fully Implemented and Production Ready

---

## 📁 Key Files

| File | Purpose | Lines of Interest |
|------|---------|-------------------|
| `backend_service.dart` | Backend API + Cache | 448-543 (fallback) |
| `horoscope_service.dart` | Orchestration | 254-378 (main method) |
| `BACKEND_RESILIENCE_REPORT.md` | Full documentation | All |
| `test_backend_resilience.sh` | Testing script | All |

---

## 🔄 Fallback Flow Diagram

```
┌─────────────────────┐
│  User Requests      │
│  Horoscope          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│ LEVEL 1: Railway API                        │
│ Endpoint: /api/coaching/getDailyHoroscope   │
│ Timeout: 10 seconds                         │
│ Success? ────────────────────────► YES ─────┼──► Return horoscope
│                                              │    Save to cache
└──────────┬───────────────────────────────────┘
           │ NO (timeout/error)
           ▼
┌─────────────────────────────────────────────┐
│ LEVEL 2: Local Cache                        │
│ Check: Memory cache → Disk cache            │
│ TTL: 24 hours (same day)                    │
│ Valid? ──────────────────────► YES ─────────┼──► Return cached
│                                              │    horoscope
└──────────┬───────────────────────────────────┘
           │ NO (miss/expired)
           ▼
┌─────────────────────────────────────────────┐
│ LEVEL 3: Local Generation                   │
│ Method: Deterministic seed-based            │
│ Languages: 6 supported                      │
│ Always succeeds ─────────────────────────► │──► Return generated
│                                              │    horoscope
└──────────────────────────────────────────────┘
```

---

## 🚀 Quick Testing

### Test Level 1 (Railway)
```bash
# With internet on, clear cache
adb shell pm clear com.zodiac.app
# Open app → Load horoscope
# Expect: 2-3 second load, Railway success log
```

### Test Level 2 (Cache)
```bash
# After Level 1 test
adb shell svc wifi disable  # Enable airplane mode
# Restart app → Load same sign
# Expect: Instant load, Cache hit log
```

### Test Level 3 (Local)
```bash
# Clear app data + airplane mode
adb shell pm clear com.zodiac.app
adb shell svc wifi disable
# Open app → Load horoscope
# Expect: <500ms load, Local generation log
```

### Run Full Test Suite
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia
./test_backend_resilience.sh
```

---

## 📊 Log Patterns to Watch

### Success Patterns
```
✅ Backend: Level 1 - Railway API success for {sign}
✅ Backend: Level 2 - Using valid cached horoscope for {sign}
✅ Backend: Level 3 - Local generation for {sign}
```

### Warning Patterns
```
⚠️ Backend: Level 1 failed - Status: {code}
⚠️ Backend: Trying Level 2 - Local cache for {sign}
⚠️ Backend: Using Level 3 - Local generation for {sign}
```

### Error Patterns (Investigate)
```
❌ Backend: Error leyendo cache
❌ Backend: Error guardando cache
❌ API returned non-200 status
```

---

## 🔧 Common Maintenance Tasks

### Check Cache Status
```dart
final status = await BackendService().getCacheStatus();
print(status);
// Output: {'status': 'valid', 'age_hours': 5, 'entries': 12}
```

### Clear Cache Manually
```dart
await BackendService().clearCache();
// Clears both memory and disk cache
```

### Force Cache Refresh
```bash
# Method 1: Clear specific sign
await BackendService().clearCache();
await BackendService().getHoroscope('aries');

# Method 2: Bulk download
await BackendService().downloadAllHoroscopes();
```

---

## 🐛 Troubleshooting

### Issue: Horoscopes always using Level 3
**Symptoms**: Generic content, Level 3 logs
**Causes**:
1. Railway API is down → Check https://zodiac-backend-api-production-8ded.up.railway.app/health
2. Network blocked → Check firewall/proxy
3. API timeout → Check Railway logs for slow responses

**Fix**:
```bash
# Verify Railway API is reachable
curl -v https://zodiac-backend-api-production-8ded.up.railway.app/api/coaching/getDailyHoroscope?sign=aries&language=en

# Check app logs for timeout
flutter logs | grep "Level 1 failed"
```

---

### Issue: Cache not persisting
**Symptoms**: Always hitting Railway API, no cache hits
**Causes**:
1. SharedPreferences not initialized → Check app startup
2. Cache being cleared too aggressively → Check cache clear calls
3. TTL validation failing → Check device time

**Fix**:
```dart
// Verify SharedPreferences works
final prefs = await SharedPreferences.getInstance();
final hasCache = prefs.containsKey('backend_horoscopes_cache');
print('Cache exists: $hasCache');

// Check cache status
final status = await BackendService().getCacheStatus();
print('Cache age: ${status['age_hours']} hours');
```

---

### Issue: Stale content shown
**Symptoms**: Yesterday's horoscope displayed today
**Causes**:
1. Cache TTL not expiring → Check `_isCacheValid()` logic
2. Device time incorrect → Check system time
3. Cache timestamp corrupted → Clear cache

**Fix**:
```dart
// Force clear and refresh
await BackendService().clearCache();
await HoroscopeService().forceReload();
```

---

### Issue: Different language shown
**Symptoms**: Horoscope in wrong language
**Causes**:
1. Language detection failing → Check `_getDetectedLanguage()`
2. Cache has wrong language → Clear cache
3. PreferencesService not initialized → Check setup

**Fix**:
```dart
// Verify language detection
final service = HoroscopeService();
final language = await service._getDetectedLanguage(); // Private, use debug
print('Detected language: $language');

// Force language update
service.forceLanguageUpdate();
```

---

## 📈 Performance Targets

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Level 1 Success Rate | >95% | TBD | ⏱️ |
| Level 1 Response Time | <3s | TBD | ⏱️ |
| Level 2 Hit Rate | >80% | TBD | ⏱️ |
| Level 2 Response Time | <100ms | TBD | ⏱️ |
| Level 3 Usage Rate | <5% | TBD | ⏱️ |
| Level 3 Response Time | <500ms | TBD | ⏱️ |
| Cache Size | <500KB | TBD | ⏱️ |

---

## 🔐 Security Notes

- All API requests use HTTPS
- CSRF tokens generated per session
- Request IDs for tracing
- No sensitive data in cache
- Timeout prevents hanging requests

---

## 📚 Additional Resources

- **Full Documentation**: `BACKEND_RESILIENCE_REPORT.md`
- **Testing Script**: `test_backend_resilience.sh`
- **Backend API Docs**: Railway dashboard
- **Crashlytics**: Firebase console for error tracking

---

## 🎓 Developer Onboarding

### New Developer Checklist

1. ✅ Read this quick guide
2. ✅ Read full report: `BACKEND_RESILIENCE_REPORT.md`
3. ✅ Review code:
   - `backend_service.dart` (lines 448-863)
   - `horoscope_service.dart` (lines 254-378)
4. ✅ Run test suite: `./test_backend_resilience.sh`
5. ✅ Test each fallback level manually
6. ✅ Monitor logs in production

### Key Concepts to Understand

1. **3-Level Cascade**: Railway → Cache → Local
2. **Cache Strategy**: Memory (fast) + Disk (persistent)
3. **TTL Validation**: Same day + <24 hours
4. **Deterministic Generation**: Same seed = same content
5. **Multi-Language**: 6 languages with templates

---

## 💡 Pro Tips

1. **Always check logs first** when debugging horoscope issues
2. **Cache is your friend** - don't clear it unnecessarily
3. **Test offline mode regularly** to ensure Level 3 works
4. **Monitor Railway API health** in production
5. **Use Crashlytics** to track API failures

---

## 📞 Support

**Questions?**
- Check full documentation: `BACKEND_RESILIENCE_REPORT.md`
- Review code comments in `backend_service.dart`
- Check Crashlytics for production errors

**Found a bug?**
- Check known issues in this guide
- Review logs for error patterns
- Test with the testing script

---

**Last Updated**: October 13, 2025
**Version**: 1.0
**Status**: Production Ready ✅
