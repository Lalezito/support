#!/bin/bash
# 🚨 EMERGENCY OVERRIDE SYSTEM - Protocolo V2.0
# Allows temporary bypass of critical file restrictions during production emergencies

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Emergency situations that justify override
VALID_EMERGENCIES=(
    "app_crash_production"
    "revenue_system_down"
    "security_breach"
    "app_store_rejection"
    "critical_user_data_loss"
)

activate_emergency_override() {
    local reason=$1
    local duration_hours=${2:-4}  # Default 4 hours

    if [[ -z "$reason" ]]; then
        echo -e "${RED}❌ Emergency reason required${NC}"
        echo "Usage: $0 \"reason\" [duration_hours]"
        echo ""
        echo "Valid emergency reasons:"
        for emergency in "${VALID_EMERGENCIES[@]}"; do
            echo "  - $emergency"
        done
        exit 1
    fi

    # Validate reason
    local valid=false
    for valid_emergency in "${VALID_EMERGENCIES[@]}"; do
        if [[ "$reason" == *"$valid_emergency"* ]]; then
            valid=true
            break
        fi
    done

    if [[ "$valid" == false ]]; then
        echo -e "${YELLOW}⚠️  Warning: Non-standard emergency reason${NC}"
        echo "Reason: $reason"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Emergency override cancelled"
            exit 1
        fi
    fi

    # Calculate expiration
    local expiration=$(date -d "+${duration_hours} hours" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -v +${duration_hours}H '+%Y-%m-%d %H:%M:%S')

    # Create override file
    echo "$expiration" > .emergency_override

    # Log emergency activation
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] EMERGENCY OVERRIDE ACTIVATED: $reason (expires: $expiration)" >> .emergency_log

    echo -e "${RED}🚨 EMERGENCY OVERRIDE ACTIVATED${NC}"
    echo "================================================"
    echo -e "📋 ${YELLOW}Reason:${NC} $reason"
    echo -e "⏰ ${YELLOW}Duration:${NC} $duration_hours hours"
    echo -e "📅 ${YELLOW}Expires:${NC} $expiration"
    echo ""
    echo -e "${YELLOW}⚠️  EMERGENCY PROTOCOLS IN EFFECT:${NC}"
    echo "   1. ⏱️  Maximum $duration_hours hours to resolve"
    echo "   2. 📞 Notify team lead immediately"
    echo "   3. 🎯 Make ONLY minimal changes to resolve emergency"
    echo "   4. 📝 Document all changes made"
    echo "   5. 🔍 Post-emergency review within 24 hours"
    echo ""
    echo -e "${GREEN}✅ Critical file restrictions temporarily lifted${NC}"

    # Set reminder for post-emergency review
    echo "echo '🔔 Emergency override expired - Post-emergency review required'" | at now + ${duration_hours} hours 2>/dev/null || true
}

check_override_status() {
    if [[ -f ".emergency_override" ]]; then
        local expiration=$(cat .emergency_override)
        local current=$(date '+%Y-%m-%d %H:%M:%S')

        if [[ "$current" > "$expiration" ]]; then
            echo -e "${YELLOW}⏰ Emergency override expired${NC}"
            rm -f .emergency_override
            echo "🔔 Post-emergency review required - see .emergency_log"
            return 1
        else
            echo -e "${RED}🚨 Emergency override active until: $expiration${NC}"
            return 0
        fi
    else
        echo -e "${GREEN}✅ No emergency override active${NC}"
        return 1
    fi
}

deactivate_override() {
    if [[ -f ".emergency_override" ]]; then
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$timestamp] EMERGENCY OVERRIDE DEACTIVATED (manual)" >> .emergency_log
        rm -f .emergency_override
        echo -e "${GREEN}✅ Emergency override deactivated${NC}"
    else
        echo "No active emergency override"
    fi
}

show_emergency_log() {
    if [[ -f ".emergency_log" ]]; then
        echo -e "${YELLOW}📋 EMERGENCY OVERRIDE LOG:${NC}"
        echo "=================================="
        cat .emergency_log
    else
        echo "No emergency log found"
    fi
}

# Main command handling
case "${1:-status}" in
    "activate"|"start")
        activate_emergency_override "$2" "$3"
        ;;
    "status"|"check")
        check_override_status
        ;;
    "deactivate"|"stop")
        deactivate_override
        ;;
    "log"|"history")
        show_emergency_log
        ;;
    *)
        if [[ -n "$1" ]]; then
            # Direct activation with reason
            activate_emergency_override "$1" "$2"
        else
            echo "🚨 EMERGENCY OVERRIDE SYSTEM"
            echo "=============================="
            echo "Usage:"
            echo "  $0 activate \"reason\" [hours]  - Activate emergency override"
            echo "  $0 status                     - Check override status"
            echo "  $0 deactivate                - Deactivate override"
            echo "  $0 log                       - Show emergency log"
            echo ""
            echo "Quick activation:"
            echo "  $0 \"emergency_reason\" [hours]"
            echo ""
            check_override_status
        fi
        ;;
esac