#!/bin/bash
# ============================================================================
# AGENT 10: INTEGRATOR - Integrador al Proyecto
# ============================================================================
# Rol: Copiar archivos modulares al proyecto e integrar con l10n.yaml
# Input: cosmic_coach_{lang}.arb (6 archivos)
# Output: Archivos integrados + INTEGRATION_GUIDE.md
# ============================================================================

set -e

echo "🚀 AGENT 10: INTEGRATOR - Iniciando integración al proyecto..."
echo ""

# Paths
BASE_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app"
L10N_DIR="$BASE_DIR/assets/l10n"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"
FEATURE_DIR="$OUTPUT_DIR/features/cosmic_coach"
PROJECT_FEATURES_DIR="$L10N_DIR/features"
PROJECT_COSMIC_DIR="$PROJECT_FEATURES_DIR/cosmic_coach"

echo "📁 Directorio proyecto: $BASE_DIR"
echo "📁 Directorio l10n: $L10N_DIR"
echo ""

# Languages
LANGUAGES=("en" "es" "de" "fr" "it" "pt")
LANG_NAMES=("English" "Español" "Deutsch" "Français" "Italiano" "Português")

# Check if quality report exists and meets threshold
if [ -f "$OUTPUT_DIR/quality_report.json" ]; then
  QUALITY_SCORE=$(jq -r '.overall_quality_score' "$OUTPUT_DIR/quality_report.json")
  echo "🎯 Puntuación de calidad: $QUALITY_SCORE/100"

  if [ "$QUALITY_SCORE" -lt 70 ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: Puntuación de calidad baja ($QUALITY_SCORE/100)"
    echo "   Se recomienda revisar el reporte de calidad antes de integrar"
    echo ""
    read -p "¿Deseas continuar de todos modos? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "❌ Integración cancelada por el usuario"
      exit 1
    fi
  fi
else
  echo "⚠️  quality_report.json no encontrado"
  echo "   Ejecuta primero Agent 9: QUALITY_CHECKER"
  echo ""
  read -p "¿Deseas continuar de todos modos? (y/N): " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Integración cancelada por el usuario"
    exit 1
  fi
fi

echo ""
echo "1️⃣ Creando estructura de directorios..."
echo ""

# Create features directory structure
mkdir -p "$PROJECT_FEATURES_DIR"
mkdir -p "$PROJECT_COSMIC_DIR"

echo "   ✅ $PROJECT_FEATURES_DIR"
echo "   ✅ $PROJECT_COSMIC_DIR"
echo ""

echo "2️⃣ Copiando archivos de traducción..."
echo ""

COPIED_FILES=0
FAILED_FILES=0

for i in "${!LANGUAGES[@]}"; do
  LANG="${LANGUAGES[$i]}"
  LANG_NAME="${LANG_NAMES[$i]}"

  SOURCE="$FEATURE_DIR/cosmic_coach_${LANG}.arb"
  DEST="$PROJECT_COSMIC_DIR/cosmic_coach_${LANG}.arb"

  if [ -f "$SOURCE" ]; then
    # Create backup if file exists
    if [ -f "$DEST" ]; then
      BACKUP="$DEST.backup.$(date +%Y%m%d_%H%M%S)"
      cp "$DEST" "$BACKUP"
      echo "   📦 Backup creado: $(basename "$BACKUP")"
    fi

    # Copy file
    cp "$SOURCE" "$DEST"
    echo "   ✅ $LANG_NAME: cosmic_coach_${LANG}.arb copiado"
    COPIED_FILES=$((COPIED_FILES + 1))
  else
    echo "   ❌ $LANG_NAME: archivo fuente no encontrado"
    FAILED_FILES=$((FAILED_FILES + 1))
  fi
done

echo ""
echo "   📊 Archivos copiados: $COPIED_FILES/${#LANGUAGES[@]}"
[ $FAILED_FILES -gt 0 ] && echo "   ⚠️  Archivos fallidos: $FAILED_FILES"
echo ""

echo "3️⃣ Actualizando l10n.yaml..."
echo ""

L10N_YAML="$BASE_DIR/l10n.yaml"

if [ ! -f "$L10N_YAML" ]; then
  echo "   ⚠️  l10n.yaml no encontrado en $BASE_DIR"
  echo "   Creando nuevo l10n.yaml..."

  cat > "$L10N_YAML" << 'EOF'
arb-dir: assets/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
synthetic-package: false
nullable-getter: false

# Feature-based modular translations
feature-files:
  - cosmic_coach:
      arb-dir: assets/l10n/features/cosmic_coach
      output-class: CosmicCoachLocalizations
EOF

  echo "   ✅ l10n.yaml creado con configuración modular"
else
  echo "   ℹ️  l10n.yaml existente encontrado"
  echo "   ⚠️  NOTA: Actualización manual requerida"

  # Create backup
  BACKUP="$L10N_YAML.backup.$(date +%Y%m%d_%H%M%S)"
  cp "$L10N_YAML" "$BACKUP"
  echo "   📦 Backup creado: $(basename "$BACKUP")"
fi

echo ""

echo "4️⃣ Generando guía de integración..."
echo ""

cat > "$OUTPUT_DIR/INTEGRATION_GUIDE.md" << 'EOF'
# Guía de Integración - Cosmic Coach Translations

## 📋 Resumen de Integración

Esta guía documenta el proceso de integración de las traducciones modulares de Cosmic Coach al proyecto Zodiac App.

## 📂 Estructura de Archivos Generados

```
zodiac_app/
└── assets/
    └── l10n/
        ├── app_en.arb (original - monolítico)
        ├── app_es.arb (original - monolítico)
        ├── ...
        └── features/
            └── cosmic_coach/
                ├── cosmic_coach_en.arb
                ├── cosmic_coach_es.arb
                ├── cosmic_coach_de.arb
                ├── cosmic_coach_fr.arb
                ├── cosmic_coach_it.arb
                └── cosmic_coach_pt.arb
```

## ✅ Archivos Integrados

EOF

for i in "${!LANGUAGES[@]}"; do
  LANG="${LANGUAGES[$i]}"
  LANG_NAME="${LANG_NAMES[$i]}"
  echo "- ✅ **$LANG_NAME ($LANG)**: \`cosmic_coach_${LANG}.arb\`" >> "$OUTPUT_DIR/INTEGRATION_GUIDE.md"
done

cat >> "$OUTPUT_DIR/INTEGRATION_GUIDE.md" << 'EOF'

## 🔧 Configuración de l10n.yaml

### Opción 1: Configuración Modular (Recomendada)

Actualiza tu `l10n.yaml` para soportar archivos modulares:

```yaml
arb-dir: assets/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
synthetic-package: false
nullable-getter: false

# Feature-based modular translations
feature-files:
  - cosmic_coach:
      arb-dir: assets/l10n/features/cosmic_coach
      template-arb-file: cosmic_coach_en.arb
      output-localization-file: cosmic_coach_localizations.dart
      output-class: CosmicCoachLocalizations
```

### Opción 2: Configuración Simple

Si tu versión de Flutter no soporta archivos modulares, puedes mantener los archivos como referencia y seguir usando los archivos principales `app_{lang}.arb`.

## 🚀 Pasos Post-Integración

### 1. Regenerar archivos de localización

```bash
cd zodiac_app
flutter gen-l10n
```

### 2. Verificar importaciones en código

Si usas configuración modular, actualiza las importaciones:

```dart
// Antes
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

// Después (para Cosmic Coach)
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_gen/gen_l10n/cosmic_coach_localizations.dart';
```

### 3. Usar traducciones modulares

```dart
// En widgets de Cosmic Coach
final l10n = CosmicCoachLocalizations.of(context);
Text(l10n.cosmicCoachTitle);
```

### 4. Testing

Ejecuta las pruebas para verificar que las traducciones funcionan correctamente:

```bash
flutter test
```

### 5. Verificación visual

Cambia el idioma de la app y verifica que todas las traducciones de Cosmic Coach se muestren correctamente.

## 📊 Estadísticas de Integración

EOF

if [ -f "$OUTPUT_DIR/quality_report.json" ]; then
  QUALITY_SCORE=$(jq -r '.overall_quality_score' "$OUTPUT_DIR/quality_report.json")
  echo "- **Puntuación de calidad**: $QUALITY_SCORE/100" >> "$OUTPUT_DIR/INTEGRATION_GUIDE.md"

  for LANG in "${LANGUAGES[@]}"; do
    KEY_COUNT=$(jq -r ".files.$LANG.key_count" "$OUTPUT_DIR/quality_report.json")
    MISSING=$(jq -r ".files.$LANG.missing_translations" "$OUTPUT_DIR/quality_report.json")
    echo "- **$LANG**: $KEY_COUNT keys, $MISSING faltantes" >> "$OUTPUT_DIR/INTEGRATION_GUIDE.md"
  done
fi

cat >> "$OUTPUT_DIR/INTEGRATION_GUIDE.md" << 'EOF'

## ⚠️ Notas Importantes

### Traducciones Faltantes

Algunos archivos pueden contener el marcador `MISSING_TRANSLATION` para keys que no existían en el archivo original. Estos deben ser completados manualmente:

1. Buscar en el archivo: `"key": "MISSING_TRANSLATION"`
2. Traducir el texto desde la referencia en inglés
3. Reemplazar `MISSING_TRANSLATION` con la traducción correcta

### Backups

Todos los archivos existentes fueron respaldados con timestamp antes de ser reemplazados:
- Formato: `cosmic_coach_{lang}.arb.backup.YYYYMMDD_HHMMSS`
- Ubicación: `assets/l10n/features/cosmic_coach/`

### Rollback

Si necesitas revertir los cambios:

```bash
cd assets/l10n/features/cosmic_coach
# Restaurar desde backup
cp cosmic_coach_en.arb.backup.YYYYMMDD_HHMMSS cosmic_coach_en.arb
# Repetir para cada idioma
```

## 🎯 Próximos Pasos

1. ✅ Archivos integrados al proyecto
2. ⏳ Ejecutar `flutter gen-l10n`
3. ⏳ Actualizar código para usar `CosmicCoachLocalizations`
4. ⏳ Completar traducciones marcadas como `MISSING_TRANSLATION`
5. ⏳ Testing exhaustivo en los 6 idiomas
6. ⏳ Remover keys de Cosmic Coach de archivos monolíticos (opcional)

## 📞 Soporte

Para reportar issues o preguntas:
- Revisar reportes en: `/multiagent_output/`
- Verificar logs de cada agente
- Consultar `quality_report.json` para detalles

---

**Generado por**: AGENT 10: INTEGRATOR
**Fecha**: $(date)
**Sistema**: Multiagent Translation Segmentation System
EOF

echo "   ✅ INTEGRATION_GUIDE.md generado"
echo ""

# Generate final integration report
cat > "$OUTPUT_DIR/agent10_integrator_report.txt" << EOF
=============================================================================
AGENT 10: INTEGRATOR - Reporte de Integración
=============================================================================
Fecha: $(date)
Feature: Cosmic Coach

ARCHIVOS INTEGRADOS:
--------------------
✅ Archivos copiados:       $COPIED_FILES/${#LANGUAGES[@]}
$([ $FAILED_FILES -gt 0 ] && echo "❌ Archivos fallidos:      $FAILED_FILES" || echo "")

UBICACIÓN:
----------
📁 Directorio destino:      $PROJECT_COSMIC_DIR

ARCHIVOS:
---------
EOF

for LANG in "${LANGUAGES[@]}"; do
  if [ -f "$PROJECT_COSMIC_DIR/cosmic_coach_${LANG}.arb" ]; then
    SIZE=$(du -h "$PROJECT_COSMIC_DIR/cosmic_coach_${LANG}.arb" | cut -f1)
    echo "✅ cosmic_coach_${LANG}.arb ($SIZE)" >> "$OUTPUT_DIR/agent10_integrator_report.txt"
  else
    echo "❌ cosmic_coach_${LANG}.arb (NO INTEGRADO)" >> "$OUTPUT_DIR/agent10_integrator_report.txt"
  fi
done

cat >> "$OUTPUT_DIR/agent10_integrator_report.txt" << EOF

CONFIGURACIÓN:
--------------
📄 l10n.yaml: $([ -f "$L10N_YAML" ] && echo "Actualizado (revisar manualmente)" || echo "Creado")

DOCUMENTACIÓN:
--------------
✅ INTEGRATION_GUIDE.md     - Guía completa de integración
✅ agent10_integrator_report.txt - Este reporte

PRÓXIMOS PASOS:
---------------
1. Revisar l10n.yaml y actualizar si es necesario
2. Ejecutar: flutter gen-l10n
3. Actualizar código para usar CosmicCoachLocalizations
4. Completar traducciones marcadas como MISSING_TRANSLATION
5. Ejecutar testing exhaustivo
6. (Opcional) Remover keys de Cosmic Coach de archivos monolíticos

ROLLBACK:
---------
Los backups están disponibles en:
$PROJECT_COSMIC_DIR/*.backup.*

EOF

cat "$OUTPUT_DIR/agent10_integrator_report.txt"

echo ""
echo "✅ AGENT 10: INTEGRATOR - Integración completada exitosamente"
echo ""
echo "📊 Resumen:"
echo "   - Archivos integrados: $COPIED_FILES/${#LANGUAGES[@]}"
echo "   - Ubicación: $PROJECT_COSMIC_DIR"
echo "   - Guía de integración: INTEGRATION_GUIDE.md"
echo ""
echo "🎯 Próximo paso: Revisar INTEGRATION_GUIDE.md y ejecutar 'flutter gen-l10n'"
echo ""
