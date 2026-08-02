import type { Request, Response, NextFunction, RequestHandler } from 'express';
import type { ZodSchema } from 'zod';

type Source = 'body' | 'params' | 'query';

export const validate = (schema: ZodSchema, source: Source = 'body'): RequestHandler =>
  (req: Request, _res: Response, next: NextFunction) => {
    const parsed = schema.safeParse(req[source]);
    if (!parsed.success) return next(parsed.error);
    (req as any)[source] = parsed.data;
    next();
  };
