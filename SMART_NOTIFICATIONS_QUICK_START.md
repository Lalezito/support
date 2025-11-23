# Smart Notification Engine - Quick Start Guide

## 🚀 Get Running in 15 Minutes

### Step 1: Database Setup (2 minutes)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend

# Run the schema
psql -U postgres -d your_database -f database/smart_notifications_schema.sql
```

**Expected Output:**
```
CREATE TABLE
CREATE INDEX
CREATE FUNCTION
CREATE TRIGGER
... (should see ~40 successful commands)
```

### Step 2: Environment Variables (1 minute)

Add to `.env`:

```bash
# Required for AI features
OPENAI_API_KEY=sk-your-key-here

# Already configured (verify they exist)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY="your-key"
FIREBASE_CLIENT_EMAIL=your-email
```

### Step 3: Register Routes (1 minute)

Edit `src/app.js` and add:

```javascript
// Add at top with other requires
const smartNotificationsRouter = require('./routes/smartNotifications');

// Add with other routes (after line ~50)
app.use('/api/notifications', smartNotificationsRouter);
```

### Step 4: Test Installation (1 minute)

```bash
# Start server
npm run dev

# In another terminal, test:
curl http://localhost:3000/api/notifications/status
```

**Expected Response:**
```json
{
  "success": true,
  "services": {
    "notificationEngine": {
      "status": "operational",
      "aiEnabled": true
    }
  }
}
```

### Step 5: Send First Test Notification (2 minutes)

```bash
# Replace USER_UUID with a real user ID from your database
curl -X POST http://localhost:3000/api/notifications/test \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "USER_UUID",
    "notificationType": "DAILY_HOROSCOPE"
  }'
```

**Success Response:**
```json
{
  "success": true,
  "notificationId": 1,
  "scheduledFor": "2025-01-23T09:00:00Z",
  "optimalTime": {
    "confidence": 87,
    "localTime": "9:00 AM"
  }
}
```

---

## 📱 Mobile Integration

### iOS (Swift)

```swift
// 1. Request permission
UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
    if granted {
        DispatchQueue.main.async {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }
}

// 2. Register FCM token
func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()

    // Send to backend
    registerFCMToken(userId: currentUserId, token: token)
}

// 3. Track notification opened
func userNotificationCenter(_ center: UNUserNotificationCenter,
                          didReceive response: UNNotificationResponse,
                          withCompletionHandler completionHandler: @escaping () -> Void) {
    let notificationId = response.notification.request.content.userInfo["notification_id"] as? Int

    trackNotificationEvent(notificationId: notificationId, eventType: "opened")
    completionHandler()
}
```

### Android (Kotlin)

```kotlin
// 1. Get FCM token
FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val token = task.result
        registerFCMToken(userId, token)
    }
}

// 2. Handle notification received
class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        val notificationId = remoteMessage.data["notification_id"]?.toInt()

        // Show notification
        showNotification(remoteMessage)

        // Track delivery
        trackNotificationEvent(notificationId, "delivered")
    }
}

// 3. Track notification opened
notificationManager.setOnNotificationClickListener { notificationId ->
    trackNotificationEvent(notificationId, "opened")
}
```

### Flutter

```dart
// 1. Initialize Firebase Messaging
final messaging = FirebaseMessaging.instance;

// Request permission
NotificationSettings settings = await messaging.requestPermission();

// Get token
String? token = await messaging.getToken();
if (token != null) {
  await registerFCMToken(userId: currentUserId, token: token);
}

// 2. Handle foreground messages
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  final notificationId = message.data['notification_id'];

  // Track delivery
  trackNotificationEvent(
    notificationId: int.parse(notificationId),
    eventType: 'delivered'
  );

  // Show local notification
  showLocalNotification(message);
});

// 3. Handle notification tap
FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
  final notificationId = message.data['notification_id'];

  // Track opened
  trackNotificationEvent(
    notificationId: int.parse(notificationId),
    eventType: 'opened'
  );

  // Navigate to screen
  navigateToScreen(message.data['deepLink']);
});
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Horoscope at User's Optimal Time

```javascript
// backend/routes/horoscope.js

router.get('/daily/:sign', async (req, res) => {
  const { sign } = req.params;
  const userId = req.user.id;  // From auth middleware

  // Generate horoscope
  const horoscope = await generateDailyHoroscope(sign);

  // Send smart notification for tomorrow
  await smartNotificationEngine.sendSmartNotification(
    userId,
    'DAILY_HOROSCOPE',
    {
      horoscopeImage: horoscope.imageUrl,
      horoscopeSnippet: horoscope.content.substring(0, 100)
    }
  );

  res.json({ success: true, horoscope });
});
```

### Use Case 2: Streak Protection

```javascript
// Automated via cron (already configured in smartNotificationEngine.js)
// Runs at 9 PM daily

// Manual trigger for testing:
await smartNotificationEngine.processStreakProtection();

// What it does:
// 1. Finds users who haven't checked in today
// 2. Calculates optimal send time (usually evening)
// 3. Sends personalized "don't break your streak" notification
// 4. Tracks engagement
```

### Use Case 3: Compatibility Alert

```javascript
// backend/routes/compatibility.js

router.post('/check', async (req, res) => {
  const { userId, partnerId } = req.body;

  // Calculate compatibility
  const result = await calculateCompatibility(userId, partnerId);

  // If high compatibility, send notification
  if (result.score > 80) {
    await smartNotificationEngine.sendSmartNotification(
      userId,
      'COMPATIBILITY_UPDATE',
      {
        partnerName: result.partnerName,
        compatibilityScore: result.score,
        reason: result.topReason
      }
    );
  }

  res.json({ success: true, result });
});
```

### Use Case 4: Re-Engagement Campaign

```javascript
// backend/cron/daily-tasks.js

cron.schedule('0 10 * * *', async () => {
  // Find users inactive for 7+ days
  const dormantUsers = await db.query(`
    SELECT id, name, zodiac_sign,
           EXTRACT(days FROM (NOW() - last_active)) as days_inactive
    FROM users
    WHERE last_active < NOW() - INTERVAL '7 days'
      AND last_active > NOW() - INTERVAL '30 days'
  `);

  for (const user of dormantUsers.rows) {
    await smartNotificationEngine.sendSmartNotification(
      user.id,
      'RE_ENGAGEMENT',
      {
        daysSinceLastUse: user.days_inactive,
        incentive: days_inactive > 14 ? 'free_premium_reading' : 'welcome_back_bonus'
      }
    );
  }
});
```

---

## 📊 Monitor Performance

### Real-Time Dashboard Query

```sql
-- Overall health (last 24 hours)
SELECT
  COUNT(*) as total_sent,
  COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END) as opened,
  ROUND(
    COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100,
    2
  ) as open_rate,
  ROUND(AVG(time_to_open_seconds) / 60, 1) as avg_time_to_open_min
FROM smart_notifications
WHERE sent_at > NOW() - INTERVAL '24 hours';
```

### Performance by Type

```sql
SELECT
  type,
  COUNT(*) as sent,
  ROUND(
    COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100,
    2
  ) as open_rate
FROM smart_notifications
WHERE sent_at > NOW() - INTERVAL '7 days'
GROUP BY type
ORDER BY open_rate DESC;
```

### Best Send Times

```sql
SELECT
  EXTRACT(hour FROM sent_at) as hour,
  COUNT(*) as sent,
  ROUND(
    COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100,
    2
  ) as open_rate
FROM smart_notifications
WHERE sent_at > NOW() - INTERVAL '30 days'
GROUP BY hour
ORDER BY open_rate DESC;
```

---

## 🔧 Troubleshooting

### Problem: "No FCM token found"

**Solution:**
```sql
-- Check if user has token
SELECT * FROM fcm_tokens WHERE user_id = 'USER_UUID';

-- If missing, user needs to:
-- 1. Open app
-- 2. Grant notification permission
-- 3. App should auto-register token
```

### Problem: Notifications not personalized

**Solution:**
```bash
# Check OpenAI key
echo $OPENAI_API_KEY

# Test AI generation
curl -X POST http://localhost:3000/api/notifications/test \
  -H "Content-Type: application/json" \
  -d '{"userId": "USER_UUID"}'

# Look for "generated": "ai" in response
```

### Problem: All notifications immediate (not optimal time)

**Solution:**
```sql
-- Check user activity data
SELECT COUNT(*) FROM user_activity_logs WHERE user_id = 'USER_UUID';

-- If < 5, not enough data for analysis
-- Solution: Log more user activity
```

---

## 🎓 Learning Path

### Day 1: Setup & First Notification
- ✅ Install database schema
- ✅ Configure environment
- ✅ Send test notification

### Day 2-3: Integration
- Integrate with mobile app
- Track user activities
- Implement FCM token registration

### Day 4-7: Optimization
- Enable AI personalization
- Set up A/B tests
- Monitor analytics

### Week 2+: Advanced Features
- Re-engagement campaigns
- Custom notification types
- Advanced behavioral analysis

---

## 📈 Success Metrics

**Week 1 Goals:**
- [ ] 100+ notifications sent
- [ ] Open rate > 40%
- [ ] Opt-out rate < 10%

**Month 1 Goals:**
- [ ] Open rate > 55%
- [ ] 1,000+ notifications sent
- [ ] DAU increase +15%
- [ ] User engagement up +20%

**Month 3 Goals:**
- [ ] Open rate > 60%
- [ ] Opt-out rate < 5%
- [ ] DAU increase +35%
- [ ] Measurable revenue impact ($2K+)

---

## 💡 Pro Tips

1. **Start Conservative**
   - Begin with 2 notifications/day max
   - Increase as you optimize

2. **A/B Test Everything**
   - Different send times
   - Message variations
   - Emoji usage

3. **Monitor User Feedback**
   - Track opt-out reasons
   - Survey engaged users
   - Iterate based on data

4. **Respect User Preferences**
   - Make settings easily accessible
   - Honor quiet hours
   - Allow granular control

5. **Focus on Value**
   - Every notification should ADD value
   - Not just reminders
   - Actionable insights

---

## 🚀 Next Steps

1. **Complete setup checklist above**
2. **Send first test notification**
3. **Integrate with mobile app**
4. **Monitor analytics for 7 days**
5. **Optimize based on data**
6. **Scale to all users**

---

## 📞 Support

**Issues?** Check the full documentation: `SMART_NOTIFICATION_ENGINE_DOCUMENTATION.md`

**Feature requests?** The system is designed to be extensible. Add custom notification types in `smartNotificationEngine.js`.

**Questions?** Review the API examples in the documentation.

---

**You're ready! Start sending intelligent notifications that users will LOVE to receive.** 🎉

**Remember:** The goal isn't to send MORE notifications. It's to send the RIGHT notifications at the RIGHT time.

**Target:** 60%+ open rate (vs industry 10-20%)

Let's make it happen! 🚀
