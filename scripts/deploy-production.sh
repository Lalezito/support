#!/bin/bash

# Production deployment script
set -e

echo "🚀 Starting production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're on main branch
if [[ $(git branch --show-current) != "main" ]]; then
    print_error "Must be on main branch to deploy"
    exit 1
fi

# Run tests
print_status "Running tests..."
cd zodiac_app
flutter test
print_status "Tests passed"

# Build Android
print_status "Building Android APK..."
flutter build apk --release --split-per-abi
print_status "Android build complete"

# Build iOS
print_status "Building iOS..."
flutter build ios --release --no-codesign
print_status "iOS build complete"

# Deploy backend (if using Railway)
print_status "Deploying backend..."
# Add your backend deployment command here
# railway deploy or similar

# Create git tag
TAG="v$(date +%Y%m%d_%H%M%S)"
git tag $TAG
git push origin $TAG

print_status "Deployment complete!"
print_status "Tag created: $TAG"
print_warning "Remember to:"
echo "  - Upload builds to stores"
echo "  - Update release notes"
echo "  - Monitor crash reports"