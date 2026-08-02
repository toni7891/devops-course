import { Router } from 'express';
import healthRouter from './health.js';
import itemsRouter from './items.js';

const router = Router();
router.use('/', healthRouter);
router.use('/items', itemsRouter);
export default router;
