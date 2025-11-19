#!/bin/bash
# ============================================================================
# AGENT 3: EXTRACTOR_EN - Extractor de Inglés
# ============================================================================
# Rol: Extraer keys de Cosmic Coach del archivo app_en.arb
# Input: cosmic_coach_keys.txt, app_en.arb
# Output: cosmic_coach_en.arb
# ============================================================================

set -e

echo "🔵 AGENT 3: EXTRACTOR_EN - Iniciando extracción..."
echo ""

# Paths
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
L10N_DIR="$BASE_DIR/assets/l10n"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
FEATURE_DIR="$OUTPUT_DIR/features/cosmic_coach"
TEMP_DIR="$OUTPUT_DIR/temp"

# Language
LANG="en"
LANG_NAME="English"

# Check prerequisites
if [ ! -f "$OUTPUT_DIR/cosmic_coach_keys.txt" ]; then
  echo "❌ Error: cosmic_coach_keys.txt no encontrado"
  exit 1
fi

mkdir -p "$FEATURE_DIR"
mkdir -p "$TEMP_DIR"

cd "$L10N_DIR"

echo "📁 Directorio: $L10N_DIR"
echo "🌍 Idioma: $LANG_NAME ($LANG)"
echo ""

ARB_FILE="app_${LANG}.arb"
OUTPUT_FILE="$FEATURE_DIR/cosmic_coach_${LANG}.arb"

if [ ! -f "$ARB_FILE" ]; then
  echo "❌ Error: $ARB_FILE no encontrado"
  exit 1
fi

TOTAL_KEYS=$(wc -l < "$OUTPUT_DIR/cosmic_coach_keys.txt" | tr -d ' ')
echo "1️⃣ Extrayendo $TOTAL_KEYS keys de $ARB_FILE..."
echo ""

# Initialize output JSON
echo "{" > "$OUTPUT_FILE"

EXTRACTED=0
MISSING=0
FIRST_ENTRY=true

# Read each key and extract from source
while IFS= read -r KEY; do
  # Skip empty lines
  [ -z "$KEY" ] && continue

  # Check if key exists in source file
  if jq -e --arg key "$KEY" 'has($key)' "$ARB_FILE" > /dev/null 2>&1; then
    # Extract the key-value pair
    VALUE=$(jq -r --arg key "$KEY" '.[$key]' "$ARB_FILE")

    # Add comma if not first entry
    if [ "$FIRST_ENTRY" = true ]; then
      FIRST_ENTRY=false
    else
      echo "," >> "$OUTPUT_FILE"
    fi

    # Write to output file (properly escaped)
    jq -n --arg key "$KEY" --arg value "$VALUE" '{($key): $value}' | \
      jq -c '.' | sed 's/^{//; s/}$//' >> "$OUTPUT_FILE"

    # Check if this is a metadata key (@...)
    if [[ "$KEY" == @* ]]; then
      # Extract metadata object
      METADATA=$(jq --arg key "$KEY" '.[$key]' "$ARB_FILE")
      echo "," >> "$OUTPUT_FILE"
      jq -n --arg key "$KEY" --argjson metadata "$METADATA" '{($key): $metadata}' | \
        jq -c '.' | sed 's/^{//; s/}$//' >> "$OUTPUT_FILE"
    fi

    EXTRACTED=$((EXTRACTED + 1))

    # Progress indicator
    if [ $((EXTRACTED % 50)) -eq 0 ]; then
      echo "   ⏳ Procesadas: $EXTRACTED/$TOTAL_KEYS..."
    fi

  else
    echo "   ⚠️  Key no encontrada: $KEY"
    MISSING=$((MISSING + 1))
  fi

done < "$OUTPUT_DIR/cosmic_coach_keys.txt"

# Close JSON
echo "" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

# Format JSON properly
jq '.' "$OUTPUT_FILE" > "$OUTPUT_FILE.tmp" && mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"

echo ""
echo "2️⃣ Validando archivo generado..."

# Validate JSON
if jq empty "$OUTPUT_FILE" 2>/dev/null; then
  echo "   ✅ JSON válido"
else
  echo "   ❌ JSON inválido"
  exit 1
fi

# Count keys in output
OUTPUT_KEYS=$(jq 'keys | length' "$OUTPUT_FILE")
echo "   ✅ Keys extraídas: $OUTPUT_KEYS"

FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
echo "   ✅ Tamaño del archivo: $FILE_SIZE"
echo ""

# Generate extraction report
cat > "$OUTPUT_DIR/agent3_extractor_${LANG}_report.txt" << EOF
=============================================================================
AGENT 3: EXTRACTOR_EN - Reporte de Extracción
=============================================================================
Fecha: $(date)
Idioma: $LANG_NAME ($LANG)

RESULTADOS:
-----------
✅ Keys solicitadas:        $TOTAL_KEYS
✅ Keys extraídas:          $EXTRACTED
$([ $MISSING -gt 0 ] && echo "⚠️  Keys faltantes:         $MISSING" || echo "✅ Keys faltantes:          0")
✅ Porcentaje de éxito:     $(echo "scale=2; $EXTRACTED * 100 / $TOTAL_KEYS" | bc)%

ARCHIVO GENERADO:
-----------------
📄 Ruta: $OUTPUT_FILE
📊 Tamaño: $FILE_SIZE
📝 Keys totales: $OUTPUT_KEYS

SIGUIENTE PASO:
---------------
Este archivo está listo para ser usado como fuente de referencia
para los extractores de otros idiomas (Agents 4-8)

EOF

cat "$OUTPUT_DIR/agent3_extractor_${LANG}_report.txt"

echo ""
echo "✅ AGENT 3: EXTRACTOR_EN - Completado exitosamente"
echo ""
echo "📊 Resumen:"
echo "   - Keys extraídas: $EXTRACTED/$TOTAL_KEYS"
echo "   - Archivo generado: cosmic_coach_${LANG}.arb"
echo "   - Ubicación: $FEATURE_DIR"
echo ""
