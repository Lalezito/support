/**
 * Check Revenue Metrics Table Structure
 *
 * Este script verifica la estructura real de la tabla revenue_metrics
 * para entender qué columnas tiene y qué índices necesita.
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

    // Verificar estructura de la tabla revenue_metrics
    console.log('📋 Estructura de la tabla revenue_metrics:');
    const columns = await client.query(`
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'revenue_metrics'
      ORDER BY ordinal_position;
    `);

    console.log(`   Columnas (${columns.rows.length}):`);
    columns.rows.forEach((col, i) => {
      console.log(`   ${i + 1}. ${col.column_name} (${col.data_type}) ${col.is_nullable === 'NO' ? 'NOT NULL' : ''}`);
    });
    console.log('');

    // Verificar índices
    console.log('📋 Índices en revenue_metrics:');
    const indexes = await client.query(`
      SELECT indexname, indexdef
      FROM pg_indexes
      WHERE tablename = 'revenue_metrics'
      ORDER BY indexname;
    `);

    console.log(`   Índices (${indexes.rows.length}):`);
    indexes.rows.forEach((idx, i) => {
      console.log(`   ${i + 1}. ${idx.indexname}`);
      console.log(`      ${idx.indexdef}`);
    });
    console.log('');

    // Verificar si hay datos
    console.log('📋 Datos en revenue_metrics:');
    const count = await client.query(`SELECT COUNT(*) as total FROM revenue_metrics;`);
    console.log(`   Total de registros: ${count.rows[0].total}`);
    console.log('');

    // Conclusión
    console.log('🎯 CONCLUSIÓN:');
    console.log('');

    const hasDateColumn = columns.rows.some(col => col.column_name === 'date');
    const hasMetricDateColumn = columns.rows.some(col => col.column_name === 'metric_date');

    if (hasDateColumn) {
      console.log('✅ La tabla TIENE columna "date"');
      console.log('   → Migration 012 esperada se ejecutó correctamente');
    } else if (hasMetricDateColumn) {
      console.log('❌ La tabla tiene "metric_date" pero NO "date"');
      console.log('   → Esta tabla fue creada por OTRA migration diferente');
      console.log('   → Migration 012 probablemente NO se ha ejecutado');
    } else {
      console.log('❌ La tabla NO tiene ni "date" ni "metric_date"');
    }

    console.log('');
    console.log('📝 PRÓXIMO PASO:');
    if (!hasDateColumn && hasMetricDateColumn) {
      console.log('   La tabla revenue_metrics actual NO es la que migration 012 crea.');
      console.log('   Opciones:');
      console.log('   1. Borrar esta tabla y dejar que migration 012 la cree correctamente');
      console.log('   2. Ignorar migration 012 y usar la tabla existente');
      console.log('   3. Verificar qué migration creó esta tabla');
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