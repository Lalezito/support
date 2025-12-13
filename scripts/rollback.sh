#!/bin/bash

# Rollback script for emergency situations

echo "🔄 Starting rollback..."

# Get previous version tag
PREVIOUS_TAG=$(git describe --abbrev=0 --tags 2>/dev/null)

if [[ -z "$PREVIOUS_TAG" ]]; then
    echo "❌ No previous tag found"
    exit 1
fi

echo "Rolling back to: $PREVIOUS_TAG"

# Checkout previous version
git checkout $PREVIOUS_TAG

# Trigger deployment of previous version
# Add your deployment commands here

echo "✅ Rollback complete"