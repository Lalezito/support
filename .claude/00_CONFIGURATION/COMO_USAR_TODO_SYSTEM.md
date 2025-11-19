# 🚀 Cómo Usar el Sistema de Eliminación de TODOs

## 📚 Documentos del Sistema

1. **TODO_EXECUTION_MASTER_PLAN_2025.md** - Plan detallado de todas las tareas
2. **TODO_COORDINATION_SYSTEM.json** - Configuración y tracking del sistema
3. **Este archivo** - Guía de uso rápido

---

## ⚡ Quick Start

### Para Desarrollador Humano

#### Opción 1: Ejecutar una fase completa
```
Ejecuta la FASE 1 del TODO_EXECUTION_MASTER_PLAN_2025
```

#### Opción 2: Ejecutar una tarea específica
```
Ejecuta la tarea [compatibility_user_id] del master plan
```

#### Opción 3: Ver progreso
```
¿Cuál es el progreso del master plan de TODOs?
```

---

### Para Agentes Claude Code

Cada agente puede auto-activarse con estos comandos:

#### ZODIAC_BACKEND_EXPERT_2025
```
Soy ZODIAC_BACKEND_EXPERT. Ejecuta mis tareas asignadas en TODO_EXECUTION_MASTER_PLAN_2025:
- FASE 1: [compatibility_user_id]
- FASE 2: [horoscope_backend_consolidation]
- FASE 3: [predictive_transits]
```

#### ZODIAC_BUSINESS_EXPERT_2025
```
Soy ZODIAC_BUSINESS_EXPERT. Ejecuta mis tareas asignadas en TODO_EXECUTION_MASTER_PLAN_2025:
- FASE 1: [pricing_provider]
- FASE 2: [crisis_content_final]
```

#### ZODIAC_FLUTTER_EXPERT_2025
```
Soy ZODIAC_FLUTTER_EXPERT. Ejecuta mis tareas asignadas en TODO_EXECUTION_MASTER_PLAN_2025:
- FASE 1: [notifier_real_impl]
- FASE 2: [offline_cache_finish], [notification_persistence]
- FASE 3: [smart_journal_analysis], [dynamic_cache_clear], [preferences_legacy_cleanup], [system_info_modernize]
- FASE 4: [compatibility_params]
```

#### ZODIAC_QA_EXPERT_2025
```
Soy ZODIAC_QA_EXPERT. Ejecuta mis tareas asignadas en TODO_EXECUTION_MASTER_PLAN_2025:
- FASE 4: [string_interp_cleanup], [final_fields], [deprecated_tests], [lint_imports]
```

---

## 📋 Workflow Recomendado

### Día 1: FASE 1 - Infraestructura Crítica
```bash
# Iniciar sesión con agentes
# Backend Expert ejecuta: [compatibility_user_id]
# Business Expert ejecuta: [pricing_provider]
# Flutter Expert ejecuta: [notifier_real_impl]

# Al finalizar el día
flutter analyze
flutter test
git commit -m "feat: Completada FASE 1 - Infraestructura Crítica"
```

### Día 2: FASE 2 - Backend & Contenido
```bash
# Backend Expert: [horoscope_backend_consolidation]
# Business Expert: [crisis_content_final]
# Flutter Expert: [offline_cache_finish], [notification_persistence]

# Al finalizar el día
flutter analyze
flutter test
git commit -m "feat: Completada FASE 2 - Backend & Contenido"
```

### Día 3: FASE 3 - Servicios Avanzados
```bash
# Backend Expert: [predictive_transits]
# Flutter Expert: [smart_journal_analysis], [dynamic_cache_clear],
#                 [preferences_legacy_cleanup], [system_info_modernize]

# Al finalizar el día
flutter analyze
flutter test
git commit -m "feat: Completada FASE 3 - Servicios Avanzados"
```

### Día 4: FASE 4 - Refactoring
```bash
# QA Expert: [string_interp_cleanup], [final_fields],
#            [deprecated_tests], [lint_imports]
# Flutter Expert: [compatibility_params]

# Al finalizar el día
flutter analyze  # DEBE estar 100% limpio
flutter test     # DEBE pasar 100%
git commit -m "refactor: Completada FASE 4 - Código 100% limpio"
```

---

## ✅ Checklist de Verificación

### Después de cada tarea
- [ ] Ejecutar `flutter analyze` (sin errores nuevos)
- [ ] Ejecutar `flutter test` (tests pasan)
- [ ] Verificar funcionalidad (manual testing)
- [ ] Commit atómico
- [ ] Actualizar TODO_COORDINATION_SYSTEM.json

### Después de cada fase
- [ ] Todos los tests pasan
- [ ] Flutter analyze limpio
- [ ] Features funcionan
- [ ] Documentación actualizada
- [ ] Commit de fase

### Verificación Final (después de FASE 4)
```bash
# Buscar TODOs restantes
grep -r "TODO" lib/ --exclude-dir=".dart_tool"
grep -r "FIXME" lib/ --exclude-dir=".dart_tool"
grep -r "HACK" lib/ --exclude-dir=".dart_tool"

# Resultado esperado: NINGUNO encontrado

# Análisis final
flutter analyze  # DEBE estar 100% limpio

# Tests finales
flutter test     # DEBE pasar 100%

# Build de producción
flutter build ios --release
flutter build appbundle --release
```

---

## 🔄 Actualizar Progreso

### Manualmente en JSON
```json
// En TODO_COORDINATION_SYSTEM.json
{
  "id": "1.1",
  "status": "completed",  // cambiar de "pending" a "completed"
  "completed_date": "2025-10-05",
  "actual_hours": 2.5
}
```

### Automáticamente (si implementamos script)
```bash
./update_progress.sh 1.1 completed
```

---

## 🎯 Comandos Útiles

### Ver todas las tareas pendientes
```bash
cat .claude/00_CONFIGURATION/TODO_COORDINATION_SYSTEM.json | jq '.phases[] | .tasks[] | select(.status == "pending") | {id, title, agent}'
```

### Ver carga de trabajo por agente
```bash
cat .claude/00_CONFIGURATION/TODO_COORDINATION_SYSTEM.json | jq '.agent_workload'
```

### Ver progreso general
```bash
cat .claude/00_CONFIGURATION/TODO_COORDINATION_SYSTEM.json | jq '.execution_status'
```

---

## 🚨 Manejo de Problemas

### Si una tarea falla
1. Documentar el blocker en detalle
2. Hacer rollback del commit si es necesario
3. Reportar al equipo
4. Ajustar plan si es necesario
5. Resolver blocker antes de continuar

### Si hay conflictos entre tareas
1. Revisar dependencias en el plan
2. Coordinar con otros agentes
3. Ejecutar en orden correcto
4. Comunicar cambios

### Si el plan necesita ajustes
1. Discutir con el equipo
2. Actualizar TODO_EXECUTION_MASTER_PLAN_2025.md
3. Actualizar TODO_COORDINATION_SYSTEM.json
4. Comunicar cambios a todos los agentes

---

## 📊 Dashboard de Progreso

```
═══════════════════════════════════════════════════════════
                   ZODIAC TODO ELIMINATION
                      Progress Dashboard
═══════════════════════════════════════════════════════════

FASE 1: Infraestructura Crítica        [ ] 0/3  (0%)
  1.1 compatibility_user_id            [ ] Backend Expert
  1.2 pricing_provider                 [ ] Business Expert
  1.3 notifier_real_impl               [ ] Flutter Expert

FASE 2: Backend & Contenido            [ ] 0/4  (0%)
  2.1 horoscope_backend_consolidation  [ ] Backend Expert
  2.2 offline_cache_finish             [ ] Flutter Expert
  2.3 crisis_content_final             [ ] Business Expert
  2.4 notification_persistence         [ ] Flutter Expert

FASE 3: Servicios Avanzados            [ ] 0/5  (0%)
  3.1 predictive_transits              [ ] Backend Expert
  3.2 smart_journal_analysis           [ ] Flutter Expert
  3.3 dynamic_cache_clear              [ ] Flutter Expert
  3.4 preferences_legacy_cleanup       [ ] Flutter Expert
  3.5 system_info_modernize            [ ] Flutter Expert

FASE 4: Refactoring                    [ ] 0/5  (0%)
  4.1 string_interp_cleanup            [ ] QA Expert
  4.2 final_fields                     [ ] QA Expert
  4.3 deprecated_tests                 [ ] QA Expert
  4.4 compatibility_params             [ ] Flutter Expert
  4.5 lint_imports                     [ ] QA Expert

═══════════════════════════════════════════════════════════
PROGRESO TOTAL: 0/17 (0%)
TIEMPO ESTIMADO RESTANTE: ~48 horas
OBJETIVO: ZERO TODOs, ZERO FIXMEs, ZERO HACKs
═══════════════════════════════════════════════════════════
```

---

## 🎊 Celebración Final

Cuando todo esté completo:

```bash
# Verificar victoria
grep -r "TODO\|FIXME\|HACK" lib/ --exclude-dir=".dart_tool" | wc -l

# Si el resultado es 0:
echo "🎉 ¡VICTORIA! CODEBASE 100% LIMPIO 🎉"

# Crear tag de celebración
git tag -a v1.0-zero-todos -m "🎊 ZERO TODOs Achievement - Codebase 100% limpio"
git push origin v1.0-zero-todos
```

---

**¡Éxito en la misión! 🚀**
