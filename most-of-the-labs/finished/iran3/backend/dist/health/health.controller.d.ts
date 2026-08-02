import { Response } from 'express';
import { Pool } from 'pg';
export declare class HealthController {
    private readonly pool;
    constructor(pool: Pool);
    getHealth(): {
        status: string;
        timestamp: string;
    };
    getReady(res: Response): Promise<void>;
}
