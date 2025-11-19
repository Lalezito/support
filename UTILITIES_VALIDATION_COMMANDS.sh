#!/bin/bash

# Common Utilities - Validation Commands
# Run these commands to validate the impact of consolidation

echo "=========================================="
echo "Common Utilities Hunter - Validation"
echo "=========================================="
echo ""

cd "$(dirname "$0")/zodiac_app"

# ========================================
# 1. COUNT CURRENT DUPLICATIONS
# ========================================

echo "1. COUNTING CURRENT DUPLICATIONS"
echo "=================================="
echo ""

echo "Backend URLs hardcoded:"
grep -r "zodiac-backend-api-production-8ded.up.railway.app" lib --include="*.dart" | wc -l

echo "Email validation implementations:"
grep -rn "isValidEmail" lib/services --include="*.dart" | wc -l

echo "Zodiac sign validation lists:"
grep -rn "const validSigns\|final validSigns" lib --include="*.dart" | wc -l

echo "Unsafe int.parse() calls (no try-catch in same line):"
grep -rn "int\.parse(" lib/services --include="*.dart" | wc -l

echo "Unsafe double.parse() calls:"
grep -rn "double\.parse(" lib/services --include="*.dart" | wc -l

echo "DateTime.parse() calls (many unsafe):"
grep -rn "DateTime\.parse(" lib/services --include="*.dart" | wc -l

echo "Null/empty checks (could be simplified):"
grep -rn "== null || .*\.isEmpty" lib/services --include="*.dart" | wc -l

echo "Duration magic numbers:"
grep -rn "Duration(seconds:\|Duration(minutes:\|Duration(hours:" lib/services --include="*.dart" | wc -l

echo "Max retry constants:"
grep -rn "maxRetries\|_maxRetries" lib/services --include="*.dart" | wc -l

echo ""
echo "=========================================="
echo "2. CODE SIZE ANALYSIS"
echo "=========================================="
echo ""

echo "Total services files:"
find lib/services -name "*.dart" -type f | wc -l

echo "Total lines in services:"
find lib/services -name "*.dart" -type f -exec wc -l {} + | tail -1

echo "Current utils files:"
ls -la lib/utils/ | wc -l

echo "Current utils total lines:"
find lib/utils -name "*.dart" -type f -exec wc -l {} + | tail -1 || echo "0 (if no utils yet)"

echo ""
echo "=========================================="
echo "3. FIND MOST CRITICAL FILES"
echo "=========================================="
echo ""

echo "Services with unsafe parsing (top 10):"
grep -rn "int\.parse(" lib/services --include="*.dart" | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo ""
echo "Services with hardcoded URLs (all):"
grep -rn "https://zodiac-backend-api" lib --include="*.dart" | cut -d: -f1 | sort | uniq

echo ""
echo "=========================================="
echo "4. DETECT POTENTIAL CRASHES"
echo "=========================================="
echo ""

echo "Files with int.parse() without try-catch (RISKY):"
echo "(These are candidates for immediate fix)"
grep -rn "int\.parse(" lib/services --include="*.dart" -A 2 -B 2 | grep -v "try\|catch" | grep "int\.parse" | cut -d: -f1-2

echo ""
echo "Files with split(':')[0] pattern (VERY RISKY):"
grep -rn "split(':')\\[0\\]\|split(':')\\[1\\]" lib/services --include="*.dart"

echo ""
echo "=========================================="
echo "5. VALIDATION SUMMARY"
echo "=========================================="
echo ""

echo "Total potential issues found:"
echo "- Backend URL duplications: $(grep -r 'zodiac-backend-api-production-8ded.up.railway.app' lib --include="*.dart" | wc -l | tr -d ' ')"
echo "- Unsafe parsing: $(grep -rn 'int\.parse(\|double\.parse(' lib/services --include="*.dart" | wc -l | tr -d ' ')"
echo "- Zodiac validations: $(grep -rn 'validSigns' lib --include="*.dart" | wc -l | tr -d ' ')"
echo "- DateTime parsing: $(grep -rn 'DateTime\.parse(' lib/services --include="*.dart" | wc -l | tr -d ' ')"
echo "- Magic durations: $(grep -rn 'Duration(seconds:\|Duration(minutes:\|Duration(hours:' lib/services --include="*.dart" | wc -l | tr -d ' ')"

echo ""
echo "=========================================="
echo "6. GENERATE FILE LIST FOR MIGRATION"
echo "=========================================="
echo ""

echo "Creating migration file list..."

echo "# Files requiring urgent attention (Phase 1)" > ../MIGRATION_FILE_LIST.txt
echo "" >> ../MIGRATION_FILE_LIST.txt

echo "## Unsafe parsing (can crash app):" >> ../MIGRATION_FILE_LIST.txt
grep -rn "int\.parse(" lib/services --include="*.dart" | cut -d: -f1 | sort | uniq >> ../MIGRATION_FILE_LIST.txt

echo "" >> ../MIGRATION_FILE_LIST.txt
echo "## Hardcoded backend URLs:" >> ../MIGRATION_FILE_LIST.txt
grep -rn "zodiac-backend-api" lib --include="*.dart" | cut -d: -f1 | sort | uniq >> ../MIGRATION_FILE_LIST.txt

echo "" >> ../MIGRATION_FILE_LIST.txt
echo "## Duplicated validations:" >> ../MIGRATION_FILE_LIST.txt
grep -rn "isValidEmail\|validSigns" lib --include="*.dart" | cut -d: -f1 | sort | uniq >> ../MIGRATION_FILE_LIST.txt

echo "File list saved to: ../MIGRATION_FILE_LIST.txt"

echo ""
echo "=========================================="
echo "7. ESTIMATE CODE REDUCTION"
echo "=========================================="
echo ""

# Count lines that will be removed
BACKEND_URLS=$(grep -r "zodiac-backend-api-production-8ded.up.railway.app" lib --include="*.dart" | wc -l | tr -d ' ')
VALIDATIONS=$(grep -rn "const validSigns\|final validSigns" lib --include="*.dart" -A 12 | wc -l | tr -d ' ')
FORMATTERS=$(grep -rn "_format\|_capitalize" lib/services --include="*.dart" -A 3 | wc -l | tr -d ' ')

TOTAL_LINES_TO_REMOVE=$((BACKEND_URLS * 2 + VALIDATIONS + FORMATTERS))

echo "Estimated lines to be removed:"
echo "- Backend URLs: ~$((BACKEND_URLS * 2)) lines"
echo "- Validations: ~$VALIDATIONS lines"
echo "- Formatters: ~$FORMATTERS lines"
echo "- TOTAL: ~$TOTAL_LINES_TO_REMOVE lines"

echo ""
echo "New utility files to add: ~950 lines (tested + documented)"
echo "Net reduction: ~$((TOTAL_LINES_TO_REMOVE - 950)) lines"

echo ""
echo "=========================================="
echo "VALIDATION COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review COMMON_UTILITIES_REPORT.md"
echo "2. Review UTILITIES_EXECUTIVE_SUMMARY.md"
echo "3. Approve Phase 1 implementation (2 hours)"
echo "4. Start with files in MIGRATION_FILE_LIST.txt"
echo ""
echo "Questions? Check UTILITIES_IMPLEMENTATION_CODE.md for ready-to-use code"
echo ""
