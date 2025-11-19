#!/bin/bash

echo "Testing horoscopeData in backend response..."

curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/ai-coach/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-horoscope-nov19",
    "message": "Como esta mi dia?",
    "userId": "test-user-nov19",
    "zodiacSign": "Capricornio",
    "language": "es"
  }' | jq '{
    hasHoroscopeData: has("horoscopeData"),
    horoscopeData: .horoscopeData,
    contentPreview: (.content | split(" ") | .[0:10] | join(" "))
  }'
