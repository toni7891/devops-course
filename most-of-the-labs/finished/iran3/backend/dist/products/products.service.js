"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var ProductsService_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProductsService = void 0;
const common_1 = require("@nestjs/common");
const pg_1 = require("pg");
const database_module_1 = require("../database/database.module");
let ProductsService = ProductsService_1 = class ProductsService {
    constructor(pool) {
        this.pool = pool;
        this.logger = new common_1.Logger(ProductsService_1.name);
    }
    async findAll() {
        try {
            const { rows } = await this.pool.query('SELECT * FROM products ORDER BY id');
            return rows;
        }
        catch (err) {
            this.logger.error('Failed to fetch products', err);
            throw new common_1.InternalServerErrorException('Failed to fetch products');
        }
    }
    async findOne(id) {
        try {
            const { rows } = await this.pool.query('SELECT * FROM products WHERE id = $1', [id]);
            if (rows.length === 0) {
                throw new common_1.NotFoundException('Not found');
            }
            return rows[0];
        }
        catch (err) {
            if (err instanceof common_1.NotFoundException)
                throw err;
            this.logger.error('Failed to fetch product', err);
            throw new common_1.InternalServerErrorException('Failed to fetch product');
        }
    }
    async updateStock(id, delta) {
        if (typeof delta !== 'number') {
            throw new common_1.BadRequestException('delta must be a number');
        }
        try {
            const { rows } = await this.pool.query(`UPDATE products SET stock = GREATEST(0, stock + $1) WHERE id = $2 RETURNING *`, [delta, id]);
            if (rows.length === 0) {
                throw new common_1.NotFoundException('Not found');
            }
            return rows[0];
        }
        catch (err) {
            if (err instanceof common_1.NotFoundException ||
                err instanceof common_1.BadRequestException) {
                throw err;
            }
            this.logger.error('Failed to update stock', err);
            throw new common_1.InternalServerErrorException('Failed to update stock');
        }
    }
};
exports.ProductsService = ProductsService;
exports.ProductsService = ProductsService = ProductsService_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, common_1.Inject)(database_module_1.DATABASE_POOL)),
    __metadata("design:paramtypes", [pg_1.Pool])
], ProductsService);
//# sourceMappingURL=products.service.js.map