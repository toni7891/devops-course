import {
  Injectable,
  Inject,
  NotFoundException,
  BadRequestException,
  InternalServerErrorException,
  Logger,
} from '@nestjs/common';
import { Pool } from 'pg';
import { DATABASE_POOL } from '../database/database.module';
import { Product } from './product.entity';

@Injectable()
export class ProductsService {
  private readonly logger = new Logger(ProductsService.name);

  constructor(
    @Inject(DATABASE_POOL) private readonly pool: Pool,
  ) {}

  async findAll(): Promise<Product[]> {
    try {
      const { rows } = await this.pool.query<Product>(
        'SELECT * FROM products ORDER BY id',
      );
      return rows;
    } catch (err) {
      this.logger.error('Failed to fetch products', err);
      throw new InternalServerErrorException('Failed to fetch products');
    }
  }

  async findOne(id: number): Promise<Product> {
    try {
      const { rows } = await this.pool.query<Product>(
        'SELECT * FROM products WHERE id = $1',
        [id],
      );
      if (rows.length === 0) {
        throw new NotFoundException('Not found');
      }
      return rows[0];
    } catch (err) {
      if (err instanceof NotFoundException) throw err;
      this.logger.error('Failed to fetch product', err);
      throw new InternalServerErrorException('Failed to fetch product');
    }
  }

  async updateStock(id: number, delta: number): Promise<Product> {
    if (typeof delta !== 'number') {
      throw new BadRequestException('delta must be a number');
    }

    try {
      const { rows } = await this.pool.query<Product>(
        `UPDATE products SET stock = GREATEST(0, stock + $1) WHERE id = $2 RETURNING *`,
        [delta, id],
      );

      if (rows.length === 0) {
        throw new NotFoundException('Not found');
      }

      return rows[0];
    } catch (err) {
      if (
        err instanceof NotFoundException ||
        err instanceof BadRequestException
      ) {
        throw err;
      }
      this.logger.error('Failed to update stock', err);
      throw new InternalServerErrorException('Failed to update stock');
    }
  }
}
