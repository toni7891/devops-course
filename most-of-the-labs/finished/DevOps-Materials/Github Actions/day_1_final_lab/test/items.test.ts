import request from 'supertest';
import { app } from '../src/app';

describe('GET /api/items', () => {
  it('should return all items', async () => {
    const res = await request(app).get('/api/items');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.total).toBeGreaterThan(0);
  });
});

describe('GET /api/items/:id', () => {
  it('should return a single item by id', async () => {
    const res = await request(app).get('/api/items/1');
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.id).toBe(1);
  });

  it('should return 404 for non-existent item', async () => {
    const res = await request(app).get('/api/items/9999');
    expect(res.status).toBe(404);
    expect(res.body.success).toBe(false);
  });

  it('should return 400 for invalid id format', async () => {
    const res = await request(app).get('/api/items/not-a-number');
    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });
});

describe('POST /api/items', () => {
  it('should create a new item', async () => {
    const res = await request(app)
      .post('/api/items')
      .send({ name: 'Test Item' })
      .set('Content-Type', 'application/json');

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.name).toBe('Test Item');
    expect(res.body.data.status).toBe('active');
  });

  it('should return 400 when name is missing', async () => {
    const res = await request(app)
      .post('/api/items')
      .send({})
      .set('Content-Type', 'application/json');

    expect(res.status).toBe(400);
    expect(res.body.success).toBe(false);
  });

  it('should create item with inactive status', async () => {
    const res = await request(app)
      .post('/api/items')
      .send({ name: 'Inactive Item', status: 'inactive' })
      .set('Content-Type', 'application/json');

    expect(res.status).toBe(201);
    expect(res.body.data.status).toBe('inactive');
  });
});

describe('404 handler', () => {
  it('should return 404 for unknown routes', async () => {
    const res = await request(app).get('/api/nonexistent');
    expect(res.status).toBe(404);
    expect(res.body.success).toBe(false);
  });
});
