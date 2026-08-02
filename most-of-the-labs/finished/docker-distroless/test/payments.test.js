'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const app = require('../src/server');

let server;
let base;

test.before(async () => {
  await new Promise((resolve) => {
    server = app.listen(0, () => {
      base = `http://localhost:${server.address().port}`;
      resolve();
    });
  });
});

test.after(() => server.close());

const post = (path, body) =>
  fetch(base + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

test('health returns ok', async () => {
  const res = await fetch(base + '/health');
  assert.equal(res.status, 200);
  const json = await res.json();
  assert.equal(json.status, 'ok');
});

test('create payment approved for even-ending card', async () => {
  const res = await post('/payments', { amount: 49.99, card: '4242424242424242' });
  assert.equal(res.status, 201);
  const json = await res.json();
  assert.equal(json.status, 'approved');
  assert.equal(json.cardLast4, '4242');
  assert.equal(json.currency, 'USD');
  assert.ok(json.id);
});

test('create payment declined for odd-ending card', async () => {
  const res = await post('/payments', { amount: 10, card: '4111111111111111' });
  assert.equal(res.status, 201);
  assert.equal((await res.json()).status, 'declined');
});

test('create rejects invalid amount', async () => {
  const res = await post('/payments', { amount: -5, card: '4242424242424242' });
  assert.equal(res.status, 400);
});

test('create rejects missing card', async () => {
  const res = await post('/payments', { amount: 5 });
  assert.equal(res.status, 400);
});

test('get payment by id', async () => {
  const created = await (await post('/payments', { amount: 20, card: '4000000000000002' })).json();
  const res = await fetch(`${base}/payments/${created.id}`);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).id, created.id);
});

test('get unknown payment returns 404', async () => {
  const res = await fetch(base + '/payments/does-not-exist');
  assert.equal(res.status, 404);
});

test('list returns array', async () => {
  const res = await fetch(base + '/payments');
  assert.equal(res.status, 200);
  assert.ok(Array.isArray(await res.json()));
});

test('refund approved payment succeeds', async () => {
  const created = await (await post('/payments', { amount: 30, card: '4000000000000008' })).json();
  assert.equal(created.status, 'approved');
  const res = await post(`/payments/${created.id}/refund`);
  assert.equal(res.status, 200);
  const json = await res.json();
  assert.equal(json.status, 'refunded');
  assert.equal(json.refunded, true);
});

test('double refund rejected', async () => {
  const created = await (await post('/payments', { amount: 30, card: '4000000000000008' })).json();
  await post(`/payments/${created.id}/refund`);
  const res = await post(`/payments/${created.id}/refund`);
  assert.equal(res.status, 409);
});

test('refund declined payment rejected', async () => {
  const created = await (await post('/payments', { amount: 30, card: '4111111111111111' })).json();
  assert.equal(created.status, 'declined');
  const res = await post(`/payments/${created.id}/refund`);
  assert.equal(res.status, 409);
});

test('refund unknown payment returns 404', async () => {
  const res = await post('/payments/does-not-exist/refund');
  assert.equal(res.status, 404);
});
