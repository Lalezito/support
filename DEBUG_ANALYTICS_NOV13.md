# 🔍 Debug Analytics - 13 Nov 2025

## 🐛 Problemas Reportados

### **1. Analytics no suma Compatibility**
- Calculaste compatibilidad
- Fuiste a Analytics
- NO se sumó el contador

### **2. Analytics dice "No data yet"**
- Ya usaste features (Coach, Compatibility)
- Analytics muestra pantalla vacía

### **3. Premium no se actualiza automáticamente**
- Obtienes upgrade a premium
- Tienes que cerrar/abrir app para que se desbloquee

---

## 🔍 Debugging Step-by-Step

### **Test 1: Verificar que los contadores se están guardando**

#### **Paso 1: Usar Compatibility**
```
1. Abre Compatibility
2. Calcula compatibilidad entre 2 signos
3. EN ESE MOMENTO, busca en logs (consola de Xcode o flutter logs):

   Debes ver:
   "📊 Compatibility count: X"

   ✅ Si lo ves → El contador SÍ se está guardando
   ❌ Si NO lo ves → El método NO se está llamando
```

#### **Paso 2: Usar Cosmic Coach**
```
1. Abre Cosmic Coach
2. Envía UN mensaje
3. EN ESE MOMENTO, busca en logs:

   Debes ver:
   "📊 Coach sessions count: X"

   ✅ Si lo ves → El contador SÍ se está guardando
   ❌ Si NO lo ves → El método NO se está llamando
```

---

### **Test 2: Verificar que Analytics lee los contadores**

#### **Después de usar Compatibility y Coach:**
```
1. Ve a Analytics (bottom nav)
2. Si dice "No data yet":
   → PULL DOWN (arrastra hacia abajo para refrescar)
3. Espera 1-2 segundos
4. ¿Qué ves ahora?

   Opción A: Sigue "No data yet"
   Opción B: Aparecen datos pero números en 0
   Opción C: Aparecen datos con números correctos (1-2)
```

---

### **Test 3: Verificar persistencia**

```
1. Usa Coach 2 veces
2. Usa Compatibility 2 veces
3. Ve a Analytics → pull down
4. Anota los números (ej: Coach=2, Compatibility=2)
5. CIERRA la app completamente
6. Reabre la app
7. Ve a Analytics → pull down
8. ¿Los números son los mismos? (2 y 2)

   ✅ Si → Persistencia funciona
   ❌ No → Persistencia NO funciona
```

---

## 🔍 Comandos de Debug

### **Ver logs en tiempo real:**

```bash
# Opción 1: Script automatizado
./check_analytics_counters.sh

# Opción 2: Manual
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter run 2>&1 | grep -E "(📊|Analytics|compatibility|coach)"
```

---

## 📊 Qué Buscar en Logs

### **Cuando usas Compatibility:**
```
[HH:MM:SS] 📊 Compatibility count: 1
[HH:MM:SS] 📊 Compatibility count: 2
...
```

### **Cuando usas Coach:**
```
[HH:MM:SS] 📊 Coach sessions count: 1
[HH:MM:SS] 📊 Coach sessions count: 2
...
```

### **Cuando abres Analytics:**
```
[HH:MM:SS] 📊 Analytics data loaded successfully
```

---

## 🐛 Diagnóstico

### **Escenario A: No ves logs de contadores**
**Problema:** Los métodos `_incrementCompatibilityCount()` o `_incrementCoachSessionCount()` NO se están llamando

**Posibles causas:**
1. El código no se compiló correctamente
2. Estás usando una versión vieja de la app
3. Hay un error silencioso (catch sin log)

**Solución:**
```bash
# Recompilar desde cero:
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
flutter pub get
flutter run
```

---

### **Escenario B: Ves logs de contadores, pero Analytics dice "No data yet"**
**Problema:** Los contadores se guardan, pero Analytics no los lee

**Posibles causas:**
1. Analytics no está leyendo de SharedPreferences
2. Hay un error en `_buildUserStats()`
3. CoreAnalyticsService falla y no hay fallback

**Solución:** Revisar código de analytics_data_provider.dart línea 113-124

---

### **Escenario C: Ves logs de contadores, Analytics muestra números pero en 0**
**Problema:** Analytics lee, pero el valor es 0

**Posibles causas:**
1. Los keys de SharedPreferences no coinciden
2. Se está leyendo antes de guardar (race condition)
3. SharedPreferences se está limpiando

**Solución:** Verificar keys:
- `'analytics_compatibility_count'`
- `'analytics_coach_sessions_count'`

---

### **Escenario D: Todo funciona pero requiere pull-down**
**Problema:** No hay auto-refresh

**Causa:** Por diseño, Analytics no se refresca automáticamente
**Solución:** Ver sección "Mejoras Propuestas" abajo

---

## 💡 Mejoras Propuestas (para después)

### **1. Auto-refresh al volver a la pantalla**
```dart
// En analytics_dashboard_screen.dart:
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  // Refresh cuando vuelves a la pantalla
  Future.microtask(() {
    ref.read(analyticsDataProvider.notifier).refresh();
  });
}
```

### **2. Listener global de eventos**
```dart
// Cuando se usa Coach o Compatibility, notificar a Analytics
// Usar EventBus o StreamController
```

### **3. Premium auto-refresh**
```dart
// Cuando cambia premium status, invalidar provider
ref.listen(premiumProvider, (previous, next) {
  if (previous != next) {
    ref.refresh(analyticsDataProvider);
  }
});
```

---

## 🎯 Plan de Acción

### **Paso 1: Confirmar el problema (5 min)**
```
1. Corre: ./check_analytics_counters.sh
2. Usa Compatibility → ¿ves "📊 Compatibility count: 1"?
3. Usa Coach → ¿ves "📊 Coach sessions count: 1"?
4. Ve a Analytics → pull down → ¿aparecen números?
```

### **Paso 2: Reportar (2 min)**
```
Reporta aquí los resultados de cada paso:

✅/❌ Compatibility count aparece en logs
✅/❌ Coach sessions count aparece en logs
✅/❌ Analytics muestra datos después de pull-down
✅/❌ Números son correctos (1-2)

Escenario que aplica: A/B/C/D (ver arriba)
```

### **Paso 3: Aplicar fix (depende del escenario)**
```
Según el escenario, aplicaremos el fix correspondiente
```

---

## 🚨 Notas Importantes

### **¿Por qué "No data yet"?**
Analytics puede mostrar "No data yet" si:
1. Es la primera vez que abres Analytics (normal)
2. CoreAnalyticsService no tiene datos aún
3. Los contadores locales están en 0
4. Hay un error al cargar datos

### **¿Por qué necesito pull-down?**
Por diseño actual, Analytics:
- Se carga al abrir la pantalla
- NO se refresca automáticamente
- Requiere pull-down manual para actualizar

Esto es **esperado** con el código actual.
Para auto-refresh, ver "Mejoras Propuestas" arriba.

### **¿Por qué Premium requiere reiniciar?**
Problema separado. Premium Provider puede no estar:
1. Invalidándose correctamente
2. Notificando a listeners
3. Refrescando después de purchase

Necesitamos investigar el flujo de Premium después de compra.

---

## 📝 Próximos Pasos

### **Inmediato:**
1. Ejecuta Test 1 y Test 2 arriba
2. Reporta qué escenario aplica (A/B/C/D)
3. Reporta los logs que ves (o NO ves)

### **Después del diagnóstico:**
1. Aplicar fix según escenario
2. Implementar auto-refresh (mejora)
3. Arreglar Premium auto-update

---

**Comando para empezar el debug:**
```bash
./check_analytics_counters.sh
```

**Busca en logs:** `📊` emoji

**Si no ves logs:** Reporta y haremos flutter clean + rebuild
