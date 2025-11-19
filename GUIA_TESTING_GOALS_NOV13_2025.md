# 🧪 GUÍA DE TESTING - Goals Fix Completo

**Fecha**: 13 de Noviembre, 2025
**Build**: Corriendo en iPhone (00008150-0015244A2288401C)
**Log**: `/tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log`

---

## ✅ FIXES IMPLEMENTADOS

### Fix 1: Sistema de Versiones (Schema Migration)
**Problema**: Goals viejos con texto genérico se cargaban desde storage
**Solución**: Sistema automático que detecta versión 1 y limpia para regenerar con versión 2 (biorhythms)

### Fix 2: Persistencia Correcta
**Problema**: Goals se regeneraban aleatoriamente cada sesión
**Solución**: Carga goals guardados PRIMERO, solo genera nuevos si está vacío

### Fix 3: Goals Completados
**Problema**: Goals completados permanecían en lista activa
**Solución**: Remueve goals de lista al completarse (ya están en historial)

### Fix 4: Prevención (Documentación)
**Problema**: Código podía cambiarse de `generateCompleteGoalSet` a `generateBiorhythmGoals`
**Solución**: Comentarios grandes + documento [CRITICAL_DO_NOT_CHANGE_NOV13.md](CRITICAL_DO_NOT_CHANGE_NOV13.md)

---

## 🎯 QUÉ TESTEAR

### TEST 1: Migración Automática de Goals Viejos

**Escenario**: Tienes goals viejos guardados de versión 1

**Pasos**:
1. Abre la app en tu iPhone
2. Ve a Cosmic Coach
3. **OBSERVA** qué goals ves

**Resultado Esperado** ✅:
- Sistema detecta goals viejos (versión 1)
- Los limpia automáticamente
- Genera goals NUEVOS con `generateCompleteGoalSet`
- Debes ver **5-7 goals variados**:
  - Goals de contexto (sueño, emoción, energía)
  - Goals de zodiac (shadow work, poderes)
  - Micro-hábitos
  - Goals de biorritmos (físico, emocional, intelectual)

**Resultado INCORRECTO** ❌:
- Ves "Acción hacia tus metas" (texto genérico)
- Solo 1-2 goals
- Goals NO relacionados con biorritmos

**Logs a Verificar**:
```bash
tail -50 /tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log | grep "version"
```

Debes ver:
```
🔄 Old goals version detected (1 < 2) - clearing for regeneration with biorhythms
📭 No saved goals found - generating new goals
✅ Generated X NEW goals
```

---

### TEST 2: Persistencia de Goals y Progreso

**Escenario**: Goals mantienen progreso entre sesiones

**Pasos**:
1. Ve a Cosmic Coach
2. Selecciona un goal
3. Marca uno de los success indicators (progreso → 33%, 50%, o 66%)
4. **SAL de Cosmic Coach** (vuelve al home)
5. **VUELVE a entrar a Cosmic Coach**

**Resultado Esperado** ✅:
- El MISMO goal está presente
- El progreso se mantiene (33%, 50%, o 66%)
- NO se regeneraron goals nuevos
- La lista es IDÉNTICA

**Resultado INCORRECTO** ❌:
- Goals diferentes
- Progreso en 0%
- Número de goals cambió

---

### TEST 3: Persistencia Tras Cerrar App Completa

**Escenario**: Goals persisten incluso tras cerrar app

**Pasos**:
1. Con el goal al 66%, **CIERRA LA APP** completamente (swipe up)
2. **ABRE LA APP** de nuevo
3. Ve a Cosmic Coach

**Resultado Esperado** ✅:
- Los MISMOS goals están presentes
- El progreso sigue al 66%
- NO hay regeneración

---

### TEST 4: Completar Goal y Verificar Eliminación

**Escenario**: Goals completados desaparecen de lista activa

**Pasos**:
1. Selecciona un goal que tenía progreso
2. Marca TODOS los success indicators (progreso → 100%)
3. Goal se marca como completado
4. **VUELVE a la lista de goals**

**Resultado Esperado** ✅:
- Goal desapareció de la lista activa
- Quedan N-1 goals activos
- Goal está en historial (puedes verificar en stats)

**Resultado INCORRECTO** ❌:
- Goal completado sigue en lista
- Puedes completarlo múltiples veces

---

### TEST 5: Goal Completado No Reaparece

**Escenario**: Goals completados NO vuelven a aparecer

**Pasos**:
1. Tras completar un goal (TEST 4)
2. **SAL y VUELVE** a Cosmic Coach
3. **CIERRA y ABRE** la app
4. Ve a Cosmic Coach otra vez

**Resultado Esperado** ✅:
- Goal completado NO reaparece
- Siguen los N-1 goals activos
- Lista se mantiene consistente

**Resultado INCORRECTO** ❌:
- Goal completado vuelve a aparecer
- Goal está en 0% otra vez

---

### TEST 6: Verificar Tipos de Goals (Variedad)

**Escenario**: Goals generados incluyen TODOS los tipos

**Pasos**:
1. Observa los goals en tu lista
2. Lee los títulos y descripciones

**Resultado Esperado** ✅:
Debes ver VARIEDAD de tipos:

**Ejemplo en Español**:
- "Recupera tu energía física" (contexto: sueño)
- "Maneja tu estrés diario" (contexto: emoción)
- "Desarrolla tu poder de liderazgo" (zodiac: Aries)
- "5 minutos de meditación" (micro-hábito)
- "Camina 10 minutos al día" (micro-hábito)
- "Día Físico Crítico - descansa" (biorritmo físico)
- "Pico Emocional - conéctate" (biorritmo emocional)

**Ejemplo en Inglés**:
- "Recover your physical energy" (context: sleep)
- "Manage your daily stress" (context: emotion)
- "Develop your leadership power" (zodiac: Aries)
- "5 minutes of meditation" (micro-habit)
- "Walk 10 minutes daily" (micro-habit)
- "Physical Critical Day - rest" (biorhythm)
- "Emotional Peak - connect" (biorhythm)

**Resultado INCORRECTO** ❌:
- Solo goals genéricos: "Acción hacia tus metas"
- Solo 1-2 goals de biorritmos
- Todos los goals son iguales

---

### TEST 7: Verificar Traducciones (Multi-idioma)

**Escenario**: Goals muestran traducciones correctas según idioma

**Pasos**:
1. Cambia el idioma de la app (Settings)
2. Ve a Cosmic Coach
3. Observa los goals

**Resultado Esperado** ✅:
- Goals traducidos al idioma seleccionado
- Español: "Tu sabiduría de Tauro sabe..."
- Portugués: "Sua sabedoria de Touro sabe..."
- Francés: "Votre sagesse Taureau sait..."
- Alemán: "Deine Stier-Weisheit weiß..."
- Italiano: "La tua saggezza Toro sa..."

**Resultado INCORRECTO** ❌:
- Textos en inglés cuando app está en español
- Mezcla de idiomas

---

## 📊 CHECKLIST COMPLETO

Marca cada test al completarlo:

- [ ] **TEST 1**: Migración automática (goals viejos → goals nuevos)
- [ ] **TEST 2**: Persistencia (sal y vuelve → mismo progreso)
- [ ] **TEST 3**: Persistencia tras cerrar app (cierra → abre → mismo progreso)
- [ ] **TEST 4**: Goal completado desaparece de lista
- [ ] **TEST 5**: Goal completado NO reaparece
- [ ] **TEST 6**: Variedad de goals (5-7 tipos diferentes)
- [ ] **TEST 7**: Traducciones correctas en múltiples idiomas

---

## 🐛 SI ENCUENTRAS PROBLEMAS

### Problema: Sigues viendo "Acción hacia tus metas"

**Causa Posible**: Goals viejos no se limpiaron

**Debug**:
```bash
# Ver logs de versión
tail -100 /tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log | grep -A 5 "version"
```

**Solución**:
1. Desinstala la app del iPhone
2. Reinstala desde Xcode
3. Abre Cosmic Coach
4. Debería generar goals frescos

---

### Problema: Goals NO persisten (siguen regenerándose)

**Causa Posible**: Problema con SharedPreferences

**Debug**:
```bash
# Ver logs de guardado/carga
tail -100 /tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log | grep -E "Saved|Loaded"
```

Debes ver:
```
💾 Saved 7 goals (version 2)
📥 Loaded 7 goals from storage (version 2)
```

**Solución**: Avísame y revisamos el código de persistencia

---

### Problema: Goals completados siguen apareciendo

**Causa Posible**: Fix de completados no se aplicó correctamente

**Debug**:
```bash
# Ver logs de completar goals
tail -100 /tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log | grep "completed"
```

Debes ver:
```
✅ Goal completed and removed from current list: [título del goal]
```

**Solución**: Avísame y verificamos el provider

---

## 📝 REPORTAR RESULTADOS

Cuando termines de testear, repórtame:

1. **Qué tests pasaron** ✅
2. **Qué tests fallaron** ❌
3. **Screenshots** si hay comportamiento inesperado
4. **Logs relevantes** si encuentras errores

**Comando para extraer logs completos**:
```bash
cat /tmp/flutter_GOALS_VERSION_SYSTEM_nov13.log | grep -E "version|goals|Loaded|Saved|completed"
```

---

## 🎯 RESUMEN

**Lo que debe funcionar ahora**:
1. ✅ Goals variados (5-7 tipos diferentes)
2. ✅ Goals persisten entre sesiones
3. ✅ Progreso se mantiene
4. ✅ Goals completados desaparecen
5. ✅ Goals completados NO reaparecen
6. ✅ Migración automática de goals viejos
7. ✅ Traducciones correctas en 6 idiomas

**Lo que NO debe pasar**:
1. ❌ Goals genéricos "Acción hacia tus metas"
2. ❌ Solo 1-2 goals de biorritmos
3. ❌ Goals diferentes cada sesión
4. ❌ Progreso que desaparece
5. ❌ Goals completados que reaparecen

---

**App está corriendo en tu iPhone ahora mismo.**

**Puedes empezar a testear inmediatamente.**

**¡Avísame qué encuentras!** 🚀
