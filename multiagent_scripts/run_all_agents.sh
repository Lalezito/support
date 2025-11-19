#!/bin/bash
# ============================================================================
# ORQUESTADOR MAESTRO - Sistema Multiagente de Segmentación
# ============================================================================
# Ejecuta todos los agentes en orden para extraer traducciones de Cosmic Coach
# de archivos monolíticos a archivos modulares
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
LOG_DIR="$OUTPUT_DIR/logs"

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Start time
START_TIME=$(date +%s)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "                  🤖 SISTEMA MULTIAGENTE DE SEGMENTACIÓN 🤖"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Feature: Cosmic Coach Translations"
echo "Inicio: $TIMESTAMP"
echo "Directorio: $SCRIPT_DIR"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Agent execution tracker (simplified for compatibility)
TOTAL_AGENTS=10
COMPLETED_AGENTS=0
FAILED_AGENTS=0

# Function to execute an agent
execute_agent() {
  local AGENT_NUM=$1
  local AGENT_NAME=$2
  local SCRIPT_FILE=$3
  local LOG_FILE="$LOG_DIR/agent${AGENT_NUM}_${AGENT_NAME}.log"

  echo ""
  echo "────────────────────────────────────────────────────────────────────────────────"
  echo -e "${CYAN}Ejecutando Agent $AGENT_NUM: $AGENT_NAME${NC}"
  echo "────────────────────────────────────────────────────────────────────────────────"
  echo ""

  # Check if script exists
  if [ ! -f "$SCRIPT_FILE" ]; then
    echo -e "${RED}❌ Error: Script no encontrado: $SCRIPT_FILE${NC}"
    AGENT_STATUS[$AGENT_NUM]="FAILED"
    FAILED_AGENTS=$((FAILED_AGENTS + 1))
    return 1
  fi

  # Make script executable
  chmod +x "$SCRIPT_FILE"

  # Execute agent and log output
  local AGENT_START=$(date +%s)

  if bash "$SCRIPT_FILE" 2>&1 | tee "$LOG_FILE"; then
    local AGENT_END=$(date +%s)
    local AGENT_DURATION=$((AGENT_END - AGENT_START))
    AGENT_TIME[$AGENT_NUM]=$AGENT_DURATION
    AGENT_STATUS[$AGENT_NUM]="SUCCESS"
    COMPLETED_AGENTS=$((COMPLETED_AGENTS + 1))

    echo ""
    echo -e "${GREEN}✅ Agent $AGENT_NUM: $AGENT_NAME completado en ${AGENT_DURATION}s${NC}"
    echo ""
    return 0
  else
    local AGENT_END=$(date +%s)
    local AGENT_DURATION=$((AGENT_END - AGENT_START))
    AGENT_TIME[$AGENT_NUM]=$AGENT_DURATION
    AGENT_STATUS[$AGENT_NUM]="FAILED"
    FAILED_AGENTS=$((FAILED_AGENTS + 1))

    echo ""
    echo -e "${RED}❌ Agent $AGENT_NUM: $AGENT_NAME FALLÓ después de ${AGENT_DURATION}s${NC}"
    echo -e "${YELLOW}Ver log: $LOG_FILE${NC}"
    echo ""
    return 1
  fi
}

# Function to execute agents in parallel
execute_parallel_agents() {
  local AGENTS=("$@")
  local PIDS=()

  echo ""
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo -e "${PURPLE}🔄 Ejecutando ${#AGENTS[@]} agentes en PARALELO${NC}"
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo ""

  # Start all agents in background
  for AGENT_INFO in "${AGENTS[@]}"; do
    IFS=':' read -r AGENT_NUM AGENT_NAME SCRIPT_FILE <<< "$AGENT_INFO"

    LOG_FILE="$LOG_DIR/agent${AGENT_NUM}_${AGENT_NAME}.log"

    echo -e "${CYAN}🚀 Iniciando Agent $AGENT_NUM: $AGENT_NAME (background)${NC}"

    # Make script executable
    chmod +x "$SCRIPT_FILE"

    # Execute in background
    (
      AGENT_START=$(date +%s)
      if bash "$SCRIPT_FILE" > "$LOG_FILE" 2>&1; then
        AGENT_END=$(date +%s)
        echo "SUCCESS:$((AGENT_END - AGENT_START))" > "$LOG_DIR/agent${AGENT_NUM}.status"
      else
        AGENT_END=$(date +%s)
        echo "FAILED:$((AGENT_END - AGENT_START))" > "$LOG_DIR/agent${AGENT_NUM}.status"
      fi
    ) &

    PIDS+=($!)
  done

  echo ""
  echo "⏳ Esperando a que todos los agentes completen..."
  echo ""

  # Wait for all to complete
  for PID in "${PIDS[@]}"; do
    wait $PID
  done

  # Collect results
  for AGENT_INFO in "${AGENTS[@]}"; do
    IFS=':' read -r AGENT_NUM AGENT_NAME SCRIPT_FILE <<< "$AGENT_INFO"
    STATUS_FILE="$LOG_DIR/agent${AGENT_NUM}.status"

    if [ -f "$STATUS_FILE" ]; then
      IFS=':' read -r STATUS DURATION < "$STATUS_FILE"
      AGENT_STATUS[$AGENT_NUM]=$STATUS
      AGENT_TIME[$AGENT_NUM]=$DURATION

      if [ "$STATUS" = "SUCCESS" ]; then
        echo -e "${GREEN}✅ Agent $AGENT_NUM: $AGENT_NAME completado en ${DURATION}s${NC}"
        COMPLETED_AGENTS=$((COMPLETED_AGENTS + 1))
      else
        echo -e "${RED}❌ Agent $AGENT_NUM: $AGENT_NAME FALLÓ después de ${DURATION}s${NC}"
        FAILED_AGENTS=$((FAILED_AGENTS + 1))
      fi

      rm "$STATUS_FILE"
    else
      echo -e "${RED}❌ Agent $AGENT_NUM: $AGENT_NAME - Estado desconocido${NC}"
      AGENT_STATUS[$AGENT_NUM]="UNKNOWN"
      FAILED_AGENTS=$((FAILED_AGENTS + 1))
    fi
  done

  echo ""
}

# ============================================================================
# FASE 1: ANÁLISIS Y VALIDACIÓN (Secuencial)
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}📊 FASE 1: ANÁLISIS Y VALIDACIÓN (Secuencial)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Agent 1: ANALYZER
execute_agent 1 "ANALYZER" "$SCRIPT_DIR/01_analyzer.sh" || {
  echo -e "${RED}❌ Error crítico en Agent 1: ANALYZER${NC}"
  echo -e "${RED}No se puede continuar sin el análisis inicial${NC}"
  exit 1
}

# Agent 2: VALIDATOR
execute_agent 2 "VALIDATOR" "$SCRIPT_DIR/02_validator.sh" || {
  echo -e "${YELLOW}⚠️  Advertencia: Agent 2: VALIDATOR falló${NC}"
  echo -e "${YELLOW}Continuando de todos modos...${NC}"
}

# ============================================================================
# FASE 2: EXTRACCIÓN (Paralelo)
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🔄 FASE 2: EXTRACCIÓN DE TRADUCCIONES (Paralelo)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Execute extractors in parallel
EXTRACTORS=(
  "3:EXTRACTOR_EN:$SCRIPT_DIR/03_extractor_en.sh"
  "4:EXTRACTOR_ES:$SCRIPT_DIR/04_extractor_es.sh"
  "5:EXTRACTOR_DE:$SCRIPT_DIR/05_extractor_de.sh"
  "6:EXTRACTOR_FR:$SCRIPT_DIR/06_extractor_fr.sh"
  "7:EXTRACTOR_IT:$SCRIPT_DIR/07_extractor_it.sh"
  "8:EXTRACTOR_PT:$SCRIPT_DIR/08_extractor_pt.sh"
)

execute_parallel_agents "${EXTRACTORS[@]}"

# Check if critical extractors succeeded
if [ "${AGENT_STATUS[3]}" != "SUCCESS" ]; then
  echo -e "${RED}❌ Error crítico: Agent 3: EXTRACTOR_EN falló${NC}"
  echo -e "${RED}No se puede continuar sin el archivo de referencia EN${NC}"
  exit 1
fi

# ============================================================================
# FASE 3: VERIFICACIÓN E INTEGRACIÓN (Secuencial)
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🔍 FASE 3: VERIFICACIÓN E INTEGRACIÓN (Secuencial)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Agent 9: QUALITY_CHECKER
execute_agent 9 "QUALITY_CHECKER" "$SCRIPT_DIR/09_quality_checker.sh" || {
  echo -e "${YELLOW}⚠️  Advertencia: Agent 9: QUALITY_CHECKER falló${NC}"
  echo -e "${YELLOW}Continuando de todos modos...${NC}"
}

# Agent 10: INTEGRATOR
execute_agent 10 "INTEGRATOR" "$SCRIPT_DIR/10_integrator.sh" || {
  echo -e "${RED}❌ Error: Agent 10: INTEGRATOR falló${NC}"
  echo -e "${YELLOW}Los archivos fueron generados pero no integrados al proyecto${NC}"
}

# ============================================================================
# REPORTE FINAL
# ============================================================================

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))
END_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ EJECUCIÓN COMPLETADA${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Finalizado: $END_TIMESTAMP"
echo "Duración total: ${TOTAL_DURATION}s ($((TOTAL_DURATION / 60))m $((TOTAL_DURATION % 60))s)"
echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "RESUMEN DE EJECUCIÓN:"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""
echo "Total de agentes: $TOTAL_AGENTS"
echo -e "${GREEN}✅ Completados: $COMPLETED_AGENTS${NC}"
echo -e "${RED}❌ Fallidos: $FAILED_AGENTS${NC}"
echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "ESTADO POR AGENTE:"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

AGENT_NAMES=(
  "ANALYZER"
  "VALIDATOR"
  "EXTRACTOR_EN"
  "EXTRACTOR_ES"
  "EXTRACTOR_DE"
  "EXTRACTOR_FR"
  "EXTRACTOR_IT"
  "EXTRACTOR_PT"
  "QUALITY_CHECKER"
  "INTEGRATOR"
)

for i in {1..10}; do
  STATUS="${AGENT_STATUS[$i]:-UNKNOWN}"
  DURATION="${AGENT_TIME[$i]:-0}"
  AGENT_NAME="${AGENT_NAMES[$((i-1))]}"

  if [ "$STATUS" = "SUCCESS" ]; then
    echo -e "Agent $i: ${GREEN}✅ $AGENT_NAME${NC} (${DURATION}s)"
  elif [ "$STATUS" = "FAILED" ]; then
    echo -e "Agent $i: ${RED}❌ $AGENT_NAME${NC} (${DURATION}s)"
  else
    echo -e "Agent $i: ${YELLOW}⚠️  $AGENT_NAME - UNKNOWN${NC}"
  fi
done

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "ARCHIVOS GENERADOS:"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""
echo "📁 Directorio de salida: $OUTPUT_DIR"
echo ""

if [ -f "$OUTPUT_DIR/cosmic_coach_keys.txt" ]; then
  KEYS_COUNT=$(wc -l < "$OUTPUT_DIR/cosmic_coach_keys.txt" | tr -d ' ')
  echo "✅ cosmic_coach_keys.txt ($KEYS_COUNT keys)"
fi

if [ -f "$OUTPUT_DIR/translation_categories_map.json" ]; then
  echo "✅ translation_categories_map.json"
fi

if [ -f "$OUTPUT_DIR/completeness_report.json" ]; then
  echo "✅ completeness_report.json"
fi

if [ -f "$OUTPUT_DIR/quality_report.json" ]; then
  QUALITY_SCORE=$(jq -r '.overall_quality_score' "$OUTPUT_DIR/quality_report.json" 2>/dev/null || echo "N/A")
  echo "✅ quality_report.json (Score: $QUALITY_SCORE/100)"
fi

if [ -f "$OUTPUT_DIR/INTEGRATION_GUIDE.md" ]; then
  echo "✅ INTEGRATION_GUIDE.md"
fi

echo ""
echo "📁 Archivos de traducción generados:"
for LANG in en es de fr it pt; do
  FILE="$OUTPUT_DIR/features/cosmic_coach/cosmic_coach_${LANG}.arb"
  if [ -f "$FILE" ]; then
    SIZE=$(du -h "$FILE" | cut -f1)
    KEYS=$(jq 'keys | length' "$FILE" 2>/dev/null || echo "?")
    echo "   ✅ cosmic_coach_${LANG}.arb ($SIZE, $KEYS keys)"
  else
    echo "   ❌ cosmic_coach_${LANG}.arb (NO GENERADO)"
  fi
done

echo ""
echo "📁 Logs de ejecución:"
echo "   $LOG_DIR/"
for i in {1..10}; do
  LOG_FILE="$LOG_DIR/agent${i}_${AGENT_NAMES[$((i-1))]}.log"
  if [ -f "$LOG_FILE" ]; then
    echo "   - agent${i}_${AGENT_NAMES[$((i-1))]}.log"
  fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🎯 PRÓXIMOS PASOS:${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "1. Revisar INTEGRATION_GUIDE.md en: $OUTPUT_DIR/INTEGRATION_GUIDE.md"
echo "2. Revisar quality_report.json para verificar calidad"
echo "3. Completar traducciones marcadas como MISSING_TRANSLATION"
echo "4. Ejecutar: cd zodiac_app && flutter gen-l10n"
echo "5. Actualizar código para usar CosmicCoachLocalizations"
echo "6. Ejecutar testing exhaustivo en los 6 idiomas"
echo ""

if [ $FAILED_AGENTS -eq 0 ]; then
  echo -e "${GREEN}✅ Todos los agentes completaron exitosamente${NC}"
  echo ""
  exit 0
else
  echo -e "${YELLOW}⚠️  Algunos agentes fallaron - Revisar logs para más detalles${NC}"
  echo ""
  exit 1
fi
