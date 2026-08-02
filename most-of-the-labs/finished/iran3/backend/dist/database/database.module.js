"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DatabaseModule = exports.DATABASE_POOL = void 0;
const common_1 = require("@nestjs/common");
const pg_1 = require("pg");
exports.DATABASE_POOL = 'DATABASE_POOL';
const pool = new pg_1.Pool({
    host: process.env.DB_HOST || 'localhost',
    port: Number(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME || 'shopflow',
    user: process.env.DB_USER || 'shopuser',
    password: process.env.DB_PASSWORD || 'shoppass',
});
async function connectWithRetry(retries = 10, delay = 3000) {
    const logger = new common_1.Logger('DatabaseModule');
    for (let i = 1; i <= retries; i++) {
        try {
            const client = await pool.connect();
            logger.log('Connected to PostgreSQL');
            client.release();
            return;
        }
        catch {
            logger.warn(`DB not ready, retry ${i}/${retries}...`);
            await new Promise((resolve) => setTimeout(resolve, delay));
        }
    }
    throw new Error('Could not connect to PostgreSQL after retries');
}
async function initDB() {
    const logger = new common_1.Logger('DatabaseModule');
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
let DatabaseModule = class DatabaseModule {
    async onModuleInit() {
        await connectWithRetry();
        await initDB();
    }
};
exports.DatabaseModule = DatabaseModule;
exports.DatabaseModule = DatabaseModule = __decorate([
    (0, common_1.Module)({
        providers: [
            {
                provide: exports.DATABASE_POOL,
                useValue: pool,
            },
        ],
        exports: [exports.DATABASE_POOL],
    })
], DatabaseModule);
//# sourceMappingURL=database.module.js.map