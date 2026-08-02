import request from 'supertest';
import { createApp } from '../src/app.js';
import { userStore } from '../src/modules/users/user.store.js';

const app = createApp();

beforeEach(() => userStore._reset());

describe('Health', () => {
  test('GET /livez', async () => {
    const res = await request(app).get('/livez');
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: 'ok' });
  });
});

describe('Users API', () => {
  test('create + list + get + update + delete', async () => {
    const create = await request(app)
      .post('/api/users')
      .send({ name: 'Ada', email: 'ada@example.com' });
    expect(create.status).toBe(201);
    expect(create.body).toMatchObject({ name: 'Ada', email: 'ada@example.com' });
    const { id } = create.body;

    const list = await request(app).get('/api/users');
    expect(list.status).toBe(200);
    expect(list.body).toHaveLength(1);

    const get = await request(app).get(`/api/users/${id}`);
    expect(get.status).toBe(200);
    expect(get.body.id).toBe(id);

    const upd = await request(app).patch(`/api/users/${id}`).send({ name: 'Ada L.' });
    expect(upd.status).toBe(200);
    expect(upd.body.name).toBe('Ada L.');

    const del = await request(app).delete(`/api/users/${id}`);
    expect(del.status).toBe(204);

    const after = await request(app).get(`/api/users/${id}`);
    expect(after.status).toBe(404);
  });

  test('rejects invalid email', async () => {
    const res = await request(app).post('/api/users').send({ name: 'X', email: 'nope' });
    expect(res.status).toBe(400);
    expect(res.body.error).toBe('ValidationError');
  });

  test('rejects duplicate email', async () => {
    await request(app).post('/api/users').send({ name: 'A', email: 'a@b.co' });
    const dup = await request(app).post('/api/users').send({ name: 'B', email: 'a@b.co' });
    expect(dup.status).toBe(409);
  });

  test('404 for unknown route', async () => {
    const res = await request(app).get('/api/nope');
    expect(res.status).toBe(404);
  });
});
