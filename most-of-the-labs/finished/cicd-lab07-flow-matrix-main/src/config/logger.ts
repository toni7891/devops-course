import pino from 'pino';
import { config } from './env.js';

export const logger = pino({
  level: config.isTest ? 'silent' : config.logLevel,
  base: { service: 'express-app' },
  transport: config.isProd
    ? undefined
    : { target: 'pino/file', options: { destination: 1 } },
});
