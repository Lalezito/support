# 🧹 Auditoría de Duplicados, Mocks y Legacy – Zodiac App

## 📌 Resumen ejecutivo
- Identificados servicios duplicados, mocks de desarrollo y capas legacy que ya no aportan valor en producción.
- Recomendado consolidar en torno a `RevenueCatService`, `PreferencesService`, `UnifiedNotificationService` y los pipelines de contenido actuales.
- Limpiar mocks reduce deuda técnica y previene falsos positivos en QA.

---

## 🔴 Duplicados críticos
- **`lib/services/consolidated/premium_storage_service.dart`** vs. **`lib/services/storage/premium_storage_manager.dart`**  
  El primero ya unifica almacenamiento premium (cifrado, logs, backups). `premium_storage_manager.dart` es un remanente simple de `SharedPreferences`. ✅ Eliminar o migrar a la capa consolidada.

- **`lib/services/subscription_service.dart`** vs. `PremiumSubscriptionManager` (en `lib/services/premium_subscription_manager.dart`)  
  `subscription_service.dart` fue regenerado completo; toda la lógica actual debe centralizarse ahí usando `rc.RevenueCatService`. ✅ Revisar llamadas en providers (`premium_provider.dart`) para evitar caminos duplicados.

- **`lib/services/premium_features_service.dart`** y `lib/services/premium_tier_system.dart`  
  Ambos contienen listados de beneficios por tier. ✅ Mantener uno (recomendado `premium_tier_system.dart`) y referenciarlo desde todos los widgets.

- **`lib/services/prediction_notification_service.dart`** y `lib/services/unified_notification_service.dart`  
  El primero aún tiene TODOs y mocks; el segundo es el orquestador real. ✅ Integrar scheduling/cancelación con `UnifiedNotificationService` y descartar la capa duplicada.

---

## 🟠 Mocks / datos simulados
- **`lib/providers/premium_provider.dart`**  
  `PaymentResult` retorna IDs `mock_payment_*`. ✅ Reemplazar por respuestas reales desde `RevenueCatIntegration`.

- **`lib/services/cosmic_chat_service.dart`**  
  `_mockAiResponses` sigue alimentando Chat aunque ya existe `AIInsights` real. ✅ Conectar a backend o consolidar con `consolidated_ai`.

- **`lib/services/subscription_service.dart`**  
  `_createMockPurchaseDetails()` devuelve `null` y está marcado como placeholder. ✅ Eliminar el flujo mock y basarse solo en `PurchaseDetails` reales.

- **`lib/services/premium_orchestrator_service.dart`**  
  Se generan respuestas mock para crisis/coaching. ✅ Integrar con `consolidated_ai` o servicios reales.

- **`lib/services/cryptography_service.dart`**  
  `_generateMockReceiptData()` usado en tests. ✅ Sustituir por fixtures controlados o mocks en entorno de prueba, no en runtime.

- **`lib/services/firebase_app_check_service.dart`**  
  Método `generateMockToken()`. ✅ Deshabilitar para builds productivos.

---

## 🟡 Código legacy / redundante
- **`lib/services/preferences_service.dart`**  
  Mantiene métodos `legacy` (`getUserLanguage`, `clearAllSensitiveDataForGDPR`) que duplican APIs nuevas. ✅ Documentar qué queda para migración y limpiar.

- **`lib/services/system_info_service.dart`**  
  API legacy para `DeviceInfoService`. ✅ Sustituir por wrappers modernos o remover.

- **`lib/services/horoscope_service.dart`**  
  Métodos “LEGACY” (`generateHybridHoroscope`, `generateInfiniteDailyHoroscope`) conviven con pipelines nuevos. ✅ Consolidar en un solo flujo.

- **`lib/services/weekly_horoscope_service.dart`** y `lib/services/backend_service.dart`  
  Métodos para descargar horóscopos en masa aún referencian endpoints antiguos. ✅ Migrar a API actual o eliminar.

- **`lib/services/offline_mode_service.dart`**  
  Métodos públicos documentados pero incompletos. ✅ Decidir si se mantiene modo offline; de lo contrario, remover.

---

## 🧪 Componentes simulados para demos
- **`lib/screens/premium_timing_dashboard_screen.dart`** y otros dashboards usan “mock dependencies” para UI. ✅ Reemplazar con providers reales o esconder en modo demo.
- **`lib/widgets/chat/typing_indicator_widget.dart`** marcado como duplicado, conviene borrar si no se usa.
- **`lib/widgets/monetization/banner_ad_widget.dart`** comenta que reemplaza un duplicado. ✅ Verificar que la ruta nueva (`AdBannerWidget`) esté en uso y limpiar archivo viejo.

---

## ✅ Acciones recomendadas
- **[storage_consolidation]** Retirar `premium_storage_manager.dart`; mover cualquier llamada a `PremiumStorageService`.
- **[revenuecat_alignment]** Actualizar providers/servicios para depender exclusivamente de `rc.RevenueCatService` + `RevenueCatIntegration`.
- **[notification_real_impl]** Completar `PredictionNotificationService` enlazándolo a `UnifiedNotificationService` y eliminar mocks.
- **[ai_mock_cleanup]** Sustituir bots mock (`cosmic_chat_service`, `premium_orchestrator_service`) por pipelines en `consolidated_ai`.
- **[legacy_retirement]** Registrar en backlog la eliminación de métodos `legacy` en `preferences_service.dart`, `system_info_service.dart`, `horoscope_service.dart`, etc.
- **[demo_components]** Catalogar pantallas/widgets que siguen en modo demo y decidir si se mudan a carpeta `demo/` o se eliminan.

---

## 🔍 Notas para seguimiento
- Todo lo marcado como ✅ puede añadirse al `TODO_EXECUTION_PLAYBOOK.md` bajo Fase 6 (Observability & Cleanup).
- Antes de eliminar archivos, confirmar que no existan dependencias en tests (`search in repo`).
- Ejecutar `flutter analyze` + suites de tests después de cada limpieza para asegurar regresiones cero.
