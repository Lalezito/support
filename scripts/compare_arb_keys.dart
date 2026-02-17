// ignore_for_file: avoid_print

import 'dart:io';
import 'dart:convert';

void main() {
  final baseDir =
      '/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n';

  // Read English template
  final enFile = File('$baseDir/app_en.arb');
  final enContent = enFile.readAsStringSync();
  final enJson = jsonDecode(enContent) as Map<String, dynamic>;

  // Extract message keys (not @metadata keys or @@locale)
  final enKeys =
      enJson.keys
          .where((key) => !key.startsWith('@') && key != '@@locale')
          .toSet();

  print('English template has ${enKeys.length} message keys\n');

  // Languages to check
  final languages = ['es', 'fr', 'de', 'it', 'pt'];

  for (final lang in languages) {
    final file = File('$baseDir/app_$lang.arb');
    final content = file.readAsStringSync();
    final json = jsonDecode(content) as Map<String, dynamic>;

    // Extract message keys
    final langKeys =
        json.keys
            .where((key) => !key.startsWith('@') && key != '@@locale')
            .toSet();

    // Find orphaned keys (in this language but not in EN)
    final orphaned = langKeys.difference(enKeys).toList()..sort();

    // Find missing keys (in EN but not in this language)
    final missing = enKeys.difference(langKeys).toList()..sort();

    print('=== ${lang.toUpperCase()} ===');
    print('ORPHANED KEYS TO REMOVE (${orphaned.length} total):');
    if (orphaned.isEmpty) {
      print('(none)');
    } else {
      print(orphaned.join(', '));
    }
    print('');

    print('MISSING KEYS (${missing.length} total, showing first 20):');
    if (missing.isEmpty) {
      print('(none)');
    } else {
      final toShow = missing.take(20).toList();
      print(toShow.join(', '));
      if (missing.length > 20) {
        print('... and ${missing.length - 20} more');
      }
    }
    print('');
    print('');
  }
}
