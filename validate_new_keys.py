#!/usr/bin/env python3
"""
Validates the actual translation values for the 3 new keys.
Extracts and displays full translations for quality review.
"""

import re
import os

BASE_PATH = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/l10n"
LANGUAGES = {
    'en': 'app_localizations_en.dart',
    'es': 'app_localizations_es.dart',
    'de': 'app_localizations_de.dart',
    'fr': 'app_localizations_fr.dart',
    'it': 'app_localizations_it.dart',
    'pt': 'app_localizations_pt.dart'
}

NEW_KEYS = ['premiumAnalysisTitle', 'premiumAnalysisDescription', 'viewAnalysis']

def extract_key_value(filepath: str, key_name: str) -> str:
    """Extract the full value of a specific key from a localization file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # Find the getter declaration
        if f'String get {key_name} =>' in line:
            # Check if it's a single-line getter
            if line.strip().endswith("';"):
                # Extract value from single line
                match = re.search(r"=> ['\"](.+?)['\"];", line)
                if match:
                    return match.group(1)

            # Multi-line getter - collect all lines until we find the closing
            value_lines = []

            # Check if value starts on same line
            if "'" in line or '"' in line:
                # Extract starting value
                parts = line.split('=>')
                if len(parts) > 1:
                    start_value = parts[1].strip().lstrip('\'"')
                    if start_value and not start_value.startswith("';"):
                        value_lines.append(start_value)

            # Collect continuation lines
            j = i + 1
            while j < len(lines):
                current_line = lines[j].strip()

                # Check if this is the end
                if current_line.endswith("';"):
                    # Add final line without the closing
                    final_value = current_line.rstrip("';").strip().strip('\'"')
                    if final_value:
                        value_lines.append(final_value)
                    break

                # Add continuation line
                cleaned = current_line.strip('\'"')
                if cleaned:
                    value_lines.append(cleaned)

                j += 1

            return ' '.join(value_lines).strip()

    return "NOT FOUND"

def main():
    print("=" * 80)
    print("NEW KEYS TRANSLATION VALIDATION")
    print("=" * 80)
    print()

    for key in NEW_KEYS:
        print(f"\n{'=' * 80}")
        print(f"KEY: {key}")
        print('=' * 80)

        for lang_code, filename in LANGUAGES.items():
            filepath = os.path.join(BASE_PATH, filename)
            value = extract_key_value(filepath, key)

            print(f"\n{lang_code.upper()} ({filename}):")
            print(f"  {value}")

        print()

    # Check for consistency patterns
    print("\n" + "=" * 80)
    print("CONSISTENCY CHECKS")
    print("=" * 80)
    print()

    # Check if all languages have translations (not placeholders)
    print("Checking for placeholder text or missing translations...")
    issues = []

    for key in NEW_KEYS:
        for lang_code, filename in LANGUAGES.items():
            filepath = os.path.join(BASE_PATH, filename)
            value = extract_key_value(filepath, key)

            # Check for common placeholder patterns
            if value == "NOT FOUND":
                issues.append(f"  ✗ {key} in {lang_code.upper()}: NOT FOUND")
            elif len(value) < 5:
                issues.append(f"  ⚠ {key} in {lang_code.upper()}: Suspiciously short ({len(value)} chars)")
            elif value.lower() in ['todo', 'tbd', 'pending', 'translate']:
                issues.append(f"  ✗ {key} in {lang_code.upper()}: Placeholder detected")

    if issues:
        print("Issues found:")
        for issue in issues:
            print(issue)
    else:
        print("✓ All translations look good!")
        print("✓ No placeholders detected")
        print("✓ All keys have substantial translations")

    print()

    # Character length analysis
    print("\n" + "=" * 80)
    print("CHARACTER LENGTH ANALYSIS")
    print("=" * 80)
    print()

    for key in NEW_KEYS:
        print(f"\n{key}:")
        lengths = {}
        for lang_code, filename in LANGUAGES.items():
            filepath = os.path.join(BASE_PATH, filename)
            value = extract_key_value(filepath, key)
            lengths[lang_code] = len(value)

        # Sort by length
        sorted_langs = sorted(lengths.items(), key=lambda x: x[1], reverse=True)

        for lang, length in sorted_langs:
            bar = '█' * (length // 5)
            print(f"  {lang.upper()}: {length:3} chars {bar}")

        avg_length = sum(lengths.values()) / len(lengths)
        print(f"  Average: {avg_length:.1f} chars")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
