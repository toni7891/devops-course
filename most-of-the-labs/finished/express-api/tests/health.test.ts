import supertest from 'supertest';
import { describe, expect, it } from 'vitest';
import app from '../src/app.js';

const req = supertest(app);

describe('GET /', () => {
  it('returns welcome message', async () => {
    const res = await req.get('/');
    expect(res.status).toBe(200);
    expect(res.body.message).toBe('Hello from student-api!');
  });
});

describe('GET /health', () => {
  it('reports ok when db is connected', async () => {
    const res = await req.get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.db).toBe('connected');
    expect(typeof res.body.uptime).toBe('number');
  });
});

describe('GET /version', () => {
  it('returns version and commit', async () => {
    const res = await req.get('/version');
    expect(res.status).toBe(200);
    expect(res.body.version).toBe('1.0');
    expect(res.body).toHaveProperty('commit');
  });
});
