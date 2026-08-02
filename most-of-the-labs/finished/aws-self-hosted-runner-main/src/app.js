'use strict';

const express = require('express');
const logger = require('./logger');
const healthRouter = require('./routes/health');
const mathRouter = require('./routes/math');

const app = express();

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(express.json());

app.use((req, _res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

// ── Routes ────────────────────────────────────────────────────────────────────
app.use('/health', healthRouter);
app.use('/math', mathRouter);

// ── 404 ───────────────────────────────────────────────────────────────────────
app.use((_req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// ── Error handler ─────────────────────────────────────────────────────────────
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  logger.error('Unhandled error', { message: err.message });
  res.status(500).json({ error: 'Internal server error' });
});

module.exports = app;
