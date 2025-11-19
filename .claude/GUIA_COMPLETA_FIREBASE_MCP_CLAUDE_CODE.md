# 🔥 GUÍA COMPLETA: CONFIGURACIÓN FIREBASE MCP PARA CLAUDE CODE

## 📋 RESUMEN EJECUTIVO

Esta guía te permite configurar Claude Code para manejar Firebase del proyecto zodiac usando el protocolo MCP (Model Context Protocol). Una vez configurado, podrás gestionar Firestore, Storage, Auth y otros servicios Firebase directamente desde Claude Code.

**Proyecto Firebase**: `zodi-a1658`  
**Servicios Disponibles**: Firestore Database, Firebase Storage, Firebase Auth, Firebase Messaging  
**Tiempo de Configuración**: 10-15 minutos  

---

## 🎯 ¿QUÉ LOGRARÁS?

Después de esta configuración, Claude Code podrá:

✅ **Gestionar Firestore Database**
- Crear, leer, actualizar y eliminar documentos
- Consultar colecciones con filtros avanzados
- Gestionar horóscopos diarios y semanales
- Administrar usuarios premium y analytics

✅ **Manejar Firebase Storage**
- Subir y descargar archivos
- Gestionar assets zodiacales (íconos, fondos)
- Obtener URLs de descarga
- Organizar estructura de carpetas

✅ **Administrar Firebase Auth**
- Consultar usuarios por ID o email
- Verificar estados de autenticación
- Gestionar perfiles de usuario

---

## 🚀 CONFIGURACIÓN PASO A PASO

### Paso 1: Obtener Credenciales Firebase Admin SDK

1. **Ve a Firebase Console**:
   ```
   https://console.firebase.google.com/project/zodi-a1658/settings/serviceaccounts/adminsdk
   ```

2. **Genera nueva clave privada**:
   - Haz clic en "Generar nueva clave privada"
   - Se descargará un archivo JSON con las credenciales

3. **Guarda las credenciales**:
   ```bash
   # Crear directorio para credenciales
   mkdir -p ~/.config/firebase
   
   # Mover el archivo descargado (renómbralo apropiadamente)
   mv ~/Downloads/zodi-a1658-firebase-adminsdk-xxxxx.json ~/.config/firebase/zodi-a1658-service-account.json
   ```

### Paso 2: Configurar Claude Desktop

1. **Crear directorio de configuración**:
   ```bash
   mkdir -p ~/Library/Application\ Support/Claude
   ```

2. **Crear archivo de configuración MCP**:
   ```bash
   cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
   {
     "mcpServers": {
       "firebase-zodiac": {
         "command": "npx",
         "args": ["@firebase/mcp-server"],
         "env": {
           "FIREBASE_PROJECT_ID": "zodi-a1658",
           "FIREBASE_STORAGE_BUCKET": "zodi-a1658.firebasestorage.app",
           "FIREBASE_AUTH_DOMAIN": "zodi-a1658.firebaseapp.com",
           "FIREBASE_MESSAGING_SENDER_ID": "764873916666",
           "GOOGLE_APPLICATION_CREDENTIALS": "/Users/$(whoami)/.config/firebase/zodi-a1658-service-account.json"
         }
       }
     }
   }
   EOF
   ```

3. **Reiniciar Claude Desktop**:
   - Cierra completamente Claude Desktop
   - Vuelve a abrirlo
   - Verifica que aparezca el servidor MCP en la configuración

### Paso 3: Verificar Instalación

1. **Probar conexión básica**:
   ```
   Comando: mcp6_firestore_list_collections
   Resultado esperado: Lista de colecciones en Firestore
   ```

2. **Verificar permisos**:
   ```
   Comando: mcp6_storage_list_files
   Resultado esperado: Lista de archivos en Storage (puede estar vacío)
   ```

---

## 🛠️ HERRAMIENTAS MCP DISPONIBLES

### 🗄️ Firestore Database

#### Gestión de Colecciones
```bash
# Listar todas las colecciones
mcp6_firestore_list_collections

# Listar documentos de una colección
mcp6_firestore_list_documents --collection="users"

# Listar con filtros
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[{"field":"sign","operator":"==","value":"aries"}]' \
  --limit=10
```

#### Gestión de Documentos
```bash
# Obtener documento específico
mcp6_firestore_get_document --collection="users" --id="user123"

# Crear nuevo documento
mcp6_firestore_add_document \
  --collection="daily_horoscopes" \
  --data='{
    "sign": "aries",
    "date": "2025-01-17",
    "language": "es",
    "content": "Hoy es un día perfecto para nuevos comienzos..."
  }'

# Actualizar documento existente
mcp6_firestore_update_document \
  --collection="users" \
  --id="user123" \
  --data='{"premium_tier": "cosmic_premium", "last_login": "2025-01-17T13:00:00Z"}'

# Eliminar documento
mcp6_firestore_delete_document --collection="temp_data" --id="old_record"
```

#### Consultas Avanzadas
```bash
# Consulta con múltiples filtros
mcp6_firestore_list_documents \
  --collection="compatibility_analyses" \
  --filters='[
    {"field":"user1_sign","operator":"==","value":"leo"},
    {"field":"compatibility_score","operator":">=","value":"80"}
  ]' \
  --orderBy='[{"field":"created_at","direction":"desc"}]' \
  --limit=5

# Consulta por rango de fechas
mcp6_firestore_list_documents \
  --collection="analytics" \
  --filters='[
    {"field":"timestamp","operator":">=","value":"2025-01-17T00:00:00Z"},
    {"field":"timestamp","operator":"<","value":"2025-01-18T00:00:00Z"}
  ]'
```

### 📁 Firebase Storage

#### Gestión de Archivos
```bash
# Listar archivos en directorio raíz
mcp6_storage_list_files

# Listar archivos en directorio específico
mcp6_storage_list_files --directoryPath="images/zodiac_signs"

# Obtener información de archivo
mcp6_storage_get_file_info --filePath="assets/signs/aries.svg"
```

#### Subida de Archivos
```bash
# Subir desde URL externa
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/aries.svg" \
  --filePath="assets/signs/aries.svg" \
  --contentType="image/svg+xml"

# Subir archivo local
mcp6_storage_upload \
  --content="/path/to/local/file.pdf" \
  --filePath="documents/user_guide.pdf" \
  --contentType="application/pdf"

# Subir con metadatos
mcp6_storage_upload_from_url \
  --url="https://example.com/cosmic_bg.jpg" \
  --filePath="backgrounds/cosmic_bg.jpg" \
  --metadata='{"category":"background","theme":"cosmic","resolution":"1920x1080"}'
```

### 👤 Firebase Authentication

```bash
# Obtener usuario por ID
mcp6_auth_get_user --identifier="user123"

# Obtener usuario por email
mcp6_auth_get_user --identifier="usuario@example.com"
```

---

## 🎯 CASOS DE USO ESPECÍFICOS DEL PROYECTO ZODIAC

### 1. Gestión de Horóscopos Diarios

#### Crear Horóscopo
```bash
mcp6_firestore_add_document \
  --collection="daily_horoscopes" \
  --data='{
    "sign": "leo",
    "date": "2025-01-17",
    "language": "es",
    "content": "Los astros te favorecen hoy, Leo. Es momento de brillar con tu luz natural y liderar proyectos importantes. Tu carisma estará en su punto máximo.",
    "generated_at": "2025-01-17T13:00:00Z",
    "ai_model": "gpt-4",
    "keywords": ["liderazgo", "carisma", "proyectos"],
    "mood_score": 85
  }'
```

#### Consultar Horóscopos por Signo
```bash
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[
    {"field":"sign","operator":"==","value":"leo"},
    {"field":"date","operator":"==","value":"2025-01-17"}
  ]'
```

#### Actualizar Horóscopo Existente
```bash
mcp6_firestore_update_document \
  --collection="daily_horoscopes" \
  --id="2025-01-17_leo_es" \
  --data='{
    "content": "Contenido actualizado del horóscopo...",
    "updated_at": "2025-01-17T14:00:00Z",
    "version": 2
  }'
```

### 2. Gestión de Usuarios Premium

#### Actualizar Usuario a Premium
```bash
mcp6_firestore_update_document \
  --collection="users" \
  --id="user123" \
  --data='{
    "premium_tier": "cosmic_premium",
    "premium_expires": "2025-12-31T23:59:59Z",
    "features_unlocked": [
      "advanced_compatibility",
      "ai_insights",
      "cosmic_coach",
      "weekly_forecasts"
    ],
    "upgraded_at": "2025-01-17T13:00:00Z"
  }'
```

#### Consultar Usuarios Premium
```bash
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[{"field":"premium_tier","operator":"!=","value":"free"}]' \
  --orderBy='[{"field":"premium_expires","direction":"asc"}]'
```

#### Verificar Expiración de Premium
```bash
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[
    {"field":"premium_tier","operator":"!=","value":"free"},
    {"field":"premium_expires","operator":"<","value":"2025-02-01T00:00:00Z"}
  ]'
```

### 3. Análisis de Compatibilidad

#### Guardar Análisis de Compatibilidad
```bash
mcp6_firestore_add_document \
  --collection="compatibility_analyses" \
  --data='{
    "user1_sign": "aries",
    "user2_sign": "leo",
    "compatibility_score": 92,
    "analysis": "Excelente compatibilidad entre signos de fuego. Ambos comparten pasión, energía y determinación. La relación será dinámica y llena de aventuras.",
    "detailed_analysis": {
      "love_compatibility": 90,
      "friendship_compatibility": 95,
      "work_compatibility": 88,
      "communication_score": 85
    },
    "strengths": ["Pasión compartida", "Energía similar", "Objetivos alineados"],
    "challenges": ["Competitividad", "Impulsividad", "Ego"],
    "advice": "Canalicen su energía hacia objetivos comunes y respeten los espacios individuales.",
    "generated_at": "2025-01-17T13:00:00Z",
    "language": "es"
  }'
```

#### Consultar Compatibilidades por Signo
```bash
mcp6_firestore_list_documents \
  --collection="compatibility_analyses" \
  --filters='[
    {"field":"user1_sign","operator":"==","value":"aries"}
  ]' \
  --orderBy='[{"field":"compatibility_score","direction":"desc"}]'
```

### 4. Gestión de Assets Zodiacales

#### Subir Íconos de Signos
```bash
# Aries
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/signs/aries.svg" \
  --filePath="assets/signs/aries.svg" \
  --contentType="image/svg+xml" \
  --metadata='{"sign":"aries","type":"icon","style":"modern"}'

# Leo
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/signs/leo.svg" \
  --filePath="assets/signs/leo.svg" \
  --contentType="image/svg+xml" \
  --metadata='{"sign":"leo","type":"icon","style":"modern"}'
```

#### Subir Fondos Cósmicos
```bash
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/backgrounds/cosmic_night.jpg" \
  --filePath="assets/backgrounds/cosmic_night.jpg" \
  --contentType="image/jpeg" \
  --metadata='{"category":"background","theme":"cosmic","resolution":"1920x1080"}'
```

#### Organizar Assets por Categorías
```bash
# Listar todos los íconos de signos
mcp6_storage_list_files --directoryPath="assets/signs"

# Listar fondos
mcp6_storage_list_files --directoryPath="assets/backgrounds"

# Listar sonidos (si los hay)
mcp6_storage_list_files --directoryPath="assets/sounds"
```

### 5. Analytics y Métricas

#### Registrar Uso de Funcionalidades
```bash
mcp6_firestore_add_document \
  --collection="analytics" \
  --data='{
    "user_id": "user123",
    "action": "compatibility_analysis",
    "timestamp": "2025-01-17T13:00:00Z",
    "metadata": {
      "signs": ["aries", "leo"],
      "premium_feature": true,
      "session_duration": 180,
      "device_type": "mobile"
    },
    "result": "success"
  }'
```

#### Consultar Métricas Diarias
```bash
mcp6_firestore_list_documents \
  --collection="analytics" \
  --filters='[
    {"field":"timestamp","operator":">=","value":"2025-01-17T00:00:00Z"},
    {"field":"timestamp","operator":"<","value":"2025-01-18T00:00:00Z"}
  ]' \
  --orderBy='[{"field":"timestamp","direction":"desc"}]'
```

#### Análisis de Funcionalidades Más Usadas
```bash
mcp6_firestore_list_documents \
  --collection="analytics" \
  --filters='[{"field":"action","operator":"==","value":"compatibility_analysis"}]' \
  --limit=100
```

---

## 📊 ESTRUCTURA DE DATOS RECOMENDADA

### Colecciones Principales

#### `users/`
```json
{
  "user_id": "user123",
  "profile": {
    "sign": "aries",
    "birth_date": "1990-04-15",
    "language": "es",
    "timezone": "America/Mexico_City"
  },
  "premium": {
    "tier": "cosmic_premium",
    "expires": "2025-12-31T23:59:59Z",
    "features": ["advanced_compatibility", "ai_insights", "cosmic_coach"]
  },
  "preferences": {
    "notifications": true,
    "theme": "dark",
    "language": "es"
  },
  "created_at": "2025-01-01T00:00:00Z",
  "last_login": "2025-01-17T13:00:00Z"
}
```

#### `daily_horoscopes/`
```json
{
  "id": "2025-01-17_aries_es",
  "sign": "aries",
  "date": "2025-01-17",
  "language": "es",
  "content": "Contenido del horóscopo...",
  "keywords": ["energía", "nuevos_comienzos", "liderazgo"],
  "mood_score": 85,
  "generated_at": "2025-01-17T06:00:00Z",
  "ai_model": "gpt-4"
}
```

#### `weekly_horoscopes/`
```json
{
  "id": "2025-W03_leo_es",
  "sign": "leo",
  "week_start": "2025-01-13",
  "week_end": "2025-01-19",
  "language": "es",
  "content": "Pronóstico semanal...",
  "themes": ["creatividad", "relaciones", "trabajo"],
  "generated_at": "2025-01-13T05:30:00Z"
}
```

#### `compatibility_analyses/`
```json
{
  "id": "analysis_123",
  "user1_sign": "aries",
  "user2_sign": "leo",
  "compatibility_score": 92,
  "analysis": "Análisis detallado...",
  "detailed_scores": {
    "love": 90,
    "friendship": 95,
    "work": 88
  },
  "created_at": "2025-01-17T13:00:00Z",
  "language": "es"
}
```

#### `ai_insights/`
```json
{
  "id": "insight_456",
  "user_id": "user123",
  "type": "cosmic_coach",
  "content": "Consejo personalizado...",
  "category": "relationships",
  "generated_at": "2025-01-17T13:00:00Z",
  "expires_at": "2025-01-24T13:00:00Z"
}
```

#### `analytics/`
```json
{
  "id": "event_789",
  "user_id": "user123",
  "action": "horoscope_view",
  "timestamp": "2025-01-17T13:00:00Z",
  "metadata": {
    "sign": "aries",
    "type": "daily",
    "session_id": "sess_123"
  }
}
```

---

## 🔧 COMANDOS DE MANTENIMIENTO

### Limpieza de Datos Antiguos

#### Eliminar Horóscopos Antiguos (>30 días)
```bash
# 1. Consultar horóscopos antiguos
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[{"field":"generated_at","operator":"<","value":"2024-12-18T00:00:00Z"}]'

# 2. Eliminar cada documento encontrado
mcp6_firestore_delete_document --collection="daily_horoscopes" --id="documento_id"
```

#### Limpiar Analytics Antiguos (>90 días)
```bash
mcp6_firestore_list_documents \
  --collection="analytics" \
  --filters='[{"field":"timestamp","operator":"<","value":"2024-10-18T00:00:00Z"}]'
```

### Backup de Datos Críticos

#### Exportar Usuarios Premium
```bash
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[{"field":"premium_tier","operator":"!=","value":"free"}]' \
  --limit=1000
```

#### Exportar Configuraciones del Sistema
```bash
mcp6_firestore_list_documents --collection="system_config"
```

### Monitoreo de Salud del Sistema

#### Verificar Cobertura de Horóscopos Diarios
```bash
# Verificar que todos los signos tengan horóscopo para hoy
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[{"field":"date","operator":"==","value":"2025-01-17"}]'
```

#### Verificar Usuarios Activos
```bash
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[{"field":"last_login","operator":">=","value":"2025-01-10T00:00:00Z"}]'
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "Firebase project not found"
```bash
# Verificar variables de entorno
echo $FIREBASE_PROJECT_ID
echo $GOOGLE_APPLICATION_CREDENTIALS

# Verificar que el archivo de credenciales existe
ls -la ~/.config/firebase/zodi-a1658-service-account.json
```

### Error: "Permission denied"
```bash
# Verificar permisos del archivo de credenciales
chmod 600 ~/.config/firebase/zodi-a1658-service-account.json

# Verificar que el archivo JSON tiene la estructura correcta
cat ~/.config/firebase/zodi-a1658-service-account.json | jq .project_id
```

### Error: "MCP server not found"
```bash
# Verificar configuración de Claude Desktop
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Reiniciar Claude Desktop completamente
```

### Error: "Collection not found"
```bash
# Crear colección si no existe
mcp6_firestore_add_document \
  --collection="nueva_coleccion" \
  --data='{"init": true, "created_at": "2025-01-17T13:00:00Z"}'
```

---

## 📚 RECURSOS ADICIONALES

### Documentación Firebase
- [Firebase Console](https://console.firebase.google.com/project/zodi-a1658)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Storage Documentation](https://firebase.google.com/docs/storage)

### Herramientas de Desarrollo
- [Firebase CLI](https://firebase.google.com/docs/cli)
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite)

### Monitoreo y Analytics
- [Firebase Performance Monitoring](https://console.firebase.google.com/project/zodi-a1658/performance)
- [Firebase Analytics](https://console.firebase.google.com/project/zodi-a1658/analytics)

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Configuración Inicial
- [ ] Credenciales Firebase Admin SDK descargadas
- [ ] Archivo de credenciales guardado en `~/.config/firebase/`
- [ ] Configuración MCP creada en Claude Desktop
- [ ] Claude Desktop reiniciado
- [ ] Conexión MCP verificada con `mcp6_firestore_list_collections`

### Funcionalidades Básicas
- [ ] Listar colecciones funciona
- [ ] Crear documento funciona
- [ ] Leer documento funciona
- [ ] Actualizar documento funciona
- [ ] Eliminar documento funciona
- [ ] Subir archivo a Storage funciona

### Casos de Uso Zodiac
- [ ] Crear horóscopo diario funciona
- [ ] Consultar horóscopos por signo funciona
- [ ] Gestionar usuarios premium funciona
- [ ] Guardar análisis de compatibilidad funciona
- [ ] Subir assets zodiacales funciona

---

## 🎉 ¡CONFIGURACIÓN COMPLETADA!

Una vez completados todos los pasos, Claude Code tendrá acceso completo a tu Firebase del proyecto zodiac. Podrás gestionar horóscopos, usuarios, análisis de compatibilidad y todos los datos de tu aplicación directamente desde la interfaz de Claude Code.

**¿Necesitas ayuda?** Consulta la sección de solución de problemas o revisa los logs de Claude Desktop para más detalles sobre cualquier error.

---

*Documento generado para el proyecto Zodiac - Firebase MCP Integration*  
*Versión: 1.0 | Fecha: 2025-01-17*
