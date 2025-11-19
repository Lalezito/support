#!/usr/bin/env dart
// 🎨 SVG GENERATOR WITH AI INTEGRATION
// Genera SVGs personalizados usando prompts de texto
// Puede integrar con APIs de generación de imágenes

import 'dart:io';
import 'dart:convert';

/// OPCIÓN 1: GENERADOR LOCAL DE SVGs (Sin API)
/// Genera SVGs proceduralmente basados en plantillas
class LocalSVGGenerator {
  /// Genera un SVG de planeta personalizado
  static String generatePlanet({
    required String name,
    required String primaryColor,
    required String secondaryColor,
    double size = 64.0,
    bool hasRings = false,
    bool hasMoons = false,
  }) {
    final svg = StringBuffer();

    svg.writeln('<svg width="$size" height="$size" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">');
    svg.writeln('  <defs>');
    svg.writeln('    <radialGradient id="${name}Glow" cx="50%" cy="50%" r="60%">');
    svg.writeln('      <stop offset="0%" style="stop-color:$primaryColor;stop-opacity:0.7"/>');
    svg.writeln('      <stop offset="100%" style="stop-color:$secondaryColor;stop-opacity:0"/>');
    svg.writeln('    </radialGradient>');
    svg.writeln('    <linearGradient id="${name}Surface" x1="0%" y1="0%" x2="100%" y2="100%">');
    svg.writeln('      <stop offset="0%" style="stop-color:$primaryColor"/>');
    svg.writeln('      <stop offset="100%" style="stop-color:$secondaryColor"/>');
    svg.writeln('    </linearGradient>');
    svg.writeln('  </defs>');

    // Planet glow
    svg.writeln('  <circle cx="32" cy="32" r="28" fill="url(#${name}Glow)" opacity="0.5">');
    svg.writeln('    <animate attributeName="opacity" dur="4s" values="0.5;0.7;0.5" repeatCount="indefinite"/>');
    svg.writeln('  </circle>');

    // Main body
    svg.writeln('  <circle cx="32" cy="32" r="20" fill="url(#${name}Surface)"/>');

    // Optional rings
    if (hasRings) {
      svg.writeln('  <ellipse cx="32" cy="32" rx="30" ry="8" fill="none" stroke="$secondaryColor" stroke-width="2" opacity="0.6"/>');
    }

    // Optional moon
    if (hasMoons) {
      svg.writeln('  <circle cx="48" cy="20" r="4" fill="#D3D3D3" opacity="0.8"/>');
    }

    svg.writeln('</svg>');

    return svg.toString();
  }

  /// Genera un SVG de constelación personalizada
  static String generateConstellation({
    required String name,
    required List<Map<String, double>> stars,
    String color = '#FFFFFF',
  }) {
    final svg = StringBuffer();

    svg.writeln('<svg width="200" height="150" viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">');

    // Connect stars with lines
    for (int i = 0; i < stars.length - 1; i++) {
      final star1 = stars[i];
      final star2 = stars[i + 1];
      svg.writeln('  <line x1="${star1['x']}" y1="${star1['y']}" x2="${star2['x']}" y2="${star2['y']}"');
      svg.writeln('        stroke="$color" stroke-width="1" opacity="0.4"/>');
    }

    // Draw stars
    for (final star in stars) {
      svg.writeln('  <circle cx="${star['x']}" cy="${star['y']}" r="2" fill="$color">');
      svg.writeln('    <animate attributeName="opacity" dur="2s" values="0.6;1;0.6" repeatCount="indefinite"/>');
      svg.writeln('  </circle>');
    }

    svg.writeln('</svg>');

    return svg.toString();
  }
}

/// OPCIÓN 2: INTEGRACIÓN CON OPENAI DALL-E (Requiere API Key)
class AIImageGenerator {
  final String apiKey;

  AIImageGenerator(this.apiKey);

  /// Genera una imagen con DALL-E y la convierte a SVG
  /// Nota: DALL-E genera PNG/JPG, necesitarías un servicio adicional para convertir a SVG
  Future<String?> generateWithDALLE(String prompt) async {
    final url = Uri.parse('https://api.openai.com/v1/images/generations');

    final response = await HttpClient().postUrl(url)
      ..headers.add('Authorization', 'Bearer $apiKey')
      ..headers.add('Content-Type', 'application/json')
      ..write(jsonEncode({
        'model': 'dall-e-3',
        'prompt': 'Minimalist SVG style cosmic illustration: $prompt',
        'size': '1024x1024',
        'quality': 'standard',
        'n': 1,
      }));

    final httpResponse = await response.close();

    if (httpResponse.statusCode == 200) {
      final responseBody = await httpResponse.transform(utf8.decoder).join();
      final data = jsonDecode(responseBody);
      return data['data'][0]['url'];
    }

    return null;
  }
}

/// OPCIÓN 3: TEMPLATES PREDEFINIDOS
class SVGTemplates {
  /// Nebula template
  static String nebula({
    required String name,
    required List<String> colors,
  }) {
    return '''
<svg width="200" height="150" viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="${name}Core" cx="50%" cy="50%" r="50%">
      ${colors.asMap().entries.map((e) =>
        '<stop offset="${(e.key / (colors.length - 1) * 100).toStringAsFixed(0)}%" style="stop-color:${e.value};stop-opacity:${0.8 - e.key * 0.2}"/>'
      ).join('\n      ')}
    </radialGradient>
  </defs>

  <ellipse cx="100" cy="75" rx="80" ry="60" fill="url(#${name}Core)" opacity="0.6">
    <animate attributeName="opacity" dur="6s" values="0.6;0.8;0.6" repeatCount="indefinite"/>
  </ellipse>

  <circle cx="60" cy="50" r="2" fill="white" opacity="0.8">
    <animate attributeName="opacity" dur="2s" values="0.8;0.4;0.8" repeatCount="indefinite"/>
  </circle>
  <circle cx="140" cy="100" r="1.5" fill="white" opacity="0.7">
    <animate attributeName="opacity" dur="2.3s" values="0.7;0.3;0.7" repeatCount="indefinite"/>
  </circle>
</svg>
''';
  }

  /// Empty state template
  static String emptyState({
    required String icon,
    required String message,
  }) {
    return '''
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="emptyBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#E6E6FA;stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:#D8BFD8;stop-opacity:0"/>
    </radialGradient>
  </defs>

  <circle cx="100" cy="100" r="90" fill="url(#emptyBg)"/>

  <!-- Icon placeholder -->
  <circle cx="100" cy="90" r="40" fill="none" stroke="#C0C0C0" stroke-width="3" stroke-dasharray="5,5">
    <animate attributeName="opacity" dur="2s" values="0.5;0.8;0.5" repeatCount="indefinite"/>
  </circle>

  <!-- Message text area -->
  <text x="100" y="160" font-size="14" fill="#808080" text-anchor="middle">$message</text>
</svg>
''';
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN - EJEMPLOS DE USO
// ═══════════════════════════════════════════════════════════════════════════

void main(List<String> args) async {
  stdout.writeln('🎨 SVG Generator - Zodiac Life Coach');
  stdout.writeln('═══════════════════════════════════════\n');

  if (args.isEmpty) {
    stdout.writeln('Usage:');
    stdout.writeln('  dart svg_generator_ai.dart planet <name> <color1> <color2>');
    stdout.writeln('  dart svg_generator_ai.dart constellation <name>');
    stdout.writeln('  dart svg_generator_ai.dart nebula <name> <color1> <color2> <color3>');
    stdout.writeln('\nExamples:');
    stdout.writeln('  dart svg_generator_ai.dart planet pluto #8B7355 #654321');
    stdout.writeln('  dart svg_generator_ai.dart nebula orion #FF1493 #8A2BE2 #4B0082');
    return;
  }

  final command = args[0];

  switch (command) {
    case 'planet':
      if (args.length < 4) {
        stdout.writeln('Error: Need planet name and 2 colors');
        return;
      }
      final svg = LocalSVGGenerator.generatePlanet(
        name: args[1],
        primaryColor: args[2],
        secondaryColor: args[3],
        hasRings: args.contains('--rings'),
        hasMoons: args.contains('--moons'),
      );

      final outputPath = 'assets/decorative/planets/${args[1]}.svg';
      await File(outputPath).writeAsString(svg);
      stdout.writeln('✅ Created: $outputPath');
      break;

    case 'constellation':
      if (args.length < 2) {
        stdout.writeln('Error: Need constellation name');
        return;
      }

      // Generate random star positions for demo
      final stars = List.generate(5, (i) => {
        'x': 40.0 + i * 30.0,
        'y': 50.0 + (i % 2) * 20.0,
      });

      final svg = LocalSVGGenerator.generateConstellation(
        name: args[1],
        stars: stars,
      );

      final outputPath = 'assets/decorative/constellations/${args[1]}.svg';
      await File(outputPath).writeAsString(svg);
      stdout.writeln('✅ Created: $outputPath');
      break;

    case 'nebula':
      if (args.length < 5) {
        stdout.writeln('Error: Need nebula name and 3 colors');
        return;
      }

      final svg = SVGTemplates.nebula(
        name: args[1],
        colors: [args[2], args[3], args[4]],
      );

      final outputPath = 'assets/decorative/nebulas/${args[1]}.svg';
      await File(outputPath).writeAsString(svg);
      stdout.writeln('✅ Created: $outputPath');
      break;

    default:
      stdout.writeln('Unknown command: $command');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// INSTRUCCIONES DE USO
// ═══════════════════════════════════════════════════════════════════════════

/*
OPCIÓN 1: GENERADOR LOCAL (Sin API, gratis)
═══════════════════════════════════════════════

1. Ejecutar desde terminal:
   cd /Users/alejandrocaceres/Desktop/appstore.zodia
   dart scripts/svg_generator_ai.dart planet pluto #8B7355 #654321
   dart scripts/svg_generator_ai.dart nebula horsehead #FF1493 #8A2BE2 #4B0082

2. Los SVGs se crearán automáticamente en assets/decorative/

VENTAJAS:
✅ Gratis
✅ Instantáneo
✅ Control total del output
✅ Consistencia garantizada

DESVENTAJAS:
⚠️  Limitado a templates predefinidos
⚠️  Requiere conocimiento de SVG para personalizar


OPCIÓN 2: INTEGRACIÓN CON OPENAI DALL-E (Requiere API Key, costo)
═══════════════════════════════════════════════════════════════════

1. Obtener API Key de OpenAI: https://platform.openai.com/api-keys

2. Configurar en .env:
   OPENAI_API_KEY=sk-...

3. Usar el generador:
   ```dart
   final generator = AIImageGenerator(Platform.environment['OPENAI_API_KEY']!);
   final imageUrl = await generator.generateWithDALLE('cosmic nebula in purple and blue');
   ```

VENTAJAS:
✅ Imágenes únicas y creativas
✅ Solo necesitas describir lo que quieres
✅ Alta calidad visual

DESVENTAJAS:
⚠️  Costo por imagen (~$0.04 por imagen con DALL-E 3)
⚠️  Genera PNG/JPG, no SVG directo
⚠️  Requiere conversión PNG → SVG (tools como vectorizer.ai)


OPCIÓN 3: HERRAMIENTAS ONLINE GRATUITAS
════════════════════════════════════════

1. SVG Generators:
   - https://app.haikei.app/ (patrones y backgrounds)
   - https://getwaves.io/ (ondas y formas orgánicas)
   - https://www.blobmaker.app/ (formas abstractas)

2. AI Image → SVG Conversion:
   - https://vectorizer.ai/ (PNG/JPG → SVG)
   - https://www.autotracer.org/ (free vectorization)

VENTAJAS:
✅ Gratis
✅ Interfaz visual fácil
✅ Exporta SVG directamente

DESVENTAJAS:
⚠️  Manual (no automatizable)
⚠️  Cada imagen requiere visita a la web


RECOMENDACIÓN PARA ZODIAC APP:
═══════════════════════════════

Para esta app, recomiendo OPCIÓN 1 (Generador Local):
- Ya tienes los SVGs críticos
- Los decorativos pueden ser procedurales
- Mantiene consistencia visual
- Gratis e instantáneo
- Puedes ajustar templates según necesites

Si necesitas algo muy específico y único, usa OPCIÓN 3 (herramientas online)
para crear 1-2 assets especiales, luego úsalos como base para tus templates.
*/
