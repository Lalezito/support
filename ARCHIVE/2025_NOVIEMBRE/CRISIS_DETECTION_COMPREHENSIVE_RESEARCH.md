# Comprehensive Crisis Detection Research
**Research Date:** January 2025
**Purpose:** Implementation of crisis detection system for mental health application

---

## TABLE OF CONTENTS
1. [Crisis Detection Keywords by Language](#crisis-detection-keywords-by-language)
2. [International Crisis Hotlines](#international-crisis-hotlines)
3. [Platform Detection Approaches](#platform-detection-approaches)
4. [Best Practices & Guidelines](#best-practices--guidelines)
5. [Legal & Compliance Requirements](#legal--compliance-requirements)
6. [Implementation Recommendations](#implementation-recommendations)

---

## CRISIS DETECTION KEYWORDS BY LANGUAGE

### Methodology & Sources
Based on academic research from:
- Crisis Text Line ML detection systems (recall = 0.89)
- Meta/Facebook Community Standards enforcement
- Discord Trust & Safety AutoMod systems
- Reddit r/SuicideWatch community monitoring
- Natural Language Processing research (2023-2025)
- Multilingual transformer models (mT5, mBERT, XML-R)

### Severity Classification System

**HIGH SEVERITY** - Immediate risk indicators:
- Direct suicidal ideation
- Specific method mentions
- Imminent harm statements
- Farewell/goodbye messages

**MEDIUM SEVERITY** - Concerning but not immediate:
- Hopelessness expressions
- Life meaninglessness
- Extreme emotional pain
- Indirect suicidal thoughts

---

### ENGLISH Keywords

#### High Severity
**Direct Suicidal Ideation:**
- "want to die"
- "kill myself"
- "end my life"
- "take my own life"
- "don't want to live"
- "ready to die"
- "going to kill myself"
- "commit suicide"
- "end it all"
- "kms" (kill myself - slang)

**Method-Specific:**
- "overdose"
- "slit my wrists"
- "hang myself"
- "jump off"
- "shoot myself"
- "cut myself"

**Imminent Action:**
- "goodbye world"
- "this is my last"
- "final goodbye"
- "won't be here tomorrow"
- "tonight's the night"

#### Medium Severity
**Extreme Distress:**
- "can't go on"
- "can't take it anymore"
- "no point in living"
- "life isn't worth it"
- "better off dead"
- "everyone would be better without me"
- "no reason to live"
- "give up on life"

**Hopelessness:**
- "no way out"
- "no escape"
- "nothing to live for"
- "pointless"
- "worthless"
- "burden to everyone"
- "permanent solution"

---

### SPANISH Keywords

#### High Severity (Alto Riesgo)
**Ideación Suicida Directa:**
- "quiero morir"
- "quiero morirme"
- "voy a matarme"
- "quiero acabar con mi vida"
- "no quiero vivir"
- "voy a suicidarme"
- "quiero desaparecer"
- "terminar con todo"

**Métodos Específicos:**
- "cortarme las venas"
- "sobredosis"
- "ahorcarme"
- "tirarme"
- "lanzarme"
- "cortarme"

**Acción Inminente:**
- "adiós mundo"
- "última vez"
- "despedida final"
- "hoy es el día"
- "ya no estaré mañana"

#### Medium Severity (Riesgo Medio)
**Angustia Extrema:**
- "no puedo más"
- "no aguanto más"
- "ya no puedo seguir"
- "rendirme"
- "darme por vencido/a"
- "mejor muerto/a"
- "todos estarían mejor sin mí"

**Desesperanza:**
- "sin salida"
- "no hay escapatoria"
- "sin sentido"
- "sin razón para vivir"
- "no vale la pena"
- "una carga para todos"

**Regional Variations (Latin America):**
- "me quiero matar" (more common in Mexico, Colombia)
- "no doy más" (Argentina, Uruguay)
- "ya no hallo qué hacer" (Mexico)
- "estoy hasta la madre" (Mexico - extreme frustration)

---

### PORTUGUESE Keywords

#### High Severity (Alto Risco)
**Ideação Suicida Direta (Brazil & Portugal):**
- "quero morrer"
- "vou me matar"
- "quero acabar com a minha vida"
- "não quero viver"
- "vou me suicidar"
- "quero desaparecer"
- "acabar com tudo"

**Métodos Específicos:**
- "cortar os pulsos"
- "overdose" / "sobredose"
- "me enforcar"
- "me jogar"
- "pular" (Brazil) / "saltar" (Portugal)

**Ação Iminente:**
- "adeus mundo"
- "última vez"
- "despedida final"
- "hoje é o dia"
- "não estarei aqui amanhã"

#### Medium Severity (Risco Médio)
**Angústia Extrema:**
- "não aguento mais"
- "não posso mais"
- "não consigo continuar"
- "desistir"
- "melhor morto/a"
- "todos ficariam melhor sem mim"

**Desesperança:**
- "sem saída"
- "sem escapatória"
- "sem sentido"
- "sem razão para viver"
- "não vale a pena"
- "um fardo para todos"

**Brazil-Specific:**
- "tô indo embora" (I'm leaving - euphemism)
- "cansei de tudo"
- "não dá mais"

---

### FRENCH Keywords

#### High Severity (Risque Élevé)
**Idéation Suicidaire Directe:**
- "veux mourir"
- "je veux me tuer"
- "en finir avec la vie"
- "me suicider"
- "veux disparaître"
- "mettre fin à mes jours"
- "ne veux plus vivre"

**Méthodes Spécifiques:**
- "me trancher les veines"
- "overdose" / "surdose"
- "me pendre"
- "sauter"
- "me jeter"

**Action Imminente:**
- "adieu monde"
- "dernière fois"
- "adieu final"
- "ce soir c'est fini"

#### Medium Severity (Risque Moyen)
**Détresse Extrême:**
- "ne peux plus continuer"
- "n'en peux plus"
- "abandonner"
- "mieux mort/e"
- "tous seraient mieux sans moi"

**Désespoir:**
- "sans issue"
- "pas d'échappatoire"
- "sans sens"
- "sans raison de vivre"
- "ne vaut pas la peine"
- "un fardeau"

---

### GERMAN Keywords

#### High Severity (Hohes Risiko)
**Direkte Suizidgedanken:**
- "will sterben"
- "mich umbringen"
- "mein Leben beenden"
- "Selbstmord begehen"
- "nicht mehr leben"
- "verschwinden will"

**Spezifische Methoden:**
- "Pulsadern aufschneiden"
- "Überdosis"
- "mich erhängen"
- "springen"
- "mich erschießen"

**Unmittelbare Handlung:**
- "letztes Mal"
- "finaler Abschied"
- "heute ist der Tag"

#### Medium Severity (Mittleres Risiko)
**Extreme Verzweiflung:**
- "kann nicht mehr"
- "ertrage es nicht mehr"
- "aufgeben"
- "besser tot"
- "allen wäre es besser ohne mich"

**Hoffnungslosigkeit:**
- "kein Ausweg"
- "keine Flucht"
- "sinnlos"
- "kein Grund zu leben"
- "es lohnt sich nicht"
- "eine Last"

---

### ITALIAN Keywords

#### High Severity (Alto Rischio)
**Ideazione Suicida Diretta:**
- "voglio morire"
- "uccidermi"
- "finire la mia vita"
- "suicidarmi"
- "non voglio vivere"
- "voglio scomparire"

**Metodi Specifici:**
- "tagliarmi le vene"
- "overdose" / "sovradosaggio"
- "impiccarmi"
- "saltare"
- "gettarmi"

**Azione Imminente:**
- "addio mondo"
- "ultima volta"
- "addio finale"
- "stasera è finita"

#### Medium Severity (Rischio Medio)
**Disagio Estremo:**
- "non ce la faccio più"
- "non posso più"
- "arrendermi"
- "meglio morto/a"
- "tutti starebbero meglio senza di me"

**Disperazione:**
- "senza via d'uscita"
- "nessuna fuga"
- "senza senso"
- "nessun motivo per vivere"
- "non ne vale la pena"
- "un peso"

---

### Additional Detection Patterns

#### Euphemisms & Slang (Multi-language)
- "sewerslide" (TikTok censorship bypass for "suicide")
- "unalive" / "unaliving" (English)
- "CTB" - "catch the bus" (pro-suicide forum slang)
- "SN" - sodium nitrite (method reference)
- "permanent sleep"
- "going to sleep forever"

#### Context Indicators
Look for combinations of:
- Giving away possessions
- Saying goodbye to loved ones
- Expressing no future plans
- Sudden calmness after depression
- Researching methods
- Updating will/final arrangements

---

## INTERNATIONAL CRISIS HOTLINES

### AMERICAS

#### United States
**988 Suicide & Crisis Lifeline**
- **Phone:** 988 (call or text)
- **Phone (alternate):** 1-800-273-8255
- **Online Chat:** https://988lifeline.org/chat/
- **Hours:** 24/7/365
- **Languages:** English, Spanish (press 2), 150+ via Language Line
- **Organization:** SAMHSA (Substance Abuse and Mental Health Services Administration)
- **Special:** Veterans can press 1 for Veterans Crisis Line

**Crisis Text Line**
- **SMS:** Text HOME to 741741
- **Hours:** 24/7/365
- **Languages:** English, Spanish (text HOLA)
- **Organization:** Crisis Text Line, Inc.

#### Canada
**9-8-8 Suicide Crisis Helpline**
- **Phone:** 988
- **SMS:** Text 988
- **Hours:** 24/7/365
- **Languages:** English, French
- **Organization:** Government of Canada
- **Launch Date:** November 30, 2023

**Kids Help Phone (Youth)**
- **Phone:** 1-800-668-6868
- **SMS:** Text CONNECT to 686868
- **Hours:** 24/7/365
- **Ages:** 5-29 years
- **Languages:** English, French

**Hope for Wellness (Indigenous Peoples)**
- **Phone:** 1-855-242-3310
- **SMS:** Text WELLNESS to 741741
- **Online Chat:** https://www.hopeforwellness.ca/
- **Hours:** 24/7/365
- **Languages:** English, French, Cree, Ojibway, Inuktitut

#### Mexico
**Línea de la Vida**
- **Phone:** 800-911-2000
- **Email:** lalineadelavida@salud.gob.mx
- **Hours:** 24/7/365
- **Languages:** Spanish
- **Organization:** Secretaría de Salud (Ministry of Health)

#### Brazil
**CVV - Centro de Valorização da Vida**
- **Phone:** 188
- **Online Chat:** https://www.cvv.org.br/
- **Email:** Through website
- **Hours:** 24/7/365
- **Languages:** Portuguese
- **Note:** Free call from any phone in Brazil

#### Argentina
**Centro de Asistencia al Suicida**
- **Phone (Buenos Aires):** 135
- **Phone (National):** 5275-1135 or 0800-345-1435
- **Hours:** 24/7/365
- **Languages:** Spanish

#### Chile
**Teléfono de la Esperanza**
- **Phone:** 717-003-717
- **Hours:** 24/7/365
- **Languages:** Spanish

#### Colombia
**Línea Nacional de Prevención del Suicidio**
- **Phone:** 106
- **Hours:** 24/7/365
- **Languages:** Spanish

**Regional Numbers:**
- Barranquilla: (00 57 5) 372-2727
- Bogotá: (57-1) 323-2425
- Medellín: (00 57 4) 284-6600

---

### EUROPE

#### Spain
**Línea 024 - Atención a la Conducta Suicida**
- **Phone:** 024
- **Hours:** 24/7/365
- **Languages:** Spanish, regional languages
- **Organization:** Ministerio de Sanidad
- **Cost:** Free

#### United Kingdom
**Samaritans**
- **Phone:** 116 123 (UK & Ireland)
- **Email:** jo@samaritans.org
- **Hours:** 24/7/365
- **Languages:** English, Welsh
- **Organization:** Samaritans

**National Suicide Prevention Helpline UK**
- **Phone:** 0800-689-5652 or 0800-689-0880
- **Hours:** 6pm-midnight (365 days)
- **Languages:** English

**Shout (Text Service)**
- **SMS:** Text SHOUT to 85258
- **Hours:** 24/7/365
- **Languages:** English

#### France
**SOS Amitié**
- **Phone:** (+33) 09-51-11-61-30
- **Online Chat:** https://www.sos-amitie.com/
- **Hours:** 24/7/365
- **Languages:** French

#### Germany
**Telefonseelsorge**
- **Phone:** 0800-111-0-111
- **Phone (alternate):** 0800-111-0-222
- **Online Chat:** https://online.telefonseelsorge.de/
- **Hours:** 24/7/365
- **Languages:** German
- **Cost:** Free

#### Italy
**Telefono Amico Italia**
- **Phone:** 02-2327-2327
- **SMS:** Text 324-011-7252
- **Email:** Through website
- **Hours:** 10:00-24:00 daily
- **Languages:** Italian

**Telefono Azzurro (Youth)**
- **Phone:** 19696
- **Hours:** 24/7/365
- **Ages:** Children and adolescents

#### Portugal
**SOS Voz Amiga**
- **Phone:** +351-213-544-545
- **Phone:** +351-912-802-669
- **Phone:** +351-963-524-660
- **Hours:** 16:00-24:00 daily (4pm-midnight)
- **Languages:** Portuguese, English, French, German, Russian, Japanese, Chinese, Arabic, Hindi, Indonesian

**SOS Estudante (Students)**
- **Phone:** 239-484-020 or 915-246-060
- **Hours:** 20:00-01:00 daily
- **Languages:** Portuguese

#### Netherlands
**113 Zelfmoordpreventie**
- **Phone:** 113 (standard rate)
- **Phone (toll-free):** 0800-0113
- **Online Chat:** https://www.113.nl/ (click "chatten")
- **Hours:** 24/7/365
- **Languages:** Dutch, English (via chat)
- **Note:** Phone only accessible from within Netherlands; international users can use chat

---

### ASIA-PACIFIC

#### Australia
**Lifeline Australia**
- **Phone:** 13-11-14
- **SMS:** Text 0477-13-11-14
- **Online Chat:** https://www.lifeline.org.au/crisis-chat/
- **Hours:** 24/7/365
- **Languages:** English, 200+ via interpreters
- **Organization:** Lifeline Australia

**Beyond Blue**
- **Phone:** 1300-22-4636
- **Online Chat:** https://www.beyondblue.org.au/get-support/get-immediate-support
- **Hours:** 24/7/365
- **Languages:** English
- **Focus:** Depression, anxiety, suicide prevention

**Suicide Call Back Service**
- **Phone:** 1300-659-467
- **Online Chat:** https://www.suicidecallbackservice.org.au/
- **Video Counselling:** Available through website
- **Hours:** 24/7/365
- **Languages:** English

#### New Zealand
**1737 Need to Talk?**
- **Phone:** 1737 or 0800-1737-1737
- **SMS:** Text 1737
- **Hours:** 24/7/365
- **Languages:** English, Māori
- **Organization:** Ministry of Health
- **Cost:** Free

**Lifeline Aotearoa**
- **Phone:** 0800-543-354
- **SMS:** Text HELP to 4357
- **Hours:** 24/7/365
- **Languages:** English

#### Japan
**TELL Lifeline**
- **Phone:** 0570-783-556
- **Phone (toll-free):** 0800-300-8355
- **Hours:** Daily 9am-11pm
- **Languages:** English
- **Organization:** Tokyo English Life Line

**Inochi no Denwa (Japanese)**
- **Phone:** 0570-783-556
- **Hours:** 24/7/365
- **Languages:** Japanese

#### India
**AASRA (Mumbai)**
- **Phone:** 91-22-2754-6669
- **Email:** aasrahelpline@yahoo.com
- **Hours:** 24/7/365
- **Languages:** English, Hindi

**Sneha Foundation (Chennai)**
- **Phone:** +91-044-2464-0050 (24/7)
- **Phone:** +91-044-2464-0060 (8am-10pm)
- **Online Chat:** https://snehaindia.org/ (7pm-1am)
- **Hours:** 24/7/365
- **Languages:** Tamil, English

**iCall (Mumbai - Tata Institute)**
- **Phone:** 9152-987-821
- **Email:** icall@tiss.edu
- **Hours:** Mon-Sat 8am-10pm
- **Languages:** English, Hindi

#### Singapore
**Samaritans of Singapore (SOS)**
- **Phone:** 1800-221-4444
- **SMS:** Not available
- **Email:** pat@sos.org.sg
- **Hours:** 24/7/365
- **Languages:** English, Mandarin

**Institute of Mental Health (IMH) Helpline**
- **Phone:** 6389-2222
- **Hours:** 24/7/365
- **Languages:** English

---

### MIDDLE EAST & AFRICA

#### Israel
**ERAN - Emotional First Aid**
- **Phone:** 1201 (within Israel)
- **Phone (international):** 972-76-884-4400
- **Online Chat:** https://en.eran.org.il/
- **Hours:** 24/7/365
- **Languages:** Hebrew, Arabic, Russian, English

**Sahar**
- **Online Chat Only:** https://sahar.org.il/
- **Hours:** 12:00pm-9:00pm daily
- **Languages:** Hebrew

#### South Africa
**Suicide Crisis Line**
- **Phone:** 0800-567-567
- **SMS:** 31393
- **Hours:** 24/7/365
- **Languages:** English, Afrikaans
- **Cost:** Free

**Life Line**
- **Phone:** 0861-322-322
- **WhatsApp:** 065-989-9238
- **Hours:** 24/7/365
- **Languages:** Multiple
- **Cost:** Free

**SADAG (South African Depression and Anxiety Group)**
- **Phone (day):** 0800-212-223 (8am-8pm)
- **Phone (night):** 0800-121-314 (8pm-8am)
- **Hours:** 24/7/365
- **Languages:** English

**Cipla Mental Health Helpline**
- **Phone:** 0800-456-789
- **WhatsApp:** 076-882-2775
- **Hours:** 24/7/365
- **Languages:** Multiple
- **Cost:** Free

---

### Global Resources

**Find A Helpline (IASP Partner)**
- **Website:** https://findahelpline.com/
- **Coverage:** 130+ countries
- **Topics:** 21 topics, 15 specialties
- **Languages:** Multiple per country
- **Search:** By country, topic, language

**Crisis Text Line (International)**
- **USA:** Text HOME to 741741
- **Canada:** Text 741741
- **UK:** Text SHOUT to 85258
- **Ireland:** Text HELLO to 50808
- **Hours:** 24/7/365

---

## PLATFORM DETECTION APPROACHES

### Meta/Facebook
**Detection Methods:**
- Proactive AI detection (removed 6.6M pieces of content in Q4 2024)
- User reporting system
- Keyword and phrase matching
- Image and video content analysis (graphic self-harm imagery)
- Context-aware moderation

**Response:**
- Connect users to local crisis resources
- Contact emergency services if immediate harm detected
- Allow discussion for support-seeking and awareness
- Remove content promoting or coordinating self-harm

**Policy (as of Jan 2025):**
- Removed third-party fact-checking in US
- Weakened some hate-speech policies
- Maintained strong suicide/self-harm prevention

### Discord
**Detection Methods:**
- AutoMod keyword filters (server-level)
- User reporting ("Report Message" > "Self-harm")
- Third-party bots (e.g., Suicide Prevention Bot)
- Trust & Safety team review

**Response:**
- Investigate reports
- May contact authorities for imminent threats
- Partner with Crisis Text Line (text DISCORD to 741741 in US)
- Partner with ThroughLine Care (international)
- Take action on users/communities promoting self-harm

**Policy:**
- No coordination or graphic depiction allowed
- Context-aware review
- Focus on preventing glorification

### Reddit
**Detection Methods:**
- AutoMod rule-based keyword detection
- Community reporting
- Moderator review (r/SuicideWatch has 13 human mods)
- Partnership with Crisis Text Line

**Response:**
- Automatic message with Crisis Text Line link
- Community support in r/SuicideWatch (40,000+ subscribers)
- Human moderator intervention
- Remove content violating policies

**Limitations:**
- Keyword approaches can miss flippant references
- May miss unreported posts
- Requires human judgment for context

### Crisis Text Line
**Detection Methods:**
- Machine learning binary classification models
- Natural language processing (NLP)
- Triage algorithm for severity assessment
- Custom keywords for institutional partners

**Performance:**
- 89% recall for suicidal risk and self-harm detection
- Reduced wait times for high-risk texters from 8 min to 3 min (median)
- 75th percentile: from 35 min to 11 min

**Response Process:**
1. Message arrives
2. ML model assesses risk level
3. Queue prioritization (high-risk first, not chronological)
4. Safety assessment in every conversation
5. Emergency intervention for ~1% of chats (imminent risk)
6. About 20% of chats involve suicidal thoughts

---

## BEST PRACTICES & GUIDELINES

### Crisis Detection Best Practices

#### 1. When to Escalate to Emergency Services

**Immediate 911/Emergency Call When:**
- Life-threatening situation
- Person has means and plan to harm themselves
- Person is actively harming themselves
- Violent behavior present
- Serious property damage occurring
- Person is unresponsive or unconscious

**Before Calling 911, Try:**
- Contact mental health professional if known
- Call county mental health crisis unit
- Call mobile crisis team (for non-violent self-harm concerns)
- Call 988 Suicide & Crisis Lifeline
- Use crisis text/chat services

**When Calling 911:**
- State: "Someone is experiencing a mental health crisis"
- Explain nature of emergency
- Mention your relationship to person
- Report if weapons are involved
- Request CIT officer (Crisis Intervention Training) if available

#### 2. Crisis Definition (NAMI)
A mental health crisis occurs when:
- Person's behavior puts them at risk of hurting themselves or others, AND/OR
- Person cannot care for themselves or function effectively in community

#### 3. Assessment Levels

**Low Risk:**
- General sadness or depression
- Stress about life circumstances
- Seeking emotional support
- No suicidal ideation expressed

**Medium Risk:**
- Hopelessness or despair
- Life feels meaningless
- Passive suicidal ideation ("wish I were dead")
- No specific plan or intent

**High Risk:**
- Active suicidal ideation with plan
- Recent suicide attempt
- Access to lethal means
- Giving away possessions
- Saying goodbyes
- Sudden calmness after severe depression

**Imminent Risk:**
- Person has plan, means, and intent
- Currently attempting self-harm
- Expressed timeline ("tonight," "today")
- Farewell messages sent
- Already engaged in preparatory behavior

---

### Location Detection Best Practices

#### Ethical Approaches to Location Detection

**1. Transparent Direct Request (RECOMMENDED)**
Ask users directly with clear explanation:

**Example Phrasing:**
```
"To provide you with the most relevant support resources, could you share
what country you're currently in? This helps us connect you with local
crisis services if needed."
```

**Why This Works:**
- Transparent and respectful
- Gives user control
- Explains purpose clearly
- Not intrusive
- GDPR/privacy compliant

**2. Optional IP Geolocation with Consent**
```
"We'd like to detect your approximate location (country only) to provide
local resources. This uses your IP address but doesn't store it.
[Allow] [No, I'll enter manually]"
```

**3. Browser Geolocation API (High Friction)**
- Requires explicit browser permission
- Often denied by users
- Good for mobile apps
- Not recommended for sensitive mental health context

#### What NOT to Do

**AVOID:**
- Silent IP tracking without disclosure
- Storing location data without consent
- Using precise geolocation (city/address level) without explicit need
- Sharing location data with third parties
- Retaining location data longer than necessary

#### Culturally Sensitive Phrasing

**Good Examples:**
- "What country are you connecting from?"
- "Where are you located so we can find local support?"
- "Which country's resources would be most helpful?"
- "To show you the right helplines, which country are you in?"

**Poor Examples:**
- "Where do you live?" (too intrusive)
- "We need your location" (demanding)
- Silent detection with no explanation (unethical)

---

### Crisis Response Communication Guidelines

#### Samaritans Media Guidelines (UK Standard)

**DO:**
- Use "ended their own life" instead of "committed suicide"
- Say "suicide attempt" not "failed suicide" or "cry for help"
- Describe as "preventable," "tragic waste," "avoidable loss"
- Include helpline numbers and support resources
- Focus on warning signs and support availability

**DON'T:**
- Use "suicide epidemic," "suicide wave," "suicide cluster" (unless confirmed)
- Use "suicide spot," "hot spot," "notorious site"
- Suggest method is quick, easy, painless, or certain
- Include technical details about methods
- Use dramatic or sensational language
- Say "committed suicide" (implies crime/sin)

#### Crisis Intervention Language

**When User Expresses Suicidal Thoughts:**

**DO Say:**
- "I'm concerned about you and want to help"
- "You don't have to face this alone"
- "Have you thought about reaching out to a crisis counselor?"
- "There are people trained to help - can I share some resources?"
- "What you're feeling is temporary, even if it doesn't feel that way"

**DON'T Say:**
- "You have so much to live for" (dismissive)
- "It could be worse" (minimizing)
- "Just think positive" (unhelpful)
- "You're being selfish" (shaming)
- "I know exactly how you feel" (presumptuous)

**Providing Resources:**
```
"I care about your safety. In [COUNTRY], you can reach trained crisis
counselors 24/7 at:
- Phone: [NUMBER]
- Text: [NUMBER]
- Chat: [URL]

These services are free, confidential, and available right now.
Would you be willing to reach out to them?"
```

---

### Detection Without Triggering

#### Passive Detection Methods

**1. Sentiment Analysis**
- Monitor overall conversation tone
- Track negative emotion escalation
- Detect hopelessness patterns
- Flag sudden shifts to positive (can indicate decision made)

**2. Contextual Keyword Matching**
Combine keywords with context:
- "I want to die" + no future tense language = higher risk
- "I feel like dying" + seeking help = medium risk
- Past mentions of therapy = context for assessment

**3. Behavioral Indicators**
- Returning user with escalating distress
- Time of contact (late night = higher risk)
- Isolation language ("nobody cares," "all alone")
- Finality language ("last time," "goodbye")

#### Non-Intrusive Resource Offering

**Progressive Disclosure:**

**Level 1 - General Wellness:**
```
"It sounds like you're going through a difficult time.
Have you considered talking to someone trained in mental health support?"
```

**Level 2 - Specific Resources:**
```
"Many people find it helpful to talk with a crisis counselor.
They're available 24/7 and conversations are confidential.
Would you like me to share contact information?"
```

**Level 3 - Direct Crisis Intervention:**
```
"I'm genuinely concerned for your safety right now. Please consider
contacting a crisis service immediately:
[Provide specific hotline for their country]

If you're in immediate danger, please call emergency services: [NUMBER]"
```

---

### Academic Research on Detection

#### NLP Detection Methods (2023-2025 Research)

**Effective Approaches:**
1. **Hybrid Models** (Structured + Unstructured Data)
   - Demographics + clinical notes
   - Billing data + narrative text
   - Better accuracy than either alone

2. **Transformer-Based Models**
   - mT5: F1 scores >85% across 6 languages
   - mBERT: Strong cross-lingual transfer
   - Context-aware (understands "I want to die" vs "I want to die laughing")

3. **Temporal Pattern Analysis**
   - Escalation tracking over time
   - Sudden changes in communication
   - Increased crisis language frequency

**Limitations:**
- Blanket keyword filtering is problematic
- Misses flippant references vs. genuine risk
- Cultural and linguistic variations critical
- Context absolutely necessary
- Low specificity without human review

#### Research-Based Indicators

**Linguistic Markers (from NLP studies):**
- First-person singular pronouns ("I," "me," "my")
- Absolute language ("always," "never," "nothing")
- Death-related words
- Negative emotion words
- Social disconnection language
- Low positive emotion words
- Fewer future tense references

---

## LEGAL & COMPLIANCE REQUIREMENTS

### GDPR Requirements for Mental Health Apps

#### Data Classification

**Mental Health Data = Special Category Data**
- Article 9 GDPR: Requires heightened protection
- Includes psychological, psychiatric, emotional data
- Location data = personal data identifier (explicit in GDPR)
- IP addresses = personal data if can profile individuals

#### Legal Bases for Processing

**For Commercial Apps (Most Restrictive):**
- **Article 9(2)(a):** Explicit consent ONLY
- Consent must be:
  - Freely given
  - Specific
  - Informed
  - Unambiguous
  - Affirmative action (not silence/pre-ticked boxes)

**For Healthcare Provision:**
- **Article 9(2)(h):** Healthcare provision (diagnosis/therapy)
- Can process without additional consent
- Must be for direct care purposes

**For Crisis Intervention:**
- **Vital interests exception** may apply in emergency
- Not clearly defined - err on side of obtaining consent

#### Consent Requirements

**Explicit Consent Standards:**
1. **Clear Disclosure:**
   ```
   "We collect location data (country-level) to provide relevant crisis
   resources. This data is processed via IP address but not stored.

   Do you consent to temporary location detection?"
   [Yes] [No - I'll enter manually]
   ```

2. **Separate Consent for Each Purpose:**
   - Crisis detection: Separate consent
   - Location tracking: Separate consent
   - Analytics: Separate consent
   - Cannot bundle

3. **Right to Withdraw:**
   - Must be as easy to withdraw as to give
   - Must inform users of this right
   - Must honor immediately

4. **Documentation:**
   - Log when consent obtained
   - Log what was consented to
   - Log when withdrawn
   - Keep records as proof

#### Data Handling Requirements

**Collection:**
- Only collect minimum necessary (country, not city)
- Explain exactly what will be collected
- Don't use deceptive language

**Storage:**
- Don't store location data if not necessary
- If must store: encrypt, limit access, set retention period
- Mental health conversation data: highest security

**Retention:**
- GDPR: Delete upon request (right to erasure)
- Define and publish retention policy
- Automatic deletion after period

**Breach Notification:**
- Report to supervisory authority within 72 hours
- Notify affected users if high risk
- Document all breaches

#### User Rights (Must Support)

1. **Right to Access** - Users can request their data
2. **Right to Rectification** - Correct inaccurate data
3. **Right to Erasure** - "Right to be forgotten"
4. **Right to Portability** - Export data in machine-readable format
5. **Right to Object** - Object to processing
6. **Right to Restrict Processing** - Limit how data is used

#### Privacy by Design

**Required Approaches:**
- Separate PII from operational data
- Use anonymization where possible
- Mobile Advertising IDs (MAIDs) instead of user IDs
- Minimal data collection
- End-to-end encryption for sensitive conversations

---

### HIPAA Considerations (US)

**When HIPAA Applies:**
- You are a "covered entity" (healthcare provider, plan, clearinghouse)
- You are a "business associate" of covered entity
- You transmit health information electronically

**Key Requirements:**
- Encryption of data in transit and at rest
- Access controls and audit logs
- 6-year retention requirement (conflicts with GDPR deletion)
- Business associate agreements (BAAs)
- Breach notification within 60 days

**When HIPAA Does NOT Apply:**
- Direct-to-consumer wellness apps (most astrology/horoscope apps)
- Anonymous crisis text lines
- Peer support communities
- General mental health information resources

**Crisis Exception:**
- HIPAA allows disclosure without authorization to prevent serious threat
- "To prevent or lessen a serious and imminent threat to health or safety"
- Similar to GDPR vital interests exception

---

### Dual Compliance (HIPAA + GDPR)

**For International Mental Health Apps:**

**Consent Management:**
- Obtain explicit consent covering both frameworks
- Block trackers until consent received
- Separate consent for different purposes

**Data Handling:**
- Meet stricter of the two requirements
- Encryption: Both require it
- Retention: HIPAA = 6 years, GDPR = delete on request
  - Solution: Anonymize after service complete, retain anonymized data
- Breach notification: GDPR = 72 hours (stricter)

**User Rights:**
- Support all GDPR rights (more extensive than HIPAA)
- Provide data portability
- Honor deletion requests (anonymize HIPAA-required data)

---

### Best Practice: Ethical Framework

**1. Transparency**
- Clear privacy policy in plain language
- Explain what data collected and why
- Explain who has access
- Explain how long retained

**2. User Control**
- Make consent optional where possible
- Provide manual alternatives (enter country vs. detect)
- Easy withdrawal mechanism
- Dashboard for data management

**3. Security**
- End-to-end encryption for conversations
- Secure API connections (TLS 1.3+)
- Regular security audits
- Incident response plan

**4. Minimization**
- Collect only what's necessary
- Country-level location, not GPS
- Temporary detection, don't store
- Anonymize analytics data

**5. Purpose Limitation**
- Use data only for stated purpose
- Don't sell mental health data (ever)
- Don't use for advertising
- Don't share with third parties without consent

---

## IMPLEMENTATION RECOMMENDATIONS

### Crisis Detection System Architecture

#### Recommended Approach

```
┌─────────────────────────────────────────────────────────┐
│                    User Message Input                    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│           Multilingual Keyword Detection                 │
│   - Match against keyword database (by language)         │
│   - Calculate keyword density                            │
│   - Flag euphemisms and slang                            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Sentiment Analysis Layer                    │
│   - Overall message tone (negative/positive)             │
│   - Emotion detection (hopelessness, despair)            │
│   - Temporal comparison (getting worse?)                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Contextual Analysis                         │
│   - Combine keyword + sentiment + context               │
│   - Check for help-seeking language                      │
│   - Identify finality indicators                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Risk Score Calculation                      │
│   Low (0-30) | Medium (31-60) | High (61-85) | Critical (86-100)
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Response Selection                          │
│   - Low: Wellness resources                              │
│   - Medium: Mental health resources                      │
│   - High: Crisis hotlines                                │
│   - Critical: Emergency + crisis hotlines                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Location Detection                          │
│   1. Ask user: "What country are you in?"                │
│   2. Fallback: IP geolocation (country only)             │
│   3. Store preference for session only                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Resource Provision                          │
│   - Lookup hotlines for user's country                   │
│   - Provide phone, text, chat options                    │
│   - Include 24/7 availability info                       │
│   - Offer international fallback (988, Crisis Text Line) │
└─────────────────────────────────────────────────────────┘
```

---

### Database Schema Recommendation

#### Crisis Keywords Table
```sql
CREATE TABLE crisis_keywords (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    language VARCHAR(10) NOT NULL,  -- ISO 639-1 code
    severity VARCHAR(20) NOT NULL,  -- 'high', 'medium'
    category VARCHAR(50),           -- 'suicidal_ideation', 'self_harm', 'hopelessness'
    weight INTEGER DEFAULT 1,       -- Scoring weight
    is_euphemism BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_keywords_language ON crisis_keywords(language);
CREATE INDEX idx_keywords_severity ON crisis_keywords(severity);
```

#### Crisis Hotlines Table
```sql
CREATE TABLE crisis_hotlines (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL,     -- ISO 3166-1 alpha-2
    country_name VARCHAR(100) NOT NULL,
    organization_name VARCHAR(200) NOT NULL,
    phone_number VARCHAR(50),
    phone_number_intl VARCHAR(50),        -- With country code
    sms_number VARCHAR(50),
    online_chat_url TEXT,
    email VARCHAR(100),
    hours_operation VARCHAR(100),         -- "24/7" or "Mon-Fri 9am-5pm"
    is_24_7 BOOLEAN DEFAULT FALSE,
    languages_supported TEXT[],            -- Array of language codes
    special_populations TEXT[],            -- ["youth", "veterans", "LGBTQ+", etc.]
    priority INTEGER DEFAULT 0,            -- 0 = primary, 1 = secondary
    is_active BOOLEAN DEFAULT TRUE,
    last_verified TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_hotlines_country ON crisis_hotlines(country_code);
CREATE INDEX idx_hotlines_active ON crisis_hotlines(is_active);
```

#### User Crisis Interactions (Audit Log)
```sql
CREATE TABLE crisis_interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),                  -- Hashed or anonymized
    session_id VARCHAR(255),
    detected_risk_level VARCHAR(20),       -- 'low', 'medium', 'high', 'critical'
    detected_keywords TEXT[],              -- Keywords that triggered
    user_message_hash VARCHAR(64),         -- SHA-256 hash, not actual message
    language_detected VARCHAR(10),
    country_provided VARCHAR(2),           -- User-provided or IP-detected
    hotlines_provided INTEGER[],           -- Foreign keys to crisis_hotlines
    user_confirmed_safety BOOLEAN,
    interaction_timestamp TIMESTAMP DEFAULT NOW(),
    notes TEXT
);

-- Retention: Auto-delete after 90 days for privacy
CREATE INDEX idx_interactions_user ON crisis_interactions(user_id);
CREATE INDEX idx_interactions_timestamp ON crisis_interactions(interaction_timestamp);
```

---

### API Endpoint Design

#### POST /api/crisis/analyze
```json
{
  "message": "I can't take it anymore, I just want it all to end",
  "language": "en",
  "userId": "anonymized-hash",
  "sessionId": "session-token"
}
```

**Response:**
```json
{
  "riskLevel": "high",
  "riskScore": 78,
  "detectedKeywords": [
    {"keyword": "can't take it anymore", "severity": "medium", "weight": 5},
    {"keyword": "want it all to end", "severity": "high", "weight": 8}
  ],
  "recommendedAction": "provide_crisis_resources",
  "message": "I'm concerned about what you shared. You don't have to face this alone. Would it be helpful if I share some crisis support resources?",
  "requestLocation": true
}
```

#### POST /api/crisis/resources
```json
{
  "countryCode": "US",
  "language": "en",
  "preferredContactMethod": "text"  // "phone", "text", "chat"
}
```

**Response:**
```json
{
  "country": "United States",
  "resources": [
    {
      "organization": "988 Suicide & Crisis Lifeline",
      "phone": "988",
      "phoneInternational": "+1-800-273-8255",
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

---

### Response Templates by Risk Level

#### Low Risk (Score 0-30)
```
"It sounds like you're going through a challenging time. Remember that
talking with someone can help. If you'd like, I can share some mental
health resources that might be helpful."

[Show Resources] [No Thanks]
```

#### Medium Risk (Score 31-60)
```
"I can see you're struggling right now, and that's really difficult.
Many people find it helpful to talk with someone trained in mental health
support. These services are free and confidential:

[Show Crisis Resources]

Would you like to see contact information for support services in your area?"

[Yes, Show Resources] [Not Right Now]
```

#### High Risk (Score 61-85)
```
"I'm genuinely concerned about what you've shared. You mentioned feelings
that sound very painful. Please know that support is available right now:

**Crisis Support (24/7, Free, Confidential):**
- Phone: [NUMBER]
- Text: [NUMBER]
- Chat: [URL]

These trained counselors are available immediately and can help you through
this. Would you be willing to reach out to them?"

[I'll Contact Them] [Show More Resources]
```

#### Critical Risk (Score 86-100)
```
"I'm very concerned for your safety right now based on what you've shared.
Please reach out for help immediately:

**CRISIS SUPPORT (AVAILABLE RIGHT NOW):**
📞 Phone: [NUMBER]
💬 Text: [NUMBER]
🌐 Chat: [URL]

**If you are in immediate danger:**
🚨 Call Emergency Services: [NUMBER]

These services are free, confidential, and available 24/7. Trained
counselors are standing by to help.

Please reach out now - you don't have to face this alone."

[I Need Help Now - Show Full Resources]
```

---

### Location Detection Implementation

#### Option 1: Direct Ask (Recommended)
```javascript
// When crisis detected, ask directly
const locationPrompt = {
  en: "To provide the most relevant support resources, what country are you currently in?",
  es: "Para brindarte los recursos de apoyo más relevantes, ¿en qué país te encuentras?",
  pt: "Para fornecer os recursos de suporte mais relevantes, em que país você está?",
  fr: "Pour vous fournir les ressources d'aide les plus pertinentes, dans quel pays êtes-vous?",
  de: "Um die relevantesten Hilfsressourcen bereitzustellen, in welchem Land befinden Sie sich?",
  it: "Per fornire le risorse di supporto più rilevanti, in quale paese ti trovi?"
};

// Provide dropdown or autocomplete
// Store choice for session only, don't persist
```

#### Option 2: IP Geolocation with Consent
```javascript
// Show consent dialog first
const consentDialog = {
  title: "Detect Your Location?",
  message: "We can detect your country (not city) to show local crisis resources. This uses your IP address temporarily and isn't stored.",
  options: [
    "Allow automatic detection",
    "I'll enter my country manually"
  ]
};

// If allowed:
async function detectCountryFromIP(ip) {
  // Use service like ipapi.co, ip-api.com, or ipgeolocation.io
  // Only retrieve country-level data
  const response = await fetch(`https://ipapi.co/${ip}/country_code/`);
  const countryCode = await response.text();
  return countryCode; // e.g., "US", "GB", "BR"
}
```

#### Option 3: Browser Language Fallback
```javascript
// Not location, but can suggest likely resources
function getPreferredLanguage() {
  return navigator.language || navigator.userLanguage; // e.g., "en-US", "es-MX"
}

// Suggest country based on language variant
// "es-MX" -> suggest Mexico resources
// "es-ES" -> suggest Spain resources
// "en-GB" -> suggest UK resources
// Still ask user to confirm!
```

---

### Testing & Validation

#### Keyword Detection Testing
```javascript
// Test cases for each language
const testCases = [
  // High severity - should trigger
  { text: "I want to die", language: "en", expectedRisk: "high" },
  { text: "quiero morir", language: "es", expectedRisk: "high" },
  { text: "me vou matar", language: "pt", expectedRisk: "high" },

  // Context matters - should not trigger or low risk
  { text: "I'm dying to see that movie", language: "en", expectedRisk: "low" },
  { text: "This weather makes me want to die lol", language: "en", expectedRisk: "low" },

  // Medium severity
  { text: "I can't go on like this", language: "en", expectedRisk: "medium" },
  { text: "no puedo más con esto", language: "es", expectedRisk: "medium" },

  // Euphemisms
  { text: "I want to unalive myself", language: "en", expectedRisk: "high" },
  { text: "thinking about ctb", language: "en", expectedRisk: "high" }
];
```

#### False Positive Minimization
- Require multiple keyword matches for high risk
- Use sentiment analysis to filter hyperbole
- Consider conversation history
- Weight context words (help-seeking reduces risk)
- Allow for humor/sarcasm detection (difficult)

#### False Negative Minimization
- Include euphemisms and slang
- Update keyword list regularly
- Monitor for new terms (social media trends)
- Accept some false positives to avoid missing real crises
- Err on side of caution

---

### Privacy-Preserving Analytics

#### What to Track (Anonymized)
```json
{
  "eventType": "crisis_detected",
  "riskLevel": "high",
  "languageDetected": "en",
  "keywordsTriggered": 3,
  "resourcesProvided": true,
  "countryCode": "US",
  "timestamp": "2025-01-23T18:30:00Z",
  "sessionDuration": 180,  // seconds
  "userEngagedWithResources": true,
  // NO user ID, NO message content, NO IP address
}
```

#### What NOT to Track
- Actual message content
- User identifiers (unless anonymized hash)
- IP addresses
- Precise timestamps (round to hour)
- Any PII

#### Aggregated Reporting
- "X% of crisis detections resulted in resource engagement"
- "Most common language: English (45%), Spanish (30%)"
- "Peak crisis detection hours: 10pm-2am UTC"
- "Countries with most requests: US, UK, Brazil"

---

### Compliance Checklist

#### Pre-Launch
- [ ] Privacy policy written and published
- [ ] Terms of service include crisis detection disclosure
- [ ] Consent mechanism implemented and tested
- [ ] User can decline location detection
- [ ] Manual country entry option available
- [ ] Data retention policy defined (recommend: session only)
- [ ] Encryption implemented (TLS 1.3+ for API, AES-256 for storage)
- [ ] GDPR user rights endpoints created (access, delete, export)
- [ ] Breach notification process documented
- [ ] Crisis hotline database verified (last 3 months)
- [ ] Response templates reviewed by mental health professional
- [ ] False positive rate tested (<10% target)
- [ ] False negative rate tested (<5% target)

#### Post-Launch Monitoring
- [ ] Weekly keyword database updates
- [ ] Monthly hotline verification
- [ ] Quarterly privacy policy review
- [ ] Quarterly security audit
- [ ] Annual penetration testing
- [ ] User feedback collection on crisis responses
- [ ] Continuous ML model improvement (if using ML)

---

## ADDITIONAL RESOURCES

### Organizations to Consult

**International:**
- International Association for Suicide Prevention (IASP)
  - Website: https://www.iasp.info/
  - Partner: Find A Helpline (https://findahelpline.com/)

**United States:**
- 988 Suicide & Crisis Lifeline (SAMHSA)
  - Website: https://988lifeline.org/
- Crisis Text Line
  - Website: https://www.crisistextline.org/

**United Kingdom:**
- Samaritans
  - Website: https://www.samaritans.org/
  - Media Guidelines: https://www.samaritans.org/about-samaritans/media-guidelines/

**Research:**
- American Association of Suicidology
- American Foundation for Suicide Prevention (AFSP)
- The Trevor Project (LGBTQ+ youth)

### Academic Papers

1. "Application of Natural Language Processing (NLP) in Detecting and Preventing Suicide Ideation: A Systematic Review" (2023)
   - Journal: International Journal of Environmental Research and Public Health
   - DOI: 10.3390/ijerph20021514

2. "The First Multilingual Model For The Detection of Suicide Texts" (2024)
   - ArXiv: 2412.15498
   - Languages: Spanish, English, German, Catalan, Portuguese, Italian

3. "A machine learning approach to identifying suicide risk among text-based crisis counseling encounters" (2023)
   - Focus: Crisis Text Line ML implementation

4. "Natural language processing system for rapid detection and intervention of mental health crisis chat messages" (2023)
   - Journal: npj Digital Medicine
   - Focus: Real-time crisis detection

### Privacy Frameworks

- GDPR Official Text: https://gdpr-info.eu/
- HIPAA Privacy Rule: https://www.hhs.gov/hipaa/for-professionals/privacy/
- SAMHSA Confidentiality Regulations: 42 CFR Part 2
- ISO 27001 (Information Security)
- SOC 2 Type II (Service Organization Controls)

---

## IMPLEMENTATION PRIORITY

### Phase 1: Minimum Viable Crisis Detection (Week 1-2)
1. Implement English keyword detection (high severity only)
2. Create crisis hotline database for top 10 countries
3. Build basic risk scoring (keyword matching)
4. Implement direct location ask
5. Create response templates for high risk
6. Add privacy policy disclosures

### Phase 2: Multilingual Support (Week 3-4)
1. Add Spanish, Portuguese, French keywords
2. Expand hotline database to 20 countries
3. Implement sentiment analysis
4. Add medium risk detection
5. Create localized response templates

### Phase 3: Advanced Detection (Week 5-8)
1. Add German, Italian keywords
2. Implement contextual analysis
3. Add euphemism detection
4. Expand hotline database to 50+ countries
5. Build analytics dashboard (anonymized)
6. Add IP geolocation option with consent

### Phase 4: ML Enhancement (Week 9-12)
1. Train ML model on labeled data
2. Implement A/B testing (keyword vs. ML)
3. Build false positive reduction
4. Add temporal pattern analysis
5. Implement continuous learning

### Phase 5: Compliance & Optimization (Ongoing)
1. Complete GDPR compliance audit
2. Implement all user rights endpoints
3. Conduct penetration testing
4. Optimize response times (<500ms)
5. Monthly keyword database updates
6. Quarterly hotline verification

---

## CRITICAL SUCCESS METRICS

### Detection Metrics
- **Recall (Sensitivity):** >85% (don't miss real crises)
- **Precision:** >60% (minimize false alarms)
- **Response Time:** <500ms for risk assessment
- **Coverage:** Hotlines for 50+ countries
- **Language Support:** 6+ languages

### User Engagement Metrics
- **Resource Click-Through:** >40% of high-risk detections
- **User-Reported Helpfulness:** >70% positive
- **Consent Rate:** >60% for location detection
- **False Positive Reports:** <5% of detections

### Compliance Metrics
- **Privacy Policy Clarity:** 8th grade reading level
- **Consent Collection:** 100% before location tracking
- **Data Breach Incidents:** 0
- **GDPR Requests Fulfilled:** 100% within 30 days
- **Hotline Verification:** <90 days since last check

---

## FINAL NOTES

### Ethical Considerations

**This is Life-Saving Technology:**
- Every false negative could be a life lost
- Err on side of caution
- Better to over-offer resources than under-offer
- But don't trigger anxiety with aggressive messaging

**User Autonomy Matters:**
- Users have right to refuse help
- Don't force crisis resources
- Don't shame users
- Provide easy opt-out

**Cultural Sensitivity:**
- Suicide stigma varies by culture
- Language matters (avoid "commit suicide")
- Religious considerations
- LGBTQ+ specific resources where available

**Legal Protection:**
- Consult lawyer for liability issues
- Consider "Good Samaritan" provisions
- Document reasonable efforts
- Don't claim to replace professional help

### Getting Help

**If you're implementing this system and need support:**
- Consult with licensed mental health professionals
- Partner with crisis organizations
- Join tech ethics communities
- Attend suicide prevention conferences
- Follow Samaritans Media Guidelines

**If you're in crisis while reading this:**
- **US:** Call/Text 988
- **International:** https://findahelpline.com/
- You matter. Help is available.

---

**Document Version:** 1.0
**Last Updated:** January 23, 2025
**Maintained By:** Crisis Detection Research Project
**Next Review:** April 2025

---

## QUICK REFERENCE TABLES

### Top 10 Countries - Quick Hotline Reference

| Country | Primary Hotline | Phone | SMS | Chat | 24/7 |
|---------|----------------|-------|-----|------|------|
| USA | 988 Lifeline | 988 | 988 | 988lifeline.org | ✓ |
| Canada | 988 Helpline | 988 | 988 | - | ✓ |
| UK | Samaritans | 116 123 | - | samaritans.org | ✓ |
| Australia | Lifeline | 13 11 14 | 0477 13 11 14 | lifeline.org.au | ✓ |
| Brazil | CVV | 188 | - | cvv.org.br | ✓ |
| Mexico | Línea de la Vida | 800-911-2000 | - | - | ✓ |
| Spain | 024 | 024 | - | - | ✓ |
| Germany | Telefonseelsorge | 0800-111-0-111 | - | telefonseelsorge.de | ✓ |
| France | SOS Amitié | 09-51-11-61-30 | - | sos-amitie.com | ✓ |
| India | AASRA | 91-22-2754-6669 | - | - | ✓ |

### Risk Level Quick Guide

| Risk Level | Score | Indicators | Response |
|------------|-------|------------|----------|
| Low | 0-30 | General sadness, stress | Offer wellness resources |
| Medium | 31-60 | Hopelessness, meaninglessness | Provide mental health resources |
| High | 61-85 | Suicidal ideation, plan forming | Show crisis hotlines prominently |
| Critical | 86-100 | Imminent risk, method+plan | Emergency message, all resources |

### Language Detection Quick Reference

| Language Code | Language | Common Countries | Sample Hotline |
|---------------|----------|------------------|----------------|
| en | English | US, UK, AU, CA, NZ | 988 (US), 116 123 (UK) |
| es | Spanish | ES, MX, AR, CL, CO | 024 (ES), 800-911-2000 (MX) |
| pt | Portuguese | BR, PT | 188 (BR) |
| fr | French | FR, CA, BE, CH | 09-51-11-61-30 (FR) |
| de | German | DE, AT, CH | 0800-111-0-111 (DE) |
| it | Italian | IT, CH | 02-2327-2327 (IT) |

---

## END OF DOCUMENT

This comprehensive research document provides everything needed to implement a crisis detection system with:
- Multilingual keyword databases
- International crisis hotlines
- Best practices for detection
- GDPR/HIPAA compliance guidelines
- Implementation recommendations
- Testing protocols
- Privacy-preserving approaches

**Remember:** This is sensitive, life-saving technology. Implement with care, consult professionals, and prioritize user safety above all else.
