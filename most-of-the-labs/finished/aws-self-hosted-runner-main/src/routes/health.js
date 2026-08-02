'use strict';

const { Router } = require('express');
const { getMachineInfo } = require('../utils/system');
const config = require('../config');

const router = Router();

// GET /health — liveness probe
router.get('/', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// GET /health/ready — readiness probe (add real checks here as the app grows)
router.get('/ready', (_req, res) => {
  res.json({ status: 'ready' });
});

// GET /health/info — system + app metadata
router.get('/info', (_req, res) => {
  res.json({
    app: config.appName,
    version: config.version,
    env: config.env,
    machine: getMachineInfo(),
  });
});

module.exports = router;
