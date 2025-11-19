#!/bin/bash

cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n

echo "=== 🌍 Reporte de Traducciones ===" echo ""
echo "Generando keys de EN (base)..."
jq -r 'keys[]' app_en.arb | sort > /tmp/en_keys.txt
EN_COUNT=$(wc -l < /tmp/en_keys.txt | tr -d ' ')
echo "EN tiene $EN_COUNT keys"
echo ""

echo "=== Comparación con otros idiomas ==="
echo ""

# Español
echo "🇪🇸 ESPAÑOL (ES)"
jq -r 'keys[]' app_es.arb | sort > /tmp/es_keys.txt
ES_COUNT=$(wc -l < /tmp/es_keys.txt | tr -d ' ')
MISSING_ES=$(comm -23 /tmp/en_keys.txt /tmp/es_keys.txt | wc -l | tr -d ' ')
EXTRA_ES=$(comm -13 /tmp/en_keys.txt /tmp/es_keys.txt | wc -l | tr -d ' ')
echo "  Total keys: $ES_COUNT"
echo "  Faltantes vs EN: $MISSING_ES"
echo "  Extras vs EN: $EXTRA_ES"
echo ""

# Alemán
echo "🇩🇪 ALEMÁN (DE)"
jq -r 'keys[]' app_de.arb | sort > /tmp/de_keys.txt
DE_COUNT=$(wc -l < /tmp/de_keys.txt | tr -d ' ')
MISSING_DE=$(comm -23 /tmp/en_keys.txt /tmp/de_keys.txt | wc -l | tr -d ' ')
EXTRA_DE=$(comm -13 /tmp/en_keys.txt /tmp/de_keys.txt | wc -l | tr -d ' ')
echo "  Total keys: $DE_COUNT"
echo "  Faltantes vs EN: $MISSING_DE"
echo "  Extras vs EN: $EXTRA_DE"
echo ""

# Francés
echo "🇫🇷 FRANCÉS (FR)"
jq -r 'keys[]' app_fr.arb | sort > /tmp/fr_keys.txt
FR_COUNT=$(wc -l < /tmp/fr_keys.txt | tr -d ' ')
MISSING_FR=$(comm -23 /tmp/en_keys.txt /tmp/fr_keys.txt | wc -l | tr -d ' ')
EXTRA_FR=$(comm -13 /tmp/en_keys.txt /tmp/fr_keys.txt | wc -l | tr -d ' ')
echo "  Total keys: $FR_COUNT"
echo "  Faltantes vs EN: $MISSING_FR"
echo "  Extras vs EN: $EXTRA_FR"
echo ""

# Italiano
echo "🇮🇹 ITALIANO (IT)"
jq -r 'keys[]' app_it.arb | sort > /tmp/it_keys.txt
IT_COUNT=$(wc -l < /tmp/it_keys.txt | tr -d ' ')
MISSING_IT=$(comm -23 /tmp/en_keys.txt /tmp/it_keys.txt | wc -l | tr -d ' ')
EXTRA_IT=$(comm -13 /tmp/en_keys.txt /tmp/it_keys.txt | wc -l | tr -d ' ')
echo "  Total keys: $IT_COUNT"
echo "  Faltantes vs EN: $MISSING_IT"
echo "  Extras vs EN: $EXTRA_IT"
echo ""

# Portugués
echo "🇵🇹 PORTUGUÉS (PT)"
jq -r 'keys[]' app_pt.arb | sort > /tmp/pt_keys.txt
PT_COUNT=$(wc -l < /tmp/pt_keys.txt | tr -d ' ')
MISSING_PT=$(comm -23 /tmp/en_keys.txt /tmp/pt_keys.txt | wc -l | tr -d ' ')
EXTRA_PT=$(comm -13 /tmp/en_keys.txt /tmp/pt_keys.txt | wc -l | tr -d ' ')
echo "  Total keys: $PT_COUNT"
echo "  Faltantes vs EN: $MISSING_PT"
echo "  Extras vs EN: $EXTRA_PT"
echo ""

echo "=== Resumen ==="
echo ""
echo "| Idioma | Keys | Faltantes | Extras |"
echo "|--------|------|-----------|--------|"
echo "| EN     | $EN_COUNT | -         | -      |"
echo "| ES     | $ES_COUNT | $MISSING_ES | $EXTRA_ES |"
echo "| DE     | $DE_COUNT | $MISSING_DE | $EXTRA_DE |"
echo "| FR     | $FR_COUNT | $MISSING_FR | $EXTRA_FR |"
echo "| IT     | $IT_COUNT | $MISSING_IT | $EXTRA_IT |"
echo "| PT     | $PT_COUNT | $MISSING_PT | $EXTRA_PT |"
echo ""

# Listar algunas keys faltantes en ES
echo "=== Ejemplos de Keys Faltantes en ESPAÑOL ===" echo ""
comm -23 /tmp/en_keys.txt /tmp/es_keys.txt | head -20
echo ""
echo "(Mostrando primeras 20 de $MISSING_ES total)"
