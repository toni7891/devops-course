import { Controller, Get, Inject, Res, HttpStatus } from '@nestjs/common';
import { Response } from 'express';
import { Pool } from 'pg';
import { DATABASE_POOL } from '../database/database.module';

@Controller()
export class HealthController {
  constructor(@Inject(DATABASE_POOL) private readonly pool: Pool) {}

  @Get('health')
  getHealth(): { status: string; timestamp: string } {
    return { status: 'ok', timestamp: new Date().toISOString() };
  }

  @Get('ready')
  async getReady(@Res() res: Response): Promise<void> {
    try {
      await this.pool.query('SELECT 1');
      res.status(HttpStatus.OK).json({ status: 'ready' });
    } catch {
      res.status(HttpStatus.SERVICE_UNAVAILABLE).json({ status: 'not ready' });
    }
  }
}
