#!/bin/bash

echo "⏳ Monitoreando Railway deployment..."

for i in {1..6}; do
  echo ""
  echo "=== Check $i/6 - $(date +%H:%M:%S) ==="

  VERSION=$(curl -s https://zodiac-backend-api-production-8ded.up.railway.app/health | jq -r '.version')
  UPTIME=$(curl -s https://zodiac-backend-api-production-8ded.up.railway.app/health | jq -r '.uptime | floor')

  echo "Version: $VERSION"
  echo "Uptime: ${UPTIME}s"

  if [[ "$VERSION" == "2.2.0"* ]]; then
    echo ""
    echo "✅ ✅ ✅ NEW VERSION DEPLOYED! ✅ ✅ ✅"
    break
  else
    if [ $i -lt 6 ]; then
      echo "⏸️  Esperando rebuild... (check $i/6)"
      sleep 20
    fi
  fi
done

echo ""
echo "=== Verificación final horoscopeData ==="
cd /Users/alejandrocaceres/Desktop/appstore.zodia
./test_railway_deployment.sh
