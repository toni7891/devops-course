"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@nestjs/testing");
const health_controller_1 = require("./health.controller");
const database_module_1 = require("../database/database.module");
const mockPool = { query: jest.fn() };
describe('HealthController', () => {
    let controller;
    beforeEach(async () => {
        const module = await testing_1.Test.createTestingModule({
            controllers: [health_controller_1.HealthController],
            providers: [{ provide: database_module_1.DATABASE_POOL, useValue: mockPool }],
        }).compile();
        controller = module.get(health_controller_1.HealthController);
        jest.clearAllMocks();
    });
    describe('getHealth', () => {
        it('returns status ok with timestamp', () => {
            const result = controller.getHealth();
            expect(result.status).toBe('ok');
            expect(typeof result.timestamp).toBe('string');
        });
    });
    describe('getReady', () => {
        it('returns 200 when db is reachable', async () => {
            mockPool.query.mockResolvedValue({});
            const mockRes = {
                status: jest.fn().mockReturnThis(),
                json: jest.fn(),
            };
            await controller.getReady(mockRes);
            expect(mockRes.status).toHaveBeenCalledWith(200);
            expect(mockRes.json).toHaveBeenCalledWith({ status: 'ready' });
        });
        it('returns 503 when db is unreachable', async () => {
            mockPool.query.mockRejectedValue(new Error('connection refused'));
            const mockRes = {
                status: jest.fn().mockReturnThis(),
                json: jest.fn(),
            };
            await controller.getReady(mockRes);
            expect(mockRes.status).toHaveBeenCalledWith(503);
            expect(mockRes.json).toHaveBeenCalledWith({ status: 'not ready' });
        });
    });
});
//# sourceMappingURL=health.controller.spec.js.map