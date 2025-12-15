# Error Doctor - Diagnóstico Experto de Errores del Proyecto Zodiac

Eres un experto en diagnosticar y resolver errores del proyecto Zodiac App. Tu trabajo es:

## 1. Diagnóstico Inicial
Ejecuta estos comandos para entender el estado actual:

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Estado de git
git status
git branch --show-current

# Verificar errores
flutter analyze 2>&1 | tail -50

# Contar errores vs warnings
flutter analyze 2>&1 | grep -c "error •" || echo "0 errors"
flutter analyze 2>&1 | grep -c "info •" || echo "0 infos"
```

## 2. Base de Conocimiento de Errores Comunes

### ERROR: Mezcla de archivos entre ramas (14k+ errores repentinos)
**Síntomas:** Miles de errores de `undefined_identifier`, `undefined_method`, imports rotos
**Causa:** `git checkout <otra-rama> -- .` mezcla archivos incompatibles
**Solución:**
```bash
git stash  # Guardar cambios locales
git checkout .  # Restaurar archivos de la rama actual
# O si necesitas los cambios:
git stash pop  # Recuperar cambios
```

### ERROR: SecretManagerService - métodos logInfo/logError no definidos
**Archivo:** `lib/services/secret_manager_service.dart`
**Causa:** La clase no extiende de una clase base con logging
**Solución:** Agregar mixin o importar AppLogger

### ERROR: AppLocalizations undefined
**Causa:** Falta import o no se generaron las localizaciones
**Solución:**
```bash
flutter gen-l10n
# O agregar import:
# import 'package:zodiac_app/l10n/app_localizations.dart';
```

### ERROR: Dependencias desactualizadas
**Síntomas:** Errores de versión, métodos deprecated
**Diagnóstico:**
```bash
flutter pub outdated
flutter pub deps
```
**Solución:**
```bash
flutter clean
flutter pub get
```

### ERROR: ZodiacSign undefined
**Causa:** Import relativo incorrecto
**Solución:** Cambiar a import absoluto:
```dart
import 'package:zodiac_app/models/zodiac_enums.dart';
```

## 3. Ramas Conocidas y Su Estado

| Rama | Estado | Errores | Notas |
|------|--------|---------|-------|
| `fix/cleanup-all-errors-2025-12-07` | ✅ Limpia | ~0 | Versión más estable |
| `agent-ux-production` | ⚠️ Casi limpia | ~67 | Última con features nuevos |
| `main` | ⚠️ Warnings | ~21k | Mayormente `avoid_print` |

## 4. Proceso de Recuperación Rápida

Si el proyecto está muy roto:
```bash
# Opción A: Volver a rama limpia
git stash
git checkout fix/cleanup-all-errors-2025-12-07
flutter clean && flutter pub get

# Opción B: Restaurar desde commit específico
git log --oneline -20  # Encontrar último commit bueno
git checkout <commit-hash> -- lib/
```

## 5. Registro de Errores Resueltos

### 2025-12-15: Mezcla de archivos entre ramas
- **Problema:** 14,617 errores por `git checkout main -- .`
- **Solución:** `git stash` restauró estado limpio de `agent-ux-production`
- **Lección:** Nunca usar `git checkout <rama> -- .` sin entender las consecuencias

---

Al ejecutar este comando, diagnostica el problema actual y sugiere la solución basándote en esta base de conocimiento. Si encuentras un error nuevo, documéntalo aquí para futuras referencias.