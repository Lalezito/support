#!/usr/bin/env python3
"""
Spanish Localization Analysis Tool
Comprehensive analysis of Spanish translations vs English source
"""

import re
import json
from collections import defaultdict

def extract_getters(file_path):
    """Extract all getter methods and their return values from a localization file"""
    getters = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match getter methods with their return values
    # Matches: String get keyName => 'value';
    pattern = r"String get (\w+)\s*=>\s*'([^']*(?:\\.[^']*)*)'\s*;"

    matches = re.finditer(pattern, content, re.MULTILINE)

    for match in matches:
        key = match.group(1)
        value = match.group(2)
        # Get line number
        line_num = content[:match.start()].count('\n') + 1
        getters[key] = {
            'value': value,
            'line': line_num
        }

    return getters

def is_english_text(text):
    """Check if text appears to be in English (common English words)"""
    english_words = [
        'the', 'and', 'or', 'is', 'are', 'was', 'were', 'have', 'has', 'had',
        'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must',
        'Premium', 'Unlock', 'Subscribe', 'Free', 'Trial', 'Cancel', 'Save',
        'View', 'Edit', 'Delete', 'Create', 'Update', 'Settings', 'Profile',
        'Account', 'Login', 'Logout', 'Sign', 'Register', 'Email', 'Password',
        'Compatibility', 'Analysis', 'Reading', 'Chart', 'Horoscope',
        'Daily', 'Weekly', 'Monthly', 'Yearly', 'Today', 'Tomorrow',
        'Zodiac', 'Sign', 'Ascendant', 'Moon', 'Planet', 'House'
    ]

    # Check if any English word appears in the text
    text_lower = text.lower()
    for word in english_words:
        if re.search(r'\b' + word.lower() + r'\b', text_lower):
            return True
    return False

def check_spanish_issues(key, value):
    """Check for common Spanish localization issues"""
    issues = []

    # Check for spacing issues
    if '  ' in value:
        issues.append('Double spacing detected')

    # Check for English remnants
    if is_english_text(value):
        issues.append('Contains English words')

    # Check for proper Spanish punctuation
    if '¿' in value and '?' not in value:
        issues.append('Opening question mark without closing')
    if '?' in value and '¿' not in value:
        issues.append('Question mark without opening ¿')

    # Check for common untranslated technical terms that should be translated
    untranslated_terms = {
        'Premium': 'Premium',  # Often kept as-is
        'Email': 'Correo electrónico',
        'Password': 'Contraseña',
        'Login': 'Iniciar sesión',
        'Logout': 'Cerrar sesión',
        'Settings': 'Configuración',
        'Profile': 'Perfil',
    }

    # Check for informal vs formal (this is basic, context matters)
    has_tu = bool(re.search(r'\bt[uú]\b', value.lower()))
    has_usted = bool(re.search(r'\busted\b', value.lower()))

    if has_tu and has_usted:
        issues.append('Mixed formal/informal (tú and usted)')

    return issues

def analyze_translations():
    """Main analysis function"""

    en_file = '/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/l10n/app_localizations_en.dart'
    es_file = '/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/l10n/app_localizations_es.dart'

    print("=" * 80)
    print("SPANISH LOCALIZATION ANALYSIS REPORT")
    print("=" * 80)
    print()

    # Extract getters from both files
    print("Extracting English translations...")
    en_getters = extract_getters(en_file)
    print(f"Found {len(en_getters)} English keys")

    print("Extracting Spanish translations...")
    es_getters = extract_getters(es_file)
    print(f"Found {len(es_getters)} Spanish keys")
    print()

    # 1. Find missing keys
    print("=" * 80)
    print("1. MISSING KEYS (exist in EN but not in ES)")
    print("=" * 80)
    missing_keys = set(en_getters.keys()) - set(es_getters.keys())
    if missing_keys:
        for key in sorted(missing_keys):
            en_value = en_getters[key]['value']
            print(f"  - {key}")
            print(f"    EN (line {en_getters[key]['line']}): {en_value}")
            print()
    else:
        print("  ✓ No missing keys found!")
    print(f"Total: {len(missing_keys)} missing keys")
    print()

    # 2. Find extra keys
    print("=" * 80)
    print("2. EXTRA KEYS (exist in ES but not in EN)")
    print("=" * 80)
    extra_keys = set(es_getters.keys()) - set(en_getters.keys())
    if extra_keys:
        for key in sorted(extra_keys):
            es_value = es_getters[key]['value']
            print(f"  - {key}")
            print(f"    ES (line {es_getters[key]['line']}): {es_value}")
            print()
    else:
        print("  ✓ No extra keys found!")
    print(f"Total: {len(extra_keys)} extra keys")
    print()

    # 3. Check for untranslated keys (identical to English)
    print("=" * 80)
    print("3. UNTRANSLATED KEYS (identical to English)")
    print("=" * 80)
    untranslated = []
    for key in sorted(es_getters.keys()):
        if key in en_getters:
            if es_getters[key]['value'] == en_getters[key]['value']:
                untranslated.append(key)
                print(f"  - {key} (line {es_getters[key]['line']})")
                print(f"    Value: {es_getters[key]['value']}")
                print()
    print(f"Total: {len(untranslated)} untranslated keys")
    print()

    # 4. Check for keys still containing English words
    print("=" * 80)
    print("4. KEYS CONTAINING ENGLISH WORDS")
    print("=" * 80)
    english_remnants = []
    for key in sorted(es_getters.keys()):
        value = es_getters[key]['value']
        if is_english_text(value) and key not in untranslated:
            english_remnants.append(key)
            print(f"  - {key} (line {es_getters[key]['line']})")
            print(f"    ES: {value}")
            if key in en_getters:
                print(f"    EN: {en_getters[key]['value']}")
            print()
    print(f"Total: {len(english_remnants)} keys with English words")
    print()

    # 5. Check for Spanish-specific issues
    print("=" * 80)
    print("5. SPANISH LOCALIZATION ISSUES")
    print("=" * 80)
    issues_found = {}
    for key in sorted(es_getters.keys()):
        value = es_getters[key]['value']
        issues = check_spanish_issues(key, value)
        if issues:
            issues_found[key] = {
                'value': value,
                'line': es_getters[key]['line'],
                'issues': issues
            }
            print(f"  - {key} (line {es_getters[key]['line']})")
            print(f"    Value: {value}")
            print(f"    Issues: {', '.join(issues)}")
            print()
    print(f"Total: {len(issues_found)} keys with issues")
    print()

    # 6. Verify the three new keys
    print("=" * 80)
    print("6. VERIFICATION OF NEW PREMIUM KEYS")
    print("=" * 80)
    new_keys = ['premiumAnalysisTitle', 'premiumAnalysisDescription', 'viewAnalysis']
    for key in new_keys:
        if key in es_getters:
            print(f"  ✓ {key} (line {es_getters[key]['line']})")
            print(f"    Value: {es_getters[key]['value']}")
        else:
            print(f"  ✗ {key} - NOT FOUND")
        print()

    # 7. Calculate quality score
    print("=" * 80)
    print("7. QUALITY SCORE")
    print("=" * 80)

    total_keys = len(en_getters)
    translated_keys = len(es_getters) - len(untranslated)
    coverage = (len(es_getters) / total_keys * 100) if total_keys > 0 else 0
    quality = ((translated_keys - len(english_remnants) - len(issues_found)) / total_keys * 100) if total_keys > 0 else 0

    print(f"  Total English keys: {total_keys}")
    print(f"  Total Spanish keys: {len(es_getters)}")
    print(f"  Coverage: {coverage:.2f}%")
    print(f"  Missing keys: {len(missing_keys)}")
    print(f"  Untranslated: {len(untranslated)}")
    print(f"  English remnants: {len(english_remnants)}")
    print(f"  Issues found: {len(issues_found)}")
    print(f"  Quality Score: {quality:.2f}%")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Coverage: {coverage:.1f}% - {'✓ Excellent' if coverage > 95 else '⚠ Needs improvement'}")
    print(f"Quality: {quality:.1f}% - {'✓ Excellent' if quality > 90 else '✓ Good' if quality > 75 else '⚠ Needs improvement'}")
    print()

    # Export detailed report
    report = {
        'summary': {
            'total_en_keys': total_keys,
            'total_es_keys': len(es_getters),
            'coverage_percent': coverage,
            'quality_percent': quality,
            'missing_keys': len(missing_keys),
            'untranslated_keys': len(untranslated),
            'english_remnants': len(english_remnants),
            'issues_found': len(issues_found)
        },
        'missing_keys': list(missing_keys),
        'untranslated_keys': untranslated,
        'english_remnants': english_remnants,
        'issues': issues_found
    }

    with open('/Users/alejandrocaceres/Desktop/appstore.zodia/spanish_localization_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("Detailed JSON report saved to: spanish_localization_report.json")

if __name__ == '__main__':
    analyze_translations()
