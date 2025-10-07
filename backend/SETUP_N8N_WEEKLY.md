# 🔄 Configuración n8n para Horóscopos Semanales

## 📋 Resumen

Esta guía te ayuda a configurar un workflow en n8n que genere automáticamente horóscopos semanales todos los lunes a las 6 AM usando ChatGPT/OpenAI.

## 🔑 Tu API Key de OpenAI

**API Key:** `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`

## 🚀 Pasos de Configuración

### 1. Configurar Credenciales OpenAI

1. En n8n, ve a **Settings > Credentials**
2. Crea nueva credencial: **OpenAI**
3. Nombre: `OpenAI_Weekly_Horoscopes`
4. API Key: Usa la API key de arriba
5. Guarda la credencial

### 2. Crear Nuevo Workflow

1. En n8n, crea un **New Workflow**
2. Nombre: `Weekly Horoscope Generator`
3. Descripción: `Generates weekly horoscopes every Monday at 6 AM`

### 3. Configurar Nodos del Workflow

#### Nodo 1: Cron Trigger
- **Tipo:** Cron
- **Nombre:** Weekly Cron (Monday 6 AM)
- **Expression:** `0 6 * * 1` (Lunes 6 AM)
- **Timezone:** Tu zona horaria local

#### Nodo 2: Set Week Dates  
- **Tipo:** Set
- **Nombre:** Calculate Week Dates
- **Valores:**
  ```json
  {
    "week_start": "={{ DateTime.now().startOf('week').toFormat('yyyy-MM-dd') }}",
    "week_end": "={{ DateTime.now().endOf('week').toFormat('yyyy-MM-dd') }}",
    "generation_date": "={{ DateTime.now().toFormat('yyyy-MM-dd') }}"
  }
  ```

#### Nodo 3: Create Combinations
- **Tipo:** Set  
- **Nombre:** Create Sign-Language Combinations
- **Configuración:** Copia las 72 combinaciones desde `n8n_weekly_workflow.json`

#### Nodo 4: Split in Batches
- **Tipo:** SplitInBatches
- **Nombre:** Process Each Combination
- **Batch Size:** 1
- **Options:** Reset después de completar

#### Nodo 5: Prepare OpenAI Input
- **Tipo:** Set
- **Nombre:** Prepare OpenAI Input  
- **Valores:** Mapear los datos de cada combinación

#### Nodo 6: OpenAI Generation
- **Tipo:** OpenAI
- **Nombre:** Generate Weekly Horoscope
- **Configuración:**
  - **Model:** gpt-4 (o gpt-3.5-turbo si prefieres)
  - **Temperature:** 0.8
  - **Max Tokens:** 1200
  - **System Message:** Copia todo el contenido de `weekly_prompt.txt`
  - **User Message:** "Generate weekly horoscope for {{ $json.sign }} in {{ $json.languageName }}"
  - **Credentials:** Usa la credencial creada en paso 1

#### Nodo 7: Parse JSON Response
- **Tipo:** Set
- **Nombre:** Parse JSON Response
- **JavaScript Code:**
  ```javascript
  return [{ json: JSON.parse($json.message.content) }];
  ```

#### Nodo 8: Send to Backend
- **Tipo:** HTTP Request
- **Nombre:** Send to Backend
- **Configuración:**
  - **Method:** POST
  - **URL:** `https://tu-backend-railway.com/api/coaching/notify`
  - **Headers:** `Content-Type: application/json`
  - **Body:**
    ```json
    {
      "type": "weekly",
      "horoscopes": "={{ $json }}"
    }
    ```

### 4. Conectar los Nodos

Conecta los nodos en este orden:
1. Cron Trigger → Calculate Week Dates
2. Calculate Week Dates → Create Combinations  
3. Create Combinations → Split in Batches
4. Split in Batches → Prepare OpenAI Input
5. Prepare OpenAI Input → OpenAI Generation
6. OpenAI Generation → Parse JSON Response  
7. Parse JSON Response → Send to Backend

### 5. Configurar tu Backend URL

**Importante:** Reemplaza `https://tu-backend-railway.com` con tu URL real de Railway.

Para obtener tu URL:
1. Ve a Railway Dashboard
2. Selecciona tu proyecto
3. Copia la URL del deployment
4. Reemplázala en el nodo "Send to Backend"

## 🧪 Pruebas

### Prueba Manual
1. En n8n, ejecuta el workflow manualmente
2. Verifica que genere los 72 horóscopos semanales
3. Confirma que lleguen a tu backend

### Verificar Backend
```bash
# Verificar que llegaron los datos semanales
curl "https://tu-backend-railway.com/api/weekly/getAllWeeklyHoroscopes?lang=es"

# Verificar health del sistema
curl "https://tu-backend-railway.com/api/admin/health?admin_key=TU_ADMIN_KEY"
```

## 📊 Estructura del Payload Enviado

El workflow enviará este formato al backend:

```json
{
  "type": "weekly",
  "horoscopes": [
    {
      "sign": "Aries",
      "language_code": "es",
      "week_start": "2025-08-25",
      "week_end": "2025-08-31", 
      "weekly_theme": "Transformación y nuevas oportunidades",
      "cosmic_overview": "Las energías planetarias favorecen cambios positivos...",
      "general": "Esta semana marca un período de...",
      "love": "En el ámbito amoroso...",
      "health": "Tu bienestar físico...",
      "money": "Las finanzas personales...",
      "career": "En el trabajo...",
      "spirituality": "Tu crecimiento espiritual...",
      "weekly_challenge": "El principal reto será...",
      "weekly_opportunity": "La mejor oportunidad...",
      "best_days": ["Lunes", "Jueves"],
      "energy_level": 8,
      "luck_rating": 6,
      "lucky_numbers": [7, 23, 41, 88],
      "lucky_colors": ["Dorado", "Verde", "Azul"],
      "power_mantra": "Confío en mi capacidad de crear cambios positivos",
      "key_advice": "Mantente abierto a las nuevas oportunidades que se presenten",
      "content_type": "weekly_cosmic_coaching",
      "generated_at": "2025-08-26"
    }
    // ... 71 combinaciones más
  ]
}
```

## ⚙️ Configuraciones Recomendadas

### Para OpenAI API
- **Model:** `gpt-4` (mejor calidad) o `gpt-3.5-turbo` (más económico)
- **Temperature:** `0.8` (creatividad balanceada)
- **Max Tokens:** `1200` (suficiente para el contenido semanal)

### Para el Cron Job
- **Hora:** 6:00 AM (antes que el workflow diario)
- **Día:** Lunes (inicio de semana)
- **Timezone:** Tu zona horaria local

## 🚨 Monitoreo y Alertas

### Verificación Automática
El backend detectará automáticamente si faltan horóscopos semanales y:
- Enviará alertas via webhook (si configurado)
- Permitirá recovery manual via admin panel

### Verificación Manual
```bash
# Verificar cobertura semanal
curl "https://tu-backend-railway.com/api/weekly/checkMissing?admin_key=TU_ADMIN_KEY"

# Forzar generación si hay faltantes  
curl -X POST "https://tu-backend-railway.com/api/admin/force-weekly?admin_key=TU_ADMIN_KEY"
```

## 💰 Consideraciones de Costos

### Estimación OpenAI API
- **72 horóscopos semanales** × **4 semanas/mes** = **288 requests/mes**
- **Costo estimado:** $15-25 USD/mes (usando GPT-4)
- **Alternativa económica:** Usar GPT-3.5-turbo (~$5-8 USD/mes)

### Optimización
- Usa `gpt-3.5-turbo` para reducir costos
- Ajusta `max_tokens` si necesitas contenido más corto
- Considera combinar algunos idiomas si el presupuesto es limitado

## ✅ Checklist Final

- [ ] Credenciales OpenAI configuradas
- [ ] Workflow creado con todos los nodos
- [ ] URL del backend actualizada
- [ ] Prompt semanal copiado correctamente
- [ ] Cron job configurado para lunes 6 AM
- [ ] Prueba manual ejecutada exitosamente
- [ ] Backend recibiendo datos correctamente
- [ ] Monitoreo configurado

## 🆘 Troubleshooting

### Problema: OpenAI devuelve error
- Verifica que la API key sea válida
- Confirma que tienes créditos en OpenAI
- Reduce `max_tokens` si hay límite

### Problema: Backend no recibe datos
- Verifica la URL del backend
- Confirma que el backend esté ejecutándose
- Revisa los logs de Railway

### Problema: JSON inválido
- Revisa el prompt para asegurar formato correcto
- Añade validación JSON en n8n
- Usa temperatura más baja (0.5-0.6)

---

**🌟 ¡Tu sistema de horóscopos semanales está listo para funcionar todos los lunes a las 6 AM!**