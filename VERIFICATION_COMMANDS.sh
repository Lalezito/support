#!/bin/bash

# Pre-Existing Errors Verification Script
# Run after implementing fixes to verify all errors are resolved

echo "🔍 Starting verification of pre-existing error fixes..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project path
PROJECT_PATH="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib"

# Function to count and display results
check_pattern() {
    local pattern=$1
    local description=$2
    local count=$(grep -r "$pattern" "$PROJECT_PATH" --include="*.dart" 2>/dev/null | wc -l | xargs)

    if [ "$count" -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC} - $description: 0 occurrences found"
    else
        echo -e "${RED}❌ FAIL${NC} - $description: $count occurrences still exist"
        echo "   Files:"
        grep -r "$pattern" "$PROJECT_PATH" --include="*.dart" -l 2>/dev/null | sed 's/^/   - /'
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Checking PremiumTier.universe references..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_pattern "PremiumTier\.universe" "PremiumTier.universe"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  Checking PremiumTier.lifetime references..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_pattern "PremiumTier\.lifetime" "PremiumTier.lifetime"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Checking SubscriptionType.lifetime references..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_pattern "SubscriptionType\.lifetime" "SubscriptionType.lifetime"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  Checking undefined variable _monthlyPremium..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if variable is defined
if grep -q "static const String _monthlyPremium" "$PROJECT_PATH/services/subscription_service.dart" 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - _monthlyPremium is now defined"
else
    echo -e "${RED}❌ FAIL${NC} - _monthlyPremium is NOT defined"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  Checking undefined variable _lifetimePremium..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if variable is defined
if grep -q "static const String _lifetimePremium" "$PROJECT_PATH/services/subscription_service.dart" 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - _lifetimePremium is now defined"
else
    echo -e "${RED}❌ FAIL${NC} - _lifetimePremium is NOT defined"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  Verifying Quick Wins isolation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check main.dart
MAIN_ERRORS=$(grep -i "universe\|lifetime" "$PROJECT_PATH/main.dart" 2>/dev/null | wc -l | xargs)
if [ "$MAIN_ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - main.dart has no universe/lifetime references"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - main.dart has $MAIN_ERRORS references (may be comments)"
fi

# Check purchase_state_notifier.dart
NOTIFIER_ERRORS=$(grep -i "universe\|lifetime" "$PROJECT_PATH/features/premium/controllers/purchase_state_notifier.dart" 2>/dev/null | wc -l | xargs)
if [ "$NOTIFIER_ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - purchase_state_notifier.dart has no universe/lifetime references"
else
    echo -e "${RED}❌ FAIL${NC} - purchase_state_notifier.dart has $NOTIFIER_ERRORS references"
fi

# Check premium_screen.dart (allowing comments)
SCREEN_CODE_ERRORS=$(grep -i "PremiumTier\\.universe\|PremiumTier\\.lifetime" "$PROJECT_PATH/screens/premium_screen.dart" 2>/dev/null | wc -l | xargs)
if [ "$SCREEN_CODE_ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - premium_screen.dart has no code references to universe/lifetime"
else
    echo -e "${RED}❌ FAIL${NC} - premium_screen.dart has $SCREEN_CODE_ERRORS code references"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  Checking for deprecated legacy files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if premium_screen_legacy.dart is deprecated
if grep -q "@Deprecated" "$PROJECT_PATH/screens/legacy/premium_screen_legacy.dart" 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - premium_screen_legacy.dart is marked as deprecated"
elif [ ! -f "$PROJECT_PATH/screens/legacy/premium_screen_legacy.dart" ]; then
    echo -e "${GREEN}✅ PASS${NC} - premium_screen_legacy.dart has been removed"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - premium_screen_legacy.dart exists but not deprecated"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count total errors remaining
TOTAL_UNIVERSE=$(grep -r "PremiumTier\.universe" "$PROJECT_PATH" --include="*.dart" 2>/dev/null | wc -l | xargs)
TOTAL_LIFETIME_TIER=$(grep -r "PremiumTier\.lifetime" "$PROJECT_PATH" --include="*.dart" 2>/dev/null | wc -l | xargs)
TOTAL_LIFETIME_SUB=$(grep -r "SubscriptionType\.lifetime" "$PROJECT_PATH" --include="*.dart" 2>/dev/null | wc -l | xargs)
TOTAL_ERRORS=$((TOTAL_UNIVERSE + TOTAL_LIFETIME_TIER + TOTAL_LIFETIME_SUB))

echo "PremiumTier.universe: $TOTAL_UNIVERSE occurrences"
echo "PremiumTier.lifetime: $TOTAL_LIFETIME_TIER occurrences"
echo "SubscriptionType.lifetime: $TOTAL_LIFETIME_SUB occurrences"
echo "─────────────────────────────────────────────────────"
echo "TOTAL ERRORS REMAINING: $TOTAL_ERRORS"
echo ""

if [ "$TOTAL_ERRORS" -eq 0 ]; then
    echo -e "${GREEN}🎉 SUCCESS! All pre-existing errors have been fixed!${NC}"
else
    echo -e "${RED}⚠️  WARNING: $TOTAL_ERRORS errors still need to be fixed${NC}"
    echo ""
    echo "Run this command to see which files still have errors:"
    echo "grep -r 'PremiumTier\\.universe\\|PremiumTier\\.lifetime\\|SubscriptionType\\.lifetime' $PROJECT_PATH --include='*.dart' -n"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Review any remaining errors above"
echo "2. Apply fixes from QUICK_FIX_TEMPLATES.md"
echo "3. Re-run this script to verify"
echo "4. Run 'flutter analyze' to check for compile errors"
echo "5. Run 'flutter test' to verify functionality"
echo ""
