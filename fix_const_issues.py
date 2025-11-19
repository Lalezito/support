#!/usr/bin/env python3
"""
Script para remover 'const' de widgets Text que usan AppLocalizations
"""
import re

file_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/screens/ascendant_profile_screen.dart"

print("📝 Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n🔄 Fixing const issues...")

# Pattern to find: const Text( followed by AppLocalizations
# Replace: Text( (without const)
fixes_made = 0

# Fix pattern: "const Text(\n                AppLocalizations"
pattern1 = r'const Text\(\s+AppLocalizations'
replacement1 = r'Text(\n                AppLocalizations'
matches1 = len(re.findall(pattern1, content))
if matches1 > 0:
    content = re.sub(pattern1, replacement1, content)
    print(f"  ✅ Fixed {matches1} occurrences of 'const Text(' with AppLocalizations")
    fixes_made += matches1

# Also fix cases where const is inline
pattern2 = r'const Text\(AppLocalizations'
replacement2 = r'Text(AppLocalizations'
matches2 = len(re.findall(pattern2, content))
if matches2 > 0:
    content = re.sub(pattern2, replacement2, content)
    print(f"  ✅ Fixed {matches2} occurrences of inline 'const Text(AppLocalizations'")
    fixes_made += matches2

# Fix TextStyle to be const when used with non-const Text
# Change: style: TextStyle( → style: const TextStyle(
# But only where Text is not const anymore
pattern3 = r'(Text\(\s+AppLocalizations[^)]+\),\s+style:\s+)TextStyle\('
replacement3 = r'\1const TextStyle('
matches3 = len(re.findall(pattern3, content))
if matches3 > 0:
    content = re.sub(pattern3, replacement3, content)
    print(f"  ✅ Added const to {matches3} TextStyle occurrences")
    fixes_made += matches3

print(f"\n✍️  Writing back to file...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n🎉 Done! Made {fixes_made} fixes")
print(f"📄 File updated: {file_path}")
