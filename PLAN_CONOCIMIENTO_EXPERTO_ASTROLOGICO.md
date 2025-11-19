# 🌟 PLAN: Sistema de Conocimiento Experto Astrológico

**Fecha:** 19 Nov 2025
**Objetivo:** Que GPT-4o-mini use conocimiento base + 72 piezas diarias como referencia permanente

---

## 🎯 ARQUITECTURA EN 3 CAPAS

### Capa 1: Librería Experta Permanente (Estática)
**Contenido:**
- Características detalladas de cada signo zodiacal
- Elementos (Fuego, Tierra, Aire, Agua)
- Planetas regentes y su influencia
- Casas astrológicas
- Aspectos planetarios
- Rituales por temporada
- Tono de voz y estilo de comunicación
- Frases típicas y vocabulario astrológico

**Implementación:**
```javascript
// backend/src/knowledge/astrology_base.js
const ASTROLOGY_KNOWLEDGE_BASE = {
  signs: {
    Capricornio: {
      element: "Tierra",
      ruling_planet: "Saturno",
      characteristics: "Ambicioso, disciplinado, práctico...",
      strengths: ["Responsable", "Disciplinado", "Autocontrol"],
      challenges: ["Pesimista", "Terco", "Desconfiado"],
      compatibility: {
        high: ["Tauro", "Virgo", "Escorpio", "Piscis"],
        medium: ["Cáncer", "Capricornio"],
        low: ["Aries", "Libra"]
      },
      career_guidance: "Excel en roles que requieren...",
      love_guidance: "En el amor, Capricornio busca...",
      wellness_tips: "Mantén equilibrio entre trabajo y...",
      lucky_elements: {
        colors: ["Verde oscuro", "Gris", "Marrón"],
        numbers: [4, 8, 13, 22],
        days: ["Sábado"],
        crystals: ["Granate", "Ónix", "Turmalina negra"]
      }
    },
    // ... los 12 signos
  },

  planets: {
    Saturno: {
      archetype: "El Maestro",
      represents: "Disciplina, estructura, karma",
      influence: "Lecciones, responsabilidad, límites"
    },
    // ... todos los planetas
  },

  houses: {
    1: { name: "Casa del Yo", represents: "Identidad, apariencia" },
    // ... 12 casas
  },

  coaching_style: {
    tone: "Empático, sabio, alentador",
    language: {
      es: {
        greetings: ["Las estrellas te saludan", "El cosmos te abraza"],
        transitions: ["Ahora bien", "Por otro lado", "Recuerda que"],
        encouragement: ["Confía en tu intuición", "El universo conspira a tu favor"]
      },
      en: {
        greetings: ["The stars greet you", "The cosmos embraces you"],
        transitions: ["Now then", "On the other hand", "Remember that"],
        encouragement: ["Trust your intuition", "The universe conspires in your favor"]
      }
    }
  }
};
```

**Storage:**
- **Archivo estático:** `knowledge/astrology_base.json` (cargado al arrancar backend)
- **Opcional futuro:** Embeddings en vector DB para búsqueda semántica

---

### Capa 2: Datos Diarios (72 Piezas Dinámicas)

**Contenido actual en `daily_horoscopes`:**
```sql
CREATE TABLE daily_horoscopes (
  id SERIAL PRIMARY KEY,
  zodiac_sign VARCHAR(20),
  date DATE,
  energy_level VARCHAR(20),     -- 'Alta', 'Media', 'Baja', 'Equilibrada'
  lucky_colors TEXT[],           -- ['Dorado', 'Naranja']
  favorable_times TEXT[],        -- ['14:00-16:00', '20:00-22:00']
  love_focus TEXT,               -- Guidance en idioma por defecto
  career_focus TEXT,
  wellness_focus TEXT,
  -- 6 idiomas × 12 signos = 72 entradas diarias
);
```

**Job automático para cargar 72 piezas:**
```javascript
// backend/src/jobs/daily_horoscope_generator.js
const cron = require('node-cron');

// Ejecutar a las 00:00 UTC cada día
cron.schedule('0 0 * * *', async () => {
  console.log('🌟 Generando 72 horóscopos diarios...');

  const signs = ['Aries', 'Tauro', 'Géminis', ...]; // 12 signos
  const languages = ['es', 'en', 'de', 'fr', 'it', 'pt']; // 6 idiomas

  for (const sign of signs) {
    // Obtener base knowledge del signo
    const signKnowledge = ASTROLOGY_KNOWLEDGE_BASE.signs[sign];

    // Calcular datos astronómicos del día
    const astronomicalData = calculateDailyAstronomy(sign, new Date());

    // Generar 6 versiones (una por idioma)
    for (const lang of languages) {
      const dailyHoroscope = await generateDailyHoroscope({
        sign,
        language: lang,
        signKnowledge,
        astronomicalData,
        date: new Date()
      });

      await saveDailyHoroscope(dailyHoroscope);
    }
  }

  console.log('✅ 72 horóscopos generados y guardados');
});
```

---

### Capa 3: Memoria por Usuario + Cache

**Ya implementado:**
```javascript
// chat_sessions table (Firebase/PostgreSQL)
{
  sessionId: "user123-session456",
  userId: "user123",
  zodiacSign: "Capricornio",
  languageCode: "es",
  messages: [...],  // Historial conversación
  metadata: {
    birthDate: "1990-01-15",
    preferences: {...}
  }
}

// Redis cache
"horoscope:Capricornio:es:2025-11-19" → cached response (TTL 24h)
```

---

## 🚀 IMPLEMENTACIÓN: PROMPT BUILDER

### Sistema de Construcción de Prompts

```javascript
// backend/src/services/promptBuilder.js

class AstrologyPromptBuilder {
  constructor() {
    this.knowledgeBase = require('../knowledge/astrology_base.json');
  }

  /**
   * Construye el prompt completo con 3 capas de conocimiento
   */
  async buildPrompt({ zodiacSign, language, message, sessionContext, date }) {
    const layers = {
      // CAPA 1: Conocimiento base del signo
      baseKnowledge: this._getSignKnowledge(zodiacSign, language),

      // CAPA 2: Datos diarios (72 piezas)
      dailyData: await this._getDailyHoroscope(zodiacSign, date),

      // CAPA 3: Contexto del usuario
      userContext: this._getUserContext(sessionContext)
    };

    return this._assemblePrompt(layers, message, language);
  }

  _getSignKnowledge(sign, language) {
    const signData = this.knowledgeBase.signs[sign];
    const style = this.knowledgeBase.coaching_style;

    return `
## CONOCIMIENTO BASE DEL SIGNO

**${sign}**
- Elemento: ${signData.element}
- Planeta regente: ${signData.ruling_planet}
- Características: ${signData.characteristics}
- Fortalezas: ${signData.strengths.join(', ')}
- Desafíos: ${signData.challenges.join(', ')}

**Guías por Área:**
- Carrera: ${signData.career_guidance}
- Amor: ${signData.love_guidance}
- Bienestar: ${signData.wellness_tips}

**Elementos de Suerte:**
- Colores: ${signData.lucky_elements.colors.join(', ')}
- Números: ${signData.lucky_elements.numbers.join(', ')}
- Cristales: ${signData.lucky_elements.crystals.join(', ')}

**Compatibilidad:**
- Alta: ${signData.compatibility.high.join(', ')}
- Media: ${signData.compatibility.medium.join(', ')}

**Estilo de Comunicación:**
Tono: ${style.tone}
Usa frases como: ${style.language[language].encouragement.join(', ')}
`.trim();
  }

  async _getDailyHoroscope(sign, date) {
    const horoscope = await db.query(
      'SELECT * FROM daily_horoscopes WHERE zodiac_sign = $1 AND date = $2',
      [sign, date]
    );

    if (!horoscope) return '';

    return `
## ENERGÍA Y GUÍA DEL DÍA (${date})

**Nivel de Energía:** ${horoscope.energy_level}
**Colores de Poder:** ${horoscope.lucky_colors.join(', ')}
**Horarios Favorables:** ${horoscope.favorable_times.join(', ')}

**Focos del Día:**
- 💖 Amor: ${horoscope.love_focus}
- 💼 Carrera: ${horoscope.career_focus}
- 🧘 Bienestar: ${horoscope.wellness_focus}
`.trim();
  }

  _getUserContext(sessionContext) {
    if (!sessionContext || !sessionContext.messages.length) {
      return '## CONTEXTO DEL USUARIO\nPrimera conversación.';
    }

    const recentMessages = sessionContext.messages.slice(-6); // Últimos 3 intercambios

    return `
## CONTEXTO DE LA CONVERSACIÓN

**Temas recientes:**
${recentMessages.map(m => `- ${m.type === 'user' ? 'Usuario' : 'Coach'}: ${m.content.substring(0, 100)}...`).join('\n')}

**Preferencias detectadas:**
${sessionContext.metadata?.preferences ? JSON.stringify(sessionContext.metadata.preferences, null, 2) : 'No detectadas aún'}
`.trim();
  }

  _assemblePrompt(layers, userMessage, language) {
    const systemPrompt = `
Eres un coach astrológico experto, empático y sabio. Tienes acceso a tres capas de conocimiento:

${layers.baseKnowledge}

---

${layers.dailyData}

---

${layers.userContext}

---

## INSTRUCCIONES DE RESPUESTA

1. **Usa TODA la información de arriba** como base para tu respuesta
2. **Integra** el conocimiento base del signo con los datos diarios actuales
3. **Personaliza** según el contexto de conversación del usuario
4. **Tono:** Empático, alentador, sabio (nunca alarmista)
5. **Idioma:** ${language}
6. **Extensión:** 2-4 párrafos (150-300 palabras)
7. **Incluye:**
   - Referencia a la energía del día si es relevante
   - Consejos prácticos aplicables HOY
   - Elementos de suerte cuando sea apropiado
   - Cierre motivador

**Mensaje del usuario:**
"${userMessage}"

**Tu respuesta:**
`.trim();

    return systemPrompt;
  }
}

module.exports = new AstrologyPromptBuilder();
```

---

## 📊 FLUJO COMPLETO

```
Usuario envía mensaje
  ↓
Backend recibe request con: zodiacSign, language, message
  ↓
PromptBuilder.buildPrompt()
  ↓
  ├─→ CAPA 1: Carga conocimiento base del signo (astrology_base.json)
  ├─→ CAPA 2: Query DB daily_horoscopes para hoy (1 de 72 piezas)
  └─→ CAPA 3: Recupera contexto sesión (chat_sessions + Redis)
  ↓
Ensambla prompt completo (500-800 tokens)
  ↓
Envía a OpenAI GPT-4o-mini
  ↓
GPT genera respuesta usando LAS 3 CAPAS
  ↓
Backend retorna response + horoscopeData
  ↓
Flutter muestra mensaje + pill + highlights
```

---

## 🛠️ IMPLEMENTACIÓN PASO A PASO

### Fase 1: Crear Knowledge Base (2 horas)

**Archivos a crear:**
```
backend/
  src/
    knowledge/
      astrology_base.json       ← Maestro de conocimiento
      prompt_templates.json     ← Templates por tipo de pregunta
    services/
      promptBuilder.js          ← Builder de prompts en capas
```

**Contenido `astrology_base.json`:**
- 12 signos × características completas
- 10 planetas × arquetipos e influencias
- 12 casas × significados
- Estilo de coaching × 6 idiomas
- Rituales, cristales, elementos

### Fase 2: Job Automático Diario (1 hora)

**Archivo:**
```javascript
// backend/src/jobs/daily_horoscope_generator.js
// Cron: 00:00 UTC diario
// Output: 72 registros en daily_horoscopes
```

**Features:**
- Cálculos astronómicos reales (posiciones planetarias)
- Generación con GPT-4 usando knowledge base
- Guardado multiidioma
- Logs y monitoring

### Fase 3: Integrar Prompt Builder (30 min)

**Modificar:**
```javascript
// backend/src/services/aiCoachService.js

const promptBuilder = require('./promptBuilder');

async _generateAIResponse(sessionId, message, sessionData, options = {}) {
  // ... código existente ...

  // NUEVO: Construir prompt en capas
  const enrichedPrompt = await promptBuilder.buildPrompt({
    zodiacSign: sessionData.zodiac_sign,
    language: options.language || 'es',
    message: message,
    sessionContext: sessionData,
    date: new Date()
  });

  // Enviar a OpenAI con prompt enriquecido
  const response = await this.openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: enrichedPrompt },
      { role: 'user', content: message }
    ],
    temperature: 0.7,
    max_tokens: 500
  });

  // ... resto del código ...
}
```

### Fase 4: Cache Inteligente (30 min)

**Estrategia:**
```javascript
// Cache key: "response:${zodiacSign}:${questionType}:${date}:${language}"

// Preguntas genéricas cachean respuesta completa (24h TTL)
"response:Capricornio:daily_overview:2025-11-19:es" → cached 24h

// Preguntas específicas usan knowledge pero no cachean
"¿Cómo puedo mejorar mi relación con mi jefe?" → no cache, 100% personalizado
```

---

## 📈 BENEFICIOS

### Para el Modelo (GPT-4o-mini):
✅ Siempre tiene acceso a conocimiento experto astrológico
✅ Combina teoría base + datos actuales del día
✅ Respuestas coherentes con el signo y la energía diaria
✅ Tono y estilo consistentes

### Para el Usuario:
✅ Respuestas profundas y fundamentadas
✅ Personalización real (su signo + hoy + su contexto)
✅ Coherencia entre daily highlights y chat
✅ Experiencia premium justificada

### Para el Sistema:
✅ No requiere fine-tuning del modelo
✅ Knowledge base editable sin reentrenar
✅ Cache reduce costos de API
✅ Escalable a nuevos idiomas/signos

---

## 🎯 PRÓXIMOS PASOS

### Inmediato (cuando Railway deploye):
1. ✅ Verificar que horoscopeData fluye correctamente
2. ✅ Test manual en iPhone con datos actuales
3. ✅ Confirmar pill + highlights funcionan

### Siguiente Sesión (Knowledge Base):
1. Crear `astrology_base.json` con 12 signos completos
2. Implementar `PromptBuilder` con 3 capas
3. Setup job diario para 72 piezas
4. Integrar en `aiCoachService`
5. Test A/B: respuestas antes vs después

### Opcional Futuro (Embeddings):
- Vector DB (Pinecone/Weaviate) para búsqueda semántica
- RAG (Retrieval-Augmented Generation) sobre libros astrológicos
- Fine-tune GPT-4 con dataset de consultas reales

---

## 💾 ESTRUCTURA DE ARCHIVOS

```
backend/
  src/
    knowledge/
      astrology_base.json          ← 12 signos + planetas + casas
      coaching_styles.json         ← Tono/vocabulario × 6 idiomas
      rituals_and_practices.json   ← Rituales, cristales, elementos

    services/
      promptBuilder.js             ← Constructor de prompts en capas
      aiCoachService.js            ← (modificar) Usar promptBuilder
      dailyHoroscopeService.js     ← (nuevo) CRUD daily_horoscopes

    jobs/
      daily_horoscope_generator.js ← Cron 00:00 UTC → 72 piezas
      cleanup_old_horoscopes.js    ← Limpieza datos >30 días

    utils/
      astronomy_calculator.js      ← Posiciones planetarias reales

  tests/
    promptBuilder.test.js
    knowledge_integrity.test.js
```

---

## 📊 MÉTRICAS DE ÉXITO

**Antes (sin knowledge base):**
- Respuestas genéricas: ~60%
- Uso de datos diarios: ~20%
- Coherencia con signo: ~40%

**Después (con 3 capas):**
- Respuestas personalizadas: >85%
- Uso de datos diarios: 100%
- Coherencia con signo: >95%
- Satisfacción usuario: +40%

---

## 🚀 COMANDOS RÁPIDOS

```bash
# Cuando Railway deploye, verificar horoscopeData:
./test_railway_deployment.sh

# Generar knowledge base (próxima sesión):
node src/scripts/generate_astrology_base.js

# Test prompt builder:
node src/tests/promptBuilder.test.js

# Ejecutar job diario manual:
node src/jobs/daily_horoscope_generator.js --manual

# Ver logs generación:
tail -f logs/daily_horoscope_generation.log
```

---

**Generado:** 19 Nov 2025
**Status:** Plan completo - Implementación próxima sesión
**Prerequisito:** Railway deployment exitoso (horoscopeData flow)
**Tiempo estimado:** Fase 1-3 = 4 horas | Fase 4 = 30 min
