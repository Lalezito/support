# 📋 PLAN DE TRADUCCIONES - Micro-Habits y Success Indicators

## 🎯 Objetivo

Traducir TODO el contenido restante de Cosmic Coach a los 6 idiomas (es/en/pt/fr/de/it)

---

## ✅ Lo Que YA Está Traducido

| Elemento | Estado |
|----------|--------|
| Títulos de goals | ✅ 6 idiomas |
| Descripciones principales | ✅ 6 idiomas |
| Explicaciones científicas | ✅ 6 idiomas |

---

## ❌ Lo Que FALTA Traducir

### 1. **Micro-Habits (Acciones Recomendadas)**

Actualmente en inglés:
```
"Do restorative yoga or tai chi"
"Light walk in nature (20-30 minutes)"
"Foam rolling or massage"
```

Necesitan estar en español:
```
"Haz yoga restaurativo o tai chi"
"Caminata ligera en la naturaleza (20-30 minutos)"
"Rodillo de espuma o masaje"
```

**Cantidad total**: ~45 micro-habits (3 por cada goal type, 6 goal types)

### 2. **Success Indicators (Cómo Medir el Progreso)**

Actualmente en inglés:
```
"Did gentle movement"
"Felt relaxed, not exhausted"
"Prioritized flexibility over intensity"
```

Necesitan estar en español:
```
"Hice movimiento suave"
"Me sentí relajado, no exhausto"
"Prioricé flexibilidad sobre intensidad"
```

**Cantidad total**: ~24 indicators (4 por cada goal type, 6 goal types)

### 3. **"When" y "Why" de cada micro-habit**

Actualmente en inglés:
```
when: "Today"
why: "Recovery phase is perfect for flexibility..."
```

Necesitan estar en español:
```
when: "Hoy"
why: "La fase de recuperación es perfecta para flexibilidad..."
```

### 4. **Labels de biorhythmType/Phase**

Actualmente:
```
"Sugerido por: Basado en tu ciclo physical"
```

Debería ser:
```
"Sugerido por: Basado en tu ciclo físico"
```

---

## 🔧 Enfoque de Solución

### Opción 1: Extender `biorhythm_translations.dart` (RECOMENDADO)

Agregar métodos para micro-habits y success indicators:

```dart
class BiorhythmTranslations {
  // Existing methods...

  // NEW: Micro-habits translations
  static List<Map<String, String>> physicalRecoveryMicroHabits(String lang) {
    switch (lang) {
      case 'es':
        return [
          {
            'habit': 'Haz yoga restaurativo o tai chi',
            'when': 'Hoy',
            'why': 'La fase de recuperación es perfecta para flexibilidad y balance',
          },
          // ... más habits
        ];
      // ... otros idiomas
    }
  }

  // NEW: Success indicators translations
  static List<String> physicalRecoveryIndicators(String lang) {
    switch (lang) {
      case 'es':
        return [
          'Hice movimiento suave',
          'Me sentí relajado, no exhausto',
          'Prioricé flexibilidad sobre intensidad',
          'El cuerpo se siente restaurado',
        ];
      // ... otros idiomas
    }
  }
}
```

### Opción 2: Archivo JSON de traducciones

Crear un archivo `cosmic_coach_translations.json` con todas las traducciones.

**Decisión**: Usar Opción 1 porque ya tenemos el helper `BiorhythmTranslations` funcionando.

---

## 📊 Estimación de Trabajo

| Tarea | Cantidad | Tiempo Estimado |
|-------|----------|-----------------|
| Traducir micro-habits físico (peak/critical/recovery) | 9 habits × 6 idiomas = 54 | 30 min |
| Traducir micro-habits emocional (peak/critical) | 6 habits × 6 idiomas = 36 | 20 min |
| Traducir micro-habits intelectual (peak/critical) | 6 habits × 6 idiomas = 36 | 20 min |
| Traducir success indicators (todos) | 24 indicators × 6 idiomas = 144 | 30 min |
| Traducir "when" y "why" | ~45 textos × 6 idiomas = 270 | 45 min |
| Traducir biorhythmType labels | 6 labels × 6 idiomas = 36 | 5 min |
| Modificar `biorhythm_goal_generator.dart` para usar traducciones | - | 30 min |
| Testing en los 6 idiomas | - | 20 min |
| **TOTAL** | **~600 strings** | **~3 horas** |

---

## 🚀 Plan de Ejecución

### Fase 1: Crear Métodos de Traducción (30 min)
1. Extender `biorhythm_translations.dart` con métodos para micro-habits
2. Agregar métodos para success indicators
3. Agregar métodos para "when" y "why"
4. Agregar mapa de biorhythmType/Phase labels

### Fase 2: Actualizar Generator (30 min)
1. Modificar `_physicalRecoveryGoal()` para usar traducciones
2. Modificar `_physicalPeakGoal()` para usar traducciones
3. Repetir para emotional e intellectual goals
4. Actualizar enhanced_coach_adapter.dart para label "Sugerido por..."

### Fase 3: Testing (20 min)
1. Cambiar idioma del iPhone a español → verificar
2. Cambiar a inglés → verificar
3. Cambiar a portugués → verificar
4. Spot-check francés, alemán, italiano

### Fase 4: Documentación (10 min)
1. Actualizar README con lista completa de traducciones
2. Crear guía de cómo agregar más traducciones en el futuro

---

## 💡 Decisión: ¿Hacemos TODO ahora o solo Español?

### Opción A: Solo Español (MÁS RÁPIDO - 30 min)
- Traducir solo al español los micro-habits más importantes
- Dejar inglés como fallback para otros idiomas temporalmente
- ✅ **PRO**: Resuelve tu problema inmediato
- ❌ **CON**: Los usuarios de otros idiomas verán mezcla

### Opción B: Los 6 Idiomas (COMPLETO - 3 horas)
- Traducir TODOS los micro-habits a los 6 idiomas
- App 100% localizada
- ✅ **PRO**: App production-ready
- ❌ **CON**: Toma más tiempo

---

## 🎯 Mi Recomendación

**Hacer Opción A AHORA (solo español)** para que puedas seguir probando la app esta noche.

**Hacer Opción B MAÑANA** cuando tengamos más tiempo y estés satisfecho con el funcionamiento general.

---

## 📝 Próximo Paso INMEDIATO

¿Quieres que traduzca solo al **español** ahora (30 min) para que veas TODO funcionando?

O prefieres que hagamos los **6 idiomas** completos (3 horas) de una vez?

**Dime qué prefieres y empiezo** 🚀

---

**Fecha**: Noviembre 12, 2025 - 22:35 hrs
**Estado Actual**: Goals funcionan pero con micro-habits en inglés
**Decisión Necesaria**: Español-only vs 6-idiomas
