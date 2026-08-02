import { Router, Request, Response } from 'express';
import { config } from '../config';

const router = Router();

router.get('/', (_req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      status: 'healthy',
      version: config.appVersion,
      environment: config.nodeEnv,
      uptime: Math.floor(process.uptime()),
      timestamp: new Date().toISOString(),
    },
  });
});

router.get('/version', (_req: Request, res: Response) => {
  res.json({
    version: process.env.APP_VERSION ?? '1.0.0',
    commitSha: process.env.COMMIT_SHA ?? 'local',
    buildTime: process.env.BUILD_TIME ?? new Date().toISOString(),
  });
});

export { router as healthRouter };
