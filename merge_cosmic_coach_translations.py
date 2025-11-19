#!/usr/bin/env python3
"""
Merge completed Cosmic Coach translations back into main monolithic ARB files
"""
import json
import sys

def merge_translations(main_arb_path, cosmic_coach_arb_path, output_path):
    """Merge Cosmic Coach translations into main ARB file"""
    
    # Load both files
    with open(main_arb_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    with open(cosmic_coach_arb_path, 'r', encoding='utf-8') as f:
        cosmic_data = json.load(f)
    
    # Track updates
    updated = 0
    added = 0
    
    # Merge cosmic coach translations into main
    for key, value in cosmic_data.items():
        if key in main_data:
            # Update existing key
            main_data[key] = value
            updated += 1
        else:
            # Add new key (shouldn't happen but handle it)
            main_data[key] = value
            added += 1
    
    # Save merged file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    return updated, added

if __name__ == '__main__':
    languages = ['es', 'de', 'fr', 'it', 'pt']
    
    print("🔄 Merging Cosmic Coach translations into main ARB files...")
    print()
    
    for lang in languages:
        main_path = f'zodiac_app/assets/l10n/app_{lang}.arb'
        cosmic_path = f'zodiac_app/assets/l10n/features/cosmic_coach/cosmic_coach_{lang}.arb'
        
        print(f"   Processing {lang.upper()}...")
        
        try:
            updated, added = merge_translations(main_path, cosmic_path, main_path)
            print(f"      ✅ Updated: {updated} keys, Added: {added} keys")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print()
    print("✅ Merge complete!")
    print()
