#!/bin/bash
# ============================================================================
# AGENT 9: QUALITY_CHECKER - Verificador de Calidad
# ============================================================================
# Rol: Validar sintaxis JSON y consistencia de archivos generados
# Input: cosmic_coach_{lang}.arb (6 archivos)
# Output: quality_report.json
# ============================================================================

set -e

echo "🔍 AGENT 9: QUALITY_CHECKER - Iniciando verificación de calidad..."
echo ""

# Paths
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
FEATURE_DIR="$OUTPUT_DIR/features/cosmic_coach"
TEMP_DIR="$OUTPUT_DIR/temp"

mkdir -p "$TEMP_DIR"

echo "📁 Directorio: $FEATURE_DIR"
echo ""

# Languages
LANGUAGES=("en" "es" "de" "fr" "it" "pt")
LANG_NAMES=("English" "Español" "Deutsch" "Français" "Italiano" "Português")

# Quality check results
declare -A JSON_VALID
declare -A KEY_COUNT
declare -A FILE_SIZE
declare -A MISSING_KEYS
declare -A QUALITY_SCORE

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

echo "1️⃣ Verificando existencia de archivos..."
echo ""

ALL_FILES_EXIST=true
for LANG in "${LANGUAGES[@]}"; do
  FILE="$FEATURE_DIR/cosmic_coach_${LANG}.arb"
  if [ -f "$FILE" ]; then
    echo "   ✅ $LANG: cosmic_coach_${LANG}.arb encontrado"
  else
    echo "   ❌ $LANG: cosmic_coach_${LANG}.arb NO ENCONTRADO"
    ALL_FILES_EXIST=false
  fi
done

echo ""

if [ "$ALL_FILES_EXIST" = false ]; then
  echo "❌ Error: No todos los archivos fueron generados"
  echo "   Ejecuta primero Agents 3-8: EXTRACTORS"
  exit 1
fi

echo "2️⃣ Validando sintaxis JSON..."
echo ""

for i in "${!LANGUAGES[@]}"; do
  LANG="${LANGUAGES[$i]}"
  LANG_NAME="${LANG_NAMES[$i]}"
  FILE="$FEATURE_DIR/cosmic_coach_${LANG}.arb"

  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

  echo "   🔍 Validando: $LANG_NAME ($LANG)"

  # Validate JSON syntax
  if jq empty "$FILE" 2>/dev/null; then
    echo "      ✅ JSON válido"
    JSON_VALID[$LANG]=true
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
  else
    echo "      ❌ JSON inválido"
    JSON_VALID[$LANG]=false
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
  fi

  # Count keys
  KEYS=$(jq 'keys | length' "$FILE" 2>/dev/null || echo "0")
  KEY_COUNT[$LANG]=$KEYS
  echo "      📊 Keys: $KEYS"

  # Get file size
  SIZE=$(du -h "$FILE" | cut -f1)
  FILE_SIZE[$LANG]=$SIZE
  echo "      💾 Tamaño: $SIZE"

  # Count MISSING_TRANSLATION markers
  MISSING=$(jq '[.[] | select(. == "MISSING_TRANSLATION")] | length' "$FILE" 2>/dev/null || echo "0")
  MISSING_KEYS[$LANG]=$MISSING
  if [ "$MISSING" -gt 0 ]; then
    echo "      ⚠️  MISSING_TRANSLATION: $MISSING"
  else
    echo "      ✅ Sin traducciones faltantes"
  fi

  # Calculate quality score (0-100)
  if [ "${JSON_VALID[$LANG]}" = true ]; then
    if [ "$MISSING" -eq 0 ]; then
      QUALITY_SCORE[$LANG]=100
    else
      # Deduct points for missing keys
      DEDUCTION=$((MISSING * 2))
      SCORE=$((100 - DEDUCTION))
      [ $SCORE -lt 0 ] && SCORE=0
      QUALITY_SCORE[$LANG]=$SCORE
    fi
  else
    QUALITY_SCORE[$LANG]=0
  fi

  echo "      🎯 Puntuación de calidad: ${QUALITY_SCORE[$LANG]}/100"
  echo ""

done

echo "3️⃣ Verificando consistencia entre idiomas..."
echo ""

# Get reference key count from English
EN_KEY_COUNT=${KEY_COUNT[en]}
echo "   📌 Referencia (EN): $EN_KEY_COUNT keys"
echo ""

CONSISTENCY_ISSUES=0
for LANG in "${LANGUAGES[@]}"; do
  [ "$LANG" = "en" ] && continue

  LANG_KEY_COUNT=${KEY_COUNT[$LANG]}
  if [ "$LANG_KEY_COUNT" -eq "$EN_KEY_COUNT" ]; then
    echo "   ✅ $LANG: $LANG_KEY_COUNT keys (consistente)"
  else
    DIFF=$((EN_KEY_COUNT - LANG_KEY_COUNT))
    echo "   ⚠️  $LANG: $LANG_KEY_COUNT keys (diferencia: $DIFF)"
    CONSISTENCY_ISSUES=$((CONSISTENCY_ISSUES + 1))
  fi
done

echo ""

# Calculate overall quality
TOTAL_QUALITY=0
for LANG in "${LANGUAGES[@]}"; do
  TOTAL_QUALITY=$((TOTAL_QUALITY + QUALITY_SCORE[$LANG]))
done
AVERAGE_QUALITY=$((TOTAL_QUALITY / ${#LANGUAGES[@]}))

echo "4️⃣ Generando reporte de calidad..."
echo ""

# Generate JSON report
cat > "$OUTPUT_DIR/quality_report.json" << EOF
{
  "analysis_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "feature": "cosmic_coach",
  "languages_analyzed": ${#LANGUAGES[@]},
  "overall_quality_score": $AVERAGE_QUALITY,
  "total_checks": $TOTAL_CHECKS,
  "passed_checks": $PASSED_CHECKS,
  "failed_checks": $FAILED_CHECKS,
  "files": {
EOF

FIRST_FILE=true
for i in "${!LANGUAGES[@]}"; do
  LANG="${LANGUAGES[$i]}"
  LANG_NAME="${LANG_NAMES[$i]}"

  if [ "$FIRST_FILE" = true ]; then
    FIRST_FILE=false
  else
    echo "," >> "$OUTPUT_DIR/quality_report.json"
  fi

  cat >> "$OUTPUT_DIR/quality_report.json" << EOF
    "$LANG": {
      "language_name": "$LANG_NAME",
      "file": "cosmic_coach_${LANG}.arb",
      "json_valid": $([ "${JSON_VALID[$LANG]}" = true ] && echo "true" || echo "false"),
      "key_count": ${KEY_COUNT[$LANG]},
      "missing_translations": ${MISSING_KEYS[$LANG]},
      "file_size": "${FILE_SIZE[$LANG]}",
      "quality_score": ${QUALITY_SCORE[$LANG]},
      "status": "$([ ${QUALITY_SCORE[$LANG]} -eq 100 ] && echo "perfect" || [ ${QUALITY_SCORE[$LANG]} -ge 80 ] && echo "good" || [ ${QUALITY_SCORE[$LANG]} -ge 60 ] && echo "acceptable" || echo "needs_work")"
    }
EOF
done

cat >> "$OUTPUT_DIR/quality_report.json" << EOF

  },
  "consistency_check": {
    "reference_language": "en",
    "reference_key_count": $EN_KEY_COUNT,
    "consistency_issues": $CONSISTENCY_ISSUES
  },
  "recommendations": [
EOF

# Add recommendations
RECOMMENDATIONS=()

if [ $CONSISTENCY_ISSUES -gt 0 ]; then
  RECOMMENDATIONS+=("Verificar diferencias de cantidad de keys entre idiomas")
fi

for LANG in "${LANGUAGES[@]}"; do
  if [ "${MISSING_KEYS[$LANG]}" -gt 0 ]; then
    RECOMMENDATIONS+=("Completar ${MISSING_KEYS[$LANG]} traducciones faltantes en $LANG")
  fi
done

if [ "${JSON_VALID[en]}" = false ]; then
  RECOMMENDATIONS+=("Corregir errores de sintaxis JSON en archivo de referencia (EN)")
fi

# Add recommendations to JSON
if [ ${#RECOMMENDATIONS[@]} -eq 0 ]; then
  echo "    \"Todos los archivos están en perfecto estado\"" >> "$OUTPUT_DIR/quality_report.json"
else
  for i in "${!RECOMMENDATIONS[@]}"; do
    if [ $i -eq 0 ]; then
      echo -n "    \"${RECOMMENDATIONS[$i]}\"" >> "$OUTPUT_DIR/quality_report.json"
    else
      echo "," >> "$OUTPUT_DIR/quality_report.json"
      echo -n "    \"${RECOMMENDATIONS[$i]}\"" >> "$OUTPUT_DIR/quality_report.json"
    fi
  done
  echo "" >> "$OUTPUT_DIR/quality_report.json"
fi

cat >> "$OUTPUT_DIR/quality_report.json" << EOF
  ]
}
EOF

echo "   ✅ quality_report.json generado"
echo ""

# Generate text report
cat > "$OUTPUT_DIR/agent9_quality_checker_report.txt" << EOF
=============================================================================
AGENT 9: QUALITY_CHECKER - Reporte de Calidad
=============================================================================
Fecha: $(date)
Feature: Cosmic Coach
Idiomas analizados: ${#LANGUAGES[@]}

PUNTUACIÓN GENERAL:
-------------------
🎯 Calidad promedio:        $AVERAGE_QUALITY/100
✅ Checks pasados:          $PASSED_CHECKS/$TOTAL_CHECKS
$([ $FAILED_CHECKS -gt 0 ] && echo "❌ Checks fallidos:         $FAILED_CHECKS" || echo "")

VALIDACIÓN POR IDIOMA:
----------------------
EOF

for i in "${!LANGUAGES[@]}"; do
  LANG="${LANGUAGES[$i]}"
  LANG_NAME="${LANG_NAMES[$i]}"

  STATUS_EMOJI="✅"
  [ "${JSON_VALID[$LANG]}" = false ] && STATUS_EMOJI="❌"
  [ "${MISSING_KEYS[$LANG]}" -gt 0 ] && STATUS_EMOJI="⚠️ "

  printf "%-12s %s JSON: %-8s Keys: %4d Missing: %3d Score: %3d/100\n" \
    "$LANG_NAME" "$STATUS_EMOJI" \
    "$([ "${JSON_VALID[$LANG]}" = true ] && echo "✅ Válido" || echo "❌ Error")" \
    "${KEY_COUNT[$LANG]}" "${MISSING_KEYS[$LANG]}" "${QUALITY_SCORE[$LANG]}" >> "$OUTPUT_DIR/agent9_quality_checker_report.txt"
done

cat >> "$OUTPUT_DIR/agent9_quality_checker_report.txt" << EOF

CONSISTENCIA:
-------------
✅ Referencia (EN):         $EN_KEY_COUNT keys
$([ $CONSISTENCY_ISSUES -eq 0 ] && echo "✅ Todos los idiomas consistentes" || echo "⚠️  Issues de consistencia: $CONSISTENCY_ISSUES")

ARCHIVOS GENERADOS:
-------------------
✅ quality_report.json         - Reporte detallado en JSON
✅ agent9_quality_checker_report.txt - Este reporte

RECOMENDACIONES:
----------------
EOF

if [ ${#RECOMMENDATIONS[@]} -eq 0 ]; then
  echo "✅ Todos los archivos están en perfecto estado" >> "$OUTPUT_DIR/agent9_quality_checker_report.txt"
else
  for REC in "${RECOMMENDATIONS[@]}"; do
    echo "⚠️  $REC" >> "$OUTPUT_DIR/agent9_quality_checker_report.txt"
  done
fi

cat >> "$OUTPUT_DIR/agent9_quality_checker_report.txt" << EOF

SIGUIENTE PASO:
---------------
$([ $AVERAGE_QUALITY -ge 80 ] && echo "✅ Ejecutar Agent 10: INTEGRATOR para integrar archivos al proyecto" || echo "⚠️  Revisar y corregir issues antes de integrar")

EOF

cat "$OUTPUT_DIR/agent9_quality_checker_report.txt"

echo ""

# Final verdict
if [ $AVERAGE_QUALITY -ge 90 ]; then
  echo "✅ AGENT 9: QUALITY_CHECKER - Calidad EXCELENTE ($AVERAGE_QUALITY/100)"
elif [ $AVERAGE_QUALITY -ge 70 ]; then
  echo "⚠️  AGENT 9: QUALITY_CHECKER - Calidad BUENA ($AVERAGE_QUALITY/100)"
else
  echo "❌ AGENT 9: QUALITY_CHECKER - Calidad BAJA ($AVERAGE_QUALITY/100)"
  echo "   Se requieren correcciones antes de integrar"
fi

echo ""
echo "📊 Resumen:"
echo "   - Puntuación promedio: $AVERAGE_QUALITY/100"
echo "   - Archivos validados: ${#LANGUAGES[@]}"
echo "   - Reportes generados en: $OUTPUT_DIR"
echo ""
