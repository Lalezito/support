# 📋 Playbook de TODOs Prioritarios – Zodiac App

> **✅ FASES 1-4 COMPLETADAS AL 100%**
>
> 🎯 **PLAN EXTENDIDO DISPONIBLE**:
> - `.claude/TODO_EXECUTION_MASTER_PLAN_2025.md` - Fases 1-4 (100% ✅)
> - `.claude/TODO_EXECUTION_MASTER_PLAN_PHASE_5-9.md` - Fases 5-9 (0% 🚀)
>
> **Fases Completadas (1-4)**:
> - ✅ Infraestructura Crítica
> - ✅ Backend & Contenido
> - ✅ Servicios Avanzados
> - ✅ Refactoring
>
> **Fases Pendientes (5-9)**:
> - 🚀 QA & Testing Integral
> - 🚀 Observability & Monitoring
> - 🚀 Documentation & Knowledge Base
> - 🚀 Test Automation & Coverage
> - 🚀 Rollout & Deployment Strategy
>
> **Para continuar**: Ejecuta `Ejecuta la FASE 5 del plan extendido`

---

## 🛠️ Estado general
- Auditoría de TODO/FIXME/HACK completada en `lib/`
- No hay errores de `flutter analyze`; solo warnings restantes
- Este playbook está diseñado para agentes Claude Code / Windsurf en `/Users/alejandrocaceres/Desktop/appstore - zodia/.claude`

---

## 🔴 Prioridad MÁXIMA (Critical Path)
- **[notifier_real_impl]** `lib/services/prediction_notification_service.dart`
  - Implementar notificaciones reales (schedule/cancel/send) usando `UnifiedNotificationService`
  - Persistir preferencias (`_loadPreferences()`, `_savePreferences()`) con `PreferencesService`
- **[compatibility_user_id]** `lib/services/consolidated_compatibility/core_compatibility_service.dart`
  - Reemplazar placeholder `userId: 'anonymous'` por `UserIdentityService` / `PreferencesService`
  - Necesario para analytics y debugging de compatibilidad
- **[pricing_provider]** `lib/providers/premium_provider.dart`
  - Definir `SubscriptionPricingInfo` o reutilizar `PremiumTierSystem`
  - Activar provider comentado para exponer precios a la UI

---

## 🟠 Prioridad ALTA
- **[notification_persistence]** `prediction_notification_service.dart`
  - Garantizar que los cambios de preferencias se guarden/restauren entre sesiones
- **[horoscope_backend_consolidation]** `lib/services/backend_service.dart`, `lib/services/horoscope_service.dart`, `lib/services/weekly_horoscope_service.dart`
  - Completar métodos marcados como “DESCARGAR TODOS LOS HORÓSCOPOS”, “MÉTODO HÍBRIDO”, etc.
  - Unificar endpoints Railway + caché local
- **[offline_cache_finish]** `lib/services/offline_mode_service.dart`
  - Terminar `_clearAllCaches()` y `getZodiacDescriptionOffline()` para soporte offline real
- **[crisis_content_final]** `lib/services/crisis_content_generator.dart`
  - Sustituir placeholders por contenido final y reglas según severidad

---

## 🟡 Prioridad MEDIA
- **[preferences_legacy_cleanup]** `lib/services/preferences_service.dart`
  - Migrar métodos legacy (`getUserLanguage`, `isPremiumUser`, GDPR cleaners) o eliminarlos si están obsoletos
- **[system_info_modernize]** `lib/services/system_info_service.dart`
  - Reemplazar métodos legacy con wrappers actualizados de `PackageInfo` / `DeviceInfo`
- **[predictive_transits]** `lib/services/predictive_astrology_service.dart`
  - Implementar `_generateFutureTransits()` y completar helpers asociados
- **[dynamic_cache_clear]** `lib/services/dynamic_content_service.dart`
  - Completar `_clearAllCaches()` para todos los servicios involucrados
- **[smart_journal_analysis]** `lib/services/smart_journaling_service.dart`
  - Revisar `_analyzeEmotionalContent` y helpers para análisis real (hoy mock)

---

## 🟢 Prioridad BAJA / Refactors
- **[string_interp_cleanup]** `lib/services/consolidated_ai/coaching_ai_service.dart`
  - Reemplazar `${variable}` → `$variable` en las líneas 804-839
- **[final_fields]**
  - `lib/services/consolidated_payments/quantum_payment_engine.dart`: `_totalPaymentsToday`, `_lastDayReset`
  - `lib/services/subscription_service.dart`: `_purchasePending`
- **[deprecated_tests]** `test/premium/subscription_payment_test.dart`
  - Migrar de `activatePremium()/deactivatePremium()` a `RevenueCatIntegration` (`purchaseSubscription`, `restorePurchases`)
- **[compatibility_params]** `lib/screens/compatibility_screen.dart`
  - Revisar parámetro `delay` sin uso en `_runCompatibilityFlow`
- **[lint_imports]** Retirar imports sobrantes:
  - `lib/screens/birth_data_collection_screen.dart`
  - `lib/screens/cosmic_coach_chat_screen.dart`

---

## ✅ Sugerencias de asignación (multi-agente)
- **Agente Notifications**: `[notifier_real_impl]`, `[notification_persistence]`
- **Agente Compatibility**: `[compatibility_user_id]`, `[compatibility_params]`
- **Agente Monetization**: `[pricing_provider]`, `[deprecated_tests]`
- **Agente Content**: `[horoscope_backend_consolidation]`, `[offline_cache_finish]`, `[crisis_content_final]`
- **Agente Preferences & Storage**: `[preferences_legacy_cleanup]`, `[system_info_modernize]`
- **Agente AI Insights**: `[smart_journal_analysis]`, `[predictive_transits]`

---

## 📚 Referencias de Documentación

### Graceful Degradation & Reliability
- **Estrategia**: `.claude/GRACEFUL_DEGRADATION_STRATEGY.md` - Patrón de degradación elegante con ejemplos de Netflix, Google, AWS
- **Implementación**: `.claude/FALLBACK_IMPROVEMENTS_REPORT.md` - Mejoras de fallbacks con logging y analytics
- **Validación QA**: `.claude/QA_FALLBACK_VALIDATION_CHECKLIST.md` - Lista de verificación para testing de fallbacks
- **Analytics**: `.claude/FINAL_IMPROVEMENTS_OCT6.md` - Integración de telemetría con CoreAnalyticsService

### Migration Planning & Tech Debt
- **Roadmap v2.0**: `.claude/MIGRATION_ROADMAP.md` - Plan de migración de métodos deprecados y tests
- **Cleanup Report**: `.claude/CLEANUP_COMPLETION_REPORT_OCT6.md` - Reporte de limpieza de código Oct 6

---

## 📎 Notas finales
- Toda la documentación/planificación debe quedar en `.claude/`
- Mantener uso de español en documentación/comentarios (según regla global)
- Antes de tocar servicios premium, validar `RevenueCatIntegration` y `PreferencesService`
- Cualquier actualización crítica → registrar en `CHANGELOG.md` y `PREMIUM_TESTING_CHECKLIST.md`
