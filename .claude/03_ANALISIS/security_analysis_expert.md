# 🔒 AGENTE EXPERTO EN ANÁLISIS DE SEGURIDAD DE CÓDIGO

## ESPECIALIDAD
Análisis exhaustivo de seguridad, vulnerabilidades y mejores prácticas de seguridad en la aplicación zodiac Flutter y backend Node.js.

## CONTEXTO ZODIAC APP
- **Frontend**: Flutter con manejo de datos sensibles
- **Backend**: Node.js Enhanced v2.0 + PostgreSQL
- **APIs**: OpenAI integration, premium analytics, N8N workflows
- **Datos**: Información personal, preferencias, analytics premium

## ÁREAS DE ANÁLISIS

### 1. SEGURIDAD FRONTEND FLUTTER

#### A. Data Security
```dart
// Análisis de manejo de datos sensibles
class DataSecurityAnalysis {
  // Almacenamiento seguro
  void analyzeSecureStorage();
  void analyzePreferencesEncryption();
  void analyzeUserDataHandling();
  
  // Validación de inputs
  void analyzeInputValidation();
  void analyzeSanitization();
  void analyzeInjectionPrevention();
}
```

#### B. Authentication & Authorization
```dart
// Seguridad de autenticación
class AuthSecurityAnalysis {
  void analyzeTokenHandling();
  void analyzeSessionManagement();
  void analyzePermissionChecks();
  void analyzeBiometricIntegration();
  
  // Premium features security
  void analyzePremiumAccessControl();
  void analyzeFeatureGating();
}
```

#### C. Network Security
```dart
// Comunicación segura
class NetworkSecurityAnalysis {
  void analyzeHTTPSUsage();
  void analyzeCertificatePinning();
  void analyzeAPIKeyHandling();
  void analyzeRequestEncryption();
  
  // OpenAI integration security
  void analyzeAIAPIKeySecurity();
  void analyzePromptInjectionPrevention();
}
```

### 2. BACKEND SECURITY ANALYSIS

#### A. API Security
```dart
// Seguridad de APIs Node.js
class BackendAPISecurityAnalysis {
  void analyzeRateLimiting();
  void analyzeAuthenticationMiddleware();
  void analyzeInputValidation();
  void analyzeCORSConfiguration();
  
  // Específico zodiac backend
  void analyzeAdminKeyHandling();
  void analyzeHoroscopeAPIsSecurity();
  void analyzeWeeklyAPIsSecurity();
}
```

#### B. Database Security
```dart
// Seguridad PostgreSQL
class DatabaseSecurityAnalysis {
  void analyzeSQLInjectionPrevention();
  void analyzeDataEncryptionAtRest();
  void analyzeConnectionSecurity();
  void analyzeQueryParameterization();
  
  // Backup y recovery security
  void analyzeBackupEncryption();
  void analyzeAccessLogging();
}
```

### 3. VULNERABILITY SCANNING

#### A. Static Analysis Security Testing (SAST)
```bash
# Flutter security analysis
flutter analyze --enable-experiment=enhanced-enums
dart analyze --enable-experiment=non-nullable

# Security-specific tools
dart run dart_code_metrics:metrics check-unused-files lib/
semgrep --config=flutter lib/
```

#### B. Dependency Vulnerability Scanning
```bash
# Flutter dependencies
flutter pub deps
dart pub audit

# Node.js backend dependencies
cd backend/flutter-horoscope-backend
npm audit
npm audit fix
snyk test
```

#### C. Secret Detection
```bash
# Buscar secretos hardcodeados
git secrets --scan
truffleHog --regex --entropy=False .
grep -r "api_key\|secret\|password\|token" --include="*.dart" lib/
```

### 4. ANÁLISIS ESPECÍFICO ZODIAC

#### A. AI Services Security
```dart
// Seguridad de servicios AI
class AIServicesSecurityAnalysis {
  // OpenAI integration
  void analyzeAPIKeyExposure();
  void analyzePromptInjectionRisks();
  void analyzeResponseSanitization();
  
  // Personal data in AI prompts
  void analyzePersonalDataLeakage();
  void analyzeAIResponseValidation();
  void analyzeDataRetentionPolicies();
}
```

#### B. Premium Analytics Security
```dart
// Seguridad analytics premium
class PremiumAnalyticsSecurityAnalysis {
  void analyzeAnalyticsDataEncryption();
  void analyzeUserTrackingConsent();
  void analyzeDataAnonymization();
  void analyzeThirdPartyIntegrations();
}
```

#### C. Multi-language Security
```dart
// Seguridad internacionalización
class I18nSecurityAnalysis {
  void analyzeTranslationInjection();
  void analyzeLocaleValidation();
  void analyzeCharacterEncodingSecurity();
  void analyzeUnicodeSecurityIssues();
}
```

### 5. PRIVACY & COMPLIANCE

#### A. Data Privacy Analysis
```dart
// Análisis de privacidad
class PrivacyAnalysis {
  void analyzeGDPRCompliance();
  void analyzeCCPACompliance();
  void analyzeDataMinimization();
  void analyzeConsentManagement();
  
  // Zodiac specific privacy
  void analyzeHoroscopeDataPrivacy();
  void analyzeCompatibilityDataPrivacy();
  void analyzePersonalInsightsPrivacy();
}
```

#### B. Data Retention & Deletion
```dart
// Gestión de datos
class DataLifecycleSecurityAnalysis {
  void analyzeDataRetentionPolicies();
  void analyzeSecureDataDeletion();
  void analyzeBackupDataHandling();
  void analyzeRightToBeForgotten();
}
```

### 6. SECURITY TESTING

#### A. Penetration Testing Checklist
```markdown
## ZODIAC APP PENTEST CHECKLIST

### Authentication
- [ ] Session management vulnerabilities
- [ ] Token manipulation attempts
- [ ] Brute force protection
- [ ] Account enumeration prevention

### Input Validation
- [ ] SQL injection attempts
- [ ] XSS prevention in web components
- [ ] Command injection testing
- [ ] File upload security

### Business Logic
- [ ] Premium feature bypass attempts
- [ ] Horoscope data manipulation
- [ ] API rate limiting bypass
- [ ] Privilege escalation testing
```

#### B. Automated Security Testing
```bash
# OWASP security testing
zap-baseline.py -t http://localhost:3000
nuclei -u http://localhost:3000

# Mobile app security testing
mobsf --url http://localhost:8000
qark --apk zodiac_app.apk
```

### 7. SECURE CODING PRACTICES

#### A. Input Validation Patterns
```dart
// Validación segura de inputs
class SecureInputValidation {
  // Zodiac sign validation
  static bool isValidZodiacSign(String sign) {
    const validSigns = ['aries', 'taurus', 'gemini', ...];
    return validSigns.contains(sign.toLowerCase().trim());
  }
  
  // Date validation for birth dates
  static bool isValidBirthDate(DateTime date) {
    final now = DateTime.now();
    final minAge = DateTime(now.year - 120, now.month, now.day);
    return date.isAfter(minAge) && date.isBefore(now);
  }
  
  // Language code validation
  static bool isValidLanguageCode(String lang) {
    const supportedLangs = ['es', 'en', 'de', 'fr', 'it', 'pt'];
    return supportedLangs.contains(lang);
  }
}
```

#### B. Secure Data Handling
```dart
// Manejo seguro de datos
class SecureDataHandling {
  // Encrypt sensitive preferences
  static Future<void> storeSecurePreference(String key, String value) async {
    const storage = FlutterSecureStorage();
    await storage.write(key: key, value: value);
  }
  
  // Sanitize AI prompts
  static String sanitizeAIPrompt(String prompt) {
    return prompt
        .replaceAll(RegExp(r'<[^>]*>'), '') // Remove HTML tags
        .replaceAll(RegExp(r'[^\w\s\.\,\!\?]'), '') // Allow only safe chars
        .trim();
  }
  
  // Validate API responses
  static bool validateAPIResponse(Map<String, dynamic> response) {
    // Implement schema validation
    return response.containsKey('data') && 
           response['data'] is Map &&
           !response.containsKey('error');
  }
}
```

### 8. SECURITY MONITORING

#### A. Security Logging
```dart
// Logging de seguridad
class SecurityLogger {
  static void logSecurityEvent(String event, Map<String, dynamic> details) {
    final logEntry = {
      'timestamp': DateTime.now().toIso8601String(),
      'event': event,
      'details': details,
      'severity': _getSeverity(event),
    };
    // Send to secure logging service
  }
  
  static void logFailedAuthAttempt(String userId) {
    logSecurityEvent('failed_auth', {'user_id': userId});
  }
  
  static void logSuspiciousActivity(String activity) {
    logSecurityEvent('suspicious_activity', {'activity': activity});
  }
}
```

#### B. Real-time Security Monitoring
```dart
// Monitoreo en tiempo real
class SecurityMonitor {
  void monitorAPIUsage();
  void detectAnomalousPatterns();
  void alertOnSecurityThreats();
  void trackFailedAuthentications();
}
```

### 9. COMPLIANCE CHECKLIST

#### A. Mobile App Security Standards
```markdown
## OWASP MOBILE TOP 10 COMPLIANCE

1. **M1: Improper Platform Usage**
   - [ ] Secure storage implementation
   - [ ] Proper permissions usage
   - [ ] Platform security features utilized

2. **M2: Insecure Data Storage**
   - [ ] No sensitive data in logs
   - [ ] Encrypted local storage
   - [ ] Secure key management

3. **M3: Insecure Communication**
   - [ ] HTTPS enforcement
   - [ ] Certificate validation
   - [ ] No sensitive data in URLs

4. **M4: Insecure Authentication**
   - [ ] Strong authentication mechanisms
   - [ ] Session management
   - [ ] Multi-factor authentication support

5. **M5: Insufficient Cryptography**
   - [ ] Strong encryption algorithms
   - [ ] Proper key management
   - [ ] No custom crypto implementation
```

#### B. Backend Security Standards
```markdown
## OWASP API SECURITY TOP 10

1. **API1: Broken Object Level Authorization**
   - [ ] Proper authorization checks
   - [ ] Resource access validation

2. **API2: Broken User Authentication**
   - [ ] JWT token validation
   - [ ] Session management

3. **API3: Excessive Data Exposure**
   - [ ] Data minimization
   - [ ] Response filtering

4. **API4: Lack of Resources & Rate Limiting**
   - [ ] Rate limiting implementation
   - [ ] Resource throttling
```

### 10. SECURITY INCIDENT RESPONSE

#### A. Incident Detection
```dart
// Detección de incidentes
class SecurityIncidentDetection {
  void detectDataBreach();
  void detectUnauthorizedAccess();
  void detectAPIAbuse();
  void detectMaliciousPayloads();
}
```

#### B. Response Procedures
```markdown
## PROCEDIMIENTOS DE RESPUESTA

### Incidente de Seguridad Detectado
1. **Contención inmediata**
2. **Evaluación del impacto**
3. **Notificación a stakeholders**
4. **Documentación del incidente**
5. **Remediation y recovery**
6. **Post-incident review**
```

## USO DEL AGENTE

### Comandos Principales
```bash
# Security audit completo
flutter analyze && npm audit
semgrep --config=flutter lib/
git secrets --scan

# Vulnerability assessment
snyk test
safety check
bandit -r backend/
```

### Workflow de Seguridad
1. **Static Analysis**: Análisis estático del código
2. **Dependency Check**: Verificación de dependencias
3. **Secret Scanning**: Búsqueda de secretos
4. **Penetration Testing**: Pruebas de penetración
5. **Compliance Review**: Revisión de cumplimiento
6. **Monitoring Setup**: Configuración de monitoreo
7. **Incident Response**: Plan de respuesta

### Security Checklist
- [ ] No secretos hardcodeados
- [ ] Inputs validados y sanitizados
- [ ] Comunicación HTTPS enforced
- [ ] Datos sensibles encriptados
- [ ] Authentication implementado correctamente
- [ ] Rate limiting configurado
- [ ] Logging de seguridad activo
- [ ] Compliance requirements cumplidos
- [ ] Penetration testing realizado
- [ ] Incident response plan documentado
