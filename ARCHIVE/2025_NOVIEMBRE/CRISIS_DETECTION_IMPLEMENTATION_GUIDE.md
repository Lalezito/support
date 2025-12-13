# Crisis Detection Implementation Guide
**For Backend Integration**

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Database Setup](#database-setup)
3. [API Endpoints](#api-endpoints)
4. [Detection Algorithm](#detection-algorithm)
5. [Location Detection](#location-detection)
6. [Response Templates](#response-templates)
7. [Privacy & Compliance](#privacy--compliance)
8. [Testing](#testing)
9. [Monitoring & Maintenance](#monitoring--maintenance)

---

## QUICK START

### Implementation Checklist

**Week 1: Minimum Viable Product**
- [ ] Load crisis keywords database (JSON)
- [ ] Load crisis hotlines database (JSON)
- [ ] Implement basic keyword matching algorithm
- [ ] Create risk scoring function
- [ ] Build response selection logic
- [ ] Add location asking mechanism
- [ ] Create response templates

**Week 2: Testing & Refinement**
- [ ] Test with sample crisis messages
- [ ] Measure false positive/negative rates
- [ ] Add sentiment analysis (optional)
- [ ] Implement privacy policy disclosure
- [ ] Create audit logging (anonymized)

**Week 3: Deployment**
- [ ] Deploy to staging
- [ ] Security audit
- [ ] Load testing
- [ ] Deploy to production
- [ ] Monitor analytics

---

## DATABASE SETUP

### Option 1: PostgreSQL Tables (Recommended)

```sql
-- Crisis Keywords Table
CREATE TABLE crisis_keywords (
    id SERIAL PRIMARY KEY,
    phrase TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('high', 'medium')),
    category VARCHAR(50),
    weight INTEGER NOT NULL DEFAULT 1,
    is_slang BOOLEAN DEFAULT FALSE,
    is_euphemism BOOLEAN DEFAULT FALSE,
    region VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_crisis_keywords_language ON crisis_keywords(language);
CREATE INDEX idx_crisis_keywords_severity ON crisis_keywords(severity);

-- Crisis Hotlines Table
CREATE TABLE crisis_hotlines (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    organization VARCHAR(200) NOT NULL,
    phone VARCHAR(50),
    phone_intl VARCHAR(50),
    sms VARCHAR(100),
    online_chat TEXT,
    email VARCHAR(100),
    hours VARCHAR(100),
    is_24_7 BOOLEAN DEFAULT FALSE,
    languages TEXT[],
    special_populations TEXT[],
    priority INTEGER DEFAULT 0,
    notes TEXT,
    last_verified TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_crisis_hotlines_country ON crisis_hotlines(country_code);
CREATE INDEX idx_crisis_hotlines_priority ON crisis_hotlines(priority);

-- Crisis Interactions Audit Log
CREATE TABLE crisis_interactions (
    id SERIAL PRIMARY KEY,
    user_id_hash VARCHAR(64), -- SHA-256 hash
    session_id VARCHAR(255),
    detected_risk_level VARCHAR(20),
    risk_score INTEGER,
    detected_keywords TEXT[],
    message_hash VARCHAR(64), -- SHA-256, not actual message
    language_detected VARCHAR(10),
    country_provided VARCHAR(2),
    hotlines_shown INTEGER[],
    user_engaged BOOLEAN,
    interaction_timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_crisis_interactions_timestamp ON crisis_interactions(interaction_timestamp);

-- Auto-delete after 90 days for privacy
CREATE OR REPLACE FUNCTION delete_old_crisis_interactions()
RETURNS void AS $$
BEGIN
    DELETE FROM crisis_interactions
    WHERE interaction_timestamp < NOW() - INTERVAL '90 days';
END;
$$ LANGUAGE plpgsql;

-- Schedule daily cleanup
-- Use pg_cron or external scheduler
```

### Option 2: Load from JSON (Simpler)

```javascript
// Node.js/Express example
const fs = require('fs');

// Load keyword database
const keywordsDB = JSON.parse(
  fs.readFileSync('./crisis_keywords_database.json', 'utf8')
);

// Load hotlines database
const hotlinesDB = JSON.parse(
  fs.readFileSync('./crisis_hotlines_database.json', 'utf8')
);

// Cache in memory for fast access
const keywordsCache = new Map();
Object.entries(keywordsDB.keywords).forEach(([lang, severities]) => {
  keywordsCache.set(lang, severities);
});
```

---

## API ENDPOINTS

### POST /api/crisis/analyze

**Request:**
```json
{
  "message": "I can't take it anymore, I just want to end it all",
  "language": "en",
  "userId": "optional-anonymized-id",
  "sessionId": "session-token"
}
```

**Response:**
```json
{
  "riskLevel": "high",
  "riskScore": 78,
  "detectedKeywords": [
    {
      "phrase": "can't take it anymore",
      "severity": "medium",
      "weight": 7
    },
    {
      "phrase": "end it all",
      "severity": "high",
      "weight": 9
    }
  ],
  "recommendedAction": "provide_crisis_resources",
  "responseMessage": "I'm concerned about what you've shared. You don't have to face this alone. Would it be helpful if I share some crisis support resources?",
  "requestLocation": true,
  "showResourcesImmediately": true
}
```

**Implementation:**

```javascript
// Express.js example
app.post('/api/crisis/analyze', async (req, res) => {
  const { message, language, userId, sessionId } = req.body;

  // Validate inputs
  if (!message || !language) {
    return res.status(400).json({ error: 'Message and language required' });
  }

  try {
    // Run detection algorithm
    const analysis = await analyzeCrisisMessage(message, language);

    // Log interaction (anonymized)
    await logCrisisInteraction({
      userIdHash: userId ? hashSHA256(userId) : null,
      sessionId,
      riskLevel: analysis.riskLevel,
      riskScore: analysis.riskScore,
      detectedKeywords: analysis.detectedKeywords.map(k => k.phrase),
      messageHash: hashSHA256(message),
      languageDetected: language
    });

    // Return analysis
    res.json(analysis);
  } catch (error) {
    console.error('Crisis analysis error:', error);
    res.status(500).json({ error: 'Analysis failed' });
  }
});
```

### POST /api/crisis/resources

**Request:**
```json
{
  "countryCode": "US",
  "language": "en",
  "preferredContactMethod": "text"
}
```

**Response:**
```json
{
  "country": "United States",
  "countryCode": "US",
  "resources": [
    {
      "organization": "988 Suicide & Crisis Lifeline",
      "phone": "988",
      "phoneIntl": "+1-800-273-8255",
      "sms": "988",
      "onlineChat": "https://988lifeline.org/chat/",
      "hours": "24/7/365",
      "languages": ["English", "Spanish", "150+ via interpreters"],
      "is24_7": true,
      "priority": 0
    },
    {
      "organization": "Crisis Text Line",
      "sms": "Text HOME to 741741",
      "onlineChat": "https://www.crisistextline.org/",
      "hours": "24/7/365",
      "languages": ["English", "Spanish (text HOLA)"],
      "is24_7": true,
      "priority": 0
    }
  ],
  "emergencyNumber": "911",
  "internationalFallback": {
    "organization": "Find A Helpline (IASP)",
    "url": "https://findahelpline.com/",
    "coverage": "130+ countries"
  }
}
```

**Implementation:**

```javascript
app.post('/api/crisis/resources', async (req, res) => {
  const { countryCode, language, preferredContactMethod } = req.body;

  if (!countryCode) {
    return res.status(400).json({ error: 'Country code required' });
  }

  try {
    // Get hotlines for country
    const resources = await getCrisisHotlines(countryCode, language);

    // Filter by preferred contact method if specified
    let filtered = resources;
    if (preferredContactMethod === 'phone') {
      filtered = resources.filter(r => r.phone);
    } else if (preferredContactMethod === 'text') {
      filtered = resources.filter(r => r.sms);
    } else if (preferredContactMethod === 'chat') {
      filtered = resources.filter(r => r.onlineChat);
    }

    // Sort by priority (0 = highest)
    filtered.sort((a, b) => a.priority - b.priority);

    res.json({
      country: filtered[0]?.country_name || 'Unknown',
      countryCode,
      resources: filtered,
      emergencyNumber: hotlinesDB.emergency_numbers[countryCode] || '112',
      internationalFallback: hotlinesDB.international_resources[0]
    });
  } catch (error) {
    console.error('Resource lookup error:', error);
    res.status(500).json({ error: 'Resource lookup failed' });
  }
});
```

---

## DETECTION ALGORITHM

### Core Algorithm

```javascript
/**
 * Analyze message for crisis indicators
 * @param {string} message - User's message
 * @param {string} language - ISO 639-1 language code
 * @returns {object} Analysis result
 */
async function analyzeCrisisMessage(message, language) {
  // 1. Normalize message
  const normalized = message.toLowerCase().trim();

  // 2. Get keywords for this language
  const keywords = keywordsCache.get(language);
  if (!keywords) {
    throw new Error(`Unsupported language: ${language}`);
  }

  // 3. Detect keywords
  const detectedKeywords = [];
  let totalScore = 0;

  // Check high severity keywords
  for (const keyword of keywords.high) {
    if (normalized.includes(keyword.phrase.toLowerCase())) {
      detectedKeywords.push({
        phrase: keyword.phrase,
        severity: 'high',
        weight: keyword.weight,
        category: keyword.category
      });
      totalScore += keyword.weight;
    }
  }

  // Check medium severity keywords
  for (const keyword of keywords.medium) {
    if (normalized.includes(keyword.phrase.toLowerCase())) {
      detectedKeywords.push({
        phrase: keyword.phrase,
        severity: 'medium',
        weight: keyword.weight,
        category: keyword.category
      });
      totalScore += keyword.weight;
    }
  }

  // 4. Apply context modifiers
  const contextModifiers = keywordsDB.context_modifiers;

  // Help-seeking reduces risk
  for (const phrase of contextModifiers.help_seeking.phrases) {
    if (normalized.includes(phrase.toLowerCase())) {
      totalScore += contextModifiers.help_seeking.weight_modifier;
      break;
    }
  }

  // Humor indicators reduce risk
  for (const phrase of contextModifiers.humor_indicators.phrases) {
    if (normalized.includes(phrase.toLowerCase())) {
      totalScore += contextModifiers.humor_indicators.weight_modifier;
      break;
    }
  }

  // Supporting others (not self) reduces risk
  for (const phrase of contextModifiers.supporting_others.phrases) {
    if (normalized.includes(phrase.toLowerCase())) {
      totalScore += contextModifiers.supporting_others.weight_modifier;
      break;
    }
  }

  // 5. Ensure minimum score
  totalScore = Math.max(0, totalScore);

  // 6. Determine risk level
  const riskLevel = getRiskLevel(totalScore, detectedKeywords);

  // 7. Generate response
  const response = generateResponse(riskLevel, language);

  return {
    riskLevel,
    riskScore: totalScore,
    detectedKeywords,
    recommendedAction: getRecommendedAction(riskLevel),
    responseMessage: response.message,
    requestLocation: riskLevel !== 'low',
    showResourcesImmediately: riskLevel === 'critical'
  };
}

/**
 * Determine risk level based on score and keywords
 */
function getRiskLevel(score, keywords) {
  // Critical if:
  // - Score >= 86, OR
  // - 3+ high severity keywords, OR
  // - Method keyword + suicidal ideation keyword
  const highSevKeywords = keywords.filter(k => k.severity === 'high');
  const hasMethod = keywords.some(k => k.category === 'method');
  const hasSuicidalIdeation = keywords.some(k =>
    k.category === 'suicidal_ideation' || k.category === 'imminent_action'
  );

  if (
    score >= 86 ||
    highSevKeywords.length >= 3 ||
    (hasMethod && hasSuicidalIdeation)
  ) {
    return 'critical';
  }

  if (score >= 61) return 'high';
  if (score >= 31) return 'medium';
  return 'low';
}

/**
 * Get recommended action based on risk level
 */
function getRecommendedAction(riskLevel) {
  const actions = {
    low: 'offer_wellness_resources',
    medium: 'provide_mental_health_resources',
    high: 'provide_crisis_resources',
    critical: 'emergency_intervention'
  };
  return actions[riskLevel];
}
```

### Advanced: Sentiment Analysis

```javascript
// Using a sentiment analysis library (optional enhancement)
const Sentiment = require('sentiment');
const sentiment = new Sentiment();

function analyzeSentiment(message) {
  const result = sentiment.analyze(message);

  // Result contains:
  // - score: overall sentiment (-5 to +5, negative = concerning)
  // - comparative: normalized score
  // - negative: array of negative words
  // - positive: array of positive words

  return result;
}

// Integrate into main algorithm
async function analyzeCrisisMessage(message, language) {
  // ... existing keyword detection ...

  // Add sentiment analysis
  if (language === 'en') { // Sentiment library is English-only
    const sentimentResult = analyzeSentiment(message);

    // Very negative sentiment increases risk
    if (sentimentResult.score < -3) {
      totalScore += 5;
    }
  }

  // ... continue with risk level determination ...
}
```

---

## LOCATION DETECTION

### Option 1: Direct Ask (Recommended)

```javascript
/**
 * Generate location request message
 */
function getLocationRequestMessage(language) {
  const messages = {
    en: "To provide the most relevant support resources, what country are you currently in?",
    es: "Para brindarte los recursos de apoyo más relevantes, ¿en qué país te encuentras?",
    pt: "Para fornecer os recursos de suporte mais relevantes, em que país você está?",
    fr: "Pour vous fournir les ressources d'aide les plus pertinentes, dans quel pays êtes-vous?",
    de: "Um die relevantesten Hilfsressourcen bereitzustellen, in welchem Land befinden Sie sich?",
    it: "Per fornire le risorse di supporto più rilevanti, in quale paese ti trovi?"
  };

  return messages[language] || messages.en;
}

// Frontend: Show dropdown with countries
const countries = [
  { code: 'US', name: 'United States' },
  { code: 'CA', name: 'Canada' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'AU', name: 'Australia' },
  // ... etc
];
```

### Option 2: IP Geolocation with Consent

```javascript
/**
 * Detect country from IP address (with user consent)
 */
async function detectCountryFromIP(ipAddress) {
  try {
    // Option A: Use ipapi.co (free tier: 1000 requests/day)
    const response = await fetch(`https://ipapi.co/${ipAddress}/json/`);
    const data = await response.json();
    return data.country_code; // e.g., "US"

    // Option B: Use ip-api.com (free, no API key needed)
    // const response = await fetch(`http://ip-api.com/json/${ipAddress}`);
    // const data = await response.json();
    // return data.countryCode;

    // Option C: Use MaxMind GeoLite2 (self-hosted, most accurate)
    // const geoip = require('geoip-lite');
    // const geo = geoip.lookup(ipAddress);
    // return geo?.country;
  } catch (error) {
    console.error('IP geolocation failed:', error);
    return null;
  }
}

// Express middleware to add country to request
app.use(async (req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  req.detectedCountry = await detectCountryFromIP(ip);
  next();
});

// In crisis endpoint
app.post('/api/crisis/analyze', async (req, res) => {
  // ...
  const suggestedCountry = req.detectedCountry;

  res.json({
    // ...
    suggestedCountry, // Frontend can show: "Are you in [Country]? [Yes] [No, I'm in...]"
  });
});
```

### Option 3: Browser Language Hint

```javascript
/**
 * Suggest country based on browser language
 */
function suggestCountryFromLanguage(languageCode) {
  const mapping = {
    'en-US': 'US',
    'en-GB': 'GB',
    'en-AU': 'AU',
    'en-CA': 'CA',
    'en-NZ': 'NZ',
    'es-ES': 'ES',
    'es-MX': 'MX',
    'es-AR': 'AR',
    'es-CL': 'CL',
    'es-CO': 'CO',
    'pt-BR': 'BR',
    'pt-PT': 'PT',
    'fr-FR': 'FR',
    'fr-CA': 'CA',
    'de-DE': 'DE',
    'de-AT': 'AT',
    'de-CH': 'CH',
    'it-IT': 'IT',
    // ... etc
  };

  return mapping[languageCode] || null;
}

// Frontend sends navigator.language
// Backend suggests country
```

### Consent Dialog Example

```javascript
// Frontend (React example)
function LocationConsentDialog({ onConsent, onDecline }) {
  return (
    <div className="consent-dialog">
      <h3>Detect Your Location?</h3>
      <p>
        We can detect your country (not city) to show local crisis resources.
        This uses your IP address temporarily and isn't stored.
      </p>
      <button onClick={onConsent}>Allow automatic detection</button>
      <button onClick={onDecline}>I'll enter my country manually</button>
    </div>
  );
}
```

---

## RESPONSE TEMPLATES

### Template System

```javascript
const responseTemplates = {
  en: {
    low: {
      message: "It sounds like you're going through a challenging time. Remember that talking with someone can help. If you'd like, I can share some mental health resources that might be helpful.",
      cta: "Show Resources"
    },
    medium: {
      message: "I can see you're struggling right now, and that's really difficult. Many people find it helpful to talk with someone trained in mental health support. These services are free and confidential.",
      cta: "Show Crisis Resources"
    },
    high: {
      message: "I'm genuinely concerned about what you've shared. You mentioned feelings that sound very painful. Please know that support is available right now.",
      cta: "Show Crisis Support",
      urgent: true
    },
    critical: {
      message: "I'm very concerned for your safety right now based on what you've shared. Please reach out for help immediately. Trained counselors are available 24/7 and can help you through this.",
      cta: "Get Help Now",
      urgent: true,
      showEmergency: true
    }
  },
  es: {
    low: {
      message: "Parece que estás pasando por un momento difícil. Recuerda que hablar con alguien puede ayudar. Si lo deseas, puedo compartir algunos recursos de salud mental que podrían ser útiles.",
      cta: "Mostrar Recursos"
    },
    medium: {
      message: "Veo que estás luchando ahora mismo, y eso es muy difícil. Muchas personas encuentran útil hablar con alguien capacitado en apoyo de salud mental. Estos servicios son gratuitos y confidenciales.",
      cta: "Mostrar Recursos de Crisis"
    },
    high: {
      message: "Estoy genuinamente preocupado/a por lo que has compartido. Mencionaste sentimientos que suenan muy dolorosos. Por favor, ten en cuenta que hay apoyo disponible ahora mismo.",
      cta: "Mostrar Apoyo en Crisis",
      urgent: true
    },
    critical: {
      message: "Estoy muy preocupado/a por tu seguridad en este momento. Por favor, busca ayuda de inmediato. Los consejeros capacitados están disponibles las 24 horas y pueden ayudarte.",
      cta: "Obtener Ayuda Ahora",
      urgent: true,
      showEmergency: true
    }
  },
  pt: {
    low: {
      message: "Parece que você está passando por um momento difícil. Lembre-se de que conversar com alguém pode ajudar. Se quiser, posso compartilhar alguns recursos de saúde mental que podem ser úteis.",
      cta: "Mostrar Recursos"
    },
    medium: {
      message: "Vejo que você está lutando agora, e isso é muito difícil. Muitas pessoas acham útil falar com alguém treinado em apoio à saúde mental. Esses serviços são gratuitos e confidenciais.",
      cta: "Mostrar Recursos de Crise"
    },
    high: {
      message: "Estou genuinamente preocupado(a) com o que você compartilhou. Você mencionou sentimentos que parecem muito dolorosos. Saiba que há apoio disponível agora mesmo.",
      cta: "Mostrar Apoio em Crise",
      urgent: true
    },
    critical: {
      message: "Estou muito preocupado(a) com sua segurança agora. Por favor, procure ajuda imediatamente. Conselheiros treinados estão disponíveis 24 horas por dia e podem ajudá-lo(a).",
      cta: "Obter Ajuda Agora",
      urgent: true,
      showEmergency: true
    }
  },
  // ... fr, de, it templates ...
};

/**
 * Generate appropriate response
 */
function generateResponse(riskLevel, language) {
  const templates = responseTemplates[language] || responseTemplates.en;
  return templates[riskLevel];
}
```

### Resource Display Template

```javascript
/**
 * Format crisis resources for display
 */
function formatCrisisResources(resources, countryCode, language, riskLevel) {
  const emergency = hotlinesDB.emergency_numbers[countryCode];

  let message = '';

  if (riskLevel === 'critical') {
    message += `🚨 **IMMEDIATE HELP AVAILABLE** 🚨\n\n`;
  }

  message += `**Crisis Support (24/7, Free, Confidential):**\n\n`;

  resources.forEach(resource => {
    message += `**${resource.organization}**\n`;
    if (resource.phone) message += `📞 Phone: ${resource.phone}\n`;
    if (resource.sms) message += `💬 Text: ${resource.sms}\n`;
    if (resource.onlineChat) message += `🌐 Chat: ${resource.onlineChat}\n`;
    if (resource.hours && !resource.is_24_7) message += `⏰ Hours: ${resource.hours}\n`;
    message += `\n`;
  });

  if (riskLevel === 'critical' && emergency) {
    message += `\n**If you are in immediate danger:**\n`;
    message += `🚨 Call Emergency Services: ${emergency}\n`;
  }

  return message;
}
```

---

## PRIVACY & COMPLIANCE

### GDPR Compliance Checklist

```javascript
/**
 * Privacy-compliant logging
 */
async function logCrisisInteraction(data) {
  // Never log actual message content
  // Never log IP addresses
  // Hash any user identifiers

  await db.crisis_interactions.insert({
    user_id_hash: data.userIdHash, // Already hashed
    session_id: data.sessionId,
    detected_risk_level: data.riskLevel,
    risk_score: data.riskScore,
    detected_keywords: data.detectedKeywords, // Array of phrases only
    message_hash: data.messageHash, // SHA-256 hash
    language_detected: data.languageDetected,
    country_provided: data.countryProvided,
    hotlines_shown: data.hotlinesShown,
    user_engaged: data.userEngaged,
    interaction_timestamp: new Date()
  });
}

/**
 * Hash function for identifiers
 */
function hashSHA256(data) {
  const crypto = require('crypto');
  return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * GDPR: Right to Erasure
 */
app.delete('/api/user/:userId/data', async (req, res) => {
  const { userId } = req.params;
  const userIdHash = hashSHA256(userId);

  // Delete all crisis interaction logs for this user
  await db.crisis_interactions.deleteMany({
    user_id_hash: userIdHash
  });

  res.json({ success: true, message: 'Data deleted' });
});

/**
 * GDPR: Right to Access
 */
app.get('/api/user/:userId/data', async (req, res) => {
  const { userId } = req.params;
  const userIdHash = hashSHA256(userId);

  const interactions = await db.crisis_interactions.findMany({
    where: { user_id_hash: userIdHash }
  });

  // Return anonymized summary (not actual messages)
  res.json({
    totalInteractions: interactions.length,
    interactions: interactions.map(i => ({
      timestamp: i.interaction_timestamp,
      riskLevel: i.detected_risk_level,
      resourcesProvided: i.hotlines_shown.length > 0
    }))
  });
});
```

### Consent Management

```javascript
/**
 * Record user consent for location detection
 */
async function recordLocationConsent(userId, consented) {
  await db.user_consents.upsert({
    where: { user_id: userId },
    update: {
      location_detection_consent: consented,
      consent_timestamp: new Date()
    },
    create: {
      user_id: userId,
      location_detection_consent: consented,
      consent_timestamp: new Date()
    }
  });
}

/**
 * Check consent before IP geolocation
 */
async function getUserLocationIfConsented(userId, ipAddress) {
  const consent = await db.user_consents.findOne({
    where: { user_id: userId }
  });

  if (consent?.location_detection_consent) {
    return await detectCountryFromIP(ipAddress);
  }

  return null; // Must ask manually
}
```

---

## TESTING

### Unit Tests

```javascript
// Jest example
const { analyzeCrisisMessage } = require('./crisisDetection');

describe('Crisis Detection', () => {
  test('detects high-risk suicidal ideation', async () => {
    const result = await analyzeCrisisMessage(
      "I want to die, I can't go on anymore",
      'en'
    );

    expect(result.riskLevel).toBe('high');
    expect(result.detectedKeywords).toHaveLength(2);
    expect(result.riskScore).toBeGreaterThan(60);
  });

  test('detects critical risk with method', async () => {
    const result = await analyzeCrisisMessage(
      "I'm going to kill myself tonight, I have the pills ready",
      'en'
    );

    expect(result.riskLevel).toBe('critical');
    expect(result.showResourcesImmediately).toBe(true);
  });

  test('does not flag hyperbole', async () => {
    const result = await analyzeCrisisMessage(
      "I'm dying to see that movie lol",
      'en'
    );

    expect(result.riskLevel).toBe('low');
  });

  test('reduces risk for help-seeking', async () => {
    const result = await analyzeCrisisMessage(
      "I feel like I want to die but I need help",
      'en'
    );

    // Should be high but not critical due to help-seeking
    expect(result.riskLevel).not.toBe('critical');
  });

  test('works in Spanish', async () => {
    const result = await analyzeCrisisMessage(
      "quiero morir, no puedo más",
      'es'
    );

    expect(result.riskLevel).toBe('high');
  });

  test('detects supporting others (lower risk)', async () => {
    const result = await analyzeCrisisMessage(
      "My friend says he wants to die, how can I help?",
      'en'
    );

    expect(result.riskLevel).toBe('low');
  });
});
```

### Integration Tests

```javascript
describe('Crisis API Integration', () => {
  test('/api/crisis/analyze endpoint', async () => {
    const response = await fetch('http://localhost:3000/api/crisis/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: "I can't take it anymore",
        language: 'en'
      })
    });

    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveProperty('riskLevel');
    expect(data).toHaveProperty('riskScore');
    expect(data).toHaveProperty('responseMessage');
  });

  test('/api/crisis/resources endpoint', async () => {
    const response = await fetch('http://localhost:3000/api/crisis/resources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        countryCode: 'US',
        language: 'en'
      })
    });

    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.resources).toHaveLength(2); // 988 + Crisis Text Line
    expect(data.emergencyNumber).toBe('911');
  });
});
```

### Test Cases Database

```javascript
const testCases = [
  // HIGH SEVERITY - Should detect
  { message: "I want to die", language: "en", expectedRisk: "high" },
  { message: "quiero morir", language: "es", expectedRisk: "high" },
  { message: "I'm going to kill myself", language: "en", expectedRisk: "critical" },
  { message: "vou me matar", language: "pt", expectedRisk: "critical" },
  { message: "goodbye world, this is my last message", language: "en", expectedRisk: "critical" },

  // MEDIUM SEVERITY
  { message: "I can't go on", language: "en", expectedRisk: "medium" },
  { message: "no puedo más", language: "es", expectedRisk: "medium" },
  { message: "life has no meaning", language: "en", expectedRisk: "medium" },

  // LOW SEVERITY - Should NOT trigger high risk
  { message: "I'm feeling sad today", language: "en", expectedRisk: "low" },
  { message: "I'm dying to see you lol", language: "en", expectedRisk: "low" },
  { message: "This pizza is to die for haha", language: "en", expectedRisk: "low" },

  // CONTEXT MODIFIERS
  { message: "I want to die but I'm seeking help", language: "en", expectedRisk: "medium" }, // Help-seeking reduces
  { message: "My friend wants to kill himself", language: "en", expectedRisk: "low" }, // Supporting others

  // FALSE POSITIVE CHECKS
  { message: "I died laughing at that joke", language: "en", expectedRisk: "low" },
  { message: "I'm dead tired", language: "en", expectedRisk: "low" },
  { message: "This is killing me lol", language: "en", expectedRisk: "low" },
];

// Run all test cases
testCases.forEach(async (testCase) => {
  const result = await analyzeCrisisMessage(testCase.message, testCase.language);
  console.log(`${testCase.message}: ${result.riskLevel} (expected: ${testCase.expectedRisk})`);
});
```

---

## MONITORING & MAINTENANCE

### Analytics Dashboard (Anonymized)

```javascript
/**
 * Get crisis detection analytics
 */
app.get('/api/admin/crisis/analytics', async (req, res) => {
  const { startDate, endDate } = req.query;

  const analytics = await db.query(`
    SELECT
      detected_risk_level,
      COUNT(*) as count,
      AVG(risk_score) as avg_score,
      language_detected,
      country_provided
    FROM crisis_interactions
    WHERE interaction_timestamp BETWEEN $1 AND $2
    GROUP BY detected_risk_level, language_detected, country_provided
  `, [startDate, endDate]);

  res.json({
    summary: {
      totalDetections: analytics.reduce((sum, row) => sum + row.count, 0),
      criticalCases: analytics.filter(r => r.detected_risk_level === 'critical')
        .reduce((sum, row) => sum + row.count, 0),
      highCases: analytics.filter(r => r.detected_risk_level === 'high')
        .reduce((sum, row) => sum + row.count, 0),
    },
    byRiskLevel: analytics,
    topLanguages: getTopLanguages(analytics),
    topCountries: getTopCountries(analytics)
  });
});

/**
 * Monitor false positive rate
 */
app.get('/api/admin/crisis/false-positives', async (req, res) => {
  // User can report false positives
  const falsePositives = await db.false_positive_reports.count();
  const totalDetections = await db.crisis_interactions.count({
    where: { detected_risk_level: ['high', 'critical'] }
  });

  const falsePositiveRate = (falsePositives / totalDetections) * 100;

  res.json({
    falsePositives,
    totalDetections,
    falsePositiveRate: falsePositiveRate.toFixed(2) + '%',
    target: '< 10%'
  });
});
```

### Monitoring Alerts

```javascript
/**
 * Alert if false positive rate exceeds threshold
 */
async function checkFalsePositiveRate() {
  const rate = await getFalsePositiveRate();

  if (rate > 10) { // 10% threshold
    await sendAlert({
      type: 'HIGH_FALSE_POSITIVE_RATE',
      message: `False positive rate is ${rate.toFixed(2)}%, exceeding 10% threshold`,
      severity: 'warning'
    });
  }
}

/**
 * Alert if critical detection rate suddenly spikes
 */
async function checkCriticalDetectionSpike() {
  const last24h = await db.crisis_interactions.count({
    where: {
      detected_risk_level: 'critical',
      interaction_timestamp: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    }
  });

  const average24h = await getAverageCriticalDetections24h();

  if (last24h > average24h * 2) { // 2x spike
    await sendAlert({
      type: 'CRITICAL_DETECTION_SPIKE',
      message: `Critical detections: ${last24h} (average: ${average24h})`,
      severity: 'warning'
    });
  }
}

// Run checks every hour
setInterval(checkFalsePositiveRate, 60 * 60 * 1000);
setInterval(checkCriticalDetectionSpike, 60 * 60 * 1000);
```

### Maintenance Schedule

```javascript
/**
 * Quarterly maintenance tasks
 */
const maintenanceTasks = {
  quarterly: [
    'Verify all crisis hotline numbers (call to confirm)',
    'Update keyword database with new slang/euphemisms',
    'Review false positive reports and adjust weights',
    'Test detection in all 6 languages',
    'Security audit',
    'Privacy policy review',
    'GDPR compliance check'
  ],
  monthly: [
    'Check hotline availability (automated)',
    'Review analytics for anomalies',
    'Update ML model (if using)',
    'Test API response times'
  ],
  weekly: [
    'Monitor false positive rate',
    'Check for new social media suicide-related slang',
    'Review user feedback'
  ]
};

/**
 * Automated hotline verification
 */
async function verifyHotlines() {
  const hotlines = await db.crisis_hotlines.findMany({
    where: {
      last_verified: {
        lt: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) // 90 days
      }
    }
  });

  for (const hotline of hotlines) {
    // Send email to admin to manually verify
    await sendAdminEmail({
      subject: `Verify ${hotline.organization} (${hotline.country_code})`,
      body: `Please verify: ${hotline.phone || hotline.online_chat}`
    });
  }
}
```

---

## DEPLOYMENT CHECKLIST

### Pre-Production

- [ ] Load and test keyword database
- [ ] Load and test hotlines database
- [ ] Implement all API endpoints
- [ ] Write comprehensive unit tests (>80% coverage)
- [ ] Write integration tests
- [ ] Test in all 6 languages
- [ ] Implement privacy-compliant logging
- [ ] Add GDPR user rights endpoints
- [ ] Create privacy policy disclosure
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Set up performance monitoring
- [ ] Configure rate limiting
- [ ] Enable HTTPS/TLS 1.3+
- [ ] Set up database backups
- [ ] Create incident response plan

### Production

- [ ] Deploy to production
- [ ] Monitor error rates
- [ ] Monitor API response times (<500ms target)
- [ ] Monitor false positive rate
- [ ] Set up alerting for spikes
- [ ] Document admin procedures
- [ ] Train support team on crisis escalation
- [ ] Create runbook for incidents

### Post-Launch (First 30 Days)

- [ ] Daily monitoring of analytics
- [ ] Weekly review of false positives
- [ ] Collect user feedback
- [ ] Adjust keyword weights if needed
- [ ] Verify hotlines still active
- [ ] Review privacy compliance
- [ ] Document lessons learned

---

## PERFORMANCE OPTIMIZATION

### Caching

```javascript
// Cache keyword database in memory
const keywordCache = new NodeCache({ stdTTL: 3600 }); // 1 hour

async function getKeywords(language) {
  let keywords = keywordCache.get(language);

  if (!keywords) {
    keywords = await db.crisis_keywords.findMany({
      where: { language }
    });
    keywordCache.set(language, keywords);
  }

  return keywords;
}

// Cache hotlines by country
const hotlineCache = new NodeCache({ stdTTL: 3600 });

async function getHotlines(countryCode) {
  let hotlines = hotlineCache.get(countryCode);

  if (!hotlines) {
    hotlines = await db.crisis_hotlines.findMany({
      where: { country_code: countryCode },
      orderBy: { priority: 'asc' }
    });
    hotlineCache.set(countryCode, hotlines);
  }

  return hotlines;
}
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

// Rate limit crisis analysis endpoint
const crisisLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute per IP
  message: 'Too many crisis analysis requests, please try again later'
});

app.post('/api/crisis/analyze', crisisLimiter, async (req, res) => {
  // ... handler
});
```

### Response Time Monitoring

```javascript
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    if (duration > 500) { // Log slow requests
      console.warn(`Slow request: ${req.path} took ${duration}ms`);
    }
  });

  next();
});
```

---

## SECURITY CONSIDERATIONS

### Input Validation

```javascript
const Joi = require('joi');

const crisisAnalysisSchema = Joi.object({
  message: Joi.string().required().max(5000), // Max 5000 chars
  language: Joi.string().required().valid('en', 'es', 'pt', 'fr', 'de', 'it'),
  userId: Joi.string().optional().max(255),
  sessionId: Joi.string().optional().max(255)
});

app.post('/api/crisis/analyze', async (req, res) => {
  const { error, value } = crisisAnalysisSchema.validate(req.body);

  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }

  // Proceed with validated data
  const analysis = await analyzeCrisisMessage(value.message, value.language);
  res.json(analysis);
});
```

### SQL Injection Prevention

```javascript
// Always use parameterized queries
await db.query(
  'SELECT * FROM crisis_hotlines WHERE country_code = $1',
  [countryCode] // Parameterized, safe from SQL injection
);

// NEVER do this:
// await db.query(`SELECT * FROM crisis_hotlines WHERE country_code = '${countryCode}'`);
```

### XSS Prevention

```javascript
// Sanitize user input before storing or displaying
const sanitizeHtml = require('sanitize-html');

function sanitizeMessage(message) {
  return sanitizeHtml(message, {
    allowedTags: [], // No HTML tags
    allowedAttributes: {}
  });
}
```

---

## FINAL NOTES

### Remember

1. **This is life-saving technology** - Err on side of caution
2. **Privacy is paramount** - Never log actual messages
3. **Update regularly** - Slang and hotlines change
4. **Test thoroughly** - False negatives can be fatal
5. **Comply with laws** - GDPR, HIPAA, local regulations
6. **Monitor constantly** - Track false positives and performance
7. **Get professional help** - Consult mental health experts
8. **Document everything** - For legal protection and maintenance

### Support

If you need help implementing this system:
- Consult licensed mental health professionals
- Partner with crisis organizations (988, Crisis Text Line)
- Join suicide prevention developer communities
- Follow Samaritans Media Guidelines
- Attend conferences (IASP, AFSP)

### Emergency Resources

If you or someone you know needs immediate help:
- **US:** 988 (call or text)
- **International:** https://findahelpline.com/

---

**Implementation Guide Version:** 1.0
**Last Updated:** January 23, 2025
**Next Review:** April 2025
