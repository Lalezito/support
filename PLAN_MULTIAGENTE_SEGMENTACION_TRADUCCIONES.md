# 🤖 Plan Maestro Multiagente - Segmentación de Traducciones

## 🎯 Objetivo Principal

**Segmentar** las traducciones de Zodiac App de archivos monolíticos (1998 keys, 116KB) a una arquitectura modular por pantalla, empezando con **Cosmic Coach** como proyecto piloto.

**Resultado esperado:**
- ✅ Traducciones organizadas por feature/pantalla
- ✅ Carga inicial reducida 80%+
- ✅ Mantenibilidad mejorada
- ✅ Base para escalar a todas las pantallas

---

## 🧠 Contexto del Proyecto

### **Situación Actual:**
```
assets/l10n/
├── app_en.arb (1998 keys, 116 KB)
├── app_es.arb (1829 keys, 106 KB)
├── app_de.arb (1755 keys, 102 KB)
├── app_fr.arb (1700 keys, 100 KB)
├── app_it.arb (2072 keys, 118 KB)
└── app_pt.arb (2019 keys, 117 KB)

Total: ~11,373 keys, ~659 KB
```

**Problemas:**
- 🔴 Archivos gigantes (difíciles de mantener)
- 🔴 Carga inicial lenta (659 KB)
- 🔴 Keys faltantes (176-320 por idioma)
- 🔴 Inconsistencias entre idiomas
- 🔴 Merge conflicts frecuentes

### **Visión Final:**
```
assets/l10n/
├── core/
│   ├── common_{lang}.arb (botones, acciones comunes)
│   ├── errors_{lang}.arb (mensajes error)
│   └── navigation_{lang}.arb (tabs, menús)
│
├── features/
│   ├── cosmic_coach/
│   │   ├── cosmic_coach_en.arb
│   │   ├── cosmic_coach_es.arb
│   │   └── ... (6 idiomas)
│   ├── analytics/
│   ├── horoscope/
│   ├── compatibility/
│   └── premium/
│
└── content/
    ├── zodiac_signs/
    └── celebrations/
```

**Beneficios:**
- ✅ Carga inicial: 659 KB → 120 KB (82% menos)
- ✅ Lazy loading por pantalla
- ✅ Más fácil de mantener
- ✅ Menos conflicts en git

---

## 🎭 Arquitectura Multiagente

### **Principio:** División del Trabajo Especializado

Cada agente tiene:
1. **Expertise específico** (análisis, extracción, validación, etc.)
2. **Autonomía** para tomar decisiones en su dominio
3. **Salidas claras** que otros agentes pueden consumir
4. **Ejecución paralela** cuando sea posible

---

## 👥 Equipo de Agentes (10 Agentes)

### **🔵 FASE 1: ANÁLISIS Y PLANIFICACIÓN** (Secuencial)

#### **Agent 1: ANALYZER - Analista de Estructura**
**Rol:** Analizar archivos actuales e identificar categorías

**Tareas:**
1. Leer `app_en.arb` y extraer todas las keys
2. Analizar prefijos y patrones (cosmic*, goal*, analytics*, etc.)
3. Contar keys por categoría
4. Identificar dependencies entre keys
5. Generar mapa de categorías

**Input:**
- `app_en.arb`

**Output:**
- `translation_categories_map.json`
  ```json
  {
    "cosmic_coach": {
      "patterns": ["cosmic*", "goal*", "habit*", "coach*"],
      "estimated_keys": 150,
      "dependencies": ["celebration", "category"]
    },
    "analytics": {...},
    ...
  }
  ```

**Herramientas:** jq, grep, análisis de patrones

**Tiempo estimado:** 5 min

---

#### **Agent 2: VALIDATOR - Validador de Completitud**
**Rol:** Verificar que los 6 idiomas tienen estructura similar

**Tareas:**
1. Comparar keys entre EN, ES, DE, FR, IT, PT
2. Identificar keys faltantes por idioma
3. Identificar keys extras (posibles duplicados)
4. Calcular % de completitud por idioma
5. Priorizar idiomas para fix

**Input:**
- Todos los archivos `app_{lang}.arb`
- `translation_categories_map.json` del Agent 1

**Output:**
- `completeness_report.json`
  ```json
  {
    "en": {"total": 1998, "missing": 0, "extra": 0},
    "es": {"total": 1829, "missing": 176, "extra": 7},
    "priority_fixes": ["es", "de", "fr"]
  }
  ```

**Herramientas:** jq, comm, diff

**Tiempo estimado:** 3 min

---

### **🟢 FASE 2: EXTRACCIÓN COSMIC COACH** (Paralelo 6 agentes)

**Trigger:** Después de Agent 1 y 2

#### **Agent 3: EXTRACTOR_EN - Extractor Inglés**
**Rol:** Extraer keys de Cosmic Coach del archivo EN

**Tareas:**
1. Leer categorías de Cosmic Coach del mapa
2. Filtrar app_en.arb por patrones: `cosmic*`, `goal*`, `habit*`, `coach*`, `celebration*` (solo las de coach)
3. Extraer metadata (@description, @placeholders)
4. Generar `cosmic_coach_en.arb`
5. Validar sintaxis JSON
6. Verificar que no se perdieron keys

**Input:**
- `app_en.arb`
- `translation_categories_map.json`

**Output:**
- `features/cosmic_coach/cosmic_coach_en.arb` (~150 keys)
- `extraction_report_en.txt`

**Herramientas:** jq, custom script

**Tiempo estimado:** 3 min

---

#### **Agent 4: EXTRACTOR_ES - Extractor Español**
**Rol:** Extraer keys de Cosmic Coach del archivo ES

**Tareas:** (Idénticas a Agent 3 pero para ES)
1. Usar las MISMAS keys que Agent 3 extrajo
2. Si una key no existe en ES, marcarla como "MISSING"
3. Generar `cosmic_coach_es.arb`
4. Reportar keys faltantes

**Input:**
- `app_es.arb`
- Lista de keys de Agent 3 (EN)

**Output:**
- `features/cosmic_coach/cosmic_coach_es.arb`
- `missing_keys_es.txt`

**Tiempo estimado:** 3 min

---

#### **Agent 5, 6, 7, 8: EXTRACTOR_{DE,FR,IT,PT}**
**Rol:** Extractores para Alemán, Francés, Italiano, Portugués

**Tareas:** (Idénticas a Agent 4)
- Extraer mismas keys que EN
- Reportar faltantes
- Generar archivos cosmic_coach_{lang}.arb

**Ejecución:** EN PARALELO con Agent 4

**Tiempo estimado:** 3 min (paralelo)

---

### **🟡 FASE 3: VALIDACIÓN Y LIMPIEZA** (Secuencial)

#### **Agent 9: QUALITY_CHECKER - Verificador de Calidad**
**Rol:** Validar que la extracción fue correcta

**Tareas:**
1. Verificar que los 6 archivos cosmic_coach_{lang}.arb tienen estructura válida
2. Comparar número de keys entre idiomas
3. Verificar que EN tiene todas las keys base
4. Identificar inconsistencias (plurales mal formados, placeholders faltantes)
5. Verificar que las traducciones tienen sentido (no están en inglés en otros idiomas)
6. Generar reporte de calidad

**Input:**
- 6 archivos `cosmic_coach_{lang}.arb`
- `completeness_report.json`

**Output:**
- `quality_report.json`
  ```json
  {
    "status": "PASS/FAIL",
    "files_validated": 6,
    "total_keys_en": 150,
    "consistency_score": 0.91,
    "issues": [
      {"file": "cosmic_coach_es.arb", "key": "goalDetails", "issue": "MISSING"},
      ...
    ]
  }
  ```

**Herramientas:** jq, custom validation scripts

**Tiempo estimado:** 4 min

---

#### **Agent 10: INTEGRATOR - Integrador y Configurador**
**Rol:** Integrar archivos nuevos con la app y actualizar configuración

**Tareas:**
1. Crear estructura de carpetas `features/cosmic_coach/`
2. Mover archivos `cosmic_coach_{lang}.arb` a carpeta
3. Actualizar `l10n.yaml` para incluir nuevos archivos
4. Generar código de localización (`flutter gen-l10n`)
5. Verificar que compila sin errores
6. Crear PR draft con cambios
7. Generar documentación de uso

**Input:**
- 6 archivos `cosmic_coach_{lang}.arb` validados
- `quality_report.json`

**Output:**
- Estructura de carpetas creada
- `l10n.yaml` actualizado
- Código generado
- `INTEGRATION_GUIDE.md` (cómo usar en la app)
- Git branch `feature/cosmic-coach-i18n-split`

**Herramientas:** Flutter CLI, git

**Tiempo estimado:** 5 min

---

## 🔄 Flujo de Ejecución

```
FASE 1 (Secuencial):
┌─────────────┐
│  Agent 1    │  Analizar estructura → translation_categories_map.json
│  ANALYZER   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Agent 2    │  Validar completitud → completeness_report.json
│  VALIDATOR  │
└──────┬──────┘
       │
       ▼
FASE 2 (PARALELO):
┌──────┬──────┬──────┬──────┬──────┐
│ Ag3  │ Ag4  │ Ag5  │ Ag6  │ Ag7  │ Ag8
│ EN   │ ES   │ DE   │ FR   │ IT   │ PT
└──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──┬──┘
   │      │      │      │      │      │
   └──────┴──────┴──────┴──────┴──────┘
                 │
                 ▼
FASE 3 (Secuencial):
┌─────────────┐
│  Agent 9    │  Verificar calidad → quality_report.json
│  QUALITY    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Agent 10   │  Integrar → Branch listo para PR
│  INTEGRATOR │
└─────────────┘
```

**Tiempo total:** ~15-20 minutos

---

## 📋 Deliverables por Agente

| Agent | Deliverable | Tamaño | Crítico |
|-------|-------------|--------|---------|
| 1 | translation_categories_map.json | 5 KB | ✅ |
| 2 | completeness_report.json | 3 KB | ✅ |
| 3 | cosmic_coach_en.arb | 10 KB | ✅ |
| 4 | cosmic_coach_es.arb + missing_keys_es.txt | 9 KB | ✅ |
| 5-8 | cosmic_coach_{de,fr,it,pt}.arb | 9 KB c/u | ✅ |
| 9 | quality_report.json | 5 KB | ✅ |
| 10 | Branch + INTEGRATION_GUIDE.md | - | ✅ |

---

## 🎯 Criterios de Éxito

### **FASE 1:**
- [ ] Agent 1 identifica 150+ keys de Cosmic Coach
- [ ] Agent 2 confirma que ES es el idioma más completo (91.2%)

### **FASE 2:**
- [ ] 6 archivos cosmic_coach_{lang}.arb generados
- [ ] EN tiene 100% de keys (base)
- [ ] Otros idiomas tienen al menos 85% de keys
- [ ] Todos los archivos son JSON válido

### **FASE 3:**
- [ ] Quality score > 0.85
- [ ] App compila sin errores
- [ ] `flutter gen-l10n` ejecuta correctamente
- [ ] Branch creado y listo para review

---

## 🛠️ Herramientas y Scripts Necesarios

### **Para Agents 1-2: Análisis**
```bash
# analyze_structure.sh
jq -r 'keys[]' app_en.arb | \
  awk -F'_' '{print $1}' | \
  sort | uniq -c | sort -rn > key_prefixes.txt
```

### **Para Agents 3-8: Extracción**
```bash
# extract_keys.sh <pattern> <input_file> <output_file>
jq 'with_entries(select(.key | test("'$1'")))' $2 > $3
```

### **Para Agent 9: Validación**
```bash
# validate_i18n.sh
for file in cosmic_coach_*.arb; do
  jq empty $file 2>&1 && echo "$file: VALID" || echo "$file: INVALID"
done
```

### **Para Agent 10: Integración**
```yaml
# l10n.yaml update
arb-dir: assets/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
synthetic-package: false

# Additional ARB files
additional-arb-files:
  - features/cosmic_coach/cosmic_coach_en.arb
```

---

## 🚀 Ejecución del Plan

### **Opción A: Automática (Recomendada)**
```bash
./run_multiagent_split.sh --feature cosmic_coach --dry-run
./run_multiagent_split.sh --feature cosmic_coach --execute
```

**Script maestro coordina:**
1. Ejecuta Agent 1
2. Ejecuta Agent 2
3. Lanza Agents 3-8 en paralelo
4. Espera a que terminen
5. Ejecuta Agent 9
6. Ejecuta Agent 10
7. Genera reporte final

### **Opción B: Manual (Paso a Paso)**
```bash
# FASE 1
./agents/01_analyzer.sh
./agents/02_validator.sh

# FASE 2 (puede ser paralelo)
./agents/03_extractor_en.sh &
./agents/04_extractor_es.sh &
./agents/05_extractor_de.sh &
./agents/06_extractor_fr.sh &
./agents/07_extractor_it.sh &
./agents/08_extractor_pt.sh &
wait

# FASE 3
./agents/09_quality_checker.sh
./agents/10_integrator.sh
```

---

## 📈 Escalabilidad a Otras Pantallas

Una vez validado con Cosmic Coach:

### **Siguiente: Analytics Dashboard**
- Usar el mismo pipeline multiagente
- Cambiar patterns: `analytics*`, `chart*`, `stats*`
- Tiempo estimado: 15 min

### **Siguiente: Horoscope**
- Patterns: `horoscope*`, `daily*`, `weekly*`, `monthly*`
- Tiempo estimado: 20 min (más keys)

### **Siguiente: Compatibility**
- Patterns: `compatibility*`, `relationship*`
- Tiempo estimado: 15 min

**Total para 4 features principales:** ~70 min

---

## ⚠️ Consideraciones y Riesgos

### **Riesgos Identificados:**

1. **Keys compartidas entre features**
   - Ejemplo: `celebration*` usado en Coach Y Analytics
   - **Mitigación:** Agent 1 detecta dependencies, crear `shared/celebrations.arb`

2. **Keys faltantes en otros idiomas**
   - ES falta 176 keys, DE/FR faltan 320
   - **Mitigación:** Agent 4-8 reportan faltantes, decidir si:
     - Dejar como MISSING (fallback a EN)
     - Auto-traducir con API
     - Marcar para traducción manual

3. **Breaking changes en código**
   - App usa `AppLocalizations.of(context)!.goalDetails`
   - **Mitigación:** Agent 10 verifica que keys siguen accesibles

4. **Tamaño de commit**
   - Modificar 6 archivos grandes + crear 6 nuevos
   - **Mitigación:** Hacer PR pequeños, feature por feature

### **Rollback Plan:**
```bash
# Si algo falla
git checkout main
git branch -D feature/cosmic-coach-i18n-split
# Archivos originales intactos
```

---

## 🎓 Aprendizajes y Mejora Continua

Después de Cosmic Coach:

1. **Retrospectiva de Agentes:**
   - ¿Qué agente tardó más?
   - ¿Dónde hubo bloqueos?
   - ¿Qué se puede paralelizar más?

2. **Optimización de Scripts:**
   - Cachear resultados de Agent 1 (no re-analizar siempre)
   - Mejorar regex de Agent 3-8

3. **Template para Nuevas Features:**
   - Reutilizar pipeline completo
   - Solo cambiar patterns de búsqueda

---

## 📊 Métricas de Éxito

### **Técnicas:**
- [ ] Reducción de tamaño: app_en.arb de 116KB → <100KB
- [ ] Keys extraídas: 150+ para Cosmic Coach
- [ ] Tiempo de ejecución: <20 min
- [ ] Build success: 0 errores

### **Calidad:**
- [ ] Completitud EN: 100%
- [ ] Completitud ES: >90%
- [ ] Completitud DE/FR/IT/PT: >85%
- [ ] Quality score: >0.85

### **Proceso:**
- [ ] 10 agentes ejecutados correctamente
- [ ] Fase 2 ejecutada en paralelo
- [ ] Branch creado y listo para PR
- [ ] Documentación generada

---

## 🎯 Próximos Pasos

**Después de aprobar este plan:**

1. **Generar scripts de agentes** (30 min)
   - 10 scripts bash individuales
   - 1 script maestro coordinador

2. **Dry-run en copia** (10 min)
   - Ejecutar en copia de archivos
   - Verificar outputs

3. **Ejecución real** (15 min)
   - Ejecutar en archivos reales
   - Crear PR

4. **Review y testing** (30 min)
   - Code review
   - Testing en app
   - Merge si todo OK

**Tiempo total end-to-end:** ~1.5 horas

---

## ✅ Decisiones Necesarias

Antes de ejecutar, necesito tu aprobación en:

1. **¿Empezar con Cosmic Coach?** (Recomendado)
   - ✅ Sí - proyecto piloto
   - ❌ No - elegir otra feature

2. **¿Keys faltantes en ES/DE/FR?**
   - ✅ Dejarlas como MISSING (fallback a EN)
   - ❌ Auto-traducir con API
   - ❌ Traducir manualmente primero

3. **¿Generar scripts ahora?**
   - ✅ Sí - generar los 10 agentes + maestro
   - ❌ No - solo aprobar el plan

---

**Plan creado:** 13 Nov 2025
**Autor:** Claude (Sonnet 4.5)
**Estado:** Esperando aprobación
**Complejidad:** Alta (10 agentes)
**Tiempo estimado:** 15-20 min ejecución, 1.5h total con scripts
