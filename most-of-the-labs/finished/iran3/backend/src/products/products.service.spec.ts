import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException, BadRequestException } from '@nestjs/common';
import { ProductsService } from './products.service';
import { DATABASE_POOL } from '../database/database.module';

const mockProduct = {
  id: 1,
  name: 'Widget',
  price: '9.99',
  stock: 10,
  created_at: '2026-06-08T00:00:00.000Z',
};

const mockPool = {
  query: jest.fn(),
};

describe('ProductsService', () => {
  let service: ProductsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProductsService,
        { provide: DATABASE_POOL, useValue: mockPool },
      ],
    }).compile();

    service = module.get<ProductsService>(ProductsService);
    jest.clearAllMocks();
  });

  describe('findAll', () => {
    it('returns all products from db', async () => {
      mockPool.query.mockResolvedValue({ rows: [mockProduct] });

      const result = await service.findAll();

      expect(result).toEqual([mockProduct]);
      expect(mockPool.query).toHaveBeenCalledWith(
        'SELECT * FROM products ORDER BY id',
      );
    });
  });

  describe('findOne', () => {
    it('returns product by id', async () => {
      mockPool.query.mockResolvedValue({ rows: [mockProduct] });

      const result = await service.findOne(1);
      expect(result).toEqual(mockProduct);
      expect(mockPool.query).toHaveBeenCalledWith(
        'SELECT * FROM products WHERE id = $1',
        [1],
      );
    });

    it('throws NotFoundException when product not found', async () => {
      mockPool.query.mockResolvedValue({ rows: [] });

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('updateStock', () => {
    it('updates stock and returns updated product', async () => {
      const updated = { ...mockProduct, stock: 9 };
      mockPool.query.mockResolvedValue({ rows: [updated] });

      const result = await service.updateStock(1, -1);

      expect(result.stock).toBe(9);
    });

    it('throws NotFoundException when product not found', async () => {
      mockPool.query.mockResolvedValue({ rows: [] });

      await expect(service.updateStock(999, -1)).rejects.toThrow(
        NotFoundException,
      );
    });

    it('throws BadRequestException when delta is not a number', async () => {
      await expect(
        service.updateStock(1, 'bad' as unknown as number),
      ).rejects.toThrow(BadRequestException);
    });
  });
});
