#!/bin/bash

# 🌍 Script de Validación i18n
# Detecta textos hardcodeados y problemas de traducción
# Parte del Plan Maestro Premium i18n - Oct 31, 2025

echo "🌍 Validando internacionalización..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERROR_COUNT=0

# ============================================
# 1. Detectar textos hardcodeados en Dart
# ============================================
echo "1️⃣  Buscando Text('hardcoded') en archivos Dart..."
echo ""

# Crear archivo temporal
TEMP_FILE=$(mktemp)

# Buscar Text(' con string hardcodeado, excluyendo:
# - AppLocalizations
# - SimpleTranslations
# - Comentarios con // OK:
# - Test files
grep -r "Text('" zodiac_app/lib/ \
  --include="*.dart" \
  --exclude-dir="test" \
  --exclude-dir="*generated*" | \
  grep -v "AppLocalizations" | \
  grep -v "SimpleTranslations" | \
  grep -v "getSimpleTranslation" | \
  grep -v "// OK:" | \
  grep -v "// i18n:" > "$TEMP_FILE"

if [ -s "$TEMP_FILE" ]; then
  echo -e "${RED}❌ Encontrados textos hardcodeados:${NC}"
  echo ""
  head -20 "$TEMP_FILE"
  LINE_COUNT=$(wc -l < "$TEMP_FILE")
  if [ "$LINE_COUNT" -gt 20 ]; then
    echo ""
    echo "... y $(($LINE_COUNT - 20)) más"
  fi
  echo ""
  ERROR_COUNT=$((ERROR_COUNT + 1))
else
  echo -e "${GREEN}✅ No se encontraron textos hardcodeados${NC}"
  echo ""
fi

rm "$TEMP_FILE"

# ============================================
# 2. Verificar que todas las claves existen en todos los idiomas
# ============================================
echo "2️⃣  Verificando paridad de claves entre idiomas..."
echo ""

# Ejecutar script Python de validación
if [ -f "scripts/check_translation_parity.py" ]; then
  python3 scripts/check_translation_parity.py
  if [ $? -ne 0 ]; then
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
else
  echo -e "${YELLOW}⚠️  Script check_translation_parity.py no encontrado${NC}"
  echo ""
fi

# ============================================
# 3. Detectar traducciones vacías
# ============================================
echo "3️⃣  Buscando traducciones vacías..."
echo ""

EMPTY_FOUND=0

for lang in en es de fr it pt; do
  # Usar grep para buscar valores vacíos en JSON
  EMPTY=$(grep -E '": ""' "zodiac_app/assets/l10n/app_$lang.arb" || true)

  if [ ! -z "$EMPTY" ]; then
    echo -e "${RED}❌ Traducciones vacías en app_$lang.arb:${NC}"
    echo "$EMPTY" | head -5
    echo ""
    EMPTY_FOUND=1
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
done

if [ $EMPTY_FOUND -eq 0 ]; then
  echo -e "${GREEN}✅ No se encontraron traducciones vacías${NC}"
  echo ""
fi

# ============================================
# 4. Verificar archivos .arb son JSON válidos
# ============================================
echo "4️⃣  Verificando sintaxis JSON de archivos .arb..."
echo ""

JSON_ERRORS=0

for lang in en es de fr it pt; do
  FILE="zodiac_app/assets/l10n/app_$lang.arb"
  if [ -f "$FILE" ]; then
    # Usar python para validar JSON
    python3 -c "import json; json.load(open('$FILE'))" 2>/dev/null
    if [ $? -ne 0 ]; then
      echo -e "${RED}❌ Sintaxis JSON inválida en $FILE${NC}"
      JSON_ERRORS=1
      ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
  else
    echo -e "${RED}❌ Archivo no encontrado: $FILE${NC}"
    JSON_ERRORS=1
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
done

if [ $JSON_ERRORS -eq 0 ]; then
  echo -e "${GREEN}✅ Todos los archivos .arb tienen sintaxis JSON válida${NC}"
  echo ""
fi

# ============================================
# RESULTADO FINAL
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ERROR_COUNT -eq 0 ]; then
  echo -e "${GREEN}✅ VALIDACIÓN i18n EXITOSA!${NC}"
  echo ""
  echo "Todos los checks pasaron correctamente."
  exit 0
else
  echo -e "${RED}❌ VALIDACIÓN i18n FALLÓ${NC}"
  echo ""
  echo "Se encontraron $ERROR_COUNT problemas."
  echo ""
  echo "Por favor corrige los errores antes de hacer commit."
  exit 1
fi
