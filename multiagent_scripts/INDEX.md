# 📚 Índice del Sistema Multiagente

Índice completo de todos los archivos y scripts del sistema de segmentación de traducciones.

## 🎯 Archivos Principales

### Documentación
- **README.md** - Documentación completa del sistema
- **QUICK_START.md** - Guía de inicio rápido (5 minutos)
- **INDEX.md** - Este archivo (índice maestro)

### Scripts de Control
- **run_all_agents.sh** - Orquestador maestro (ejecuta todo el sistema)
- **verify_system.sh** - Verificador de requisitos y pre-flight check

## 🤖 Agentes del Sistema

### Fase 1: Análisis y Validación (Secuencial)

#### Agent 1: ANALYZER
- **Script:** `01_analyzer.sh`
- **Rol:** Analista de Estructura
- **Input:** `app_en.arb`
- **Output:** `cosmic_coach_keys.txt`, `translation_categories_map.json`
- **Función:** Identifica keys de Cosmic Coach usando patrones
- **Duración:** ~5-10 segundos

#### Agent 2: VALIDATOR
- **Script:** `02_validator.sh`
- **Rol:** Validador de Completitud
- **Input:** `cosmic_coach_keys.txt`, `app_{lang}.arb` (6 archivos)
- **Output:** `completeness_report.json`
- **Función:** Verifica existencia de keys en 6 idiomas
- **Duración:** ~10-15 segundos

### Fase 2: Extracción de Traducciones (Paralelo)

#### Agent 3: EXTRACTOR_EN
- **Script:** `03_extractor_en.sh`
- **Rol:** Extractor de Inglés
- **Input:** `cosmic_coach_keys.txt`, `app_en.arb`
- **Output:** `cosmic_coach_en.arb`
- **Función:** Extrae traducciones EN (archivo de referencia)
- **Duración:** ~5-10 segundos

#### Agent 4: EXTRACTOR_ES
- **Script:** `04_extractor_es.sh`
- **Rol:** Extractor de Español
- **Input:** `cosmic_coach_keys.txt`, `app_es.arb`
- **Output:** `cosmic_coach_es.arb`
- **Función:** Extrae traducciones ES
- **Duración:** ~5-10 segundos

#### Agent 5: EXTRACTOR_DE
- **Script:** `05_extractor_de.sh`
- **Rol:** Extractor de Alemán
- **Input:** `cosmic_coach_keys.txt`, `app_de.arb`
- **Output:** `cosmic_coach_de.arb`
- **Función:** Extrae traducciones DE
- **Duración:** ~5-10 segundos

#### Agent 6: EXTRACTOR_FR
- **Script:** `06_extractor_fr.sh`
- **Rol:** Extractor de Francés
- **Input:** `cosmic_coach_keys.txt`, `app_fr.arb`
- **Output:** `cosmic_coach_fr.arb`
- **Función:** Extrae traducciones FR
- **Duración:** ~5-10 segundos

#### Agent 7: EXTRACTOR_IT
- **Script:** `07_extractor_it.sh`
- **Rol:** Extractor de Italiano
- **Input:** `cosmic_coach_keys.txt`, `app_it.arb`
- **Output:** `cosmic_coach_it.arb`
- **Función:** Extrae traducciones IT
- **Duración:** ~5-10 segundos

#### Agent 8: EXTRACTOR_PT
- **Script:** `08_extractor_pt.sh`
- **Rol:** Extractor de Portugués
- **Input:** `cosmic_coach_keys.txt`, `app_pt.arb`
- **Output:** `cosmic_coach_pt.arb`
- **Función:** Extrae traducciones PT
- **Duración:** ~5-10 segundos

**Nota:** Los Agents 3-8 se ejecutan en paralelo, tiempo total ~10-15 segundos.

### Fase 3: Verificación e Integración (Secuencial)

#### Agent 9: QUALITY_CHECKER
- **Script:** `09_quality_checker.sh`
- **Rol:** Verificador de Calidad
- **Input:** `cosmic_coach_{lang}.arb` (6 archivos)
- **Output:** `quality_report.json`
- **Función:** Valida JSON, cuenta keys, verifica consistencia
- **Duración:** ~5-10 segundos

#### Agent 10: INTEGRATOR
- **Script:** `10_integrator.sh`
- **Rol:** Integrador al Proyecto
- **Input:** `cosmic_coach_{lang}.arb` (6 archivos)
- **Output:** Archivos copiados + `INTEGRATION_GUIDE.md`
- **Función:** Copia archivos e integra al proyecto
- **Duración:** ~5-10 segundos

## 📂 Estructura de Directorios

```
multiagent_scripts/
├── README.md                          # Documentación completa
├── QUICK_START.md                     # Guía de inicio rápido
├── INDEX.md                           # Este índice
├── run_all_agents.sh                  # Orquestador maestro ⭐
├── verify_system.sh                   # Verificador del sistema
├── 01_analyzer.sh                     # Agent 1: ANALYZER
├── 02_validator.sh                    # Agent 2: VALIDATOR
├── 03_extractor_en.sh                 # Agent 3: EXTRACTOR_EN
├── 04_extractor_es.sh                 # Agent 4: EXTRACTOR_ES
├── 05_extractor_de.sh                 # Agent 5: EXTRACTOR_DE
├── 06_extractor_fr.sh                 # Agent 6: EXTRACTOR_FR
├── 07_extractor_it.sh                 # Agent 7: EXTRACTOR_IT
├── 08_extractor_pt.sh                 # Agent 8: EXTRACTOR_PT
├── 09_quality_checker.sh              # Agent 9: QUALITY_CHECKER
└── 10_integrator.sh                   # Agent 10: INTEGRATOR
```

## 📊 Outputs Generados

Los scripts generan outputs en: `/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/`

```
multiagent_output/
├── cosmic_coach_keys.txt              # Lista de keys identificadas
├── translation_categories_map.json    # Mapa de categorías
├── completeness_report.json           # Reporte de completitud
├── quality_report.json                # Reporte de calidad
├── INTEGRATION_GUIDE.md               # Guía de integración
├── agent1_analyzer_report.txt         # Reporte Agent 1
├── agent2_validator_report.txt        # Reporte Agent 2
├── agent3_extractor_en_report.txt     # Reporte Agent 3
├── agent4_extractor_es_report.txt     # Reporte Agent 4
├── agent5_extractor_de_report.txt     # Reporte Agent 5
├── agent6_extractor_fr_report.txt     # Reporte Agent 6
├── agent7_extractor_it_report.txt     # Reporte Agent 7
├── agent8_extractor_pt_report.txt     # Reporte Agent 8
├── agent9_quality_checker_report.txt  # Reporte Agent 9
├── agent10_integrator_report.txt      # Reporte Agent 10
├── features/
│   └── cosmic_coach/
│       ├── cosmic_coach_en.arb        # Traducciones EN
│       ├── cosmic_coach_es.arb        # Traducciones ES
│       ├── cosmic_coach_de.arb        # Traducciones DE
│       ├── cosmic_coach_fr.arb        # Traducciones FR
│       ├── cosmic_coach_it.arb        # Traducciones IT
│       └── cosmic_coach_pt.arb        # Traducciones PT
├── logs/
│   ├── agent1_ANALYZER.log
│   ├── agent2_VALIDATOR.log
│   ├── agent3_EXTRACTOR_EN.log
│   ├── agent4_EXTRACTOR_ES.log
│   ├── agent5_EXTRACTOR_DE.log
│   ├── agent6_EXTRACTOR_FR.log
│   ├── agent7_EXTRACTOR_IT.log
│   ├── agent8_EXTRACTOR_PT.log
│   ├── agent9_QUALITY_CHECKER.log
│   └── agent10_INTEGRATOR.log
└── temp/
    └── ... (archivos temporales)
```

## 🚀 Flujos de Ejecución

### Flujo Completo (Recomendado)
```bash
# Verificar sistema
./verify_system.sh

# Ejecutar todo
./run_all_agents.sh

# Revisar resultados
cat ../multiagent_output/quality_report.json | jq '.'
```

### Flujo Manual (Por Fases)
```bash
# Fase 1: Análisis
./01_analyzer.sh
./02_validator.sh

# Fase 2: Extracción (manual uno por uno, o en background)
./03_extractor_en.sh &
./04_extractor_es.sh &
./05_extractor_de.sh &
./06_extractor_fr.sh &
./07_extractor_it.sh &
./08_extractor_pt.sh &
wait

# Fase 3: Verificación
./09_quality_checker.sh
./10_integrator.sh
```

### Flujo de Re-ejecución
```bash
# Si solo necesitas re-extraer un idioma específico
./04_extractor_es.sh

# Re-verificar calidad
./09_quality_checker.sh

# Re-integrar
./10_integrator.sh
```

## 📖 Guías de Uso

### Para Principiantes
1. Lee **QUICK_START.md** - 5 minutos para empezar
2. Ejecuta `./verify_system.sh`
3. Ejecuta `./run_all_agents.sh`
4. Sigue las instrucciones en pantalla

### Para Usuarios Avanzados
1. Lee **README.md** - Documentación completa
2. Ejecuta agentes individuales según necesites
3. Revisa logs y reportes JSON
4. Personaliza scripts según tu flujo de trabajo

### Para Debugging
1. Revisa logs en `../multiagent_output/logs/`
2. Verifica reportes JSON con `jq`
3. Ejecuta agentes individuales para aislar problemas
4. Usa `set -x` en scripts para debug detallado

## 🔧 Personalización

### Modificar Patrones de Búsqueda
Edita `01_analyzer.sh` líneas 41-52:
```bash
PATTERNS=(
  "cosmic"
  "coach"
  "goal"
  # Agrega más patrones aquí
)
```

### Cambiar Threshold de Calidad
Edita `10_integrator.sh` línea ~35:
```bash
if [ "$QUALITY_SCORE" -lt 70 ]; then  # Cambiar threshold aquí
```

### Agregar Nuevos Idiomas
1. Duplica un script extractor (ej: `04_extractor_es.sh`)
2. Cambia `LANG="es"` a tu nuevo idioma
3. Actualiza arrays de idiomas en otros scripts

## 📞 Referencias Rápidas

### Comandos Esenciales
```bash
# Verificar sistema
./verify_system.sh

# Ejecutar todo
./run_all_agents.sh

# Ver calidad
cat ../multiagent_output/quality_report.json | jq '.overall_quality_score'

# Buscar faltantes
grep -r "MISSING_TRANSLATION" ../multiagent_output/features/
```

### Archivos Importantes
- **cosmic_coach_keys.txt** - Lista de keys a extraer
- **quality_report.json** - Score de calidad y detalles
- **completeness_report.json** - Keys faltantes por idioma
- **INTEGRATION_GUIDE.md** - Guía post-ejecución

### Troubleshooting
- **jq not found:** `brew install jq`
- **Permission denied:** `chmod +x *.sh`
- **JSON invalid:** Revisar logs en `../multiagent_output/logs/`
- **Quality low:** Revisar `quality_report.json` → recommendations

## 🎯 Estado del Sistema

Para verificar el estado actual:
```bash
./verify_system.sh
```

Resultado esperado:
```
✅ 10 agentes encontrados y ejecutables
✅ 6 archivos fuente válidos
✅ Todas las dependencias instaladas
✅ Sistema listo para ejecutar
```

## 📝 Notas de Versión

- **Versión:** 1.0.0
- **Fecha:** Noviembre 2025
- **Agentes:** 10
- **Idiomas soportados:** 6 (EN, ES, DE, FR, IT, PT)
- **Features soportados:** Cosmic Coach
- **Duración estimada:** 1-2 minutos

---

**Uso Recomendado:**
1. Ejecuta `./verify_system.sh` primero
2. Lee `QUICK_START.md` si es tu primera vez
3. Ejecuta `./run_all_agents.sh`
4. Revisa `INTEGRATION_GUIDE.md` al finalizar

**Ayuda:** Consulta README.md para documentación completa.
