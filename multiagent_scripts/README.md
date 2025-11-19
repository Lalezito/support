# 🤖 Sistema Multiagente de Segmentación de Traducciones

Sistema automatizado para extraer traducciones de features específicos (Cosmic Coach) desde archivos de localización monolíticos a archivos modulares en 6 idiomas.

## 📋 Índice

- [Descripción General](#-descripción-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Agentes Disponibles](#-agentes-disponibles)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Flujo de Ejecución](#-flujo-de-ejecución)
- [Outputs Generados](#-outputs-generados)
- [Troubleshooting](#-troubleshooting)

## 🎯 Descripción General

Este sistema multiagente automatiza el proceso de segmentación de traducciones, permitiendo migrar de una arquitectura monolítica a una modular basada en features.

**Problema que resuelve:**
- Archivos `app_{lang}.arb` monolíticos difíciles de mantener
- Traducciones mezcladas de diferentes features
- Difícil rastrear completitud de traducciones por feature
- Complicado trabajar en paralelo en diferentes features

**Solución:**
- Extracción automática de keys por feature (Cosmic Coach)
- Validación de completitud en 6 idiomas
- Generación de archivos modulares independientes
- Reportes de calidad detallados
- Integración automatizada al proyecto

## 🏗 Arquitectura del Sistema

El sistema está compuesto por 10 agentes especializados organizados en 3 fases:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FASE 1: ANÁLISIS                              │
│                         (Secuencial)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Agent 1: ANALYZER       → Identifica keys de Cosmic Coach          │
│  Agent 2: VALIDATOR      → Valida completitud en 6 idiomas          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       FASE 2: EXTRACCIÓN                             │
│                         (Paralelo)                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Agent 3: EXTRACTOR_EN   → Extrae traducciones EN                   │
│  Agent 4: EXTRACTOR_ES   → Extrae traducciones ES                   │
│  Agent 5: EXTRACTOR_DE   → Extrae traducciones DE                   │
│  Agent 6: EXTRACTOR_FR   → Extrae traducciones FR                   │
│  Agent 7: EXTRACTOR_IT   → Extrae traducciones IT                   │
│  Agent 8: EXTRACTOR_PT   → Extrae traducciones PT                   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                  FASE 3: VERIFICACIÓN E INTEGRACIÓN                  │
│                         (Secuencial)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Agent 9: QUALITY_CHECKER → Valida calidad de archivos              │
│  Agent 10: INTEGRATOR     → Integra al proyecto                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 🤖 Agentes Disponibles

### Agent 1: ANALYZER
**Rol:** Analista de Estructura
- **Input:** `app_en.arb`
- **Output:** `cosmic_coach_keys.txt`, `translation_categories_map.json`
- **Función:** Identifica todas las keys relacionadas con Cosmic Coach usando patrones de búsqueda

### Agent 2: VALIDATOR
**Rol:** Validador de Completitud
- **Input:** `cosmic_coach_keys.txt`, `app_{lang}.arb` (6 archivos)
- **Output:** `completeness_report.json`
- **Función:** Verifica que todas las keys existan en los 6 idiomas

### Agents 3-8: EXTRACTORS
**Rol:** Extractores de Traducciones
- **Input:** `cosmic_coach_keys.txt`, `app_{lang}.arb`
- **Output:** `cosmic_coach_{lang}.arb`
- **Función:** Extrae las keys identificadas a archivos modulares
- **Nota:** Keys faltantes se marcan como `MISSING_TRANSLATION`

### Agent 9: QUALITY_CHECKER
**Rol:** Verificador de Calidad
- **Input:** `cosmic_coach_{lang}.arb` (6 archivos)
- **Output:** `quality_report.json`
- **Función:** Valida sintaxis JSON, cuenta keys, verifica consistencia

### Agent 10: INTEGRATOR
**Rol:** Integrador al Proyecto
- **Input:** `cosmic_coach_{lang}.arb` (6 archivos)
- **Output:** Archivos copiados a proyecto + `INTEGRATION_GUIDE.md`
- **Función:** Copia archivos al proyecto y genera guía de integración

## 📦 Requisitos

### Software Necesario
- **Bash** 4.0+ (macOS viene con Bash 3.2, puede funcionar pero 4.0+ es recomendado)
- **jq** - Parser JSON para Bash
  ```bash
  brew install jq
  ```
- **bc** - Calculadora para Bash (generalmente pre-instalado)

### Verificar Instalación
```bash
# Verificar jq
jq --version

# Verificar bc
bc --version

# Verificar bash
bash --version
```

## 🚀 Instalación

1. **Clonar o ubicar el proyecto:**
   ```bash
   cd /Users/alejandrocaceres/Desktop/appstore.zodia
   ```

2. **Verificar estructura:**
   ```bash
   ls -la multiagent_scripts/
   # Deberías ver todos los scripts 01-10 + run_all_agents.sh
   ```

3. **Hacer scripts ejecutables:**
   ```bash
   chmod +x multiagent_scripts/*.sh
   ```

4. **Verificar que jq esté instalado:**
   ```bash
   which jq
   # Si no está instalado: brew install jq
   ```

## 💻 Uso

### Opción 1: Ejecutar Todo el Sistema (Recomendado)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia
./multiagent_scripts/run_all_agents.sh
```

Este comando ejecutará:
- **Fase 1** (Secuencial): Análisis y validación
- **Fase 2** (Paralelo): Extracción de 6 idiomas simultáneamente
- **Fase 3** (Secuencial): Verificación e integración

### Opción 2: Ejecutar Agentes Individuales

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia

# Ejecutar solo el analizador
./multiagent_scripts/01_analyzer.sh

# Ejecutar solo el validador
./multiagent_scripts/02_validator.sh

# Ejecutar un extractor específico
./multiagent_scripts/03_extractor_en.sh

# Ejecutar verificador de calidad
./multiagent_scripts/09_quality_checker.sh

# Ejecutar integrador
./multiagent_scripts/10_integrator.sh
```

### Opción 3: Ejecutar por Fases

```bash
# Fase 1: Análisis
./multiagent_scripts/01_analyzer.sh
./multiagent_scripts/02_validator.sh

# Fase 2: Extracción (manual, uno por uno)
./multiagent_scripts/03_extractor_en.sh
./multiagent_scripts/04_extractor_es.sh
# ... etc

# Fase 3: Verificación
./multiagent_scripts/09_quality_checker.sh
./multiagent_scripts/10_integrator.sh
```

## 🔄 Flujo de Ejecución

### Flujo Detallado

```
1. ANALYZER (Agent 1)
   ├─ Lee app_en.arb
   ├─ Busca patterns: cosmic, coach, goal, habit, etc.
   ├─ Genera cosmic_coach_keys.txt con ~150-300 keys
   └─ Genera translation_categories_map.json

2. VALIDATOR (Agent 2)
   ├─ Lee cosmic_coach_keys.txt
   ├─ Verifica existencia en app_{lang}.arb (6 idiomas)
   ├─ Identifica keys faltantes por idioma
   └─ Genera completeness_report.json

3. EXTRACTORS (Agents 3-8) - EN PARALELO
   ├─ Cada agente procesa su idioma
   ├─ Extrae keys de cosmic_coach_keys.txt
   ├─ Marca MISSING_TRANSLATION si no existe
   └─ Genera cosmic_coach_{lang}.arb

4. QUALITY_CHECKER (Agent 9)
   ├─ Valida sintaxis JSON de 6 archivos
   ├─ Cuenta keys por idioma
   ├─ Verifica consistencia
   ├─ Calcula quality score (0-100)
   └─ Genera quality_report.json

5. INTEGRATOR (Agent 10)
   ├─ Crea estructura de directorios
   ├─ Copia archivos a proyecto
   ├─ Actualiza l10n.yaml
   └─ Genera INTEGRATION_GUIDE.md
```

### Tiempos Estimados

- **Agent 1 (ANALYZER):** ~5-10 segundos
- **Agent 2 (VALIDATOR):** ~10-15 segundos
- **Agents 3-8 (EXTRACTORS):** ~30-60 segundos (en paralelo)
- **Agent 9 (QUALITY_CHECKER):** ~5-10 segundos
- **Agent 10 (INTEGRATOR):** ~5-10 segundos

**Total estimado:** ~1-2 minutos

## 📊 Outputs Generados

### Directorio de Salida
```
/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/
├── cosmic_coach_keys.txt                    # Lista de keys identificadas
├── translation_categories_map.json          # Mapa de categorías
├── completeness_report.json                 # Reporte de completitud
├── quality_report.json                      # Reporte de calidad
├── INTEGRATION_GUIDE.md                     # Guía de integración
├── agent1_analyzer_report.txt              # Reporte Agent 1
├── agent2_validator_report.txt             # Reporte Agent 2
├── agent3_extractor_en_report.txt          # Reporte Agent 3
├── ... (reportes agents 4-10)
├── features/
│   └── cosmic_coach/
│       ├── cosmic_coach_en.arb             # Traducciones EN
│       ├── cosmic_coach_es.arb             # Traducciones ES
│       ├── cosmic_coach_de.arb             # Traducciones DE
│       ├── cosmic_coach_fr.arb             # Traducciones FR
│       ├── cosmic_coach_it.arb             # Traducciones IT
│       └── cosmic_coach_pt.arb             # Traducciones PT
├── logs/
│   ├── agent1_ANALYZER.log
│   ├── agent2_VALIDATOR.log
│   └── ... (logs de todos los agentes)
└── temp/
    └── ... (archivos temporales)
```

### Archivos Clave

#### `cosmic_coach_keys.txt`
Lista de todas las keys identificadas para Cosmic Coach:
```
cosmicCoachTitle
cosmicCoachSubtitle
goalPlanner
addGoal
...
```

#### `completeness_report.json`
Reporte de completitud por idioma:
```json
{
  "total_keys_to_validate": 250,
  "languages": {
    "en": {
      "present_keys": 250,
      "missing_keys": 0,
      "completeness_percentage": 100.00,
      "status": "complete"
    },
    "es": {
      "present_keys": 248,
      "missing_keys": 2,
      "completeness_percentage": 99.20,
      "status": "incomplete",
      "missing_keys_list": ["key1", "key2"]
    }
    ...
  }
}
```

#### `quality_report.json`
Reporte de calidad de archivos generados:
```json
{
  "overall_quality_score": 95,
  "files": {
    "en": {
      "json_valid": true,
      "key_count": 250,
      "missing_translations": 0,
      "quality_score": 100,
      "status": "perfect"
    },
    ...
  }
}
```

## 🔍 Troubleshooting

### Error: `jq: command not found`
```bash
# Solución:
brew install jq
```

### Error: `bc: command not found`
```bash
# Solución:
brew install bc
```

### Error: `cosmic_coach_keys.txt no encontrado`
```bash
# Solución: Ejecutar Agent 1 primero
./multiagent_scripts/01_analyzer.sh
```

### Error: `JSON inválido en archivos generados`
```bash
# Revisar logs del agente que falló
cat multiagent_output/logs/agent3_EXTRACTOR_EN.log

# Verificar archivos fuente
jq empty zodiac_app/assets/l10n/app_en.arb
```

### Warning: `Keys marcadas como MISSING_TRANSLATION`
Esto es normal si algunas traducciones no existen en el archivo original.

**Solución:**
1. Revisar `completeness_report.json` para ver qué keys faltan
2. Agregar traducciones manualmente a los archivos `.arb`
3. Re-ejecutar el extractor correspondiente

### Error: `Permission denied`
```bash
# Solución: Hacer scripts ejecutables
chmod +x multiagent_scripts/*.sh
```

### Verificar Estado del Sistema
```bash
# Ver todos los reportes generados
ls -lh multiagent_output/*.txt
ls -lh multiagent_output/*.json

# Ver calidad general
cat multiagent_output/quality_report.json | jq '.overall_quality_score'

# Ver keys faltantes por idioma
cat multiagent_output/completeness_report.json | jq '.languages'
```

## 📝 Notas Importantes

### Patrones de Búsqueda
El Agent 1 (ANALYZER) busca estas palabras clave:
- `cosmic`
- `coach`
- `goal`
- `habit`
- `micro`
- `celebration`
- `smart_goals`
- `new_goals`
- `addGoal`
- `completeGoal`
- `deleteGoal`

Si necesitas agregar más patrones, edita `01_analyzer.sh` línea 41-52.

### Keys Metadata
Keys que empiezan con `@` (como `@goalPlanner`) son metadata de Flutter ARB y se incluyen automáticamente.

### Backup Automático
El Agent 10 (INTEGRATOR) crea backups automáticos antes de sobrescribir archivos:
- Formato: `cosmic_coach_{lang}.arb.backup.YYYYMMDD_HHMMSS`
- Ubicación: `zodiac_app/assets/l10n/features/cosmic_coach/`

### Ejecución Paralela
Los Agents 3-8 se ejecutan en paralelo para optimizar tiempo. Cada uno trabaja con su idioma independientemente.

## 🎯 Próximos Pasos Después de la Ejecución

1. **Revisar Reportes:**
   ```bash
   cat multiagent_output/quality_report.json | jq '.'
   cat multiagent_output/INTEGRATION_GUIDE.md
   ```

2. **Completar Traducciones Faltantes:**
   - Buscar `MISSING_TRANSLATION` en archivos generados
   - Traducir desde la referencia en inglés
   - Reemplazar el marcador con la traducción

3. **Regenerar Localizaciones:**
   ```bash
   cd zodiac_app
   flutter gen-l10n
   ```

4. **Actualizar Código:**
   ```dart
   // Usar CosmicCoachLocalizations en lugar de AppLocalizations
   import 'package:flutter_gen/gen_l10n/cosmic_coach_localizations.dart';

   final l10n = CosmicCoachLocalizations.of(context);
   Text(l10n.cosmicCoachTitle);
   ```

5. **Testing:**
   ```bash
   flutter test
   flutter run
   ```

## 📞 Soporte

Para reportar issues o hacer preguntas:
- Revisar logs en: `multiagent_output/logs/`
- Verificar reportes en: `multiagent_output/`
- Consultar `quality_report.json` para diagnóstico

---

**Sistema creado por:** Zodiac App Development Team
**Versión:** 1.0.0
**Fecha:** Noviembre 2025
**Licencia:** Uso interno del proyecto
