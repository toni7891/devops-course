'use strict';

const request = require('supertest');
const app = require('../src/app');

describe('POST /math/add', () => {
  it('adds two numbers', async () => {
    const res = await request(app).post('/math/add').send({ a: 2, b: 3 });
    expect(res.status).toBe(200);
    expect(res.body.result).toBe(5);
  });

  it('returns 400 when a field is missing', async () => {
    const res = await request(app).post('/math/add').send({ a: 2 });
    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/"b"/);
  });
});

describe('POST /math/multiply', () => {
  it('multiplies two numbers', async () => {
    const res = await request(app).post('/math/multiply').send({ a: 3, b: 4 });
    expect(res.status).toBe(200);
    expect(res.body.result).toBe(12);
  });

  it('returns 400 when a field is missing', async () => {
    const res = await request(app).post('/math/multiply').send({ b: 4 });
    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/"a"/);
  });
});
