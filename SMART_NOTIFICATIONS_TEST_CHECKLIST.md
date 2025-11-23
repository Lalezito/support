# Smart Notification Engine - Testing Checklist

## 🧪 Complete Testing Guide

Use this checklist to verify your Smart Notification Engine is working perfectly.

---

## ✅ Phase 1: Installation Verification (Day 1)

### Database Setup

- [ ] Run `smart_notifications_schema.sql`
- [ ] Verify 8 tables created:
  ```sql
  SELECT table_name FROM information_schema.tables 
  WHERE table_schema = 'public' 
  AND table_name LIKE '%notification%' OR table_name = 'user_activity_logs';
  ```
  **Expected:** 8 rows

- [ ] Verify indexes created:
  ```sql
  SELECT COUNT(*) FROM pg_indexes 
  WHERE tablename LIKE '%notification%';
  ```
  **Expected:** 20+ indexes

- [ ] Check sample templates:
  ```sql
  SELECT COUNT(*) FROM notification_templates;
  ```
  **Expected:** 5+ templates

### Environment Configuration

- [ ] Verify OpenAI key: `echo $OPENAI_API_KEY`
- [ ] Verify Firebase credentials exist
- [ ] Check Redis connection (if using):
  ```bash
  redis-cli ping
  ```
  **Expected:** PONG

### API Routes

- [ ] Routes registered in `src/app.js`
- [ ] Server starts without errors: `npm run dev`
- [ ] Status endpoint works:
  ```bash
  curl http://localhost:3000/api/notifications/status
  ```
  **Expected:** `"status": "operational"`

---

## ✅ Phase 2: Basic Functionality (Day 2)

### Test Send Notification

- [ ] Send test notification:
  ```bash
  curl -X POST http://localhost:3000/api/notifications/test \
    -H "Content-Type: application/json" \
    -d '{"userId": "YOUR_USER_UUID"}'
  ```

- [ ] Verify notification in database:
  ```sql
  SELECT * FROM smart_notifications ORDER BY sent_at DESC LIMIT 1;
  ```

- [ ] Check scheduled notifications:
  ```sql
  SELECT * FROM scheduled_notifications WHERE status = 'pending';
  ```

### Test Spam Prevention

- [ ] Send 4 notifications to same user within 1 hour
  **Expected:** 4th should be blocked with "daily_limit_reached"

- [ ] Send notification during quiet hours (11 PM - 7 AM)
  **Expected:** Blocked with "quiet_hours" (unless priority >= 9)

- [ ] Send notification <2 hours after user opened app
  **Expected:** Blocked with "recently_used_app"

### Test User Preferences

- [ ] Get preferences:
  ```bash
  curl http://localhost:3000/api/notifications/preferences/USER_UUID
  ```

- [ ] Update preferences:
  ```bash
  curl -X PUT http://localhost:3000/api/notifications/preferences/USER_UUID \
    -H "Content-Type: application/json" \
    -d '{"max_per_day": 2, "quiet_hours_start": 22}'
  ```

- [ ] Verify update in database:
  ```sql
  SELECT max_per_day FROM user_notification_preferences WHERE user_id = 'USER_UUID';
  ```

---

## ✅ Phase 3: AI & Intelligence (Day 3)

### AI Content Generation

- [ ] Verify OpenAI API works:
  ```bash
  curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
  ```

- [ ] Send notification and check for AI generation:
  ```sql
  SELECT title, body, data->'generated' as generated_by
  FROM smart_notifications
  WHERE sent_at > NOW() - INTERVAL '1 hour'
  ORDER BY sent_at DESC LIMIT 1;
  ```
  **Expected:** `generated_by = "ai"` (if OpenAI key valid)

- [ ] Verify fallback to templates when AI fails:
  - Temporarily use invalid OpenAI key
  - Send notification
  - Check: `generated_by = "template"`

### Behavior Analysis

- [ ] Log some user activity:
  ```bash
  curl -X POST http://localhost:3000/api/notifications/log-activity \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "activityType": "app_open",
      "deviceType": "iOS"
    }'
  ```

- [ ] Repeat 10-20 times at different hours

- [ ] Get behavior profile:
  ```bash
  curl http://localhost:3000/api/notifications/behavior/USER_UUID
  ```

- [ ] Verify profile contains:
  - `usagePatterns.peakHours` array
  - `engagement.engagementScore` number
  - `churnRisk.riskScore` number
  - `optimalTimes.bestOverall` array

### Send Time Optimization

- [ ] Send notification with behavior data:
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "DAILY_HOROSCOPE",
      "context": {}
    }'
  ```

- [ ] Check optimal time was calculated:
  ```json
  {
    "optimalTime": {
      "optimalTime": "...",
      "confidence": 70,
      "reasoning": "...",
      "userTimezone": "..."
    }
  }
  ```

---

## ✅ Phase 4: Tracking & Analytics (Day 4)

### Event Tracking

- [ ] Get a notification ID from database
- [ ] Track delivered:
  ```bash
  curl -X POST http://localhost:3000/api/notifications/track-event \
    -H "Content-Type: application/json" \
    -d '{"notificationId": 123, "eventType": "delivered"}'
  ```

- [ ] Track opened:
  ```bash
  curl -X POST http://localhost:3000/api/notifications/track-event \
    -H "Content-Type: application/json" \
    -d '{"notificationId": 123, "eventType": "opened"}'
  ```

- [ ] Verify timestamps in database:
  ```sql
  SELECT sent_at, delivered_at, opened_at, time_to_open_seconds
  FROM smart_notifications WHERE id = 123;
  ```
  **Expected:** All fields populated, time_to_open calculated

### Analytics Queries

- [ ] Get overall analytics:
  ```bash
  curl http://localhost:3000/api/notifications/analytics?days=7
  ```

- [ ] Verify response contains:
  - `overall.open_rate` (percentage)
  - `overall.click_rate` (percentage)
  - `byType` array with per-type stats
  - `dailyTrend` array

- [ ] Run performance view:
  ```sql
  SELECT * FROM notification_performance_summary;
  ```

- [ ] Check user engagement scores:
  ```sql
  SELECT * FROM user_engagement_scores LIMIT 10;
  ```

---

## ✅ Phase 5: All Notification Types (Day 5)

### Test Each Type

- [ ] **DAILY_HOROSCOPE**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "DAILY_HOROSCOPE",
      "context": {"horoscopeImage": "https://example.com/image.jpg"}
    }'
  ```

- [ ] **STREAK_PROTECTION**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "STREAK_PROTECTION",
      "context": {"streakDays": 47}
    }'
  ```

- [ ] **PERFECT_TIMING**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "PERFECT_TIMING",
      "context": {}
    }'
  ```

- [ ] **PREDICTION_ALERT**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "PREDICTION_ALERT",
      "context": {
        "category": "love",
        "hoursUntil": 24,
        "predictionId": 123
      }
    }'
  ```

- [ ] **COMPATIBILITY_UPDATE**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "COMPATIBILITY_UPDATE",
      "context": {
        "partnerName": "Alex",
        "compatibilityScore": 89
      }
    }'
  ```

- [ ] **MOON_PHASE**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "MOON_PHASE",
      "context": {"moonPhase": "Full Moon"}
    }'
  ```

- [ ] **PERSONALIZED_INSIGHT**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "PERSONALIZED_INSIGHT",
      "context": {"insight": "most creative in the evenings"}
    }'
  ```

- [ ] **RE_ENGAGEMENT**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "RE_ENGAGEMENT",
      "context": {
        "daysSinceLastUse": 7,
        "incentive": "free_reading"
      }
    }'
  ```

- [ ] **PREMIUM_OFFER**
  ```bash
  curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{
      "userId": "USER_UUID",
      "notificationType": "PREMIUM_OFFER",
      "context": {"offerId": "winter_sale"}
    }'
  ```

### Verify Each Type

- [ ] Check database for all 9 types:
  ```sql
  SELECT type, COUNT(*) FROM smart_notifications
  GROUP BY type ORDER BY type;
  ```
  **Expected:** 9 different types

---

## ✅ Phase 6: Mobile Integration (Day 6-7)

### iOS Testing

- [ ] FCM token registration works
- [ ] Notification appears on device
- [ ] Tapping opens app
- [ ] Deep link navigation works
- [ ] Event tracking (opened) fires
- [ ] Badge count updates

### Android Testing

- [ ] FCM token registration works
- [ ] Notification appears on device
- [ ] Tapping opens app
- [ ] Deep link navigation works
- [ ] Event tracking (opened) fires
- [ ] Actions buttons work

### Flutter Testing

- [ ] Firebase Messaging initialized
- [ ] Token registration works
- [ ] Foreground notifications shown
- [ ] Background notifications handled
- [ ] onMessageOpenedApp works
- [ ] Deep links navigate correctly

---

## ✅ Phase 7: Automated Campaigns (Week 2)

### Cron Jobs

- [ ] Verify cron jobs initialized:
  - Check server logs for "Notification Engine cron jobs initialized"

- [ ] Test daily horoscope automation:
  ```javascript
  // In Node REPL or test file:
  const engine = require('./src/services/smartNotificationEngine');
  await engine.processDailyHoroscopes();
  ```

- [ ] Test streak protection automation:
  ```javascript
  await engine.processStreakProtection();
  ```

- [ ] Check scheduled notifications queue:
  ```sql
  SELECT type, COUNT(*) FROM scheduled_notifications
  WHERE status = 'pending' GROUP BY type;
  ```

### Re-Engagement Campaign

- [ ] Create dormant test user (inactive 8 days)
- [ ] Run re-engagement campaign:
  ```javascript
  await engine.processReEngagementCampaign();
  ```

- [ ] Verify notification sent:
  ```sql
  SELECT * FROM smart_notifications
  WHERE type = 're_engagement'
  ORDER BY sent_at DESC LIMIT 5;
  ```

---

## ✅ Phase 8: Performance Testing (Week 2)

### Load Testing

- [ ] Send 100 notifications rapidly:
  ```bash
  for i in {1..100}; do
    curl -X POST http://localhost:3000/api/notifications/send \
      -H "Content-Type: application/json" \
      -d '{"userId": "USER_'$i'", "notificationType": "DAILY_HOROSCOPE"}' &
  done
  wait
  ```

- [ ] Check all succeeded:
  ```sql
  SELECT COUNT(*) FROM smart_notifications
  WHERE sent_at > NOW() - INTERVAL '5 minutes';
  ```
  **Expected:** 100 (or close, accounting for spam prevention)

### Response Time Testing

- [ ] Measure send notification:
  ```bash
  time curl -X POST http://localhost:3000/api/notifications/send \
    -H "Content-Type: application/json" \
    -d '{"userId": "USER_UUID", "notificationType": "DAILY_HOROSCOPE"}'
  ```
  **Target:** <500ms

- [ ] Measure behavior profile:
  ```bash
  time curl http://localhost:3000/api/notifications/behavior/USER_UUID
  ```
  **Target:** <800ms (first time), <50ms (cached)

- [ ] Measure analytics:
  ```bash
  time curl http://localhost:3000/api/notifications/analytics?days=7
  ```
  **Target:** <1s

### Database Performance

- [ ] Run EXPLAIN ANALYZE on key queries:
  ```sql
  EXPLAIN ANALYZE
  SELECT * FROM smart_notifications
  WHERE user_id = 'USER_UUID'
  ORDER BY sent_at DESC LIMIT 20;
  ```
  **Target:** <10ms

- [ ] Check index usage:
  ```sql
  SELECT schemaname, tablename, indexname, idx_scan
  FROM pg_stat_user_indexes
  WHERE tablename LIKE '%notification%'
  ORDER BY idx_scan DESC;
  ```
  **Expected:** All indexes being used (idx_scan > 0)

---

## ✅ Phase 9: A/B Testing (Week 3)

### Create A/B Test

- [ ] Insert test variant:
  ```sql
  INSERT INTO notification_ab_tests (
    notification_type, test_name, variants, traffic_allocation
  ) VALUES (
    'DAILY_HOROSCOPE',
    'Emoji Test',
    '[
      {"id": "control", "emoji": ""},
      {"id": "variant_a", "emoji": "🌟"}
    ]',
    '{"control": 50, "variant_a": 50}'
  );
  ```

- [ ] Send 100 notifications
- [ ] Verify 50/50 distribution:
  ```sql
  SELECT data->>'variantId' as variant, COUNT(*)
  FROM smart_notifications
  WHERE type = 'DAILY_HOROSCOPE'
  AND sent_at > NOW() - INTERVAL '1 hour'
  GROUP BY variant;
  ```

### Analyze Results

- [ ] Check performance by variant:
  ```sql
  SELECT
    data->>'variantId' as variant,
    COUNT(*) as sent,
    COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END) as opened,
    ROUND(
      COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100,
      2
    ) as open_rate
  FROM smart_notifications
  WHERE type = 'DAILY_HOROSCOPE'
  GROUP BY variant;
  ```

---

## ✅ Phase 10: Production Readiness (Week 4)

### Security

- [ ] Environment variables secured (not in git)
- [ ] API keys rotated if exposed
- [ ] Rate limiting configured
- [ ] HTTPS enabled in production

### Monitoring

- [ ] Error alerts configured
- [ ] Performance metrics tracked
- [ ] Database slow query alerts set
- [ ] OpenAI API failure alerts configured

### Backup & Recovery

- [ ] Database backups configured
- [ ] Disaster recovery plan documented
- [ ] Rollback procedure tested

### Documentation

- [ ] API documentation complete
- [ ] Mobile integration guide tested
- [ ] Troubleshooting guide verified
- [ ] Team trained on system

---

## 🎯 Success Criteria

After all tests pass, you should see:

### Week 1
- [x] All 8 tables created
- [x] All notification types working
- [x] AI generation functional
- [x] Spam prevention working
- [x] Event tracking accurate

### Week 2
- [x] Mobile integration complete
- [x] Automated campaigns running
- [x] Performance targets met
- [x] Analytics dashboard working

### Week 3
- [x] A/B testing functional
- [x] 100+ notifications sent successfully
- [x] Open rate > 40%
- [x] Zero critical errors

### Week 4 (Production)
- [x] Open rate > 55%
- [x] Opt-out rate < 8%
- [x] Response time < 500ms
- [x] DAU increased by 15%+

---

## 📊 Final Validation Checklist

Run these queries to verify everything:

```sql
-- 1. Tables exist
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_name IN (
  'smart_notifications',
  'scheduled_notifications',
  'user_notification_preferences',
  'notification_analytics',
  'notification_ab_tests',
  'notification_templates',
  'user_activity_logs',
  'notification_campaigns'
);
-- Expected: 8

-- 2. Sample data exists
SELECT
  (SELECT COUNT(*) FROM smart_notifications) as sent_count,
  (SELECT COUNT(*) FROM user_activity_logs) as activity_count,
  (SELECT COUNT(*) FROM notification_templates) as template_count;
-- Expected: sent_count > 0, template_count >= 5

-- 3. Performance metrics
SELECT
  COUNT(*) as total_sent,
  COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END) as total_opened,
  ROUND(
    COUNT(CASE WHEN opened_at IS NOT NULL THEN 1 END)::numeric / COUNT(*) * 100,
    2
  ) as open_rate
FROM smart_notifications;
-- Expected: open_rate > 40

-- 4. System health
SELECT
  'Notifications' as metric,
  COUNT(*) as value,
  'Last 24h' as period
FROM smart_notifications WHERE sent_at > NOW() - INTERVAL '24 hours'
UNION ALL
SELECT
  'Activities',
  COUNT(*),
  'Last 24h'
FROM user_activity_logs WHERE created_at > NOW() - INTERVAL '24 hours'
UNION ALL
SELECT
  'Scheduled',
  COUNT(*),
  'Pending'
FROM scheduled_notifications WHERE status = 'pending';
-- Expected: All values > 0 for active system
```

---

## ✅ Certification

Once all tests pass, your Smart Notification Engine is:

- ✅ **Fully Functional** - All features working
- ✅ **Production Ready** - Security & performance validated
- ✅ **Scalable** - Load tested and optimized
- ✅ **Intelligent** - AI and ML features operational
- ✅ **Monitored** - Analytics and alerts configured

**Congratulations! You're ready to send intelligent notifications at scale.** 🎉

**Target Achievement:**
- Open Rate: 60%+
- Opt-Out Rate: <5%
- DAU Increase: +40%
- Revenue Impact: +$14K/month

**Let's make it happen!** 🚀
