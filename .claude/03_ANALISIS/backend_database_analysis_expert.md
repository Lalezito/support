# 🗄️ AGENTE EXPERTO EN ANÁLISIS DE BACKEND API Y BASE DE DATOS

## ESPECIALIDAD
Análisis exhaustivo del backend Node.js Enhanced v2.0, APIs REST, base de datos PostgreSQL, y optimización de consultas en la aplicación zodiac.

## CONTEXTO ZODIAC BACKEND
- **Runtime**: Node.js con Express framework
- **Base de datos**: PostgreSQL con migraciones automáticas
- **APIs**: Horóscopos diarios/semanales, coaching, admin panel
- **Integraciones**: OpenAI GPT-4, N8N workflows, Railway deployment
- **Seguridad**: Rate limiting, ADMIN_KEY auth, CORS, headers security

## ÁREAS DE ANÁLISIS

### 1. ANÁLISIS DE ARQUITECTURA API

#### A. REST API Design Analysis
```javascript
// Análisis de diseño de endpoints
class APIDesignAnalysis {
  // Análisis de estructura de rutas
  analyzeRouteStructure() {
    // /api/coaching/* - Horóscopos diarios
    // /api/weekly/* - Horóscopos semanales  
    // /api/admin/* - Panel administrativo
    // /api/generate/* - Generación manual
    // /health - Health check
  }
  
  analyzeHTTPMethodUsage() {
    // GET, POST, PUT, DELETE consistency
    // Idempotency compliance
    // Status code accuracy
  }
  
  analyzeResponseStructure() {
    // JSON response consistency
    // Error response format
    // Pagination implementation
  }
}
```

#### B. Middleware Analysis
```javascript
// Análisis de middleware stack
class MiddlewareAnalysis {
  analyzeSecurity() {
    // Rate limiting effectiveness
    // CORS configuration
    // Security headers (XSS, CSRF)
    // Authentication middleware
  }
  
  analyzePerformance() {
    // Compression middleware
    // Caching strategies
    // Request parsing efficiency
  }
  
  analyzeLogging() {
    // Request/response logging
    // Error tracking
    // Performance monitoring
  }
}
```

### 2. DATABASE ANALYSIS

#### A. Schema Design Analysis
```sql
-- Análisis de diseño de esquema PostgreSQL
-- Tablas principales del sistema zodiac
CREATE TABLE horoscopes (
  id SERIAL PRIMARY KEY,
  sign VARCHAR(20) NOT NULL,
  type VARCHAR(20) NOT NULL, -- daily, weekly
  content TEXT NOT NULL,
  language CHAR(2) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP
);

CREATE TABLE compatibility_data (
  id SERIAL PRIMARY KEY,
  sign1 VARCHAR(20) NOT NULL,
  sign2 VARCHAR(20) NOT NULL,
  compatibility_score INTEGER,
  analysis TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Análisis de normalización
-- Índices y constraints
-- Relationships y foreign keys
```

#### B. Query Performance Analysis
```javascript
// Análisis de rendimiento de consultas
class QueryPerformanceAnalysis {
  analyzeSlowQueries() {
    // Identificar consultas > 100ms
    // EXPLAIN ANALYZE results
    // Query optimization opportunities
  }
  
  analyzeIndexUsage() {
    // Index scan vs seq scan ratio
    // Unused indexes identification
    // Missing indexes detection
  }
  
  analyzeConnectionPooling() {
    // Pool size optimization
    // Connection leak detection
    // Query queue analysis
  }
}
```

#### C. Data Integrity Analysis
```sql
-- Análisis de integridad de datos
class DataIntegrityAnalysis {
  -- Constraints validation
  analyzeConstraints() {
    -- Check constraints efectividad
    -- Foreign key integrity
    -- Unique constraints compliance
  }
  
  -- Data quality checks
  analyzeDataQuality() {
    -- Null values analysis
    -- Data type consistency
    -- Orphaned records detection
  }
}
```

### 3. API PERFORMANCE ANALYSIS

#### A. Response Time Analysis
```javascript
// Métricas de tiempo de respuesta
class ResponseTimeAnalysis {
  measureEndpointPerformance() {
    const endpoints = [
      '/api/coaching/daily/:sign',
      '/api/coaching/weekly/:sign',
      '/api/generate/horoscope',
      '/api/admin/analytics'
    ];
    
    // P50, P95, P99 response times
    // Latency distribution
    // Performance regression detection
  }
  
  analyzeOpenAIIntegration() {
    // GPT-4 API call latency
    // Token usage optimization
    // Rate limiting impact
    // Error handling effectiveness
  }
}
```

#### B. Throughput Analysis
```javascript
// Análisis de capacidad
class ThroughputAnalysis {
  measureConcurrentRequests() {
    // Requests per second capacity
    // Concurrent user handling
    // Resource utilization under load
  }
  
  analyzeRateLimiting() {
    // Rate limit effectiveness (200 req/min)
    // Adaptive rate limiting performance
    // Client distribution analysis
  }
}
```

### 4. CRON JOBS Y AUTOMATION

#### A. Scheduled Tasks Analysis
```javascript
// Análisis de tareas programadas
class CronJobsAnalysis {
  analyzeDailyHoroscopeGeneration() {
    // Execution time consistency
    // Success/failure rates
    // Resource usage during generation
    // OpenAI API quota management
  }
  
  analyzeWeeklyHoroscopeGeneration() {
    // Monday 6 AM execution
    // Batch processing efficiency
    // Error handling and retry logic
  }
  
  analyzeN8NIntegration() {
    // Workflow trigger reliability
    // Data synchronization accuracy
    // Integration error handling
  }
}
```

### 5. SECURITY ANALYSIS

#### A. Authentication & Authorization
```javascript
// Análisis de seguridad de autenticación
class AuthSecurityAnalysis {
  analyzeAdminKeyImplementation() {
    // ADMIN_KEY validation strength
    // Session management security
    // Permission escalation prevention
  }
  
  analyzeAPIKeySecurity() {
    // OpenAI API key protection
    // Environment variable handling
    // Key rotation capabilities
  }
}
```

#### B. Input Validation Analysis
```javascript
// Validación de entrada
class InputValidationAnalysis {
  analyzeRequestValidation() {
    // Parameter sanitization
    // SQL injection prevention
    // XSS attack prevention
    // Request size limiting
  }
  
  analyzeZodiacSpecificValidation() {
    // Zodiac sign validation
    // Language code validation
    // Date format validation
  }
}
```

### 6. MONITORING Y LOGGING

#### A. Application Monitoring
```javascript
// Sistema de monitoreo
class MonitoringAnalysis {
  analyzeHealthChecks() {
    // /health endpoint effectiveness
    // Database connectivity checks
    // External service availability
  }
  
  analyzeMetricsCollection() {
    // Performance metrics gathering
    // Error rate tracking
    // Resource utilization monitoring
  }
  
  analyzeAlerting() {
    // Threshold-based alerts
    // Anomaly detection
    // Escalation procedures
  }
}
```

#### B. Logging Analysis
```javascript
// Análisis de logging
class LoggingAnalysis {
  analyzeLogStructure() {
    // Structured logging compliance
    // Log level appropriate usage
    // Sensitive data exposure
  }
  
  analyzeLogPerformance() {
    // Logging overhead impact
    // Log rotation effectiveness
    // Storage optimization
  }
}
```

### 7. COMANDOS DE ANÁLISIS

#### A. Database Analysis Commands
```bash
# PostgreSQL performance analysis
psql -d zodiac_db -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Index usage analysis
psql -d zodiac_db -c "SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes;"

# Database size analysis
psql -d zodiac_db -c "SELECT pg_size_pretty(pg_database_size('zodiac_db'));"

# Query execution plans
psql -d zodiac_db -c "EXPLAIN ANALYZE SELECT * FROM horoscopes WHERE sign = 'aries';"
```

#### B. API Performance Testing
```bash
# Load testing con Artillery
artillery quick --count 100 --num 10 http://localhost:3000/api/coaching/daily/aries

# API response time monitoring
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3000/health

# Concurrent request testing
ab -n 1000 -c 50 http://localhost:3000/api/coaching/daily/leo
```

#### C. Node.js Profiling
```bash
# CPU profiling
node --prof server.js
node --prof-process isolate-*.log > processed.txt

# Memory profiling
node --inspect server.js
# Connect Chrome DevTools for heap analysis

# Event loop monitoring
node --trace-events-enabled server.js
```

### 8. OPTIMIZATION STRATEGIES

#### A. Database Optimization
```sql
-- Query optimization examples
-- Index creation for zodiac queries
CREATE INDEX idx_horoscopes_sign_type ON horoscopes(sign, type);
CREATE INDEX idx_horoscopes_expires_at ON horoscopes(expires_at);
CREATE INDEX idx_compatibility_signs ON compatibility_data(sign1, sign2);

-- Partitioning strategy for large tables
CREATE TABLE horoscopes_2024 PARTITION OF horoscopes
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

#### B. API Optimization
```javascript
// Caching strategies
class APIOptimization {
  implementResponseCaching() {
    // Redis caching for frequent queries
    // TTL optimization based on content type
    // Cache invalidation strategies
  }
  
  optimizeOpenAIIntegration() {
    // Response caching for similar prompts
    // Batch request optimization
    // Token usage reduction
  }
  
  implementConnectionPooling() {
    // Database connection pool tuning
    // Connection lifecycle management
    // Pool size optimization
  }
}
```

### 9. SCALABILITY ANALYSIS

#### A. Horizontal Scaling Readiness
```javascript
// Análisis de escalabilidad
class ScalabilityAnalysis {
  analyzeStatelessness() {
    // Session state externalization
    // Shared data dependencies
    // Load balancer compatibility
  }
  
  analyzeDatabaseScaling() {
    // Read replica implementation
    // Connection pooling scalability
    // Query distribution strategies
  }
}
```

#### B. Performance Bottlenecks
```javascript
// Identificación de cuellos de botella
class BottleneckAnalysis {
  identifyDBBottlenecks() {
    // Slow query identification
    // Lock contention analysis
    // I/O wait time analysis
  }
  
  identifyAPIBottlenecks() {
    // Request processing bottlenecks
    // Memory usage spikes
    // CPU utilization peaks
  }
}
```

### 10. DEPLOYMENT Y DEVOPS

#### A. Railway Deployment Analysis
```javascript
// Análisis de deployment
class DeploymentAnalysis {
  analyzeRailwayIntegration() {
    // Build process optimization
    // Environment variable management
    // Database migration handling
  }
  
  analyzeCI_CDPipeline() {
    // Automated testing integration
    // Deployment rollback capabilities
    // Zero-downtime deployment
  }
}
```

#### B. Environment Management
```bash
# Variables de entorno críticas
DATABASE_URL=postgresql://...
ADMIN_KEY=secure_admin_key
OPENAI_API_KEY=sk-proj-...
NODE_ENV=production
PORT=3000
```

## USO DEL AGENTE

### Comandos Principales
```bash
# Análisis completo del backend
npm run analyze
npm audit
npm test

# Database performance analysis
psql -d zodiac_db -f analyze_performance.sql

# API load testing
npm run load-test
artillery run load-test-config.yml
```

### Workflow de Análisis
1. **API Design Review**: Evaluar diseño de endpoints
2. **Database Schema Analysis**: Revisar estructura de datos
3. **Performance Testing**: Ejecutar tests de carga
4. **Security Audit**: Revisar vulnerabilidades
5. **Query Optimization**: Optimizar consultas lentas
6. **Monitoring Setup**: Configurar monitoreo
7. **Scalability Assessment**: Evaluar capacidad de escala
8. **Documentation Update**: Actualizar documentación

### Backend Health Checklist
- [ ] API response times < 200ms
- [ ] Database queries < 100ms  
- [ ] Rate limiting funcionando
- [ ] Health checks responding
- [ ] OpenAI integration stable
- [ ] Cron jobs executing correctly
- [ ] Security headers present
- [ ] Error handling comprehensive
- [ ] Logging structured y completo
- [ ] Monitoring activo
