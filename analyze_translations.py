#!/usr/bin/env python3
"""
Translation Keys Analysis Script
Analyzes app_localizations_en.dart to categorize and identify issues
"""

import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Read the file content
file_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/l10n/app_localizations_en.dart"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all translation keys and their values
pattern = r'String get (\w+) => [\'"]([^\'"]+)[\'"];'
simple_keys = re.findall(pattern, content)

# Extract method-based translations (with parameters)
method_pattern = r'String (\w+)\([^)]+\) \{'
method_keys = re.findall(method_pattern, content)

# Combine all keys
all_keys = set([key for key, _ in simple_keys] + method_keys)

print(f"TOTAL TRANSLATION KEYS: {len(all_keys)}")
print("=" * 80)

# Category definitions
categories = {
    'UI_NAVIGATION': ['back', 'next', 'skip', 'close', 'cancel', 'save', 'done', 'continue',
                      'start', 'finish', 'exit', 'open', 'select', 'confirm', 'apply'],
    'HOROSCOPE': ['horoscope', 'daily', 'weekly', 'monthly', 'yearly', 'prediction',
                  'today', 'week', 'month', 'year'],
    'ZODIAC_SIGNS': ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                     'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'],
    'COMPATIBILITY': ['compatibility', 'compatible', 'relationship', 'love', 'friendship',
                      'business', 'strengths', 'challenges', 'advice'],
    'PREMIUM': ['premium', 'subscription', 'upgrade', 'unlock', 'lifetime', 'monthly',
                'purchase', 'restore', 'subscribe'],
    'ONBOARDING': ['onboarding', 'welcome', 'intro', 'tutorial', 'getting'],
    'COSMIC_LIFE_COACH': ['cosmic', 'coach', 'checkin', 'advice', 'guidance', 'insight',
                          'ai', 'pattern', 'progress', 'streak'],
    'BIRTH_DATA': ['birth', 'ascendant', 'calculate', 'time', 'location', 'birthdate'],
    'SETTINGS': ['settings', 'language', 'theme', 'dark', 'light', 'notification',
                 'preference', 'privacy', 'data'],
    'ACCOUNT': ['account', 'signin', 'signout', 'signup', 'email', 'password',
                'profile', 'user', 'sync'],
    'ELEMENTS': ['fire', 'earth', 'air', 'water', 'element', 'cardinal', 'fixed', 'mutable'],
    'PLANETS': ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
                'uranus', 'neptune', 'pluto'],
    'MOON_PHASES': ['newmoon', 'fullmoon', 'waxing', 'waning', 'crescent', 'gibbous', 'quarter'],
    'EMOTIONS': ['mood', 'energy', 'focus', 'feeling', 'emotion', 'state'],
    'PREDICTIONS': ['prediction', 'verify', 'active', 'pending', 'history'],
    'ERRORS': ['error', 'failed', 'invalid', 'warning', 'alert'],
    'SUCCESS': ['success', 'complete', 'saved', 'activated', 'restored'],
    'ACTIONS': ['add', 'edit', 'delete', 'remove', 'update', 'refresh', 'reload',
                'export', 'import', 'share', 'download'],
    'STATUS': ['loading', 'processing', 'generating', 'pending', 'active', 'ready',
               'enabled', 'disabled'],
    'QUALITY': ['excellent', 'good', 'fair', 'low', 'moderate', 'high', 'best'],
    'TIME': ['morning', 'afternoon', 'evening', 'night', 'today', 'week', 'month', 'year'],
    'DATES': ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december'],
    'WEEKDAYS': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
    'FEATURES': ['feature'],
    'GDPR': ['gdpr', 'consent', 'privacy', 'rights', 'data'],
    'WELLNESS': ['fitness', 'mindfulness', 'wellness', 'healing', 'growth', 'adventure'],
    'GOALS': ['goal', 'statistics', 'streak', 'completed'],
}

# Categorize keys
categorized_keys: Dict[str, List[str]] = defaultdict(list)
uncategorized_keys: Set[str] = set(all_keys)

for key in all_keys:
    key_lower = key.lower()
    found_category = False

    for category, keywords in categories.items():
        if any(keyword in key_lower for keyword in keywords):
            categorized_keys[category].append(key)
            uncategorized_keys.discard(key)
            found_category = True
            break

    if not found_category:
        categorized_keys['UNCATEGORIZED'].append(key)

# Print categorized results
print("\n📊 CATEGORIZATION BY DOMAIN")
print("=" * 80)
for category in sorted(categorized_keys.keys()):
    keys = sorted(categorized_keys[category])
    print(f"\n{category}: {len(keys)} keys")
    if len(keys) <= 20:
        for key in keys:
            print(f"  - {key}")
    else:
        print(f"  (showing first 20 of {len(keys)})")
        for key in keys[:20]:
            print(f"  - {key}")

# Analyze naming patterns
print("\n\n🔍 NAMING PATTERN ANALYSIS")
print("=" * 80)

camelCase_keys = [k for k in all_keys if any(c.isupper() for c in k[1:])]
snake_case_keys = [k for k in all_keys if '_' in k]
all_lower_keys = [k for k in all_keys if k.islower()]

print(f"camelCase keys: {len(camelCase_keys)}")
print(f"snake_case keys: {len(snake_case_keys)}")
print(f"all lowercase keys: {len(all_lower_keys)}")

# Find potential duplicates
print("\n\n⚠️  POTENTIAL ISSUES")
print("=" * 80)

# Similar keys (potential duplicates)
print("\n1. Similar/Duplicate Keys:")
similar_groups = defaultdict(list)
for key in all_keys:
    base = key.lower().replace('_', '')
    similar_groups[base].append(key)

duplicates = {k: v for k, v in similar_groups.items() if len(v) > 1}
if duplicates:
    for base, keys in sorted(duplicates.items())[:10]:
        print(f"  {base}: {', '.join(keys)}")
else:
    print("  ✓ No obvious duplicates found")

# Too generic keys
print("\n2. Too Generic Keys:")
generic_keys = [k for k in all_keys if k in ['error', 'success', 'info', 'warning',
                                              'title', 'description', 'name', 'data',
                                              'select', 'view', 'list', 'item']]
if generic_keys:
    for key in generic_keys:
        print(f"  - {key}")
else:
    print("  ✓ No overly generic keys")

# Inconsistent naming
print("\n3. Inconsistent Naming Patterns:")
inconsistent = []

# Check for mixed conventions
for key in all_keys:
    if '_' in key and any(c.isupper() for c in key):
        inconsistent.append(f"{key} (mixed snake_case and camelCase)")

if inconsistent:
    for issue in inconsistent[:10]:
        print(f"  - {issue}")
else:
    print("  ✓ Consistent naming convention")

# Keys with unusual characters
print("\n4. Keys with Unusual Patterns:")
unusual = []
for key in all_keys:
    if any(char in key for char in ['@', '#', '$', '%', '&', '*']):
        unusual.append(key)
    if key[0].isupper():
        unusual.append(f"{key} (starts with uppercase)")

if unusual:
    for key in unusual[:10]:
        print(f"  - {key}")
else:
    print("  ✓ No unusual patterns")

# Check for missing contextual translations
print("\n5. Missing Contextual Variations:")
context_checks = [
    ('title', 'description'),
    ('button', 'label'),
    ('error', 'success'),
    ('enabled', 'disabled'),
]

missing_context = []
for base, context in context_checks:
    base_keys = [k for k in all_keys if base in k.lower()]
    context_keys = [k for k in all_keys if context in k.lower()]

    if len(base_keys) > 0 and len(context_keys) == 0:
        missing_context.append(f"Has {base} keys but no {context} keys")

if missing_context:
    for issue in missing_context:
        print(f"  - {issue}")
else:
    print("  ✓ Good contextual coverage")

# Very long key names
print("\n6. Overly Long Key Names:")
long_keys = [k for k in all_keys if len(k) > 40]
if long_keys:
    for key in sorted(long_keys, key=len, reverse=True)[:10]:
        print(f"  - {key} ({len(key)} chars)")
else:
    print("  ✓ No overly long keys")

# Keys that look like they have hardcoded values
print("\n7. Potential Hardcoded Strings in Keys:")
hardcoded_patterns = [
    r'\d+',  # numbers
    r'[A-Z]{2,}',  # consecutive uppercase
]

potential_hardcoded = []
for key, value in simple_keys:
    if 'feature' in key.lower() and re.search(r'feature\d+', key.lower()):
        potential_hardcoded.append(f"{key}: {value[:50]}")

if potential_hardcoded:
    for issue in potential_hardcoded[:5]:
        print(f"  - {issue}")
else:
    print("  ✓ No obvious hardcoded patterns")

# Summary statistics
print("\n\n📈 SUMMARY STATISTICS")
print("=" * 80)
print(f"Total keys: {len(all_keys)}")
print(f"Categorized: {sum(len(v) for k, v in categorized_keys.items() if k != 'UNCATEGORIZED')}")
print(f"Uncategorized: {len(categorized_keys.get('UNCATEGORIZED', []))}")
print(f"Simple keys: {len(simple_keys)}")
print(f"Method keys (with parameters): {len(method_keys)}")

# Recommendations
print("\n\n💡 RECOMMENDATIONS")
print("=" * 80)

print("""
1. NAMING CONSISTENCY:
   - Standardize on camelCase (current majority) or snake_case
   - Current mix: {camel} camelCase, {snake} snake_case, {lower} lowercase
   - Recommendation: Stick with camelCase for consistency

2. ORGANIZATION:
   - Group related keys with prefixes (e.g., 'premium_', 'compatibility_')
   - Create logical namespaces for large domains
   - Current: {unc} uncategorized keys need better organization

3. DUPLICATE REDUCTION:
   - Review {dup} potential duplicate key groups
   - Consolidate similar translations where appropriate
   - Ensure each key has a unique, clear purpose

4. CONTEXTUAL CLARITY:
   - Add suffixes for context: _title, _description, _button, _label
   - Example: 'premium' → 'premiumTitle', 'premiumDescription'
   - Improves maintainability and searchability

5. KEY NAMING:
   - Avoid overly generic names (error, data, info)
   - Be specific about context and usage
   - Example: 'error' → 'purchaseError', 'networkError'

6. DOCUMENTATION:
   - Add comments for complex or ambiguous translations
   - Document when keys are used in multiple contexts
   - Create a translation style guide

7. PREMIUM FEATURE KEYS:
   - Replace generic 'feature1', 'feature2' with descriptive names
   - Example: 'feature1' → 'premiumUnlimitedHoroscopes'
   - Improves code readability and maintenance

8. INTERNATIONALIZATION:
   - Ensure all user-facing strings use localization
   - Check for any hardcoded strings in the codebase
   - Verify all placeholders have proper parameter names

9. GDPR COMPLIANCE:
   - Good coverage of GDPR-related keys
   - Ensure all consent flows are properly translated
   - Maintain consistency across all languages

10. TESTING:
    - Implement automated tests for missing translations
    - Check for unused translation keys
    - Verify parameter interpolation works correctly
""".format(
    camel=len(camelCase_keys),
    snake=len(snake_case_keys),
    lower=len(all_lower_keys),
    unc=len(categorized_keys.get('UNCATEGORIZED', [])),
    dup=len(duplicates)
))

print("\n✅ ANALYSIS COMPLETE")
print("=" * 80)
