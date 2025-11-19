# 🚀 Quick Start - Sistema Multiagente

Guía rápida para ejecutar el sistema de segmentación de traducciones en 5 minutos.

## ⚡ Inicio Rápido (3 pasos)

### 1. Verificar Sistema
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_scripts
./verify_system.sh
```

**Resultado esperado:**
- ✅ Todos los checks pasados
- ✅ 10 agentes encontrados
- ✅ Archivos fuente válidos

Si algún check falla, sigue las instrucciones en pantalla.

### 2. Ejecutar Sistema Completo
```bash
./run_all_agents.sh
```

**Duración:** ~1-2 minutos

**Qué hace:**
- Analiza archivos de traducción
- Valida completitud en 6 idiomas
- Extrae traducciones de Cosmic Coach
- Verifica calidad
- Integra al proyecto

### 3. Revisar Resultados
```bash
# Ver reporte de calidad
cat ../multiagent_output/quality_report.json | jq '.'

# Ver guía de integración
cat ../multiagent_output/INTEGRATION_GUIDE.md

# Ver archivos generados
ls -lh ../multiagent_output/features/cosmic_coach/
```

## 📋 Checklist Post-Ejecución

- [ ] ✅ Sistema ejecutado sin errores
- [ ] ✅ Quality score > 80/100
- [ ] ✅ 6 archivos .arb generados
- [ ] ✅ Revisar INTEGRATION_GUIDE.md
- [ ] ✅ Completar traducciones MISSING_TRANSLATION
- [ ] ✅ Ejecutar `flutter gen-l10n`
- [ ] ✅ Testing en los 6 idiomas

## 🔧 Comandos Útiles

### Ver Estado del Sistema
```bash
# Verificar archivos generados
ls -lh ../multiagent_output/features/cosmic_coach/

# Ver logs de ejecución
ls ../multiagent_output/logs/

# Ver reportes
ls ../multiagent_output/*.json
```

### Verificar Calidad
```bash
# Score general
cat ../multiagent_output/quality_report.json | jq '.overall_quality_score'

# Keys por idioma
cat ../multiagent_output/quality_report.json | jq '.files'

# Completitud por idioma
cat ../multiagent_output/completeness_report.json | jq '.languages'
```

### Buscar Traducciones Faltantes
```bash
# Buscar MISSING_TRANSLATION en todos los archivos
grep -r "MISSING_TRANSLATION" ../multiagent_output/features/cosmic_coach/

# Buscar en un idioma específico
grep "MISSING_TRANSLATION" ../multiagent_output/features/cosmic_coach/cosmic_coach_es.arb
```

### Re-ejecutar Agentes Específicos
```bash
# Re-ejecutar solo extractores (si completaste traducciones faltantes)
./03_extractor_en.sh
./04_extractor_es.sh
./05_extractor_de.sh
./06_extractor_fr.sh
./07_extractor_it.sh
./08_extractor_pt.sh

# Re-ejecutar verificación de calidad
./09_quality_checker.sh

# Re-ejecutar integración
./10_integrator.sh
```

## 🎯 Flujo de Trabajo Típico

### Primera Ejecución
```bash
# 1. Verificar sistema
./verify_system.sh

# 2. Ejecutar todo
./run_all_agents.sh

# 3. Revisar resultados
cat ../multiagent_output/quality_report.json | jq '.overall_quality_score'

# 4. Ver traducciones faltantes
grep -r "MISSING_TRANSLATION" ../multiagent_output/features/cosmic_coach/
```

### Completar Traducciones Faltantes
```bash
# 1. Identificar keys faltantes
cat ../multiagent_output/completeness_report.json | jq '.languages.es.missing_keys_list'

# 2. Agregar traducciones a archivos fuente
# Editar: zodiac_app/assets/l10n/app_es.arb

# 3. Re-ejecutar extractor
./04_extractor_es.sh

# 4. Verificar calidad nuevamente
./09_quality_checker.sh
```

### Integrar al Proyecto
```bash
# 1. Verificar calidad final
cat ../multiagent_output/quality_report.json | jq '.overall_quality_score'

# 2. Ejecutar integrador
./10_integrator.sh

# 3. Regenerar localizaciones Flutter
cd ../zodiac_app
flutter gen-l10n

# 4. Ejecutar tests
flutter test
```

## ⚠️ Troubleshooting Rápido

### "jq: command not found"
```bash
brew install jq
```

### "Permission denied"
```bash
chmod +x *.sh
```

### "Quality score bajo"
```bash
# Ver detalles
cat ../multiagent_output/quality_report.json | jq '.recommendations'

# Buscar problemas
grep "MISSING_TRANSLATION" ../multiagent_output/features/cosmic_coach/*.arb
```

### "JSON inválido"
```bash
# Verificar archivo específico
jq empty ../multiagent_output/features/cosmic_coach/cosmic_coach_en.arb

# Ver log del agente
cat ../multiagent_output/logs/agent3_EXTRACTOR_EN.log
```

## 📊 Interpretación de Resultados

### Quality Score
- **90-100**: ✅ Excelente - Listo para integrar
- **70-89**: ⚠️ Bueno - Revisar warnings
- **< 70**: ❌ Necesita correcciones

### Completeness Percentage
- **100%**: ✅ Todas las keys presentes
- **95-99%**: ⚠️ Faltan pocas keys
- **< 95%**: ❌ Muchas keys faltantes

### Missing Translations
- **0**: ✅ Perfecto
- **1-5**: ⚠️ Aceptable (completar después)
- **> 5**: ❌ Requiere atención

## 🎓 Próximos Pasos

1. **Revisar INTEGRATION_GUIDE.md** - Guía completa de integración
2. **Completar traducciones** - Reemplazar MISSING_TRANSLATION
3. **Regenerar l10n** - `flutter gen-l10n`
4. **Actualizar código** - Usar CosmicCoachLocalizations
5. **Testing** - Verificar en los 6 idiomas

## 📞 Ayuda

- **README completo:** `cat README.md`
- **Documentación detallada:** Ver README.md
- **Logs:** `multiagent_output/logs/`
- **Reportes:** `multiagent_output/*.json`

---

**Tip:** Ejecuta `./verify_system.sh` antes de cada ejecución para asegurar que todo esté en orden.
