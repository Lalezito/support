#!/usr/bin/env python3
"""
Comprehensive Translation Validation Script
Validates all 4 translation files for Cosmic Goals
"""

import json
import re
from pathlib import Path

# Emoji regex pattern
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F9FF"  # Emoticons & symbols
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F680-\U0001F6FF"  # Transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # Flags
    "\U00002600-\U000027BF"  # Miscellaneous symbols
    "\U0001F900-\U0001F9FF"  # Supplemental symbols
    "]+",
    flags=re.UNICODE
)

def count_emojis(text):
    """Count emojis in a string"""
    return len(EMOJI_PATTERN.findall(text))

def extract_all_strings(data):
    """Extract all translatable strings from JSON structure"""
    strings = []

    # Tips database
    if "1_tips_database" in data and "strings" in data["1_tips_database"]:
        strings.extend(data["1_tips_database"]["strings"].values())

    # Celebration messages
    if "2_celebration_messages" in data and "categories" in data["2_celebration_messages"]:
        for category_messages in data["2_celebration_messages"]["categories"].values():
            if isinstance(category_messages, list):
                strings.extend(category_messages)

    # UI strings
    if "3_ui_strings" in data and "strings" in data["3_ui_strings"]:
        strings.extend(data["3_ui_strings"]["strings"].values())

    return strings

def validate_file(filepath, lang_name):
    """Validate a single translation file"""
    print(f"\n{'='*60}")
    print(f"VALIDATING {lang_name}")
    print('='*60)

    results = {
        "language": lang_name,
        "file": filepath.name,
        "json_valid": False,
        "string_count": 0,
        "emoji_count": 0,
        "placeholder_count": 0,
        "issues": []
    }

    # 1. JSON Syntax Validation
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results["json_valid"] = True
        print(f"✅ JSON: Valid")
    except Exception as e:
        results["issues"].append(f"JSON syntax error: {e}")
        print(f"❌ JSON: INVALID - {e}")
        return results

    # 2. String Count Validation
    all_strings = extract_all_strings(data)
    results["string_count"] = len(all_strings)

    tips_count = len(data.get("1_tips_database", {}).get("strings", {}))
    celebration_count = 0
    if "2_celebration_messages" in data:
        for cat_msgs in data["2_celebration_messages"]["categories"].values():
            celebration_count += len(cat_msgs) if isinstance(cat_msgs, list) else 0
    ui_count = len(data.get("3_ui_strings", {}).get("strings", {}))

    print(f"✅ Strings: {results['string_count']}/89")
    print(f"   - Tips: {tips_count}/38")
    print(f"   - Celebrations: {celebration_count}/39")
    print(f"   - UI: {ui_count}/12")

    if results["string_count"] != 89:
        results["issues"].append(f"Expected 89 strings, found {results['string_count']}")

    # 3. Emoji Count Validation
    total_emojis = sum(count_emojis(s) for s in all_strings)
    results["emoji_count"] = total_emojis
    print(f"✅ Emojis: {total_emojis}/89")

    if total_emojis != 89:
        results["issues"].append(f"Expected 89 emojis, found {total_emojis}")

    # 4. Placeholder Validation
    file_content = filepath.read_text(encoding='utf-8')
    placeholder_matches = re.findall(r'\{userSign\}', file_content)
    results["placeholder_count"] = len(placeholder_matches)
    print(f"✅ Placeholders: {results['placeholder_count']} instances of {{userSign}}")

    if results["placeholder_count"] < 3:
        results["issues"].append(f"Expected at least 3 {{userSign}} placeholders, found {results['placeholder_count']}")

    # 5. Length Analysis
    print(f"\n📏 Length Analysis:")
    total_length = sum(len(s) for s in all_strings)
    avg_length = total_length / len(all_strings) if all_strings else 0
    print(f"   - Total characters: {total_length}")
    print(f"   - Average per string: {avg_length:.1f}")

    return results

def main():
    """Main validation function"""
    base_path = Path(__file__).parent

    languages = {
        "FRENCH": "COSMIC_GOALS_FRENCH_TRANSLATIONS.json",
        "GERMAN": "COSMIC_GOALS_GERMAN_TRANSLATIONS.json",
        "PORTUGUESE": "COSMIC_GOALS_PORTUGUESE_TRANSLATIONS.json",
        "ITALIAN": "COSMIC_GOALS_ITALIAN_TRANSLATIONS.json"
    }

    all_results = []

    # Validate each file
    for lang_name, filename in languages.items():
        filepath = base_path / filename
        if not filepath.exists():
            print(f"\n❌ {lang_name}: File not found - {filename}")
            continue

        results = validate_file(filepath, lang_name)
        all_results.append(results)

    # Summary Report
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print('='*60)

    all_pass = True
    for result in all_results:
        status = "✅ PASS" if not result["issues"] else "⚠️  ISSUES FOUND"
        if result["issues"]:
            all_pass = False

        print(f"\n{result['language']}: {status}")
        print(f"  - JSON: {'Valid' if result['json_valid'] else 'INVALID'}")
        print(f"  - Strings: {result['string_count']}/89")
        print(f"  - Emojis: {result['emoji_count']}/89")
        print(f"  - Placeholders: {result['placeholder_count']}")

        if result["issues"]:
            print(f"  ⚠️  Issues:")
            for issue in result["issues"]:
                print(f"     - {issue}")

    print(f"\n{'='*60}")
    if all_pass:
        print("🎉 FINAL APPROVAL: YES - All translations validated successfully!")
    else:
        print("⚠️  FINAL APPROVAL: REVIEW NEEDED - Issues found above")
    print('='*60)

    return 0 if all_pass else 1

if __name__ == "__main__":
    exit(main())
