# 🌍 PROBLEMA: Mensajes de Carga No Siguen el Idioma

**Fecha:** 22 de Noviembre, 2025
**Reportado por:** Usuario
**Severidad:** Media

---

## 🔍 PROBLEMA IDENTIFICADO

Los mensajes de carga inicial (splash screen, landing, etc.) **NO están siguiendo el idioma seleccionado** por el usuario. Aparecen siempre en inglés aunque el usuario haya seleccionado otro idioma.

### Pantallas Afectadas

1. **SplashScreen** (`lib/screens/splash_screen.dart`)
2. **CosmicLoadingScreen** (widget usado en múltiples lugares)
3. Cualquier pantalla que use `LoadingMessages` antes de que el idioma esté cargado

---

## 🛠️ ANÁLISIS TÉCNICO

### Código Actual del SplashScreen

```dart
@override
Widget build(BuildContext context) {
  final l10n = AppLocalizations.of(context)!;
  return CosmicLoadingScreen(
    message: l10n.loadingAppTitle,        // ❌ Context puede no tener idioma correcto aún
    subtitle: l10n.loadingInitializing,   // ❌ Context puede no tener idioma correcto aún
    showProgress: false,
  );
}
```

### El Problema

1. **El `SplashScreen` intenta usar `AppLocalizations.of(context)!`**
2. **PERO el contexto aún no tiene el `Locale` correcto** porque:
   - El idioma se carga desde `PreferencesService`
   - El `LanguageNotifier` carga el idioma de forma asíncrona en `build()`
   - El `MaterialApp` recibe `locale: Locale(currentLanguage)` de `languageProvider`
   - **Pero en el primer frame, `currentLanguage` puede ser 'en' por defecto**

### Flujo del Problema

```
1. App inicia
2. LanguageNotifier.build() lee de SharedPreferences (async)
3. Mientras tanto, currentLanguage = 'en' (default)
4. MaterialApp se construye con locale: Locale('en')
5. SplashScreen se construye
6. AppLocalizations.of(context) devuelve traducciones en inglés
7. Usuario ve "Loading..." en vez de "Cargando..." ❌
```

---

## ✅ SOLUCIONES PROPUESTAS

### Opción 1: Usar ConsumerWidget en SplashScreen (RECOMENDADO)

Hacer que el SplashScreen sea reactivo al `languageProvider`:

```dart
class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  // ... resto del código ...

  @override
  Widget build(BuildContext context) {
    // ✅ Reacciona cuando el idioma cambia
    final currentLanguage = ref.watch(languageProvider);
    final l10n = AppLocalizations.of(context)!;

    return CosmicLoadingScreen(
      message: l10n.loadingAppTitle,
      subtitle: l10n.loadingInitializing,
      showProgress: false,
    );
  }
}
```

**Pros:**
- ✅ Usa i18n nativo de Flutter
- ✅ Reactivo a cambios de idioma
- ✅ No duplica traducciones

**Contras:**
- ⚠️ Sigue habiendo un flash inicial en inglés hasta que el provider se actualiza

### Opción 2: Inicializar languageProvider ANTES del build

Modificar `LanguageNotifier` para que cargue el idioma de forma síncrona:

```dart
class LanguageNotifier extends Notifier<String> {
  @override
  String build() {
    final prefs = ref.read(preferencesServiceProvider);

    // ✅ Leer sincrónicamente si PreferencesService ya está inicializado
    if (prefs.isInitialized) {
      try {
        return prefs.userLanguage;
      } catch (e) {
        return 'en';
      }
    }

    return 'en';
  }

  // ... resto del código ...
}
```

**Pros:**
- ✅ Elimina el flash inicial
- ✅ El idioma está disponible desde el primer frame

**Contras:**
- ⚠️ Depende de que `PreferencesService` esté inicializado primero

### Opción 3: Usar LoadingMessages con idioma del provider

Modificar `LoadingMessages` para aceptar el idioma del provider:

```dart
// En SplashScreen
@override
Widget build(BuildContext context) {
  final currentLanguage = ref.watch(languageProvider);

  return CosmicLoadingScreen(
    message: LoadingMessages.getMessage('general', currentLanguage),
    subtitle: LoadingMessages.getMessage('initializing', currentLanguage),
    showProgress: false,
  );
}
```

Y agregar más contextos a `LoadingMessages`:

```dart
// En LoadingMessages
case 'initializing':
  if (language == 'es') return 'Inicializando...';
  if (language == 'fr') return 'Initialisation...';
  if (language == 'de') return 'Initialisierung...';
  if (language == 'it') return 'Inizializzazione...';
  if (language == 'pt') return 'Inicializando...';
  return 'Initializing...';
```

**Pros:**
- ✅ No depende de `AppLocalizations`
- ✅ Usa directamente el idioma del provider
- ✅ Funciona incluso antes de que MaterialApp esté listo

**Contras:**
- ⚠️ Duplica traducciones (ya existen en i18n)

---

## 🎯 SOLUCIÓN RECOMENDADA

**Combinar Opción 1 + Opción 2:**

1. **Asegurar que `PreferencesService` se inicializa ANTES del primer build** (en `main.dart`)
2. **Hacer que `LanguageNotifier` lea el idioma sincrónicamente** si `PreferencesService` ya está listo
3. **Usar `ref.watch(languageProvider)` en componentes** para reaccionar a cambios

### Implementación

#### Paso 1: Verificar inicialización en main.dart

```dart
// En _MyAppState
Future<void> _initializeApp() async {
  setState(() => _isLoading = true);

  try {
    // ✅ Inicializar PreferencesService PRIMERO
    final prefsService = ref.read(preferencesServiceProvider);
    if (!prefsService.isInitialized) {
      await prefsService.initialize();
    }

    // ✅ Ahora el languageProvider puede leer el idioma correctamente
    final language = ref.read(languageProvider);
    AppLogger.debug('App iniciada con idioma: $language');

    // ... resto de inicializaciones ...
  } finally {
    setState(() => _isLoading = false);
  }
}
```

#### Paso 2: Modificar LanguageNotifier

```dart
class LanguageNotifier extends Notifier<String> {
  @override
  String build() {
    final prefs = ref.read(preferencesServiceProvider);

    // ✅ Lectura síncrona si ya está inicializado
    if (prefs.isInitialized) {
      try {
        final lang = prefs.userLanguage;
        AppLogger.debug('LanguageNotifier: idioma cargado = $lang');
        return lang;
      } catch (e) {
        AppLogger.error('LanguageNotifier: error leyendo idioma', e);
        return 'en';
      }
    }

    AppLogger.warning('LanguageNotifier: PreferencesService no inicializado, usando default');
    return 'en';
  }

  void setLanguage(String value) {
    final prefs = ref.read(preferencesServiceProvider);
    prefs.setUserLanguage(value);
    state = value;
  }
}
```

#### Paso 3: Asegurar que SplashScreen reacciona

```dart
// Ya está usando ConsumerWidget, solo necesita watch
@override
Widget build(BuildContext context) {
  // ✅ Esto hace que rebuild cuando cambie el idioma
  ref.watch(languageProvider);

  final l10n = AppLocalizations.of(context)!;
  return CosmicLoadingScreen(
    message: l10n.loadingAppTitle,
    subtitle: l10n.loadingInitializing,
    showProgress: false,
  );
}
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

- [ ] Verificar que `PreferencesService` se inicializa antes del primer build
- [ ] Modificar `LanguageNotifier` para lectura síncrona
- [ ] Agregar logs para debugging
- [ ] Asegurar que `SplashScreen` hace `ref.watch(languageProvider)`
- [ ] Verificar que `CosmicLoadingScreen` recibe textos correctos
- [ ] Probar con todos los idiomas soportados
- [ ] Verificar que no hay flash de inglés al inicio

---

## 🧪 PRUEBAS NECESARIAS

1. **Prueba 1:** Usuario nuevo (sin idioma guardado)
   - ✅ Debe mostrar inglés por defecto
   - ✅ Después de seleccionar idioma, debe usar ese idioma

2. **Prueba 2:** Usuario existente (con idioma guardado)
   - ✅ Debe mostrar mensajes en el idioma guardado desde el inicio
   - ✅ NO debe haber flash de inglés

3. **Prueba 3:** Cambio de idioma
   - ✅ Al cambiar idioma, splash debe actualizarse en próximo inicio

4. **Prueba 4:** Todos los idiomas
   - [ ] English: "Initializing..."
   - [ ] Español: "Inicializando..."
   - [ ] Français: "Initialisation..."
   - [ ] Deutsch: "Initialisierung..."
   - [ ] Italiano: "Inizializzazione..."
   - [ ] Português: "Inicializando..."

---

## 📂 ARCHIVOS AFECTADOS

- `lib/screens/splash_screen.dart` - ✅ Ya usa i18n
- `lib/widgets/ui/cosmic_loading_screen.dart` - ✅ Recibe strings
- `lib/providers/consolidated_providers.dart` - 🔧 Modificar `LanguageNotifier`
- `lib/main.dart` - 🔧 Verificar orden de inicialización
- `lib/utils/loading_messages.dart` - ℹ️ Backup para contextos sin i18n

---

## 🎬 PRÓXIMOS PASOS

1. Implementar solución recomendada
2. Probar con hot restart (no hot reload)
3. Verificar logs de inicialización
4. Documentar resultados
