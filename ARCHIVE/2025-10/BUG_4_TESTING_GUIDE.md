# Bug #4 Testing Guide: Cosmic Coach Language Detection

## Quick Test (2 minutes)

### Test 1: Spanish Language
1. Open the app
2. Go to Settings
3. Change language to **Spanish (Español)**
4. Navigate to Cosmic Coach (Coach Cósmico)
5. Send a message: "¿Cómo puedes ayudarme?"
6. **Expected**: AI responds completely in Spanish with zodiac-specific insights

### Test 2: English Language
1. In Settings, change language to **English**
2. Navigate to Cosmic Coach
3. Send a message: "How can you help me?"
4. **Expected**: AI responds in English with personalized guidance

## Comprehensive Test Scenarios

### Scenario 1: General Questions (Spanish)
**User Input**: "Hola, ¿qué puedes hacer por mí?"

**Expected Response Elements**:
- ✅ Main message in Spanish
- ✅ Personalized to user's zodiac sign
- ✅ Suggestions in Spanish
- ✅ Next steps in Spanish
- ✅ Resources in Spanish

**Example Response**:
```
"Tu coach cósmico tiene insights sobre orientación general como Aries.
Deja que las estrellas guíen tu camino hoy."

Suggestions:
- "Nutre tus relaciones con comunicación honesta"

Next Steps:
- "Reflexiona sobre la respuesta"
- "Toma acción basada en los insights"
```

### Scenario 2: Goal Setting (Spanish)
**User Input**: "Quiero establecer una nueva meta"

**Expected**:
- ✅ Encouragement in Spanish
- ✅ Aries-specific trait messages in Spanish
- ✅ Goal-related suggestions

**Example Keywords to Look For**:
- "¡Tu progreso es notable!"
- "Tu espíritu guerrero supera cualquier obstáculo"
- "Divide en pasos más pequeños"

### Scenario 3: Emotional Support (Spanish)
**User Input**: "Me siento triste hoy"

**Expected**:
- ✅ Supportive message in Spanish
- ✅ Moon phase energy in Spanish
- ✅ Emotional wellness resources

**Example Keywords**:
- "Siento que has pasado por un momento difícil"
- "La Luna [fase] apoya..."
- "Apps de seguimiento de bienestar"

### Scenario 4: Career Advice (Spanish)
**User Input**: "Necesito consejo sobre mi carrera"

**Expected**:
- ✅ Career-specific guidance in Spanish
- ✅ Zodiac sign career traits
- ✅ Professional development suggestions

**Example Keywords**:
- "naturaleza Aries"
- "¿cómo se vería realmente el éxito para ti?"
- "Herramientas de planificación de carrera"

### Scenario 5: Relationship Questions (Spanish)
**User Input**: "¿Cómo mejorar mis relaciones?"

**Expected**:
- ✅ Relationship-specific advice
- ✅ "Aries aporta energía apasionada a las relaciones"
- ✅ Communication suggestions in Spanish

## Language Switch Test

### Test Both Ways:
1. **Spanish → English**:
   - Set app to Spanish
   - Get Spanish response
   - Change to English in Settings
   - Send new message
   - Should get English response

2. **English → Spanish**:
   - Set app to English
   - Get English response
   - Change to Spanish in Settings
   - Send new message
   - Should get Spanish response

## Edge Cases to Test

### Edge Case 1: No Language Set
**Setup**: Fresh install with no language preference
**Expected**: Defaults to English responses

### Edge Case 2: Rapid Language Switching
**Steps**:
1. Send message in Spanish
2. Immediately switch to English
3. Send another message
**Expected**: Each response in appropriate language

### Edge Case 3: All 12 Zodiac Signs
Test that each zodiac sign returns proper Spanish traits:
- Aries (Aries)
- Tauro (Taurus)
- Géminis (Gemini)
- Cáncer (Cancer)
- Leo (Leo)
- Virgo (Virgo)
- Libra (Libra)
- Escorpio (Scorpio)
- Sagitario (Sagittarius)
- Capricornio (Capricorn)
- Acuario (Aquarius)
- Piscis (Pisces)

## Response Quality Checks

### Spanish Response Should Include:

1. **Zodiac-Specific Traits** (in Spanish):
   - "Tu valentía natural" (for Aries)
   - "Tu perseverancia natural" (for Taurus)
   - "Tu mente versátil" (for Gemini)
   - etc.

2. **Moon Phase Energy** (in Spanish):
   - "La Luna Nueva apoya nuevos comienzos"
   - "La Luna Llena ilumina verdades"
   - etc.

3. **Response Types** (all in Spanish):
   - Guidance: "Basándome en tu energía..."
   - Insight: "Lo que estoy notando aquí..."
   - Encouragement: "¡Tu progreso es notable!"
   - Question: "¿Qué te dice tu intuición?"
   - Challenge: "Veo potencial para un crecimiento aún mayor"
   - Strategy: "Creemos una estrategia que honre tus fortalezas"
   - Resource: "Recomiendo explorar..."

4. **Suggestions Categories**:
   - Relationships: "Practica la escucha activa y la empatía"
   - Career: "Enfócate en tus fortalezas profesionales únicas"
   - Personal Growth: "Dedica tiempo a la auto-reflexión"
   - Wellness: "Prioriza el autocuidado que resuene contigo"

## Visual Verification Checklist

When testing, visually confirm:
- [ ] No English words in Spanish responses
- [ ] Proper Spanish grammar and accents (á, é, í, ó, ú, ñ)
- [ ] Natural-sounding Spanish (not machine-translated)
- [ ] Consistent tone and formality level
- [ ] All UI elements respect language setting

## Performance Test

1. Send 10 consecutive messages in Spanish
2. Verify each response:
   - [ ] Arrives in < 3 seconds
   - [ ] Is completely in Spanish
   - [ ] Is contextually relevant
   - [ ] Includes zodiac personalization

## Regression Test

Verify that English responses still work correctly:
1. Set language to English
2. Test all same scenarios above
3. Confirm all responses are in English
4. Verify no Spanish text appears

## Success Criteria

✅ **PASS** if:
- All responses match user's language setting
- Spanish responses are grammatically correct
- Zodiac traits appear in appropriate language
- Moon phase messages are localized
- Suggestions, resources, and next steps are translated
- No mixing of English/Spanish in same response
- Language switches work immediately

❌ **FAIL** if:
- Any English text appears when language is Spanish
- Any Spanish text appears when language is English
- Responses are not contextually appropriate
- Language switching doesn't work
- App crashes or shows errors

## Report Template

```
Date: ____________________
Tester: __________________
Device: __________________
OS Version: ______________

[ ] Test 1: Spanish Language - PASS/FAIL
[ ] Test 2: English Language - PASS/FAIL
[ ] Scenario 1: General Questions - PASS/FAIL
[ ] Scenario 2: Goal Setting - PASS/FAIL
[ ] Scenario 3: Emotional Support - PASS/FAIL
[ ] Scenario 4: Career Advice - PASS/FAIL
[ ] Scenario 5: Relationship Questions - PASS/FAIL
[ ] Language Switch Test - PASS/FAIL
[ ] Edge Cases - PASS/FAIL
[ ] Performance Test - PASS/FAIL

Issues Found:
1. _________________________________
2. _________________________________
3. _________________________________

Overall Status: PASS / FAIL
```
