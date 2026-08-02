import express from 'express';
import { requestLogger } from './middleware/requestLogger';
import { errorHandler } from './middleware/errorHandler';
import { notFound } from './middleware/notFound';
import { healthRouter } from './routes/health';
import { itemsRouter } from './routes/items';

const app = express();

// Body parsing
app.use(express.json());

// Request logging
app.use(requestLogger);

// Routes
app.use('/health', healthRouter);
app.use('/api/items', itemsRouter);

// 404 handler — must come after all routes
app.use(notFound);

// Error handler — must be last
app.use(errorHandler);

export { app };
