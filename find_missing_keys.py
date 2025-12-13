#!/usr/bin/env python3
"""
Script to find missing translation keys in ARB files.
Identifies keys present in app_en.arb but missing in other language files.
"""

import json
import sys
from pathlib import Path

def load_arb_keys(file_path):
    """Load keys from an ARB file, excluding metadata keys."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Filter out metadata keys (those starting with @)
    return {k for k in data.keys() if not k.startswith('@')}

def prioritize_keys(keys):
    """Categorize keys by priority based on their naming patterns."""
    critical = []
    high = []
    medium = []
    low = []

    for key in sorted(keys):
        key_lower = key.lower()

        # Critical: UI buttons and actions
        if any(x in key_lower for x in ['save', 'cancel', 'delete', 'edit', 'confirm', 'submit', 'continue', 'skip', 'next', 'back', 'done', 'close']):
            critical.append(key)
        # High: Errors and empty states
        elif any(x in key_lower for x in ['error', 'failed', 'empty', 'no_', 'loading', 'success']):
            high.append(key)
        # High: Premium features
        elif any(x in key_lower for x in ['premium', 'subscribe', 'upgrade', 'unlock', 'trial']):
            high.append(key)
        # Medium: Labels and descriptions
        elif any(x in key_lower for x in ['label', 'title', 'description', 'hint', 'placeholder']):
            medium.append(key)
        # Low: Everything else
        else:
            low.append(key)

    return critical, high, medium, low

def main():
    base_path = Path('/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n')

    # Load English keys (baseline)
    en_keys = load_arb_keys(base_path / 'app_en.arb')
    print(f"✓ English baseline: {len(en_keys)} keys\n")

    languages = {
        'de': 'German',
        'fr': 'French',
        'it': 'Italian',
        'pt': 'Portuguese'
    }

    for lang_code, lang_name in languages.items():
        print(f"\n{'='*80}")
        print(f"🔍 Analyzing {lang_name} (app_{lang_code}.arb)")
        print('='*80)

        lang_keys = load_arb_keys(base_path / f'app_{lang_code}.arb')
        missing = en_keys - lang_keys

        print(f"\n📊 Statistics:")
        print(f"  - Current keys: {len(lang_keys)}")
        print(f"  - Missing keys: {len(missing)}")
        print(f"  - Coverage: {(len(lang_keys)/len(en_keys)*100):.1f}%")

        if missing:
            critical, high, medium, low = prioritize_keys(missing)

            print(f"\n📋 Missing Keys by Priority:")
            print(f"  🔴 Critical (UI Actions): {len(critical)}")
            print(f"  🟠 High (Errors/Premium): {len(high)}")
            print(f"  🟡 Medium (Labels): {len(medium)}")
            print(f"  ⚪ Low (Other): {len(low)}")

            # Show top critical keys
            if critical:
                print(f"\n🔴 Top Critical Keys (showing first 20):")
                for key in critical[:20]:
                    print(f"     - {key}")
                if len(critical) > 20:
                    print(f"     ... and {len(critical) - 20} more")

            # Show top high priority keys
            if high:
                print(f"\n🟠 Top High Priority Keys (showing first 20):")
                for key in high[:20]:
                    print(f"     - {key}")
                if len(high) > 20:
                    print(f"     ... and {len(high) - 20} more")

            # Write full list to file
            output_file = base_path / f'missing_keys_{lang_code}.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Missing keys in {lang_name} ({lang_code})\n")
                f.write(f"Total: {len(missing)}\n\n")

                f.write("CRITICAL (UI Actions):\n")
                for key in critical:
                    f.write(f"  {key}\n")

                f.write("\nHIGH (Errors/Premium):\n")
                for key in high:
                    f.write(f"  {key}\n")

                f.write("\nMEDIUM (Labels):\n")
                for key in medium:
                    f.write(f"  {key}\n")

                f.write("\nLOW (Other):\n")
                for key in low:
                    f.write(f"  {key}\n")

            print(f"\n💾 Full list saved to: {output_file}")

if __name__ == '__main__':
    main()
