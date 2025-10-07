#!/bin/bash

# Zodiac Life Coach Self-Improvement System Launcher
# This script provides easy commands to manage the self-improvement system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_DIR="${SCRIPT_DIR}"
PYTHON_SCRIPT="${SYSTEM_DIR}/self_improvement_system.py"
CONFIG_FILE="${SYSTEM_DIR}/self_improvement_config.json"
DASHBOARD_SCRIPT="${SYSTEM_DIR}/monitoring_dashboard.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log "Checking system dependencies..."

    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed."
        exit 1
    fi

    if ! python3 -c "import json, sqlite3, threading, requests" 2>/dev/null; then
        error "Required Python modules are missing. Install with: pip install requests"
        exit 1
    fi

    success "All dependencies are available"
}

# Initialize the system
init_system() {
    log "Initializing Self-Improvement System..."

    # Create necessary directories
    mkdir -p "${SYSTEM_DIR}/data"
    mkdir -p "${SYSTEM_DIR}/logs"
    mkdir -p "${SYSTEM_DIR}/backups"

    # Initialize database if it doesn't exist
    if [ ! -f "${SYSTEM_DIR}/performance_metrics.db" ]; then
        log "Creating performance metrics database..."
        python3 -c "
from ${SYSTEM_DIR}/self_improvement_system import PerformanceTracker
tracker = PerformanceTracker('${SYSTEM_DIR}/performance_metrics.db')
print('Database initialized successfully')
"
    fi

    # Create default config if it doesn't exist
    if [ ! -f "${CONFIG_FILE}" ]; then
        warn "Configuration file not found. Using defaults."
    fi

    # Initialize knowledge graph
    if [ ! -f "${SYSTEM_DIR}/knowledge_graph.json" ]; then
        echo '{"domains": {}, "relationships": {}, "update_history": [], "version": "1.0"}' > "${SYSTEM_DIR}/knowledge_graph.json"
        log "Knowledge graph initialized"
    fi

    success "System initialization complete"
}

# Start the self-improvement system
start_system() {
    log "Starting Self-Improvement System..."

    if [ -f "${SYSTEM_DIR}/.system.pid" ]; then
        local pid=$(cat "${SYSTEM_DIR}/.system.pid")
        if ps -p $pid > /dev/null 2>&1; then
            warn "System is already running (PID: $pid)"
            return 0
        else
            rm -f "${SYSTEM_DIR}/.system.pid"
        fi
    fi

    # Start the system in background
    nohup python3 "${PYTHON_SCRIPT}" > "${SYSTEM_DIR}/logs/system.log" 2>&1 &
    local pid=$!
    echo $pid > "${SYSTEM_DIR}/.system.pid"

    sleep 2

    if ps -p $pid > /dev/null 2>&1; then
        success "Self-Improvement System started (PID: $pid)"
        log "View logs with: tail -f ${SYSTEM_DIR}/logs/system.log"
    else
        error "Failed to start system. Check logs for details."
        rm -f "${SYSTEM_DIR}/.system.pid"
        exit 1
    fi
}

# Stop the self-improvement system
stop_system() {
    log "Stopping Self-Improvement System..."

    if [ -f "${SYSTEM_DIR}/.system.pid" ]; then
        local pid=$(cat "${SYSTEM_DIR}/.system.pid")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            sleep 2
            if ps -p $pid > /dev/null 2>&1; then
                warn "Process didn't stop gracefully, forcing termination..."
                kill -9 $pid
            fi
            rm -f "${SYSTEM_DIR}/.system.pid"
            success "System stopped"
        else
            warn "System is not running"
            rm -f "${SYSTEM_DIR}/.system.pid"
        fi
    else
        warn "No PID file found. System may not be running."
    fi
}

# Check system status
check_status() {
    log "Checking system status..."

    if [ -f "${SYSTEM_DIR}/.system.pid" ]; then
        local pid=$(cat "${SYSTEM_DIR}/.system.pid")
        if ps -p $pid > /dev/null 2>&1; then
            success "System is running (PID: $pid)"

            # Check system health
            if [ -f "${SYSTEM_DIR}/performance_metrics.db" ]; then
                local metric_count=$(sqlite3 "${SYSTEM_DIR}/performance_metrics.db" "SELECT COUNT(*) FROM metrics;" 2>/dev/null || echo "0")
                log "Metrics collected: $metric_count"
            fi

            if [ -f "${SYSTEM_DIR}/knowledge_graph.json" ]; then
                local domain_count=$(python3 -c "
import json
try:
    with open('${SYSTEM_DIR}/knowledge_graph.json', 'r') as f:
        data = json.load(f)
        print(len(data.get('domains', {})))
except:
    print('0')
" 2>/dev/null)
                log "Knowledge domains: $domain_count"
            fi
        else
            warn "System is not running (stale PID file)"
            rm -f "${SYSTEM_DIR}/.system.pid"
        fi
    else
        warn "System is not running"
    fi
}

# Start monitoring dashboard
start_dashboard() {
    log "Starting Monitoring Dashboard..."
    python3 "${DASHBOARD_SCRIPT}"
}

# View system logs
view_logs() {
    local log_type="${1:-system}"

    case $log_type in
        "system")
            if [ -f "${SYSTEM_DIR}/logs/system.log" ]; then
                tail -f "${SYSTEM_DIR}/logs/system.log"
            else
                warn "System log not found"
            fi
            ;;
        "performance")
            log "Performance metrics from database:"
            sqlite3 "${SYSTEM_DIR}/performance_metrics.db" "
                SELECT datetime(timestamp), name, value, target
                FROM metrics
                ORDER BY timestamp DESC
                LIMIT 20;
            " 2>/dev/null || warn "Could not read performance metrics"
            ;;
        *)
            error "Unknown log type: $log_type"
            echo "Available types: system, performance"
            ;;
    esac
}

# Backup system data
backup_system() {
    local backup_dir="${SYSTEM_DIR}/backups/backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"

    log "Creating system backup at $backup_dir..."

    # Backup database
    if [ -f "${SYSTEM_DIR}/performance_metrics.db" ]; then
        cp "${SYSTEM_DIR}/performance_metrics.db" "$backup_dir/"
        log "Database backed up"
    fi

    # Backup knowledge graph
    if [ -f "${SYSTEM_DIR}/knowledge_graph.json" ]; then
        cp "${SYSTEM_DIR}/knowledge_graph.json" "$backup_dir/"
        log "Knowledge graph backed up"
    fi

    # Backup learning history
    if [ -f "${SYSTEM_DIR}/learning_history.json" ]; then
        cp "${SYSTEM_DIR}/learning_history.json" "$backup_dir/"
        log "Learning history backed up"
    fi

    # Backup configuration
    if [ -f "${CONFIG_FILE}" ]; then
        cp "${CONFIG_FILE}" "$backup_dir/"
        log "Configuration backed up"
    fi

    success "Backup created at $backup_dir"
}

# Reset system (with confirmation)
reset_system() {
    warn "This will reset all learning data and metrics!"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Resetting system..."

        # Stop system if running
        stop_system

        # Remove data files
        rm -f "${SYSTEM_DIR}/performance_metrics.db"
        rm -f "${SYSTEM_DIR}/knowledge_graph.json"
        rm -f "${SYSTEM_DIR}/learning_history.json"

        # Reinitialize
        init_system

        success "System reset complete"
    else
        log "Reset cancelled"
    fi
}

# Show help
show_help() {
    cat << EOF
🌟 Zodiac Life Coach Self-Improvement System Manager

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  init          Initialize the system (create directories, databases)
  start         Start the self-improvement system
  stop          Stop the self-improvement system
  restart       Restart the system (stop + start)
  status        Check system status
  dashboard     Start the monitoring dashboard
  logs [type]   View system logs (types: system, performance)
  backup        Create a backup of system data
  reset         Reset all system data (WARNING: destructive)
  help          Show this help message

Examples:
  $0 init                 # Initialize system
  $0 start                # Start the system
  $0 dashboard            # View real-time dashboard
  $0 logs system          # View system logs
  $0 backup               # Create backup

For more information, see the implementation roadmap and architecture documentation.
EOF
}

# Main command dispatcher
main() {
    case "${1:-help}" in
        "init")
            check_dependencies
            init_system
            ;;
        "start")
            check_dependencies
            start_system
            ;;
        "stop")
            stop_system
            ;;
        "restart")
            stop_system
            sleep 1
            check_dependencies
            start_system
            ;;
        "status")
            check_status
            ;;
        "dashboard")
            check_dependencies
            start_dashboard
            ;;
        "logs")
            view_logs "$2"
            ;;
        "backup")
            backup_system
            ;;
        "reset")
            reset_system
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"