/**
 * Fix Railway PostgreSQL Migrations - Direct Connection
 *
 * Este script se conecta directamente a Railway PostgreSQL y:
 * 1. Verifica qué migrations están ejecutadas
 * 2. Ejecuta el fix del índice "date" si es necesario
 * 3. Marca la migration 012 como ejecutada
 *
 * Uso: node fix_railway_postgresql_direct.js
 */

const { Client } = require('pg');

// Railway PostgreSQL connection string
// Obtenerla de: Railway → PostgreSQL → Variables → DATABASE_URL
const DATABASE_URL = process.env.DATABASE_URL || process.env.PGDATABASE_URL;

if (!DATABASE_URL) {
  console.error('❌ ERROR: DATABASE_URL no está configurada');
  console.error('');
  console.error('Obtener de Railway:');
  console.error('1. Railway Dashboard → PostgreSQL');
  console.error('2. Variables tab');
  console.error('3. Copiar el valor de DATABASE_URL');
  console.error('4. Ejecutar: export DATABASE_URL="postgresql://..."');
  console.error('5. Ejecutar: node fix_railway_postgresql_direct.js');
  process.exit(1);
}

async function main() {
  const client = new Client({
    connectionString: DATABASE_URL,
    ssl: {
      rejectUnauthorized: false // Railway requiere SSL
    }
  });

  try {
    console.log('🔄 Conectando a Railway PostgreSQL...');
    await client.connect();
    console.log('✅ Conectado exitosamente');
    console.log('');

    // Paso 1: Verificar si existe la tabla migrations
    console.log('📋 Paso 1: Verificando tabla de migrations...');
    const migrationTableCheck = await client.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'migrations'
      );
    `);

    const hasMigrationsTable = migrationTableCheck.rows[0].exists;
    console.log(`   Tabla 'migrations' existe: ${hasMigrationsTable ? '✅ Sí' : '❌ No'}`);
    console.log('');

    if (hasMigrationsTable) {
      // Paso 2: Ver qué migrations están ejecutadas
      console.log('📋 Paso 2: Migrations ejecutadas:');
      const executedMigrations = await client.query(`
        SELECT name, executed_at
        FROM migrations
        ORDER BY executed_at ASC;
      `);

      executedMigrations.rows.forEach((row, index) => {
        console.log(`   ${index + 1}. ${row.name} (${new Date(row.executed_at).toISOString()})`);
      });
      console.log('');

      // Verificar si migration 012 está ejecutada
      const has012 = executedMigrations.rows.some(row =>
        row.name.includes('012') || row.name.includes('revenue_optimization')
      );
      console.log(`   Migration 012 ejecutada: ${has012 ? '✅ Sí' : '❌ No'}`);
      console.log('');
    }

    // Paso 3: Verificar si existe la tabla revenue_metrics
    console.log('📋 Paso 3: Verificando tabla revenue_metrics...');
    const revenueMetricsCheck = await client.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'revenue_metrics'
      );
    `);

    const hasRevenueMetrics = revenueMetricsCheck.rows[0].exists;
    console.log(`   Tabla 'revenue_metrics' existe: ${hasRevenueMetrics ? '✅ Sí' : '❌ No'}`);
    console.log('');

    if (hasRevenueMetrics) {
      // Paso 4: Verificar índices en revenue_metrics
      console.log('📋 Paso 4: Verificando índices en revenue_metrics...');
      const indexes = await client.query(`
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE tablename = 'revenue_metrics'
        ORDER BY indexname;
      `);

      console.log(`   Índices encontrados: ${indexes.rows.length}`);
      indexes.rows.forEach((row, index) => {
        console.log(`   ${index + 1}. ${row.indexname}`);
        console.log(`      ${row.indexdef}`);
      });
      console.log('');
    }

    // Paso 5: FIX - Recrear índice con comillas
    console.log('🔧 Paso 5: Aplicando fix del índice "date"...');

    try {
      // Borrar índice viejo si existe
      await client.query(`DROP INDEX IF EXISTS idx_revenue_metrics_date;`);
      console.log('   ✅ Índice viejo eliminado (si existía)');

      // Crear tabla si no existe
      if (!hasRevenueMetrics) {
        await client.query(`
          CREATE TABLE IF NOT EXISTS revenue_metrics (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL UNIQUE,
            total_users INTEGER DEFAULT 0,
            premium_users INTEGER DEFAULT 0,
            new_users INTEGER DEFAULT 0,
            new_conversions INTEGER DEFAULT 0,
            churned_users INTEGER DEFAULT 0,
            daily_revenue DECIMAL(10, 2) DEFAULT 0,
            avg_revenue_per_user DECIMAL(10, 2) DEFAULT 0,
            conversion_rate DECIMAL(5, 2) DEFAULT 0,
            churn_rate DECIMAL(5, 2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW()
          );
        `);
        console.log('   ✅ Tabla revenue_metrics creada');
      }

      // Crear índice con comillas
      await client.query(`
        CREATE INDEX IF NOT EXISTS idx_revenue_metrics_date
        ON revenue_metrics("date");
      `);
      console.log('   ✅ Índice nuevo creado con comillas: idx_revenue_metrics_date ON revenue_metrics("date")');
      console.log('');
    } catch (error) {
      console.error('   ❌ Error aplicando fix:', error.message);
      console.log('');
    }

    // Paso 6: Marcar migration 012 como ejecutada (si tabla migrations existe)
    if (hasMigrationsTable) {
      console.log('📋 Paso 6: Marcando migration 012 como ejecutada...');

      try {
        await client.query(`
          INSERT INTO migrations (name, executed_at)
          VALUES ('012_create_revenue_optimization_tables.sql', NOW())
          ON CONFLICT (name) DO NOTHING;
        `);
        console.log('   ✅ Migration 012 marcada como ejecutada');
        console.log('');
      } catch (error) {
        console.error('   ❌ Error marcando migration:', error.message);
        console.log('');
      }
    }

    // Paso 7: Verificación final
    console.log('📋 Paso 7: Verificación final...');
    const finalIndexes = await client.query(`
      SELECT indexname, indexdef
      FROM pg_indexes
      WHERE tablename = 'revenue_metrics'
      AND indexname = 'idx_revenue_metrics_date';
    `);

    if (finalIndexes.rows.length > 0) {
      console.log('   ✅ Índice verificado exitosamente:');
      console.log(`      ${finalIndexes.rows[0].indexdef}`);
      console.log('');
      console.log('🎉 FIX COMPLETADO EXITOSAMENTE');
      console.log('');
      console.log('📋 Próximos pasos:');
      console.log('1. Railway Dashboard → Backend Service');
      console.log('2. CMD + K → "Deploy Latest Commit"');
      console.log('3. Esperar 3-5 minutos');
      console.log('4. Verificar que el backend acepte premiumTier sin receiptData');
    } else {
      console.log('   ❌ El índice no se creó correctamente');
      console.log('');
      console.log('Revisar errores arriba.');
    }

  } catch (error) {
    console.error('❌ ERROR:', error.message);
    console.error('');
    console.error('Stack trace:', error.stack);
    process.exit(1);
  } finally {
    await client.end();
    console.log('');
    console.log('🔌 Conexión cerrada');
  }
}

main();