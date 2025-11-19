#!/bin/bash

# SPACING CONSOLIDATION VERIFICATION SCRIPT
# Verifies that spacing system consolidation is successful
# Run this after the consolidation to ensure everything is correct

echo "🔍 SPACING SYSTEM CONSOLIDATION VERIFICATION"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to project root
cd "$(dirname "$0")/.." || exit 1

# Counter for issues
ISSUES=0

echo "📋 Test 1: Check for AppSpacing usage in application code"
echo "-----------------------------------------------------------"
APP_SPACING_USAGE=$(grep -r "AppSpacing\." zodiac_app/lib --exclude-dir=design_system --include="*.dart" 2>/dev/null | wc -l)
if [ "$APP_SPACING_USAGE" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - No AppSpacing usage found in application code"
else
    echo -e "${RED}❌ FAIL${NC} - Found $APP_SPACING_USAGE occurrences of AppSpacing in application code"
    echo "Files with AppSpacing usage:"
    grep -r "AppSpacing\." zodiac_app/lib --exclude-dir=design_system --include="*.dart" -l
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "📋 Test 2: Check ZodiacSpacing is imported in design system"
echo "-----------------------------------------------------------"
ZODIAC_SPACING_IMPORTS=$(grep -r "import.*zodiac_spacing" zodiac_app/lib/design_system --include="*.dart" 2>/dev/null | wc -l)
if [ "$ZODIAC_SPACING_IMPORTS" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Found $ZODIAC_SPACING_IMPORTS imports of zodiac_spacing in design system"
else
    echo -e "${RED}❌ FAIL${NC} - No zodiac_spacing imports found in design system"
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "📋 Test 3: Verify deprecation notices in app_spacing.dart"
echo "-----------------------------------------------------------"
if grep -q "@Deprecated" zodiac_app/lib/design_system/app_spacing.dart 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - Deprecation notices found in app_spacing.dart"
else
    echo -e "${RED}❌ FAIL${NC} - No deprecation notices in app_spacing.dart"
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "📋 Test 4: Check documentation references ZodiacSpacing"
echo "-----------------------------------------------------------"
DOC_ZODIAC_REFS=$(grep -c "ZodiacSpacing" zodiac_app/lib/design_system/design_system_documentation.md 2>/dev/null)
DOC_APP_REFS=$(grep -c "AppSpacing\." zodiac_app/lib/design_system/design_system_documentation.md 2>/dev/null)

if [ "$DOC_ZODIAC_REFS" -gt "$DOC_APP_REFS" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Documentation uses ZodiacSpacing ($DOC_ZODIAC_REFS refs) over AppSpacing ($DOC_APP_REFS refs)"
else
    echo -e "${YELLOW}⚠️  WARN${NC} - Documentation has more AppSpacing ($DOC_APP_REFS) than ZodiacSpacing ($DOC_ZODIAC_REFS) references"
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "📋 Test 5: Check for hardcoded spacing values (informational)"
echo "-----------------------------------------------------------"
HARDCODED_SPACING=$(grep -r "EdgeInsets\.all(16\.0)\|EdgeInsets\.all(24\.0)\|EdgeInsets\.all(8\.0)" zodiac_app/lib/screens --include="*.dart" 2>/dev/null | wc -l)
if [ "$HARDCODED_SPACING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  INFO${NC} - Found $HARDCODED_SPACING hardcoded spacing values in screens"
    echo "This is a separate issue - consider migrating to design tokens"
    echo ""
    echo "Example files with hardcoded spacing:"
    grep -r "EdgeInsets\.all(16\.0)" zodiac_app/lib/screens --include="*.dart" -l 2>/dev/null | head -5
else
    echo -e "${GREEN}✅ EXCELLENT${NC} - No hardcoded spacing values found!"
fi
echo ""

echo "📋 Test 6: Verify both spacing files exist"
echo "-----------------------------------------------------------"
if [ -f "zodiac_app/lib/design_system/app_spacing.dart" ] && [ -f "zodiac_app/lib/design_system/zodiac_spacing.dart" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Both spacing files exist (app_spacing.dart is deprecated)"
else
    echo -e "${RED}❌ FAIL${NC} - One or both spacing files are missing"
    ISSUES=$((ISSUES + 1))
fi
echo ""

echo "📋 Test 7: Check ZodiacDesignSystem uses ZodiacSpacing"
echo "-----------------------------------------------------------"
if grep -q "ZodiacSpacing spacing" zodiac_app/lib/design_system/zodiac_design_system.dart 2>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - ZodiacDesignSystem correctly uses ZodiacSpacing"
else
    echo -e "${RED}❌ FAIL${NC} - ZodiacDesignSystem does not reference ZodiacSpacing"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Summary
echo "=============================================="
echo "📊 VERIFICATION SUMMARY"
echo "=============================================="

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo ""
    echo "Spacing consolidation is successful!"
    echo "app_spacing.dart is properly deprecated and can be safely removed in v4.0.0"
    exit 0
else
    echo -e "${RED}❌ $ISSUES TEST(S) FAILED${NC}"
    echo ""
    echo "Please review the failed tests above and fix the issues."
    exit 1
fi
