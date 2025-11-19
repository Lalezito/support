#!/bin/bash
# ============================================================================
# VERIFICADOR DEL SISTEMA - Pre-flight Check
# ============================================================================
# Verifica que todos los requisitos estén instalados y los scripts existan
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia"
L10N_DIR="$BASE_DIR/zodiac_app/assets/l10n"

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}🔍 VERIFICACIÓN DEL SISTEMA MULTIAGENTE${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

# Function to check command
check_command() {
  local CMD=$1
  local NAME=$2
  local INSTALL_CMD=$3

  if command -v "$CMD" &> /dev/null; then
    VERSION=$($CMD --version 2>&1 | head -n1)
    echo -e "${GREEN}✅ $NAME instalado${NC}: $VERSION"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    return 0
  else
    echo -e "${RED}❌ $NAME NO instalado${NC}"
    echo -e "   ${YELLOW}Instalar con: $INSTALL_CMD${NC}"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    return 1
  fi
}

# Function to check file
check_file() {
  local FILE=$1
  local NAME=$2
  local REQUIRED=$3

  if [ -f "$FILE" ]; then
    SIZE=$(du -h "$FILE" | cut -f1)
    echo -e "${GREEN}✅ $NAME encontrado${NC} ($SIZE)"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    return 0
  else
    if [ "$REQUIRED" = "required" ]; then
      echo -e "${RED}❌ $NAME NO encontrado${NC}: $FILE"
      CHECKS_FAILED=$((CHECKS_FAILED + 1))
      return 1
    else
      echo -e "${YELLOW}⚠️  $NAME NO encontrado${NC}: $FILE"
      WARNINGS=$((WARNINGS + 1))
      return 0
    fi
  fi
}

# Function to check directory
check_directory() {
  local DIR=$1
  local NAME=$2
  local REQUIRED=$3

  if [ -d "$DIR" ]; then
    echo -e "${GREEN}✅ $NAME encontrado${NC}: $DIR"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    return 0
  else
    if [ "$REQUIRED" = "required" ]; then
      echo -e "${RED}❌ $NAME NO encontrado${NC}: $DIR"
      CHECKS_FAILED=$((CHECKS_FAILED + 1))
      return 1
    else
      echo -e "${YELLOW}⚠️  $NAME NO encontrado${NC}: $DIR"
      WARNINGS=$((WARNINGS + 1))
      return 0
    fi
  fi
}

# 1. Check required commands
echo "1️⃣ Verificando dependencias del sistema..."
echo ""

check_command "bash" "Bash" "Pre-instalado en macOS"
check_command "jq" "jq (JSON processor)" "brew install jq"
check_command "bc" "bc (calculator)" "brew install bc"

echo ""

# 2. Check agent scripts
echo "2️⃣ Verificando scripts de agentes..."
echo ""

AGENT_SCRIPTS=(
  "01_analyzer.sh:Agent 1: ANALYZER"
  "02_validator.sh:Agent 2: VALIDATOR"
  "03_extractor_en.sh:Agent 3: EXTRACTOR_EN"
  "04_extractor_es.sh:Agent 4: EXTRACTOR_ES"
  "05_extractor_de.sh:Agent 5: EXTRACTOR_DE"
  "06_extractor_fr.sh:Agent 6: EXTRACTOR_FR"
  "07_extractor_it.sh:Agent 7: EXTRACTOR_IT"
  "08_extractor_pt.sh:Agent 8: EXTRACTOR_PT"
  "09_quality_checker.sh:Agent 9: QUALITY_CHECKER"
  "10_integrator.sh:Agent 10: INTEGRATOR"
)

for AGENT_INFO in "${AGENT_SCRIPTS[@]}"; do
  IFS=':' read -r SCRIPT_FILE AGENT_NAME <<< "$AGENT_INFO"
  FILE="$SCRIPT_DIR/$SCRIPT_FILE"

  if [ -f "$FILE" ]; then
    if [ -x "$FILE" ]; then
      echo -e "${GREEN}✅ $AGENT_NAME${NC} (ejecutable)"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      echo -e "${YELLOW}⚠️  $AGENT_NAME${NC} (no ejecutable - se arreglará automáticamente)"
      chmod +x "$FILE"
      echo -e "   ${GREEN}✅ Permisos de ejecución otorgados${NC}"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo -e "${RED}❌ $AGENT_NAME NO encontrado${NC}: $FILE"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
  fi
done

echo ""

# 3. Check orchestrator
echo "3️⃣ Verificando orquestador maestro..."
echo ""

ORCHESTRATOR="$SCRIPT_DIR/run_all_agents.sh"
if [ -f "$ORCHESTRATOR" ]; then
  if [ -x "$ORCHESTRATOR" ]; then
    echo -e "${GREEN}✅ run_all_agents.sh encontrado y ejecutable${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    echo -e "${YELLOW}⚠️  run_all_agents.sh encontrado pero no ejecutable${NC}"
    chmod +x "$ORCHESTRATOR"
    echo -e "   ${GREEN}✅ Permisos de ejecución otorgados${NC}"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  echo -e "${RED}❌ run_all_agents.sh NO encontrado${NC}"
  CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

echo ""

# 4. Check source files
echo "4️⃣ Verificando archivos fuente de traducción..."
echo ""

check_directory "$L10N_DIR" "Directorio l10n" "required"

LANGUAGES=("en" "es" "de" "fr" "it" "pt")
for LANG in "${LANGUAGES[@]}"; do
  check_file "$L10N_DIR/app_${LANG}.arb" "app_${LANG}.arb" "required"
done

echo ""

# 5. Check output directory
echo "5️⃣ Verificando estructura de directorios..."
echo ""

OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
check_directory "$OUTPUT_DIR" "Directorio de salida" "optional"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo -e "   ${BLUE}ℹ️  Creando directorio de salida...${NC}"
  mkdir -p "$OUTPUT_DIR"
  echo -e "   ${GREEN}✅ Directorio creado${NC}"
fi

echo ""

# 6. Check JSON validity of source files
echo "6️⃣ Verificando validez JSON de archivos fuente..."
echo ""

for LANG in "${LANGUAGES[@]}"; do
  FILE="$L10N_DIR/app_${LANG}.arb"
  if [ -f "$FILE" ]; then
    if jq empty "$FILE" 2>/dev/null; then
      KEYS=$(jq 'keys | length' "$FILE")
      echo -e "${GREEN}✅ app_${LANG}.arb válido${NC} ($KEYS keys)"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      echo -e "${RED}❌ app_${LANG}.arb inválido (JSON corrupto)${NC}"
      CHECKS_FAILED=$((CHECKS_FAILED + 1))
    fi
  fi
done

echo ""

# 7. System information
echo "7️⃣ Información del sistema..."
echo ""

echo -e "${BLUE}OS:${NC} $(uname -s) $(uname -r)"
echo -e "${BLUE}Bash version:${NC} $BASH_VERSION"
echo -e "${BLUE}Shell:${NC} $SHELL"
echo -e "${BLUE}Usuario:${NC} $(whoami)"
echo -e "${BLUE}Directorio scripts:${NC} $SCRIPT_DIR"
echo -e "${BLUE}Directorio base:${NC} $BASE_DIR"

echo ""

# Final summary
echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${BLUE}📊 RESUMEN DE VERIFICACIÓN${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

TOTAL_CHECKS=$((CHECKS_PASSED + CHECKS_FAILED))
echo "Total de verificaciones: $TOTAL_CHECKS"
echo -e "${GREEN}✅ Checks pasados: $CHECKS_PASSED${NC}"
echo -e "${RED}❌ Checks fallidos: $CHECKS_FAILED${NC}"
echo -e "${YELLOW}⚠️  Advertencias: $WARNINGS${NC}"

echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo -e "${GREEN}✅ SISTEMA LISTO PARA EJECUTAR${NC}"
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo ""
  echo "Ejecuta el sistema con:"
  echo ""
  echo "  cd $SCRIPT_DIR"
  echo "  ./run_all_agents.sh"
  echo ""
  echo "O ejecuta agentes individuales:"
  echo ""
  echo "  ./01_analyzer.sh"
  echo "  ./02_validator.sh"
  echo "  ..."
  echo ""
  exit 0
else
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo -e "${RED}❌ SISTEMA NO ESTÁ LISTO${NC}"
  echo "════════════════════════════════════════════════════════════════════════════════"
  echo ""
  echo "Por favor, corrige los errores antes de ejecutar:"
  echo ""

  if ! command -v jq &> /dev/null; then
    echo "  • Instalar jq: brew install jq"
  fi

  if ! command -v bc &> /dev/null; then
    echo "  • Instalar bc: brew install bc"
  fi

  echo ""
  echo "Revisa los mensajes de error arriba para más detalles."
  echo ""
  exit 1
fi
