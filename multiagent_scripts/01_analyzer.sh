#!/bin/bash
# ============================================================================
# AGENT 1: ANALYZER - Analista de Estructura
# ============================================================================
# Rol: Analizar archivos de traducción e identificar keys de Cosmic Coach
# Input: app_en.arb
# Output: translation_categories_map.json, cosmic_coach_keys.txt
# ============================================================================

set -e

echo "🔵 AGENT 1: ANALYZER - Iniciando análisis..."
echo ""

# Paths
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
L10N_DIR="$BASE_DIR/assets/l10n"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
TEMP_DIR="$OUTPUT_DIR/temp"

# Create output directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

cd "$L10N_DIR"

echo "📁 Directorio: $L10N_DIR"
echo ""

# Step 1: Extract all keys from EN
echo "1️⃣ Extrayendo todas las keys de app_en.arb..."
jq -r 'keys[]' app_en.arb > "$TEMP_DIR/all_keys_en.txt"
TOTAL_KEYS=$(wc -l < "$TEMP_DIR/all_keys_en.txt" | tr -d ' ')
echo "   ✅ Total keys en EN: $TOTAL_KEYS"
echo ""

# Step 2: Find Cosmic Coach related keys
echo "2️⃣ Identificando keys de Cosmic Coach..."

# Patterns for Cosmic Coach
PATTERNS=(
  "cosmic"
  "coach"
  "goal"
  "habit"
  "micro"
  "celebration"
  "smart_goals"
  "new_goals"
  "addGoal"
  "completeGoal"
  "deleteGoal"
)

# Create combined grep pattern
GREP_PATTERN=$(IFS="|"; echo "${PATTERNS[*]}")

# Extract matching keys (case insensitive)
grep -iE "$GREP_PATTERN" "$TEMP_DIR/all_keys_en.txt" > "$TEMP_DIR/cosmic_coach_keys_raw.txt" || true

# Remove duplicates and sort
sort -u "$TEMP_DIR/cosmic_coach_keys_raw.txt" > "$OUTPUT_DIR/cosmic_coach_keys.txt"

COACH_KEYS=$(wc -l < "$OUTPUT_DIR/cosmic_coach_keys.txt" | tr -d ' ')
echo "   ✅ Keys de Cosmic Coach encontradas: $COACH_KEYS"
echo ""

# Step 3: Analyze key patterns
echo "3️⃣ Analizando patrones de keys..."

# Count by prefix
echo "   Prefijos más comunes:"
cat "$OUTPUT_DIR/cosmic_coach_keys.txt" | \
  sed 's/\([A-Z]\)/ \1/g' | \
  awk '{print $1}' | \
  sort | uniq -c | sort -rn | head -10 | \
  while read count prefix; do
    printf "   - %-20s: %3d keys\n" "$prefix" "$count"
  done

echo ""

# Step 4: Check for dependencies (keys used by Cosmic Coach but not in patterns)
echo "4️⃣ Buscando dependencias..."

# Keys que empiezan con @ (metadata)
grep -E '^@' "$OUTPUT_DIR/cosmic_coach_keys.txt" > "$TEMP_DIR/metadata_keys.txt" || true
METADATA_COUNT=$(wc -l < "$TEMP_DIR/metadata_keys.txt" | tr -d ' ')

# Keys regulares (sin @)
grep -vE '^@' "$OUTPUT_DIR/cosmic_coach_keys.txt" > "$TEMP_DIR/regular_keys.txt" || true
REGULAR_COUNT=$(wc -l < "$TEMP_DIR/regular_keys.txt" | tr -d ' ')

echo "   - Keys regulares: $REGULAR_COUNT"
echo "   - Keys de metadata (@...): $METADATA_COUNT"
echo ""

# Step 5: Generate category map JSON
echo "5️⃣ Generando mapa de categorías..."

cat > "$OUTPUT_DIR/translation_categories_map.json" << EOF
{
  "cosmic_coach": {
    "feature_name": "Cosmic Coach",
    "description": "Goal tracking, habits, cosmic guidance, celebrations",
    "patterns": [
      "cosmic*",
      "coach*",
      "goal*",
      "habit*",
      "micro*",
      "celebration*",
      "smart_goals*",
      "new_goals*",
      "addGoal*",
      "completeGoal*",
      "deleteGoal*"
    ],
    "total_keys_found": $COACH_KEYS,
    "regular_keys": $REGULAR_COUNT,
    "metadata_keys": $METADATA_COUNT,
    "percentage_of_total": $(echo "scale=2; $COACH_KEYS * 100 / $TOTAL_KEYS" | bc),
    "dependencies": [
      "celebration",
      "category"
    ],
    "output_files": {
      "en": "features/cosmic_coach/cosmic_coach_en.arb",
      "es": "features/cosmic_coach/cosmic_coach_es.arb",
      "de": "features/cosmic_coach/cosmic_coach_de.arb",
      "fr": "features/cosmic_coach/cosmic_coach_fr.arb",
      "it": "features/cosmic_coach/cosmic_coach_it.arb",
      "pt": "features/cosmic_coach/cosmic_coach_pt.arb"
    }
  }
}
EOF

echo "   ✅ Mapa creado: translation_categories_map.json"
echo ""

# Step 6: Generate summary report
echo "6️⃣ Generando reporte de análisis..."

cat > "$OUTPUT_DIR/agent1_analyzer_report.txt" << EOF
=============================================================================
AGENT 1: ANALYZER - Reporte de Análisis
=============================================================================
Fecha: $(date)
Feature: Cosmic Coach

RESULTADOS:
-----------
✅ Total keys en app_en.arb:        $TOTAL_KEYS
✅ Keys de Cosmic Coach:             $COACH_KEYS
✅ Porcentaje del total:             $(echo "scale=1; $COACH_KEYS * 100 / $TOTAL_KEYS" | bc)%
✅ Keys regulares:                   $REGULAR_COUNT
✅ Keys de metadata (@...):          $METADATA_COUNT

ARCHIVOS GENERADOS:
-------------------
✅ cosmic_coach_keys.txt             - Lista de keys a extraer
✅ translation_categories_map.json   - Mapa de categorías
✅ agent1_analyzer_report.txt        - Este reporte

SIGUIENTE PASO:
---------------
Ejecutar Agent 2: VALIDATOR para verificar completitud en los 6 idiomas

EOF

cat "$OUTPUT_DIR/agent1_analyzer_report.txt"

echo ""
echo "✅ AGENT 1: ANALYZER - Completado exitosamente"
echo ""
echo "📊 Resumen:"
echo "   - Keys encontradas: $COACH_KEYS / $TOTAL_KEYS ($( echo "scale=1; $COACH_KEYS * 100 / $TOTAL_KEYS" | bc)%)"
echo "   - Archivos generados en: $OUTPUT_DIR"
echo ""
