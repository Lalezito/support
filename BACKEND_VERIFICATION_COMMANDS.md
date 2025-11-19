# BACKEND VERIFICATION COMMANDS
Quick reference for backend health checks and troubleshooting

## Quick Health Check

```bash
# Run the automated health check script
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
./quick-health-check.sh
```

## Manual Endpoint Tests

### 1. Health Check
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/health | jq
```

### 2. Ping Check
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/ping | jq
```

### 3. Get All Horoscopes
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/coaching/getAllHoroscopes | jq
```

### 4. Get Weekly Horoscopes
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/weekly/getAllWeeklyHoroscopes | jq
```

### 5. Trigger Manual Daily Generation (Admin)
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/daily \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" \
  -H "Content-Type: application/json"
```

### 6. Trigger Manual Weekly Generation (Admin)
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/weekly \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" \
  -H "Content-Type: application/json"
```

### 7. Check Generation Status (Admin)
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/status \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" | jq
```

### 8. Test OpenAI Connection (Admin)
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/test \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" \
  -H "Content-Type: application/json"
```

### 9. System Analytics (Admin)
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/admin/analytics \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" | jq
```

### 10. Detailed System Status (Admin)
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/admin/system-status \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" | jq
```

## Performance Testing

### Measure Response Time
```bash
curl -w "\nTime Total: %{time_total}s\nHTTP Code: %{http_code}\n" \
  -o /dev/null -s \
  https://zodiac-backend-api-production-8ded.up.railway.app/health
```

### Concurrent Request Test (10 requests)
```bash
for i in {1..10}; do
  curl -s https://zodiac-backend-api-production-8ded.up.railway.app/ping &
done
wait
```

### Load Test with Apache Bench (100 requests, 10 concurrent)
```bash
ab -n 100 -c 10 https://zodiac-backend-api-production-8ded.up.railway.app/health
```

## Local Development Commands

### Start Development Server
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
npm run dev
```

### Start Production Mode Locally
```bash
npm run start
```

### Start Safe Mode
```bash
npm run start:safe
```

### Start Minimal Test Server
```bash
npm run start:minimal
```

## Database Commands

### Test Database Connection
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
node -e "const db = require('./src/config/db'); db.testConnection().then(console.log).catch(console.error);"
```

### Reset Database (DANGER)
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
node reset-database.js
```

### Run Migrations
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
node migrations/run_all_migrations.js
```

## Security Commands

### Check for Vulnerabilities
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
npm audit
```

### Fix Vulnerabilities (Auto)
```bash
npm audit fix
```

### Fix Vulnerabilities (Force)
```bash
npm audit fix --force
```

### Update Specific Vulnerable Package
```bash
npm update validator express-validator
```

### Check for Outdated Packages
```bash
npm outdated
```

## Railway Commands

### View Railway Logs
```bash
railway logs --tail
```

### Deploy to Railway
```bash
railway up
```

### Check Railway Status
```bash
railway status
```

### Set Environment Variable
```bash
railway variables set VARIABLE_NAME=value
```

### Get Environment Variables
```bash
railway variables
```

## Monitoring Commands

### Watch Logs (Local)
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
tail -f logs/*.log
```

### Check Server Process (Local)
```bash
ps aux | grep node
```

### Check Port Usage
```bash
lsof -i :3000
```

### Kill Process on Port 3000
```bash
kill -9 $(lsof -t -i:3000)
```

## Testing Commands

### Test AI Coach API
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend
node test-ai-coach-api.js
```

### Test Personalization System
```bash
node test-personalization-system.js
```

### Test Goal Planner
```bash
node test-goal-planner.js
```

### Test Neural API
```bash
node test-neural-api.js
```

### Test Railway Deployment
```bash
node test-railway-deployment.js
```

## Backup Commands

### Backup Database
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database
```bash
psql $DATABASE_URL < backup_file.sql
```

## Circuit Breaker Status

### Check Circuit Breaker Health (via API)
```bash
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/admin/system-status \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" | jq '.circuitBreakers'
```

## Redis Commands (when connected)

### Check Redis Connection
```bash
redis-cli -h YOUR_REDIS_HOST -p YOUR_REDIS_PORT ping
```

### Get All Keys
```bash
redis-cli -h YOUR_REDIS_HOST -p YOUR_REDIS_PORT keys "*"
```

### Flush All Cache
```bash
redis-cli -h YOUR_REDIS_HOST -p YOUR_REDIS_PORT FLUSHALL
```

## Environment Files

### Production Environment
```bash
cat /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend/.env.production
```

### Local Environment
```bash
cat /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend/.env.local
```

### Template Environment
```bash
cat /Users/alejandrocaceres/Desktop/appstore.zodia/backend/flutter-horoscope-backend/.env.template
```

## Quick Fixes

### Restart Railway Service
```bash
railway restart
```

### Clear npm Cache
```bash
npm cache clean --force
```

### Reinstall Dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

### Force Cron Job Execution (Manual)
```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/admin/force-weekly \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE"
```

## Troubleshooting

### Issue: Empty Horoscopes Database
**Solution:**
```bash
# Trigger manual generation
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/daily \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE"
```

### Issue: Circuit Breaker Open
**Solution:**
```bash
# Check admin status to see circuit breaker state
curl https://zodiac-backend-api-production-8ded.up.railway.app/api/admin/system-status \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE" | jq '.circuitBreakers'

# Wait for automatic reset or restart service
```

### Issue: Rate Limited
**Solution:**
```bash
# Wait for rate limit window to reset
# Or contact admin to reset rate limits
```

### Issue: Database Connection Failed
**Solution:**
```bash
# Check Railway database status
railway status

# Verify DATABASE_URL is correct
echo $DATABASE_URL
```

### Issue: OpenAI API Errors
**Solution:**
```bash
# Test OpenAI connection
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/generate/test \
  -H "x-admin-key: YOUR_ADMIN_KEY_HERE"

# Check OpenAI API key is valid
# Verify OpenAI account has credits
```

## Security Checklist

- [ ] Rotate DATABASE_URL
- [ ] Rotate OPENAI_API_KEY
- [ ] Rotate ADMIN_KEY
- [ ] Run npm audit fix
- [ ] Update vulnerable dependencies
- [ ] Remove .env from git if committed
- [ ] Enable Redis for production
- [ ] Set up monitoring alerts
- [ ] Configure Sentry for error tracking
- [ ] Enable AWS Secrets Manager

## Notes

- Replace `YOUR_ADMIN_KEY_HERE` with actual admin key from .env
- All admin endpoints require `x-admin-key` header
- Production URL: https://zodiac-backend-api-production-8ded.up.railway.app
- Local URL: http://localhost:3000

## Related Documentation

- Main Health Report: `/BACKEND_HEALTH_REPORT_OCT29_2025.md`
- Quick Health Script: `/backend/flutter-horoscope-backend/quick-health-check.sh`
- Deployment Checklist: `/backend/flutter-horoscope-backend/DEPLOYMENT_CHECKLIST.md`
- Health Endpoint Docs: `/backend/flutter-horoscope-backend/HEALTH_ENDPOINT_DOCUMENTATION.md`
