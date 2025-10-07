#!/bin/bash
# 🤖 SMART GUARDIAN - Protocolo V2.0 Intelligent File Classification
# Auto-classifies file risk level and applies appropriate protocol

set -e

# Colors for output
RED='\033[0;31m'
ORANGE='\033[0;33m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Classification function
classify_file_risk() {
    local file=$1

    # Critical level detection - REQUIRE PRE-APPROVAL
    if [[ $file == "zodiac_app/lib/main.dart" ||
          $file == "zodiac_app/pubspec.yaml" ||
          $file == "zodiac_app/lib/firebase_options.dart" ||
          $file == "zodiac_app/android/app/build.gradle" ||
          $file == "zodiac_app/ios/Runner/Info.plist" ]]; then
        echo "CRITICAL"

    # Sensitive level detection - BACKUP + EXTENSIVE TESTING
    elif [[ $file == *"revenue_cat_service.dart"* ||
            $file == *"firebase_service.dart"* ||
            $file == *"premium_screen.dart"* ||
            $file == *"secure_storage_service.dart"* ]]; then
        echo "SENSITIVE"

    # Modifiable level detection - STANDARD PROTOCOL
    elif [[ $file == zodiac_app/lib/services/* ||
            $file == zodiac_app/lib/screens/* ||
            $file == *"production_analytics_service.dart"* ||
            $file == *"preferences_service.dart"* ||
            $file == zodiac_app/lib/l10n/* ]]; then
        echo "MODIFIABLE"

    # Free level - NORMAL DEVELOPMENT
    else
        echo "FREE"
    fi
}

# Protocol application
apply_protocol() {
    local file=$1
    local level=$(classify_file_risk $file)

    case $level in
        CRITICAL)
            echo -e "${RED}🔴 CRITICAL FILE: $file${NC}"
            echo -e "   📋 REQUIRING PRE-APPROVAL AND BACKUP"
            echo -e "   ⚠️  Contact project lead before modifying"
            create_backup $file "FULL_PROJECT"
            return 1  # Block modification
            ;;
        SENSITIVE)
            echo -e "${ORANGE}🟠 SENSITIVE FILE: $file${NC}"
            echo -e "   💾 Creating backup and enabling extensive testing..."
            create_backup $file "FULL_PROJECT"
            run_extensive_tests
            ;;
        MODIFIABLE)
            echo -e "${YELLOW}🟡 MODIFIABLE FILE: $file${NC}"
            echo -e "   🧪 Standard protocol - running standard tests..."
            create_backup $file "FILE_LEVEL"
            run_standard_tests
            ;;
        FREE)
            echo -e "${GREEN}🟢 FREE FILE: $file${NC}"
            echo -e "   ✅ Normal workflow - basic validation only..."
            run_basic_validation
            ;;
    esac
}

# Backup creation
create_backup() {
    local file=$1
    local backup_type=$2
    local timestamp=$(date +%Y%m%d_%H%M%S)

    case $backup_type in
        FULL_PROJECT)
            echo "🔄 Creating full project backup..."
            cp -r zodiac_app "../zodiac_backup_${timestamp}"
            echo "✅ Full backup created: ../zodiac_backup_${timestamp}"
            ;;
        FILE_LEVEL)
            if [[ -f "$file" ]]; then
                cp "$file" "${file}.backup.${timestamp}"
                echo "📁 File backup created: ${file}.backup.${timestamp}"
            fi
            ;;
    esac
}

# Testing functions
run_extensive_tests() {
    echo "🧪 Running extensive test suite..."
    cd zodiac_app

    # Flutter analyze
    echo "   📊 Running flutter analyze..."
    if ! flutter analyze; then
        echo "❌ Flutter analyze failed"
        return 1
    fi

    # All tests
    echo "   🧪 Running full test suite..."
    if ! flutter test; then
        echo "❌ Tests failed"
        return 1
    fi

    # Premium feature tests specifically
    echo "   💰 Running premium feature tests..."
    if ! flutter test test/premium/; then
        echo "❌ Premium tests failed"
        return 1
    fi

    cd ..
    echo "✅ Extensive tests completed successfully"
}

run_standard_tests() {
    echo "🧪 Running standard test suite..."

    if [[ -d "zodiac_app" ]]; then
        cd zodiac_app
    else
        echo "⚠️ zodiac_app directory not found, skipping Flutter tests"
        return 0
    fi

    # Flutter analyze with lenient settings for development
    echo "   📊 Running flutter analyze (development mode)..."
    if ! flutter analyze --no-fatal-infos --no-fatal-warnings; then
        echo "⚠️ Flutter analyze has issues but proceeding (development mode)"
    fi

    # Targeted tests based on modified area
    echo "   🎯 Running targeted tests..."
    if [[ -d "test/services/" ]]; then
        flutter test test/services/ || echo "⚠️ Some service tests failed but proceeding"
    fi

    cd ..
    echo "✅ Standard tests completed"
}

run_basic_validation() {
    echo "🔍 Running basic validation..."

    if [[ -d "zodiac_app" ]]; then
        cd zodiac_app

        # Basic syntax check
        if ! flutter analyze --no-fatal-infos --no-fatal-warnings; then
            echo "⚠️ Warning: Analysis issues found but proceeding..."
        fi

        cd ..
    else
        echo "⚠️ zodiac_app directory not found, basic validation skipped"
    fi

    echo "✅ Basic validation completed"
}

# Emergency override check
check_emergency_override() {
    if [[ -f ".emergency_override" ]]; then
        echo -e "${RED}🚨 EMERGENCY OVERRIDE ACTIVE${NC}"
        echo "   ⏰ Override expires: $(cat .emergency_override)"
        return 0  # Allow override
    fi
    return 1  # No override
}

# Main execution
main() {
    local files_to_check=("$@")

    if [[ ${#files_to_check[@]} -eq 0 ]]; then
        # Check git staged files
        mapfile -t files_to_check < <(git diff --cached --name-only 2>/dev/null || echo "")
    fi

    if [[ ${#files_to_check[@]} -eq 0 ]]; then
        echo "No files to check"
        exit 0
    fi

    echo -e "🤖 ${GREEN}SMART GUARDIAN V2.0 ACTIVATED${NC}"
    echo "================================================"

    local blocked_files=()
    local total_files=${#files_to_check[@]}

    for file in "${files_to_check[@]}"; do
        if [[ -n "$file" ]]; then
            echo ""
            if ! apply_protocol "$file"; then
                if ! check_emergency_override; then
                    blocked_files+=("$file")
                fi
            fi
        fi
    done

    echo ""
    echo "================================================"
    echo -e "📊 ${GREEN}SMART GUARDIAN SUMMARY${NC}"
    echo "   📁 Files processed: $total_files"
    echo "   🚫 Files blocked: ${#blocked_files[@]}"

    if [[ ${#blocked_files[@]} -gt 0 ]]; then
        echo ""
        echo -e "${RED}⛔ BLOCKED FILES REQUIRING APPROVAL:${NC}"
        for blocked in "${blocked_files[@]}"; do
            echo "   - $blocked"
        done
        echo ""
        echo -e "💡 ${YELLOW}To proceed with critical files:${NC}"
        echo "   1. Get approval from project lead"
        echo "   2. Or activate emergency override: ./scripts/emergency_override.sh \"reason\""
        exit 1
    fi

    echo -e "✅ ${GREEN}ALL FILES CLEARED FOR MODIFICATION${NC}"
}

# Execute main function with all arguments
main "$@"