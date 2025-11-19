#!/bin/bash
# ============================================================================
# ORQUESTADOR MAESTRO SIMPLIFICADO - Sistema Multiagente de Segmentación
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
LOG_DIR="$OUTPUT_DIR/logs"

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

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

# ============================================================================
# FASE 1: ANÁLISIS SECUENCIAL
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}📊 FASE 1: ANÁLISIS (Secuencial)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Agent 1: ANALYZER
echo -e "${CYAN}▶ Agent 1: ANALYZER${NC}"
chmod +x 01_analyzer.sh
if ./01_analyzer.sh 2>&1 | tee "$LOG_DIR/agent1_analyzer.log"; then
  echo -e "${GREEN}✅ Agent 1 completado${NC}"
else
  echo -e "${RED}❌ Agent 1 falló${NC}"
  exit 1
fi

echo ""

# Agent 2: VALIDATOR
echo -e "${CYAN}▶ Agent 2: VALIDATOR${NC}"
chmod +x 02_validator.sh
if ./02_validator.sh 2>&1 | tee "$LOG_DIR/agent2_validator.log"; then
  echo -e "${GREEN}✅ Agent 2 completado${NC}"
else
  echo -e "${RED}❌ Agent 2 falló${NC}"
  exit 1
fi

# ============================================================================
# FASE 2: EXTRACCIÓN PARALELA
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${PURPLE}🔄 FASE 2: EXTRACCIÓN (Paralela - 6 idiomas)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Make all extractor scripts executable
chmod +x 03_extractor_en.sh
chmod +x 04_extractor_es.sh
chmod +x 05_extractor_de.sh
chmod +x 06_extractor_fr.sh
chmod +x 07_extractor_it.sh
chmod +x 08_extractor_pt.sh

# Start all extractors in parallel
echo -e "${CYAN}🚀 Iniciando 6 extractores en paralelo...${NC}"
echo ""

./03_extractor_en.sh > "$LOG_DIR/agent3_extractor_en.log" 2>&1 &
PID_EN=$!
echo "  Agent 3 (EN) - PID: $PID_EN"

./04_extractor_es.sh > "$LOG_DIR/agent4_extractor_es.log" 2>&1 &
PID_ES=$!
echo "  Agent 4 (ES) - PID: $PID_ES"

./05_extractor_de.sh > "$LOG_DIR/agent5_extractor_de.log" 2>&1 &
PID_DE=$!
echo "  Agent 5 (DE) - PID: $PID_DE"

./06_extractor_fr.sh > "$LOG_DIR/agent6_extractor_fr.log" 2>&1 &
PID_FR=$!
echo "  Agent 6 (FR) - PID: $PID_FR"

./07_extractor_it.sh > "$LOG_DIR/agent7_extractor_it.log" 2>&1 &
PID_IT=$!
echo "  Agent 7 (IT) - PID: $PID_IT"

./08_extractor_pt.sh > "$LOG_DIR/agent8_extractor_pt.log" 2>&1 &
PID_PT=$!
echo "  Agent 8 (PT) - PID: $PID_PT"

echo ""
echo "⏳ Esperando a que todos los extractores completen..."
echo ""

# Wait for all
wait $PID_EN && echo -e "${GREEN}✅ Agent 3 (EN) completado${NC}" || echo -e "${RED}❌ Agent 3 (EN) falló${NC}"
wait $PID_ES && echo -e "${GREEN}✅ Agent 4 (ES) completado${NC}" || echo -e "${RED}❌ Agent 4 (ES) falló${NC}"
wait $PID_DE && echo -e "${GREEN}✅ Agent 5 (DE) completado${NC}" || echo -e "${RED}❌ Agent 5 (DE) falló${NC}"
wait $PID_FR && echo -e "${GREEN}✅ Agent 6 (FR) completado${NC}" || echo -e "${RED}❌ Agent 6 (FR) falló${NC}"
wait $PID_IT && echo -e "${GREEN}✅ Agent 7 (IT) completado${NC}" || echo -e "${RED}❌ Agent 7 (IT) falló${NC}"
wait $PID_PT && echo -e "${GREEN}✅ Agent 8 (PT) completado${NC}" || echo -e "${RED}❌ Agent 8 (PT) falló${NC}"

# ============================================================================
# FASE 3: VALIDACIÓN E INTEGRACIÓN
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🔍 FASE 3: VALIDACIÓN E INTEGRACIÓN (Secuencial)${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Agent 9: QUALITY_CHECKER
echo -e "${CYAN}▶ Agent 9: QUALITY_CHECKER${NC}"
chmod +x 09_quality_checker.sh
if ./09_quality_checker.sh 2>&1 | tee "$LOG_DIR/agent9_quality_checker.log"; then
  echo -e "${GREEN}✅ Agent 9 completado${NC}"
else
  echo -e "${RED}❌ Agent 9 falló${NC}"
  exit 1
fi

echo ""

# Agent 10: INTEGRATOR
echo -e "${CYAN}▶ Agent 10: INTEGRATOR${NC}"
chmod +x 10_integrator.sh
if ./10_integrator.sh 2>&1 | tee "$LOG_DIR/agent10_integrator.log"; then
  echo -e "${GREEN}✅ Agent 10 completado${NC}"
else
  echo -e "${RED}❌ Agent 10 falló${NC}"
  exit 1
fi

# ============================================================================
# RESUMEN FINAL
# ============================================================================

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ SISTEMA MULTIAGENTE COMPLETADO EXITOSAMENTE${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Duración total: ${TOTAL_DURATION}s"
echo "Archivos generados en: $OUTPUT_DIR"
echo "Logs en: $LOG_DIR"
echo ""
echo "Próximos pasos:"
echo "  1. Revisar reporte de calidad: cat $OUTPUT_DIR/quality_report.json"
echo "  2. Ver archivos generados: ls -lh $OUTPUT_DIR/features/cosmic_coach/"
echo "  3. Integrar en Flutter: Seguir instrucciones en integration_guide.md"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
