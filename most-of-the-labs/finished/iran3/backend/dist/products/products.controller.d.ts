import { ProductsService } from './products.service';
import { Product } from './product.entity';
export declare class ProductsController {
    private readonly productsService;
    constructor(productsService: ProductsService);
    findAll(): Promise<Product[]>;
    findOne(id: number): Promise<Product>;
    updateStock(id: number, body: {
        delta: number;
    }): Promise<Product>;
}
