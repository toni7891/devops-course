import { Pool } from 'pg';
import { Product } from './product.entity';
export declare class ProductsService {
    private readonly pool;
    private readonly logger;
    constructor(pool: Pool);
    findAll(): Promise<Product[]>;
    findOne(id: number): Promise<Product>;
    updateStock(id: number, delta: number): Promise<Product>;
}
