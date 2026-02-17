// ignore_for_file: avoid_print

import 'dart:io';
import 'dart:convert';

/// Fixes all ARB localization errors in app_en.arb:
/// 1. Removes section comment @_SECTION entries
/// 2. Removes orphan @metadata entries (no corresponding message key)
/// 3. Fixes duplicate top-level keys (keeps first occurrence)
/// 4. Adds placeholder metadata for keys with {param} patterns
/// 5. Adds empty @key metadata for keys missing it
void main() {
  final arbPath = 'zodiac_app/assets/l10n/app_en.arb';
  final file = File(arbPath);

  if (!file.existsSync()) {
    print('ERROR: $arbPath not found');
    exit(1);
  }

  final content = file.readAsStringSync();

  // Step 1: Parse with duplicate detection using line-by-line approach
  final entries = _parseArbPreservingOrder(content);
  print('Parsed ${entries.length} entries from $arbPath');

  // Step 2: Deduplicate - keep FIRST occurrence for message keys
  final seen = <String>{};
  final deduped = <MapEntry<String, dynamic>>[];
  int dupeCount = 0;

  for (final entry in entries) {
    if (seen.contains(entry.key)) {
      print('  DUPLICATE removed: "${entry.key}" (keeping first)');
      dupeCount++;
    } else {
      seen.add(entry.key);
      deduped.add(entry);
    }
  }
  print('Removed $dupeCount duplicate keys');

  // Step 3: Separate message keys and @metadata keys
  final messageKeys = <String, dynamic>{};
  final metaKeys = <String, dynamic>{};

  for (final entry in deduped) {
    if (entry.key.startsWith('@')) {
      metaKeys[entry.key] = entry.value;
    } else {
      messageKeys[entry.key] = entry.value;
    }
  }

  print('Message keys: ${messageKeys.length}');
  print('Metadata keys: ${metaKeys.length}');

  // Step 4: Remove section comment @_SECTION entries and orphan @metadata
  int removedSections = 0;
  int removedOrphans = 0;
  final cleanedMeta = <String, dynamic>{};

  for (final entry in metaKeys.entries) {
    final key = entry.key;

    // Keep @@locale
    if (key == '@@locale') {
      cleanedMeta[key] = entry.value;
      continue;
    }

    // Remove @_SECTION_NAME entries (section comments)
    if (key.startsWith('@_') &&
        key == key.toUpperCase().replaceAll(RegExp(r'[^A-Z_@]'), '')) {
      // Check if it's an uppercase section header like @_COMPATIBILITY_SHARING
      final msgKey = key.substring(1); // Remove @ prefix
      if (!messageKeys.containsKey(msgKey)) {
        print('  SECTION removed: "$key"');
        removedSections++;
        continue;
      }
    }

    // Check if corresponding message key exists
    final msgKey = key.substring(1); // Remove @ prefix
    if (!messageKeys.containsKey(msgKey)) {
      print('  ORPHAN removed: "$key" (no message key "$msgKey")');
      removedOrphans++;
      continue;
    }

    cleanedMeta[key] = entry.value;
  }

  print('Removed $removedSections section comments');
  print('Removed $removedOrphans orphan metadata entries');

  // Step 5: Add placeholder metadata for keys with {param} patterns
  final placeholderRegex = RegExp(r'\{(\w+)\}');
  int addedPlaceholders = 0;

  for (final entry in messageKeys.entries) {
    final key = entry.key;
    final value = entry.value;
    if (value is! String) continue;
    if (key == '@@locale') continue;

    final matches = placeholderRegex.allMatches(value);
    if (matches.isEmpty) continue;

    final metaKey = '@$key';
    final existingMeta = cleanedMeta[metaKey];

    // Check if metadata already has placeholders defined
    if (existingMeta is Map && existingMeta.containsKey('placeholders')) {
      // Verify all placeholders are defined
      final existingPlaceholders = existingMeta['placeholders'] as Map;
      final missingParams = <String>[];
      for (final match in matches) {
        final param = match.group(1)!;
        if (!existingPlaceholders.containsKey(param)) {
          missingParams.add(param);
        }
      }
      if (missingParams.isNotEmpty) {
        // Add missing placeholders
        final updatedPlaceholders = Map<String, dynamic>.from(
          existingPlaceholders,
        );
        for (final param in missingParams) {
          updatedPlaceholders[param] = {'type': _inferType(param)};
        }
        cleanedMeta[metaKey] = {
          ...Map<String, dynamic>.from(existingMeta),
          'placeholders': updatedPlaceholders,
        };
        addedPlaceholders++;
      }
    } else {
      // No metadata or no placeholders section - create it
      final placeholders = <String, dynamic>{};
      for (final match in matches) {
        final param = match.group(1)!;
        placeholders[param] = {'type': _inferType(param)};
      }
      cleanedMeta[metaKey] = {
        if (existingMeta is Map) ...Map<String, dynamic>.from(existingMeta),
        'placeholders': placeholders,
      };
      addedPlaceholders++;
    }
  }

  print('Added/fixed placeholder metadata for $addedPlaceholders keys');

  // Step 6: Add empty @key for ALL message keys that lack metadata
  int addedEmptyMeta = 0;

  for (final key in messageKeys.keys) {
    if (key == '@@locale') continue;
    final metaKey = '@$key';
    if (!cleanedMeta.containsKey(metaKey)) {
      cleanedMeta[metaKey] = {};
      addedEmptyMeta++;
    }
  }

  print('Added empty metadata for $addedEmptyMeta keys');

  // Step 7: Build final ordered JSON output
  // Order: @@locale first, then message keys interleaved with their @metadata
  final buffer = StringBuffer();
  buffer.writeln('{');

  // @@locale first
  buffer.writeln('  "@@locale": "en",');

  final sortedMessageKeys =
      messageKeys.keys.where((k) => k != '@@locale').toList();

  for (int i = 0; i < sortedMessageKeys.length; i++) {
    final key = sortedMessageKeys[i];
    final value = messageKeys[key];
    final metaKey = '@$key';
    final meta = cleanedMeta[metaKey];
    final isLast = i == sortedMessageKeys.length - 1;

    // Write the message key
    final encodedValue = json.encode(value);
    buffer.write('  ${json.encode(key)}: $encodedValue');

    if (meta != null) {
      buffer.writeln(',');
      // Write the metadata
      final encodedMeta = json.encode(meta);
      buffer.write('  ${json.encode(metaKey)}: $encodedMeta');
    }

    if (!isLast) {
      buffer.writeln(',');
    } else {
      buffer.writeln();
    }
  }

  buffer.writeln('}');

  // Write back
  file.writeAsStringSync(buffer.toString());

  final totalKeys = sortedMessageKeys.length;
  print('\n=== SUMMARY ===');
  print('Total message keys: $totalKeys');
  print('Duplicate keys removed: $dupeCount');
  print('Section comments removed: $removedSections');
  print('Orphan metadata removed: $removedOrphans');
  print('Placeholder metadata added/fixed: $addedPlaceholders');
  print('Empty metadata added: $addedEmptyMeta');
  print('File written: $arbPath');
}

String _inferType(String paramName) {
  // Common int parameters
  if ([
    'count',
    'days',
    'hours',
    'weeks',
    'number',
    'remaining',
    'total',
    'percentage',
    'score',
    'level',
    'index',
    'limit',
  ].contains(paramName)) {
    return 'int';
  }
  return 'String';
}

/// Parse ARB file preserving order and detecting duplicates.
/// Standard json.decode silently drops duplicates.
List<MapEntry<String, dynamic>> _parseArbPreservingOrder(String content) {
  final entries = <MapEntry<String, dynamic>>[];

  // Use a regex-based approach to extract top-level key-value pairs
  // This handles the specific structure of ARB files (flat JSON with nested @metadata)
  // JsonDecoder not needed - using manual parsing to preserve order

  // First, let's find all top-level keys and their positions
  // We need to handle nested objects (like @metadata with placeholders)
  int pos = content.indexOf('{');
  if (pos == -1) return entries;
  pos++; // Skip opening brace

  while (pos < content.length) {
    // Skip whitespace and commas
    while (pos < content.length &&
        (content[pos] == ' ' ||
            content[pos] == '\n' ||
            content[pos] == '\r' ||
            content[pos] == '\t' ||
            content[pos] == ',')) {
      pos++;
    }

    if (pos >= content.length || content[pos] == '}') break;

    // Expect a quoted key
    if (content[pos] != '"') {
      pos++;
      continue;
    }

    // Extract key
    final keyStart = pos;
    pos++; // Skip opening quote
    while (pos < content.length && content[pos] != '"') {
      if (content[pos] == '\\') pos++; // Skip escaped char
      pos++;
    }
    pos++; // Skip closing quote
    final key = content.substring(keyStart + 1, pos - 1);

    // Skip colon and whitespace
    while (pos < content.length &&
        (content[pos] == ' ' ||
            content[pos] == '\n' ||
            content[pos] == '\r' ||
            content[pos] == '\t' ||
            content[pos] == ':')) {
      pos++;
    }

    // Extract value - could be string, object, number, etc.
    dynamic value;
    if (content[pos] == '"') {
      // String value
      final valueStart = pos;
      pos++; // Skip opening quote
      while (pos < content.length && content[pos] != '"') {
        if (content[pos] == '\\') pos++; // Skip escaped char
        pos++;
      }
      pos++; // Skip closing quote
      value = json.decode(content.substring(valueStart, pos));
    } else if (content[pos] == '{') {
      // Object value - find matching closing brace
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
      // Array value
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
      // Number, boolean, or null
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
