/**
 * Lab control tests — drive CI failure paths on demand.
 *
 * Default run: all green (skipped/passing). CI status-function and
 * continue-on-error steps need a real failing signal to react to;
 * toggle these via env so students control the outcome.
 *
 *   FAIL_MODE=1   -> forces a hard failure (use to watch failure()/always())
 *   FLAKY_MODE=1  -> ~50% random failure (use to watch fail-fast/matrix + retries)
 */
import request from 'supertest';
import { createApp } from '../src/app.js';

const app = createApp();

describe('Lab: flow control', () => {
  test('app boots and serves /livez', async () => {
    const res = await request(app).get('/livez');
    expect(res.status).toBe(200);
  });

  const failMode = process.env.FAIL_MODE === '1';
  (failMode ? test : test.skip)('FAIL_MODE: deliberate hard failure', () => {
    throw new Error('FAIL_MODE=1 — intentional failure for CI flow lab');
  });

  const flakyMode = process.env.FLAKY_MODE === '1';
  (flakyMode ? test : test.skip)('FLAKY_MODE: passes ~50% of the time', () => {
    const ok = Math.random() < 0.5;
    expect(ok).toBe(true);
  });
});
