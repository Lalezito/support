#!/bin/bash

# 🔍 Check Analytics Counters Debug Script
# Verifica los contadores de analytics en SharedPreferences

echo "🔍 Analytics Counters Debug"
echo "=========================="
echo ""

# Run flutter app with debug prints
echo "📱 Ejecutando flutter run con logs de analytics..."
echo ""
echo "Busca en los logs:"
echo "  - '📊 Coach sessions count: X'"
echo "  - '📊 Compatibility count: X'"
echo ""
echo "Instrucciones:"
echo "1. Usa Cosmic Coach → envía mensaje"
echo "2. Usa Compatibility → calcula compatibilidad"
echo "3. Ve a Analytics → pull down para refrescar"
echo "4. Busca los logs arriba para ver si los contadores aumentan"
echo ""
echo "Press Ctrl+C para salir cuando termines"
echo ""

cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Run and filter for analytics logs
flutter run 2>&1 | grep --line-buffered -E "(📊|Analytics|compatibility|coach)" | while IFS= read -r line; do
    echo "[$(date +%H:%M:%S)] $line"
done
