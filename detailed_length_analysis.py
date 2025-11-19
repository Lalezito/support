#!/usr/bin/env python3
"""
Detailed Length Analysis comparing translations to source
"""

import json
from pathlib import Path

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_strings_dict(data):
    """Extract strings as a dictionary for comparison"""
    strings = {}

    # Tips
    if "1_tips_database" in data:
        for key, val in data["1_tips_database"]["strings"].items():
            strings[f"tip_{key}"] = val

    # Celebrations
    if "2_celebration_messages" in data:
        for cat_name, messages in data["2_celebration_messages"]["categories"].items():
            for i, msg in enumerate(messages):
                strings[f"cel_{cat_name}_{i}"] = msg

    # UI
    if "3_ui_strings" in data:
        for key, val in data["3_ui_strings"]["strings"].items():
            strings[f"ui_{key}"] = val

    return strings

def calculate_variance(source_len, target_len):
    """Calculate percentage variance"""
    if source_len == 0:
        return 0
    return ((target_len - source_len) / source_len) * 100

def main():
    base_path = Path(__file__).parent

    # Load source
    source = load_json(base_path / "COSMIC_GOALS_STRINGS_TO_TRANSLATE.json")
    source_strings = extract_strings_dict(source)

    languages = {
        "French": "COSMIC_GOALS_FRENCH_TRANSLATIONS.json",
        "German": "COSMIC_GOALS_GERMAN_TRANSLATIONS.json",
        "Portuguese": "COSMIC_GOALS_PORTUGUESE_TRANSLATIONS.json",
        "Italian": "COSMIC_GOALS_ITALIAN_TRANSLATIONS.json"
    }

    print("="*80)
    print("DETAILED LENGTH ANALYSIS - COMPARING TO ENGLISH SOURCE")
    print("="*80)

    for lang_name, filename in languages.items():
        filepath = base_path / filename
        target = load_json(filepath)
        target_strings = extract_strings_dict(target)

        print(f"\n{lang_name.upper()}:")
        print("-" * 80)

        variances = []
        outliers = []

        for key in source_strings.keys():
            if key in target_strings:
                source_len = len(source_strings[key])
                target_len = len(target_strings[key])
                variance = calculate_variance(source_len, target_len)
                variances.append(variance)

                # Flag outliers (>30% difference)
                if abs(variance) > 30:
                    outliers.append({
                        'key': key,
                        'source_len': source_len,
                        'target_len': target_len,
                        'variance': variance,
                        'source': source_strings[key][:50] + '...',
                        'target': target_strings[key][:50] + '...'
                    })

        avg_variance = sum(variances) / len(variances) if variances else 0
        min_variance = min(variances) if variances else 0
        max_variance = max(variances) if variances else 0

        print(f"Average length variance: {avg_variance:+.1f}%")
        print(f"Range: {min_variance:+.1f}% to {max_variance:+.1f}%")

        within_20 = sum(1 for v in variances if abs(v) <= 20)
        within_30 = sum(1 for v in variances if abs(v) <= 30)
        total = len(variances)

        print(f"Within ±20%: {within_20}/{total} ({100*within_20/total:.1f}%)")
        print(f"Within ±30%: {within_30}/{total} ({100*within_30/total:.1f}%)")

        if outliers:
            print(f"\n⚠️  {len(outliers)} OUTLIERS (>30% variance):")
            for out in outliers[:5]:  # Show first 5
                print(f"  - {out['key']}: {out['variance']:+.1f}%")
                print(f"    EN ({out['source_len']} chars): {out['source']}")
                print(f"    {lang_name[:2].upper()} ({out['target_len']} chars): {out['target']}")
        else:
            print(f"\n✅ No outliers found (all within ±30%)")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
