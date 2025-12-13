# 📋 TODOs PENDIENTES - FEATURES REALES

**Fecha:** 25 de Noviembre, 2025
**Estado:** Documentación de features pendientes de implementación

---

## 🔴 CRÍTICO - Integración RevenueCat

### 1. Compras Reales en Premium Controller
**Archivo:** `lib/controllers/premium_controller.dart`
**Línea:** 41
```dart
// TODO: Implementar lógica real de compra
```
**Descripción:** Actualmente usa placeholder. Necesita:
- Integración con RevenueCat SDK
- Validación de recibos
- Manejo de errores de compra
- Webhooks para sincronización

### 2. Restauración de Compras
**Archivo:** `lib/controllers/premium_controller.dart`
**Línea:** 67
```dart
// TODO: Implementar restauración real
```
**Descripción:** Funcionalidad para restaurar compras previas del usuario

---

## 🟡 IMPORTANTE - Card Generation Service

### 3. Legacy Card Generation
**Archivo:** `lib/services/card_generator_service.dart`
**Línea:** 278
```dart
// TODO: Implement legacy card generation
```

### 4. Compatibility Card Generation
**Archivo:** `lib/services/card_generator_service.dart`
**Línea:** 296
```dart
// TODO: Implement compatibility card generation
```

### 5. Cosmic Insight Card Generation
**Archivo:** `lib/services/card_generator_service.dart`
**Línea:** 307
```dart
// TODO: Implement cosmic insight card generation
```

### 6. Widget Capture
**Archivo:** `lib/services/card_generator_service.dart`
**Línea:** 317
```dart
// TODO: Implement widget capture
```
**Descripción:** Feature para compartir en redes sociales con imágenes personalizadas

---

## 🟢 NICE TO HAVE - UI Navigation

### 7. Navegación a Vista Detalle
**Archivo:** `lib/screens/conversation_history_screen.dart`
**Línea:** 173
```dart
// TODO: Navigate to conversation detail view
```
**Descripción:** Pantalla para ver conversación completa

### 8. Navegación a Upgrade Flow
**Archivo:** `lib/screens/premium_screen.dart`
**Línea:** 2511
```dart
// TODO: Navegar a upgrade flow
```

---

## 🔵 CONFIGURACIÓN - Premium Screen Adapters

### 9. Premium Screen V2
**Archivo:** `lib/screens/premium_screen_adapter.dart`
**Línea:** 26
```dart
// TODO: return PremiumScreenV2();
```
**Descripción:** Nueva versión de la pantalla premium (cuando esté lista)

### 10. Premium Screen Legacy
**Archivo:** `lib/screens/premium_screen_adapter.dart`
**Línea:** 35
```dart
// TODO: return PremiumScreenLegacy();
```
**Descripción:** Versión legacy para compatibilidad con versiones anteriores

---

## ⚪ DEPENDENCIAS - Packages

### 11. Cached Network Image
**Archivo:** `lib/widgets/cosmic_image_gallery.dart`
**Línea:** 12
```dart
// TODO: Add cached_network_image to pubspec.yaml
```
**Descripción:** Optimización de carga de imágenes con caché

---

## 📊 PRIORIZACIÓN

### Orden recomendado de implementación:

1. **RevenueCat Integration** (Crítico para monetización)
   - Sin esto no hay ingresos
   - Estimado: 2-3 días

2. **Card Generation Service** (Importante para engagement)
   - Feature de compartir en redes sociales
   - Estimado: 3-4 días

3. **Navigation Features** (Mejora UX)
   - Completar flujos de navegación
   - Estimado: 1-2 días

4. **Premium Screen Versions** (Futuro)
   - Cuando se decida renovar UI
   - Estimado: Variable

5. **Dependencies** (Quick win)
   - Agregar package cuando sea necesario
   - Estimado: 5 minutos

---

## 💡 NOTAS IMPORTANTES

- Los TODOs de l10n ya fueron implementados (no requieren trabajo)
- Los print statements en tests son OK mantenerlos
- El sistema de cambio de plan ya está implementado
- Los precios están configurados: Cósmico $6.99, Estelar $19.99

---

**Preparado por:** Claude Code
**Estado:** Documentación completa de features pendientes