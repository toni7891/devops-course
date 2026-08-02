import type { Request, Response, NextFunction, ErrorRequestHandler, RequestHandler } from 'express';
import { ZodError } from 'zod';
import { HttpError } from '../errors/HttpError.js';
import { logger } from '../config/logger.js';

export const notFoundHandler: RequestHandler = (req, _res, next) => {
  next(HttpError.notFound(`Route ${req.method} ${req.originalUrl} not found`));
};

export const errorHandler: ErrorRequestHandler = (err: unknown, _req: Request, res: Response, _next: NextFunction) => {
  if (err instanceof ZodError) {
    return res.status(400).json({
      error: 'ValidationError',
      message: 'Invalid request payload',
      details: err.flatten(),
    });
  }
  if (err instanceof HttpError) {
    return res.status(err.status).json({
      error: err.constructor.name,
      message: err.message,
      ...(err.details ? { details: err.details } : {}),
    });
  }
  logger.error({ err }, 'Unhandled error');
  res.status(500).json({ error: 'InternalServerError', message: 'Something went wrong' });
};
