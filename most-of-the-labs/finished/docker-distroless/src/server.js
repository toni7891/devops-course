'use strict';

const express = require('express');
const paymentsRouter = require('./routes/payments');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.use('/payments', paymentsRouter);

// 404
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

// Only bind a port when run directly, not when imported by tests.
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Dummy payment system listening on http://localhost:${PORT}`);
  });
}

module.exports = app;
