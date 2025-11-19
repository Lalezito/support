#!/bin/bash
# ============================================================================
# AGENT 9: QUALITY_CHECKER (FIXED) - Verificador de Calidad
# ============================================================================

set -e

echo "🔍 AGENT 9: QUALITY_CHECKER - Iniciando verificación de calidad..."
echo ""

# Paths
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
FEATURES_DIR="$OUTPUT_DIR/features/cosmic_coach"

cd "$OUTPUT_DIR"

echo "📁 Directorio: $FEATURES_DIR"
echo ""

if [ ! -d "$FEATURES_DIR" ]; then
  echo "❌ Error: Directorio de features no encontrado"
  exit 1
fi

echo "1️⃣ Verificando archivos generados..."
echo ""

LANGUAGES=("en" "es" "de" "fr" "it" "pt")
ALL_VALID=true

# Start quality report
cat > quality_report.json << 'EOF_START'
{
  "validation_date": "
EOF_START
date -u +"%Y-%m-%dT%H:%M:%SZ" >> quality_report.json
cat >> quality_report.json << 'EOF_MID'
",
  "files": {
EOF_MID

FIRST_FILE=true

for LANG in "${LANGUAGES[@]}"; do
  FILE="$FEATURES_DIR/cosmic_coach_${LANG}.arb"

  echo "   Verificando: cosmic_coach_${LANG}.arb"

  if [ ! -f "$FILE" ]; then
    echo "      ❌ Archivo no encontrado"
    ALL_VALID=false
    continue
  fi

  # Check JSON validity
  if jq empty "$FILE" 2>/dev/null; then
    JSON_VALID=true
    KEY_COUNT=$(jq '. | length' "$FILE")
    FILE_SIZE=$(du -h "$FILE" | awk '{print $1}')
    echo "      ✅ Válido: $KEY_COUNT keys, $FILE_SIZE"
  else
    JSON_VALID=false
    KEY_COUNT=0
    FILE_SIZE="0"
    echo "      ❌ JSON inválido"
    ALL_VALID=false
  fi

  # Add to report
  if [ "$FIRST_FILE" = true ]; then
    FIRST_FILE=false
  else
    echo "," >> quality_report.json
  fi

  cat >> quality_report.json << EOF
    "cosmic_coach_${LANG}.arb": {
      "valid_json": $JSON_VALID,
      "key_count": $KEY_COUNT,
      "file_size": "$FILE_SIZE"
    }
EOF
done

# Close JSON
cat >> quality_report.json << 'EOF_END'
  },
  "overall_status": "
EOF_END

if [ "$ALL_VALID" = true ]; then
  echo "PASS" >> quality_report.json
else
  echo "FAIL" >> quality_report.json
fi

cat >> quality_report.json << 'EOF_FINAL'
"
}
EOF_FINAL

echo ""
echo "2️⃣ Verificando consistencia entre idiomas..."
echo ""

# Get EN key count as reference
EN_FILE="$FEATURES_DIR/cosmic_coach_en.arb"
EN_KEYS=$(jq -r 'keys[]' "$EN_FILE" | wc -l | tr -d ' ')

echo "   Base (EN): $EN_KEYS keys"
echo ""

for LANG in es de fr it pt; do
  FILE="$FEATURES_DIR/cosmic_coach_${LANG}.arb"
  if [ -f "$FILE" ]; then
    LANG_KEYS=$(jq -r 'keys[]' "$FILE" | wc -l | tr -d ' ')
    DIFF=$((EN_KEYS - LANG_KEYS))

    if [ "$DIFF" -eq 0 ]; then
      echo "   ✅ $LANG: $LANG_KEYS keys (igual que EN)"
    elif [ "$DIFF" -gt 0 ]; then
      echo "   ⚠️  $LANG: $LANG_KEYS keys (-$DIFF vs EN)"
    else
      EXTRA=$((-DIFF))
      echo "   ⚠️  $LANG: $LANG_KEYS keys (+$EXTRA vs EN)"
    fi
  fi
done

echo ""
echo "✅ AGENT 9: QUALITY_CHECKER - Completado"
echo ""
echo "📊 Reporte generado: quality_report.json"
echo ""

# Display summary
if [ "$ALL_VALID" = true ]; then
  echo "✅ TODOS LOS ARCHIVOS SON VÁLIDOS"
else
  echo "⚠️  ALGUNOS ARCHIVOS TIENEN PROBLEMAS"
fi
echo ""
