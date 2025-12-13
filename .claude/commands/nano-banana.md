# Nano Banana - PDF Icon Generator Agent

Agente especializado en generación de iconos PNG para PDFs usando **Google Gemini AI (Nano Banana)**.

## Uso Rápido

```bash
# Generar TODOS los iconos (~54 imágenes, ~$2.10)
node .claude/scripts/nano-banana-generator.js --type all

# Ver ayuda completa
node .claude/scripts/nano-banana-generator.js --help
```

## Categorías de Iconos

| Categoría | Cantidad | Tamaño | Descripción |
|-----------|----------|--------|-------------|
| `zodiac` | 12 | 128x128 px | Constelaciones zodiacales |
| `planets` | 10 | 64x64 px | Símbolos planetarios |
| `moon` | 8 | 48x48 px | Fases lunares |
| `activities` | 12 | 32x32 px | Iconos de actividades |
| `decorative` | 10 | 24x24 px | Elementos decorativos |
| `cover` | - | 1200x800 px | Portadas de PDF |

## Comandos por Categoría

```bash
# Signos zodiacales
node .claude/scripts/nano-banana-generator.js --type zodiac --all
node .claude/scripts/nano-banana-generator.js --type zodiac --items "aries,leo"

# Planetas
node .claude/scripts/nano-banana-generator.js --type planets --all

# Fases lunares
node .claude/scripts/nano-banana-generator.js --type moon --all

# Actividades
node .claude/scripts/nano-banana-generator.js --type activities --all

# Decorativos
node .claude/scripts/nano-banana-generator.js --type decorative --all

# Portada de compatibilidad
node .claude/scripts/nano-banana-generator.js --type cover --signs "aries,leo"

# Prompt personalizado (con modelo Pro)
node .claude/scripts/nano-banana-generator.js --prompt "mystical sun" --pro
```

## Estructura de Output

```
zodiac_app/assets/images/pdf_icons/
├── zodiac/           # aries.png, taurus.png, ...
├── planets/          # venus.png, mars.png, ...
├── moon_phases/      # new_moon.png, full_moon.png, ...
├── activities/       # stargazing.png, dinner.png, ...
├── decorative/       # star_gold.png, heart_pink.png, ...
└── covers/           # cover_aries_leo.png, ...
```

## Especificaciones Técnicas

- **Formato**: PNG-24 con transparencia (alpha channel)
- **Estilo**: Línea dorada (#FFD700) sobre fondo transparente
- **Resolución**: Optimizado para PDFs (300 DPI equivalente)
- **Modo color**: RGBA

## Iconos Incluidos

### Zodiac (12)
aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces

### Planets (10)
venus, mars, jupiter, saturn, mercury, moon, sun, uranus, neptune, pluto

### Moon Phases (8)
new_moon, waxing_crescent, first_quarter, waxing_gibbous, full_moon, waning_gibbous, last_quarter, waning_crescent

### Activities (12)
stargazing, dinner, theater, meditation, sports, art, travel, cooking, music, reading, nature, spa

### Decorative (10)
star_gold, heart_pink, checkmark, sparkles, infinity, arrow_up, arrow_down, circle_dot, diamond, cross

## Costo Estimado

- ~$0.039 por imagen
- ~$2.10 por todos los 54 iconos
- Los iconos se generan una vez y se reutilizan infinitamente

## Requisitos

- API Key de Google AI Studio con billing habilitado
- Node.js 16+