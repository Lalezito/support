#!/bin/bash

# Health check script for production monitoring

API_URL="https://api.zodiacapp.com"
BACKEND_URL="https://flutter-horoscope-backend-production.up.railway.app"

echo "🔍 Running health checks..."

# Check API
if curl -s --max-time 10 "$API_URL/health" > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API is down"
    exit 1
fi

# Check backend
if curl -s --max-time 10 "$BACKEND_URL/health" > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is down"
    exit 1
fi

# Check database connectivity (if exposed)
# Add more checks as needed

echo "🎉 All systems healthy!"