# 📱 PHASE 2: FCM TOKENS TABLE SETUP

**Status**: ⏳ Ready to execute
**Estimated Time**: 3 minutes
**Priority**: 🔴 HIGH - Required for push notifications

---

## 🎯 Quick Setup Instructions

### Step 1: Access Railway Database (1 min)

1. Go to: https://railway.app
2. Login and select project: **zodiac-backend-api-production**
3. Click on **PostgreSQL** service
4. Click on **Data** tab

### Step 2: Execute SQL (1 min)

**Copy and paste this SQL into the query editor:**

```sql
-- Create FCM tokens table
CREATE TABLE IF NOT EXISTS fcm_tokens (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255),
  fcm_token TEXT NOT NULL,
  device_type VARCHAR(50) DEFAULT 'unknown',
  device_id VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices
CREATE INDEX IF NOT EXISTS idx_fcm_tokens_user_id ON fcm_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_fcm_tokens_fcm_token ON fcm_tokens(fcm_token);
CREATE INDEX IF NOT EXISTS idx_fcm_tokens_created_at ON fcm_tokens(created_at);

-- Create trigger function
CREATE OR REPLACE FUNCTION update_fcm_tokens_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger
DROP TRIGGER IF EXISTS trigger_update_fcm_tokens_updated_at ON fcm_tokens;
CREATE TRIGGER trigger_update_fcm_tokens_updated_at
  BEFORE UPDATE ON fcm_tokens
  FOR EACH ROW
  EXECUTE FUNCTION update_fcm_tokens_updated_at();
```

Click **"Run"** or **"Execute"**.

### Step 3: Verify Table Created (1 min)

Run this query to verify:

```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'fcm_tokens'
ORDER BY ordinal_position;
```

**Expected**: Should show 7 columns (id, user_id, fcm_token, device_type, device_id, created_at, updated_at)

---

## ✅ Success Criteria

- [ ] Table `fcm_tokens` created without errors
- [ ] Query returns 7 columns
- [ ] Indices created successfully
- [ ] Trigger created successfully

---

## 🧪 Test Backend Endpoint

Once table is created, test from terminal:

```bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/notifications/register-token \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "fcm_token": "test_token_xyz",
    "device_type": "iOS",
    "device_id": "test_device_001"
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "FCM token registered successfully"
}
```

**NOT Expected**: `{"error":"Failed to register token"}` (this means table not created)

---

## 🚨 Troubleshooting

### Error: "relation fcm_tokens already exists"

**Solution**: Table already created ✅ You're done!

### Error: Permission denied

**Solution**: Use Railway dashboard Data tab instead of Query tab

### Backend still returns 500

**Solution**:
1. Verify table created: `SELECT * FROM fcm_tokens LIMIT 1;`
2. Check Railway deployment logs
3. Force redeploy backend if needed

---

**File Created**: October 7, 2025
**Ref**: `.claude/BACKEND_FIX_PLAN.md` Phase 2
**Full SQL**: `backend/flutter-horoscope-backend/migrations/create_fcm_tokens_table.sql`
