'use strict';

const request = require('supertest');
const app = require('../src/app');

describe('GET /health', () => {
  it('returns 200 and status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(typeof res.body.uptime).toBe('number');
  });
});

describe('GET /health/ready', () => {
  it('returns 200 and status ready', async () => {
    const res = await request(app).get('/health/ready');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ready');
  });
});

describe('GET /health/info', () => {
  it('returns app metadata and machine info', async () => {
    const res = await request(app).get('/health/info');
    expect(res.status).toBe(200);
    expect(res.body.app).toBe('aws-self-hosted-runner');
    expect(res.body.machine).toHaveProperty('hostname');
    expect(res.body.machine).toHaveProperty('nodeVersion');
  });
});

describe('404', () => {
  it('returns 404 for unknown routes', async () => {
    const res = await request(app).get('/does-not-exist');
    expect(res.status).toBe(404);
    expect(res.body.error).toBe('Not found');
  });
});
