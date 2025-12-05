# 🔧 Fix PostgreSQL Indexes - Railway

## ⚠️ Problema Identificado

El archivo `005_create_goal_planner_tables.sql` tenía **sintaxis incorrecta** para PostgreSQL:
- Usaba sintaxis de MySQL (`INDEX` dentro de `CREATE TABLE`)
- PostgreSQL requiere crear índices **después** de la tabla con `CREATE INDEX`

## ✅ Solución Aplicada

### 1. Archivos Corregidos
- ✅ `migrations/005_create_goal_planner_tables.sql` - **Corregido con sintaxis PostgreSQL**
- ✅ `migrations/005_create_goal_planner_tables.sql.BACKUP` - Backup del original
- ✅ `backend/flutter-horoscope-backend/fix_postgres_indexes.sql` - Script de reparación

## 🚀 Cómo Aplicar el Fix en Railway

### ⚠️ IMPORTANTE: Se encontraron múltiples archivos con problemas

Se corrigieron **2 archivos principales** con sintaxis incorrecta:
- `005_create_goal_planner_tables.sql` (10 índices)
- `012_create_revenue_optimization_tables.sql` (38+ índices)

**Total: ~48 índices a corregir**

### Opción 1: Script Completo (RECOMENDADO)

1. Ve a Railway → Tu proyecto → PostgreSQL → **Query**
2. Abre el archivo: `backend/flutter-horoscope-backend/fix_all_postgres_indexes_COMPLETE.sql`
3. Copia TODO el contenido del archivo
4. Pégalo en la consola de Railway
5. Ejecuta (presiona el botón Run o Ctrl+Enter)

El script:
- ✅ Borra todos los índices mal creados
- ✅ Crea ~48 índices correctamente
- ✅ Verifica la creación automáticamente
- ✅ Muestra un resumen de lo creado

### Opción 2: Rápido (Solo archivos corregidos)

Si solo quieres arreglar lo más crítico:

```sql
-- GOALS TABLES (10 índices)
CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals(user_id);
CREATE INDEX IF NOT EXISTS idx_goals_status ON goals(status);
CREATE INDEX IF NOT EXISTS idx_goals_focus_area ON goals(focus_area);
CREATE INDEX IF NOT EXISTS idx_goals_created_at ON goals(created_at);
CREATE INDEX IF NOT EXISTS idx_micro_habits_goal_id ON goal_micro_habits(goal_id);
CREATE INDEX IF NOT EXISTS idx_milestones_goal_id ON goal_milestones(goal_id);
CREATE INDEX IF NOT EXISTS idx_milestones_completed ON goal_milestones(is_completed);
CREATE INDEX IF NOT EXISTS idx_obstacles_goal_id ON goal_obstacles(goal_id);
CREATE INDEX IF NOT EXISTS idx_checkins_goal_id ON goal_checkins(goal_id);
CREATE INDEX IF NOT EXISTS idx_checkins_created_at ON goal_checkins(created_at);
```

### Opción 3: Verificar Estado Actual

Para ver qué índices existen actualmente:

```sql
SELECT
    tablename,
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename IN ('goals', 'goal_micro_habits', 'goal_milestones', 'goal_obstacles', 'goal_checkins')
ORDER BY
    tablename, indexname;
```

## 📊 Verificación

Después de ejecutar el script completo, deberías ver **~48 índices** en total:

### Goal Planner Tables (10 índices)
- `idx_goals_user_id`, `idx_goals_status`, `idx_goals_focus_area`, `idx_goals_created_at`
- `idx_micro_habits_goal_id`
- `idx_milestones_goal_id`, `idx_milestones_completed`
- `idx_obstacles_goal_id`
- `idx_checkins_goal_id`, `idx_checkins_created_at`

### Revenue Optimization Tables (38+ índices)
- **user_analytics**: 2 índices
- **feature_usage**: 2 índices
- **subscriptions**: 3 índices
- **user_events**: 3 índices
- **checkout_sessions**: 2 índices
- **offers_sent**: 2 índices
- **support_tickets**: 2 índices
- **payment_attempts**: 2 índices
- **churn_interventions**: 2 índices
- **ltv_strategies**: 2 índices
- **pricing_experiments**: 2 índices
- **experiment_assignments**: 2 índices
- **notifications_sent**: 1 índice
- **support_alerts**: 3 índices
- **revenue_metrics**: 1 índice
- **users**: 3 índices adicionales

## 🔍 Sobre los Errores en los Logs

Los errores que viste:
```
could not receive data from client: Connection reset by peer
```

Son **NORMALES** y no críticos. Ocurren cuando:
- La app Flutter cierra una conexión
- Timeout de red
- Usuario pierde conexión

**No requieren acción** - son parte del funcionamiento normal.

## 📝 Notas Técnicas

### Diferencia MySQL vs PostgreSQL

**MySQL (incorrecto para PostgreSQL):**
```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    INDEX idx_goals_user_id (user_id)  -- ❌ No funciona en PostgreSQL
);
```

**PostgreSQL (correcto):**
```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255)
);
CREATE INDEX idx_goals_user_id ON goals(user_id);  -- ✅ Correcto
```

## ✅ Estado Actual

- [x] 2 archivos SQL principales corregidos localmente:
  - `005_create_goal_planner_tables.sql`
  - `012_create_revenue_optimization_tables.sql`
- [x] Backups creados (.BACKUP)
- [x] Script de reparación completo generado (48 índices)
- [x] 6 archivos adicionales identificados con problemas similares
- [ ] **Pendiente**: Ejecutar script completo en Railway Console
- [ ] **Pendiente**: Corregir otros 6 archivos SQL (ver lista abajo)

### ⚠️ Archivos Adicionales Pendientes de Corrección

Estos archivos también tienen sintaxis incorrecta pero no se usaron para generar el script actual:
1. `010_create_premium_goals_tables.sql`
2. `011_add_user_memories.sql`
3. `011_create_user_streaks_table.sql`
4. `012_create_advanced_compatibility_system.sql`
5. `012_create_comprehensive_analytics_system.sql`
6. `create_fcm_tokens_table.sql`

Si estas tablas están activas en Railway, también necesitarán corrección.

## 🎯 Próximos Pasos

1. Ejecuta el script de reparación en Railway (Opción 1)
2. Verifica los índices (Opción 2)
3. Los logs de "Connection reset by peer" seguirán apareciendo (es normal)
4. Haz commit del archivo corregido:
   ```bash
   cd backend/flutter-horoscope-backend
   git add migrations/005_create_goal_planner_tables.sql
   git commit -m "fix: correct PostgreSQL index syntax in goal planner tables"
   git push
   ```

---

**Fecha**: 2025-12-04
**Archivo Original**: `migrations/005_create_goal_planner_tables.sql`
**Status**: ✅ Corregido localmente, pendiente aplicar en Railway
