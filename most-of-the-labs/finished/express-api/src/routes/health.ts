import { Router } from 'express';
import mongoose from 'mongoose';
import { config } from '../config/env.js';

const router = Router();

router.get('/', (_req, res) => {
  res.json({ message: 'Hello from student-api!' });
});

router.get('/health', (_req, res) => {
  const ready = mongoose.connection.readyState === 1;
  res.status(ready ? 200 : 503).json({
    status: ready ? 'ok' : 'degraded',
    db: ready ? 'connected' : 'disconnected',
    uptime: Math.floor(process.uptime()),
  });
});

router.get('/version', (_req, res) => {
  res.json({ version: '1.0', commit: config.commitSha });
});

export default router;
