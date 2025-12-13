# 💰 ANÁLISIS DE COSTOS - COSMIC COACH

**Fecha:** 22 Nov 2025
**API:** OpenAI GPT-4 (asumido)
**Límites actuales:** 100 mensajes/día por usuario

---

## 📊 ESCENARIOS DE USO

### Escenario 1: Usuario Casual
**Perfil:** Usa Cosmic Coach 2-3 veces por semana
- **Mensajes/día:** 5 mensajes
- **Mensajes/mes:** ~65 mensajes (5 × 13 días activos)

### Escenario 2: Usuario Activo
**Perfil:** Usa Cosmic Coach diariamente
- **Mensajes/día:** 20 mensajes
- **Mensajes/mes:** ~600 mensajes (20 × 30 días)

### Escenario 3: Usuario Power (límite máximo)
**Perfil:** Usa el límite completo diario
- **Mensajes/día:** 100 mensajes (límite actual)
- **Mensajes/mes:** ~3,000 mensajes (100 × 30 días)

---

## 💵 COSTOS POR MODELO DE OPENAI

### Opción 1: GPT-4o (recomendado para producción)
**Precio (Dic 2024):**
- Input: $2.50 / 1M tokens
- Output: $10.00 / 1M tokens

**Tokens promedio por conversación:**
- Prompt del sistema: ~500 tokens
- Mensaje del usuario: ~50 tokens
- Contexto (horóscopo datos): ~200 tokens
- Respuesta del AI: ~300 tokens
- **Total por mensaje:** ~1,050 tokens
  - Input: ~750 tokens
  - Output: ~300 tokens

**Costo por mensaje:**
- Input: 750 tokens × $2.50 / 1M = $0.001875
- Output: 300 tokens × $10.00 / 1M = $0.003000
- **Total: ~$0.0049 por mensaje** (medio centavo USD)

---

### Opción 2: GPT-4o-mini (más económico)
**Precio (Dic 2024):**
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens

**Tokens promedio:** Igual que GPT-4o (~1,050 tokens)

**Costo por mensaje:**
- Input: 750 tokens × $0.150 / 1M = $0.0001125
- Output: 300 tokens × $0.600 / 1M = $0.0001800
- **Total: ~$0.00029 por mensaje** (0.03 centavos USD)

---

### Opción 3: GPT-3.5-turbo (legacy, no recomendado)
**Precio:**
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens

**Costo por mensaje:** ~$0.00082

---

## 💰 COSTOS MENSUALES POR USUARIO

### Con GPT-4o ($0.0049/mensaje):

| Tipo Usuario | Mensajes/mes | Costo/mes/usuario |
|-------------|-------------|------------------|
| Casual      | 65          | **$0.32**        |
| Activo      | 600         | **$2.94**        |
| Power       | 3,000       | **$14.70**       |

### Con GPT-4o-mini ($0.00029/mensaje):

| Tipo Usuario | Mensajes/mes | Costo/mes/usuario |
|-------------|-------------|------------------|
| Casual      | 65          | **$0.019**       |
| Activo      | 600         | **$0.174**       |
| Power       | 3,000       | **$0.870**       |

---

## 📈 COSTOS TOTALES POR BASE DE USUARIOS

### Escenario A: 100 usuarios activos/día
**Distribución:**
- 50% Casual (50 usuarios) → 65 msg/mes
- 40% Activo (40 usuarios) → 600 msg/mes
- 10% Power (10 usuarios) → 3,000 msg/mes

**Mensajes totales/mes:**
- Casual: 50 × 65 = 3,250
- Activo: 40 × 600 = 24,000
- Power: 10 × 3,000 = 30,000
- **TOTAL: 57,250 mensajes/mes**

**Costos mensuales:**
- **GPT-4o:** 57,250 × $0.0049 = **$280.52/mes**
- **GPT-4o-mini:** 57,250 × $0.00029 = **$16.60/mes**

---

### Escenario B: 500 usuarios activos/día
**Distribución:**
- 50% Casual (250) → 65 msg/mes
- 40% Activo (200) → 600 msg/mes
- 10% Power (50) → 3,000 msg/mes

**Mensajes totales/mes:**
- Casual: 250 × 65 = 16,250
- Activo: 200 × 600 = 120,000
- Power: 50 × 3,000 = 150,000
- **TOTAL: 286,250 mensajes/mes**

**Costos mensuales:**
- **GPT-4o:** 286,250 × $0.0049 = **$1,402.62/mes**
- **GPT-4o-mini:** 286,250 × $0.00029 = **$83.01/mes**

---

### Escenario C: 1,000 usuarios activos/día
**Mensajes totales/mes:** ~572,500 mensajes

**Costos mensuales:**
- **GPT-4o:** **$2,805.25/mes**
- **GPT-4o-mini:** **$166.02/mes**

---

### Escenario D: 10,000 usuarios activos/día (éxito masivo)
**Mensajes totales/mes:** ~5,725,000 mensajes

**Costos mensuales:**
- **GPT-4o:** **$28,052.50/mes** ($336,630/año)
- **GPT-4o-mini:** **$1,660.25/mes** ($19,923/año)

---

## 🎯 RECOMENDACIONES

### 1. Usar GPT-4o-mini como default ✅
**Razones:**
- 17× más barato que GPT-4o
- Calidad suficiente para conversaciones de horóscopo
- Escalable hasta 10,000 usuarios por solo ~$1,660/mes
- Permite crecimiento sin preocupación por costos

**Cuando usar GPT-4o:**
- Usuarios premium de pago
- Conversaciones complejas (chart natal analysis)
- Testing de calidad

---

### 2. Implementar Rate Limiting Inteligente

**Free Tier:**
- Límite: 30 mensajes/día
- Costo máximo/usuario/mes: $0.26 (GPT-4o-mini)

**Premium Tier:**
- Límite: 100 mensajes/día
- Costo máximo/usuario/mes: $0.87 (GPT-4o-mini)
- Precio sugerido: $4.99/mes → Margen 82%

---

### 3. Optimizar Tokens

**Actualmente:** ~1,050 tokens/mensaje

**Optimizaciones posibles:**
- ✅ Reducir system prompt (500 → 300 tokens) = -200 tokens
- ✅ Cachear horóscopo data del día = -150 tokens
- ✅ Comprimir contexto histórico = -100 tokens
- **Nuevo total:** ~600 tokens/mensaje (-43%)

**Impacto:**
- GPT-4o: $0.0049 → **$0.0028** (-43%)
- GPT-4o-mini: $0.00029 → **$0.00017** (-43%)

---

## 📊 COMPARACIÓN CON REVENUE

### Modelo Premium: $4.99/mes

**Usuario Premium promedio:**
- Usa ~600 mensajes/mes (activo)
- Costo API: $0.174 (GPT-4o-mini)
- **Margen: $4.82** (96.5%)

**Con 1,000 usuarios premium:**
- Revenue: $4,990/mes
- Costo API: ~$174/mes
- **Ganancia neta: $4,816/mes** (96.5% margen)

### Con optimización de tokens:
- Costo API: ~$100/mes
- **Ganancia neta: $4,890/mes** (98% margen)

---

## 🚨 ALERTAS DE COSTO

### Límite diario sugerido (seguridad):
**Si usas GPT-4o-mini:**
- 100,000 mensajes/día = $29/día = ~$870/mes
- Alerta en 75,000 mensajes/día ($22/día)

**Si usas GPT-4o:**
- 10,000 mensajes/día = $49/día = ~$1,470/mes
- Alerta en 7,500 mensajes/día ($37/día)

---

## 💡 ESTRATEGIA HÍBRIDA (RECOMENDADO)

### Tier 1: Free Users
- Modelo: **GPT-4o-mini**
- Límite: 10 mensajes/día
- Costo: $0.087/mes/usuario
- Objetivo: Conversión a premium

### Tier 2: Premium Users
- Modelo: **GPT-4o-mini**
- Límite: 100 mensajes/día
- Costo: $0.87/mes/usuario
- Precio: $4.99/mes
- Margen: 82%

### Tier 3: VIP/Elite (futuro)
- Modelo: **GPT-4o** (mejor calidad)
- Límite: 200 mensajes/día
- Costo: $29.40/mes/usuario
- Precio: $49.99/mes
- Margen: 41%

---

## 📈 PROYECCIÓN DE CRECIMIENTO

### Año 1 (conservador):
- Mes 1-3: 100 usuarios → $17/mes
- Mes 4-6: 500 usuarios → $83/mes
- Mes 7-9: 1,000 usuarios → $166/mes
- Mes 10-12: 2,000 usuarios → $332/mes
- **Promedio año 1:** ~$150/mes en costos API

### Año 2 (crecimiento):
- 10,000 usuarios activos
- **Costo mensual:** $1,660 (GPT-4o-mini)
- Con 20% premium ($4.99/mes): **$9,980/mes revenue**
- **Ganancia neta:** $8,320/mes

---

## ✅ CONCLUSIÓN

### Costos muy manejables con GPT-4o-mini:

| Usuarios Activos | Costo Mensual | Revenue (20% premium) | Ganancia |
|-----------------|---------------|----------------------|----------|
| 100             | $17           | $100                 | $83      |
| 500             | $83           | $499                 | $416     |
| 1,000           | $166          | $998                 | $832     |
| 5,000           | $830          | $4,990               | $4,160   |
| 10,000          | $1,660        | $9,980               | $8,320   |

### Recomendación final:
1. ✅ **Usar GPT-4o-mini** para todos los usuarios
2. ✅ **Free tier:** 10 mensajes/día
3. ✅ **Premium tier:** 100 mensajes/día a $4.99/mes
4. ✅ **Optimizar tokens** para reducir costos 40%
5. ✅ **Monitorear uso** con alertas en $500/mes

**Con esta estrategia, los costos de API son insignificantes comparados con el revenue potencial.**

---

**Última actualización:** 2025-11-22
**Precios basados en:** OpenAI pricing Dic 2024
**Nota:** Precios pueden cambiar, revisar mensualmente
