# 🔥 GUÍA COMPLETA: CONFIGURAR FIREBASE EN RAILWAY
## **Setup de Variables de Entorno para Backend Node.js**

**Fecha:** 2025-10-03  
**Objetivo:** Configurar Firebase Admin SDK en Railway  
**Tiempo:** 15-20 minutos  

---

## 📋 PREREQUISITOS

```
✅ Cuenta de Railway (https://railway.app)
✅ Proyecto backend desplegado en Railway
✅ Cuenta Firebase (https://console.firebase.google.com)
✅ Proyecto Firebase creado ("Zodiac: Life Coach")
```

---

## 🔥 PASO 1: OBTENER SERVICE ACCOUNT KEY DE FIREBASE

### **1.1 Ir a Firebase Console**
```
1. Abrir: https://console.firebase.google.com
2. Seleccionar proyecto: "Zodiac: Life Coach"
3. Click en ⚙️ (Settings) arriba izquierda
4. Click "Project settings"
```

### **1.2 Generar Service Account**
```
5. Ir a pestaña "Service accounts"
6. Scroll down hasta "Firebase Admin SDK"
7. Seleccionar lenguaje: "Node.js"
8. Click botón "Generate new private key"
9. Confirmar en modal: "Generate key"
10. Se descargará archivo JSON (ej: zodiac-life-coach-firebase-adminsdk-xyz.json)
```

### **1.3 Formato del archivo descargado**
```json
{
  "type": "service_account",
  "project_id": "zodiac-life-coach",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xyz@zodiac-life-coach.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

⚠️ **IMPORTANTE:** Este archivo contiene información sensible. NO lo compartas ni lo subas a GitHub.

---

## 🚂 PASO 2: CONFIGURAR EN RAILWAY

### **2.1 Acceder a Railway Dashboard**
```
1. Ir a: https://railway.app/dashboard
2. Login con tu cuenta
3. Seleccionar el proyecto del backend Zodiac
4. Click en el servicio (ej: "zodiac-backend" o similar)
```

### **2.2 Agregar Variables de Entorno**
```
5. Click en pestaña "Variables"
6. Click botón "+ New Variable"
```

---

## 🔑 PASO 3: VARIABLES DE ENTORNO REQUERIDAS

### **Opción A: Service Account Completo (Recomendado)**

**Variable 1: FIREBASE_SERVICE_ACCOUNT**
```
Key: FIREBASE_SERVICE_ACCOUNT
Value: [Pegar TODO el contenido del archivo JSON en una sola línea]

Ejemplo (minificado):
{"type":"service_account","project_id":"zodiac-life-coach","private_key_id":"abc123...","private_key":"-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-xyz@zodiac-life-coach.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/..."}
```

**Cómo minificar el JSON:**
```bash
# Método 1: Online
1. Ir a: https://www.minifier.org/
2. Pegar contenido del archivo JSON
3. Click "Minify"
4. Copiar resultado

# Método 2: Terminal (macOS/Linux)
cat zodiac-life-coach-firebase-adminsdk-xyz.json | jq -c
```

---

### **Opción B: Variables Individuales (Alternativa)**

Si Railway tiene límite de caracteres por variable, usar este método:

```
FIREBASE_PROJECT_ID=zodiac-life-coach

FIREBASE_PRIVATE_KEY_ID=abc123...

FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
-----END PRIVATE KEY-----

FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xyz@zodiac-life-coach.iam.gserviceaccount.com

FIREBASE_CLIENT_ID=123456789

FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth

FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token

FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs

FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xyz%40zodiac-life-coach.iam.gserviceaccount.com
```

---

## 💻 PASO 4: CONFIGURAR CÓDIGO DEL BACKEND

### **4.1 Verificar estructura del proyecto**

Tu backend debe tener algo así:

```
zodiac-backend/
├── src/
│   ├── config/
│   │   └── firebase.js       ← Configuración de Firebase
│   ├── services/
│   │   └── firebaseService.js
│   └── index.js
├── package.json
└── .env (local only)
```

### **4.2 Código de inicialización - firebase.js**

```javascript
// src/config/firebase.js

const admin = require('firebase-admin');

let firebaseApp;

function initializeFirebase() {
  if (firebaseApp) {
    return firebaseApp; // Ya inicializado
  }

  try {
    // OPCIÓN A: Service Account completo desde variable
    if (process.env.FIREBASE_SERVICE_ACCOUNT) {
      const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
      
      firebaseApp = admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
        databaseURL: `https://${serviceAccount.project_id}.firebaseio.com`
      });
      
      console.log('✅ Firebase initialized with SERVICE_ACCOUNT');
      return firebaseApp;
    }
    
    // OPCIÓN B: Variables individuales
    if (process.env.FIREBASE_PROJECT_ID && process.env.FIREBASE_PRIVATE_KEY) {
      const serviceAccount = {
        type: "service_account",
        project_id: process.env.FIREBASE_PROJECT_ID,
        private_key_id: process.env.FIREBASE_PRIVATE_KEY_ID,
        private_key: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
        client_email: process.env.FIREBASE_CLIENT_EMAIL,
        client_id: process.env.FIREBASE_CLIENT_ID,
        auth_uri: process.env.FIREBASE_AUTH_URI || "https://accounts.google.com/o/oauth2/auth",
        token_uri: process.env.FIREBASE_TOKEN_URI || "https://oauth2.googleapis.com/token",
        auth_provider_x509_cert_url: process.env.FIREBASE_AUTH_PROVIDER_CERT_URL || "https://www.googleapis.com/oauth2/v1/certs",
        client_x509_cert_url: process.env.FIREBASE_CLIENT_CERT_URL
      };
      
      firebaseApp = admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
        databaseURL: `https://${process.env.FIREBASE_PROJECT_ID}.firebaseio.com`
      });
      
      console.log('✅ Firebase initialized with INDIVIDUAL VARS');
      return firebaseApp;
    }
    
    // OPCIÓN C: Desarrollo local con archivo
    if (process.env.NODE_ENV === 'development') {
      const serviceAccount = require('../../firebase-service-account.json');
      
      firebaseApp = admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
        databaseURL: `https://${serviceAccount.project_id}.firebaseio.com`
      });
      
      console.log('✅ Firebase initialized with LOCAL FILE (dev only)');
      return firebaseApp;
    }
    
    throw new Error('❌ No Firebase credentials found');
    
  } catch (error) {
    console.error('❌ Firebase initialization error:', error);
    throw error;
  }
}

// Exportar instancias
module.exports = {
  initializeFirebase,
  getFirestore: () => admin.firestore(),
  getAuth: () => admin.auth(),
  getStorage: () => admin.storage(),
  getMessaging: () => admin.messaging(),
};
```

### **4.3 Uso en el backend**

```javascript
// src/index.js

const express = require('express');
const { initializeFirebase } = require('./config/firebase');

const app = express();

// Inicializar Firebase al arrancar
initializeFirebase();

// Rutas de ejemplo
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', firebase: 'connected' });
});

// ... resto de rutas

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
```

---

## 🔍 PASO 5: TESTING Y VALIDACIÓN

### **5.1 Verificar variables en Railway**

```
1. Railway Dashboard
2. Tu proyecto → Variables tab
3. Verificar que FIREBASE_SERVICE_ACCOUNT existe
4. Click para ver (oculta por seguridad)
```

### **5.2 Hacer redeploy**

```
5. Railway automáticamente re-despliega al cambiar variables
6. O manualmente: Click "Deploy" en Railway
7. Esperar logs de deployment
```

### **5.3 Verificar logs de Railway**

```
8. Click en pestaña "Deployments"
9. Click en deployment más reciente
10. Buscar en logs:
    ✅ "Firebase initialized with SERVICE_ACCOUNT"
    ✅ "Server running on port 3000"

❌ Si hay errores:
   - "Firebase initialization error" → Revisar formato JSON
   - "Invalid service account" → Regenerar key en Firebase
   - "Parse error" → Verificar que JSON está bien minificado
```

### **5.4 Test endpoint**

```bash
# Desde terminal local:
curl https://tu-backend.railway.app/api/health

# Respuesta esperada:
{
  "status": "ok",
  "firebase": "connected"
}
```

---

## 🛡️ PASO 6: SEGURIDAD Y MEJORES PRÁCTICAS

### **6.1 Nunca hacer:**
```
❌ Subir archivo JSON a GitHub
❌ Hardcodear credenciales en código
❌ Compartir service account key
❌ Usar misma key en múltiples ambientes
```

### **6.2 Siempre hacer:**
```
✅ Usar variables de entorno
✅ Diferentes service accounts para dev/staging/prod
✅ Rotar keys periódicamente
✅ Monitorear uso en Firebase Console
✅ Habilitar solo los permisos necesarios
```

### **6.3 Agregar a .gitignore**
```gitignore
# Firebase service account
firebase-service-account*.json
*-firebase-adminsdk-*.json

# Environment variables
.env
.env.local
.env.production
```

---

## 📱 PASO 7: VARIABLES ADICIONALES (Opcionales)

Dependiendo de tu backend, podrías necesitar:

```bash
# OpenAI (para AI features)
OPENAI_API_KEY=sk-...

# Railway Database
DATABASE_URL=postgresql://...

# App Config
NODE_ENV=production
PORT=3000

# RevenueCat (si usas en backend)
REVENUECAT_API_KEY=...

# N8N Webhooks (si usas)
N8N_WEBHOOK_URL=https://...
```

---

## ✅ CHECKLIST FINAL

```
□ Service account key descargado de Firebase
□ JSON minificado correctamente
□ FIREBASE_SERVICE_ACCOUNT agregado en Railway
□ Código backend configurado (firebase.js)
□ Deployment exitoso
□ Logs muestran "Firebase initialized"
□ Endpoint /api/health funciona
□ .gitignore actualizado
□ Variables sensibles NO en código
```

---

## 🐛 TROUBLESHOOTING

### **Error: "Invalid service account"**
```
Causa: JSON malformado o incompleto
Solución:
1. Re-descargar key de Firebase
2. Verificar que JSON está completo
3. Minificar correctamente (sin espacios/saltos)
4. Re-pegar en Railway
```

### **Error: "Parse error"**
```
Causa: private_key con \n mal escapado
Solución:
1. Verificar que private_key tiene \\n (doble backslash)
2. O usar variables individuales (Opción B)
```

### **Error: "Permission denied"**
```
Causa: Service account sin permisos
Solución:
1. Firebase Console → IAM & Admin
2. Verificar que service account tiene rol "Firebase Admin SDK Service Agent"
3. O agregar manualmente rol "Editor" o "Owner"
```

### **Error: Railway no detecta cambios**
```
Solución:
1. Hacer cambio dummy en código (ej: agregar comentario)
2. Git commit + push
3. Railway auto-redespliega
```

---

## 🚀 COMANDOS RÁPIDOS

### **Minificar JSON (Terminal macOS/Linux):**
```bash
cat firebase-service-account.json | jq -c
```

### **Verificar Firebase localmente:**
```bash
# En tu backend local:
node -e "console.log(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT))"
```

### **Test de conexión:**
```bash
curl https://tu-backend.railway.app/api/health
```

---

## 📚 RECURSOS

```
Firebase Console:
https://console.firebase.google.com

Railway Dashboard:
https://railway.app/dashboard

Firebase Admin SDK Docs:
https://firebase.google.com/docs/admin/setup

Railway Environment Variables:
https://docs.railway.app/develop/variables
```

---

## ✨ RESULTADO FINAL

Después de seguir esta guía tendrás:

```
✅ Firebase Admin SDK funcionando en Railway
✅ Backend conectado a Firestore
✅ Variables de entorno seguras
✅ Deployment automático configurado
✅ Logs mostrando inicialización correcta
✅ Endpoint health check funcional
```

**🎯 Tu backend está listo para usar Firebase en producción!**

---

**Fecha creación:** 2025-10-03  
**Versión:** 1.0  
**Mantenedor:** Zodiac Team
