# 🧪 Biorhythm Motivational Messages - Testing Guide
**Created:** November 13, 2025

---

## 🎯 QUICK TEST

### How to Test in the App

1. **Navigate to Cosmic Coach** in the app
2. **Look for biorhythm goals** with these titles:
   - "Critical Physical Day" / "Día Físico Crítico" / etc.
   - "Physical Recovery" / "Recuperación Física" / etc.
   - "Emotional Critical" / "Día Emocional Crítico" / etc.
   - "Intellectual Critical" / "Día Intelectual Crítico" / etc.

3. **Check the motivational message** at the bottom of each goal card

---

## 🌐 WHAT TO VERIFY

### English (en)
- [ ] Physical Critical: "Your {Sign} wisdom knows: rest days are training days too. Honor your body's cycles."
- [ ] Physical Recovery: "Your {Sign} knows: growth happens during recovery, not during action."
- [ ] Emotional Critical: "Your {Sign} sensitivity is a gift. Honor your emotional rhythms."
- [ ] Intellectual Critical: "Your {Sign} knows: not every day is for genius. Some days are for showing up."

### Spanish (es)
- [ ] Physical Critical: "Tu sabiduría de {Signo} sabe: los días de descanso son días de entrenamiento también. Honra los ciclos de tu cuerpo."
- [ ] Physical Recovery: "Tu {Signo} sabe: el crecimiento ocurre durante la recuperación, no durante la acción."
- [ ] Emotional Critical: "Tu sensibilidad de {Signo} es un regalo. Honra tus ritmos emocionales."
- [ ] Intellectual Critical: "Tu {Signo} sabe: no todos los días son para el genio. Algunos días son para aparecer."

### Portuguese (pt)
- [ ] Physical Critical: "Sua sabedoria de {Signo} sabe: dias de descanso são dias de treino também. Honre os ciclos do seu corpo."
- [ ] Physical Recovery: "Seu {Signo} sabe: o crescimento acontece durante a recuperação, não durante a ação."
- [ ] Emotional Critical: "Sua sensibilidade de {Signo} é um presente. Honre seus ritmos emocionais."
- [ ] Intellectual Critical: "Seu {Signo} sabe: nem todo dia é para ser gênio. Alguns dias são para aparecer."

### French (fr)
- [ ] Physical Critical: "Votre sagesse {Signe} sait: les jours de repos sont aussi des jours d'entraînement. Honorez les cycles de votre corps."
- [ ] Physical Recovery: "Votre {Signe} sait: la croissance se produit pendant la récupération, pas pendant l'action."
- [ ] Emotional Critical: "Votre sensibilité {Signe} est un cadeau. Honorez vos rythmes émotionnels."
- [ ] Intellectual Critical: "Votre {Signe} sait: tous les jours ne sont pas pour le génie. Certains jours sont pour se montrer."

### German (de)
- [ ] Physical Critical: "Deine {Zeichen}-Weisheit weiß: Ruhetage sind auch Trainingstage. Ehre die Zyklen deines Körpers."
- [ ] Physical Recovery: "Dein {Zeichen} weiß: Wachstum geschieht während der Erholung, nicht während der Aktion."
- [ ] Emotional Critical: "Deine {Zeichen}-Sensibilität ist ein Geschenk. Ehre deine emotionalen Rhythmen."
- [ ] Intellectual Critical: "Dein {Zeichen} weiß: Nicht jeder Tag ist für Genie. Manche Tage sind fürs Erscheinen."

### Italian (it)
- [ ] Physical Critical: "La tua saggezza {Segno} sa: i giorni di riposo sono anche giorni di allenamento. Onora i cicli del tuo corpo."
- [ ] Physical Recovery: "Il tuo {Segno} sa: la crescita avviene durante il recupero, non durante l'azione."
- [ ] Emotional Critical: "La tua sensibilità {Segno} è un dono. Onora i tuoi ritmi emotivi."
- [ ] Intellectual Critical: "Il tuo {Segno} sa: non ogni giorno è per il genio. Alcuni giorni sono per presentarsi."

---

## 🔄 HOW TO CHANGE LANGUAGE FOR TESTING

### Option 1: In-App Settings
1. Open the app
2. Go to **Settings** → **Language**
3. Select language (English, Español, Português, Français, Deutsch, Italiano)
4. Navigate back to Cosmic Coach
5. Verify messages are in the selected language

### Option 2: Device Settings (iOS)
1. Open **Settings** app
2. Go to **General** → **Language & Region**
3. Add/select preferred language
4. Restart the app
5. Verify messages update

---

## 🐛 WHAT COULD GO WRONG

### Issue 1: Messages Still in English
**Possible Causes:**
- Language code not being passed correctly to `generateBiorhythmGoals()`
- User's language preference not being detected

**How to Debug:**
```dart
// Add debug print in biorhythm_goal_generator.dart
print('🌐 Generating goals with language: $languageCode');
```

### Issue 2: Zodiac Sign Not Translated
**Expected Behavior:**
- The zodiac sign name itself should be translated elsewhere in the app
- Example: "Taurus" → "Tauro" (Spanish), "Touro" (Portuguese), etc.

**Note:** This fix only translates the motivational message template, not the zodiac sign names themselves.

### Issue 3: Some Languages Work, Others Don't
**Check:**
- Verify the language code being passed matches our supported codes
- Supported: 'en', 'es', 'pt', 'fr', 'de', 'it'
- Unsupported languages should fallback to English

---

## 🎯 TESTING SCENARIOS

### Scenario 1: Language Switching
1. Start in English
2. Note the motivational message
3. Switch to Spanish
4. Verify message changes to Spanish
5. Repeat for all languages

### Scenario 2: Different Zodiac Signs
Test with multiple zodiac signs to ensure the `$zodiacSign` variable is properly inserted:
- Aries
- Taurus
- Gemini
- Cancer
- Leo
- Virgo
- Libra
- Scorpio
- Sagittarius
- Capricorn
- Aquarius
- Pisces

### Scenario 3: Different Biorhythm Phases
The motivational messages only appear in these phases:
- **Physical Critical** (transition day)
- **Physical Recovery** (low energy day)
- **Emotional Critical** (transition day)
- **Intellectual Critical** (transition day)

**Note:** Peak phases already had translations and were not modified.

---

## 📱 WHERE TO FIND THESE MESSAGES IN THE APP

### Location in UI
1. Open **Cosmic Coach** tab
2. Scroll to **Biorhythm Goals** section
3. Look for goal cards with:
   - Yellow/orange border (critical phase)
   - Blue/calm colors (recovery phase)
4. The motivational message appears at the bottom of each goal card

### When These Goals Appear
These goals are **automatically generated** based on your:
- **Birth date** (determines biorhythm cycles)
- **Current date** (determines current phase)

Critical/recovery phases occur approximately:
- **Physical Critical:** Every ~23 days
- **Physical Recovery:** Days 12-23 of physical cycle
- **Emotional Critical:** Every ~28 days
- **Intellectual Critical:** Every ~33 days

---

## ✅ SUCCESS CRITERIA

The implementation is successful if:

1. ✅ **All 4 message types** are translated in all 6 languages
2. ✅ **Language switching** works without restarting the app
3. ✅ **Zodiac sign** is properly inserted into the message
4. ✅ **No syntax errors** or crashes
5. ✅ **English fallback** works for unsupported languages
6. ✅ **Messages are readable** and grammatically correct

---

## 🚀 NEXT STEPS AFTER TESTING

If everything works:
1. Mark this task as complete
2. Update the main project documentation
3. Consider adding unit tests for these methods

If issues are found:
1. Document the specific issue
2. Check the language code being passed
3. Verify zodiac sign translation is working
4. Review console logs for errors

---

**Testing prepared by: Claude Code Agent**
**Date:** November 13, 2025
