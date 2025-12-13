# 🐛 BUG REPORT - Testing Usuario Nov 17, 2025

**Fecha:** 17 Noviembre 2025
**Testeador:** Usuario
**Status:** 3 PROBLEMAS ENCONTRADOS

---

## ✅ LO QUE FUNCIONA BIEN

1. ✅ **Traducciones correctas** - Usuario dice: "la traducción está bastante mejor"
2. ✅ **Category labels traducen** - Ya no aparecen en inglés
3. ✅ **Alemán funciona** - "las nuevas metas si se generaron en alemán"
4. ✅ **Español funciona** - Traducciones en español correctas

---

## ❌ PROBLEMA 1: Texto Violeta Invisible en Fondo Oscuro

### Evidencia (Usuario)
> "con los violetas Este, es, no se ven en, eh, con la oscuridad que hay en el fondo. Tendrían que tener como un brillo, me parece. ¿Me explico? Esta es la lunita y él la dice, eeeeh, coso, esclaff, emotional y todo eso. Fit, tendrían que tener como un brillo abajo de los titulos, porque se pierden."

**Categorías afectadas:**
- 🌙 **sleep** (SCHLAF) - Purple (#5E35B1)
- Posiblemente otras con colores oscuros

**Problema:** Texto de color oscuro (violeta) sobre fondo oscuro → invisible

**Solución sugerida:** Usuario pide "brillo" (shadow/glow) debajo de los títulos

---

## ❌ PROBLEMA 2: Botón "Generate New Goals" Sin Traducir

### Evidencia (Usuario)
> "Generate new goals. Está en inglés, eso tendría que no estar en inglés, en alemán tampoco. El botón para generar nuevas metas"

**Ubicación:** Botón para generar nuevas metas en Cosmic Coach

**Estado actual:** Hardcodeado en inglés "Generate New Goals"

**Debería decir:**
- Español: "Generar Nuevas Metas"
- Alemán: "Neue Ziele Generieren"
- Português: "Gerar Novas Metas"
- Français: "Générer de Nouveaux Objectifs"
- Italiano: "Genera Nuovi Obiettivi"

---

## ❌ PROBLEMA 3: Cambio de Idioma NO Actualiza Goals Existentes

### Evidencia (Usuario)
> "cambié el idioma. Puse en español la app, y las apps siguen en alemán. O sea, no se cambian cuando se cambian el idioma. Tengo que generar las metas nuevamente, y ahí sí cambian el idioma."

**Flujo actual:**
1. Usuario tiene goals en alemán
2. Cambia app a español
3. Goals siguen mostrándose en alemán ❌
4. Usuario debe regenerar goals manualmente
5. Nuevos goals aparecen en español ✅

**Flujo esperado:**
1. Usuario tiene goals en alemán
2. Cambia app a español
3. Goals existentes se traducen automáticamente ✅ (sin regenerar)

**Causa probable:**
- Goals se guardan con textos hardcodeados en el idioma original
- No hay listener para cambio de idioma que re-traduzca goals existentes

---

## 📊 RESUMEN

| Problema | Severidad | Archivo afectado | Status |
|----------|-----------|------------------|--------|
| **1. Texto violeta invisible** | MEDIA | `expandable_goal_card.dart` o theme | PENDIENTE |
| **2. Botón sin traducir** | MEDIA | Cosmic Coach screen | PENDIENTE |
| **3. No auto-traduce al cambiar idioma** | ALTA | Goal persistence / state management | PENDIENTE |

---

## 🎯 PRIORIDAD DE FIXES

### 1. **ALTA PRIORIDAD** - Problema 3: Auto-traducción
**Por qué:** UX crítica - usuario no debería regenerar goals manualmente

**Solución técnica:**
- Agregar listener a cambio de idioma en provider
- Re-traducir goals existentes cuando cambia languageCode
- Actualizar state y UI automáticamente

### 2. **MEDIA PRIORIDAD** - Problema 1: Contraste texto
**Por qué:** Usabilidad - texto invisible

**Solución técnica:**
- Agregar text shadow/glow a category labels en fondo oscuro
- O cambiar color de texto a blanco con shadow oscuro
- O agregar background semi-transparente

### 3. **MEDIA PRIORIDAD** - Problema 2: Botón sin traducir
**Por qué:** Inconsistencia - resto de UI está traducido

**Solución técnica:**
- Agregar traducción a l10n/app_*.arb
- Usar AppLocalizations en botón

---

## ✅ CONFIRMACIÓN USUARIO

**Lo que funciona:**
> "la traducción está bastante mejor"
> "las nuevas metas si se generaron en alemán"

**Problemas encontrados:**
1. Violeta se pierde en fondo oscuro
2. Botón "Generate New Goals" en inglés
3. Cambio de idioma no actualiza goals existentes

---

**Generado:** 17 Noviembre 2025
**Próximo paso:** Arreglar los 3 problemas identificados
