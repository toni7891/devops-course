'use strict';

const { env } = require('./config');

const LEVELS = { error: 0, warn: 1, info: 2, debug: 3 };
const currentLevel = env === 'test' ? LEVELS.warn : LEVELS.debug;

function log(level, message, meta = {}) {
  if (LEVELS[level] > currentLevel) return;
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...(Object.keys(meta).length ? { meta } : {}),
  };
  const out = level === 'error' ? process.stderr : process.stdout;
  out.write(JSON.stringify(entry) + '\n');
}

const logger = {
  error: (msg, meta) => log('error', msg, meta),
  warn: (msg, meta) => log('warn', msg, meta),
  info: (msg, meta) => log('info', msg, meta),
  debug: (msg, meta) => log('debug', msg, meta),
};

module.exports = logger;
