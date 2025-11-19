# 🎯 PLAN MAESTRO: COSMIC COACH SETTINGS + MEJORAS
## Implementación Multiagente + Multiidioma (6 idiomas)
**Fecha:** 18 Noviembre 2025

---

## 📊 OVERVIEW DEL PROYECTO

### Objetivos
1. ✅ Implementar sistema completo de settings para Cosmic Coach
2. ✅ Agregar 15+ nuevas funcionalidades avanzadas
3. ✅ Soporte completo en 6 idiomas (ES, EN, DE, FR, IT, PT)
4. ✅ Optimizaciones de performance y cache
5. ✅ Features premium exclusivos

### Métricas de Éxito
- 🎯 Settings funcionales en todos los idiomas
- ⚡ Reducción 30% en uso de memoria (lazy loading)
- 💾 Sistema de cache optimizado (compresión)
- 📱 UI/UX premium y responsive
- 🚀 0 errores de compilación

---

## 🤖 DISTRIBUCIÓN DE AGENTES

### **AGENTE 1: Backend & Core Logic Specialist** 🔧
**Responsabilidad:** Servicios, lógica de negocio, persistencia

**Tareas:**
1. Extender `PreferencesService` con nuevos settings:
   ```dart
   // Nuevos getters/setters:
   - chatMode: 'quick' | 'balanced' | 'detailed'
   - coachPersonality: 'professional' | 'friendly' | 'mystical'
   - showQuickReplies: bool
   - autoSaveConversations: bool
   - preferBackend: bool (premium)
   - dailyMessageLimit: int (premium)
   ```

2. Crear `ConversationHistoryService`:
   ```dart
   - Future<List<ConversationHistory>> getHistory()
   - Future<void> saveConversation(String title)
   - Future<void> loadConversation(String id)
   - Future<void> deleteConversation(String id)
   - Future<void> exportConversation(String id, ExportFormat)
   ```

3. Crear `ChatCacheService`:
   ```dart
   - Future<int> calculateCacheSize()
   - Future<void> clearCache()
   - Future<void> compressCache()
   - Future<Map<String, dynamic>> getCacheStats()
   ```

4. Mejorar `HoroscopeChatService`:
   ```dart
   - Implementar lazy loading de templates por idioma
   - Agregar modo 'quick' (100% local)
   - Agregar modo 'detailed' (50/50 backend/local)
   - Sistema de favoritos de mensajes
   ```

**Archivos a crear/modificar:**
- `lib/services/preferences_service.dart` (modificar)
- `lib/services/conversation_history_service.dart` (nuevo)
- `lib/services/chat_cache_service.dart` (nuevo)
- `lib/services/horoscope_chat_service.dart` (modificar)
- `lib/models/conversation_history.dart` (nuevo)

**Estimado:** 3-4 horas

---

### **AGENTE 2: UI/UX Specialist** 🎨
**Responsabilidad:** Pantallas, widgets, navegación

**Tareas:**
1. Crear `CosmicCoachSettingsScreen`:
   - Secciones: Behavior, Interface, Premium, Data Management
   - Componentes: DropdownButton, SegmentedButton, Switches, Sliders
   - Dark mode compatible
   - Responsive design

2. Crear `ConversationHistoryScreen`:
   - Lista de conversaciones guardadas
   - Preview de mensajes
   - Actions: View, Delete, Export
   - Empty state elegante

3. Crear `FavoriteMessagesScreen`:
   - Lista de mensajes favoritos
   - Categorías (Daily, Love, Career, etc.)
   - Actions: Unfavorite, Share, Copy

4. Modificar `CosmicCoachChatScreen`:
   - Agregar menú mejorado con nuevas opciones
   - Botón de favorito en cada mensaje
   - Indicador de modo offline
   - Banner de premium features

5. Crear widgets reutilizables:
   - `SettingSectionHeader`
   - `SettingCard`
   - `PremiumFeatureBadge`
   - `ConversationListTile`
   - `FavoriteMessageCard`

**Archivos a crear/modificar:**
- `lib/screens/cosmic_coach_settings_screen.dart` (nuevo)
- `lib/screens/conversation_history_screen.dart` (nuevo)
- `lib/screens/favorite_messages_screen.dart` (nuevo)
- `lib/screens/cosmic_coach_chat_screen.dart` (modificar)
- `lib/widgets/settings/setting_section_header.dart` (nuevo)
- `lib/widgets/settings/setting_card.dart` (nuevo)
- `lib/widgets/settings/premium_feature_badge.dart` (nuevo)
- `lib/widgets/chat/conversation_list_tile.dart` (nuevo)
- `lib/widgets/chat/favorite_message_card.dart` (nuevo)

**Estimado:** 4-5 horas

---

### **AGENTE 3: Translations Master (Español)** 🇪🇸
**Responsabilidad:** Traducciones al español

**Tareas:**
1. Agregar nuevas keys a `app_es.arb`:
   - Settings screen (30+ strings)
   - Conversation history (15+ strings)
   - Favorites (10+ strings)
   - Error messages (5+ strings)
   - Success messages (5+ strings)

2. Validar consistencia con strings existentes
3. Verificar género y formalidad adecuados
4. Review de UX en español

**Archivo:** `assets/l10n/app_es.arb`

**Keys a agregar (ejemplo):**
```json
{
  "chatSettings": "Configuración del Chat",
  "behavior": "Comportamiento",
  "responseMode": "Modo de Respuesta",
  "responseModeDescription": "Elige cómo responde el coach",
  "quickMode": "Rápido (100% local)",
  "balancedMode": "Balanceado (IA + local)",
  "detailedMode": "Detallado (Más IA)",
  "coachPersonality": "Personalidad del Coach",
  "coachPersonalityDescription": "Ajusta el tono de las respuestas",
  "professional": "Profesional",
  "friendly": "Amigable",
  "mystical": "Místico",
  "interface": "Interfaz",
  "showQuickReplies": "Mostrar Respuestas Rápidas",
  "showQuickRepliesDescription": "Mostrar preguntas sugeridas",
  "autoSaveConversations": "Auto-guardar Conversaciones",
  "autoSaveDescription": "Guardar automáticamente el historial del chat",
  "preferBackendAI": "Preferir Respuestas IA",
  "preferBackendDescription": "Usar más IA para respuestas complejas",
  "dailyMessageLimit": "Límite Diario de Mensajes",
  "dailyMessageLimitDescription": "Máximo de mensajes por día",
  "dataManagement": "Gestión de Datos",
  "cacheSize": "Tamaño del Caché",
  "calculating": "Calculando...",
  "totalConversations": "Conversaciones Guardadas",
  "conversationHistory": "Historial de Conversaciones",
  "favoriteMessages": "Mensajes Favoritos",
  "exportConversation": "Exportar Conversación",
  "clearCache": "Limpiar Caché",
  "cacheCleared": "Caché limpiado exitosamente",
  "conversationSaved": "Conversación guardada",
  "conversationDeleted": "Conversación eliminada",
  "messageAddedToFavorites": "Mensaje agregado a favoritos",
  "messageRemovedFromFavorites": "Mensaje eliminado de favoritos",
  "exportedSuccessfully": "Exportado exitosamente",
  "noConversationsYet": "No hay conversaciones guardadas aún",
  "noFavoritesYet": "No tienes mensajes favoritos aún",
  "startChatting": "Comienza a chatear con tu coach cósmico",
  "tapToSave": "Toca para guardar una conversación",
  "tapStarToFavorite": "Toca la estrella para marcar como favorito",
  "offlineMode": "Modo Sin Conexión",
  "offlineModeDescription": "Usando solo respuestas locales",
  "backOnline": "Conexión restaurada",
  "conversationTitle": "Título de la Conversación",
  "enterTitle": "Ingresa un título...",
  "cancel": "Cancelar",
  "save": "Guardar",
  "delete": "Eliminar",
  "export": "Exportar",
  "share": "Compartir",
  "copy": "Copiar",
  "confirmDelete": "¿Confirmar Eliminación?",
  "confirmDeleteConversation": "¿Estás seguro de que quieres eliminar esta conversación?",
  "confirmDeleteMessage": "Esta acción no se puede deshacer",
  "premiumFeature": "Función Premium",
  "upgradeToUnlock": "Actualiza para desbloquear",
  "unlimitedMessages": "Mensajes Ilimitados",
  "advancedAI": "IA Avanzada",
  "conversationExport": "Exportar Conversaciones",
  "priorityResponses": "Respuestas Prioritarias"
}
```

**Estimado:** 2 horas

---

### **AGENTE 4: Translations Master (English)** 🇺🇸
**Responsabilidad:** Traducciones al inglés

**Tareas:**
1. Traducir todas las keys de español a inglés
2. Validar tono profesional y natural
3. Verificar consistencia con terminología existente
4. Review de UX en inglés

**Archivo:** `assets/l10n/app_en.arb`

**Estimado:** 2 horas

---

### **AGENTE 5: Translations Master (Deutsch, Français, Italiano, Português)** 🌍
**Responsabilidad:** Traducciones a alemán, francés, italiano y portugués

**Tareas:**
1. Traducir todas las keys a los 4 idiomas
2. Validar con nativos si es posible
3. Verificar formalidad y género
4. Usar traducciones existentes como referencia

**Archivos:**
- `assets/l10n/app_de.arb`
- `assets/l10n/app_fr.arb`
- `assets/l10n/app_it.arb`
- `assets/l10n/app_pt.arb`

**Estimado:** 3-4 horas

---

### **AGENTE 6: Integration & Testing Specialist** ✅
**Responsabilidad:** Integración, testing, validación

**Tareas:**
1. Integrar todos los componentes
2. Verificar navegación entre pantallas
3. Testing de cada feature:
   - ✅ Settings se guardan correctamente
   - ✅ Conversaciones se guardan/cargan
   - ✅ Favoritos funcionan
   - ✅ Cache se calcula/limpia
   - ✅ Export funciona
   - ✅ Todos los idiomas muestran textos correctos

4. Testing de edge cases:
   - Sin conexión
   - Sin premium
   - Cache vacío
   - Historial vacío
   - Cambio de idioma con datos existentes

5. Performance testing:
   - Lazy loading efectivo
   - Compresión de cache
   - Paginación del historial

6. Crear documento de testing:
   - Checklist de funcionalidades
   - Screenshots de cada pantalla
   - Bugs encontrados y resueltos

**Archivos a crear:**
- `TESTING_REPORT_COSMIC_COACH_SETTINGS.md`
- `SCREENSHOTS_COSMIC_COACH_SETTINGS/` (carpeta)

**Estimado:** 2-3 horas

---

### **AGENTE 7: Documentation & Polish Specialist** 📚
**Responsabilidad:** Documentación, código limpio, comentarios

**Tareas:**
1. Agregar comentarios JSDoc a todos los métodos nuevos
2. Crear README para cada nuevo servicio
3. Documentar arquitectura del sistema de settings
4. Crear guía de usuario (cómo usar settings)
5. Limpiar código:
   - Remover TODOs obsoletos
   - Formatear con `dart format`
   - Verificar imports no usados
   - Optimizar imports

6. Crear changelog detallado

**Archivos a crear:**
- `COSMIC_COACH_SETTINGS_ARCHITECTURE.md`
- `USER_GUIDE_COSMIC_COACH_SETTINGS.md`
- `CHANGELOG_NOV18_2025.md`

**Estimado:** 2 horas

---

## 📋 ESTRUCTURA DE ARCHIVOS COMPLETA

```
zodiac_app/
├── lib/
│   ├── screens/
│   │   ├── cosmic_coach_chat_screen.dart (modificar)
│   │   ├── cosmic_coach_settings_screen.dart (nuevo) ← AGENTE 2
│   │   ├── conversation_history_screen.dart (nuevo) ← AGENTE 2
│   │   └── favorite_messages_screen.dart (nuevo) ← AGENTE 2
│   ├── services/
│   │   ├── preferences_service.dart (modificar) ← AGENTE 1
│   │   ├── horoscope_chat_service.dart (modificar) ← AGENTE 1
│   │   ├── conversation_history_service.dart (nuevo) ← AGENTE 1
│   │   └── chat_cache_service.dart (nuevo) ← AGENTE 1
│   ├── models/
│   │   ├── conversation_history.dart (nuevo) ← AGENTE 1
│   │   └── favorite_message.dart (nuevo) ← AGENTE 1
│   └── widgets/
│       ├── settings/
│       │   ├── setting_section_header.dart (nuevo) ← AGENTE 2
│       │   ├── setting_card.dart (nuevo) ← AGENTE 2
│       │   └── premium_feature_badge.dart (nuevo) ← AGENTE 2
│       └── chat/
│           ├── conversation_list_tile.dart (nuevo) ← AGENTE 2
│           └── favorite_message_card.dart (nuevo) ← AGENTE 2
├── assets/l10n/
│   ├── app_es.arb (modificar) ← AGENTE 3
│   ├── app_en.arb (modificar) ← AGENTE 4
│   ├── app_de.arb (modificar) ← AGENTE 5
│   ├── app_fr.arb (modificar) ← AGENTE 5
│   ├── app_it.arb (modificar) ← AGENTE 5
│   └── app_pt.arb (modificar) ← AGENTE 5
└── docs/
    ├── COSMIC_COACH_SETTINGS_ARCHITECTURE.md (nuevo) ← AGENTE 7
    ├── USER_GUIDE_COSMIC_COACH_SETTINGS.md (nuevo) ← AGENTE 7
    ├── TESTING_REPORT_COSMIC_COACH_SETTINGS.md (nuevo) ← AGENTE 6
    └── CHANGELOG_NOV18_2025.md (nuevo) ← AGENTE 7
```

---

## 🚀 PLAN DE EJECUCIÓN MULTIAGENTE

### **FASE 1: PREPARACIÓN (30 min)**
**Objetivo:** Setup y definición de contratos

**Tareas secuenciales:**
1. ✅ Crear este plan maestro
2. ✅ Definir modelos de datos (`ConversationHistory`, `FavoriteMessage`)
3. ✅ Definir interfaces de servicios (method signatures)
4. ✅ Crear estructura de carpetas

**Output:**
- Contratos claros para cada agente
- Modelos definidos
- No hay dependencias bloqueantes

---

### **FASE 2: DESARROLLO PARALELO (4-6 horas)**
**Objetivo:** Todos los agentes trabajan simultáneamente

**Grupos paralelos:**

**🔵 Grupo A - Backend (AGENTE 1)**
- Tiempo: 3-4 horas
- Sin dependencias de otros agentes
- Output: Servicios funcionando con tests básicos

**🟢 Grupo B - Frontend (AGENTE 2)**
- Tiempo: 4-5 horas
- Puede usar mocks de servicios temporalmente
- Output: UI completa y navegable

**🟡 Grupo C - Traducciones (AGENTES 3, 4, 5)**
- Tiempo: 2-4 horas (paralelo entre idiomas)
- Sin dependencias
- Output: Todos los `.arb` actualizados

**Sincronización intermedia (a las 2 horas):**
- Quick check de progreso
- Resolver bloqueos
- Ajustar si es necesario

---

### **FASE 3: INTEGRACIÓN (2-3 horas)**
**Objetivo:** Unir todo y hacerlo funcionar

**Tareas secuenciales:**

1. **AGENTE 6 toma el control**
2. Conectar UI con servicios reales
3. Probar cada flujo completo:
   - Open settings → Change mode → Save → Verify
   - Save conversation → View history → Delete
   - Mark favorite → View favorites → Remove
   - Clear cache → Verify
   - Export conversation → Verify file

4. Testing multiidioma:
   - Cambiar idioma en cada pantalla
   - Verificar que todo se traduce
   - Verificar acentos y caracteres especiales

5. Fix bugs encontrados

---

### **FASE 4: POLISH & DOCUMENTATION (2 horas)**
**Objetivo:** Código limpio y documentado

**AGENTE 7 toma el control:**
1. Code cleanup
2. Agregar comentarios
3. Crear documentación
4. Screenshots
5. Changelog

---

### **FASE 5: VALIDACIÓN FINAL (1 hora)**
**Objetivo:** Todo funciona perfectamente

**Checklist final:**
- ✅ Flutter analyze: 0 errores
- ✅ Compilación release: OK
- ✅ Todos los idiomas: OK
- ✅ Dark mode: OK
- ✅ Premium features: OK
- ✅ Performance: Optimizado
- ✅ Documentación: Completa

---

## 📊 TIMELINE ESTIMADO

```
Total: 10-13 horas de trabajo multiagente
       (2-3 días calendario trabajando en paralelo)

Desglose:
├─ Fase 1: Preparación          → 0.5h
├─ Fase 2: Desarrollo Paralelo  → 4-6h (paralelo, real: 6h máximo)
├─ Fase 3: Integración          → 2-3h
├─ Fase 4: Polish & Docs        → 2h
└─ Fase 5: Validación Final     → 1h

TOTAL CALENDARIO: ~12 horas (1.5 días intensivos)
```

---

## 🎯 CRITERIOS DE ACEPTACIÓN

### Must-Have (Crítico)
- ✅ Settings screen funcional en 6 idiomas
- ✅ Historial de conversaciones funcional
- ✅ Sistema de favoritos funcional
- ✅ Cache management funcional
- ✅ Modo offline indicator
- ✅ Premium features bloqueados correctamente
- ✅ 0 crashes, 0 errores de compilación
- ✅ Dark mode OK en todas las pantallas

### Should-Have (Importante)
- ✅ Export conversations
- ✅ Lazy loading de templates
- ✅ Cache compression
- ✅ Paginación de historial
- ✅ Personalidad del coach ajustable

### Nice-to-Have (Opcional)
- 🔄 Analytics de uso de settings
- 🔄 A/B testing de personalidades
- 🔄 Sugerencias contextuales basadas en historial
- 🔄 Widgets de estadísticas de uso

---

## 🚨 RIESGOS Y MITIGACIONES

### Riesgo 1: Conflictos de merge
**Probabilidad:** Media
**Impacto:** Alto
**Mitigación:**
- Cada agente trabaja en archivos separados
- Commits frecuentes con prefijos claros: `[AGENTE-X]`
- Integración controlada por AGENTE 6

### Riesgo 2: Traducciones incorrectas
**Probabilidad:** Media
**Impacto:** Medio
**Mitigación:**
- Usar traducciones existentes como referencia
- Review cruzado entre agentes
- Testing con usuarios nativos (opcional)

### Riesgo 3: Performance degradation
**Probabilidad:** Baja
**Impacto:** Alto
**Mitigación:**
- Lazy loading obligatorio
- Cache compression
- Performance testing en FASE 3

### Riesgo 4: Breaking changes en código existente
**Probabilidad:** Baja
**Impacto:** Alto
**Mitigación:**
- No modificar interfaces públicas
- Agregar nuevos métodos en vez de cambiar existentes
- Testing exhaustivo de regresión

---

## 📝 CONVENCIONES DE CÓDIGO

### Commits
```
[AGENTE-1] feat: Add conversation history service
[AGENTE-2] ui: Create settings screen layout
[AGENTE-3] i18n: Add Spanish translations for settings
[AGENTE-6] test: Integration tests for settings flow
```

### Branches
```
feature/cosmic-coach-settings-agent1
feature/cosmic-coach-settings-agent2
...
```

### Comentarios
```dart
/// 🔧 AGENTE-1: Service for managing conversation history
///
/// Provides CRUD operations for saved conversations:
/// - Save current chat as a conversation
/// - Load previous conversations
/// - Delete old conversations
/// - Export conversations to various formats
///
/// **Storage:** Uses SharedPreferences with JSON serialization
/// **Cache:** In-memory cache for fast access
/// **Multiuser:** Isolated by userId
class ConversationHistoryService {
  // ...
}
```

---

## ✅ DELIVERABLES FINALES

1. **Código:**
   - ✅ 10+ archivos nuevos
   - ✅ 4 archivos modificados
   - ✅ 0 warnings, 0 errores

2. **Traducciones:**
   - ✅ 60+ nuevas strings en 6 idiomas
   - ✅ Consistencia validada

3. **Documentación:**
   - ✅ Architecture guide
   - ✅ User guide
   - ✅ Testing report
   - ✅ Changelog

4. **Testing:**
   - ✅ Checklist completo
   - ✅ Screenshots de todas las pantallas
   - ✅ Performance report

---

## 🎬 PRÓXIMOS PASOS

**AHORA MISMO:**
1. ✅ Aprobar este plan
2. 🔄 Activar los 7 agentes en paralelo
3. 🔄 Iniciar FASE 1

**¿Listo para empezar?** 🚀

Responde con:
- **"GO"** → Activo todos los agentes ahora
- **"REVIEW"** → Quieres ajustar algo del plan primero
- **"PHASE X"** → Quieres empezar por una fase específica

---

# 🧬 VERSIÓN 2: PLAN MAESTRO EXTENDIDO (MULTIAGENTE + CLAUDE CODE)

Esta sección extiende el plan original para que el sistema de Cosmic Coach quede **irreconocible** a nivel de calidad, modularidad y flujo de trabajo con Claude Code.

## 1. Metas globales ampliadas

- **Experiencia usuario**
  - NPS interno del coach cósmico > 9/10.
  - Tiempo medio hasta primera respuesta útil < 5 segundos.
- **Calidad de contenido**
  - Respuestas coherentes con signo, casa y contexto de conversación.
  - Sin contradicciones entre chat, cartas y features premium.
- **Internacionalización**
  - 6 idiomas 100% cubiertos, sin `TODO` ni textos hardcodeados.
- **Arquitectura**
  - Cualquier nuevo modo/setting se pueda agregar en < 30 minutos.

## 2. Mapa de módulos refinado

1. **Core Settings & Modes**
   - `PreferencesService` + enums de `chatMode`, `coachPersonality` y flags premium.
   - Perfiles de configuración prearmados: `starter`, `powerUser`, `mystic`.
2. **Conversation Engine**
   - `ConversationHistoryService` para historial.
   - `FavoriteMessageService` separado para favoritos.
   - `ChatCacheService` para tamaño, limpieza y compresión de caché.
3. **Cosmic Coach Brain**
   - `HoroscopeChatService` con modos `quick`, `balanced`, `detailed`.
   - Reutilización de plantillas del resto de la app (no duplicar contenido).
4. **UI Settings & Flows**
   - `CosmicCoachSettingsScreen` + onboarding del coach.
   - `ConversationHistoryScreen` + `FavoriteMessagesScreen`.
   - Panel de estado cósmico dentro del chat.
5. **i18n Layer**
   - Plantilla unificada de keys.
   - Reglas sobre tono, formalidad y terminología astral.
6. **Quality & Guardrails**
   - Tests para cada modo de respuesta.
   - Escenarios extremos (offline, sin premium, heavy users, cambios de idioma).

## 3. Nuevos componentes de backend

### 3.1. CosmicProfile & CosmicProfileService

- **Objetivo:** cambiar la experiencia completa del usuario con un solo perfil.
- **Conceptos:**
  - `CosmicProfile` (`starter`, `powerUser`, `mystic`).
  - `CosmicProfilePreset` con configuración recomendada.
- **Responsabilidades del servicio:**
  - Detectar el perfil por defecto según datos del usuario.
  - Aplicar un perfil sobre `PreferencesService`.
  - Permitir que el usuario cambie de perfil desde settings.

> Implementación concreta delegada al **AGENTE 1 / Backend Smith**.

---

## 4. Nuevas capas de UX

### 4.1. Onboarding del coach cósmico

- 2–3 pantallas donde el usuario:
  - Elige personalidad del coach.
  - Elige modo de respuesta.
  - Ve un ejemplo de respuesta antes de confirmar.
- Guardar elecciones como preferencias iniciales vía `PreferencesService`.

### 4.2. Panel de estado cósmico en el chat

- Badges visibles en `CosmicCoachChatScreen` para:
  - Modo actual (Quick / Balanced / Detailed).
  - Personalidad activa.
  - Estado de conexión (offline/online).
- Indicadores claros cuando se está usando una función premium.

> Implementación concreta delegada al **AGENTE 2 / UI Nebula**.

---

## 5. Reglas globales de i18n (alineadas con el proyecto)

- Comentarios y documentación en **español**.
- Código y nombres de variables en **inglés**.
- Tono cálido, directo, sin exceso de jerga esotérica.
- Misma terminología de signos, casas y aspectos en todas las secciones.

> Implementación concreta delegada a **Language Oracle (AGENTES 3–5)** sobre los `.arb`.

---

## 6. Estrategia de calidad reforzada

- Tests específicos por modo de respuesta:
  - Quick: 0 llamadas a backend.
  - Balanced: proporción aproximada de backend/local.
  - Detailed: respeto de límites diarios y premium.
- “Cosmic Scenarios” mínimos:
  - Usuario sin premium y sin conexión.
  - Usuario premium heavy user.
  - Usuario que cambia mucho de idioma.

> Diseño y verificación a cargo de **Guardian of Consistency (AGENTE 6 + 7)**.

---

## 7. Agentes recomendados para Claude Code

Estos son agentes conceptuales que puedes configurar como presets/perfiles en Claude Code.

### 7.1. Cosmic Architect

- **Rol:** director de orquesta.
- **Enfoque:** arquitectura, responsabilidades por módulo, decisiones de alto nivel.
- **Uso:** cuando quieras redefinir el sistema o planificar grandes cambios sin tocar código todavía.

### 7.2. Backend Smith

- **Rol:** AGENTE 1 especializado en `lib/services` y `lib/models`.
- **Enfoque:** servicios, modelos, lógica de negocio, performance y premium/free.
- **Uso:** para crear o modificar servicios como `ConversationHistoryService`, `ChatCacheService`, `CosmicProfileService` y extensiones de `PreferencesService`.

### 7.3. UI Nebula

- **Rol:** AGENTE 2 especializado en `lib/screens` y `lib/widgets`.
- **Enfoque:** layouts, navegación, microinteracciones, dark mode, responsiveness.
- **Uso:** para pantallas nuevas, flows, y refactor de UI usando solo keys de i18n.

### 7.4. Language Oracle

- **Rol:** maestro de traducciones (AGENTES 3–5 unificados).
- **Enfoque:** `.arb`, tono, consistencia terminológica, detección de strings sin traducir.
- **Uso:** para generar o revisar bloques de traducciones en los 6 idiomas.

### 7.5. Guardian of Consistency

- **Rol:** mezcla de AGENTE 6 + 7.
- **Enfoque:** integración, testing, performance, limpieza de código y documentación.
- **Uso:** para cerrar features, proponer tests, detectar regresiones y sugerir refactors acotados.

---

## 8. Cómo trabajar con estos agentes en el día a día

1. **Elegir agente según tarea** (no usar un solo perfil genérico).
2. **Dar siempre un objetivo concreto** de 1–2 frases.
3. **Especificar archivos/carpetas clave** antes de pedir cambios.
4. **Mantener las reglas de idioma:**
   - Código en inglés.
   - Comentarios/documentación en español.
5. **Usar Guardian of Consistency** al final de cada feature grande para validar que nada se rompió.

Con esta versión 2 del plan, el sistema de Cosmic Coach queda preparado para evolucionar de forma agresiva, modular y totalmente alineada con un flujo de trabajo multiagente usando Claude Code.
