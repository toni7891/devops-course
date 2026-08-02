import request from 'supertest';
import { app } from '../src/app';

describe('GET /health', () => {
  it('should return 200 with healthy status', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.status).toBe('healthy');
  });

  it('should include version and environment fields', async () => {
    const res = await request(app).get('/health');
    expect(res.body.data).toHaveProperty('version');
    expect(res.body.data).toHaveProperty('environment');
    expect(res.body.data).toHaveProperty('uptime');
    expect(res.body.data).toHaveProperty('timestamp');
  });
});

describe('GET /health/version', () => {
  it('should return 200', async () => {
    const res = await request(app).get('/health/version');
    expect(res.status).toBe(200);
  });

  it('should return version, commitSha, buildTime fields', async () => {
    const res = await request(app).get('/health/version');
    expect(res.body).toHaveProperty('version');
    expect(res.body).toHaveProperty('commitSha');
    expect(res.body).toHaveProperty('buildTime');
  });
});
