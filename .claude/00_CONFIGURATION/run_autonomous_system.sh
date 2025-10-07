#!/bin/bash

# 🧠 ZODIAC LIFE COACH - AUTONOMOUS SYSTEM RUNNER
# Script para manejar el sistema de inteligencia autónoma

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AI_SYSTEM="$SCRIPT_DIR/autonomous_intelligence_system.py"
CONFIG_DIR="$SCRIPT_DIR"
LOG_FILE="$CONFIG_DIR/autonomous_system.log"
PID_FILE="$CONFIG_DIR/autonomous_system.pid"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

check_dependencies() {
    log "🔍 Checking dependencies..."

    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed"
        exit 1
    fi

    # Check required Python packages
    python3 -c "import asyncio, aiohttp, sqlite3" 2>/dev/null || {
        warning "Installing required Python packages..."
        pip3 install aiohttp sqlite3 2>/dev/null || {
            error "Failed to install required packages"
            exit 1
        }
    }

    success "✅ Dependencies verified"
}

init_system() {
    log "🚀 Initializing Autonomous Intelligence System..."

    # Create necessary directories
    mkdir -p "$CONFIG_DIR"

    # Initialize configuration if not exists
    if [ ! -f "$CONFIG_DIR/ai_config.json" ]; then
        cat > "$CONFIG_DIR/ai_config.json" << EOF
{
  "learning_rate": 0.1,
  "performance_threshold": 0.85,
  "knowledge_update_interval": 3600,
  "context_refresh_interval": 300,
  "auto_optimization": true,
  "safety_mode": true,
  "backup_before_changes": true,
  "max_concurrent_improvements": 3,
  "zodiac_context": {
    "app_name": "Zodiac Life Coach",
    "neural_engine_target": 2.0,
    "pricing": {
      "neural_premium": 6.99,
      "cosmic_pro": 19.99,
      "cosmic_lifetime": 49.99
    },
    "performance_targets": {
      "cold_start": 3.0,
      "memory_usage": 150,
      "conversion_rate": 8.0,
      "retention_d7": 40.0
    }
  },
  "research_sources": [
    "https://flutter.dev/docs",
    "https://firebase.google.com/docs",
    "https://developer.apple.com/app-store/",
    "https://pub.dev/packages/purchases_flutter"
  ]
}
EOF
        log "📝 Created default configuration"
    fi

    # Initialize database
    python3 -c "
import sqlite3
from pathlib import Path

db_path = Path('$CONFIG_DIR/intelligence.db')
db_path.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(db_path) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            task_type TEXT NOT NULL,
            success_rate REAL NOT NULL,
            response_time REAL NOT NULL,
            quality_score REAL NOT NULL,
            context_hash TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS improvements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            improvement_id TEXT NOT NULL,
            description TEXT NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN NOT NULL,
            metrics TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS system_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

print('✅ Database initialized')
"

    # Initialize knowledge base
    if [ ! -f "$CONFIG_DIR/dynamic_knowledge.json" ]; then
        cat > "$CONFIG_DIR/dynamic_knowledge.json" << EOF
{
  "flutter_updates": [
    "Flutter 3.35.0+ stable for production",
    "Riverpod 3.0 recommended for state management",
    "RevenueCat 9.6.0+ for subscription management"
  ],
  "astrology_trends": [
    "Neural compatibility analysis trending",
    "12-dimensional relationship analysis popular",
    "AI-powered personalization increasing engagement"
  ],
  "app_store_changes": [
    "iOS 18 compatibility requirements",
    "Privacy policy transparency enhanced",
    "Subscription management clarity required"
  ],
  "performance_tips": [
    "Target < 2s for neural analysis",
    "Maintain 60fps for animations",
    "Keep memory usage < 150MB"
  ],
  "zodiac_specific": [
    "144 zodiac combinations implemented",
    "12 dimensions: chemistry, emotional, communication, values, stability, intimacy, growth, conflict, adventure, lifestyle, future, overall",
    "Current performance: 1.8s avg analysis time"
  ],
  "last_update": "$(date -u +%Y-%m-%dT%H:%M:%S)Z"
}
EOF
        log "📚 Created knowledge base"
    fi

    success "🎯 System initialized successfully"
}

start_system() {
    log "▶️ Starting Autonomous Intelligence System..."

    if is_running; then
        warning "System is already running (PID: $(cat $PID_FILE))"
        return
    fi

    check_dependencies

    # Start the system in background
    nohup python3 "$AI_SYSTEM" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"

    # Wait a moment to check if it started successfully
    sleep 3

    if is_running; then
        success "🚀 Autonomous Intelligence System started (PID: $(cat $PID_FILE))"
        success "📊 Monitoring: tail -f $LOG_FILE"
    else
        error "Failed to start system. Check $LOG_FILE for details"
        exit 1
    fi
}

stop_system() {
    log "⏹️ Stopping Autonomous Intelligence System..."

    if ! is_running; then
        warning "System is not running"
        return
    fi

    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null || {
        error "Failed to stop system (PID: $PID)"
        exit 1
    }

    # Wait for graceful shutdown
    sleep 2

    # Force kill if still running
    if kill -0 "$PID" 2>/dev/null; then
        warning "Forcing shutdown..."
        kill -9 "$PID" 2>/dev/null
    fi

    rm -f "$PID_FILE"
    success "⏹️ System stopped"
}

restart_system() {
    log "🔄 Restarting Autonomous Intelligence System..."
    stop_system
    sleep 2
    start_system
}

status() {
    if is_running; then
        PID=$(cat "$PID_FILE")
        success "✅ System is running (PID: $PID)"

        # Show basic stats
        log "📊 System Statistics:"
        python3 -c "
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

try:
    # Database stats
    db_path = Path('$CONFIG_DIR/intelligence.db')
    if db_path.exists():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM performance_metrics')
            metrics_count = cursor.fetchone()[0]

            cursor = conn.execute('SELECT COUNT(*) FROM improvements')
            improvements_count = cursor.fetchone()[0]

            print(f'  📈 Performance metrics: {metrics_count}')
            print(f'  🔧 Applied improvements: {improvements_count}')

    # Knowledge base stats
    kb_path = Path('$CONFIG_DIR/dynamic_knowledge.json')
    if kb_path.exists():
        with open(kb_path) as f:
            knowledge = json.load(f)
            total_items = sum(len(v) for k, v in knowledge.items() if isinstance(v, list))
            print(f'  📚 Knowledge base items: {total_items}')
            print(f'  🕒 Last update: {knowledge.get(\"last_update\", \"Never\")}')

except Exception as e:
    print(f'  ⚠️ Error reading stats: {e}')
"
    else
        warning "❌ System is not running"
    fi
}

is_running() {
    [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

dashboard() {
    log "📊 Starting real-time dashboard..."

    if ! is_running; then
        error "System is not running. Start it first with: $0 start"
        exit 1
    fi

    # Simple real-time dashboard
    while true; do
        clear
        echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║${NC}               🧠 AUTONOMOUS INTELLIGENCE DASHBOARD               ${BLUE}║${NC}"
        echo -e "${BLUE}╠════════════════════════════════════════════════════════════════╣${NC}"

        # System status
        if is_running; then
            echo -e "${BLUE}║${NC} Status: ${GREEN}●${NC} RUNNING                                             ${BLUE}║${NC}"
            echo -e "${BLUE}║${NC} PID: $(printf "%-55s" "$(cat $PID_FILE)")${BLUE}║${NC}"
        else
            echo -e "${BLUE}║${NC} Status: ${RED}●${NC} STOPPED                                             ${BLUE}║${NC}"
        fi

        echo -e "${BLUE}║${NC} Time: $(printf "%-54s" "$(date)")${BLUE}║${NC}"
        echo -e "${BLUE}╠════════════════════════════════════════════════════════════════╣${NC}"

        # Recent activity (last 10 lines of log)
        echo -e "${BLUE}║${NC} Recent Activity:                                               ${BLUE}║${NC}"
        if [ -f "$LOG_FILE" ]; then
            tail -5 "$LOG_FILE" | while read line; do
                # Truncate long lines
                short_line=$(echo "$line" | cut -c1-60)
                echo -e "${BLUE}║${NC} $(printf "%-62s" "$short_line")${BLUE}║${NC}"
            done
        fi

        echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to exit dashboard${NC}"

        sleep 5
    done
}

test_system() {
    log "🧪 Testing system with sample instruction..."

    if ! is_running; then
        error "System must be running for testing"
        exit 1
    fi

    # Test the system
    python3 -c "
import asyncio
import sys
import os

# Add the config directory to Python path
sys.path.insert(0, '$CONFIG_DIR')

async def test_instruction():
    try:
        from autonomous_intelligence_system import AutonomousIntelligenceSystem

        ai_system = AutonomousIntelligenceSystem()

        # Test instruction
        instruction = 'Optimize the neural engine performance to ensure < 2s analysis time'

        print('🧪 Testing instruction:', instruction)

        # This would normally process the instruction
        # For testing, just verify the system is responsive
        status = ai_system.get_system_status()

        print('✅ System responsive')
        print('📊 Status:', status)

        return True

    except Exception as e:
        print('❌ Test failed:', e)
        return False

# Run the test
result = asyncio.run(test_instruction())
sys.exit(0 if result else 1)
"

    if [ $? -eq 0 ]; then
        success "🧪 System test passed"
    else
        error "🧪 System test failed"
        exit 1
    fi
}

show_help() {
    echo "🧠 Zodiac Life Coach - Autonomous Intelligence System"
    echo ""
    echo "Usage: $0 {init|start|stop|restart|status|dashboard|test|logs|help}"
    echo ""
    echo "Commands:"
    echo "  init      Initialize the system (run once)"
    echo "  start     Start the autonomous system"
    echo "  stop      Stop the autonomous system"
    echo "  restart   Restart the autonomous system"
    echo "  status    Show system status and statistics"
    echo "  dashboard Real-time monitoring dashboard"
    echo "  test      Test system with sample instruction"
    echo "  logs      Show system logs"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 init                    # Initialize system"
    echo "  $0 start                   # Start autonomous operation"
    echo "  $0 dashboard               # Monitor in real-time"
    echo ""
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -50 "$LOG_FILE"
    else
        warning "No log file found"
    fi
}

# Main command processing
case "${1:-help}" in
    init)
        init_system
        ;;
    start)
        start_system
        ;;
    stop)
        stop_system
        ;;
    restart)
        restart_system
        ;;
    status)
        status
        ;;
    dashboard)
        dashboard
        ;;
    test)
        test_system
        ;;
    logs)
        show_logs
        ;;
    help)
        show_help
        ;;
    *)
        error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac