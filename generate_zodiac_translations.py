#!/usr/bin/env python3
"""
Generate complete zodiac_specific_goal_translations.dart file
with all 2,304 translations (384 texts × 6 languages)
"""

import re
from pathlib import Path

# File paths
BASE_DIR = Path("/Users/alejandrocaceres/Desktop/appstore.zodia")
TRANSLATION_FILES = {
    'en': BASE_DIR / "ZODIAC_CANONICAL_TEXTS_ENGLISH_NOV17.md",
    'es': BASE_DIR / "ZODIAC_TRANSLATIONS_ES_NOV17.md",
    'pt': BASE_DIR / "ZODIAC_TRANSLATIONS_PT_NOV17.md",
    'fr': BASE_DIR / "ZODIAC_TRANSLATIONS_FR_NOV17.md",
    'de': BASE_DIR / "ZODIAC_TRANSLATIONS_DE_NOV17.md",
    'it': BASE_DIR / "ZODIAC_TRANSLATIONS_IT_NOV17.md",
}
OUTPUT_FILE = BASE_DIR / "zodiac_app/lib/services/cosmic_coach/zodiac_specific_goal_translations.dart"

# Zodiac signs in order
SIGNS = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
         'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

def escape_dart_string(s):
    """Escape single quotes and backslashes for Dart strings"""
    return s.replace('\\', '\\\\').replace("'", "\\'")

def parse_translation_file(filepath):
    """Parse a translation markdown file and extract all texts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    translations = {}

    # Extract all ID-text pairs
    # Pattern: **SHADOW_001** [label]\n```\nText here\n```
    pattern = r'\*\*([A-Z_0-9]+)\*\*\s*\[.*?\]\s*```\s*(.+?)\s*```'
    matches = re.findall(pattern, content, re.DOTALL)

    for text_id, text in matches:
        # Clean up the text
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        translations[text_id] = text

    return translations

def get_shadow_work_data(sign_index, lang_code, translations):
    """Get shadow work goal data for a sign"""
    base_id = sign_index * 12  # 12 fields per sign

    title = translations.get(f'SHADOW_{base_id+1:03d}', '')
    description = translations.get(f'SHADOW_{base_id+2:03d}', '')
    habit_1 = translations.get(f'SHADOW_{base_id+3:03d}', '')
    when_1 = translations.get(f'SHADOW_{base_id+4:03d}', '')
    why_1 = translations.get(f'SHADOW_{base_id+5:03d}', '')
    habit_2 = translations.get(f'SHADOW_{base_id+6:03d}', '')
    when_2 = translations.get(f'SHADOW_{base_id+7:03d}', '')
    why_2 = translations.get(f'SHADOW_{base_id+8:03d}', '')
    success_1 = translations.get(f'SHADOW_{base_id+9:03d}', '')
    success_2 = translations.get(f'SHADOW_{base_id+10:03d}', '')
    success_3 = translations.get(f'SHADOW_{base_id+11:03d}', '')
    motivation = translations.get(f'SHADOW_{base_id+12:03d}', '')

    return {
        'title': escape_dart_string(title),
        'description': escape_dart_string(description),
        'habit_1': escape_dart_string(habit_1),
        'when_1': escape_dart_string(when_1),
        'why_1': escape_dart_string(why_1),
        'habit_2': escape_dart_string(habit_2),
        'when_2': escape_dart_string(when_2),
        'why_2': escape_dart_string(why_2),
        'success_1': escape_dart_string(success_1),
        'success_2': escape_dart_string(success_2),
        'success_3': escape_dart_string(success_3),
        'motivation': escape_dart_string(motivation),
    }

def get_superpower_data(sign_index, lang_code, translations):
    """Get superpower goal data for a sign"""
    base_id = sign_index * 12

    title = translations.get(f'POWER_{base_id+1:03d}', '')
    description = translations.get(f'POWER_{base_id+2:03d}', '')
    habit_1 = translations.get(f'POWER_{base_id+3:03d}', '')
    when_1 = translations.get(f'POWER_{base_id+4:03d}', '')
    why_1 = translations.get(f'POWER_{base_id+5:03d}', '')
    habit_2 = translations.get(f'POWER_{base_id+6:03d}', '')
    when_2 = translations.get(f'POWER_{base_id+7:03d}', '')
    why_2 = translations.get(f'POWER_{base_id+8:03d}', '')
    success_1 = translations.get(f'POWER_{base_id+9:03d}', '')
    success_2 = translations.get(f'POWER_{base_id+10:03d}', '')
    success_3 = translations.get(f'POWER_{base_id+11:03d}', '')
    motivation = translations.get(f'POWER_{base_id+12:03d}', '')

    return {
        'title': escape_dart_string(title),
        'description': escape_dart_string(description),
        'habit_1': escape_dart_string(habit_1),
        'when_1': escape_dart_string(when_1),
        'why_1': escape_dart_string(why_1),
        'habit_2': escape_dart_string(habit_2),
        'when_2': escape_dart_string(when_2),
        'why_2': escape_dart_string(why_2),
        'success_1': escape_dart_string(success_1),
        'success_2': escape_dart_string(success_2),
        'success_3': escape_dart_string(success_3),
        'motivation': escape_dart_string(motivation),
    }

def get_micro_habits_data(sign_index, lang_code, translations):
    """Get micro-habits data for a sign"""
    base_id = sign_index * 8  # 8 fields per sign

    habit_1 = translations.get(f'HABIT_{base_id+1:03d}', '')
    when_1 = translations.get(f'HABIT_{base_id+2:03d}', '')
    why_1 = translations.get(f'HABIT_{base_id+3:03d}', '')
    category_1 = translations.get(f'HABIT_{base_id+4:03d}', '')
    habit_2 = translations.get(f'HABIT_{base_id+5:03d}', '')
    when_2 = translations.get(f'HABIT_{base_id+6:03d}', '')
    why_2 = translations.get(f'HABIT_{base_id+7:03d}', '')
    category_2 = translations.get(f'HABIT_{base_id+8:03d}', '')

    return {
        'habit_1': escape_dart_string(habit_1),
        'when_1': escape_dart_string(when_1),
        'why_1': escape_dart_string(why_1),
        'category_1': escape_dart_string(category_1),
        'habit_2': escape_dart_string(habit_2),
        'when_2': escape_dart_string(when_2),
        'why_2': escape_dart_string(why_2),
        'category_2': escape_dart_string(category_2),
    }

def generate_shadow_function(sign, sign_index, all_translations):
    """Generate a complete shadow work function for a sign"""
    lines = []
    lines.append(f"  static Map<String, dynamic> _{sign}ShadowGoal(String lang) {{")
    lines.append("    switch (lang) {")

    # Generate all 6 language cases
    for lang_code in ['es', 'pt', 'fr', 'de', 'it']:
        data = get_shadow_work_data(sign_index, lang_code, all_translations[lang_code])

        lines.append(f"      case '{lang_code}':")
        lines.append("        return {")
        lines.append(f"          'title': '{data['title']}',")
        lines.append(f"          'description': '{data['description']}',")
        lines.append("          'category': 'shadow_work',")
        lines.append("          'difficulty': 'medium',")
        lines.append("          'microHabits': [")
        lines.append("            {")
        lines.append(f"              'habit': '{data['habit_1']}',")
        lines.append(f"              'when': '{data['when_1']}',")
        lines.append(f"              'why': '{data['why_1']}',")
        lines.append("            },")
        lines.append("            {")
        lines.append(f"              'habit': '{data['habit_2']}',")
        lines.append(f"              'when': '{data['when_2']}',")
        lines.append(f"              'why': '{data['why_2']}',")
        lines.append("            },")
        lines.append("          ],")
        lines.append("          'successIndicators': [")
        lines.append(f"            '{data['success_1']}',")
        lines.append(f"            '{data['success_2']}',")
        lines.append(f"            '{data['success_3']}',")
        lines.append("          ],")
        lines.append(f"          'motivation': '{data['motivation']}',")
        lines.append("        };")
        lines.append("")

    # English (default)
    data = get_shadow_work_data(sign_index, 'en', all_translations['en'])
    lines.append("      default: // English")
    lines.append("        return {")
    lines.append(f"          'title': '{data['title']}',")
    lines.append(f"          'description': '{data['description']}',")
    lines.append("          'category': 'shadow_work',")
    lines.append("          'difficulty': 'medium',")
    lines.append("          'microHabits': [")
    lines.append("            {")
    lines.append(f"              'habit': '{data['habit_1']}',")
    lines.append(f"              'when': '{data['when_1']}',")
    lines.append(f"              'why': '{data['why_1']}',")
    lines.append("            },")
    lines.append("            {")
    lines.append(f"              'habit': '{data['habit_2']}',")
    lines.append(f"              'when': '{data['when_2']}',")
    lines.append(f"              'why': '{data['why_2']}',")
    lines.append("            },")
    lines.append("          ],")
    lines.append("          'successIndicators': [")
    lines.append(f"            '{data['success_1']}',")
    lines.append(f"            '{data['success_2']}',")
    lines.append(f"            '{data['success_3']}',")
    lines.append("          ],")
    lines.append(f"          'motivation': '{data['motivation']}',")
    lines.append("        };")
    lines.append("    }")
    lines.append("  }")

    return '\n'.join(lines)

def generate_superpower_function(sign, sign_index, all_translations):
    """Generate a complete superpower function for a sign"""
    lines = []
    lines.append(f"  static Map<String, dynamic> _{sign}SuperpowerGoal(String lang) {{")
    lines.append("    switch (lang) {")

    for lang_code in ['es', 'pt', 'fr', 'de', 'it']:
        data = get_superpower_data(sign_index, lang_code, all_translations[lang_code])

        lines.append(f"      case '{lang_code}':")
        lines.append("        return {")
        lines.append(f"          'title': '{data['title']}',")
        lines.append(f"          'description': '{data['description']}',")
        lines.append("          'category': 'superpower',")
        lines.append("          'difficulty': 'medium',")
        lines.append("          'microHabits': [")
        lines.append("            {")
        lines.append(f"              'habit': '{data['habit_1']}',")
        lines.append(f"              'when': '{data['when_1']}',")
        lines.append(f"              'why': '{data['why_1']}',")
        lines.append("            },")
        lines.append("            {")
        lines.append(f"              'habit': '{data['habit_2']}',")
        lines.append(f"              'when': '{data['when_2']}',")
        lines.append(f"              'why': '{data['why_2']}',")
        lines.append("            },")
        lines.append("          ],")
        lines.append("          'successIndicators': [")
        lines.append(f"            '{data['success_1']}',")
        lines.append(f"            '{data['success_2']}',")
        lines.append(f"            '{data['success_3']}',")
        lines.append("          ],")
        lines.append(f"          'motivation': '{data['motivation']}',")
        lines.append("        };")
        lines.append("")

    # English (default)
    data = get_superpower_data(sign_index, 'en', all_translations['en'])
    lines.append("      default: // English")
    lines.append("        return {")
    lines.append(f"          'title': '{data['title']}',")
    lines.append(f"          'description': '{data['description']}',")
    lines.append("          'category': 'superpower',")
    lines.append("          'difficulty': 'medium',")
    lines.append("          'microHabits': [")
    lines.append("            {")
    lines.append(f"              'habit': '{data['habit_1']}',")
    lines.append(f"              'when': '{data['when_1']}',")
    lines.append(f"              'why': '{data['why_1']}',")
    lines.append("            },")
    lines.append("            {")
    lines.append(f"              'habit': '{data['habit_2']}',")
    lines.append(f"              'when': '{data['when_2']}',")
    lines.append(f"              'why': '{data['why_2']}',")
    lines.append("            },")
    lines.append("          ],")
    lines.append("          'successIndicators': [")
    lines.append(f"            '{data['success_1']}',")
    lines.append(f"            '{data['success_2']}',")
    lines.append(f"            '{data['success_3']}',")
    lines.append("          ],")
    lines.append(f"          'motivation': '{data['motivation']}',")
    lines.append("        };")
    lines.append("    }")
    lines.append("  }")

    return '\n'.join(lines)

def generate_micro_habits_function(sign, sign_index, all_translations):
    """Generate a complete micro-habits function for a sign"""
    lines = []
    lines.append(f"  static List<Map<String, dynamic>> _{sign}MicroHabits(String lang) {{")
    lines.append("    switch (lang) {")

    for lang_code in ['es', 'pt', 'fr', 'de', 'it']:
        data = get_micro_habits_data(sign_index, lang_code, all_translations[lang_code])

        lines.append(f"      case '{lang_code}':")
        lines.append("        return [")
        lines.append("          {")
        lines.append(f"            'habit': '{data['habit_1']}',")
        lines.append(f"            'when': '{data['when_1']}',")
        lines.append(f"            'why': '{data['why_1']}',")
        lines.append(f"            'category': '{data['category_1']}',")
        lines.append("          },")
        lines.append("          {")
        lines.append(f"            'habit': '{data['habit_2']}',")
        lines.append(f"            'when': '{data['when_2']}',")
        lines.append(f"            'why': '{data['why_2']}',")
        lines.append(f"            'category': '{data['category_2']}',")
        lines.append("          },")
        lines.append("        ];")
        lines.append("")

    # English (default)
    data = get_micro_habits_data(sign_index, 'en', all_translations['en'])
    lines.append("      default: // English")
    lines.append("        return [")
    lines.append("          {")
    lines.append(f"            'habit': '{data['habit_1']}',")
    lines.append(f"            'when': '{data['when_1']}',")
    lines.append(f"            'why': '{data['why_1']}',")
    lines.append(f"            'category': '{data['category_1']}',")
    lines.append("          },")
    lines.append("          {")
    lines.append(f"            'habit': '{data['habit_2']}',")
    lines.append(f"            'when': '{data['when_2']}',")
    lines.append(f"            'why': '{data['why_2']}',")
    lines.append(f"            'category': '{data['category_2']}',")
    lines.append("          },")
    lines.append("        ];")
    lines.append("    }")
    lines.append("  }")

    return '\n'.join(lines)

def main():
    print("🚀 Starting generation of zodiac_specific_goal_translations.dart")
    print(f"📁 Output: {OUTPUT_FILE}")

    # Parse all translation files
    print("\n📖 Parsing translation files...")
    all_translations = {}
    for lang_code, filepath in TRANSLATION_FILES.items():
        print(f"  - Loading {lang_code.upper()}: {filepath.name}")
        all_translations[lang_code] = parse_translation_file(filepath)
        print(f"    ✓ Found {len(all_translations[lang_code])} translations")

    # Generate file header
    dart_code = """// ignore_for_file: lines_longer_than_80_chars

/// Zodiac-specific goal translations
/// Generated by multiagent system - Nov 17, 2025
///
/// Supports 6 languages: EN, ES, PT, FR, DE, IT
/// Total translations: 2,304 (384 texts × 6 idiomas)
///
/// Usage:
/// ```dart
/// final shadowGoal = ZodiacSpecificGoalTranslations.getShadowWorkGoal('aries', 'es');
/// final superpowerGoal = ZodiacSpecificGoalTranslations.getSuperpowerGoal('taurus', 'pt');
/// final microHabits = ZodiacSpecificGoalTranslations.getMicroHabits('gemini', 'fr');
/// ```
class ZodiacSpecificGoalTranslations {

  // ======================
  // SHADOW WORK GOALS (12 signos)
  // ======================

  /// Returns a shadow work goal for the given zodiac sign and language
  ///
  /// Parameters:
  /// - [zodiacSign]: Sign name (case-insensitive, supports variants)
  /// - [languageCode]: 'en', 'es', 'pt', 'fr', 'de', 'it'
  static Map<String, dynamic> getShadowWorkGoal(
    String zodiacSign,
    String languageCode,
  ) {
    final sign = zodiacSign.toLowerCase();

    switch (sign) {
      case 'aries':
      case 'widder':
      case 'bélier':
      case 'ariete':
      case 'áries':
        return _ariesShadowGoal(languageCode);

      case 'taurus':
      case 'tauro':
      case 'stier':
      case 'taureau':
      case 'toro':
      case 'touro':
        return _taurusShadowGoal(languageCode);

      case 'gemini':
      case 'géminis':
      case 'gêmeos':
      case 'gémeaux':
      case 'zwillinge':
      case 'gemelli':
        return _geminiShadowGoal(languageCode);

      case 'cancer':
      case 'cáncer':
      case 'cancro':
      case 'krebs':
        return _cancerShadowGoal(languageCode);

      case 'leo':
      case 'león':
      case 'leão':
      case 'lion':
      case 'löwe':
      case 'leone':
        return _leoShadowGoal(languageCode);

      case 'virgo':
      case 'virgem':
      case 'vierge':
      case 'jungfrau':
      case 'vergine':
        return _virgoShadowGoal(languageCode);

      case 'libra':
      case 'balance':
      case 'balança':
      case 'waage':
      case 'bilancia':
        return _libraShadowGoal(languageCode);

      case 'scorpio':
      case 'escorpio':
      case 'escorpião':
      case 'scorpion':
      case 'skorpion':
      case 'scorpione':
        return _scorpioShadowGoal(languageCode);

      case 'sagittarius':
      case 'sagitario':
      case 'sagitário':
      case 'sagittaire':
      case 'schütze':
        return _sagittariusShadowGoal(languageCode);

      case 'capricorn':
      case 'capricornio':
      case 'capricórnio':
      case 'capricorne':
      case 'steinbock':
        return _capricornShadowGoal(languageCode);

      case 'aquarius':
      case 'acuario':
      case 'aquário':
      case 'verseau':
      case 'wassermann':
      case 'acquario':
        return _aquariusShadowGoal(languageCode);

      case 'pisces':
      case 'piscis':
      case 'peixes':
      case 'poissons':
      case 'fische':
      case 'pesci':
        return _piscesShadowGoal(languageCode);

      default:
        return _ariesShadowGoal(languageCode);
    }
  }

"""

    # Generate all 12 shadow work functions
    print("\n🌑 Generating Shadow Work goals (12 signs × 6 languages)...")
    for i, sign in enumerate(SIGNS):
        print(f"  - {sign.capitalize()}")
        dart_code += "\n  // --- " + sign.capitalize() + " Shadow Work ---\n"
        dart_code += generate_shadow_function(sign, i, all_translations) + "\n"

    # Add superpower goals section
    dart_code += """
  // ======================
  // SUPERPOWER GOALS (12 signos)
  // ======================

  /// Returns a superpower goal for the given zodiac sign and language
  ///
  /// Parameters:
  /// - [zodiacSign]: Sign name (case-insensitive, supports variants)
  /// - [languageCode]: 'en', 'es', 'pt', 'fr', 'de', 'it'
  static Map<String, dynamic> getSuperpowerGoal(
    String zodiacSign,
    String languageCode,
  ) {
    final sign = zodiacSign.toLowerCase();

    switch (sign) {
      case 'aries':
      case 'widder':
      case 'bélier':
      case 'ariete':
      case 'áries':
        return _ariesSuperpowerGoal(languageCode);

      case 'taurus':
      case 'tauro':
      case 'stier':
      case 'taureau':
      case 'toro':
      case 'touro':
        return _taurusSuperpowerGoal(languageCode);

      case 'gemini':
      case 'géminis':
      case 'gêmeos':
      case 'gémeaux':
      case 'zwillinge':
      case 'gemelli':
        return _geminiSuperpowerGoal(languageCode);

      case 'cancer':
      case 'cáncer':
      case 'cancro':
      case 'krebs':
        return _cancerSuperpowerGoal(languageCode);

      case 'leo':
      case 'león':
      case 'leão':
      case 'lion':
      case 'löwe':
      case 'leone':
        return _leoSuperpowerGoal(languageCode);

      case 'virgo':
      case 'virgem':
      case 'vierge':
      case 'jungfrau':
      case 'vergine':
        return _virgoSuperpowerGoal(languageCode);

      case 'libra':
      case 'balance':
      case 'balança':
      case 'waage':
      case 'bilancia':
        return _libraSuperpowerGoal(languageCode);

      case 'scorpio':
      case 'escorpio':
      case 'escorpião':
      case 'scorpion':
      case 'skorpion':
      case 'scorpione':
        return _scorpioSuperpowerGoal(languageCode);

      case 'sagittarius':
      case 'sagitario':
      case 'sagitário':
      case 'sagittaire':
      case 'schütze':
        return _sagittariusSuperpowerGoal(languageCode);

      case 'capricorn':
      case 'capricornio':
      case 'capricórnio':
      case 'capricorne':
      case 'steinbock':
        return _capricornSuperpowerGoal(languageCode);

      case 'aquarius':
      case 'acuario':
      case 'aquário':
      case 'verseau':
      case 'wassermann':
      case 'acquario':
        return _aquariusSuperpowerGoal(languageCode);

      case 'pisces':
      case 'piscis':
      case 'peixes':
      case 'poissons':
      case 'fische':
      case 'pesci':
        return _piscesSuperpowerGoal(languageCode);

      default:
        return _ariesSuperpowerGoal(languageCode);
    }
  }

"""

    # Generate all 12 superpower functions
    print("\n⭐ Generating Superpower goals (12 signs × 6 languages)...")
    for i, sign in enumerate(SIGNS):
        print(f"  - {sign.capitalize()}")
        dart_code += "\n  // --- " + sign.capitalize() + " Superpower ---\n"
        dart_code += generate_superpower_function(sign, i, all_translations) + "\n"

    # Add micro-habits section
    dart_code += """
  // ======================
  // MICRO-HABITS (12 signos)
  // ======================

  /// Returns micro-habits for the given zodiac sign and language
  ///
  /// Parameters:
  /// - [zodiacSign]: Sign name (case-insensitive, supports variants)
  /// - [languageCode]: 'en', 'es', 'pt', 'fr', 'de', 'it'
  static List<Map<String, dynamic>> getMicroHabits(
    String zodiacSign,
    String languageCode,
  ) {
    final sign = zodiacSign.toLowerCase();

    switch (sign) {
      case 'aries':
      case 'widder':
      case 'bélier':
      case 'ariete':
      case 'áries':
        return _ariesMicroHabits(languageCode);

      case 'taurus':
      case 'tauro':
      case 'stier':
      case 'taureau':
      case 'toro':
      case 'touro':
        return _taurusMicroHabits(languageCode);

      case 'gemini':
      case 'géminis':
      case 'gêmeos':
      case 'gémeaux':
      case 'zwillinge':
      case 'gemelli':
        return _geminiMicroHabits(languageCode);

      case 'cancer':
      case 'cáncer':
      case 'cancro':
      case 'krebs':
        return _cancerMicroHabits(languageCode);

      case 'leo':
      case 'león':
      case 'leão':
      case 'lion':
      case 'löwe':
      case 'leone':
        return _leoMicroHabits(languageCode);

      case 'virgo':
      case 'virgem':
      case 'vierge':
      case 'jungfrau':
      case 'vergine':
        return _virgoMicroHabits(languageCode);

      case 'libra':
      case 'balance':
      case 'balança':
      case 'waage':
      case 'bilancia':
        return _libraMicroHabits(languageCode);

      case 'scorpio':
      case 'escorpio':
      case 'escorpião':
      case 'scorpion':
      case 'skorpion':
      case 'scorpione':
        return _scorpioMicroHabits(languageCode);

      case 'sagittarius':
      case 'sagitario':
      case 'sagitário':
      case 'sagittaire':
      case 'schütze':
        return _sagittariusMicroHabits(languageCode);

      case 'capricorn':
      case 'capricornio':
      case 'capricórnio':
      case 'capricorne':
      case 'steinbock':
        return _capricornMicroHabits(languageCode);

      case 'aquarius':
      case 'acuario':
      case 'aquário':
      case 'verseau':
      case 'wassermann':
      case 'acquario':
        return _aquariusMicroHabits(languageCode);

      case 'pisces':
      case 'piscis':
      case 'peixes':
      case 'poissons':
      case 'fische':
      case 'pesci':
        return _piscesMicroHabits(languageCode);

      default:
        return _ariesMicroHabits(languageCode);
    }
  }

"""

    # Generate all 12 micro-habits functions
    print("\n🎯 Generating Micro-Habits (12 signs × 6 languages)...")
    for i, sign in enumerate(SIGNS):
        print(f"  - {sign.capitalize()}")
        dart_code += "\n  // --- " + sign.capitalize() + " Micro-Habits ---\n"
        dart_code += generate_micro_habits_function(sign, i, all_translations) + "\n"

    # Close the class
    dart_code += "}\n"

    # Write to file
    print(f"\n💾 Writing to {OUTPUT_FILE}...")
    OUTPUT_FILE.write_text(dart_code, encoding='utf-8')

    # Statistics
    lines = len(dart_code.split('\n'))
    chars = len(dart_code)

    print("\n✅ GENERATION COMPLETE!")
    print(f"📊 Statistics:")
    print(f"  - Total lines: {lines:,}")
    print(f"  - Total characters: {chars:,}")
    print(f"  - Functions generated: 36 (12 signs × 3 types)")
    print(f"  - Languages: 6 (EN, ES, PT, FR, DE, IT)")
    print(f"  - Total translations: 2,304 (384 × 6)")
    print(f"\n📁 File saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
