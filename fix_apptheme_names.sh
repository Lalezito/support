#!/bin/bash

# Fix AppTheme property names in all goal planner screens

find zodiac_app/lib/features/premium/screens/goal_planner -name "*.dart" -exec sed -i '' \
  -e 's/AppTheme\.goldAccent/AppTheme.accentGold/g' \
  -e 's/AppTheme\.primaryColor/AppTheme.primaryBlue/g' \
  -e 's/AppTheme\.secondaryColor/AppTheme.cosmicDeep/g' \
  -e 's/AppTheme\.cardColor/AppTheme.primaryBlue/g' \
  {} \;

echo "✅ Fixed AppTheme property names in all goal planner screens"
