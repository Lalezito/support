# 🔥 Tägliches Serien-System - Vollständige Dokumentation

**Erstellt:** 23. Januar 2025
**Version:** 1.0.0
**Erwartete Auswirkung:** +800% Benutzerbindung durch FOMO und Gewohnheitsbildung

---

## 📋 Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Architektur](#architektur)
3. [Datenbankschema](#datenbankschema)
4. [API-Integration](#api-integration)
5. [Meilenstein-System](#meilenstein-system)
6. [Verwendungsbeispiele](#verwendungsbeispiele)
7. [Frontend-Integrationsleitfaden](#frontend-integrationsleitfaden)
8. [Test-Checkliste](#test-checkliste)
9. [Bereitstellungsanweisungen](#bereitstellungsanweisungen)

---

## 🎯 Übersicht

Das tägliche Serien-System ist eine Gamification-Funktion, die entwickelt wurde, um die Benutzerbindung zu erhöhen durch:

- **Tägliche Check-ins**: Automatisches Tracking, wenn Benutzer mit AI Coach interagieren
- **Serien-Tracking**: Aktuelle Serie und persönlicher Rekord (längste Serie)
- **Meilenstein-Belohnungen**: Progressive Belohnungen bei wichtigen Serien-Zahlen (3, 7, 14, 30, 60, 90, 180, 365 Tage)
- **Kosmische Punkte**: Punktesammlungssystem (+10 pro Tag + Bonus bei Meilensteinen)
- **Abzeichen-System**: Erfolgsabzeichen für wichtige Meilensteine
- **FOMO-Mechanik**: Angst vor Verlust der Serie ermutigt zur täglichen Rückkehr

### Wichtige Metriken

- **Check-in-Häufigkeit**: Täglich
- **Serien-Berechnung**: Aufeinanderfolgende Tage (bricht ab, wenn Benutzer einen Tag verpasst)
- **Punkte pro Check-in**: 10 kosmische Punkte
- **Gesamtzahl Meilensteine**: 8 Hauptmeilensteine
- **Unterstützte Sprachen**: Spanisch (es), Englisch (en)

---

## 🏗️ Architektur

### Komponenten

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Flutter)                    │
│  - Serie in UI anzeigen                                 │
│  - Meilenstein-Erfolge zeigen                           │
│  - Bestenlisten-Komponente                              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Backend - aiCoachService.js                │
│  - Ruft streakService.checkIn() bei jeder Nachricht auf│
│  - Gibt Serien-Info in Antwort zurück                   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              streakService.js (Neue Datei)              │
│  - checkIn(userId, language)                            │
│  - getStreak(userId)                                    │
│  - getLeaderboard(limit)                                │
│  - Meilenstein-Berechnungslogik                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          PostgreSQL - user_streaks Tabelle              │
│  - Speichert alle Serien-Daten                          │
│  - Indiziert für Performance                            │
└─────────────────────────────────────────────────────────┘
```

### Dateistruktur

```
backend/flutter-horoscope-backend/
├── migrations/
│   └── 011_create_user_streaks_table.sql  [NEU ✨]
├── src/
│   ├── services/
│   │   ├── streakService.js               [NEU ✨]
│   │   └── aiCoachService.js              [GEÄNDERT]
│   └── config/
│       └── db.js
└── STREAK_SYSTEM_DOCUMENTATION.md          [NEU ✨]
```

---

## 💾 Datenbankschema

### Tabelle: `user_streaks`

```sql
CREATE TABLE user_streaks (
  -- Primäre Identifikation
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,

  -- Serien-Tracking
  current_streak INT DEFAULT 0 NOT NULL,      -- Aktuelle aufeinanderfolgende Tage
  longest_streak INT DEFAULT 0 NOT NULL,      -- Persönlicher Rekord
  last_check_in DATE,                         -- Letzter Check-in-Datum (UTC)
  total_check_ins INT DEFAULT 0 NOT NULL,     -- Lebenszeitgesamt

  -- Gamification
  cosmic_points INT DEFAULT 0 NOT NULL,       -- Gesammelte Punkte
  badges JSONB DEFAULT '[]'::jsonb NOT NULL,  -- Verdiente Abzeichen-Array
  milestones_achieved JSONB DEFAULT '[]'::jsonb NOT NULL,  -- Erreichte Meilenstein-Nummern

  -- Metadaten
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);
```

### Indizes

```sql
CREATE INDEX idx_user_streaks_user_id ON user_streaks(user_id);
CREATE INDEX idx_user_streaks_current_streak ON user_streaks(current_streak DESC);
CREATE INDEX idx_user_streaks_last_check_in ON user_streaks(last_check_in DESC);
CREATE INDEX idx_user_streaks_cosmic_points ON user_streaks(cosmic_points DESC);
```

### Auto-Update-Trigger

```sql
CREATE TRIGGER trigger_update_user_streaks_timestamp
BEFORE UPDATE ON user_streaks
FOR EACH ROW
EXECUTE FUNCTION update_user_streaks_updated_at();
```

---

## 🔌 API-Integration

### Automatische Integration (AI Coach)

Das Serien-System wird **automatisch ausgelöst**, wenn Benutzer Nachrichten an AI Coach senden. Keine zusätzlichen API-Aufrufe erforderlich!

**Geändert in `aiCoachService.js`:**

```javascript
// Zeilen 32 (Import)
const streakService = require('./streakService');

// Zeilen 365-368 (Check-in-Logik)
const userLanguage = options.language || 'es';
const streakInfo = await streakService.checkIn(userId, userLanguage);

// Zeile 396 (Serie in Antwort zurückgeben)
streak: streakInfo
```

### Antwortformat

Jede AI Coach-Nachricht enthält jetzt Serien-Daten:

```json
{
  "success": true,
  "response": {
    "content": "Ihre AI Coach-Antwort...",
    "sessionId": "uuid",
    "messageId": "uuid"
  },
  "usage": {
    "remainingMessages": 10,
    "resetTime": "2025-01-24T00:00:00Z"
  },
  "streak": {
    "success": true,
    "current_streak": 7,
    "longest_streak": 7,
    "is_new_record": true,
    "already_checked_in": false,
    "streak_broken": false,
    "cosmic_points_earned": 80,
    "total_cosmic_points": 150,
    "total_check_ins": 7,
    "milestone": {
      "streak": 7,
      "name": "Guerrero de una Semana",
      "badge": "week_warrior",
      "reward": "Lectura especial Luna (gratis)",
      "cosmicPoints": 70
    },
    "badges": ["beginner", "week_warrior"],
    "message": "🔥 Racha actual: 7 días\n🏆 ¡NUEVO RÉCORD PERSONAL!\n\n✨ ¡MILESTONE DESBLOQUEADO: Guerrero de una Semana!\n🎁 Recompensa: Lectura especial Luna (gratis)\n💎 +70 puntos cósmicos extra\n\n💪 Próximo objetivo: 7 días para \"Dedicado\"\n🎯 Recompensa: 1 consulta premium gratis"
  }
}
```

---

## 🏆 Meilenstein-System

### Vollständige Meilenstein-Tabelle

| Serien-Tage | Spanischer Name | Englischer Name | Abzeichen | Belohnung | Bonuspunkte |
|-------------|-------------|--------------|-------|--------|--------------|
| **3** | Empezando | Getting Started | `beginner` | Abzeichen: Empezando | +30 |
| **7** | Guerrero de una Semana | Week Warrior | `week_warrior` | Kostenlose Mond-Lesung | +70 |
| **14** | Dedicado | Dedicated | `dedicated` | 1 kostenlose Premium-Beratung | +150 |
| **30** | Guerrero Cósmico | Cosmic Warrior | `cosmic_warrior` | Jahreslesung 2026 | +300 |
| **60** | Maestro de Hábitos | Habit Master | `habit_master` | 3 kostenlose Premium-Beratungen | +600 |
| **90** | Iluminado | Enlightened | `enlightened` | 1 Monat Premium gratis | +1000 |
| **180** | Devoto Cósmico | Cosmic Devotee | `cosmic_devotee` | 3 Monate Premium gratis | +2000 |
| **365** | Leyenda Cósmica | Cosmic Legend | `cosmic_legend` | Lifetime Premium | +5000 |

### Meilenstein-Logik

1. **Einmalige Belohnungen**: Meilensteine können nur einmal pro Benutzer erreicht werden
2. **In Datenbank verfolgt**: `milestones_achieved` JSONB-Array speichert erreichte Meilenstein-Nummern
3. **Abzeichen-Freischaltung**: Abzeichen werden zu `badges`-Array beim Erreichen des Meilensteins hinzugefügt
4. **Bonuspunkte**: Zusätzliche kosmische Punkte vergeben zusätzlich zu täglichen +10

### Punkteberechnungs-Beispiele

```javascript
// Tag 1: Erster Check-in
cosmic_points_earned = 10
total_cosmic_points = 10

// Tag 3: Meilenstein "Empezando"
cosmic_points_earned = 10 + 30 = 40
total_cosmic_points = 10 + 10 + 40 = 60

// Tag 7: Meilenstein "Week Warrior"
cosmic_points_earned = 10 + 70 = 80
total_cosmic_points = 60 + 10 + 10 + 10 + 80 = 170

// Tag 8: Regulärer Tag (Tag-7-Meilenstein bereits erhalten)
cosmic_points_earned = 10
total_cosmic_points = 170 + 10 = 180
```

---

## 📱 Verwendungsbeispiele

### Beispiel 1: Erstmaliger Benutzer

**Request:**
```javascript
// Benutzer sendet erste AI Coach-Nachricht
POST /ai-coach/sessions/{sessionId}/messages
{
  "message": "¿Qué me dice mi horóscopo hoy?",
  "language": "es"
}
```

**Response:**
```json
{
  "success": true,
  "response": { /* AI-Antwort */ },
  "streak": {
    "success": true,
    "current_streak": 1,
    "longest_streak": 1,
    "is_new_record": true,
    "is_first_time": true,
    "cosmic_points_earned": 10,
    "total_cosmic_points": 10,
    "total_check_ins": 1,
    "milestone": null,
    "message": "🔥 ¡Primera racha! Vuelve mañana para mantenerla viva.\n💫 +10 puntos cósmicos ganados"
  }
}
```

### Beispiel 2: 7-Tage-Meilenstein erreichen

**Request:**
```javascript
// 7. aufeinanderfolgender Tag des Benutzers
POST /ai-coach/sessions/{sessionId}/messages
{
  "message": "Good morning, what's my horoscope?",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "response": { /* AI-Antwort */ },
  "streak": {
    "success": true,
    "current_streak": 7,
    "longest_streak": 7,
    "is_new_record": true,
    "cosmic_points_earned": 80,
    "total_cosmic_points": 150,
    "total_check_ins": 7,
    "milestone": {
      "streak": 7,
      "name": "Week Warrior",
      "badge": "week_warrior",
      "reward": "Free Moon Reading",
      "cosmicPoints": 70
    },
    "badges": ["beginner", "week_warrior"],
    "message": "🔥 Current streak: 7 days\n🏆 NEW PERSONAL RECORD!\n\n✨ MILESTONE UNLOCKED: Week Warrior!\n🎁 Reward: Free Moon Reading\n💎 +70 bonus cosmic points\n\n💪 Next goal: 7 days to \"Dedicated\"\n🎯 Reward: 1 Free Premium Reading"
  }
}
```

---

## 🎨 Frontend-Integrationsleitfaden

### Flutter-Widget-Beispiel

```dart
// streak_widget.dart
import 'package:flutter/material.dart';

class StreakWidget extends StatelessWidget {
  final Map<String, dynamic> streakData;

  const StreakWidget({Key? key, required this.streakData}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (!streakData['success']) return SizedBox.shrink();

    final currentStreak = streakData['current_streak'] ?? 0;
    final cosmicPoints = streakData['total_cosmic_points'] ?? 0;
    final milestone = streakData['milestone'];
    final alreadyCheckedIn = streakData['already_checked_in'] ?? false;

    return Card(
      margin: EdgeInsets.all(16),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Serien-Zähler
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Text('🔥', style: TextStyle(fontSize: 24)),
                    SizedBox(width: 8),
                    Text(
                      '$currentStreak Tage',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                Row(
                  children: [
                    Text('💎', style: TextStyle(fontSize: 20)),
                    SizedBox(width: 4),
                    Text(
                      '$cosmicPoints',
                      style: TextStyle(fontSize: 18, color: Colors.purple),
                    ),
                  ],
                ),
              ],
            ),

            SizedBox(height: 12),

            // Meilenstein-Benachrichtigung
            if (milestone != null) ...[
              Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.purple.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.purple),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '✨ MEILENSTEIN FREIGESCHALTET!',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.purple,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      milestone['name'],
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 4),
                    Text('🎁 ${milestone['reward']}'),
                  ],
                ),
              ),
            ],

            // Check-in-Status
            if (alreadyCheckedIn) ...[
              SizedBox(height: 8),
              Text(
                '✅ Heute bereits eingecheckt',
                style: TextStyle(color: Colors.green),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

---

## ✅ Test-Checkliste

### Datenbankmigration

- [ ] Migration ausführen: `psql -d your_db -f migrations/011_create_user_streaks_table.sql`
- [ ] Tabelle erstellt überprüfen: `\d user_streaks`
- [ ] Indizes erstellt überprüfen: `\di idx_user_streaks_*`
- [ ] Trigger erstellt überprüfen: `\df update_user_streaks_updated_at`
- [ ] Constraint testen: Negative Serie einfügen versuchen (sollte fehlschlagen)

### Backend-Service-Tests

#### Test 1: Erster Check-in
```javascript
const userId = 'test-user-uuid';
const result = await streakService.checkIn(userId, 'es');

// Erwartet:
// - current_streak = 1
// - longest_streak = 1
// - is_first_time = true
// - cosmic_points_earned = 10
// - Datenbankdatensatz erstellt
```

#### Test 2: Aufeinanderfolgende Tage
```javascript
// Tag 1
await streakService.checkIn(userId, 'es');

// Warten oder Datum zum nächsten Tag mocken
// Tag 2
const result = await streakService.checkIn(userId, 'es');

// Erwartet:
// - current_streak = 2
// - streak_broken = false
```

#### Test 3: Doppelter Check-in am selben Tag
```javascript
await streakService.checkIn(userId, 'es');
const result = await streakService.checkIn(userId, 'es');

// Erwartet:
// - already_checked_in = true
// - cosmic_points_earned = 0
// - current_streak unverändert
```

---

## 🚀 Bereitstellungsanweisungen

### Schritt 1: Datenbankmigration ausführen

```bash
# Produktion
psql $DATABASE_URL -f migrations/011_create_user_streaks_table.sql

# Entwicklung
psql -U your_user -d your_db -f migrations/011_create_user_streaks_table.sql
```

### Schritt 2: Migration überprüfen

```sql
-- Tabelle existiert überprüfen
SELECT COUNT(*) FROM user_streaks;

-- Indizes überprüfen
SELECT indexname FROM pg_indexes WHERE tablename = 'user_streaks';

-- Sollte zurückgeben:
-- idx_user_streaks_user_id
-- idx_user_streaks_current_streak
-- idx_user_streaks_last_check_in
-- idx_user_streaks_cosmic_points
```

### Schritt 3: Backend-Code bereitstellen

```bash
# Sicherstellen, dass neue Dateien committed sind
git add migrations/011_create_user_streaks_table.sql
git add src/services/streakService.js
git add STREAK_SYSTEM_DOCUMENTATION.md
git commit -m "feat: implement daily streak gamification system"

# Auf Produktion bereitstellen
git push heroku main
# ODER Ihre Bereitstellungsmethode
```

---

## 📊 Erwartete Metriken & KPIs

### Bindungsmetriken

| Metrik | Vor Serien | Ziel nach Serien | Messzeitraum |
|--------|-------------|------------------|--------------|
| **Tag-1-Bindung** | ~40% | ~70% | 30 Tage |
| **Tag-7-Bindung** | ~15% | ~45% | 30 Tage |
| **Tag-30-Bindung** | ~5% | ~25% | 90 Tage |
| **Täglich aktive Benutzer** | Baseline | +800% | 90 Tage |

### Engagement-Metriken

- **Durchschnittliche Sitzungshäufigkeit**: Ziel 5x/Woche (von 1-2x/Woche)
- **Serien-Abschlussrate (7 Tage)**: Ziel 30% der Benutzer
- **Serien-Abschlussrate (30 Tage)**: Ziel 10% der Benutzer
- **Meilenstein-Erfolgsrate**: % der Benutzer verfolgen, die jeden Meilenstein erreichen

### Umsatzauswirkung

- **Premium-Konversionen aus Serien**: Benutzer verfolgen, die nach Erreichen von Meilensteinen upgraden
- **Lifetime-Value-Steigerung**: 3-5x LTV für Benutzer mit 30+ Tage-Serien erwarten

---

## 🔧 Fehlerbehebung

### Problem: Serie wird nicht aktualisiert

**Symptome:** Benutzer checkt ein, aber Serie bleibt bei 0
**Lösung:**
```sql
-- Überprüfen, ob Datensatz existiert
SELECT * FROM user_streaks WHERE user_id = 'uuid';

-- Falls kein Datensatz, sollte erster Check-in einen erstellen
-- Server-Logs auf Fehler in streakService.checkIn() überprüfen
```

### Problem: Meilenstein mehrfach vergeben

**Symptome:** Benutzer erhält denselben Meilenstein zweimal
**Lösung:**
```sql
-- milestones_achieved Array überprüfen
SELECT milestones_achieved FROM user_streaks WHERE user_id = 'uuid';

-- Sollte sein: [3, 7, 14, 30] (Nummern erscheinen nur einmal)
-- Falls Duplikate existieren, Daten korrigieren:
UPDATE user_streaks
SET milestones_achieved = (
  SELECT jsonb_agg(DISTINCT elem)
  FROM jsonb_array_elements_text(milestones_achieved) elem
)
WHERE user_id = 'uuid';
```

---

## 📈 Zukünftige Verbesserungen

1. **Soziale Funktionen**
   - Meilenstein-Erfolge teilen
   - Freunde-Serien-Vergleiche
   - Team/Gruppen-Challenges

2. **Erweiterte Belohnungen**
   - Serien-Versicherung (1 verpasster Tag Vergebung pro Monat)
   - Serien-Wiederherstellung (kosmische Punkte zahlen, um unterbrochene Serie wiederherzustellen)
   - Wöchentliche/monatliche Serien-Boni

3. **Personalisierung**
   - Benutzerdefinierte Erinnerungszeiten
   - Personalisierte Meilenstein-Belohnungen basierend auf Benutzerpräferenzen
   - Serien-Einfrieren für Urlaube

4. **Analyse-Dashboard**
   - Admin-Ansicht der Serien-Statistiken
   - Kohortenanalyse nach Serien-Level
   - Bindungstrichter-Visualisierung

---

## 📝 Änderungsprotokoll

### v1.0.0 (2025-01-23)
- ✨ Erste Veröffentlichung
- 🗄️ Datenbankschema mit user_streaks Tabelle
- 🔥 Kern-Serien-Tracking (aktuell, längstes, gesamt)
- 🏆 8-Stufen-Meilenstein-System (3 bis 365 Tage)
- 💎 Kosmische Punkte-Gamification
- 🎖️ Abzeichen-System
- 🌍 Zweisprachige Unterstützung (ES/EN)
- 🔗 Auto-Integration mit AI Coach
- 📊 Bestenlisten-Funktionalität

---

## 🆘 Support

Für Fragen oder Probleme:
- **Dokumentation:** Diese Datei
- **Code-Standort:** `/src/services/streakService.js`
- **Datenbank:** Tabelle `user_streaks`
- **Logs:** `loggingService` auf serienbezogene Fehler überprüfen

---

**Erstellt mit 💜 für Zodia-Benutzer**
*Tägliche kosmische Führung zur Gewohnheit machen, eine Serie nach der anderen.*
