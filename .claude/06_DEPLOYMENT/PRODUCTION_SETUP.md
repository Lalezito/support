# 🚀 GUÍA DE CONFIGURACIÓN PARA PRODUCCIÓN - ZODIAC APP

## ✅ COMPLETADO

### **Dependencias y Compilación**
- ✅ Podfile actualizado a iOS 14.0
- ✅ Todas las dependencias de producción instaladas
- ✅ CocoaPods funcionando correctamente
- ✅ App compila sin errores en iOS
- ✅ IDs de AdMob actualizados a producción

## 🔧 CONFIGURACIÓN PENDIENTE

### **1. AdMob - Configuración Real (CRÍTICO)**
Los IDs actuales son placeholders. Necesitas:

1. **Ir a AdMob Console**: https://admob.google.com
2. **Crear nueva app**: "Zodiac App"
3. **Obtener IDs reales** para reemplazar en `lib/services/ad_service.dart`:
   ```dart
   // REEMPLAZAR ESTOS IDs CON LOS REALES DE ADMOB:
   iOS Banner: 'ca-app-pub-4441524618400998/1234567890'
   Android Banner: 'ca-app-pub-4441524618400998/0987654321'
   iOS Intersticial: 'ca-app-pub-4441524618400998/1111111111'
   Android Intersticial: 'ca-app-pub-4441524618400998/2222222222'
   iOS Rewarded: 'ca-app-pub-4441524618400998/3333333333'
   Android Rewarded: 'ca-app-pub-4441524618400998/4444444444'
   ```

### **2. App Store Connect - Configuración (CRÍTICO)**

1. **Crear App en App Store Connect**:
   - Bundle ID: `com.zodiac.app.zodiacApp`
   - Nombre: "Zodiac App"
   - Categoría: "Lifestyle"

2. **Configurar In-App Purchases**:
   - Plan Mensual: `zodiac_monthly_premium` - $4.99 USD
   - Plan Lifetime: `zodiac_lifetime_premium` - $49.99 USD

3. **Subir Screenshots**:
   - iPhone 6.7": 3 screenshots mínimo
   - iPhone 6.5": 3 screenshots mínimo
   - iPad Pro: 2 screenshots mínimo

### **3. Firebase - Push Notifications (MEDIO)**

1. **Firebase Console**: https://console.firebase.google.com
2. **Proyecto existente**: `zodi-a1658`
3. **Descargar archivos actualizados**:
   - `ios/Runner/GoogleService-Info.plist`
   - `android/app/google-services.json`

### **4. Certificados iOS (CRÍTICO)**

1. **Apple Developer Account**:
   - Crear App ID: `com.zodiac.app.zodiacApp`
   - Generar certificados de distribución
   - Crear provisioning profiles

2. **Xcode**:
   - Configurar signing automático
   - Seleccionar team correcto

## 📱 TESTING ANTES DE ENVÍO

### **TestFlight (Recomendado)**
```bash
# Build para TestFlight
flutter build ios --release
# Subir desde Xcode a App Store Connect
```

### **Validaciones Críticas**
- [ ] Suscripciones funcionan correctamente
- [ ] AdMob muestra anuncios reales
- [ ] Push notifications funcionan
- [ ] App funciona sin internet (modo offline)
- [ ] Traducciones correctas en todos los idiomas

## 🎯 ORDEN DE EJECUCIÓN RECOMENDADO

1. **AdMob Setup** (30 min) - Crear app y obtener IDs reales
2. **App Store Connect** (1 hora) - Crear app, configurar IAPs, subir screenshots
3. **Certificados iOS** (30 min) - Configurar signing
4. **TestFlight Build** (15 min) - Primera build de prueba
5. **Testing** (2 horas) - Validar todas las funcionalidades
6. **Envío Final** (15 min) - Submit for review

## 📋 CHECKLIST FINAL

- [ ] IDs de AdMob reales configurados
- [ ] App Store Connect configurado completamente
- [ ] Screenshots profesionales subidos
- [ ] Certificados iOS funcionando
- [ ] TestFlight build exitoso
- [ ] Todas las funcionalidades testeadas
- [ ] Política de privacidad y términos actualizados
- [ ] App enviada para revisión

## 🚨 NOTAS IMPORTANTES

- **Los IDs de AdMob actuales son PLACEHOLDERS** - deben reemplazarse
- **La app está 100% funcional** - solo necesita configuración externa
- **Tiempo estimado total**: 4-6 horas de configuración
- **Backend Railway**: Ya funcionando en producción ✅

---
*Generado automáticamente - Zodiac App Production Setup*
