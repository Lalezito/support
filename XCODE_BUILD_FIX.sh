#!/bin/bash
# 🔧 XCODE BUILD FIX SCRIPT
# Soluciona error PhaseScriptExecution en Xcode
# Fecha: October 10, 2025

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔧 XCODE BUILD ERROR FIX - Zodiac App${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Store original directory
ORIGINAL_DIR=$(pwd)
PROJECT_DIR="/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Error: Project directory not found${NC}"
    echo "   Expected: $PROJECT_DIR"
    exit 1
fi

echo -e "${YELLOW}⚠️  WARNING: Project path contains spaces!${NC}"
echo "   Current: /Users/.../Desktop/appstore - zodia/zodiac_app"
echo "   Recommended: Rename to 'appstore-zodia' (no spaces)"
echo ""
read -p "Continue anyway? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}ℹ️  To rename:${NC}"
    echo "   cd /Users/alejandrocaceres/Desktop"
    echo "   mv 'appstore - zodia' 'appstore-zodia'"
    exit 0
fi

echo ""
echo -e "${GREEN}🧹 Step 1/5: Cleaning Flutter build cache...${NC}"
cd "$PROJECT_DIR"
flutter clean
rm -rf build/
echo -e "${GREEN}   ✓ Flutter cache cleared${NC}"

echo ""
echo -e "${GREEN}📦 Step 2/5: Getting Flutter dependencies...${NC}"
flutter pub get
echo -e "${GREEN}   ✓ Dependencies updated${NC}"

echo ""
echo -e "${GREEN}🍎 Step 3/5: Cleaning CocoaPods...${NC}"
cd "$PROJECT_DIR/ios"

# Deintegrate pods
if command -v pod &> /dev/null; then
    pod deintegrate 2>/dev/null || echo "   (pod deintegrate not needed)"
else
    echo -e "${YELLOW}   ⚠️  CocoaPods not found. Installing...${NC}"
    sudo gem install cocoapods
fi

# Remove old pods
rm -rf Pods Podfile.lock .symlinks
echo -e "${GREEN}   ✓ Old pods removed${NC}"

echo ""
echo -e "${GREEN}📦 Step 4/5: Installing CocoaPods dependencies...${NC}"
pod install
echo -e "${GREEN}   ✓ Pods installed${NC}"

echo ""
echo -e "${GREEN}🔍 Step 5/5: Verifying installation...${NC}"

# Check if Pods directory exists
if [ -d "Pods" ]; then
    echo -e "${GREEN}   ✓ Pods directory created${NC}"
else
    echo -e "${RED}   ❌ Pods directory not found${NC}"
    exit 1
fi

# Check if Podfile.lock exists
if [ -f "Podfile.lock" ]; then
    echo -e "${GREEN}   ✓ Podfile.lock created${NC}"
else
    echo -e "${RED}   ❌ Podfile.lock not found${NC}"
    exit 1
fi

# Check Flutter symlinks
if [ -d ".symlinks" ]; then
    echo -e "${GREEN}   ✓ Flutter symlinks created${NC}"
else
    echo -e "${YELLOW}   ⚠️  Flutter symlinks not found (may regenerate on build)${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ CLEANUP COMPLETED SUCCESSFULLY${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "   1. Open Xcode:"
echo "      open /Users/alejandrocaceres/Desktop/appstore\\ -\\ zodia/zodiac_app/ios/Runner.xcworkspace"
echo ""
echo "   2. In Xcode:"
echo "      • Product → Clean Build Folder (⇧⌘K)"
echo "      • Product → Scheme → Edit Scheme"
echo "        → Set Run configuration to 'Debug'"
echo "      • Product → Build (⌘B)"
echo ""
echo "   3. Verify signing:"
echo "      • Target Runner → Signing & Capabilities"
echo "      • Enable 'Automatically manage signing'"
echo "      • Select your development team"
echo ""
echo -e "${RED}⚠️  IMPORTANT RECOMMENDATION:${NC}"
echo "   Rename project directory to remove spaces:"
echo "   cd /Users/alejandrocaceres/Desktop"
echo "   mv 'appstore - zodia' 'appstore-zodia'"
echo ""
echo -e "${GREEN}🎯 This will prevent future build issues with shell scripts.${NC}"
echo ""

# Return to original directory
cd "$ORIGINAL_DIR"
