'use strict';

const app = require('./app');
const config = require('./config');
const logger = require('./logger');

const server = app.listen(config.port, () => {
  logger.info(`${config.appName} v${config.version} listening`, {
    port: config.port,
    env: config.env,
  });
});

// Graceful shutdown
function shutdown(signal) {
  logger.info(`Received ${signal}, shutting down…`);
  server.close(() => {
    logger.info('Server closed');
    process.exit(0);
  });
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
