# iOS Widget System - Technical Specification

## Executive Summary

Arcanapp implements a **complete WidgetKit ecosystem** that no other astrology app in the App Store offers. This document provides technical evidence of our unique widget implementation.

---

## iOS Home Screen Widgets (4 Total)

### 1. Daily Horoscope Widget
**File:** `ios/ArcanappWidgets/DailyHoroscopeWidget.swift`

| Feature | Description |
|---------|-------------|
| Sizes | Small, Medium |
| Data Source | App Groups shared container |
| Update Frequency | Every 6 hours |
| Personalization | User's zodiac sign, daily message |
| Visual Elements | Zodiac symbol, energy level, lucky element |

### 2. Moon Phase Widget
**File:** `ios/ArcanappWidgets/MoonPhaseWidget.swift`

| Feature | Description |
|---------|-------------|
| Sizes | Small, Medium |
| Calculation | Astronomical algorithm based on synodic month (29.53059 days) |
| Data Points | Phase name, emoji, illumination percentage |
| Predictions | Next phase date calculation |

**Technical Implementation:**
- Uses reference new moon date (January 6, 2000 at 18:14 UTC)
- Calculates precise illumination using cosine function
- Supports all 8 lunar phases

### 3. Biorhythm Widget
**File:** `ios/ArcanappWidgets/BiorhythmWidget.swift` (1107 lines of Swift code)

| Feature | Description |
|---------|-------------|
| Sizes | Small, Medium, Large |
| Cycles | 7 total (Physical, Emotional, Intellectual + 4 extended) |
| Visualization | Progress bars, sparkline charts, circular gauges |
| Predictions | Critical day alerts, peak predictions, activity suggestions |

**Unique Features:**
- **7-day sparkline forecast** with 3-color visualization
- **Critical day warning system** (exclamation triangle when approaching zero-crossing)
- **Activity recommendations** based on cycle combination
- **Extended cycles** (Intuitive 38-day, Spiritual 53-day, Aesthetic 43-day, Awareness 48-day)

**Mathematical Foundation:**
```swift
// Cycle periods in days
let physicalPeriod = 23
let emotionalPeriod = 28
let intellectualPeriod = 33
let intuitivePeriod = 38
let spiritualPeriod = 53
let aestheticPeriod = 43
let awarenessPeriod = 48
```

### 4. Lucky Numbers Widget
**File:** `ios/ArcanappWidgets/LuckyNumbersWidget.swift`

| Feature | Description |
|---------|-------------|
| Size | Small |
| Numbers | 6 daily numbers |
| Algorithm | Deterministic generation based on date and user data |
| Visual | Grid layout with golden gradient circles |

---

## watchOS Companion App

**Directory:** `ios/ArcanappWatch Watch App/`

### 5 Swipeable Views:

1. **Biorhythm View** (`BiorhythmWatchView`)
   - 3 main cycles with progress bars
   - Extended cycles in compact grid
   - Critical day warnings
   - Activity suggestions

2. **Predictions View** (`BiorhythmPredictionsWatchView`)
   - Next peak prediction
   - Critical day warnings
   - Next low prediction
   - Weekly overview with color-coded day indicators
   - Average energy summary

3. **Horoscope View** (`HoroscopeWatchView`)
   - Zodiac symbol (Unicode)
   - Sign name
   - Energy level
   - Daily message (3 lines max)

4. **Moon Phase View** (`MoonPhaseWatchView`)
   - Large phase emoji
   - Phase name
   - Illumination percentage
   - Guidance description

5. **Lucky Numbers View** (`LuckyNumbersWatchView`)
   - 6 numbers in 3x2 grid
   - Golden gradient design
   - Star icon header

### Watch Face Complications:

**File:** `ios/ArcanappWatch Watch App/Complications.swift`

1. **Circular Complication** - Biorhythm gauge with percentage
2. **Modular Complication** - Text display with cycle status

---

## Data Synchronization Architecture

```
┌─────────────────┐     App Groups      ┌─────────────────┐
│   Flutter App   │ ◄─────────────────► │   iOS Widgets   │
│   (Main App)    │   Shared Container  │   (WidgetKit)   │
└────────┬────────┘                     └────────┬────────┘
         │                                       │
         │         App Groups                    │
         └─────────────────────────────────────►│
                                                 │
                                        ┌────────▼────────┐
                                        │   watchOS App   │
                                        │  (WatchKit)     │
                                        └─────────────────┘
```

**App Group ID:** `group.com.zodiac.app.zodiacApp`

**Shared Data Keys:**
- `biorhythm_widget` - JSON with 7 cycle percentages, predictions, sparkline data
- `daily_horoscope_widget` - JSON with sign, message, energy level
- `moon_phase_widget` - JSON with phase data, illumination
- `lucky_numbers_widget` - JSON with 6 numbers array

---

## Lines of Native Swift Code

| Component | Lines of Code |
|-----------|---------------|
| BiorhythmWidget.swift | 1,107 |
| DailyHoroscopeWidget.swift | ~300 |
| MoonPhaseWidget.swift | ~250 |
| LuckyNumbersWidget.swift | ~200 |
| ContentView.swift (watchOS) | 899 |
| Complications.swift | ~150 |
| **Total Native Swift** | **~2,900 lines** |

---

## Competitive Analysis

| Feature | Co-Star | The Pattern | Sanctuary | Nebula | **Arcanapp** |
|---------|---------|-------------|-----------|--------|------------------------|
| Home Screen Widgets | 0 | 0 | 0 | 0 | **4 widgets** |
| watchOS App | No | No | No | No | **Yes (5 views)** |
| Watch Complications | No | No | No | No | **Yes (2 types)** |
| Biorhythm Widget | No | No | No | No | **Yes (unique)** |
| 7-Day Sparkline | No | No | No | No | **Yes (unique)** |

**Conclusion:** No astrology app in the App Store offers this level of WidgetKit and watchOS integration.

---

## Screenshots Available

1. iOS Home Screen showing all 4 widgets
2. Biorhythm widget (all 3 sizes)
3. watchOS app - all 5 views
4. Watch face with complications

---

*Document prepared for Apple App Review Appeal*
*February 2025*
