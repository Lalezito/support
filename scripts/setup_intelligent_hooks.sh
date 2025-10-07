#!/bin/bash
# 🪝 INTELLIGENT GIT HOOKS SETUP - Protocolo V2.0
# Configures smart git hooks for automated compliance and safety

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_ROOT="/Users/alejandrocaceres/Desktop/appstore - zodia"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

setup_pre_commit_hook() {
    echo -e "${BLUE}🪝 Setting up intelligent pre-commit hook...${NC}"

    cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# 🤖 INTELLIGENT PRE-COMMIT HOOK - Protocolo V2.0
# Automatically applies Smart Guardian checks before commits

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🤖 Smart Guardian V2.0 - Pre-commit Analysis${NC}"
echo "=================================================="

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

if [[ -z "$STAGED_FILES" ]]; then
    echo "No files staged for commit"
    exit 0
fi

# Run Smart Guardian on staged files
if ! ./scripts/smart_guardian.sh $STAGED_FILES; then
    echo ""
    echo -e "${RED}❌ Smart Guardian blocked commit${NC}"
    echo -e "   Some files require approval or have failed safety checks"
    echo -e "   Use emergency override if this is a production emergency:"
    echo -e "   ${YELLOW}./scripts/emergency_override.sh \"reason\"${NC}"
    exit 1
fi

# Run intelligent testing on staged files
echo ""
echo -e "${BLUE}🧪 Running intelligent tests for staged files...${NC}"
if ! ./scripts/intelligent_test_suite.sh targeted; then
    echo ""
    echo -e "${RED}❌ Tests failed for staged changes${NC}"
    echo -e "   Please fix failing tests before committing"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All pre-commit checks passed - commit allowed${NC}"
echo "=================================================="
EOF

    chmod +x "$HOOKS_DIR/pre-commit"
    echo -e "✅ Pre-commit hook installed"
}

setup_pre_push_hook() {
    echo -e "${BLUE}🪝 Setting up intelligent pre-push hook...${NC}"

    cat > "$HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# 🚀 INTELLIGENT PRE-PUSH HOOK - Protocolo V2.0
# Comprehensive validation before pushing to remote

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Smart Guardian V2.0 - Pre-push Validation${NC}"
echo "======================================================"

# Check if we're pushing to main branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" == "main" ]]; then
    echo -e "${YELLOW}⚠️  Pushing to main branch - Extra validation required${NC}"

    # Run comprehensive tests
    echo -e "${BLUE}🧪 Running comprehensive test suite...${NC}"
    if ! ./scripts/intelligent_test_suite.sh all; then
        echo -e "${RED}❌ Comprehensive tests failed${NC}"
        echo -e "   Cannot push to main with failing tests"
        exit 1
    fi

    # Check for emergency overrides (shouldn't push with active override)
    if [[ -f ".emergency_override" ]]; then
        echo -e "${RED}❌ Cannot push to main with active emergency override${NC}"
        echo -e "   Deactivate emergency override first: ./scripts/emergency_override.sh deactivate"
        exit 1
    fi
fi

# Verify critical services still work
echo -e "${BLUE}🔍 Verifying critical services...${NC}"
cd zodiac_app

# Quick smoke test - verify app compiles
if ! flutter build apk --debug --tree-shake-icons >/dev/null 2>&1; then
    echo -e "${RED}❌ App fails to compile${NC}"
    exit 1
fi

cd ..

echo -e "${GREEN}✅ All pre-push validation passed${NC}"
echo "======================================================"
EOF

    chmod +x "$HOOKS_DIR/pre-push"
    echo -e "✅ Pre-push hook installed"
}

setup_post_commit_hook() {
    echo -e "${BLUE}🪝 Setting up intelligent post-commit hook...${NC}"

    cat > "$HOOKS_DIR/post-commit" << 'EOF'
#!/bin/bash
# 📊 INTELLIGENT POST-COMMIT HOOK - Protocolo V2.0
# Analytics and monitoring after successful commits

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get commit info
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=format:"%s")
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

echo -e "${BLUE}📊 Post-commit Analysis${NC}"
echo "========================"
echo -e "🔍 Commit: ${GREEN}${COMMIT_HASH:0:8}${NC}"
echo -e "📝 Message: $COMMIT_MSG"

# Count file types changed
SERVICE_FILES=$(echo "$CHANGED_FILES" | grep -c "service\.dart" || echo "0")
SCREEN_FILES=$(echo "$CHANGED_FILES" | grep -c "screen\.dart" || echo "0")
WIDGET_FILES=$(echo "$CHANGED_FILES" | grep -c "widget\.dart" || echo "0")

echo -e "📁 Files changed:"
echo -e "   🔧 Services: $SERVICE_FILES"
echo -e "   🖼️  Screens: $SCREEN_FILES"
echo -e "   🧩 Widgets: $WIDGET_FILES"

# Log for analytics
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] COMMIT: $COMMIT_HASH | FILES: $(echo "$CHANGED_FILES" | wc -l) | SERVICES: $SERVICE_FILES | SCREENS: $SCREEN_FILES" >> .commit_analytics

echo -e "${GREEN}✅ Post-commit analysis complete${NC}"
EOF

    chmod +x "$HOOKS_DIR/post-commit"
    echo -e "✅ Post-commit hook installed"
}

setup_commit_msg_hook() {
    echo -e "${BLUE}🪝 Setting up intelligent commit message hook...${NC}"

    cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/bin/bash
# 📝 INTELLIGENT COMMIT MESSAGE HOOK - Protocolo V2.0
# Ensures commit messages follow conventions and include context

set -e

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat $COMMIT_MSG_FILE)

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Skip if this is a merge commit
if echo "$COMMIT_MSG" | grep -q "^Merge"; then
    exit 0
fi

# Check for emergency context
if [[ -f ".emergency_override" ]]; then
    # Add emergency context to commit message if not present
    if ! echo "$COMMIT_MSG" | grep -q "🚨"; then
        echo -e "\n\n🚨 EMERGENCY COMMIT - Override active" >> $COMMIT_MSG_FILE
        echo -e "Emergency reason: $(cat .emergency_override 2>/dev/null || echo 'Unknown')" >> $COMMIT_MSG_FILE
        echo -e "${YELLOW}⚠️  Added emergency context to commit message${NC}"
    fi
fi

# Check commit message length and format
MSG_LENGTH=$(echo "$COMMIT_MSG" | head -1 | wc -c)

if [[ $MSG_LENGTH -lt 10 ]]; then
    echo -e "${RED}❌ Commit message too short (minimum 10 characters)${NC}"
    echo -e "Current: '$COMMIT_MSG'"
    exit 1
fi

if [[ $MSG_LENGTH -gt 72 ]]; then
    echo -e "${YELLOW}⚠️  Commit message first line is long (>72 characters)${NC}"
    echo -e "Consider breaking into title + description"
fi

# Suggest conventional commit format if not following pattern
CONVENTIONAL_PATTERNS="^(feat|fix|docs|style|refactor|perf|test|chore|build|ci)(\(.+\))?: .+"

if ! echo "$COMMIT_MSG" | grep -qE "$CONVENTIONAL_PATTERNS"; then
    echo -e "${YELLOW}💡 Suggestion: Use conventional commit format${NC}"
    echo -e "   feat: add new feature"
    echo -e "   fix: fix bug"
    echo -e "   refactor: refactor code"
    echo -e "   etc."
fi

echo -e "${GREEN}✅ Commit message validation passed${NC}"
EOF

    chmod +x "$HOOKS_DIR/commit-msg"
    echo -e "✅ Commit message hook installed"
}

main() {
    echo -e "${GREEN}🚀 INTELLIGENT GIT HOOKS SETUP V2.0${NC}"
    echo "=================================================="

    # Check if we're in a git repository
    if [[ ! -d "$REPO_ROOT/.git" ]]; then
        echo -e "${RED}❌ Not in a git repository${NC}"
        exit 1
    fi

    # Create hooks directory if it doesn't exist
    mkdir -p "$HOOKS_DIR"

    # Setup all hooks
    setup_pre_commit_hook
    setup_pre_push_hook
    setup_post_commit_hook
    setup_commit_msg_hook

    echo ""
    echo -e "${GREEN}🎉 INTELLIGENT GIT HOOKS INSTALLATION COMPLETE${NC}"
    echo "=============================================="
    echo -e "✅ Pre-commit: Smart Guardian + Intelligent Testing"
    echo -e "✅ Pre-push: Comprehensive validation for main branch"
    echo -e "✅ Post-commit: Analytics and monitoring"
    echo -e "✅ Commit-msg: Message validation and emergency context"
    echo ""
    echo -e "${BLUE}📋 HOOKS SUMMARY:${NC}"
    echo -e "   🤖 Smart Guardian runs on every commit"
    echo -e "   🧪 Intelligent testing based on modified files"
    echo -e "   🚨 Emergency override system integrated"
    echo -e "   📊 Commit analytics for project insights"
    echo -e "   📝 Commit message conventions enforced"
    echo ""
    echo -e "${YELLOW}💡 Next steps:${NC}"
    echo -e "   1. Test the hooks with a small commit"
    echo -e "   2. Configure team members with same hooks"
    echo -e "   3. Review .commit_analytics for insights"
}

main "$@"