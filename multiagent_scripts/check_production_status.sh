#!/bin/bash

# Production Status Checker Script
# Checks the status of all production optimization agents

echo "📊 Production Agents Status Report"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_DIR="zodiac_app/.multiagent-tracking"

# Function to check agent status
check_agent() {
    local agent_name=$1
    local status_file="$BASE_DIR/agent-${agent_name,,}.status"

    if [[ -f "$status_file" ]]; then
        local status=$(cat "$status_file")
        if [[ "$status" == "complete" ]]; then
            echo -e "${GREEN}✅ $agent_name: COMPLETE${NC}"
        elif [[ "$status" == "in_progress" ]]; then
            echo -e "${YELLOW}🔄 $agent_name: IN PROGRESS${NC}"
        elif [[ "$status" == "failed" ]]; then
            echo -e "${RED}❌ $agent_name: FAILED${NC}"
        else
            echo -e "${BLUE}⏳ $agent_name: $status${NC}"
        fi
    else
        echo -e "${YELLOW}⏸️  $agent_name: NOT STARTED${NC}"
    fi
}

# Check orchestrator
if [[ -f "$BASE_DIR/orchestrator.start_time" ]]; then
    START_TIME=$(cat "$BASE_DIR/orchestrator.start_time")
    echo -e "${BLUE}🎯 Orchestrator started: $START_TIME${NC}"
    echo ""
fi

# Check all agents
echo "Agent Status:"
echo "-------------"
check_agent "Performance"
check_agent "Security"
check_agent "UX"
check_agent "Testing"
check_agent "Analytics"
check_agent "Deployment"

echo ""
echo "Progress Summary:"
echo "----------------"

# Count completed agents
COMPLETED=$(find "$BASE_DIR" -name "*.status" -exec grep -l "complete" {} \; | wc -l)
TOTAL=6
PERCENTAGE=$((COMPLETED * 100 / TOTAL))

echo "Completed: $COMPLETED/$TOTAL ($PERCENTAGE%)"

if [[ $COMPLETED -eq $TOTAL ]]; then
    echo -e "${GREEN}🎉 All agents completed! Ready for production.${NC}"
elif [[ $COMPLETED -ge 4 ]]; then
    echo -e "${YELLOW}⚠️  Most agents completed. Review remaining items.${NC}"
else
    echo -e "${RED}❌ Many agents still pending. Continue execution.${NC}"
fi

echo ""
echo "Next Steps:"
echo "-----------"
if [[ $COMPLETED -lt $TOTAL ]]; then
    echo "1. Check individual agent logs for errors"
    echo "2. Restart failed agents if needed"
    echo "3. Run integration tests after completion"
fi

echo "4. Execute final production validation"
echo "5. Deploy to staging environment"
echo "6. Run user acceptance testing"