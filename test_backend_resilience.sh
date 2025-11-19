#!/bin/bash

# Backend Resilience Testing Script
# Tests the 3-level fallback cascade: Railway → Cache → Local
# Location: /Users/alejandrocaceres/Desktop/appstore.zodia/

echo "═══════════════════════════════════════════════════════════"
echo "  Backend Resilience Testing Suite"
echo "  Testing: Railway → Cache → Local Generation Cascade"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test header
print_test_header() {
    echo ""
    echo "───────────────────────────────────────────────────────────"
    echo -e "${BLUE}TEST $1: $2${NC}"
    echo "───────────────────────────────────────────────────────────"
}

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASSED${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Function to wait for user confirmation
wait_for_user() {
    echo ""
    echo -e "${YELLOW}Press ENTER when ready to continue...${NC}"
    read
}

# Function to check logs
check_log() {
    local pattern=$1
    local description=$2

    echo "Checking logs for: $pattern"

    # Capture logs (adjust based on your logging system)
    # For Flutter: flutter logs | grep "$pattern"
    # For now, we'll simulate

    echo "  Expected log pattern: $pattern"
    echo "  Description: $description"
}

# ═══════════════════════════════════════════════════════════════
# TEST 1: LEVEL 1 - RAILWAY API SUCCESS
# ═══════════════════════════════════════════════════════════════
print_test_header "1" "Railway API Success (Level 1)"

echo "Prerequisites:"
echo "  ✓ Device has internet connection"
echo "  ✓ Railway backend is operational"
echo ""

echo "Steps:"
echo "  1. Clear app cache"
echo "  2. Open app and navigate to horoscope screen"
echo "  3. Select any zodiac sign (e.g., Aries)"
echo ""

check_log "Backend: Level 1 - Railway API success" "Railway API responded successfully"

echo ""
echo "Expected Results:"
echo "  ✓ Horoscope loads within 2-3 seconds"
echo "  ✓ Log shows: 'Backend: Level 1 - Railway API success for aries'"
echo "  ✓ Content is in correct language"
echo "  ✓ Ratings and lucky numbers are present"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Railway API works correctly"
else
    print_result 1 "Railway API failed or slow"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 2: LEVEL 2 - CACHE FUNCTIONALITY
# ═══════════════════════════════════════════════════════════════
print_test_header "2" "Cache Functionality (Level 2)"

echo "Prerequisites:"
echo "  ✓ Test 1 completed successfully (cache populated)"
echo ""

echo "Steps:"
echo "  1. Enable airplane mode"
echo "  2. Restart the app (clear memory cache)"
echo "  3. Navigate to horoscope screen"
echo "  4. Select the same zodiac sign from Test 1"
echo ""

check_log "Backend: Level 2 - Using valid cached horoscope" "Cache retrieved successfully"

echo ""
echo "Expected Results:"
echo "  ✓ Horoscope loads instantly (< 100ms)"
echo "  ✓ Log shows: 'Backend: Level 2 - Using valid cached horoscope for aries'"
echo "  ✓ Content is identical to Test 1"
echo "  ✓ No network requests made"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Cache system works correctly"
else
    print_result 1 "Cache retrieval failed"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 3: LEVEL 3 - OFFLINE GENERATION
# ═══════════════════════════════════════════════════════════════
print_test_header "3" "Offline Generation (Level 3)"

echo "Prerequisites:"
echo "  ✓ App data cleared (no cache exists)"
echo "  ✓ Airplane mode enabled"
echo ""

echo "Steps:"
echo "  1. Clear app data completely (uninstall/reinstall or clear data)"
echo "  2. Keep airplane mode enabled"
echo "  3. Open app and navigate to horoscope screen"
echo "  4. Select any zodiac sign"
echo ""

check_log "Backend: Using Level 3 - Local generation" "Local content generated"

echo ""
echo "Expected Results:"
echo "  ✓ Horoscope generates within 500ms"
echo "  ✓ Log shows: 'Backend: Using Level 3 - Local generation for aries'"
echo "  ✓ Content is generic but meaningful"
echo "  ✓ All fields populated (ratings, advice, lucky numbers)"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Local generation works correctly"
else
    print_result 1 "Local generation failed"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 4: CACHE EXPIRATION (TTL)
# ═══════════════════════════════════════════════════════════════
print_test_header "4" "Cache Expiration (24-hour TTL)"

echo "Prerequisites:"
echo "  ✓ Cache populated with 24+ hour old data"
echo "  ✓ Airplane mode enabled"
echo ""

echo "Steps:"
echo "  1. Complete Test 1 to populate cache"
echo "  2. Wait 24 hours OR manually adjust system time +24 hours"
echo "  3. Enable airplane mode"
echo "  4. Open app and load horoscope"
echo ""

check_log "Backend: Using Level 3 - Local generation" "Expired cache ignored"

echo ""
echo "Expected Results:"
echo "  ✓ Cache detected as expired"
echo "  ✓ Log shows: 'Backend: Using Level 3 - Local generation for aries'"
echo "  ✓ New content generated locally"
echo "  ✓ Expired cache not used"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Cache TTL validation works"
else
    print_result 1 "Expired cache was used incorrectly"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 5: COMPLETE FALLBACK CASCADE
# ═══════════════════════════════════════════════════════════════
print_test_header "5" "Complete Fallback Cascade (All 3 Levels)"

echo "This test verifies all three levels work in sequence"
echo ""

echo "Part A - Level 1 Success:"
echo "  1. Start with internet connected"
echo "  2. Clear app cache"
echo "  3. Load horoscope"
echo ""
echo "Did Level 1 work? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Level 1 (Railway) successful"
else
    print_result 1 "Level 1 (Railway) failed"
fi

echo ""
echo "Part B - Level 2 Cache:"
echo "  4. Enable airplane mode"
echo "  5. Close and reopen app"
echo "  6. Load same horoscope"
echo ""
echo "Did Level 2 work? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Level 2 (Cache) successful"
else
    print_result 1 "Level 2 (Cache) failed"
fi

echo ""
echo "Part C - Level 3 Local:"
echo "  7. Clear app data"
echo "  8. Keep airplane mode on"
echo "  9. Load horoscope"
echo ""
echo "Did Level 3 work? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Level 3 (Local) successful"
else
    print_result 1 "Level 3 (Local) failed"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 6: MULTI-LANGUAGE SUPPORT
# ═══════════════════════════════════════════════════════════════
print_test_header "6" "Multi-Language Support"

echo "Testing fallback in all 6 supported languages"
echo ""

languages=("English" "Spanish" "German" "French" "Italian" "Portuguese")
language_codes=("en" "es" "de" "fr" "it" "pt")

for i in "${!languages[@]}"; do
    echo "Testing ${languages[$i]} (${language_codes[$i]})..."
    echo "  1. Change device language to ${languages[$i]}"
    echo "  2. Enable airplane mode"
    echo "  3. Clear app data"
    echo "  4. Load horoscope"
    echo ""
    echo "Is content in ${languages[$i]}? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_result 0 "${languages[$i]} template works"
    else
        print_result 1 "${languages[$i]} template failed"
    fi
done

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 7: NETWORK FAILURE SIMULATION
# ═══════════════════════════════════════════════════════════════
print_test_header "7" "Network Failure Handling"

echo "Prerequisites:"
echo "  ✓ Configure firewall to block Railway API"
echo "  ✓ OR use Charles Proxy to simulate 503 error"
echo ""

echo "Steps:"
echo "  1. Block Railway API (keep internet 'connected')"
echo "  2. Clear app cache"
echo "  3. Load horoscope"
echo "  4. Observe timeout and fallback"
echo ""

check_log "Backend: Level 1 failed" "Railway API timeout detected"
check_log "Backend: Using Level 3" "Fell back to local generation"

echo ""
echo "Expected Results:"
echo "  ✓ Initial attempt times out after 10 seconds"
echo "  ✓ Log shows Level 1 failure"
echo "  ✓ Falls back to Level 3 (no cache)"
echo "  ✓ Content loads within 11 seconds total"
echo "  ✓ No crash or infinite loading"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Network failure handled gracefully"
else
    print_result 1 "Network failure caused issues"
fi

wait_for_user

# ═══════════════════════════════════════════════════════════════
# TEST 8: CONCURRENT REQUESTS
# ═══════════════════════════════════════════════════════════════
print_test_header "8" "Concurrent Request Handling"

echo "Prerequisites:"
echo "  ✓ App cache cleared"
echo "  ✓ Internet connected"
echo ""

echo "Steps:"
echo "  1. Open app"
echo "  2. Quickly navigate to 3 different zodiac signs"
echo "  3. Do this within 2-3 seconds (rapid switching)"
echo ""

check_log "Request en progreso" "Duplicate requests detected and handled"

echo ""
echo "Expected Results:"
echo "  ✓ All 3 requests complete successfully"
echo "  ✓ No duplicate API calls for same sign"
echo "  ✓ Cache populated efficiently"
echo "  ✓ No race conditions or crashes"
echo ""

echo "Did the test pass? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    print_result 0 "Concurrent requests handled correctly"
else
    print_result 1 "Concurrent requests caused issues"
fi

# ═══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  TEST SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))

echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo "Backend resilience system is fully operational."
    exit 0
else
    echo -e "${YELLOW}⚠️  SOME TESTS FAILED${NC}"
    echo "Review failed tests and investigate issues."
    exit 1
fi