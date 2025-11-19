#!/bin/bash
# Script para monitorear logs de compartir en tiempo real

echo "🔍 Monitoreando logs de SHARE en tiempo real..."
echo "📱 Ahora puedes probar el botón de compartir en la app"
echo "🛑 Presiona Ctrl+C para detener"
echo ""
echo "=========================================="
echo ""

tail -f /tmp/flutter_debug_share_oct30.log | grep --line-buffered -E "(SHARE DEBUG|shareHoroscope|Error|Exception|Failed)" --color=always
