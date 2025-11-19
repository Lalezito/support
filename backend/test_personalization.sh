#!/bin/bash

# ✨ TESTING SCRIPT - Cosmic Coach Astrological Personalization
# Fecha: 19 Noviembre 2025
# Propósito: Verificar que la personalización funciona correctamente

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Backend URL
BACKEND_URL=${BACKEND_URL:-"https://zodiac-backend-api-production-8ded.up.railway.app"}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}✨ COSMIC COACH - Personalization Testing${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 1: Leo vs Aries - Mismo mensaje, respuestas diferentes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${YELLOW}📋 Test 1: Personalización por Signo Zodiacal${NC}"
echo -e "   Enviando mismo mensaje a Leo y Aries..."
echo ""

# Leo request
echo -e "${GREEN}🦁 LEO Request:${NC}"
LEO_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo puedo mejorar mi día hoy?",
    "userId": "test_leo_user",
    "zodiacSign": "Leo",
    "language": "es"
  }')

echo "$LEO_RESPONSE" | jq -r '.response' | head -c 500
echo -e "\n${BLUE}...(truncated)${NC}\n"

# Verificar keywords Leo
if echo "$LEO_RESPONSE" | grep -qi "leo\|carisma\|liderazgo\|14:00\|20:00"; then
  echo -e "${GREEN}✅ PASS: Leo response mentions zodiac sign or horoscope keywords${NC}"
else
  echo -e "${RED}❌ FAIL: Leo response doesn't mention personalized data${NC}"
fi
echo ""

# Aries request
echo -e "${GREEN}🔥 ARIES Request:${NC}"
ARIES_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo puedo mejorar mi día hoy?",
    "userId": "test_aries_user",
    "zodiacSign": "Aries",
    "language": "es"
  }')

echo "$ARIES_RESPONSE" | jq -r '.response' | head -c 500
echo -e "\n${BLUE}...(truncated)${NC}\n"

# Verificar keywords Aries
if echo "$ARIES_RESPONSE" | grep -qi "aries\|energía\|acción\|08:00\|18:00\|marte"; then
  echo -e "${GREEN}✅ PASS: Aries response mentions zodiac sign or horoscope keywords${NC}"
else
  echo -e "${RED}❌ FAIL: Aries response doesn't mention personalized data${NC}"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 2: Memoria Conversacional
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 Test 2: Memoria Conversacional${NC}"
echo -e "   Enviando 2 mensajes secuenciales..."
echo ""

# First message
echo -e "${GREEN}📨 Mensaje 1: Presentación${NC}"
curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, me llamo Alejandro y soy desarrollador de apps móviles",
    "userId": "test_memory_user",
    "zodiacSign": "Leo",
    "language": "es"
  }' | jq -r '.response' | head -c 300
echo -e "\n${BLUE}...(truncated)${NC}\n"

sleep 2

# Second message (should reference first)
echo -e "${GREEN}📨 Mensaje 2: Pregunta sobre trabajo${NC}"
MEMORY_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué consejo tienes para mi trabajo hoy?",
    "userId": "test_memory_user",
    "zodiacSign": "Leo",
    "language": "es"
  }')

echo "$MEMORY_RESPONSE" | jq -r '.response' | head -c 500
echo -e "\n${BLUE}...(truncated)${NC}\n"

# Verificar memoria
if echo "$MEMORY_RESPONSE" | grep -qi "alejandro\|desarrollador\|apps\|móviles"; then
  echo -e "${GREEN}✅ PASS: AI remembers context from previous message${NC}"
else
  echo -e "${RED}❌ FAIL: AI doesn't remember previous context${NC}"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 3: Multiidioma
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 Test 3: Multiidioma (Inglés)${NC}"
echo -e "   Leo en inglés..."
echo ""

EN_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I improve my day today?",
    "userId": "test_english_user",
    "zodiacSign": "Leo",
    "language": "en"
  }')

echo "$EN_RESPONSE" | jq -r '.response' | head -c 500
echo -e "\n${BLUE}...(truncated)${NC}\n"

# Verificar inglés
if echo "$EN_RESPONSE" | grep -qi "leo\|sun\|jupiter\|leadership\|charisma"; then
  echo -e "${GREEN}✅ PASS: English response is personalized${NC}"
else
  echo -e "${RED}❌ FAIL: English response not personalized${NC}"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 4: Fallback sin horóscopo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 Test 4: Fallback sin Horóscopo${NC}"
echo -e "   Usando signo sin datos en DB (Gemini/Francés)..."
echo ""

NO_HOROSCOPE_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment puis-je améliorer ma journée?",
    "userId": "test_no_horoscope_user",
    "zodiacSign": "Gemini",
    "language": "fr"
  }')

echo "$NO_HOROSCOPE_RESPONSE" | jq -r '.response' | head -c 400
echo -e "\n${BLUE}...(truncated)${NC}\n"

# Verificar que funciona sin error
if echo "$NO_HOROSCOPE_RESPONSE" | jq -e '.response' > /dev/null 2>&1; then
  echo -e "${GREEN}✅ PASS: Graceful degradation - works without horoscope${NC}"
else
  echo -e "${RED}❌ FAIL: Error when no horoscope available${NC}"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Test 5: Performance (Response Time)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 Test 5: Performance (Response Time)${NC}"
echo -e "   Midiendo tiempo de respuesta..."
echo ""

START_TIME=$(date +%s%3N)
curl -s -X POST "${BACKEND_URL}/api/horoscope-chat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quick test",
    "userId": "test_performance_user",
    "zodiacSign": "Leo",
    "language": "es"
  }' > /dev/null
END_TIME=$(date +%s%3N)

RESPONSE_TIME=$((END_TIME - START_TIME))

echo -e "   Response time: ${BLUE}${RESPONSE_TIME}ms${NC}"

if [ $RESPONSE_TIME -lt 5000 ]; then
  echo -e "${GREEN}✅ PASS: Response time < 5s${NC}"
else
  echo -e "${RED}❌ FAIL: Response time > 5s (too slow)${NC}"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESUMEN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Testing Complete${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Para ver logs detallados en Railway:"
echo -e "  ${YELLOW}railway logs --tail 100${NC}"
echo ""
echo -e "Para verificar cache de Redis:"
echo -e "  ${YELLOW}redis-cli KEYS daily_horoscope:*${NC}"
echo ""
