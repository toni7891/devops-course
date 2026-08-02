import { Router } from 'express';

const router = Router();
const startedAt = Date.now();

router.get('/livez', (_req, res) => res.json({ status: 'ok' }));
router.get('/readyz', (_req, res) => res.json({ status: 'ready', uptimeMs: Date.now() - startedAt }));

export default router;
