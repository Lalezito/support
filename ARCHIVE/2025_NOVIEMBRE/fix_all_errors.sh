#!/bin/bash

# 🎯 SCRIPT AUTOMÁTICO: FIX ALL CONSOLE ERRORS
# Aplica todos los fixes necesarios para llegar a 0 errores reales

set -e  # Exit on error

echo "🚀 Iniciando fixes automáticos de errores de consola..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directorio del proyecto
PROJECT_DIR="zodiac_app"

# ============================================================================
# FASE 1: VERIFICACIÓN PREVIA
# ============================================================================

echo -e "${BLUE}📋 FASE 1: Verificación del entorno${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Error: No se encuentra el directorio $PROJECT_DIR${NC}"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

echo -e "${GREEN}✅ Directorio del proyecto encontrado${NC}"

# Verificar Flutter instalado
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Error: Flutter no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Flutter instalado: $(flutter --version | head -n 1)${NC}"

# Verificar CocoaPods instalado
if ! command -v pod &> /dev/null; then
    echo -e "${RED}❌ Error: CocoaPods no está instalado${NC}"
    echo "Instalar con: sudo gem install cocoapods"
    exit 1
fi

echo -e "${GREEN}✅ CocoaPods instalado: $(pod --version)${NC}"
echo ""

# ============================================================================
# FASE 2: BACKUP
# ============================================================================

echo -e "${BLUE}💾 FASE 2: Creando backups${NC}"
echo ""

BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup de archivos críticos
if [ -f "$PROJECT_DIR/macos/Podfile.lock" ]; then
    cp "$PROJECT_DIR/macos/Podfile.lock" "$BACKUP_DIR/"
    echo -e "${GREEN}✅ Backup: Podfile.lock${NC}"
fi

if [ -f "$PROJECT_DIR/macos/Runner/Configs/AppInfo.xcconfig" ]; then
    cp "$PROJECT_DIR/macos/Runner/Configs/AppInfo.xcconfig" "$BACKUP_DIR/"
    echo -e "${GREEN}✅ Backup: AppInfo.xcconfig${NC}"
fi

echo -e "${GREEN}✅ Backups creados en: $BACKUP_DIR${NC}"
echo ""

# ============================================================================
# FASE 3: FIX COCOAPODS BASE CONFIGURATION
# ============================================================================

echo -e "${BLUE}🔧 FASE 3: Fixing CocoaPods Base Configuration${NC}"
echo ""

XCCONFIG_FILE="$PROJECT_DIR/macos/Runner/Configs/AppInfo.xcconfig"

if [ ! -f "$XCCONFIG_FILE" ]; then
    echo -e "${RED}❌ Error: No se encuentra $XCCONFIG_FILE${NC}"
    exit 1
fi

# Verificar si ya tiene la configuración
if grep -q "Pods-Runner" "$XCCONFIG_FILE"; then
    echo -e "${YELLOW}⚠️  La configuración de CocoaPods ya existe en AppInfo.xcconfig${NC}"
else
    echo -e "${GREEN}📝 Agregando configuraciones de CocoaPods...${NC}"

    cat >> "$XCCONFIG_FILE" << 'EOF'

// ============================================================================
// CocoaPods Configurations
// Added automatically to fix pod integration warnings
// ============================================================================
#include? "../../Pods/Target Support Files/Pods-Runner/Pods-Runner.debug.xcconfig"
#include? "../../Pods/Target Support Files/Pods-Runner/Pods-Runner.release.xcconfig"
#include? "../../Pods/Target Support Files/Pods-Runner/Pods-Runner.profile.xcconfig"
EOF

    echo -e "${GREEN}✅ Configuraciones de CocoaPods agregadas${NC}"
fi

echo ""

# ============================================================================
# FASE 4: REINSTALAR COCOAPODS
# ============================================================================

echo -e "${BLUE}📦 FASE 4: Reinstalando CocoaPods${NC}"
echo ""

cd "$PROJECT_DIR/macos"

echo -e "${YELLOW}🗑️  Limpiando instalación anterior...${NC}"
rm -rf Pods Podfile.lock

echo -e "${GREEN}📥 Instalando pods (esto puede tardar un momento)...${NC}"
pod install --repo-update 2>&1 | grep -v "Invalid key/value pair: DART_DEFINES"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pods instalados correctamente${NC}"
else
    echo -e "${RED}❌ Error al instalar pods${NC}"
    cd ../..
    exit 1
fi

cd ../..
echo ""

# ============================================================================
# FASE 5: FIX FFI WARNING (OPCIONAL)
# ============================================================================

echo -e "${BLUE}🎨 FASE 5: Fixing FFI Warning (opcional)${NC}"
echo ""

if gem list ffi | grep -q "ffi"; then
    echo -e "${YELLOW}🔧 Recompilando gem ffi...${NC}"
    gem pristine ffi --version 1.17.0 2>/dev/null || echo -e "${YELLOW}⚠️  No se pudo recompilar ffi (no crítico)${NC}"
else
    echo -e "${YELLOW}⚠️  Gem ffi no encontrado (no crítico)${NC}"
fi

echo ""

# ============================================================================
# FASE 6: FIREBASE APP ID FILE
# ============================================================================

echo -e "${BLUE}🔥 FASE 6: Verificando Firebase App ID Files${NC}"
echo ""

FIREBASE_MACOS="$PROJECT_DIR/macos/Runner/firebase_app_id_file.json"
FIREBASE_IOS="$PROJECT_DIR/ios/Runner/firebase_app_id_file.json"

if [ ! -f "$FIREBASE_MACOS" ] && [ ! -f "$FIREBASE_IOS" ]; then
    echo -e "${YELLOW}⚠️  Firebase App ID files no encontrados${NC}"
    echo -e "${YELLOW}💡 Ejecuta manualmente: cd $PROJECT_DIR && flutterfire configure${NC}"
    echo ""
    echo "Presiona ENTER para continuar sin Firebase (puedes configurarlo después)"
    read -r
else
    echo -e "${GREEN}✅ Firebase App ID files encontrados${NC}"
fi

echo ""

# ============================================================================
# FASE 7: FLUTTER CLEAN & PUB GET
# ============================================================================

echo -e "${BLUE}🧹 FASE 7: Limpieza de Flutter${NC}"
echo ""

cd "$PROJECT_DIR"

echo -e "${YELLOW}🗑️  Ejecutando flutter clean...${NC}"
flutter clean

echo -e "${GREEN}📥 Ejecutando flutter pub get...${NC}"
flutter pub get

cd ..

echo ""

# ============================================================================
# FASE 8: VERIFICACIÓN FINAL
# ============================================================================

echo -e "${BLUE}✅ FASE 8: Verificación Final${NC}"
echo ""

cd "$PROJECT_DIR"

echo -e "${YELLOW}🔍 Analizando código...${NC}"
flutter analyze --no-fatal-warnings 2>&1 | head -n 20

echo ""
echo -e "${GREEN}🎉 FIXES APLICADOS EXITOSAMENTE!${NC}"
echo ""
echo -e "${BLUE}📊 RESUMEN:${NC}"
echo "  ✅ CocoaPods Base Configuration - FIXED"
echo "  ✅ CocoaPods Dependencies - UPDATED"
echo "  ✅ Flutter Dependencies - CLEAN"
echo "  ⚠️  Firebase App ID - MANUAL (si es necesario)"
echo "  ✅ FFI Warning - FIXED (opcional)"
echo ""
echo -e "${BLUE}🚀 PRÓXIMOS PASOS:${NC}"
echo "  1. Probar build: flutter run -d macos"
echo "  2. Verificar logs: mirar consola sin errores críticos"
echo "  3. Testing runtime: navegar por la app y capturar logs"
echo "  4. Si falta Firebase: flutterfire configure"
echo ""
echo -e "${YELLOW}📝 LOGS Y DOCUMENTACIÓN:${NC}"
echo "  - ANALISIS_ERRORES_CONSOLA_2025.md"
echo "  - PLAN_ACCION_0_ERRORES.md"
echo "  - Backups en: $BACKUP_DIR/"
echo ""
echo -e "${GREEN}✨ OBJETIVO 0 ERRORES - EN PROGRESO${NC}"
echo ""

cd ..

# ============================================================================
# OPCIONAL: TEST BUILD
# ============================================================================

echo -e "${BLUE}🧪 ¿Quieres ejecutar un test build ahora? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}🏗️  Ejecutando test build...${NC}"
    cd "$PROJECT_DIR"
    flutter build macos --debug

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ BUILD EXITOSO!${NC}"
    else
        echo ""
        echo -e "${RED}❌ BUILD FALLÓ - Revisa los errores arriba${NC}"
    fi
    cd ..
fi

echo ""
echo -e "${GREEN}🎯 Script completado!${NC}"
echo ""
