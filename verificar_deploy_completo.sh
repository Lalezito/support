#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  VERIFICACIÓN COMPLETA POST-DEPLOY - Railway + Flutter   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 1. Verificar Railway Health
echo "📡 1. VERIFICANDO RAILWAY BACKEND..."
echo "   URL: https://zodiac-backend-api-production-8ded.up.railway.app/health"
echo ""

HEALTH=$(curl -s https://zodiac-backend-api-production-8ded.up.railway.app/health)
VERSION=$(echo "$HEALTH" | jq -r '.version')
UPTIME=$(echo "$HEALTH" | jq -r '.uptime | floor')

echo "   Version: $VERSION"
echo "   Uptime: ${UPTIME}s"
echo ""

if [[ "$VERSION" == "2.2.0"* ]]; then
  echo "   ✅ VERSION NUEVA DEPLOYADA!"
else
  echo "   ❌ Aún en version vieja: $VERSION"
  exit 1
fi

if [ "$UPTIME" -lt 300 ]; then
  echo "   ✅ Uptime bajo (recién deployado)"
else
  echo "   ⚠️  Uptime alto (${UPTIME}s) - puede ser deployment viejo"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 2. Verificar horoscopeData en Response
echo "📊 2. PROBANDO ENDPOINT AI COACH..."
echo ""

RESPONSE=$(curl -s -X POST https://zodiac-backend-api-production-8ded.up.railway.app/api/ai-coach/chat/message \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test-verificacion","message":"Hola","userId":"test","zodiacSign":"Capricornio","language":"es"}')

HAS_HOROSCOPE=$(echo "$RESPONSE" | jq 'has("horoscopeData")')

if [ "$HAS_HOROSCOPE" = "true" ]; then
  echo "   ✅ horoscopeData PRESENTE en response!"
  echo ""
  echo "   Datos recibidos:"
  echo "$RESPONSE" | jq '.horoscopeData' | head -15
else
  echo "   ❌ horoscopeData NO encontrado"
  echo ""
  echo "   Response keys:"
  echo "$RESPONSE" | jq 'keys'
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 3. Checklist Features Flutter
echo "📱 3. CHECKLIST FEATURES FLUTTER"
echo ""
echo "   Ahora que backend está listo, verifica en iPhone:"
echo ""
echo "   [ ] Abrir Cosmic Coach"
echo "   [ ] Enviar mensaje: '¿Cómo está mi día?'"
echo ""
echo "   VERIFICAR:"
echo "   [ ] ✅ Header pill aparece: ⚡ Alta • 🎨 Dorado"
echo "   [ ] ✅ Daily highlights card ANTES del mensaje AI"
echo "   [ ] ✅ No mezcla de idiomas (todo en español)"
echo "   [ ] ✅ Respuestas personalizadas con datos astrológicos"
echo "   [ ] ✅ Botón favoritos funciona"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 4. Comando Hot Restart Flutter
echo "🔄 4. HOT RESTART FLUTTER APP"
echo ""
echo "   Si la app YA está corriendo en iPhone:"
echo "   → En terminal Flutter, presiona: R"
echo ""
echo "   Si NO está corriendo:"
echo "   → cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
echo "   → flutter run -d 00008150-0015244A2288401C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 5. Resumen Final
if [[ "$VERSION" == "2.2.0"* ]] && [ "$HAS_HOROSCOPE" = "true" ]; then
  echo "╔═══════════════════════════════════════════════════════════╗"
  echo "║                                                           ║"
  echo "║  ✅ ✅ ✅  BACKEND LISTO PARA TESTING  ✅ ✅ ✅           ║"
  echo "║                                                           ║"
  echo "║  • Version 2.2.0 deployada                                ║"
  echo "║  • horoscopeData disponible                               ║"
  echo "║  • Endpoints funcionando                                  ║"
  echo "║                                                           ║"
  echo "║  → PRÓXIMO: Hot restart Flutter y probar features        ║"
  echo "║                                                           ║"
  echo "╚═══════════════════════════════════════════════════════════╝"
  exit 0
else
  echo "╔═══════════════════════════════════════════════════════════╗"
  echo "║                                                           ║"
  echo "║  ⚠️  BACKEND AÚN NO ESTÁ LISTO                           ║"
  echo "║                                                           ║"
  echo "║  Espera unos minutos más y vuelve a ejecutar:            ║"
  echo "║  ./verificar_deploy_completo.sh                           ║"
  echo "║                                                           ║"
  echo "╚═══════════════════════════════════════════════════════════╝"
  exit 1
fi
