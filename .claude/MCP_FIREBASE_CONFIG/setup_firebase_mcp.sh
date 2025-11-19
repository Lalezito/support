#!/bin/bash

# 🔥 CONFIGURACIÓN MCP FIREBASE PARA PROYECTO ZODIAC
# ================================================

echo "🚀 Configurando servidor MCP Firebase para proyecto zodiac..."

# Instalar el servidor MCP Firebase
echo "📦 Instalando servidor MCP Firebase..."
npm install -g @modelcontextprotocol/server-firebase

# Crear directorio para credenciales si no existe
mkdir -p ~/.config/firebase

# Copiar configuración a Claude Desktop
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
mkdir -p "$CLAUDE_CONFIG_DIR"

echo "📋 Copiando configuración a Claude Desktop..."
cp claude_desktop_config.json "$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo "✅ Configuración MCP Firebase completada!"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Obtén las credenciales de Firebase Admin SDK desde:"
echo "   https://console.firebase.google.com/project/zodi-a1658/settings/serviceaccounts/adminsdk"
echo ""
echo "2. Guarda el archivo JSON de credenciales como:"
echo "   ~/.config/firebase/zodi-a1658-service-account.json"
echo ""
echo "3. Reinicia Claude Desktop para cargar la configuración MCP"
echo ""
echo "4. Verifica la conexión usando: mcp6_firestore_list_collections"
echo ""
echo "🔐 VARIABLES DE ENTORNO CONFIGURADAS:"
echo "   - FIREBASE_PROJECT_ID: zodi-a1658"
echo "   - FIREBASE_STORAGE_BUCKET: zodi-a1658.firebasestorage.app"
echo "   - FIREBASE_AUTH_DOMAIN: zodi-a1658.firebaseapp.com"
echo "   - FIREBASE_MESSAGING_SENDER_ID: 764873916666"
