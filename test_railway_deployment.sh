#!/bin/bash

echo "=== RAILWAY DEPLOYMENT VERIFICATION ==="
echo ""
echo "1. Checking backend version..."
VERS=$(curl -s https://zodiac-backend-api-production-8ded.up.railway.app/health | jq -r '.version')
UPTIME=$(curl -s https://zodiac-backend-api-production-8ded.up.railway.app/health | jq -r '.uptime')
echo "   Version: $VERS"
echo "   Uptime: $UPTIME seconds"
echo ""

if [[ "$VERS" == "2.2.0"* ]]; then
  echo "✅ NEW VERSION DEPLOYED!"
else
  echo "⏸️  Still on old version - waiting for Railway..."
fi

echo ""
echo "2. Testing horoscopeData endpoint..."
RESPONSE=$(curl -s -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/ai-coach/chat/message \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test-nov19","message":"Hola","userId":"test","zodiacSign":"Capricornio","language":"es"}')

HAS_HOROSCOPE=$(echo "$RESPONSE" | jq 'has("horoscopeData")')
echo "   Has horoscopeData: $HAS_HOROSCOPE"

if [ "$HAS_HOROSCOPE" = "true" ]; then
  echo "   ✅ horoscopeData PRESENT in response!"
  echo ""
  echo "   Data preview:"
  echo "$RESPONSE" | jq '.horoscopeData'
else
  echo "   ❌ horoscopeData MISSING"
  echo "   Response keys:"
  echo "$RESPONSE" | jq 'keys'
fi

echo ""
echo "=== END VERIFICATION ==="
