# Crisis Detection Quick Reference Guide

## FILES CREATED

1. **CRISIS_DETECTION_COMPREHENSIVE_RESEARCH.md** (67 KB)
   - Complete research findings
   - Platform approaches (Meta, Discord, Reddit, Crisis Text Line)
   - International hotlines (25 countries)
   - Best practices and guidelines
   - Legal/compliance requirements

2. **crisis_keywords_database.json** (14 KB)
   - 240+ keywords across 6 languages
   - English, Spanish, Portuguese, French, German, Italian
   - High/medium severity classification
   - Context modifiers
   - Scoring rules

3. **crisis_hotlines_database.json** (12 KB)
   - 45 crisis hotlines
   - 25 countries covered
   - Phone, SMS, chat contact methods
   - Hours of operation
   - Languages supported

4. **CRISIS_DETECTION_IMPLEMENTATION_GUIDE.md** (32 KB)
   - Database setup (SQL + JSON)
   - API endpoint examples
   - Detection algorithm code
   - Location detection methods
   - Response templates
   - Testing examples
   - Privacy compliance code

---

## QUICK IMPLEMENTATION STEPS

### Step 1: Load Data (5 minutes)
```javascript
const keywordsDB = require('./crisis_keywords_database.json');
const hotlinesDB = require('./crisis_hotlines_database.json');
```

### Step 2: Core Detection Function (30 minutes)
```javascript
function analyzeCrisisMessage(message, language) {
  const normalized = message.toLowerCase();
  const keywords = keywordsDB.keywords[language];

  let score = 0;
  let detected = [];

  // Check high severity
  keywords.high.forEach(kw => {
    if (normalized.includes(kw.phrase.toLowerCase())) {
      score += kw.weight;
      detected.push(kw);
    }
  });

  // Check medium severity
  keywords.medium.forEach(kw => {
    if (normalized.includes(kw.phrase.toLowerCase())) {
      score += kw.weight;
      detected.push(kw);
    }
  });

  // Determine risk level
  let riskLevel = 'low';
  if (score >= 86) riskLevel = 'critical';
  else if (score >= 61) riskLevel = 'high';
  else if (score >= 31) riskLevel = 'medium';

  return { riskLevel, score, detected };
}
```

### Step 3: Get Resources (15 minutes)
```javascript
function getCrisisHotlines(countryCode) {
  return hotlinesDB.hotlines
    .filter(h => h.country_code === countryCode)
    .sort((a, b) => a.priority - b.priority);
}
```

### Step 4: Ask Location (10 minutes)
```javascript
const locationPrompts = {
  en: "To provide relevant support resources, what country are you in?",
  es: "¿En qué país te encuentras?",
  pt: "Em que país você está?",
  fr: "Dans quel pays êtes-vous?",
  de: "In welchem Land befinden Sie sich?",
  it: "In quale paese ti trovi?"
};
```

### Step 5: Show Resources (10 minutes)
```javascript
function formatResources(resources, countryCode) {
  let msg = "**Crisis Support (24/7, Free, Confidential):**\n\n";

  resources.forEach(r => {
    msg += `**${r.organization}**\n`;
    if (r.phone) msg += `📞 ${r.phone}\n`;
    if (r.sms) msg += `💬 ${r.sms}\n`;
    if (r.online_chat) msg += `🌐 ${r.online_chat}\n\n`;
  });

  return msg;
}
```

**Total Time:** ~70 minutes for basic implementation

---

## TOP 10 HOTLINES BY COUNTRY

| Country | Hotline | Phone | SMS | 24/7 |
|---------|---------|-------|-----|------|
| 🇺🇸 USA | 988 Lifeline | 988 | 988 | ✓ |
| 🇨🇦 Canada | 988 Helpline | 988 | 988 | ✓ |
| 🇬🇧 UK | Samaritans | 116 123 | - | ✓ |
| 🇦🇺 Australia | Lifeline | 13 11 14 | 0477 13 11 14 | ✓ |
| 🇧🇷 Brazil | CVV | 188 | - | ✓ |
| 🇲🇽 Mexico | Línea de la Vida | 800-911-2000 | - | ✓ |
| 🇪🇸 Spain | 024 | 024 | - | ✓ |
| 🇩🇪 Germany | Telefonseelsorge | 0800-111-0-111 | - | ✓ |
| 🇫🇷 France | SOS Amitié | 09-51-11-61-30 | - | ✓ |
| 🇮🇳 India | AASRA | 91-22-2754-6669 | - | ✓ |

---

## KEYWORD EXAMPLES BY LANGUAGE

### English (High Severity)
- "want to die"
- "kill myself"
- "end my life"
- "goodbye world"
- "overdose"
- "unalive" (euphemism)

### Spanish (High Severity)
- "quiero morir"
- "voy a matarme"
- "no quiero vivir"
- "adiós mundo"
- "sobredosis"

### Portuguese (High Severity)
- "quero morrer"
- "vou me matar"
- "não quero viver"
- "adeus mundo"
- "overdose"

### French (High Severity)
- "veux mourir"
- "je veux me tuer"
- "me suicider"
- "adieu monde"
- "surdose"

### German (High Severity)
- "will sterben"
- "mich umbringen"
- "Selbstmord begehen"
- "Überdosis"

### Italian (High Severity)
- "voglio morire"
- "uccidermi"
- "suicidarmi"
- "addio mondo"
- "sovradosaggio"

---

## RISK LEVELS

### Low (Score 0-30)
- **Indicators:** General sadness, stress
- **Response:** "Would you like some wellness resources?"
- **Action:** Offer optional mental health info

### Medium (Score 31-60)
- **Indicators:** Hopelessness, "no puedo más", "can't go on"
- **Response:** "Many find it helpful to talk with someone trained..."
- **Action:** Provide mental health resources

### High (Score 61-85)
- **Indicators:** Active ideation, "want to die", plan forming
- **Response:** "I'm concerned. Support is available right now."
- **Action:** Show crisis hotlines prominently

### Critical (Score 86-100)
- **Indicators:** Imminent risk, method + plan + intent
- **Response:** "I'm VERY concerned for your safety. Get help NOW."
- **Action:** Emergency intervention, show all resources + 911

---

## API ENDPOINTS

### POST /api/crisis/analyze
**Input:**
```json
{
  "message": "I can't take it anymore",
  "language": "en"
}
```

**Output:**
```json
{
  "riskLevel": "medium",
  "riskScore": 45,
  "responseMessage": "I can see you're struggling...",
  "requestLocation": true
}
```

### POST /api/crisis/resources
**Input:**
```json
{
  "countryCode": "US",
  "language": "en"
}
```

**Output:**
```json
{
  "resources": [
    {
      "organization": "988 Lifeline",
      "phone": "988",
      "sms": "988",
      "hours": "24/7"
    }
  ]
}
```

---

## PRIVACY REQUIREMENTS

### GDPR Compliance
- ✓ Never log actual message content
- ✓ Never log IP addresses
- ✓ Hash user IDs (SHA-256)
- ✓ Delete data after 90 days
- ✓ Provide data export
- ✓ Provide data deletion
- ✓ Obtain explicit consent for location

### What to Log (SAFE)
```javascript
{
  "user_id_hash": "sha256_hash",
  "risk_level": "high",
  "risk_score": 75,
  "keywords_detected": 3,
  "language": "en",
  "country": "US",
  "timestamp": "2025-01-23T18:00:00Z"
}
```

### What NOT to Log (NEVER)
- ❌ Actual message content
- ❌ IP addresses
- ❌ Precise geolocation
- ❌ Personal identifiers
- ❌ Conversation history

---

## LOCATION DETECTION

### Option 1: Direct Ask (Recommended)
```
"To provide relevant support, what country are you in?"
[Dropdown: United States, Canada, UK, ...]
```

### Option 2: IP Geolocation (With Consent)
```
"Detect country from IP? (Country only, not city)"
[Allow] [No, I'll enter manually]
```

### Option 3: Browser Language Hint
```javascript
navigator.language // "en-US" → suggest USA
                   // "es-MX" → suggest Mexico
```

---

## TESTING CHECKLIST

### Test Cases to Run
- [ ] "I want to die" → High risk
- [ ] "quiero morir" → High risk
- [ ] "I'm going to kill myself tonight" → Critical
- [ ] "I'm dying to see that movie lol" → Low (false positive check)
- [ ] "My friend wants to die" → Low (supporting others)
- [ ] "I can't go on but need help" → Medium (help-seeking)
- [ ] Test all 6 languages
- [ ] Test all risk levels
- [ ] Test location detection
- [ ] Test resource lookup for 10 countries
- [ ] Test GDPR data deletion
- [ ] Test response time (<500ms)

---

## MAINTENANCE SCHEDULE

### Weekly
- Check false positive rate (<10% target)
- Monitor analytics for anomalies
- Review new slang/euphemisms

### Monthly
- Verify hotline availability
- Update keyword database
- Review user feedback
- Test in all languages

### Quarterly
- Call all hotlines to verify
- Security audit
- Privacy compliance check
- Update documentation

---

## PERFORMANCE TARGETS

| Metric | Target | Critical |
|--------|--------|----------|
| API Response Time | <500ms | <1000ms |
| False Positive Rate | <10% | <15% |
| False Negative Rate | <5% | <10% |
| Uptime | >99.5% | >99% |
| Hotline Verification | <90 days | <180 days |

---

## WHEN TO ESCALATE

### Contact Emergency Services (911) When:
- Life-threatening situation
- Person has means + plan + intent
- Person is actively harming themselves
- Violent behavior present

### Provide Crisis Hotline When:
- Suicidal ideation expressed
- Self-harm mentioned
- Extreme distress
- Hopelessness with risk indicators

### Offer Wellness Resources When:
- General sadness/stress
- No specific crisis indicators
- User seeking general support

---

## BEST PRACTICES

### DO
✓ Ask location directly and transparently
✓ Explain why you need location
✓ Provide manual entry option
✓ Show resources for user's country
✓ Use non-judgmental language
✓ Respect user autonomy
✓ Log anonymized data only
✓ Update hotlines regularly
✓ Test in all languages

### DON'T
✗ Track location silently
✗ Store actual message content
✗ Use shame/guilt language
✗ Force crisis resources
✗ Assume false positives are safe
✗ Neglect maintenance
✗ Skip testing
✗ Ignore privacy laws

---

## EMERGENCY CONTACTS BY REGION

**Americas:**
- USA: 988 | Text 988
- Canada: 988 | Text 988
- Mexico: 800-911-2000
- Brazil: 188

**Europe:**
- Spain: 024
- UK: 116 123 | Text SHOUT to 85258
- France: 09-51-11-61-30
- Germany: 0800-111-0-111

**Asia-Pacific:**
- Australia: 13 11 14 | Text 0477 13 11 14
- New Zealand: 1737 | Text 1737
- Japan: 0570-783-556 (EN) / 0800-300-8355
- India: 91-22-2754-6669 (AASRA)
- Singapore: 1800-221-4444 (SOS)

**Global Fallback:**
- Find A Helpline: https://findahelpline.com/ (130+ countries)

---

## RESOURCES

### Organizations
- **IASP** (International): https://www.iasp.info/
- **988 Lifeline** (USA): https://988lifeline.org/
- **Crisis Text Line** (USA): https://www.crisistextline.org/
- **Samaritans** (UK): https://www.samaritans.org/
- **Find A Helpline** (Global): https://findahelpline.com/

### Research Papers
- "Application of NLP in Detecting Suicide Ideation" (2023)
- "Multilingual Model for Detection of Suicide Texts" (2024)
- "Machine Learning for Crisis Text Line" (2023)

### Guidelines
- Samaritans Media Guidelines
- GDPR Official Text: https://gdpr-info.eu/
- SAMHSA National Guidelines

---

## SUPPORT

**If you need help implementing:**
- Consult mental health professionals
- Partner with crisis organizations
- Review academic research
- Follow ethical guidelines

**If you're in crisis while reading this:**
- **US:** 988 (call/text)
- **Global:** https://findahelpline.com/
- You matter. Help is available.

---

## FINAL CHECKLIST

Before going live:
- [ ] Keywords loaded for all 6 languages
- [ ] Hotlines loaded for 25+ countries
- [ ] Detection algorithm tested (>85% recall)
- [ ] Privacy policy published
- [ ] GDPR compliance verified
- [ ] Location consent implemented
- [ ] Response templates in all languages
- [ ] API endpoints secured (HTTPS)
- [ ] Rate limiting enabled
- [ ] Error monitoring configured
- [ ] Analytics dashboard created
- [ ] False positive tracking active
- [ ] Admin trained on escalation
- [ ] Incident response plan documented

---

**Quick Reference Version:** 1.0
**Last Updated:** January 23, 2025
**Files:** 4 total (research, keywords, hotlines, implementation guide)
**Total Documentation:** ~125 KB

**Remember:** This is life-saving technology. Implement carefully, test thoroughly, and prioritize user safety above all else.
