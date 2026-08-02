"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const products_controller_1 = require("./products.controller");
const products_service_1 = require("./products.service");
const common_1 = require("@nestjs/common");
const mockProduct = {
    id: 1,
    name: 'Widget',
    price: '9.99',
    stock: 10,
    created_at: new Date(),
};
const mockService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    updateStock: jest.fn(),
};
describe('ProductsController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [products_controller_1.ProductsController],
            providers: [{ provide: products_service_1.ProductsService, useValue: mockService }],
        }).compile();
        controller = module.get(products_controller_1.ProductsController);
        jest.clearAllMocks();
    });
    describe('findAll', () => {
        it('delegates to service and returns result', async () => {
            const payload = { source: 'db', data: [mockProduct] };
            mockService.findAll.mockResolvedValue(payload);
            const result = await controller.findAll();
            expect(result).toEqual(payload);
            expect(mockService.findAll).toHaveBeenCalledTimes(1);
        });
    });
    describe('findOne', () => {
        it('returns product for valid id', async () => {
            mockService.findOne.mockResolvedValue(mockProduct);
            const result = await controller.findOne(1);
            expect(result).toEqual(mockProduct);
            expect(mockService.findOne).toHaveBeenCalledWith(1);
        });
        it('propagates NotFoundException from service', async () => {
            mockService.findOne.mockRejectedValue(new common_1.NotFoundException());
            await expect(controller.findOne(999)).rejects.toThrow(common_1.NotFoundException);
        });
    });
    describe('updateStock', () => {
        it('calls service with id and delta', async () => {
            const updated = { ...mockProduct, stock: 9 };
            mockService.updateStock.mockResolvedValue(updated);
            const result = await controller.updateStock(1, { delta: -1 });
            expect(result.stock).toBe(9);
            expect(mockService.updateStock).toHaveBeenCalledWith(1, -1);
        });
    });
});
//# sourceMappingURL=products.controller.spec.js.map