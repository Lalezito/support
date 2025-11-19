#!/usr/bin/env python3
"""
Script para reemplazar textos hardcoded en ascendant_profile_screen.dart
con llamadas a AppLocalizations
"""

import re

file_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/ascendant_profile_screen.dart"

# Lista de reemplazos: (texto_antiguo, key_nueva, nota)
replacements = [
    ("'Calculating your rising sign...'", "AppLocalizations.of(context)!.calculatingRisingSign", "Línea ~174"),
    ("'Unable to load ascendant data'", "AppLocalizations.of(context)!.unableToLoadAscendantData", "Línea ~192"),
    ("'Please complete your birth data in Settings'", "AppLocalizations.of(context)!.completeBirthDataInSettings", "Línea ~201"),
    ("'Go Back'", "AppLocalizations.of(context)!.goBack", "Línea ~209"),
    ("'Your Rising Sign'", "AppLocalizations.of(context)!.yourRisingSign", "Línea ~266"),
    ("'Rising Sign (Ascendant)'", "AppLocalizations.of(context)!.risingSignAscendant", "Línea ~360"),
    ("'About Your Ascendant'", "AppLocalizations.of(context)!.aboutYourAscendant", "Línea ~384"),
    ("'Personality Traits'", "AppLocalizations.of(context)!.personalityTraits", "Línea ~417"),
    ("'Physical Presence'", "AppLocalizations.of(context)!.physicalPresence", "Línea ~450"),
    ("'First Impression'", "AppLocalizations.of(context)!.firstImpression", "Línea ~483"),
    ("'Your Strengths'", "AppLocalizations.of(context)!.yourStrengths", "Línea ~516"),
    ("'Growth Areas'", "AppLocalizations.of(context)!.growthAreas", "Línea ~549"),
    ("'Career Path'", "AppLocalizations.of(context)!.careerPath", "Línea ~582"),
    ("'Solar Energy Analysis'", "AppLocalizations.of(context)!.solarEnergyAnalysis", "Línea ~622"),
    ("'Today\\'s Guidance'", "AppLocalizations.of(context)!.todaysGuidance", "Línea ~677"),
    ("\"Today's Guidance\"", "AppLocalizations.of(context)!.todaysGuidance", "Línea ~677 (variante)"),
]

print("📝 Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n🔄 Replacing hardcoded texts...")
replacements_made = 0

for old_text, new_text, note in replacements:
    if old_text in content:
        content = content.replace(old_text, new_text)
        print(f"  ✅ Replaced {note}: {old_text[:40]}... → {new_text[:50]}...")
        replacements_made += 1
    else:
        print(f"  ⚠️  Not found {note}: {old_text}")

print(f"\n✍️  Writing back to file...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n🎉 Done! Made {replacements_made} replacements")
print(f"📄 File updated: {file_path}")
