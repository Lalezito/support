# 📖 User Guide - Cosmic Coach Settings

**Guía completa para usuarios y desarrolladores**

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Settings Screen](#settings-screen)
3. [Conversation History](#conversation-history)
4. [Favorite Messages](#favorite-messages)
5. [Cache Management](#cache-management)
6. [FAQs](#faqs)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

El sistema **Cosmic Coach Settings** te permite personalizar tu experiencia con el coach cósmico, gestionar conversaciones pasadas y guardar mensajes importantes para consultar después.

### ¿Qué puedes hacer?

✅ Ajustar el comportamiento del coach
✅ Guardar conversaciones completas
✅ Marcar mensajes como favoritos
✅ Buscar en tu historial
✅ Exportar y compartir
✅ Gestionar el almacenamiento

---

## ⚙️ Settings Screen

### Acceso
**Ruta:** Cosmic Coach → Settings Icon (⚙️)

### Secciones Disponibles

#### 1️⃣ Behavior (Comportamiento)

##### Response Mode (Modo de Respuesta)
Controla la longitud y detalle de las respuestas del coach.

**Opciones:**
- **⚡ Quick:** Respuestas breves y directas
  - Ideal para consultas rápidas
  - 1-2 párrafos
  - Enfoque en lo esencial

- **⚖️ Balanced:** Respuestas equilibradas (Por defecto)
  - Balance entre detalle y brevedad
  - 3-4 párrafos
  - Recomendado para la mayoría

- **📄 Detailed:** Respuestas extensas y profundas
  - Análisis completo
  - 5+ párrafos
  - Para exploraciones profundas

**Ejemplo:**

```
Pregunta: "¿Cómo está mi día hoy?"

Quick Mode:
"Tu día es favorable para comunicarte.
Evita decisiones impulsivas en la tarde."

Balanced Mode:
"Las estrellas indican un día favorable para la comunicación.
Tu mercurio retrógrado sugiere precaución en decisiones importantes.
En la tarde, energía baja - descansa. En la noche, socializa."

Detailed Mode:
"Tu carta astral para hoy muestra... [análisis extenso]
Mercurio en tu casa... [explicación detallada]
Recomendaciones específicas por hora... [guía completa]"
```

---

##### Coach Personality (Personalidad del Coach)

**Opciones:**
- **😊 Friendly:** Tono cercano y amigable
  - Usa emojis frecuentemente
  - Lenguaje casual
  - "¡Hey! Te veo radiante hoy ✨"

- **💼 Professional:** Tono formal y serio
  - Vocabulario técnico
  - Sin emojis
  - "Su configuración astral indica..."

- **✨ Mystical:** Tono místico y espiritual
  - Lenguaje poético
  - Referencias cósmicas
  - "El universo conspira a tu favor..."

---

#### 2️⃣ Interface (Interfaz)

##### Quick Replies (Respuestas Rápidas)
**Toggle:** ON/OFF

**Cuando está ON:**
- Muestra sugerencias de preguntas
- Botones clickeables debajo del chat
- Acelera la conversación

**Ejemplo:**
```
[¿Amor?] [¿Carrera?] [¿Salud?]
```

##### Auto-save Conversations
**Toggle:** ON/OFF

**Cuando está ON:**
- Guarda automáticamente cada conversación
- No necesitas hacer nada manualmente
- Historial siempre actualizado

**Cuando está OFF:**
- Conversaciones no se guardan
- Modo "privado"
- Sin ocupar storage

---

#### 3️⃣ Premium Features

##### Prefer Backend AI
**Disponible:** Solo Premium ⭐
**Toggle:** ON/OFF

**Beneficios cuando está ON:**
- Usa IA avanzada en la nube
- Respuestas más personalizadas
- Acceso a modelos GPT-4
- Mayor precisión astrológica

**Free users:**
- Usa IA local optimizada
- Igualmente funcional
- Respuestas de calidad

---

##### Daily Message Limit
**Free users:** 5-50 mensajes/día (configurable)
**Premium users:** ∞ Ilimitado

**Slider:**
```
5 ──────o──────── 50
        ↑
    Tu límite
```

---

#### 4️⃣ Data Management

##### Cache Size Display
**Visualización:**
```
┌────────────────────────────────┐
│ 📁 Cache Size                  │
│ 45 conversations               │
│                                │
│ ████████░░░░░░░ 3.45 MB       │
│ Maximum: 10 MB                 │
└────────────────────────────────┘
```

**Significado:**
- **Verde (0-5 MB):** Todo bien
- **Amarillo (5-8 MB):** Considera limpiar
- **Rojo (8-10 MB):** Limpieza recomendada

---

##### Clear Cache
**Botón:** "Clear Cache"
**Acción:** Elimina TODAS las conversaciones y favoritos

**⚠️ Advertencia:**
```
Esta acción eliminará:
✓ 45 conversaciones guardadas
✓ 12 mensajes favoritos
✓ 3.45 MB de datos

Esto NO se puede deshacer.
```

**Cuándo usar:**
- Storage casi lleno
- Quieres empezar de cero
- Vas a vender/regalar el dispositivo

---

## 💬 Conversation History

### Acceso
**Ruta:** Settings → Conversation History

### Features

#### 📱 Vista Principal

```
┌────────────────────────────────────┐
│ ← Conversation History             │
├────────────────────────────────────┤
│ 🔍 [Search conversations...]       │
├────────────────────────────────────┤
│ 💼 Career advice session           │
│ 5 messages • Yesterday             │
│ "How can I improve my career..."   │
├────────────────────────────────────┤
│ ❤️ Love compatibility              │
│ 12 messages • 2 days ago           │
│ "Is my partner compatible..."      │
├────────────────────────────────────┤
│ 🌟 Daily horoscope chat            │
│ 3 messages • Nov 15                │
│ "What does today bring..."         │
└────────────────────────────────────┘
```

---

#### 🔍 Búsqueda en Tiempo Real

**Cómo funciona:**
1. Escribe en la barra de búsqueda
2. Resultados instantáneos
3. Busca en títulos Y contenido

**Ejemplo:**
```
Búsqueda: "amor"

Resultados:
✓ "Love compatibility" (título)
✓ "Career advice" (contiene "amor" en mensaje)
✓ "Daily horoscope" (contiene "amor" en respuesta)
```

---

#### 👁️ Ver Conversación

**Tap en cualquier conversación:**
```
┌────────────────────────────────────┐
│ Love compatibility            [×]  │
├────────────────────────────────────┤
│ You                                │
│ ┌────────────────────────────┐    │
│ │ Is my partner compatible?  │    │
│ └────────────────────────────┘    │
│                                    │
│             Cosmic Coach           │
│     ┌────────────────────────────┐ │
│     │ Let me analyze your...     │ │
│     │ Your signs show great...   │ │
│     └────────────────────────────┘ │
│                                    │
│ You                                │
│ ┌────────────────────────────┐    │
│ │ What about our future?     │    │
│ └────────────────────────────┘    │
├────────────────────────────────────┤
│              [Close]               │
└────────────────────────────────────┘
```

---

#### 📤 Exportar Conversación

**Swipe left → Export**

**Resultado:**
```
══════════════════════════════════════════════════
  Love compatibility
══════════════════════════════════════════════════

Created: 2025-11-16 14:30
Category: love
Messages: 12

──────────────────────────────────────────────────

[YOU] 2025-11-16 14:30
Is my partner compatible with me?

[COSMIC COACH] 2025-11-16 14:31
Let me analyze your astrological compatibility...
[respuesta completa]

[YOU] 2025-11-16 14:35
What about our future together?

[COSMIC COACH] 2025-11-16 14:36
The stars indicate...
[respuesta completa]
```

**Compartir vía:**
- WhatsApp
- Email
- SMS
- Copy to clipboard
- Share to any app

---

#### 🗑️ Eliminar Conversación

**Swipe left → Delete**

**Confirmación:**
```
⚠️ Delete Conversation?

This will permanently delete "Love compatibility"
and all its 12 messages.

This action cannot be undone.

[Cancel]  [Delete]
```

---

#### 🔄 Pull to Refresh
**Gesto:** Desliza hacia abajo desde el top
**Acción:** Recarga la lista

---

## ⭐ Favorite Messages

### Acceso
**Ruta:** Settings → Favorite Messages

### ¿Qué son los Favoritos?

Los favoritos te permiten **marcar mensajes específicos** que quieres recordar o consultar frecuentemente.

**Diferencia con Conversation History:**
- History: Conversaciones completas
- Favorites: Mensajes individuales importantes

---

### Cómo Marcar Favoritos

**En el chat:**
1. Long press en mensaje del coach
2. Tap en icono ⭐
3. ¡Listo! Mensaje guardado

**Opciones adicionales:**
- Agregar categoría
- Agregar nota personal
- Agregar tags

---

### 📱 Vista Principal

```
┌────────────────────────────────────┐
│ ← Favorite Messages      [Filter]  │
├────────────────────────────────────┤
│ 🔍 [Search favorites...]           │
├────────────────────────────────────┤
│ ❤️ LOVE COMPATIBILITY              │
│ ┌────────────────────────────────┐ │
│ │ "Your Venus aligns perfectly   │ │
│ │  with their Mars, creating..." │ │
│ │                                │ │
│ │ 💭 My note: Remember this!     │ │
│ │ 🏷️ important, relationship     │ │
│ │                                │ │
│ │ Marked: Nov 16, 14:32          │ │
│ │ [Share] [Edit Note] [Remove]   │ │
│ └────────────────────────────────┘ │
├────────────────────────────────────┤
│ 💼 CAREER                          │
│ ┌────────────────────────────────┐ │
│ │ "Jupiter in your 10th house    │ │
│ │  suggests career growth..."    │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

---

### 🏷️ Sistema de Categorías

**Categorías automáticas:**
- ❤️ Love Compatibility
- 💼 Career Advice
- 🌟 Daily Horoscope
- 🧘 Wellness
- 💰 Financial
- 👥 Relationships
- 🎯 Goals
- ✨ Other

**Cómo se asignan:**
- Automático según contexto del chat
- Puedes cambiarla manualmente
- Filtrable en la vista

---

### 🔍 Filtros Avanzados

#### Por Categoría
**Tap Filter icon → Select category**

```
All Categories ✓
─────────────────
❤️ Love (5)
💼 Career (3)
🌟 Daily (8)
🧘 Wellness (2)
```

#### Por Búsqueda
**Busca en:**
- Contenido del mensaje
- Notas personales
- Tags

**Ejemplo:**
```
Búsqueda: "venus"

Resultados:
✓ "Your Venus aligns..." (contenido)
✓ "Check Venus transit" (nota)
✓ Tagged: "venus-mars" (tag)
```

---

### 📝 Notas Personales

**Agregar nota:**
1. Tap en favorito
2. Tap "Edit Note"
3. Escribe tu nota
4. Save

**Ejemplo de uso:**
```
Mensaje original:
"Mercury retrograde ends on Nov 20"

Tu nota:
"Important! Remember to send that email
after Nov 20. Also check contract."
```

---

### 🏷️ Sistema de Tags

**Uso de tags:**
- Organización personalizada
- Búsqueda rápida
- Agrupación flexible

**Ejemplos de tags:**
```
- "important"
- "to-revisit"
- "2025-goals"
- "relationship-advice"
- "mercury-retrograde"
```

**Agregar tag:**
1. Tap en favorito
2. Tap "Add Tag"
3. Escribe tag
4. Enter

---

### 📤 Compartir Favorito

**Tap Share:**

**Output:**
```
"Your Venus aligns perfectly with their Mars,
creating a powerful attraction..."

Note: Remember this for anniversary planning!

Shared from Zodiac Life Coach
```

**Compartir vía:**
- WhatsApp
- Instagram
- Twitter/X
- Screenshot
- Copy text

---

### 🗑️ Remover Favorito

**Tap Remove:**

```
⚠️ Remove Favorite?

This will remove this message from your
favorites. You can always mark it as
favorite again later.

[Cancel]  [Remove]
```

---

## 🗄️ Cache Management

### ¿Qué es el Cache?

El cache almacena:
- Conversaciones guardadas
- Mensajes favoritos
- Configuraciones temporales

### Límites del Sistema

```
┌─────────────────────────────┐
│ Límite por Usuario          │
├─────────────────────────────┤
│ Conversaciones: 100 máximo  │
│ Favoritos: 500 máximo       │
│ Cache total: 10 MB máximo   │
└─────────────────────────────┘
```

---

### Limpieza Automática

**El sistema limpia automáticamente:**

1️⃣ **Cuando cache > 10 MB:**
   - Elimina conversaciones > 90 días

2️⃣ **Si aún excede:**
   - Elimina conversaciones > 60 días

3️⃣ **Si aún excede:**
   - Elimina conversaciones > 30 días

**Favoritos:**
- NUNCA se eliminan automáticamente
- Solo limpieza manual

---

### Limpieza Manual

**Settings → Clear Cache:**

**Opciones:**
```
┌────────────────────────────┐
│ Clear All Cache            │
│ Delete everything          │
├────────────────────────────┤
│ Clear Old Conversations    │
│ Keep last 30 days          │
├────────────────────────────┤
│ Clear Favorites Only       │
│ Keep conversations         │
└────────────────────────────┘
```

---

## ❓ FAQs

### General

**Q: ¿Los datos se sincronizan entre dispositivos?**
A: No. Los datos son locales por dispositivo.

**Q: ¿Puedo recuperar datos eliminados?**
A: No. La eliminación es permanente.

**Q: ¿Los datos están encriptados?**
A: Sí, SharedPreferences usa encriptación del OS.

---

### Conversaciones

**Q: ¿Cuántas conversaciones puedo guardar?**
A: Máximo 100 por usuario.

**Q: ¿Qué pasa si llego al límite?**
A: Se eliminan las más antiguas automáticamente.

**Q: ¿Puedo editar una conversación guardada?**
A: No. Son read-only para mantener integridad.

---

### Favoritos

**Q: ¿Cuántos favoritos puedo tener?**
A: Máximo 500 por usuario.

**Q: ¿Puedo mover un favorito a otra categoría?**
A: Sí. Tap en favorito → Edit → Change category.

**Q: ¿Las notas tienen límite de caracteres?**
A: No hay límite específico (razonable).

---

### Performance

**Q: ¿Afecta el performance tener muchos datos?**
A: No. El cache en memoria optimiza el acceso.

**Q: ¿Cuánto storage ocupa típicamente?**
A: Promedio: 2-5 MB. Máximo: 10 MB.

**Q: ¿Debo limpiar el cache regularmente?**
A: No necesario. El sistema auto-optimiza.

---

## 🔧 Troubleshooting

### Problema: No se guardan las conversaciones

**Soluciones:**
1. ✅ Verifica que Auto-save esté ON
2. ✅ Revisa storage disponible en dispositivo
3. ✅ Reinstala la app (último recurso)

---

### Problema: No encuentro una conversación guardada

**Soluciones:**
1. ✅ Usa la búsqueda
2. ✅ Pull to refresh
3. ✅ Verifica que no se haya auto-eliminado (>90 días)

---

### Problema: Favoritos desaparecen

**Causas posibles:**
1. ❌ Limpiaste el cache
2. ❌ Reinstalaste la app
3. ❌ Cambiaste de usuario

**Prevención:**
- Exporta favoritos regularmente
- No uses Clear All Cache a menos que sea necesario

---

### Problema: Cache lleno constantemente

**Soluciones:**
1. ✅ Exporta conversaciones importantes
2. ✅ Limpia conversaciones antiguas manualmente
3. ✅ Reduce Daily Message Limit
4. ✅ Desactiva Auto-save para chats casuales

---

### Problema: Búsqueda no encuentra nada

**Soluciones:**
1. ✅ Verifica ortografía
2. ✅ Busca palabras más genéricas
3. ✅ Intenta buscar por categoría
4. ✅ Pull to refresh

---

### Problema: App lenta con muchos datos

**Soluciones:**
1. ✅ Clear Cache (libera RAM)
2. ✅ Reinicia la app
3. ✅ Actualiza a la última versión
4. ✅ Reduce a <50 conversaciones

---

## 📞 Soporte

**¿Necesitas más ayuda?**

- 📧 Email: support@zodiaclifecoach.com
- 💬 In-app chat support
- 📚 [Documentación completa](./COSMIC_COACH_SETTINGS_ARCHITECTURE.md)
- 🚀 [Quick Start Guide](./QUICK_START_COSMIC_COACH_SETTINGS.md)

---

**Guía creada por:** Agente 7 - Documentation Specialist
**Versión:** 1.0.0
**Última actualización:** 18 Noviembre 2025
