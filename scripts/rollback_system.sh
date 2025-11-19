#!/bin/bash

# 🔄 SISTEMA DE ROLLBACK COMPLETO - ZODIAC CONSOLIDATION
# Fecha: 19 septiembre 2025
# Propósito: Rollback multi-nivel para consolidación
# Autor: Claude + Alejandro

set -e

# Configuración
PROJECT_ROOT="/Users/alejandrocaceres/Desktop/appstore - zodia"
BACKUP_ROOT="$PROJECT_ROOT/backups"
LOG_FILE="$BACKUP_ROOT/rollback_log_$(date +%Y%m%d_%H%M%S).log"

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

# Listar backups disponibles
list_backups() {
    log "📋 Listando backups disponibles..."

    echo -e "${YELLOW}=== BACKUPS COMPLETOS ===${NC}"
    if [ -d "$BACKUP_ROOT/full_project" ]; then
        ls -la "$BACKUP_ROOT/full_project" | grep backup_full_project | while read line; do
            echo -e "${GREEN}📦${NC} $line"
        done
    else
        warn "No hay backups completos disponibles"
    fi

    echo -e "${YELLOW}=== BACKUPS POR ZONA ===${NC}"
    for zone in services widgets screens design_system core utils; do
        if [ -d "$BACKUP_ROOT/zones/$zone" ]; then
            ZONE_BACKUPS=$(ls "$BACKUP_ROOT/zones/$zone" 2>/dev/null | grep backup_ | wc -l)
            if [ "$ZONE_BACKUPS" -gt 0 ]; then
                echo -e "${GREEN}📁 $zone:${NC} $ZONE_BACKUPS backups"
                ls "$BACKUP_ROOT/zones/$zone" | grep backup_ | head -3
            fi
        fi
    done

    echo -e "${YELLOW}=== BACKUPS DE ARCHIVOS ===${NC}"
    if [ -d "$BACKUP_ROOT/files/original" ]; then
        FILE_BACKUPS=$(ls "$BACKUP_ROOT/files/original" 2>/dev/null | wc -l)
        echo -e "${GREEN}📄${NC} Archivos individuales: $FILE_BACKUPS backups"
    fi
}

# Validar backup existe
validate_backup() {
    local BACKUP_TYPE="$1"
    local BACKUP_ID="$2"
    local ZONE_NAME="$3"

    case "$BACKUP_TYPE" in
        "full")
            BACKUP_FILE="$BACKUP_ROOT/full_project/backup_full_project_${BACKUP_ID}.tar.gz"
            if [ ! -f "$BACKUP_FILE" ]; then
                error "❌ Backup completo no encontrado: $BACKUP_ID"
                return 1
            fi
            ;;
        "zone")
            BACKUP_FILE="$BACKUP_ROOT/zones/${ZONE_NAME}/backup_${ZONE_NAME}_zone_${BACKUP_ID}.tar.gz"
            if [ ! -f "$BACKUP_FILE" ]; then
                error "❌ Backup de zona no encontrado: $ZONE_NAME / $BACKUP_ID"
                return 1
            fi
            ;;
        "file")
            # Para archivos, el BACKUP_ID es el nombre del archivo
            BACKUP_FILE="$BACKUP_ROOT/files/original/${BACKUP_ID}_*.bak"
            if ! ls $BACKUP_FILE 1> /dev/null 2>&1; then
                error "❌ Backup de archivo no encontrado: $BACKUP_ID"
                return 1
            fi
            ;;
    esac

    success "✅ Backup validado: $BACKUP_FILE"
    return 0
}

# Rollback completo
rollback_full() {
    local BACKUP_ID="$1"

    log "🔄 Iniciando rollback completo con backup: $BACKUP_ID"

    # Validar backup
    if ! validate_backup "full" "$BACKUP_ID"; then
        exit 1
    fi

    BACKUP_FILE="$BACKUP_ROOT/full_project/backup_full_project_${BACKUP_ID}.tar.gz"

    # Confirmar acción
    echo -e "${RED}⚠️  ATENCIÓN: Esto restaurará TODO el proyecto al estado del backup${NC}"
    echo -e "${RED}⚠️  Todos los cambios posteriores se perderán${NC}"
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warn "❌ Rollback cancelado por el usuario"
        exit 1
    fi

    # Crear backup del estado actual antes de rollback
    log "💾 Creando backup del estado actual antes de rollback..."
    TEMP_BACKUP="$BACKUP_ROOT/pre_rollback_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar --exclude='backups' -czf "$TEMP_BACKUP" -C "$PROJECT_ROOT/.." "$(basename "$PROJECT_ROOT")" || warn "⚠️ No se pudo crear backup pre-rollback"

    # Realizar rollback
    log "🔄 Extrayendo backup completo..."

    # Crear directorio temporal
    TEMP_DIR="$BACKUP_ROOT/temp_restore_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$TEMP_DIR"

    # Extraer backup
    tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

    # Mover archivos (excepto backups)
    EXTRACTED_DIR="$TEMP_DIR/$(basename "$PROJECT_ROOT")"

    if [ -d "$EXTRACTED_DIR" ]; then
        # Preservar carpeta backups
        if [ -d "$PROJECT_ROOT/backups" ]; then
            mv "$PROJECT_ROOT/backups" "$TEMP_DIR/backups_preserve"
        fi

        # Remover proyecto actual
        rm -rf "$PROJECT_ROOT"/*
        rm -rf "$PROJECT_ROOT"/.??*

        # Restaurar desde backup
        cp -r "$EXTRACTED_DIR"/* "$PROJECT_ROOT/"
        cp -r "$EXTRACTED_DIR"/.??* "$PROJECT_ROOT/" 2>/dev/null || true

        # Restaurar carpeta backups
        if [ -d "$TEMP_DIR/backups_preserve" ]; then
            mv "$TEMP_DIR/backups_preserve" "$PROJECT_ROOT/backups"
        fi

        success "✅ Rollback completo finalizado"

        # Limpiar directorio temporal
        rm -rf "$TEMP_DIR"

        # Mostrar estado post-rollback
        cd "$PROJECT_ROOT"
        log "📊 Estado post-rollback:"
        git status 2>/dev/null || warn "⚠️ No es un repositorio git"

    else
        error "❌ Error extrayendo backup"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
}

# Rollback zona específica
rollback_zone() {
    local ZONE_NAME="$1"
    local BACKUP_ID="$2"

    log "📁 Iniciando rollback de zona: $ZONE_NAME con backup: $BACKUP_ID"

    # Validar backup
    if ! validate_backup "zone" "$BACKUP_ID" "$ZONE_NAME"; then
        exit 1
    fi

    BACKUP_FILE="$BACKUP_ROOT/zones/${ZONE_NAME}/backup_${ZONE_NAME}_zone_${BACKUP_ID}.tar.gz"
    ZONE_PATH="$PROJECT_ROOT/zodiac_app/lib/$ZONE_NAME"

    # Confirmar acción
    echo -e "${YELLOW}⚠️  Esto restaurará la zona $ZONE_NAME al backup $BACKUP_ID${NC}"
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warn "❌ Rollback de zona cancelado"
        exit 1
    fi

    # Backup actual de la zona antes de rollback
    if [ -d "$ZONE_PATH" ]; then
        TEMP_ZONE_BACKUP="$BACKUP_ROOT/zones/$ZONE_NAME/pre_rollback_${ZONE_NAME}_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "$TEMP_ZONE_BACKUP" -C "$(dirname "$ZONE_PATH")" "$(basename "$ZONE_PATH")" || warn "⚠️ No se pudo crear backup pre-rollback de zona"
        log "💾 Backup pre-rollback creado: $(basename "$TEMP_ZONE_BACKUP")"
    fi

    # Crear directorio temporal
    TEMP_DIR="$BACKUP_ROOT/temp_zone_restore_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$TEMP_DIR"

    # Extraer backup de zona
    tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

    # Determinar directorio extraído
    EXTRACTED_ZONE_DIR="$TEMP_DIR/$ZONE_NAME"
    if [ ! -d "$EXTRACTED_ZONE_DIR" ]; then
        # Buscar directorio extraído
        EXTRACTED_ZONE_DIR=$(find "$TEMP_DIR" -type d -name "$ZONE_NAME" | head -1)
    fi

    if [ -d "$EXTRACTED_ZONE_DIR" ]; then
        # Remover zona actual
        if [ -d "$ZONE_PATH" ]; then
            rm -rf "$ZONE_PATH"
        fi

        # Restaurar zona desde backup
        cp -r "$EXTRACTED_ZONE_DIR" "$(dirname "$ZONE_PATH")/"

        success "✅ Rollback de zona $ZONE_NAME completado"

        # Limpiar directorio temporal
        rm -rf "$TEMP_DIR"

        # Mostrar archivos restaurados
        log "📊 Archivos restaurados en zona $ZONE_NAME:"
        find "$ZONE_PATH" -name "*.dart" | wc -l | xargs echo "Archivos .dart:"

    else
        error "❌ Error extrayendo backup de zona"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
}

# Rollback archivo específico
rollback_file() {
    local FILE_NAME="$1"
    local BACKUP_ID="$2"

    log "📄 Iniciando rollback de archivo: $FILE_NAME"

    # Buscar backup del archivo
    BACKUP_PATTERN="$BACKUP_ROOT/files/original/${FILE_NAME}_*.bak"

    if [ -n "$BACKUP_ID" ]; then
        BACKUP_FILE="$BACKUP_ROOT/files/original/${FILE_NAME}_${BACKUP_ID}.bak"
    else
        # Usar el backup más reciente
        BACKUP_FILE=$(ls -t $BACKUP_PATTERN 2>/dev/null | head -1)
    fi

    if [ ! -f "$BACKUP_FILE" ]; then
        error "❌ Backup de archivo no encontrado: $FILE_NAME"
        echo "Backups disponibles:"
        ls $BACKUP_PATTERN 2>/dev/null || echo "No hay backups para $FILE_NAME"
        exit 1
    fi

    # Buscar archivo original en el proyecto
    ORIGINAL_FILE=$(find "$PROJECT_ROOT" -name "$FILE_NAME" -path "*/lib/*" | head -1)

    if [ -z "$ORIGINAL_FILE" ]; then
        error "❌ Archivo original no encontrado: $FILE_NAME"
        exit 1
    fi

    # Confirmar acción
    echo -e "${YELLOW}⚠️  Esto restaurará $FILE_NAME desde backup$(NC}"
    echo -e "${YELLOW}⚠️  Archivo actual: $ORIGINAL_FILE${NC}"
    echo -e "${YELLOW}⚠️  Backup: $(basename "$BACKUP_FILE")${NC}"
    read -p "¿Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        warn "❌ Rollback de archivo cancelado"
        exit 1
    fi

    # Crear backup del archivo actual
    CURRENT_BACKUP="$BACKUP_ROOT/files/original/${FILE_NAME}_pre_rollback_$(date +%Y%m%d_%H%M%S).bak"
    cp "$ORIGINAL_FILE" "$CURRENT_BACKUP" || warn "⚠️ No se pudo crear backup del archivo actual"

    # Restaurar archivo
    cp "$BACKUP_FILE" "$ORIGINAL_FILE"

    success "✅ Archivo $FILE_NAME restaurado desde $(basename "$BACKUP_FILE")"
    log "💾 Backup del archivo actual creado: $(basename "$CURRENT_BACKUP")"
}

# Rollback automático (último backup)
rollback_last() {
    log "🔄 Buscando último backup para rollback automático..."

    # Buscar el backup completo más reciente
    LAST_FULL_BACKUP=$(ls -t "$BACKUP_ROOT/full_project/backup_full_project_"*.tar.gz 2>/dev/null | head -1)

    if [ -n "$LAST_FULL_BACKUP" ]; then
        BACKUP_ID=$(basename "$LAST_FULL_BACKUP" | sed 's/backup_full_project_\(.*\).tar.gz/\1/')
        warn "🎯 Último backup encontrado: $BACKUP_ID"

        echo -e "${RED}⚠️  ROLLBACK AUTOMÁTICO AL ÚLTIMO BACKUP${NC}"
        echo -e "${RED}⚠️  Backup: $BACKUP_ID${NC}"
        read -p "¿Continuar con rollback automático? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rollback_full "$BACKUP_ID"
        else
            warn "❌ Rollback automático cancelado"
        fi
    else
        error "❌ No se encontraron backups para rollback automático"
        exit 1
    fi
}

# Función principal
main() {
    echo -e "${BLUE}🔄 SISTEMA DE ROLLBACK ZODIAC CONSOLIDATION${NC}"
    echo -e "${BLUE}============================================${NC}"

    # Crear log file
    mkdir -p "$BACKUP_ROOT"

    case "$1" in
        "--full")
            if [ -z "$2" ]; then
                error "❌ Uso: $0 --full [backup_id]"
                exit 1
            fi
            rollback_full "$2"
            ;;
        "--zone")
            if [ -z "$2" ] || [ -z "$3" ]; then
                error "❌ Uso: $0 --zone [zona] [backup_id]"
                exit 1
            fi
            rollback_zone "$2" "$3"
            ;;
        "--file")
            if [ -z "$2" ]; then
                error "❌ Uso: $0 --file [nombre_archivo] [backup_id_opcional]"
                exit 1
            fi
            rollback_file "$2" "$3"
            ;;
        "--last")
            rollback_last
            ;;
        "--list")
            list_backups
            ;;
        "--help")
            echo "🔄 Sistema de Rollback Zodiac Consolidation"
            echo ""
            echo "Uso:"
            echo "  $0 --full [backup_id]           # Rollback completo"
            echo "  $0 --zone [zona] [backup_id]    # Rollback zona específica"
            echo "  $0 --file [archivo] [backup_id] # Rollback archivo específico"
            echo "  $0 --last                       # Rollback al último backup"
            echo "  $0 --list                       # Listar backups disponibles"
            echo "  $0 --help                       # Mostrar esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  $0 --full 20250919_143022"
            echo "  $0 --zone services 20250919_143022"
            echo "  $0 --file compatibility_service.dart"
            echo "  $0 --last"
            echo "  $0 --list"
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