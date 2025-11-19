#!/bin/bash
curl -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/ai-coach/chat/message \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test","message":"Hola","userId":"test","zodiacSign":"Capricornio","language":"es"}' \
  | jq '.'
