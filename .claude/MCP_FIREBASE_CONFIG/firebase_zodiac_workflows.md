# 🔥 FLUJOS DE TRABAJO FIREBASE PARA PROYECTO ZODIAC

## Herramientas MCP Firebase Disponibles

### 🗄️ Firestore Database
```bash
# Listar colecciones
mcp6_firestore_list_collections

# Obtener documento específico
mcp6_firestore_get_document --collection="users" --id="user123"

# Agregar nuevo documento
mcp6_firestore_add_document --collection="horoscopes" --data='{"sign":"aries","date":"2025-01-17","content":"Tu día será..."}'

# Actualizar documento existente
mcp6_firestore_update_document --collection="users" --id="user123" --data='{"premium":true}'

# Eliminar documento
mcp6_firestore_delete_document --collection="temp_data" --id="old_record"

# Consultar documentos con filtros
mcp6_firestore_list_documents --collection="horoscopes" --filters='[{"field":"sign","operator":"==","value":"leo"}]'
```

### 📁 Firebase Storage
```bash
# Listar archivos en Storage
mcp6_storage_list_files --directoryPath="images/zodiac_signs"

# Obtener información de archivo
mcp6_storage_get_file_info --filePath="images/zodiac_signs/aries.png"

# Subir archivo desde URL
mcp6_storage_upload_from_url --url="https://example.com/image.jpg" --filePath="images/new_image.jpg"

# Subir archivo local
mcp6_storage_upload --content="/path/to/local/file.pdf" --filePath="documents/user_guide.pdf"
```

### 👤 Firebase Authentication
```bash
# Obtener usuario por ID
mcp6_auth_get_user --identifier="user123"

# Obtener usuario por email
mcp6_auth_get_user --identifier="usuario@example.com"
```

## Casos de Uso Específicos del Proyecto Zodiac

### 1. Gestión de Horóscopos
```bash
# Crear horóscopo diario
mcp6_firestore_add_document \
  --collection="daily_horoscopes" \
  --data='{
    "sign": "aries",
    "date": "2025-01-17",
    "language": "es",
    "content": "Hoy es un día perfecto para...",
    "generated_at": "2025-01-17T12:00:00Z",
    "ai_model": "gpt-4"
  }'

# Consultar horóscopos por signo y fecha
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[
    {"field":"sign","operator":"==","value":"leo"},
    {"field":"date","operator":"==","value":"2025-01-17"}
  ]'
```

### 2. Gestión de Usuarios Premium
```bash
# Actualizar usuario a premium
mcp6_firestore_update_document \
  --collection="users" \
  --id="user123" \
  --data='{
    "premium_tier": "cosmic_premium",
    "premium_expires": "2025-12-31T23:59:59Z",
    "features_unlocked": ["advanced_compatibility", "ai_insights", "cosmic_coach"]
  }'

# Consultar usuarios premium
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[{"field":"premium_tier","operator":"!=","value":"free"}]'
```

### 3. Análisis de Compatibilidad
```bash
# Guardar resultado de compatibilidad
mcp6_firestore_add_document \
  --collection="compatibility_analyses" \
  --data='{
    "user1_sign": "aries",
    "user2_sign": "leo",
    "compatibility_score": 85,
    "analysis": "Excelente compatibilidad de fuego...",
    "generated_at": "2025-01-17T12:00:00Z",
    "language": "es"
  }'
```

### 4. Gestión de Assets Zodiacales
```bash
# Subir íconos de signos zodiacales
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/aries.svg" \
  --filePath="assets/signs/aries.svg" \
  --contentType="image/svg+xml"

# Subir fondos cósmicos
mcp6_storage_upload_from_url \
  --url="https://cdn.zodiac.com/cosmic_bg.jpg" \
  --filePath="assets/backgrounds/cosmic_bg.jpg" \
  --contentType="image/jpeg"
```

### 5. Analytics y Métricas
```bash
# Crear registro de uso de funcionalidad
mcp6_firestore_add_document \
  --collection="analytics" \
  --data='{
    "user_id": "user123",
    "action": "compatibility_analysis",
    "timestamp": "2025-01-17T12:00:00Z",
    "metadata": {
      "signs": ["aries", "leo"],
      "premium_feature": true
    }
  }'

# Consultar métricas por fecha
mcp6_firestore_list_documents \
  --collection="analytics" \
  --filters='[
    {"field":"timestamp","operator":">=","value":"2025-01-17T00:00:00Z"},
    {"field":"timestamp","operator":"<","value":"2025-01-18T00:00:00Z"}
  ]'
```

## Estructura de Datos Recomendada

### Colecciones Principales
```
📁 users/
  └── {userId}/
      ├── profile: {sign, birth_date, language, timezone}
      ├── premium: {tier, expires, features}
      └── preferences: {notifications, theme, language}

📁 daily_horoscopes/
  └── {date}_{sign}_{language}/
      ├── content: string
      ├── generated_at: timestamp
      └── ai_model: string

📁 weekly_horoscopes/
  └── {week_start}_{sign}_{language}/
      ├── content: string
      ├── week_range: {start, end}
      └── generated_at: timestamp

📁 compatibility_analyses/
  └── {analysisId}/
      ├── signs: [sign1, sign2]
      ├── score: number
      ├── analysis: string
      └── created_at: timestamp

📁 ai_insights/
  └── {insightId}/
      ├── user_id: string
      ├── type: "cosmic_coach" | "relationship" | "career"
      ├── content: string
      └── generated_at: timestamp
```

## Comandos de Mantenimiento

### Limpieza de Datos Antiguos
```bash
# Eliminar horóscopos antiguos (más de 30 días)
mcp6_firestore_list_documents \
  --collection="daily_horoscopes" \
  --filters='[{"field":"generated_at","operator":"<","value":"2024-12-18T00:00:00Z"}]'

# Luego eliminar cada documento encontrado
mcp6_firestore_delete_document --collection="daily_horoscopes" --id="{documentId}"
```

### Backup de Datos Críticos
```bash
# Exportar configuraciones de usuarios premium
mcp6_firestore_list_documents \
  --collection="users" \
  --filters='[{"field":"premium_tier","operator":"!=","value":"free"}]' \
  --limit=1000
```

## Integración con Backend Node.js

El servidor MCP Firebase puede trabajar en paralelo con tu backend Node.js existente:

- **Backend Node.js**: Generación automática de horóscopos, cron jobs, APIs REST
- **MCP Firebase**: Gestión manual de datos, análisis, mantenimiento, debugging

Ambos sistemas pueden acceder a la misma base de datos Firebase sin conflictos.
