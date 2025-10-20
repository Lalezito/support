#!/bin/bash

# 🤖 MULTIAGENT TODO SYSTEM - Quick Commands
# Uso: ./multiagent.sh [comando]

set -e

PROJECT_ROOT="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
TODO_FILE="/Users/alejandrocaceres/Desktop/appstore.zodia/MULTIAGENT_TODO_SYSTEM.md"

# Colores
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║       🤖 MULTIAGENT TODO SYSTEM - ZODIAC APP         ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para mostrar ayuda
show_help() {
    show_banner
    echo -e "${GREEN}Comandos disponibles:${NC}\n"

    echo -e "${YELLOW}📋 GESTIÓN DE TAREAS:${NC}"
    echo "  ./multiagent.sh list          - Ver todas las tareas pendientes"
    echo "  ./multiagent.sh critical      - Ver solo tareas críticas (🔴)"
    echo "  ./multiagent.sh important     - Ver tareas importantes (🟡)"
    echo "  ./multiagent.sh status        - Resumen del estado actual"
    echo ""

    echo -e "${YELLOW}🔍 BÚSQUEDA Y ANÁLISIS:${NC}"
    echo "  ./multiagent.sh search-hardcoded   - Buscar textos hardcodeados"
    echo "  ./multiagent.sh search-premium     - Buscar usos de isPremiumProvider"
    echo "  ./multiagent.sh analyze-translations - Analizar estado de traducciones"
    echo ""

    echo -e "${YELLOW}🛠️ FIXES RÁPIDOS:${NC}"
    echo "  ./multiagent.sh fix-translations   - Iniciar fix de traducciones Cosmic Coach"
    echo "  ./multiagent.sh fix-analytics      - Iniciar fix de Analytics dashboard"
    echo "  ./multiagent.sh fix-premium        - Buscar y reemplazar isPremiumProvider"
    echo ""

    echo -e "${YELLOW}✅ TESTING:${NC}"
    echo "  ./multiagent.sh test-premium       - Testear funcionalidades premium"
    echo "  ./multiagent.sh test-translations  - Verificar traducciones"
    echo ""

    echo -e "${YELLOW}📊 REPORTES:${NC}"
    echo "  ./multiagent.sh report-full        - Reporte completo del estado"
    echo "  ./multiagent.sh report-commits     - Ver commits recientes"
    echo "  ./multiagent.sh report-progress    - Ver progreso de la sesión"
    echo ""

    echo -e "${YELLOW}🚀 DEPLOY:${NC}"
    echo "  ./multiagent.sh build              - Build iOS release"
    echo "  ./multiagent.sh install            - Instalar en iPhone"
    echo ""
}

# Ver todas las tareas
list_tasks() {
    show_banner
    echo -e "${GREEN}📋 TODAS LAS TAREAS PENDIENTES:${NC}\n"
    cat "$TODO_FILE" | grep -A 100 "TAREAS PENDIENTES PRIORITARIAS" | grep -E "^- \[" | head -20
}

# Ver solo críticas
critical_tasks() {
    show_banner
    echo -e "${RED}🔴 TAREAS CRÍTICAS:${NC}\n"
    cat "$TODO_FILE" | sed -n '/### 🔴 CRÍTICO/,/### 🟡 IMPORTANTE/p' | grep -E "^- \["
}

# Ver importantes
important_tasks() {
    show_banner
    echo -e "${YELLOW}🟡 TAREAS IMPORTANTES:${NC}\n"
    cat "$TODO_FILE" | sed -n '/### 🟡 IMPORTANTE/,/### 🟢 MEJORAS/p' | grep -E "^- \["
}

# Estado actual
show_status() {
    show_banner
    echo -e "${GREEN}📊 ESTADO ACTUAL DEL PROYECTO:${NC}\n"

    echo -e "${BLUE}Branch actual:${NC}"
    cd "$PROJECT_ROOT" && git branch --show-current

    echo -e "\n${BLUE}Último commit:${NC}"
    cd "$PROJECT_ROOT" && git log --oneline -1

    echo -e "\n${BLUE}Archivos modificados:${NC}"
    cd "$PROJECT_ROOT" && git status --short

    echo -e "\n${BLUE}Tareas críticas pendientes:${NC}"
    cat "$TODO_FILE" | sed -n '/### 🔴 CRÍTICO/,/### 🟡 IMPORTANTE/p' | grep -c "^- \[ \]" || echo "0"

    echo -e "\n${BLUE}Tareas completadas hoy:${NC}"
    cat "$TODO_FILE" | sed -n '/### ✅ Completado/,/### 📈 Métricas/p' | grep -c "^- \[x\]" || echo "0"
}

# Buscar textos hardcodeados
search_hardcoded() {
    show_banner
    echo -e "${GREEN}🔍 BUSCANDO TEXTOS HARDCODEADOS EN ESPAÑOL...${NC}\n"

    cd "$PROJECT_ROOT"
    echo -e "${YELLOW}Cosmic Coach Screen:${NC}"
    grep -n '"[A-ZÁÉÍÓÚÑ][a-záéíóúñ ]*"' lib/screens/cosmic_coach_screen.dart | head -10 || echo "No encontrado"

    echo -e "\n${YELLOW}Cosmic Coach Chat Screen:${NC}"
    grep -n '"[A-ZÁÉÍÓÚÑ][a-záéíóúñ ]*"' lib/screens/cosmic_coach_chat_screen.dart | head -10 || echo "No encontrado"

    echo -e "\n${BLUE}Total de archivos con posibles hardcoded:${NC}"
    find lib/screens -name "*.dart" -exec grep -l '"[A-ZÁÉÍÓÚÑ]' {} \; | wc -l
}

# Buscar isPremiumProvider
search_premium() {
    show_banner
    echo -e "${GREEN}🔍 BUSCANDO USOS DE isPremiumProvider (obsoleto)...${NC}\n"

    cd "$PROJECT_ROOT"
    echo -e "${YELLOW}Archivos que usan isPremiumProvider:${NC}"
    grep -r "isPremiumProvider" lib/ --include="*.dart" -l || echo "Ninguno encontrado (¡Perfecto!)"

    echo -e "\n${GREEN}Archivos que usan isPremiumUserProvider (correcto):${NC}"
    grep -r "isPremiumUserProvider" lib/ --include="*.dart" -l | head -5 || echo "No encontrado"
}

# Analizar traducciones
analyze_translations() {
    show_banner
    echo -e "${GREEN}🌐 ANALIZANDO ESTADO DE TRADUCCIONES...${NC}\n"

    cd "$PROJECT_ROOT"

    echo -e "${BLUE}Archivos ARB disponibles:${NC}"
    ls -1 assets/l10n/*.arb 2>/dev/null || echo "No se encontraron archivos ARB"

    echo -e "\n${BLUE}Claves relacionadas con Cosmic Coach:${NC}"
    grep -h "cosmicCoach" assets/l10n/*.arb 2>/dev/null | head -5 || echo "Ninguna encontrada - NECESITA TRADUCCIONES"
}

# Reporte completo
report_full() {
    show_banner
    echo -e "${GREEN}📊 REPORTE COMPLETO DEL ESTADO${NC}\n"

    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}1. INFORMACIÓN DEL PROYECTO${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    cd "$PROJECT_ROOT"
    echo "Branch: $(git branch --show-current)"
    echo "Último commit: $(git log --oneline -1)"
    echo "Archivos modificados: $(git status --short | wc -l)"

    echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}2. TAREAS CRÍTICAS PENDIENTES${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    cat "$TODO_FILE" | sed -n '/### 🔴 CRÍTICO/,/### 🟡 IMPORTANTE/p' | grep "^- \[ \]" || echo "Ninguna"

    echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}3. TAREAS COMPLETADAS HOY${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    cat "$TODO_FILE" | sed -n '/### ✅ Completado/,/### 📈 Métricas/p' | grep "^- \[x\]" | tail -5 || echo "Ninguna"

    echo -e "\n${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${YELLOW}4. MÉTRICAS DE CALIDAD${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    cat "$TODO_FILE" | sed -n '/### 📈 Métricas/,/---/p' | grep -v "^#" | grep -v "^---" || echo "No disponible"
}

# Commits recientes
report_commits() {
    show_banner
    echo -e "${GREEN}📝 COMMITS RECIENTES:${NC}\n"

    cd "$PROJECT_ROOT"
    git log --oneline --graph --decorate -10
}

# Build iOS
build_ios() {
    show_banner
    echo -e "${GREEN}🚀 BUILDING iOS RELEASE...${NC}\n"

    cd "$PROJECT_ROOT"
    /Users/alejandrocaceres/flutter/bin/flutter build ios --release
}

# Main
case "${1:-help}" in
    list)
        list_tasks
        ;;
    critical)
        critical_tasks
        ;;
    important)
        important_tasks
        ;;
    status)
        show_status
        ;;
    search-hardcoded)
        search_hardcoded
        ;;
    search-premium)
        search_premium
        ;;
    analyze-translations)
        analyze_translations
        ;;
    report-full)
        report_full
        ;;
    report-commits)
        report_commits
        ;;
    build)
        build_ios
        ;;
    help|*)
        show_help
        ;;
esac
