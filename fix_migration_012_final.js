/**
 * Fix Migration 012 - Final Solution
 *
 * Railway ya tiene tabla revenue_metrics con columna "metric_date".
 * Migration 012 intenta crear su propia versión con columna "date".
 *
 * Solución: Ejecutar solo las partes de migration 012 que SÍ se necesitan,
 * ignorando la tabla revenue_metrics que ya existe.
 */

const { Client } = require('pg');

const DATABASE_URL = process.env.DATABASE_URL || process.env.PGDATABASE_URL;

if (!DATABASE_URL) {
  console.error('❌ ERROR: DATABASE_URL no está configurada');
  process.exit(1);
}

async function main() {
  const client = new Client({
    connectionString: DATABASE_URL,
    ssl: {
      rejectUnauthorized: false
    }
  });

  try {
    console.log('🔄 Conectando a Railway PostgreSQL...');
    await client.connect();
    console.log('✅ Conectado exitosamente');
    console.log('');

    // Paso 1: Crear tablas que faltan (sin revenue_metrics)
    console.log('📋 Paso 1: Creando tablas necesarias...');

    // user_analytics
    await client.query(`
      CREATE TABLE IF NOT EXISTS user_analytics (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        session_id VARCHAR(255),
        session_duration INTEGER,
        feature_name VARCHAR(100),
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log('   ✅ user_analytics');

    // feature_usage
    await client.query(`
      CREATE TABLE IF NOT EXISTS feature_usage (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        feature_name VARCHAR(100) NOT NULL,
        usage_count INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log('   ✅ feature_usage');

    // subscriptions
    await client.query(`
      CREATE TABLE IF NOT EXISTS subscriptions (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        tier VARCHAR(20) NOT NULL,
        amount_paid DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT NOW(),
        expires_at TIMESTAMP,
        updated_at TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log('   ✅ subscriptions');

    // user_events
    await client.query(`
      CREATE TABLE IF NOT EXISTS user_events (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        event_type VARCHAR(100) NOT NULL,
        event_data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log('   ✅ user_events');

    console.log('');

    // Paso 2: Crear migrations table si no existe
    console.log('📋 Paso 2: Preparando tabla de migrations...');

    await client.query(`
      CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        executed_at TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log('   ✅ Tabla migrations existe');
    console.log('');

    // Paso 3: Marcar migration 012 como ejecutada
    console.log('📋 Paso 3: Marcando migration 012 como ejecutada...');

    const result = await client.query(`
      INSERT INTO migrations (name, executed_at)
      VALUES ('012_create_revenue_optimization_tables.sql', NOW())
      ON CONFLICT (name) DO NOTHING
      RETURNING name;
    `);

    if (result.rows.length > 0) {
      console.log('   ✅ Migration 012 marcada como ejecutada por primera vez');
    } else {
      console.log('   ℹ️  Migration 012 ya estaba marcada como ejecutada');
    }
    console.log('');

    // Paso 4: Verificar estado final
    console.log('📋 Paso 4: Verificación final...');

    const migrations = await client.query(`
      SELECT name, executed_at
      FROM migrations
      ORDER BY executed_at DESC
      LIMIT 5;
    `);

    console.log(`   Últimas 5 migrations ejecutadas:`);
    migrations.rows.forEach((m, i) => {
      const date = new Date(m.executed_at).toISOString().split('T')[0];
      console.log(`   ${i + 1}. ${m.name} (${date})`);
    });
    console.log('');

    console.log('🎉 FIX COMPLETADO EXITOSAMENTE');
    console.log('');
    console.log('📋 Próximos pasos:');
    console.log('1. Railway Dashboard → Backend Service');
    console.log('2. CMD + K → "Deploy Latest Commit"');
    console.log('3. Esperar 3-5 minutos');
    console.log('4. Verificar que migrations 012 pase sin errores');
    console.log('5. Probar endpoint de premium tier');
    console.log('');
    console.log('✅ Ahora Railway debería poder desplegar sin errores de migration 012');

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