#!/bin/bash
# ============================================================================
# AGENT 2: VALIDATOR - Validador de Completitud
# ============================================================================
# Rol: Validar que todas las keys de Cosmic Coach existan en los 6 idiomas
# Input: cosmic_coach_keys.txt
# Output: completeness_report.json
# ============================================================================

set -e

echo "🟢 AGENT 2: VALIDATOR - Iniciando validación..."
echo ""

# Paths
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
L10N_DIR="$BASE_DIR/assets/l10n"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
TEMP_DIR="$OUTPUT_DIR/temp"

# Check prerequisites
if [ ! -f "$OUTPUT_DIR/cosmic_coach_keys.txt" ]; then
  echo "❌ Error: cosmic_coach_keys.txt no encontrado"
  echo "   Ejecuta primero Agent 1: ANALYZER"
  exit 1
fi

mkdir -p "$TEMP_DIR"

cd "$L10N_DIR"

echo "📁 Directorio: $L10N_DIR"
echo ""

# Languages to validate
LANGUAGES=("en" "es" "de" "fr" "it" "pt")
TOTAL_KEYS=$(wc -l < "$OUTPUT_DIR/cosmic_coach_keys.txt" | tr -d ' ')

echo "1️⃣ Validando $TOTAL_KEYS keys en ${#LANGUAGES[@]} idiomas..."
echo ""

# Initialize counters
declare -A MISSING_COUNT
declare -A PRESENT_COUNT
declare -A COMPLETENESS

# Initialize report
cat > "$OUTPUT_DIR/completeness_report.json" << EOF
{
  "analysis_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "total_keys_to_validate": $TOTAL_KEYS,
  "languages": {
EOF

FIRST_LANG=true

# Check each language
for LANG in "${LANGUAGES[@]}"; do
  echo "   🔍 Validando: $LANG"

  ARB_FILE="app_${LANG}.arb"

  if [ ! -f "$ARB_FILE" ]; then
    echo "      ⚠️  Archivo no encontrado: $ARB_FILE"
    MISSING_COUNT[$LANG]=$TOTAL_KEYS
    PRESENT_COUNT[$LANG]=0
    COMPLETENESS[$LANG]=0
    continue
  fi

  # Extract keys from ARB file
  jq -r 'keys[]' "$ARB_FILE" > "$TEMP_DIR/keys_${LANG}.txt"

  # Find missing keys
  grep -vxFf "$TEMP_DIR/keys_${LANG}.txt" "$OUTPUT_DIR/cosmic_coach_keys.txt" > "$TEMP_DIR/missing_${LANG}.txt" || true

  MISSING=$(wc -l < "$TEMP_DIR/missing_${LANG}.txt" | tr -d ' ')
  PRESENT=$((TOTAL_KEYS - MISSING))
  PERCENTAGE=$(echo "scale=2; $PRESENT * 100 / $TOTAL_KEYS" | bc)

  MISSING_COUNT[$LANG]=$MISSING
  PRESENT_COUNT[$LANG]=$PRESENT
  COMPLETENESS[$LANG]=$PERCENTAGE

  # Status emoji
  if [ "$MISSING" -eq 0 ]; then
    STATUS="✅"
  elif [ "$MISSING" -le 5 ]; then
    STATUS="⚠️ "
  else
    STATUS="❌"
  fi

  echo "      $STATUS Presentes: $PRESENT/$TOTAL_KEYS (${PERCENTAGE}%) - Faltantes: $MISSING"

  # Add to JSON (with comma handling)
  if [ "$FIRST_LANG" = true ]; then
    FIRST_LANG=false
  else
    echo "," >> "$OUTPUT_DIR/completeness_report.json"
  fi

  cat >> "$OUTPUT_DIR/completeness_report.json" << EOF
    "$LANG": {
      "present_keys": $PRESENT,
      "missing_keys": $MISSING,
      "completeness_percentage": $PERCENTAGE,
      "status": "$([ $MISSING -eq 0 ] && echo "complete" || echo "incomplete")",
      "missing_keys_list": [
EOF

  # Add missing keys to JSON
  if [ -f "$TEMP_DIR/missing_${LANG}.txt" ] && [ "$MISSING" -gt 0 ]; then
    awk '{printf "        \"%s\"%s\n", $0, (NR==c?"":",") }' c="$MISSING" "$TEMP_DIR/missing_${LANG}.txt" >> "$OUTPUT_DIR/completeness_report.json"
  fi

  cat >> "$OUTPUT_DIR/completeness_report.json" << EOF
      ]
    }
EOF

done

# Close JSON
cat >> "$OUTPUT_DIR/completeness_report.json" << EOF

  },
  "summary": {
    "total_languages": ${#LANGUAGES[@]},
    "fully_complete_languages": $(for lang in "${LANGUAGES[@]}"; do [ "${MISSING_COUNT[$lang]}" -eq 0 ] && echo "1"; done | wc -l | tr -d ' '),
    "languages_with_missing_keys": $(for lang in "${LANGUAGES[@]}"; do [ "${MISSING_COUNT[$lang]}" -gt 0 ] && echo "1"; done | wc -l | tr -d ' ')
  }
}
EOF

echo ""
echo "2️⃣ Generando estadísticas..."
echo ""

# Calculate overall statistics
TOTAL_POSSIBLE=$((TOTAL_KEYS * ${#LANGUAGES[@]}))
TOTAL_PRESENT=0
for LANG in "${LANGUAGES[@]}"; do
  TOTAL_PRESENT=$((TOTAL_PRESENT + PRESENT_COUNT[$LANG]))
done
OVERALL_COMPLETENESS=$(echo "scale=2; $TOTAL_PRESENT * 100 / $TOTAL_POSSIBLE" | bc)

echo "   📊 Estadísticas Globales:"
echo "      - Total posible: $TOTAL_POSSIBLE keys"
echo "      - Total presente: $TOTAL_PRESENT keys"
echo "      - Completitud general: ${OVERALL_COMPLETENESS}%"
echo ""

# Generate text report
cat > "$OUTPUT_DIR/agent2_validator_report.txt" << EOF
=============================================================================
AGENT 2: VALIDATOR - Reporte de Validación
=============================================================================
Fecha: $(date)
Feature: Cosmic Coach
Keys validadas: $TOTAL_KEYS

COMPLETITUD POR IDIOMA:
-----------------------
EOF

for LANG in "${LANGUAGES[@]}"; do
  STATUS_EMOJI="✅"
  [ "${MISSING_COUNT[$LANG]}" -gt 0 ] && STATUS_EMOJI="⚠️ "
  printf "%-6s: %3s Presentes: %4d/%4d (%6.2f%%) - Faltantes: %3d\n" \
    "$LANG" "$STATUS_EMOJI" "${PRESENT_COUNT[$LANG]}" "$TOTAL_KEYS" \
    "${COMPLETENESS[$LANG]}" "${MISSING_COUNT[$LANG]}" >> "$OUTPUT_DIR/agent2_validator_report.txt"
done

cat >> "$OUTPUT_DIR/agent2_validator_report.txt" << EOF

ESTADÍSTICAS GLOBALES:
----------------------
✅ Total posible:           $TOTAL_POSSIBLE keys
✅ Total presente:          $TOTAL_PRESENT keys
✅ Completitud general:     ${OVERALL_COMPLETENESS}%

ARCHIVOS GENERADOS:
-------------------
✅ completeness_report.json    - Reporte detallado en JSON
✅ agent2_validator_report.txt - Este reporte

SIGUIENTE PASO:
---------------
Ejecutar Agents 3-8: EXTRACTORS para generar archivos modulares

NOTAS:
------
EOF

# Add warnings for languages with missing keys
for LANG in "${LANGUAGES[@]}"; do
  if [ "${MISSING_COUNT[$LANG]}" -gt 0 ]; then
    echo "⚠️  $LANG tiene ${MISSING_COUNT[$LANG]} keys faltantes - se marcarán como MISSING" >> "$OUTPUT_DIR/agent2_validator_report.txt"
  fi
done

cat "$OUTPUT_DIR/agent2_validator_report.txt"

echo ""
echo "✅ AGENT 2: VALIDATOR - Completado exitosamente"
echo ""
echo "📊 Resumen:"
echo "   - Completitud general: ${OVERALL_COMPLETENESS}%"
echo "   - Idiomas completos: $(for lang in "${LANGUAGES[@]}"; do [ "${MISSING_COUNT[$lang]}" -eq 0 ] && echo -n "1 "; done | wc -w | tr -d ' ')/${#LANGUAGES[@]}"
echo "   - Reportes generados en: $OUTPUT_DIR"
echo ""
