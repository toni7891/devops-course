import { Module, OnModuleInit, Logger } from '@nestjs/common';
import { Pool } from 'pg';

export const DATABASE_POOL = 'DATABASE_POOL';

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: Number(process.env.DB_PORT) || 5432,
  database: process.env.DB_NAME || 'shopflow',
  user: process.env.DB_USER || 'shopuser',
  password: process.env.DB_PASSWORD || 'shoppass',
});

async function connectWithRetry(retries = 10, delay = 3000): Promise<void> {
  const logger = new Logger('DatabaseModule');
  for (let i = 1; i <= retries; i++) {
    try {
      const client = await pool.connect();
      logger.log('Connected to PostgreSQL');
      client.release();
      return;
    } catch {
      logger.warn(`DB not ready, retry ${i}/${retries}...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
  throw new Error('Could not connect to PostgreSQL after retries');
}

async function initDB(): Promise<void> {
  const logger = new Logger('DatabaseModule');
  await pool.query(`
    CREATE TABLE IF NOT EXISTS products (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      price NUMERIC(10,2) NOT NULL,
      stock INTEGER NOT NULL DEFAULT 0,
      created_at TIMESTAMP DEFAULT NOW()
    );
  `);
  const { rowCount } = await pool.query('SELECT 1 FROM products LIMIT 1');
  if (rowCount === 0) {
    await pool.query(`
      INSERT INTO products (name, price, stock) VALUES
        ('Laptop Pro 15"',   1299.99, 42),
        ('Wireless Mouse',      29.99, 150),
        ('USB-C Hub 7-in-1',    49.99, 88),
        ('Mechanical Keyboard', 89.99, 60),
        ('4K Monitor 27"',     399.99, 25);
    `);
    logger.log('Seeded products table');
  }
}

@Module({
  providers: [
    {
      provide: DATABASE_POOL,
      useValue: pool,
    },
  ],
  exports: [DATABASE_POOL],
})
export class DatabaseModule implements OnModuleInit {
  async onModuleInit(): Promise<void> {
    await connectWithRetry();
    await initDB();
  }
}
