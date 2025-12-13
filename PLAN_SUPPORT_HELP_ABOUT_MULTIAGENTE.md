# Plan Multi-Agente: Support, Help Center & About

## Fecha: 2025-12-09

## Objetivo
Mejorar profesionalmente las secciones de Support, Help Center, Feedback y About en la app.

---

## Distribución de Agentes

### AGENTE 1: Dependencies & SupportService
- Añadir url_launcher y package_info_plus a pubspec.yaml
- Crear lib/services/support_service.dart
- Email unificado: support@zodiaclifecoach.app

### AGENTE 2: FAQ System
- Crear lib/models/faq_models.dart
- Crear lib/data/faq_data.dart con ~25 FAQs

### AGENTE 3: HelpCenterScreen
- Crear lib/screens/help_center_screen.dart
- FAQs expandibles por categoría
- Botón Contact Support funcional

### AGENTE 4: FeedbackScreen
- Crear lib/screens/feedback_screen.dart
- Tipos: Bug, Feature, General, Rate
- Envío por email pre-llenado

### AGENTE 5: AboutScreen
- Crear lib/screens/about_screen.dart
- Versión dinámica con package_info_plus
- Links a Privacy, Terms, Website

### AGENTE 6: Fix Hardcoded Spanish
- Arreglar terms_and_privacy_screen.dart
- Localizar diálogos de Apple Subscription y Support

### AGENTE 7: Update Settings Screen
- Modificar settings_screen.dart
- Navegar a nuevas pantallas en lugar de diálogos

### AGENTE 8: Translations (6 idiomas)
- Añadir ~80-100 claves nuevas a cada archivo ARB
- EN, ES, DE, FR, IT, PT

---

## Estado: ✅ COMPLETADO

### Resumen de Archivos Creados/Modificados:

**Nuevos archivos:**
- `zodiac_app/lib/screens/help_center_screen.dart` - Pantalla de Help Center con FAQs expandibles
- `zodiac_app/lib/screens/feedback_screen.dart` - Pantalla de Feedback con 4 tipos
- `zodiac_app/lib/screens/about_screen.dart` - Pantalla About con versión dinámica
- `zodiac_app/lib/models/faq_models.dart` - Modelos para FAQ
- `zodiac_app/lib/data/faq_data.dart` - Datos de FAQ (5 categorías, 24 preguntas)
- `zodiac_app/lib/services/support_service.dart` - Servicio para emails y URLs

**Archivos modificados:**
- `zodiac_app/lib/screens/settings_screen.dart` - Navegación a nuevas pantallas
- `zodiac_app/lib/screens/terms_and_privacy_screen.dart` - Textos localizados
- `zodiac_app/assets/l10n/app_en.arb` - 25 claves nuevas
- `zodiac_app/assets/l10n/app_es.arb` - 25 claves nuevas
- `zodiac_app/assets/l10n/app_de.arb` - 25 claves nuevas
- `zodiac_app/assets/l10n/app_fr.arb` - 25 claves nuevas
- `zodiac_app/assets/l10n/app_it.arb` - 25 claves nuevas
- `zodiac_app/assets/l10n/app_pt.arb` - 25 claves nuevas

### Total: 150 claves de traducción añadidas (25 x 6 idiomas)
