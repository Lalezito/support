#!/usr/bin/env dart
/// Dart Translation Validation Script
/// ===================================
/// Validates translation files for consistency, quality, and completeness.
///
/// Usage:
///   dart run scripts/validate_translations.dart [--verbose] [--strict]
///
/// Options:
///   --verbose    Show detailed validation output
///   --strict     Fail on warnings (not just errors)
///
/// Author: Claude Code Agent
/// Date: October 15, 2025

import 'dart:io';
import 'dart:convert';

// ANSI Color Codes
const String colorReset = '\x1B[0m';
const String colorGreen = '\x1B[92m';
const String colorYellow = '\x1B[93m';
const String colorRed = '\x1B[91m';
const String colorBlue = '\x1B[94m';
const String colorCyan = '\x1B[96m';
const String colorBold = '\x1B[1m';

class ValidationResult {
  final String category;
  final String level; // 'error', 'warning', 'info'
  final String message;
  final String? file;

  ValidationResult({
    required this.category,
    required this.level,
    required this.message,
    this.file,
  });
}

class TranslationValidator {
  final bool verbose;
  final bool strict;
  final List<ValidationResult> results = [];
  final Map<String, int> stats = {
    'errors': 0,
    'warnings': 0,
    'info': 0,
    'files_checked': 0,
  };

  final List<String> languages = ['en', 'es', 'de', 'fr', 'it', 'pt'];
  final Map<String, Map<String, dynamic>> translations = {};

  TranslationValidator({this.verbose = false, this.strict = false});

  void log(String message, {String color = colorReset, bool bold = false}) {
    final prefix = bold ? colorBold : '';
    stdout.writeln('$prefix$color$message$colorReset');
  }

  void addResult(String category, String level, String message, {String? file}) {
    results.add(ValidationResult(
      category: category,
      level: level,
      message: message,
      file: file,
    ));

    if (level == 'error') stats['errors'] = (stats['errors'] ?? 0) + 1;
    if (level == 'warning') stats['warnings'] = (stats['warnings'] ?? 0) + 1;
    if (level == 'info') stats['info'] = (stats['info'] ?? 0) + 1;

    if (verbose || level == 'error') {
      final icon = level == 'error' ? '✗' : level == 'warning' ? '⚠' : 'ℹ';
      final color = level == 'error' ? colorRed : level == 'warning' ? colorYellow : colorBlue;
      log('  $icon $message', color: color);
    }
  }

  Future<void> loadTranslations() async {
    log('\nLoading translation files...', color: colorCyan, bold: true);

    final l10nDir = Directory('zodiac_app/assets/l10n');
    if (!l10nDir.existsSync()) {
      log('Error: l10n directory not found', color: colorRed);
      exit(1);
    }

    for (final lang in languages) {
      final file = File('${l10nDir.path}/app_$lang.arb');
      if (!file.existsSync()) {
        addResult('Files', 'error', 'Missing translation file: app_$lang.arb');
        continue;
      }

      try {
        final contents = await file.readAsString();
        final data = jsonDecode(contents) as Map<String, dynamic>;
        translations[lang] = data;
        stats['files_checked'] = (stats['files_checked'] ?? 0) + 1;
        log('  Loaded: app_$lang.arb (${data.length} keys)', color: colorGreen);
      } catch (e) {
        addResult('Files', 'error', 'Failed to parse app_$lang.arb: $e', file: 'app_$lang.arb');
      }
    }
  }

  void validateKeyParity() {
    log('\nValidating key parity across languages...', color: colorCyan, bold: true);

    if (!translations.containsKey('en')) {
      addResult('Parity', 'error', 'English base file not loaded');
      return;
    }

    final enKeys = translations['en']!.keys.where((k) => !k.startsWith('@')).toSet();

    for (final lang in languages) {
      if (lang == 'en' || !translations.containsKey(lang)) continue;

      final langKeys = translations[lang]!.keys.where((k) => !k.startsWith('@')).toSet();

      // Check for missing keys
      final missing = enKeys.difference(langKeys);
      if (missing.isNotEmpty) {
        addResult(
          'Parity',
          'warning',
          '$lang missing ${missing.length} keys: ${missing.take(5).join(", ")}${missing.length > 5 ? "..." : ""}',
          file: 'app_$lang.arb',
        );
      }

      // Check for extra keys
      final extra = langKeys.difference(enKeys);
      if (extra.isNotEmpty) {
        addResult(
          'Parity',
          'warning',
          '$lang has ${extra.length} extra keys: ${extra.take(5).join(", ")}${extra.length > 5 ? "..." : ""}',
          file: 'app_$lang.arb',
        );
      }

      // Success case
      if (missing.isEmpty && extra.isEmpty) {
        addResult('Parity', 'info', '$lang has perfect key parity', file: 'app_$lang.arb');
      }
    }
  }

  void validateNamingConventions() {
    log('\nValidating naming conventions...', color: colorCyan, bold: true);

    if (!translations.containsKey('en')) return;

    final conventions = <String, int>{
      'camelCase': 0,
      'snake_case': 0,
      'lowercase': 0,
      'mixed': 0,
    };

    final problematicKeys = <String>[];

    for (final key in translations['en']!.keys) {
      if (key.startsWith('@')) continue;

      // Analyze naming pattern
      if (key.contains('_') && key.contains(RegExp(r'[A-Z]'))) {
        conventions['mixed'] = (conventions['mixed'] ?? 0) + 1;
        problematicKeys.add(key);
      } else if (key.contains('_')) {
        conventions['snake_case'] = (conventions['snake_case'] ?? 0) + 1;
      } else if (key.contains(RegExp(r'[A-Z]'))) {
        conventions['camelCase'] = (conventions['camelCase'] ?? 0) + 1;
      } else {
        conventions['lowercase'] = (conventions['lowercase'] ?? 0) + 1;
      }
    }

    // Report mixed convention keys
    if (problematicKeys.isNotEmpty) {
      addResult(
        'Naming',
        'warning',
        'Found ${problematicKeys.length} keys with mixed naming (snake_case + camelCase): ${problematicKeys.take(5).join(", ")}',
        file: 'app_en.arb',
      );
    }

    // Report convention distribution
    log('\n  Naming Convention Distribution:', color: colorCyan);
    conventions.forEach((convention, count) {
      final percentage = (count / translations['en']!.length * 100).toStringAsFixed(1);
      log('    $convention: $count ($percentage%)', color: colorBlue);
    });

    // Recommendation
    final total = translations['en']!.length;
    final camelCasePercentage = ((conventions['camelCase'] ?? 0) / total * 100);
    if (camelCasePercentage > 60) {
      addResult('Naming', 'info', 'Recommend standardizing to camelCase (already $camelCasePercentage% coverage)');
    }
  }

  void validateEnglishInTranslations() {
    log('\nChecking for English text in non-English files...', color: colorCyan, bold: true);

    final englishIndicators = [
      'the', 'and', 'or', 'but', 'your', 'you', 'with', 'this', 'that',
      'have', 'from', 'they', 'been', 'which', 'their', 'about', 'more'
    ];

    for (final lang in languages) {
      if (lang == 'en' || !translations.containsKey(lang)) continue;

      int suspiciousCount = 0;
      final suspiciousKeys = <String>[];

      translations[lang]!.forEach((key, value) {
        if (key.startsWith('@') || value is! String) return;

        final lowerValue = value.toString().toLowerCase();
        final englishWords = englishIndicators.where(
          (word) => RegExp(r'\b' + word + r'\b').hasMatch(lowerValue)
        ).length;

        if (englishWords >= 3) {
          suspiciousCount++;
          if (suspiciousKeys.length < 5) {
            suspiciousKeys.add('$key: "${value.toString().substring(0, value.toString().length > 50 ? 50 : value.toString().length)}..."');
          }
        }
      });

      if (suspiciousCount > 0) {
        addResult(
          'Quality',
          'warning',
          '$lang has $suspiciousCount keys with potential English text',
          file: 'app_$lang.arb',
        );
        if (verbose && suspiciousKeys.isNotEmpty) {
          log('    Examples:', color: colorYellow);
          for (final example in suspiciousKeys) {
            log('      - $example', color: colorYellow);
          }
        }
      } else {
        addResult('Quality', 'info', '$lang appears to have proper translations', file: 'app_$lang.arb');
      }
    }
  }

  void validateTranslationPlaceholders() {
    log('\nChecking for [TRANSLATE] placeholders...', color: colorCyan, bold: true);

    for (final lang in languages) {
      if (lang == 'en' || !translations.containsKey(lang)) continue;

      final placeholders = <String>[];

      translations[lang]!.forEach((key, value) {
        if (key.startsWith('@') || value is! String) return;

        if (value.toString().contains('[TRANSLATE]')) {
          placeholders.add(key);
        }
      });

      if (placeholders.isNotEmpty) {
        addResult(
          'Completeness',
          'warning',
          '$lang has ${placeholders.length} untranslated placeholders: ${placeholders.take(5).join(", ")}${placeholders.length > 5 ? "..." : ""}',
          file: 'app_$lang.arb',
        );
      } else {
        addResult('Completeness', 'info', '$lang has no translation placeholders', file: 'app_$lang.arb');
      }
    }
  }

  void calculateTranslationQuality() {
    log('\nCalculating translation quality scores...', color: colorCyan, bold: true);

    if (!translations.containsKey('en')) return;

    final enKeyCount = translations['en']!.keys.where((k) => !k.startsWith('@')).length;

    for (final lang in languages) {
      if (lang == 'en' || !translations.containsKey(lang)) continue;

      final langData = translations[lang]!;
      final langKeyCount = langData.keys.where((k) => !k.startsWith('@')).length;

      // Calculate metrics
      final coverage = (langKeyCount / enKeyCount * 100);
      int placeholderCount = 0;
      int suspiciousCount = 0;

      langData.forEach((key, value) {
        if (key.startsWith('@') || value is! String) return;

        if (value.toString().contains('[TRANSLATE]')) placeholderCount++;

        // Simple heuristic for untranslated content
        if (lang != 'en' && value.toString() == translations['en']?[key]) {
          suspiciousCount++;
        }
      });

      final qualityScore = coverage - (placeholderCount / langKeyCount * 100) - (suspiciousCount / langKeyCount * 50);

      final scoreColor = qualityScore >= 95 ? colorGreen : qualityScore >= 85 ? colorYellow : colorRed;
      log('  $lang: ${qualityScore.toStringAsFixed(1)}% quality score', color: scoreColor);
      log('    - Coverage: ${coverage.toStringAsFixed(1)}%', color: colorBlue);
      log('    - Placeholders: $placeholderCount', color: colorBlue);
      log('    - Suspicious: $suspiciousCount', color: colorBlue);

      if (qualityScore < 85) {
        addResult(
          'Quality',
          'warning',
          '$lang quality score is below 85% (${qualityScore.toStringAsFixed(1)}%)',
          file: 'app_$lang.arb',
        );
      }
    }
  }

  void printSummary() {
    log('\n${"=" * 80}', color: colorCyan);
    log('Validation Summary', color: colorCyan, bold: true);
    log('${"=" * 80}', color: colorCyan);

    log('\nFiles checked:  ${stats["files_checked"]}', color: colorGreen);
    log('Errors:         ${stats["errors"]}', color: stats["errors"]! > 0 ? colorRed : colorGreen);
    log('Warnings:       ${stats["warnings"]}', color: stats["warnings"]! > 0 ? colorYellow : colorGreen);
    log('Info:           ${stats["info"]}', color: colorBlue);

    if (results.isNotEmpty && !verbose) {
      log('\nTop Issues:', color: colorYellow);
      final topIssues = results.where((r) => r.level == 'error' || r.level == 'warning').take(10);
      for (final issue in topIssues) {
        final icon = issue.level == 'error' ? '✗' : '⚠';
        final color = issue.level == 'error' ? colorRed : colorYellow;
        log('  $icon [${issue.category}] ${issue.message}', color: color);
      }
    }

    log('\n${"=" * 80}\n', color: colorCyan);

    // Exit code
    if (stats['errors']! > 0) {
      log('FAILED: Translation validation found errors', color: colorRed, bold: true);
      exit(1);
    } else if (strict && stats['warnings']! > 0) {
      log('FAILED: Translation validation found warnings (strict mode)', color: colorYellow, bold: true);
      exit(1);
    } else {
      log('SUCCESS: All validations passed', color: colorGreen, bold: true);
      exit(0);
    }
  }

  Future<void> run() async {
    log('${"=" * 80}', color: colorCyan);
    log('Translation Validation Script', color: colorCyan, bold: true);
    log('${"=" * 80}', color: colorCyan);

    if (strict) {
      log('\n[STRICT MODE] Warnings will be treated as errors', color: colorYellow, bold: true);
    }

    await loadTranslations();

    if (translations.isEmpty) {
      log('\nNo translations loaded. Exiting.', color: colorRed);
      exit(1);
    }

    validateKeyParity();
    validateNamingConventions();
    validateEnglishInTranslations();
    validateTranslationPlaceholders();
    calculateTranslationQuality();

    printSummary();
  }
}

void main(List<String> arguments) async {
  final verbose = arguments.contains('--verbose') || arguments.contains('-v');
  final strict = arguments.contains('--strict') || arguments.contains('-s');

  final validator = TranslationValidator(verbose: verbose, strict: strict);

  try {
    await validator.run();
  } catch (e) {
    stderr.writeln('${colorRed}${colorBold}Fatal error: $e$colorReset');
    exit(1);
  }
}
