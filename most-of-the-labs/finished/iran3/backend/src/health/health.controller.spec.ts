import { Test, TestingModule } from '@nestjs/testing';
import { HealthController } from './health.controller';
import { DATABASE_POOL } from '../database/database.module';

const mockPool = { query: jest.fn() };

describe('HealthController', () => {
  let controller: HealthController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [HealthController],
      providers: [{ provide: DATABASE_POOL, useValue: mockPool }],
    }).compile();

    controller = module.get<HealthController>(HealthController);
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

      await controller.getReady(mockRes as any);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({ status: 'ready' });
    });

    it('returns 503 when db is unreachable', async () => {
      mockPool.query.mockRejectedValue(new Error('connection refused'));
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn(),
      };

      await controller.getReady(mockRes as any);

      expect(mockRes.status).toHaveBeenCalledWith(503);
      expect(mockRes.json).toHaveBeenCalledWith({ status: 'not ready' });
    });
  });
});
