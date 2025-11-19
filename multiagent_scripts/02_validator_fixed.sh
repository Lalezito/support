#!/bin/bash
# ============================================================================
# AGENT 2: VALIDATOR (FIXED) - Validador de Completitud
# ============================================================================

set -e

echo "🟢 AGENT 2: VALIDATOR - Iniciando validación..."
echo ""

# Paths
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
L10N_DIR="$BASE_DIR/assets/l10n"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
TEMP_DIR="$OUTPUT_DIR/temp"

mkdir -p "$TEMP_DIR"
cd "$L10N_DIR"

echo "📁 Directorio: $L10N_DIR"
echo ""

# Read cosmic coach keys
KEYS_FILE="$OUTPUT_DIR/cosmic_coach_keys.txt"
if [ ! -f "$KEYS_FILE" ]; then
  echo "❌ Error: cosmic_coach_keys.txt no encontrado"
  echo "   Ejecuta primero Agent 1: ANALYZER"
  exit 1
fi

TOTAL_KEYS=$(wc -l < "$KEYS_FILE" | tr -d ' ')
echo "1️⃣ Validando $TOTAL_KEYS keys en 6 idiomas..."
echo ""

LANGUAGES=("en" "es" "de" "fr" "it" "pt")

# Start JSON report
cat > "$OUTPUT_DIR/completeness_report.json" << 'EOF_START'
{
  "analysis_date": "
EOF_START
date -u +"%Y-%m-%dT%H:%M:%SZ" >> "$OUTPUT_DIR/completeness_report.json"
cat >> "$OUTPUT_DIR/completeness_report.json" << 'EOF_MID'
",
  "total_keys_to_validate":
EOF_MID
echo "$TOTAL_KEYS," >> "$OUTPUT_DIR/completeness_report.json"
cat >> "$OUTPUT_DIR/completeness_report.json" << 'EOF_LANGS'
  "languages": {
EOF_LANGS

FIRST_LANG=true

# Check each language
for LANG in "${LANGUAGES[@]}"; do
  echo "   🔍 Validando: $LANG"

  ARB_FILE="app_${LANG}.arb"

  if [ ! -f "$ARB_FILE" ]; then
    echo "      ⚠️  Archivo no encontrado: $ARB_FILE"
    continue
  fi

  # Extract keys from ARB file
  jq -r 'keys[]' "$ARB_FILE" > "$TEMP_DIR/keys_${LANG}.txt"

  # Find missing keys
  grep -vxFf "$TEMP_DIR/keys_${LANG}.txt" "$KEYS_FILE" > "$TEMP_DIR/missing_${LANG}.txt" || true

  MISSING=$(wc -l < "$TEMP_DIR/missing_${LANG}.txt" | tr -d ' ')
  PRESENT=$((TOTAL_KEYS - MISSING))
  PERCENTAGE=$(echo "scale=2; $PRESENT * 100 / $TOTAL_KEYS" | bc)

  # Status emoji
  if [ "$MISSING" -eq 0 ]; then
    STATUS="✅"
  elif [ "$MISSING" -le 5 ]; then
    STATUS="⚠️ "
  else
    STATUS="❌"
  fi

  echo "      $STATUS Presentes: $PRESENT/$TOTAL_KEYS (${PERCENTAGE}%) - Faltantes: $MISSING"

  # Add to JSON
  if [ "$FIRST_LANG" = true ]; then
    FIRST_LANG=false
  else
    echo "," >> "$OUTPUT_DIR/completeness_report.json"
  fi

  cat >> "$OUTPUT_DIR/completeness_report.json" << EOF
    "$LANG": {
      "present": $PRESENT,
      "missing": $MISSING,
      "total": $TOTAL_KEYS,
      "completeness_percentage": $PERCENTAGE
    }
EOF

  # Save missing keys list
  if [ "$MISSING" -gt 0 ]; then
    cp "$TEMP_DIR/missing_${LANG}.txt" "$OUTPUT_DIR/missing_keys_${LANG}.txt"
  fi
done

# Close JSON
cat >> "$OUTPUT_DIR/completeness_report.json" << 'EOF_END'
  },
  "summary": "Validation complete for 6 languages"
}
EOF_END

echo ""
echo "2️⃣ Resumen de validación:"
echo ""

for LANG in "${LANGUAGES[@]}"; do
  if [ -f "$TEMP_DIR/missing_${LANG}.txt" ]; then
    MISSING=$(wc -l < "$TEMP_DIR/missing_${LANG}.txt" | tr -d ' ')
    PRESENT=$((TOTAL_KEYS - MISSING))
    PERCENTAGE=$(echo "scale=1; $PRESENT * 100 / $TOTAL_KEYS" | bc)

    if [ "$MISSING" -eq 0 ]; then
      echo "   ✅ $LANG: 100% completo"
    elif [ "$MISSING" -le 5 ]; then
      echo "   ⚠️  $LANG: ${PERCENTAGE}% completo (${MISSING} faltantes)"
    else
      echo "   ❌ $LANG: ${PERCENTAGE}% completo (${MISSING} faltantes)"
    fi
  fi
done

echo ""
echo "✅ AGENT 2: VALIDATOR - Completado"
echo ""
echo "📊 Archivos generados:"
echo "   - completeness_report.json"
echo "   - missing_keys_*.txt (para cada idioma con faltantes)"
echo ""
