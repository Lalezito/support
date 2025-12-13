# 📊 Mapa Completo de social_sharing_service.dart

**Archivo:** `lib/services/social_sharing_service.dart`
**Líneas totales:** 3,545
**Fecha análisis:** Noviembre 2025
**Backup:** `social_sharing_service.dart.backup` ✅

---

## 📋 ESTRUCTURA DEL ARCHIVO

### 1. IMPORTS (Líneas 1-15)
```dart
- dart:io, dart:math, dart:typed_data, dart:ui
- flutter/material.dart, flutter/rendering.dart
- google_fonts, share_plus, appinio_social_share, url_launcher, path_provider
- models/horoscope.dart, l10n/app_localizations.dart
- core/types/compatibility_types.dart
```

### 2. ENUMS Y CLASES DE CONFIGURACIÓN (Líneas 18-139)

#### `enum ShareCardFormat` (Línea 18)
- `modern`
- `story`

#### `class _CardFormatConfig` (Línea 21-139)
**Propiedades de configuración de tarjetas** (69 propiedades):
- Dimensiones: width, height, pixelScale
- Insets: contentInsetX, contentInsetTop, contentInsetBottom
- Bordes: contentBorderRadius, borderGlowOpacity, borderGlowBlur, borderGlowSpread
- Header: headerScale
- Mood: moodFontScale, moodHorizontalPadding, moodVerticalPadding
- Sign: signFontMax, signFontMin, signNameMaxWidth, signFontDecrement, signOffsetX, signMarginRight, signMinYOffset
- Text Box: textBoxHorizontalMargin, textBoxTopOffset, textBoxHeightFactor, textBoxBorderRadius, textBoxBorderOpacity, textBoxBorderWidth
- Body: bodyFontSize, bodyLineHeight, bodyHorizontalPaddingFactor, bodyOffsetX, bodyOffsetY
- Date: dateFontSize
- Lucky: luckyTopSpacing, luckyBottomSpacing, luckyStartX, luckyMaxWidthFactor, luckyLabelFont, luckyValueFont, luckyLineSpacing, luckyCircleOffset, luckyCircleRadius, luckyCircleSpacing, luckyGlowScale, luckyColorSpacing, luckyMoodScale

---

### 3. CLASE PRINCIPAL: SocialSharingService (Línea 141-3545)

#### A. CONSTANTES DE PLATAFORMAS (Líneas 142-152)
```dart
SHARING_VERSION = 'SocialSharing-1.0.0'
PLATFORM_INSTAGRAM = 'instagram'
PLATFORM_FACEBOOK = 'facebook'
PLATFORM_TWITTER = 'twitter'
PLATFORM_WHATSAPP = 'whatsapp'
PLATFORM_TELEGRAM = 'telegram'
```

#### B. CONSTANTES DE BRANDING (Líneas 152-154)
```dart
APP_NAME = 'Zodiac Life Coach'
APP_DOWNLOAD_LINK = 'https://apps.apple.com/app/zodiac-life-coach'
WEBSITE_URL = 'https://zodiaclifecoach.app'
```

#### C. CONSTANTES DE DIMENSIONES (Líneas 157-169)
```dart
CARD_WIDTH = 1920.0
CARD_HEIGHT = 1080.0
BORDER_RADIUS = 24.0
PADDING = 40.0
MODERN_CARD_WIDTH = 2688.0
MODERN_CARD_HEIGHT = 1512.0
_SQUARE_CARD_WIDTH = 1080.0
_SQUARE_CARD_HEIGHT = 1080.0
_STORY_CARD_WIDTH = 1080.0
_STORY_CARD_HEIGHT = 1920.0
```

#### D. CONFIGURACIONES DE TARJETAS (Líneas 174-326)
```dart
Map<ShareCardFormat, _CardFormatConfig> _cardFormatConfigs
- ShareCardFormat.modern (152 líneas de config)
- ShareCardFormat.story (152 líneas de config)
```

#### E. TRADUCCIONES DE MESES (Líneas 327-416)
```dart
Map<String, List<String>> _monthNamesByLanguage
- 'en': ['January', 'February', ...]
- 'es': ['enero', 'febrero', ...]
- 'de': ['Januar', 'Februar', ...]
- 'fr': ['janvier', 'février', ...]
- 'it': ['gennaio', 'febbraio', ...]
- 'pt': ['janeiro', 'fevereiro', ...]
```

---

### 4. MÉTODOS PÚBLICOS DE COMPARTIR

#### `shareHoroscope()` (Líneas 417-584) - 168 líneas
**Parámetros:**
- required Horoscope horoscope
- String? platform
- required BuildContext context
- String? languageCode
- ShareCardFormat? format

**Funcionalidad:**
- Genera tarjeta de horóscopo
- Comparte en plataforma específica o general
- Genera texto para compartir
- Tracking de analytics

#### `shareCompatibility()` (Líneas 585-640) - 56 líneas
**Parámetros:**
- required CompatibilityResult compatibility
- String? platform
- required BuildContext context
- String? languageCode

**Funcionalidad:**
- Genera tarjeta de compatibilidad
- Comparte análisis de compatibilidad

#### `shareCosmicInsight()` (Líneas 641-688) - 48 líneas
**Parámetros:**
- required String insightText
- required String category
- String? platform
- required BuildContext context
- String? languageCode

**Funcionalidad:**
- Comparte insights cósmicos personalizados

---

### 5. GENERADORES DE TARJETAS (CARD GENERATORS)

#### `_generateHoroscopeCard()` (Líneas 689-705) - 17 líneas
Dispatcher que llama a Modern o Legacy según configuración

#### `_generateHoroscopeCardModern()` (Líneas 706-840) - 135 líneas
**Generador principal de tarjetas modernas**
- Layout 16:9 horizontal
- Diseño glassmorphism
- Efectos de glow
- Multi-idioma

#### `_generateHoroscopeCardLegacy()` (Líneas 841-938) - 98 líneas
**Generador de tarjetas legacy** (no usado actualmente)

#### `_generateCompatibilityCard()` (Líneas 939-1008) - 70 líneas
**Generador de tarjetas de compatibilidad**

#### `_generateCosmicInsightCard()` (Líneas 1009-1075) - 67 líneas
**Generador de tarjetas de insights**

---

### 6. UTILIDADES DE RENDERIZADO (Líneas 1076-2353)

#### `_captureWidget()` (Líneas 1076-1098) - 23 líneas
Captura widget a imagen usando RepaintBoundary

#### Métodos de dibujo (Líneas 1099-2353) - ~1,250 líneas
**IMPORTANTE: Esta es la sección MÁS GRANDE**

Incluye múltiples métodos privados estáticos:
- `_drawModernHoroscope()`
- `_drawLegacyHoroscope()`
- `_drawCompatibilityCard()`
- `_drawInsightCard()`
- Helpers de texto, colores, gradientes, efectos

---

### 7. TRADUCCIONES DE SIGNOS (Líneas 2354-2637)

#### `_signTranslations` (Líneas 2354-2452) - 99 líneas
```dart
Map<String, Map<String, String>>
- 'en': {'aries': 'Aries', ...}
- 'es': {'aries': 'Aries', ...}
- 'de', 'fr', 'it', 'pt'
```

#### `_signDateRanges` (Líneas 2453-2637) - 185 líneas
```dart
Map<String, Map<String, String>>
- Rangos de fechas por signo y idioma
- 6 idiomas × 12 signos = 72 entradas
```

---

### 8. MÉTODOS DE TEXTO Y FORMATO (Líneas 2638-3053)

#### `_drawCompatibilityText()` (Líneas 2638-2746) - 109 líneas
Dibuja texto de compatibilidad con layout responsive

#### `_drawInsightText()` (Líneas 2747-2949) - 203 líneas
Dibuja texto de insights con wrapping

#### Helpers de formato (Líneas 2950-3053) - ~100 líneas
- `_getTranslatedSignName()`
- `_formatDateRangeForSign()`
- `_getMonthName()`
- `_splitTextIntoLines()`
- etc.

---

### 9. UTILIDADES DE ARCHIVO (Líneas 3054-3132)

#### `_saveImageToTemp()` (Líneas 3054-3073) - 20 líneas
Guarda imagen en directorio temporal

#### `_shareGeneric()` (Líneas 3074-3132) - 59 líneas
Compartir genérico usando share_plus

---

### 10. ANALYTICS Y FONTS (Líneas 3133-3202)

#### `_trackSharingAnalytics()` (Líneas 3133-3143) - 11 líneas
Placeholder para analytics

#### `_ensureCanvasFontsLoaded()` (Líneas 3144-3202) - 59 líneas
Precarga fuentes de GoogleFonts

---

### 11. COMPARTIR EN PLATAFORMAS (Líneas 3203-3440)

#### `_shareToInstagram()` (Líneas 3203-3245) - 43 líneas
Compartir en Instagram Stories

#### `_shareToWhatsApp()` (Líneas 3246-3291) - 46 líneas
Compartir en WhatsApp

#### `_shareToFacebook()` (Líneas 3292-3335) - 44 líneas
Compartir en Facebook

#### `_shareToTwitter()` (Líneas 3336-3392) - 57 líneas
Compartir en Twitter/X

#### `_shareToTelegram()` (Líneas 3393-3440) - 48 líneas
Compartir en Telegram

---

### 12. HELPERS DE TEXTO (Líneas 3441-3545)

#### Métodos de generación de texto (Líneas 3441-3545) - ~100 líneas
- `_generateShareText()`
- `_generateCompatibilityText()`
- `_generateInsightText()`
- `_getHashtagsForLanguage()`
- `_getCompatibilityHashtags()`
- `_getInsightHashtags()`

---

## 📊 RESUMEN DE DISTRIBUCIÓN

| Sección | Líneas | % |
|---------|--------|---|
| Imports + Enums + Config | 1-139 | 139 (4%) |
| Constantes | 140-416 | 277 (8%) |
| Métodos públicos | 417-688 | 272 (8%) |
| Card generators | 689-1075 | 387 (11%) |
| Utilidades de dibujo | 1076-2353 | 1,278 (36%) ⭐ |
| Traducciones | 2354-2637 | 284 (8%) |
| Texto y formato | 2638-3053 | 416 (12%) |
| File utils | 3054-3132 | 79 (2%) |
| Analytics + Fonts | 3133-3202 | 70 (2%) |
| Platform sharing | 3203-3440 | 238 (7%) |
| Text helpers | 3441-3545 | 105 (3%) |
| **TOTAL** | **3,545** | **100%** |

---

## 🎯 PLAN DE REFACTORING

### Módulo 1: `branding_helper.dart` (~400 líneas)
**Contenido:**
- Constantes de plataformas (PLATFORM_*)
- Constantes de branding (APP_NAME, URLs)
- Constantes de dimensiones (CARD_WIDTH, etc)
- Configuraciones de tarjetas (_cardFormatConfigs)
- Traducciones de meses (_monthNamesByLanguage)

### Módulo 2: `share_localization_helper.dart` (~500 líneas)
**Contenido:**
- Traducciones de signos (_signTranslations)
- Rangos de fechas (_signDateRanges)
- Helpers de formato de texto
- Generación de hashtags
- Helpers de idioma

### Módulo 3: `card_generator_service.dart` (~1,400 líneas)
**Contenido:**
- _generateHoroscopeCard()
- _generateHoroscopeCardModern()
- _generateHoroscopeCardLegacy()
- _generateCompatibilityCard()
- _generateCosmicInsightCard()
- _captureWidget()
- TODAS las utilidades de dibujo (1,278 líneas)
- Helpers de texto y formato

### Módulo 4: `platform_share_service.dart` (~500 líneas)
**Contenido:**
- _shareToInstagram()
- _shareToWhatsApp()
- _shareToFacebook()
- _shareToTwitter()
- _shareToTelegram()
- _shareGeneric()
- _saveImageToTemp()
- Helpers de compartir

### Módulo 5: `social_sharing_service.dart` (REFACTORIZADO - ~750 líneas)
**Contenido:**
- Clase principal SocialSharingService
- shareHoroscope() - llama a CardGenerator + PlatformShare
- shareCompatibility() - llama a CardGenerator + PlatformShare
- shareCosmicInsight() - llama a CardGenerator + PlatformShare
- _trackSharingAnalytics()
- _ensureCanvasFontsLoaded()
- Imports de los 4 módulos

---

## ✅ CHECKLIST DE SEGURIDAD

- [x] Backup creado: `social_sharing_service.dart.backup`
- [ ] Todos los métodos públicos identificados
- [ ] Todos los métodos privados mapeados
- [ ] Todas las constantes documentadas
- [ ] Todas las traducciones preservadas
- [ ] Estructura de directorios creada
- [ ] Módulos extraídos y compilando
- [ ] Tests de integración pasando
- [ ] No se perdió ninguna funcionalidad

---

**Generado por:** Claude Code
**Fecha:** Noviembre 2025
