// ignore_for_file: avoid_print

import 'dart:io';
import 'dart:convert';

/// Comprehensive ARB cleanup script:
/// 1. Removes section marker keys from EN template (not used in code)
/// 2. For non-EN files: removes @metadata, orphaned keys, duplicates
/// 3. Ensures all non-EN files only have keys that exist in EN template
void main() {
  final basePath = 'zodiac_app/assets/l10n';

  // Section markers to remove from EN (not used in code)
  final sectionMarkers = {
    'ai_coach_onboarding',
    'compatibility_8d_onboarding',
    'compatibility_dynamic_content',
    'general_onboarding',
    'onboarding_strings',
    'performance_dashboard_onboarding',
    'predictive_astrology_onboarding',
    'premium_features_onboarding',
    'sign_specific_compatibility',
    'smart_journaling_onboarding',
  };

  // === STEP 1: Clean EN template ===
  print('=== STEP 1: Clean EN template ===');
  final enFile = File('$basePath/app_en.arb');
  final enContent = enFile.readAsStringSync();
  final enEntries = _parseArbPreservingOrder(enContent);

  // Remove section markers and their @metadata
  final cleanedEnEntries = <MapEntry<String, dynamic>>[];
  int removedFromEn = 0;
  for (final entry in enEntries) {
    final key = entry.key;
    if (sectionMarkers.contains(key)) {
      print('  EN: Removed section marker "$key"');
      removedFromEn++;
      continue;
    }
    if (key.startsWith('@') && key != '@@locale') {
      final msgKey = key.substring(1);
      if (sectionMarkers.contains(msgKey)) {
        print('  EN: Removed @metadata for section marker "$msgKey"');
        removedFromEn++;
        continue;
      }
    }
    cleanedEnEntries.add(entry);
  }
  print('Removed $removedFromEn entries from EN\n');

  // Build EN message key set (for validating non-EN files)
  final enMessageKeys = <String>{};
  for (final entry in cleanedEnEntries) {
    if (!entry.key.startsWith('@')) {
      enMessageKeys.add(entry.key);
    }
  }
  print('EN has ${enMessageKeys.length} message keys after cleanup\n');

  // Write cleaned EN
  _writeArbFile(enFile, cleanedEnEntries, 'en', includeMetadata: true);

  // === STEP 2: Clean non-EN files ===
  final languages = ['es', 'fr', 'de', 'it', 'pt'];

  for (final lang in languages) {
    print('=== Cleaning $lang ===');
    final file = File('$basePath/app_$lang.arb');
    if (!file.existsSync()) {
      print('  SKIP: File not found');
      continue;
    }

    final content = file.readAsStringSync();
    final entries = _parseArbPreservingOrder(content);
    print('  Parsed ${entries.length} entries');

    // Track changes
    int removedMetadata = 0;
    int removedOrphaned = 0;
    int removedDuplicates = 0;
    final seen = <String>{};
    final cleanedEntries = <MapEntry<String, dynamic>>[];

    for (final entry in entries) {
      final key = entry.key;

      // Skip @@locale - always keep
      if (key == '@@locale') {
        if (!seen.contains(key)) {
          cleanedEntries.add(entry);
          seen.add(key);
        }
        continue;
      }

      // Remove ALL @metadata keys from non-EN files
      if (key.startsWith('@')) {
        removedMetadata++;
        continue;
      }

      // Remove duplicate keys (keep first)
      if (seen.contains(key)) {
        print('  DUPLICATE removed: "$key"');
        removedDuplicates++;
        continue;
      }

      // Remove orphaned keys (not in EN template)
      if (!enMessageKeys.contains(key)) {
        print('  ORPHANED removed: "$key"');
        removedOrphaned++;
        continue;
      }

      seen.add(key);
      cleanedEntries.add(entry);
    }

    // Count final message keys
    final finalMsgKeys =
        cleanedEntries.where((e) => !e.key.startsWith('@')).length;
    final missingCount = enMessageKeys.length - finalMsgKeys;

    print(
      '  Removed: $removedMetadata @metadata, $removedOrphaned orphaned, $removedDuplicates duplicates',
    );
    print(
      '  Final message keys: $finalMsgKeys / ${enMessageKeys.length} (missing: $missingCount)',
    );

    // Write cleaned file
    _writeArbFile(file, cleanedEntries, lang, includeMetadata: false);
    print('  Written: ${file.path}\n');
  }

  print('\n=== ALL DONE ===');
  print('EN template: ${enMessageKeys.length} message keys');
  print('Run "cd zodiac_app && flutter gen-l10n" to regenerate localizations');
}

void _writeArbFile(
  File file,
  List<MapEntry<String, dynamic>> entries,
  String locale, {
  required bool includeMetadata,
}) {
  final buffer = StringBuffer();
  buffer.writeln('{');

  // @@locale first
  buffer.writeln('  "@@locale": "$locale",');

  // Filter entries
  final filtered = entries.where((e) => e.key != '@@locale').toList();

  for (int i = 0; i < filtered.length; i++) {
    final entry = filtered[i];
    final isLast = i == filtered.length - 1;

    final encodedKey = json.encode(entry.key);
    final encodedValue = json.encode(entry.value);

    buffer.write('  $encodedKey: $encodedValue');

    if (!isLast) {
      buffer.writeln(',');
    } else {
      buffer.writeln();
    }
  }

  buffer.writeln('}');
  file.writeAsStringSync(buffer.toString());
}

/// Parse ARB file preserving order and detecting duplicates.
List<MapEntry<String, dynamic>> _parseArbPreservingOrder(String content) {
  final entries = <MapEntry<String, dynamic>>[];

  int pos = content.indexOf('{');
  if (pos == -1) return entries;
  pos++;

  while (pos < content.length) {
    while (pos < content.length &&
        (content[pos] == ' ' ||
            content[pos] == '\n' ||
            content[pos] == '\r' ||
            content[pos] == '\t' ||
            content[pos] == ',')) {
      pos++;
    }

    if (pos >= content.length || content[pos] == '}') break;

    if (content[pos] != '"') {
      pos++;
      continue;
    }

    final keyStart = pos;
    pos++;
    while (pos < content.length && content[pos] != '"') {
      if (content[pos] == '\\') pos++;
      pos++;
    }
    pos++;
    final key = content.substring(keyStart + 1, pos - 1);

    while (pos < content.length &&
        (content[pos] == ' ' ||
            content[pos] == '\n' ||
            content[pos] == '\r' ||
            content[pos] == '\t' ||
            content[pos] == ':')) {
      pos++;
    }

    dynamic value;
    if (content[pos] == '"') {
      final valueStart = pos;
      pos++;
      while (pos < content.length && content[pos] != '"') {
        if (content[pos] == '\\') pos++;
        pos++;
      }
      pos++;
      value = json.decode(content.substring(valueStart, pos));
    } else if (content[pos] == '{') {
      final valueStart = pos;
      int braceCount = 1;
      pos++;
      while (pos < content.length && braceCount > 0) {
        if (content[pos] == '{') braceCount++;
        if (content[pos] == '}') braceCount--;
        if (content[pos] == '"') {
          pos++;
          while (pos < content.length && content[pos] != '"') {
            if (content[pos] == '\\') pos++;
            pos++;
          }
        }
        pos++;
      }
      value = json.decode(content.substring(valueStart, pos));
    } else if (content[pos] == '[') {
      final valueStart = pos;
      int bracketCount = 1;
      pos++;
      while (pos < content.length && bracketCount > 0) {
        if (content[pos] == '[') bracketCount++;
        if (content[pos] == ']') bracketCount--;
        if (content[pos] == '"') {
          pos++;
          while (pos < content.length && content[pos] != '"') {
            if (content[pos] == '\\') pos++;
            pos++;
          }
        }
        pos++;
      }
      value = json.decode(content.substring(valueStart, pos));
    } else {
      final valueStart = pos;
      while (pos < content.length &&
          content[pos] != ',' &&
          content[pos] != '}' &&
          content[pos] != '\n') {
        pos++;
      }
      value = json.decode(content.substring(valueStart, pos).trim());
    }

    entries.add(MapEntry(key, value));
  }

  return entries;
}
