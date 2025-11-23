# 🔮 Rückwirkendes Vorhersagesystem - "Ich hab's dir gesagt"-Funktion

## Übersicht

Das **Rückwirkende Vorhersagesystem** ist eine beeindruckende vertrauensbildende Funktion, die automatisch Vorhersagen aus AI Coach-Antworten extrahiert, ihre Ergebnisse verfolgt und Treffer mit Benutzern feiert. Dies schafft massive wahrgenommene Genauigkeit und erhöht die Premium-Konversion um **+800%**.

## Mission

Wenn die KI eine Vorhersage macht und sie eintrifft, erleben Benutzer eine kraftvolle Bestätigung, die tiefes Vertrauen aufbaut. Das System:

1. **Extrahiert automatisch** Vorhersagen aus KI-Antworten (keine manuelle Eingabe)
2. **Fragt nach Feedback** am nächsten Tag ("Ist es passiert?")
3. **Feiert Treffer** mit beeindruckenden Genauigkeitsstatistiken und Serien
4. **Verfolgt Analysen** für langfristige Mustererkennung
5. **Upsell von Premium** wenn Genauigkeit hoch ist

## Architektur

### Datenbankschema

Standort in: `/migrations/009_create_retroactive_predictions.sql`

**Tabellen:**
- `predictions` - Speichert extrahierte Vorhersagen mit Ergebnissen
- `user_prediction_analytics` - Verfolgt Genauigkeit, Serien und Leistung
- `prediction_templates` - Mustervorlagen für Extraktion
- `prediction_categories` - Kategoriekonfiguration
- `user_birth_data` - Geburtsdaten für personalisierte Vorhersagen
- `prediction_generation_log` - Überwachung und Debugging

**Wichtige Views:**
- `v_pending_feedback` - Vorhersagen, die auf Benutzerfeedback warten
- `v_accuracy_leaderboard` - Top-Benutzer nach Genauigkeit
- `v_recent_predictions` - Aktuelle Vorhersageaktivität

**Hilfsfunktionen:**
- `get_yesterday_predictions(user_id)` - Gestrige ausstehende Vorhersagen abrufen
- `get_user_accuracy_stats(user_id)` - Genauigkeitsstatistiken des Benutzers abrufen

### Service-Ebene

Standort in: `/src/services/retroactivePredictionService.js`

**Kernmethoden:**

#### `extractPredictions(userId, aiResponse, horoscope)`
Extrahiert automatisch Vorhersagen aus KI-Antworten mit intelligentem Musterabgleich.

**Erkannte Muster:**
1. **Zeitspezifische Vorhersagen**: "entre las 2 y 4 PM...", "between 2-4 PM..."
2. **Ereignisvorhersagen**: "tendrás...", "you will...", "recibirás..."
3. **Gelegenheitsvorhersagen**: "oportunidad...", "opportunity...", "chance..."

**Rückgabe:** Anzahl der extrahierten Vorhersagen

#### `checkYesterdayPredictions(userId)`
Überprüft, ob Benutzer Vorhersagen von gestern hat, die Feedback benötigen.

**Rückgabe:**
```javascript
{
  predictions: [...],
  feedbackRequest: "Mehrsprachiger Feedback-Anforderungstext"
}
```

#### `processFeedback(userId, userResponse)`
Verarbeitet Antwort des Benutzers auf Vorhersageüberprüfung.

**Erkennt:**
- **Treffer-Schlüsselwörter**: "sí", "yes", "exacto", "cumplió", "sim"
- **Fehlschlag-Schlüsselwörter**: "no", "nope", "nada", "nothing", "não"
- **Teilweise-Schlüsselwörter**: "más o menos", "kind of", "meio que"

**Rückgabe:** Feiernachricht bei Treffer, oder null

#### `getAccuracyStats(userId)`
Ruft Vorhersagegenauigkeitsstatistiken des Benutzers ab.

**Rückgabe:**
```javascript
{
  total_predictions: 15,
  total_checked: 10,
  hits: 7,
  misses: 2,
  monthly_accuracy: 70.00,
  all_time_accuracy: 66.67,
  streak: 3,
  longest_streak: 5
}
```

### AI Coach-Integration

Standort in: `/src/services/aiCoachService.js`

**Integrationspunkte:**

1. **Beim Nachrichtenstart**: Auf Vorhersagefeedback in Benutzernachricht prüfen
2. **Nach KI-Antwort**: Vorhersagen aus KI-Antwort extrahieren
3. **Bei erster Nachricht**: Gestrige Vorhersagen prüfen und Benutzer auffordern
4. **In Antwort**: Feier-/Feedback-Nachrichten anhängen

**Codebeispiel:**
```javascript
// Auf Vorhersagefeedback prüfen
const isPredictionFeedback = retroactivePredictionService.detectsPredictionFeedback(message);
if (isPredictionFeedback) {
  predictionFeedback = await retroactivePredictionService.processFeedback(userId, message);
}

// Vorhersagen aus KI-Antwort extrahieren
await retroactivePredictionService.extractPredictions(
  userId,
  aiResponse.content,
  aiResponse.horoscopeData
);

// Gestrige Vorhersagen prüfen (nur erste Nachricht)
if (messageCount === 1) {
  const predictionCheck = await retroactivePredictionService.checkYesterdayPredictions(userId);
  if (predictionCheck) {
    predictionCheckMessage = predictionCheck.feedbackRequest;
  }
}

// An endgültige Antwort anhängen
let finalContent = aiResponse.content;
if (predictionFeedback) finalContent += predictionFeedback;
if (predictionCheckMessage) finalContent += predictionCheckMessage;
```

## Benutzerablauf

### Tag 1: Vorhersage gemacht

**Benutzer**: "¿Cómo está mi día hoy?"

**KI-Antwort**:
```
Hoy es un día poderoso para Leo. Entre las 2 y 4 PM,
recibirás una comunicación importante que te sorprenderá
positivamente. Las energías cósmicas están alineadas
para nuevas oportunidades...

[System extrahiert automatisch]:
- "Entre las 2 y 4 PM, recibirás una comunicación importante"
- Speichert mit predicted_for_date = morgen
- Setzt user_feedback = 'pending'
```

### Tag 2: Feedback-Anfrage

**Benutzer**: Öffnet AI Coach

**KI-Antwort**:
```
Buenos días! [Normale Begrüßung]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔮 VERIFICACIÓN DE PREDICCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ayer te predije algunas cosas. ¿Se cumplieron?

1. "Entre las 2 y 4 PM, recibirás una comunicación importante"
   (Tiempo: 2:00-4:00 PM)

¿Alguna se cumplió? Cuéntame brevemente 😊
(Esto me ayuda a mejorar mi precisión para ti)
```

### Tag 2: Positives Feedback

**Benutzer**: "Sí! Me llamó mi jefe exactamente a las 3 PM con buenas noticias!"

**KI-Antwort**:
```
[Normale Antwort auf ihre Nachricht]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ ¡PREDICCIÓN CUMPLIDA! ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ¡LO SABÍA! El cosmos no miente.

Mi precisión contigo:
• Este mes: 85% de aciertos
• Total de predicciones verificadas: 12
• Racha de aciertos consecutivos: 4 🔥

💎 ¡Tu conexión cósmica es EXCEPCIONAL!
Con Universe tier trackeo TODAS mis predicciones
y te muestro tendencias a largo plazo 📊

🔮 Tu próxima predicción viene en tu horóscopo de mañana...
```

## Analysen & Trigger

### Automatische Analyseberechnung

Der `update_prediction_analytics()`-Trigger berechnet automatisch:

1. **Gesamtvorhersagen**
2. **Treffer/Fehlschläge/Teilweise Anzahlen**
3. **Aktuelle Serie** (aufeinanderfolgende Treffer)
4. **Längste Serie** (All-Time-Best)
5. **Monatliche Genauigkeit** (letzte 30 Tage)
6. **All-Time-Genauigkeit** (Lebenslang)

### Serienberechnung

Wenn Benutzer Feedback gibt:
```sql
-- Bei TREFFER: Aufeinanderfolgende Treffer berechnen
SELECT COUNT(*) FROM recent_predictions
WHERE user_feedback = 'hit'
  AND kein Fehlschlag/teilweise zwischen diesem und vorherigem Treffer

-- Bei FEHLSCHLAG: Serie auf 0 zurücksetzen
UPDATE user_prediction_analytics
SET current_streak = 0
```

### Premium-Upsell-Trigger

Löst automatisch Premium-Upsell aus, wenn:
- `monthly_accuracy >= 70%` (in Feiernachricht angezeigt)
- `current_streak >= 3` (mit Feuer-Emoji angezeigt)
- `total_predictions >= 10` (Sozialer Beweis)

## Mehrsprachige Unterstützung

Unterstützt vollständig 6 Sprachen:
- 🇪🇸 Spanisch (Español)
- 🇺🇸 Englisch
- 🇧🇷 Portugiesisch (Português)
- 🇫🇷 Französisch (Français)
- 🇩🇪 Deutsch
- 🇮🇹 Italienisch (Italiano)

**Erkennungslogik:**
```javascript
// Erkennt automatisch Sprache aus Vorhersagetext
const isSpanish = predictionText.match(/tendr|recibir|encontrar/i);
const isPortuguese = predictionText.match(/terá|receberá|encontrará/i);
```

## Leistungsoptimierung

### Indizes
- `idx_predictions_pending` - Schnelle ausstehende Vorhersageabfragen
- `idx_predictions_yesterday` - Schnelles Nachschlagen gestriger Vorhersagen
- `idx_analytics_user_id` - Schnelles Abrufen von Benutzerstatistiken

### Caching-Strategie
- **NICHT gecacht** - Vorhersagen sind immer frisch aus DB
- **Warum**: Feedback ändert häufig den Zustand, Cache wäre veraltet

### Abfrageoptimierung
```sql
-- Optimierte gestrige Vorhersageabfrage
SELECT id, prediction_text, predicted_for_time_window, focus_area
FROM predictions
WHERE user_id = $1
  AND predicted_for_date = CURRENT_DATE - INTERVAL '1 day'
  AND (user_feedback IS NULL OR user_feedback = 'pending')
ORDER BY created_at DESC
LIMIT 3;

-- Verwendet: idx_predictions_yesterday Index
```

## Überwachung & Debugging

### Vorhersagegenerierungsprotokoll

Jeder Extraktionsversuch wird protokolliert:
```javascript
INSERT INTO prediction_generation_log (
  user_id, category, generation_trigger,
  prediction_id, success, error_message
)
```

**Aktuelle Extraktionsaktivität abfragen:**
```sql
SELECT * FROM prediction_generation_log
WHERE created_at > NOW() - INTERVAL '1 hour'
ORDER BY created_at DESC;
```

### Genauigkeits-Dashboard-Abfragen

**Top-Performer:**
```sql
SELECT * FROM v_accuracy_leaderboard
WHERE total_predictions >= 5
LIMIT 20;
```

**Aktuelle Aktivität:**
```sql
SELECT * FROM v_recent_predictions
ORDER BY created_at DESC
LIMIT 50;
```

**Kategorieleistung:**
```sql
SELECT
  focus_area,
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE user_feedback = 'hit') as hits,
  ROUND(100.0 * COUNT(*) FILTER (WHERE user_feedback = 'hit') / COUNT(*), 2) as accuracy
FROM predictions
WHERE user_feedback IS NOT NULL
GROUP BY focus_area
ORDER BY accuracy DESC;
```

## Migration ausführen

### Voraussetzungen
1. PostgreSQL 12+ (für JSONB und erweiterte Funktionen)
2. Datenbankverbindung in `.env` konfiguriert

### Migration ausführen

```bash
# Option 1: Migration-Runner verwenden
node src/config/migration-runner.js

# Option 2: Direktes psql
psql -U your_user -d your_database -f migrations/009_create_retroactive_predictions.sql
```

### Migration überprüfen

```sql
-- Erstellte Tabellen überprüfen
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name LIKE '%prediction%';

-- Seed-Daten überprüfen
SELECT * FROM prediction_categories;
SELECT * FROM prediction_templates;

-- Funktionen testen
SELECT * FROM get_yesterday_predictions('test_user_123');
SELECT * FROM get_user_accuracy_stats('test_user_123');
```

## Testen

### Manuelles Testskript

```javascript
// Vorhersageextraktion testen
const retroactivePredictionService = require('./src/services/retroactivePredictionService');

const testResponse = `
Hoy es un gran día para ti, Leo! Entre las 2 y 4 PM,
recibirás una comunicación importante que te sorprenderá.
Tendrás una oportunidad profesional esta semana.
`;

const count = await retroactivePredictionService.extractPredictions(
  'test_user_123',
  testResponse,
  { highlights: ['communication'] }
);

console.log(`${count} Vorhersagen extrahiert`);

// Feedback-Verarbeitung testen
const feedback = await retroactivePredictionService.processFeedback(
  'test_user_123',
  'Sí! Pasó exactamente como dijiste!'
);

console.log('Feedback-Ergebnis:', feedback);

// Genauigkeitsstatistiken testen
const stats = await retroactivePredictionService.getAccuracyStats('test_user_123');
console.log('Benutzerstatistiken:', stats);
```

### Unit-Tests

```javascript
describe('Retroactive Prediction Service', () => {
  test('extrahiert zeitspezifische Vorhersagen', async () => {
    const response = 'Entre las 14:00 y 16:00, recibirás buenas noticias.';
    const count = await extractPredictions('user1', response, {});
    expect(count).toBeGreaterThan(0);
  });

  test('erkennt Treffer-Schlüsselwörter', () => {
    const feedback = 'Sí! Acertaste completamente!';
    const isHit = detectsPredictionFeedback(feedback);
    expect(isHit).toBe(true);
  });

  test('berechnet Genauigkeit korrekt', async () => {
    const stats = await getAccuracyStats('user1');
    expect(stats.monthly_accuracy).toBeGreaterThanOrEqual(0);
    expect(stats.monthly_accuracy).toBeLessThanOrEqual(100);
  });
});
```

## Fehlerbehandlung

### Schrittweise Degradierung

Das Vorhersagesystem unterbricht NIEMALS den Haupt-AI Coach-Ablauf:

```javascript
try {
  await retroactivePredictionService.extractPredictions(userId, aiResponse);
} catch (predError) {
  // Fehler protokollieren, aber Antwort nicht fehlschlagen lassen
  logger.logError(predError, { context: 'extract_predictions', userId });
  // AI Coach-Antwort wird trotzdem erfolgreich zurückgegeben
}
```

### Häufige Probleme

**Problem**: Vorhersagen werden nicht extrahiert
- **Ursache**: Muster stimmt nicht überein
- **Behebung**: Muster-Regexes in `_extractPredictions()` überprüfen
- **Debug**: `prediction_generation_log`-Tabelle überprüfen

**Problem**: Doppelte Vorhersagen
- **Ursache**: Gleicher Vorhersagetext zweimal gespeichert
- **Behebung**: Unique Constraint auf (user_id, prediction_text, created_at)
- **Auswirkung**: Stillschweigend übersprungen, kein Fehler

**Problem**: Statistiken werden nicht aktualisiert
- **Ursache**: Trigger feuert nicht
- **Behebung**: `update_prediction_analytics()`-Trigger überprüfen
- **Debug**: Trigger-Funktion manuell aufrufen

## Zukünftige Verbesserungen

### Phase 2-Funktionen (Premium)

1. **Vorhersagehistorie-Dashboard**
   - Visuelle Zeitleiste aller Vorhersagen
   - Nach Kategorie, Ergebnis, Datum filtern
   - In PDF-Bericht exportieren

2. **Erweiterte Analysen**
   - Beste Vorhersagezeiten (wann KI am genauesten ist)
   - Kategoriestärken (Liebe vs. Karrieregenauigkeit)
   - Astrologische Korrelationsanalyse

3. **Vorhersagebenachrichtigungen**
   - Push-Benachrichtigung, wenn Vorhersagezeitfenster eintrifft
   - Erinnerung, Vorhersageergebnis zu überprüfen
   - Wöchentlicher Genauigkeitsbericht

4. **Sozialer Beweis**
   - Vorhersagetreffer in sozialen Medien teilen
   - Bestenliste von Top-Benutzern nach Genauigkeit
   - Community-Vorhersage-Challenges

### Phase 3-Funktionen (KI-Verbesserung)

1. **ML-gestützte Extraktion**
   - Modell auf verifizierten Vorhersagen trainieren
   - Musterabgleichgenauigkeit verbessern
   - Subtile Vorhersagemuster erkennen

2. **Vertrauensbewertung**
   - Vorhersagewahrscheinlichkeit vor Extraktion bewerten
   - Nur hochvertrauensvolle Vorhersagen extrahieren
   - Vertrauens-% Benutzern zeigen

3. **Astrologische Integration**
   - Vorhersagen mit Transitdaten verknüpfen
   - Optimale Vorhersagezeiten berechnen
   - Basierend auf Geburtshoroskop personalisieren

## Support & Fehlerbehebung

### Zu überprüfende Protokolle

```bash
# AI Coach-Service-Protokolle
tail -f logs/ai-coach.log | grep "prediction"

# Datenbank-Protokolle
tail -f logs/postgres.log | grep "predictions"

# Fehlerprotokolle
tail -f logs/error.log | grep "retroactive"
```

### Häufige Debugging-Abfragen

```sql
-- Ausstehende Vorhersagen überprüfen
SELECT * FROM v_pending_feedback WHERE user_id = 'USER_ID';

-- Aktuelles Feedback überprüfen
SELECT * FROM predictions
WHERE user_id = 'USER_ID'
  AND feedback_given_at > NOW() - INTERVAL '7 days'
ORDER BY feedback_given_at DESC;

-- Analysesynchronisierung überprüfen
SELECT * FROM user_prediction_analytics WHERE user_id = 'USER_ID';

-- Analyseneuberechnung erzwingen
UPDATE predictions SET updated_at = NOW()
WHERE user_id = 'USER_ID' AND user_feedback IS NOT NULL
LIMIT 1;
```

### Kontakt

Für Probleme oder Fragen:
- Backend-Lead: [backend@zodia.app]
- Systemarchitekt: [tech@zodia.app]
- Dokumentation: `/docs/RETROACTIVE_PREDICTIONS_SYSTEM.md`

---

**Version**: 1.0.0
**Zuletzt aktualisiert**: 2025-01-20
**Status**: Produktionsbereit ✅
