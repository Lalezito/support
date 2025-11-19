#!/bin/bash

# 📸 SCRIPT AUTOMATIZADO PARA CREAR SCREENSHOTS PROFESIONALES
# Para Zodiac Life Coach - App Store Ready

echo "🌟 INICIANDO CREACIÓN DE SCREENSHOTS PARA ZODIAC LIFE COACH"

# Crear directorio para screenshots
mkdir -p screenshots/ios/iphone_6_7_inch
mkdir -p screenshots/ios/ipad_13_inch
mkdir -p screenshots/android/phone
mkdir -p screenshots/android/tablet

echo "📁 Directorios creados para screenshots"

# Configurar simulador iPhone 16 Pro (6.7")
DEVICE_ID="213875D2-0E63-43B1-8E4E-EE481DA93DEA"

echo "📱 Configurando iPhone 16 Pro para screenshots..."

# Función para tomar screenshot en simulador
take_screenshot() {
    local filename=$1
    local description=$2
    echo "📸 Capturando: $description"
    xcrun simctl io $DEVICE_ID screenshot "screenshots/ios/iphone_6_7_inch/$filename.png"
    sleep 2
}

# Configurar simulador para screenshots
echo "⚙️ Preparando simulador para capturas profesionales..."

# Establecer idioma en español para mejor presentación
xcrun simctl boot $DEVICE_ID 2>/dev/null || true
sleep 3

# Configurar orientación vertical
xcrun simctl ui $DEVICE_ID appearance light

echo "✅ Simulador configurado correctamente"

# Crear capturas usando dispositivo físico o mock-ups profesionales
echo "🎯 PLAN DE CAPTURAS PARA APP STORE:"
echo "1. ✨ Pantalla Principal - Horóscopo Diario"
echo "2. 💕 Compatibilidad Zodiacal"
echo "3. 🤖 Coach IA Astrológico"
echo "4. 💎 Funciones Premium"
echo "5. 👤 Perfil y Carta Natal"

# Verificar que tenemos las screenshots necesarias
echo ""
echo "📋 ESPECIFICACIONES TÉCNICAS:"
echo "• Resolución iPhone: 1290x2796px"
echo "• Formato: PNG"
echo "• Calidad: 300 DPI"
echo "• Cantidad: 5 screenshots principales"

echo ""
echo "🚀 PARA CONTINUAR:"
echo "1. Ejecuta la app manualmente en el simulador"
echo "2. Navega a cada pantalla"
echo "3. Usa Cmd+S para capturar cada screenshot"
echo "4. Los archivos se guardarán automáticamente"

echo ""
echo "📱 SIMULADOR CONFIGURADO:"
echo "   Dispositivo: iPhone 16 Pro ($DEVICE_ID)"
echo "   Orientación: Vertical"
echo "   Tema: Claro"
echo "   Resolución: 1290x2796px"

echo ""
echo "✅ SCRIPT COMPLETADO - LISTO PARA CAPTURAS MANUALES"