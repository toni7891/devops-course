import supertest from 'supertest';
import { describe, expect, it } from 'vitest';
import app from '../src/app.js';

const req = supertest(app);

describe('GET /items', () => {
  it('returns empty array initially', async () => {
    const res = await req.get('/items');
    expect(res.status).toBe(200);
    expect(res.body).toEqual([]);
  });
});

describe('POST /items', () => {
  it('creates a new item', async () => {
    const res = await req
      .post('/items')
      .send({ name: 'Widget', description: 'A useful widget' });
    expect(res.status).toBe(201);
    expect(res.body.name).toBe('Widget');
    expect(res.body._id).toBeDefined();
  });

  it('rejects items without a name', async () => {
    const res = await req.post('/items').send({ description: 'No name' });
    expect(res.status).toBe(400);
  });
});

describe('GET /items/:id', () => {
  it('returns an item by id', async () => {
    const created = await req.post('/items').send({ name: 'FindMe' });
    const res = await req.get(`/items/${created.body._id}`);
    expect(res.status).toBe(200);
    expect(res.body.name).toBe('FindMe');
  });

  it('returns 404 for an unknown id', async () => {
    const res = await req.get('/items/000000000000000000000000');
    expect(res.status).toBe(404);
  });
});

describe('PUT /items/:id', () => {
  it('updates an item', async () => {
    const created = await req.post('/items').send({ name: 'Before' });
    const res = await req
      .put(`/items/${created.body._id}`)
      .send({ name: 'After' });
    expect(res.status).toBe(200);
    expect(res.body.name).toBe('After');
  });
});

describe('DELETE /items/:id', () => {
  it('deletes an item and returns 204', async () => {
    const created = await req.post('/items').send({ name: 'Ephemeral' });
    const del = await req.delete(`/items/${created.body._id}`);
    expect(del.status).toBe(204);
    const get = await req.get(`/items/${created.body._id}`);
    expect(get.status).toBe(404);
  });
});
