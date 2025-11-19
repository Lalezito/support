#!/bin/bash

# 🔒 SISTEMA DE BACKUP COMPLETO - ZODIAC CONSOLIDATION
# Fecha: 19 septiembre 2025
# Propósito: Backup multi-nivel antes de consolidación
# Autor: Claude + Alejandro

set -e

# Configuración
PROJECT_ROOT="/Users/alejandrocaceres/Desktop/appstore - zodia"
BACKUP_ROOT="$PROJECT_ROOT/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_ROOT/backup_log_$TIMESTAMP.log"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR $(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS $(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARNING $(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

# Crear estructura de backup
setup_backup_structure() {
    log "🏗️  Creando estructura de backup..."

    mkdir -p "$BACKUP_ROOT"/{full_project,zones,files,git_states,reports}
    mkdir -p "$BACKUP_ROOT"/zones/{services,widgets,screens,design_system,core,utils}
    mkdir -p "$BACKUP_ROOT"/files/{original,pre_edit,rollback}

    success "✅ Estructura de backup creada"
}

# Backup completo del proyecto
backup_full_project() {
    log "📦 Iniciando backup completo del proyecto..."

    FULL_BACKUP_NAME="backup_full_project_$TIMESTAMP.tar.gz"
    FULL_BACKUP_PATH="$BACKUP_ROOT/full_project/$FULL_BACKUP_NAME"

    # Excluir carpetas innecesarias
    tar --exclude='node_modules' \
        --exclude='.git' \
        --exclude='build' \
        --exclude='backups' \
        --exclude='*.log' \
        --exclude='.flutter-plugins*' \
        --exclude='*.iml' \
        -czf "$FULL_BACKUP_PATH" \
        -C "$PROJECT_ROOT/.." \
        "$(basename "$PROJECT_ROOT")"

    # Validar backup
    if [ -f "$FULL_BACKUP_PATH" ]; then
        BACKUP_SIZE=$(du -h "$FULL_BACKUP_PATH" | cut -f1)
        success "✅ Backup completo creado: $FULL_BACKUP_NAME ($BACKUP_SIZE)"

        # Crear metadata
        cat > "$BACKUP_ROOT/full_project/backup_metadata_$TIMESTAMP.json" << EOF
{
  "timestamp": "$TIMESTAMP",
  "backup_file": "$FULL_BACKUP_NAME",
  "backup_size": "$BACKUP_SIZE",
  "project_path": "$PROJECT_ROOT",
  "git_branch": "$(git branch --show-current)",
  "git_commit": "$(git rev-parse HEAD)",
  "flutter_version": "$(flutter --version | head -1)",
  "dart_version": "$(dart --version)"
}
EOF

    else
        error "❌ Error creando backup completo"
        exit 1
    fi
}

# Backup estado Git
backup_git_state() {
    log "🌿 Creando backup del estado Git..."

    GIT_BACKUP_DIR="$BACKUP_ROOT/git_states/git_state_$TIMESTAMP"
    mkdir -p "$GIT_BACKUP_DIR"

    cd "$PROJECT_ROOT"

    # Información de Git
    git status --porcelain > "$GIT_BACKUP_DIR/git_status.txt"
    git log --oneline -10 > "$GIT_BACKUP_DIR/git_log.txt"
    git branch -a > "$GIT_BACKUP_DIR/git_branches.txt"
    git diff > "$GIT_BACKUP_DIR/git_diff.txt"
    git diff --cached > "$GIT_BACKUP_DIR/git_diff_staged.txt"

    # Backup stash si existe
    if git stash list | grep -q .; then
        git stash list > "$GIT_BACKUP_DIR/git_stash_list.txt"
    fi

    success "✅ Estado Git respaldado"
}

# Backup árbol de dependencias
backup_dependency_tree() {
    log "🌳 Creando backup del árbol de dependencias..."

    DEP_BACKUP_DIR="$BACKUP_ROOT/reports/dependencies_$TIMESTAMP"
    mkdir -p "$DEP_BACKUP_DIR"

    cd "$PROJECT_ROOT/zodiac_app"

    # Flutter dependencies
    if [ -f "pubspec.yaml" ]; then
        cp pubspec.yaml "$DEP_BACKUP_DIR/"
        cp pubspec.lock "$DEP_BACKUP_DIR/"
        flutter pub deps > "$DEP_BACKUP_DIR/flutter_deps.txt" 2>/dev/null || true
    fi

    # Backend dependencies si existe
    if [ -f "../backend/package.json" ]; then
        cp ../backend/package.json "$DEP_BACKUP_DIR/"
        cp ../backend/package-lock.json "$DEP_BACKUP_DIR/" 2>/dev/null || true
    fi

    success "✅ Dependencias respaldadas"
}

# Backup zona específica
backup_zone() {
    local ZONE_NAME="$1"
    local ZONE_PATH="$2"

    log "📁 Creando backup de zona: $ZONE_NAME..."

    if [ ! -d "$ZONE_PATH" ]; then
        error "❌ Zona no encontrada: $ZONE_PATH"
        return 1
    fi

    ZONE_BACKUP_NAME="backup_${ZONE_NAME}_zone_$TIMESTAMP.tar.gz"
    ZONE_BACKUP_PATH="$BACKUP_ROOT/zones/$ZONE_NAME/$ZONE_BACKUP_NAME"

    mkdir -p "$BACKUP_ROOT/zones/$ZONE_NAME"

    tar -czf "$ZONE_BACKUP_PATH" -C "$(dirname "$ZONE_PATH")" "$(basename "$ZONE_PATH")"

    if [ -f "$ZONE_BACKUP_PATH" ]; then
        ZONE_SIZE=$(du -h "$ZONE_BACKUP_PATH" | cut -f1)
        success "✅ Backup zona $ZONE_NAME: $ZONE_SIZE"

        # Metadata zona
        cat > "$BACKUP_ROOT/zones/$ZONE_NAME/zone_metadata_$TIMESTAMP.json" << EOF
{
  "zone_name": "$ZONE_NAME",
  "zone_path": "$ZONE_PATH",
  "backup_file": "$ZONE_BACKUP_NAME",
  "backup_size": "$ZONE_SIZE",
  "timestamp": "$TIMESTAMP",
  "file_count": $(find "$ZONE_PATH" -type f | wc -l),
  "dart_files": $(find "$ZONE_PATH" -name "*.dart" | wc -l)
}
EOF
    else
        error "❌ Error en backup zona $ZONE_NAME"
        return 1
    fi
}

# Backup archivo específico
backup_file() {
    local FILE_PATH="$1"

    if [ ! -f "$FILE_PATH" ]; then
        error "❌ Archivo no encontrado: $FILE_PATH"
        return 1
    fi

    local FILE_NAME=$(basename "$FILE_PATH")
    local FILE_BACKUP_NAME="${FILE_NAME}_${TIMESTAMP}.bak"
    local FILE_BACKUP_PATH="$BACKUP_ROOT/files/original/$FILE_BACKUP_NAME"

    mkdir -p "$BACKUP_ROOT/files/original"
    cp "$FILE_PATH" "$FILE_BACKUP_PATH"

    success "✅ Archivo respaldado: $FILE_NAME"

    # Crear script de rollback
    cat > "$BACKUP_ROOT/files/rollback/rollback_${FILE_NAME}_${TIMESTAMP}.sh" << EOF
#!/bin/bash
# Rollback script para: $FILE_NAME
# Timestamp: $TIMESTAMP
# Original: $FILE_PATH

echo "🔄 Restaurando $FILE_NAME..."
cp "$FILE_BACKUP_PATH" "$FILE_PATH"
echo "✅ $FILE_NAME restaurado desde backup $TIMESTAMP"
EOF

    chmod +x "$BACKUP_ROOT/files/rollback/rollback_${FILE_NAME}_${TIMESTAMP}.sh"
}

# Validar espacio en disco
check_disk_space() {
    log "💾 Verificando espacio en disco..."

    AVAILABLE_SPACE=$(df -h "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
    AVAILABLE_BYTES=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')

    # Necesitamos al menos 5GB (5000000 KB)
    if [ "$AVAILABLE_BYTES" -lt 5000000 ]; then
        error "❌ Espacio insuficiente. Disponible: $AVAILABLE_SPACE. Necesario: >5GB"
        exit 1
    fi

    success "✅ Espacio disponible: $AVAILABLE_SPACE"
}

# Generar reporte de backup
generate_backup_report() {
    log "📊 Generando reporte de backup..."

    REPORT_PATH="$BACKUP_ROOT/reports/backup_report_$TIMESTAMP.md"

    cat > "$REPORT_PATH" << EOF
# 📋 REPORTE DE BACKUP - ZODIAC CONSOLIDATION

**Fecha**: $(date '+%Y-%m-%d %H:%M:%S')
**Timestamp**: $TIMESTAMP
**Proyecto**: Zodiac App Consolidation

## 📊 ESTADÍSTICAS DE BACKUP

### Backup Completo
- **Archivo**: backup_full_project_$TIMESTAMP.tar.gz
- **Tamaño**: $(du -h "$BACKUP_ROOT/full_project/backup_full_project_$TIMESTAMP.tar.gz" 2>/dev/null | cut -f1 || echo "N/A")
- **Estado**: ✅ Completado

### Estado Git
- **Branch**: $(git branch --show-current)
- **Commit**: $(git rev-parse --short HEAD)
- **Estado**: $(git status --porcelain | wc -l) archivos modificados

### Zonas Disponibles para Backup
- **services/**: $(find "$PROJECT_ROOT/zodiac_app/lib/services" -name "*.dart" 2>/dev/null | wc -l) archivos dart
- **widgets/**: $(find "$PROJECT_ROOT/zodiac_app/lib/widgets" -name "*.dart" 2>/dev/null | wc -l) archivos dart
- **screens/**: $(find "$PROJECT_ROOT/zodiac_app/lib/screens" -name "*.dart" 2>/dev/null | wc -l) archivos dart
- **design_system/**: $(find "$PROJECT_ROOT/zodiac_app/lib/design_system" -name "*.dart" 2>/dev/null | wc -l) archivos dart
- **core/**: $(find "$PROJECT_ROOT/zodiac_app/lib/core" -name "*.dart" 2>/dev/null | wc -l) archivos dart
- **utils/**: $(find "$PROJECT_ROOT/zodiac_app/lib/utils" -name "*.dart" 2>/dev/null | wc -l) archivos dart

## 🔧 COMANDOS DE USO

### Backup por Zona
\`\`\`bash
# Services
./scripts/backup_system.sh --zone services "$PROJECT_ROOT/zodiac_app/lib/services"

# Widgets
./scripts/backup_system.sh --zone widgets "$PROJECT_ROOT/zodiac_app/lib/widgets"

# Screens
./scripts/backup_system.sh --zone screens "$PROJECT_ROOT/zodiac_app/lib/screens"
\`\`\`

### Backup Archivo Individual
\`\`\`bash
./scripts/backup_system.sh --file "path/to/file.dart"
\`\`\`

### Rollback
\`\`\`bash
# Rollback completo
./scripts/rollback_system.sh --full $TIMESTAMP

# Rollback zona
./scripts/rollback_system.sh --zone services $TIMESTAMP

# Rollback archivo
./scripts/rollback_system.sh --file "filename.dart" $TIMESTAMP
\`\`\`

## ⚠️ ARCHIVOS PRESERVADOS

### UX Específicos (NUNCA TOCAR)
- compatibility_screen.dart
- home_screen.dart (custom logic)

### Traducciones (PRESERVAR SIEMPRE)
- lib/l10n/*
- lib/utils/simple_translations.dart

### Performance Críticos
- main_performance_optimized.dart
- core/*performance*
- core/*memory*

---
**✅ Sistema de backup listo para consolidación**
EOF

    success "✅ Reporte generado: backup_report_$TIMESTAMP.md"
}

# Función principal
main() {
    echo -e "${BLUE}🔒 SISTEMA DE BACKUP ZODIAC CONSOLIDATION${NC}"
    echo -e "${BLUE}===========================================${NC}"

    case "$1" in
        "--full")
            setup_backup_structure
            check_disk_space
            backup_full_project
            backup_git_state
            backup_dependency_tree
            generate_backup_report
            success "🎉 Backup completo finalizado!"
            ;;
        "--zone")
            if [ -z "$2" ] || [ -z "$3" ]; then
                error "❌ Uso: $0 --zone [nombre_zona] [ruta_zona]"
                exit 1
            fi
            setup_backup_structure
            backup_zone "$2" "$3"
            ;;
        "--file")
            if [ -z "$2" ]; then
                error "❌ Uso: $0 --file [ruta_archivo]"
                exit 1
            fi
            setup_backup_structure
            backup_file "$2"
            ;;
        "--help")
            echo "🔒 Sistema de Backup Zodiac Consolidation"
            echo ""
            echo "Uso:"
            echo "  $0 --full                    # Backup completo del proyecto"
            echo "  $0 --zone [nombre] [ruta]    # Backup zona específica"
            echo "  $0 --file [ruta]             # Backup archivo específico"
            echo "  $0 --help                    # Mostrar esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  $0 --full"
            echo "  $0 --zone services \"/path/to/lib/services\""
            echo "  $0 --file \"/path/to/file.dart\""
            ;;
        *)
            error "❌ Opción no válida: $1"
            echo "Usa --help para ver opciones disponibles"
            exit 1
            ;;
    esac
}

# Ejecutar
main "$@"