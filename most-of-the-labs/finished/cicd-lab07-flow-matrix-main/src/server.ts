import { createApp } from './app.js';
import { config } from './config/env.js';
import { logger } from './config/logger.js';

const app = createApp();
const server = app.listen(config.port, () => {
  logger.info(`Listening on http://localhost:${config.port} [${config.nodeEnv}]`);
});

const shutdown = (signal: string) => {
  logger.info(`${signal} received, shutting down`);
  server.close((err) => {
    if (err) {
      logger.error({ err }, 'Error during shutdown');
      process.exit(1);
    }
    process.exit(0);
  });
  setTimeout(() => {
    logger.warn('Forced exit after timeout');
    process.exit(1);
  }, 10_000).unref();
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('unhandledRejection', (reason) => logger.error({ reason }, 'Unhandled rejection'));
process.on('uncaughtException', (err) => {
  logger.fatal({ err }, 'Uncaught exception');
  process.exit(1);
});
