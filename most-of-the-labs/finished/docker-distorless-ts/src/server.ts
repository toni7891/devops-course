import express, { Request, Response, NextFunction } from 'express';
import paymentsRouter from './routes/payments';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.use('/payments', paymentsRouter);

// 404
app.use((_req: Request, res: Response) => {
  res.status(404).json({ error: 'Not found' });
});

// Error handler
app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

// Only bind a port when run directly, not when imported by tests.
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Dummy payment system listening on http://localhost:${PORT}`);
  });
}

export default app;
