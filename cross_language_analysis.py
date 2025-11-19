#!/usr/bin/env python3
"""
Cross-Language Localization Consistency Analyzer
Analyzes all 6 localization files for key parity, completeness, and quality metrics.
"""

import re
import os
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict

# File paths
BASE_PATH = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/l10n"
LANGUAGES = {
    'en': 'app_localizations_en.dart',
    'es': 'app_localizations_es.dart',
    'de': 'app_localizations_de.dart',
    'fr': 'app_localizations_fr.dart',
    'it': 'app_localizations_it.dart',
    'pt': 'app_localizations_pt.dart'
}

# New keys to validate
NEW_KEYS = ['premiumAnalysisTitle', 'premiumAnalysisDescription', 'viewAnalysis']

def extract_keys_from_file(filepath: str) -> Dict[str, Tuple[int, str]]:
    """Extract all getter method names (keys) from a localization file with line numbers and values."""
    keys = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match getter methods: String get keyName => 'value';
        getter_match = re.match(r'\s*String get (\w+)\s*=>\s*["\'](.+?)["\'];', line)
        if getter_match:
            key_name = getter_match.group(1)
            value = getter_match.group(2)
            keys[key_name] = (i + 1, value)
            i += 1
            continue

        # Match multi-line getters (start): String get keyName =>
        getter_start = re.match(r'\s*String get (\w+)\s*=>', line)
        if getter_start:
            key_name = getter_start.group(1)

            # Check if value starts on same line
            if "'" in line or '"' in line:
                # Extract value starting from this line
                value_start = line.split('=>')[1].strip() if '=>' in line else ''
                value_start = value_start.strip('\'"')

                # Collect continuation lines
                full_value = value_start
                j = i + 1
                while j < len(lines) and not lines[j].strip().endswith("';"):
                    full_value += lines[j].strip().strip('\'"')
                    j += 1

                # Add final line
                if j < len(lines):
                    full_value += lines[j].strip().rstrip("';").strip('\'"')

                keys[key_name] = (i + 1, full_value[:100])  # Truncate long values
            else:
                # Value on next line
                keys[key_name] = (i + 1, "(multi-line)")

            i += 1
            continue

        i += 1

    return keys

def analyze_localization_files():
    """Main analysis function."""

    print("=" * 80)
    print("CROSS-LANGUAGE LOCALIZATION CONSISTENCY ANALYSIS")
    print("=" * 80)
    print()

    # Step 1: Extract keys from all files
    all_keys = {}
    file_paths = {}

    print("Reading localization files...")
    for lang_code, filename in LANGUAGES.items():
        filepath = os.path.join(BASE_PATH, filename)
        file_paths[lang_code] = filepath

        if os.path.exists(filepath):
            all_keys[lang_code] = extract_keys_from_file(filepath)
            print(f"  {lang_code.upper()}: {len(all_keys[lang_code])} keys found")
        else:
            print(f"  {lang_code.upper()}: FILE NOT FOUND!")
            all_keys[lang_code] = {}

    print()

    # Get baseline (English) keys
    en_keys = set(all_keys['en'].keys())
    total_keys = len(en_keys)

    # Step 2: Key Parity Analysis
    print("=" * 80)
    print("1. KEY PARITY ANALYSIS")
    print("=" * 80)
    print()

    missing_in_languages = defaultdict(set)
    extra_in_languages = defaultdict(set)

    for lang_code in LANGUAGES.keys():
        if lang_code == 'en':
            continue

        lang_keys = set(all_keys[lang_code].keys())

        # Missing in this language (exists in EN but not in lang)
        missing = en_keys - lang_keys
        if missing:
            missing_in_languages[lang_code] = missing

        # Extra in this language (exists in lang but not in EN)
        extra = lang_keys - en_keys
        if extra:
            extra_in_languages[lang_code] = extra

    # Print missing keys
    print("Keys Missing in Other Languages (exist in EN but not in target):")
    print("-" * 80)
    for lang_code in sorted(missing_in_languages.keys()):
        print(f"\n{lang_code.upper()} - Missing {len(missing_in_languages[lang_code])} keys:")
        for key in sorted(missing_in_languages[lang_code])[:20]:  # Show first 20
            print(f"  - {key}")
        if len(missing_in_languages[lang_code]) > 20:
            print(f"  ... and {len(missing_in_languages[lang_code]) - 20} more")

    if not missing_in_languages:
        print("  ✓ No missing keys! All languages have all EN keys.")

    print("\n" + "-" * 80)
    print("\nKeys Extra in Other Languages (exist in target but not in EN):")
    print("-" * 80)
    for lang_code in sorted(extra_in_languages.keys()):
        print(f"\n{lang_code.upper()} - Extra {len(extra_in_languages[lang_code])} keys:")
        for key in sorted(extra_in_languages[lang_code])[:10]:
            print(f"  - {key}")
        if len(extra_in_languages[lang_code]) > 10:
            print(f"  ... and {len(extra_in_languages[lang_code]) - 10} more")

    if not extra_in_languages:
        print("  ✓ No extra keys! All languages match EN structure.")

    print("\n")

    # Step 3: Key Parity Matrix
    print("=" * 80)
    print("2. KEY PARITY MATRIX")
    print("=" * 80)
    print()

    # Get all unique keys across all languages
    all_unique_keys = set()
    for keys in all_keys.values():
        all_unique_keys.update(keys.keys())

    print(f"Total unique keys across all languages: {len(all_unique_keys)}")
    print()

    # Create CSV matrix (sample - first 30 keys)
    print("Sample Key Parity Matrix (first 30 keys):")
    print("-" * 80)
    print("Key," + ",".join([lang.upper() for lang in LANGUAGES.keys()]))

    sample_keys = sorted(list(all_unique_keys))[:30]
    for key in sample_keys:
        row = [key]
        for lang_code in LANGUAGES.keys():
            row.append("✓" if key in all_keys[lang_code] else "✗")
        print(",".join(row))

    print("\n")

    # Step 4: Translation Completeness
    print("=" * 80)
    print("3. TRANSLATION COMPLETENESS METRICS")
    print("=" * 80)
    print()

    completeness = {}
    for lang_code in LANGUAGES.keys():
        lang_keys = set(all_keys[lang_code].keys())
        completion_pct = (len(lang_keys) / total_keys * 100) if total_keys > 0 else 0
        completeness[lang_code] = {
            'total_keys': len(lang_keys),
            'percentage': completion_pct,
            'missing_count': len(en_keys - lang_keys) if lang_code != 'en' else 0
        }

    # Sort by completion percentage
    sorted_langs = sorted(completeness.items(), key=lambda x: x[1]['percentage'], reverse=True)

    print(f"Baseline (EN): {total_keys} keys")
    print()
    print("Language | Total Keys | Completion % | Missing Keys")
    print("-" * 70)
    for lang_code, metrics in sorted_langs:
        print(f"{lang_code.upper():8} | {metrics['total_keys']:10} | {metrics['percentage']:11.2f}% | {metrics['missing_count']:12}")

    print("\n")

    # Best and worst
    best_lang = sorted_langs[0][0]
    worst_lang = sorted_langs[-1][0]

    print(f"Best Coverage:  {best_lang.upper()} ({completeness[best_lang]['percentage']:.2f}%)")
    print(f"Worst Coverage: {worst_lang.upper()} ({completeness[worst_lang]['percentage']:.2f}%)")

    print("\n")

    # Step 5: New Keys Validation
    print("=" * 80)
    print("4. NEW KEYS VALIDATION")
    print("=" * 80)
    print()

    print(f"Validating {len(NEW_KEYS)} newly added keys across all languages:")
    print()

    new_keys_status = {}
    for key in NEW_KEYS:
        status = {}
        for lang_code in LANGUAGES.keys():
            exists = key in all_keys[lang_code]
            status[lang_code] = exists
            if exists:
                line_num, value = all_keys[lang_code][key]
                status[f'{lang_code}_line'] = line_num
                status[f'{lang_code}_value'] = value[:80]  # Truncate
        new_keys_status[key] = status

    for key in NEW_KEYS:
        print(f"\nKey: {key}")
        print("-" * 70)
        status = new_keys_status[key]

        for lang_code in LANGUAGES.keys():
            exists = status[lang_code]
            if exists:
                line_num = status[f'{lang_code}_line']
                value = status[f'{lang_code}_value']
                print(f"  {lang_code.upper()}: ✓ Line {line_num:4} | {value}")
            else:
                print(f"  {lang_code.upper()}: ✗ MISSING")

    print("\n")

    # Summary for new keys
    all_present = all(all(status[lang] for lang in LANGUAGES.keys()) for status in new_keys_status.values())
    if all_present:
        print("✓ All new keys are present in ALL languages!")
    else:
        print("✗ Some new keys are missing in some languages")

    print("\n")

    # Step 6: Quality Metrics Summary
    print("=" * 80)
    print("5. QUALITY METRICS SUMMARY")
    print("=" * 80)
    print()

    # Calculate systematic gaps (keys missing in ALL non-EN languages)
    systematic_gaps = en_keys.copy()
    for lang_code in LANGUAGES.keys():
        if lang_code != 'en':
            lang_keys = set(all_keys[lang_code].keys())
            systematic_gaps &= lang_keys

    keys_missing_everywhere = en_keys - systematic_gaps

    print(f"Total EN Keys: {total_keys}")
    print(f"Keys present in ALL languages: {len(systematic_gaps)}")
    print(f"Keys missing in at least ONE language: {len(keys_missing_everywhere)}")
    print()

    if keys_missing_everywhere:
        print("Keys missing in at least one language (sample - first 15):")
        for key in sorted(list(keys_missing_everywhere))[:15]:
            # Show which languages are missing this key
            missing_in = [lang.upper() for lang in LANGUAGES.keys() if key not in all_keys[lang]]
            print(f"  - {key}: missing in {', '.join(missing_in)}")
        if len(keys_missing_everywhere) > 15:
            print(f"  ... and {len(keys_missing_everywhere) - 15} more")

    print("\n")

    # Step 7: Priority Languages for Improvement
    print("=" * 80)
    print("6. PRIORITY LANGUAGES FOR IMPROVEMENT")
    print("=" * 80)
    print()

    # Sort by missing count (descending)
    priority_order = sorted(
        [(lang, completeness[lang]['missing_count']) for lang in LANGUAGES.keys() if lang != 'en'],
        key=lambda x: x[1],
        reverse=True
    )

    print("Languages ranked by number of missing translations:")
    print()
    for rank, (lang_code, missing_count) in enumerate(priority_order, 1):
        urgency = "HIGH" if missing_count > 50 else "MEDIUM" if missing_count > 10 else "LOW"
        print(f"{rank}. {lang_code.upper()}: {missing_count} missing keys - Priority: {urgency}")

    print("\n")

    # Export full CSV matrix
    print("=" * 80)
    print("EXPORTING FULL KEY PARITY MATRIX TO CSV")
    print("=" * 80)
    print()

    csv_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/key_parity_matrix.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("Key," + ",".join([lang.upper() for lang in LANGUAGES.keys()]) + "\n")

        # All keys
        for key in sorted(all_unique_keys):
            row = [key]
            for lang_code in LANGUAGES.keys():
                row.append("YES" if key in all_keys[lang_code] else "NO")
            f.write(",".join(row) + "\n")

    print(f"✓ Full matrix exported to: {csv_path}")
    print(f"  Total rows: {len(all_unique_keys) + 1} (including header)")

    print("\n")

    # Export missing keys report
    print("Exporting detailed missing keys report...")
    report_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/missing_keys_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("MISSING KEYS DETAILED REPORT\n")
        f.write("=" * 80 + "\n\n")

        for lang_code in sorted(LANGUAGES.keys()):
            if lang_code == 'en':
                continue

            missing = missing_in_languages.get(lang_code, set())
            f.write(f"\n{lang_code.upper()} - {len(missing)} missing keys:\n")
            f.write("-" * 80 + "\n")

            for key in sorted(missing):
                en_line, en_value = all_keys['en'].get(key, (0, ''))
                f.write(f"  {key}\n")
                f.write(f"    EN (line {en_line}): {en_value[:100]}\n")

            if not missing:
                f.write("  ✓ No missing keys!\n")

    print(f"✓ Missing keys report exported to: {report_path}")

    print("\n")
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    analyze_localization_files()
