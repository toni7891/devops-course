'use strict';

const { Router } = require('express');
const { add, multiply } = require('../utils/math');

const router = Router();

// POST /math/add   { "a": 2, "b": 3 }  → { "result": 5 }
router.post('/add', (req, res) => {
  const { a, b } = req.body;
  if (a === undefined || b === undefined) {
    return res.status(400).json({ error: 'Both "a" and "b" are required' });
  }
  try {
    res.json({ result: add(Number(a), Number(b)) });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// POST /math/multiply  { "a": 3, "b": 4 }  → { "result": 12 }
router.post('/multiply', (req, res) => {
  const { a, b } = req.body;
  if (a === undefined || b === undefined) {
    return res.status(400).json({ error: 'Both "a" and "b" are required' });
  }
  try {
    res.json({ result: multiply(Number(a), Number(b)) });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;
