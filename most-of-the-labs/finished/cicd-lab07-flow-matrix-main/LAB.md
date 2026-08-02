# Lab 07 — CI Execution Flow & Matrix Builds

Learn how a GitHub Actions pipeline reacts to step outcomes: conditional
execution (`success()` / `failure()` / `always()`), `continue-on-error`,
matrix builds, and cross-job gating with `needs` + outputs.

## The app

Express + TypeScript API (in-memory store, no auth). You will **not** change
app logic. You drive the pipeline by toggling test outcomes.

## Control switches

`tests/flow.test.ts` reads two env vars (default = off, all green):

| Env          | Effect                                            |
|--------------|---------------------------------------------------|
| `FAIL_MODE=1`  | One test throws — hard failure                   |
| `FLAKY_MODE=1` | One test passes ~50% of the time — random failure |

Run locally:

```bash
npm ci
npm run lint
npm run typecheck
npm test                 # all green, 2 skipped
FAIL_MODE=1 npm test     # forced failure
FLAKY_MODE=1 npm test    # flaky
```

## The pipeline (`.github/workflows/ci.yml`)

Three jobs:

1. **lint-typecheck** — fast gate. `npm run lint`, `npm run typecheck`.
2. **test** — `needs: lint-typecheck`. **Matrix**: `{ubuntu, windows} × node {20,22}`
   plus an `include` leg `node 18` marked experimental.
   - `continue-on-error` only on the experimental leg → its failure does
     **not** fail the matrix. Watch step **outcome** vs **conclusion**.
   - `if: success()` step — runs only when tests passed.
   - `if: failure()` step — collects diagnostics only on failure.
   - `if: always()` step — cleanup, runs regardless.
   - Job emits `outputs.result` from the test step's outcome.
3. **report** — `needs: test`, `if: always()`. Reads `needs.test.result`
   and gates: pass step on success, failing step (`exit 1`) on failure.

Trigger manually with inputs:

```
Actions tab → CI → Run workflow → toggle fail_mode / flaky_mode
```

## Tasks

1. Push as-is. Confirm all jobs green; read the `success()` / `always()`
   step logs in the `test` job. Note the `failure()` step did **not** run.
2. Run workflow with `fail_mode = true`. Observe:
   - which steps run in the `test` job now (`failure()` + `always()`, not `success()`),
   - `report` job: `needs.test.result` value, fail gate exits 1.
3. Run with `flaky_mode = true` a few times. Explain why `fail-fast: false`
   matters for matrix debugging.
4. Find the experimental Node 18 leg. Explain the difference between a step's
   **outcome** and **conclusion** when `continue-on-error` is set.

## Acceptance

- [ ] Default run: 3 jobs green.
- [ ] `fail_mode` run: `test` fails, `failure()`+`always()` steps ran,
      `report` fail gate exits 1.
- [ ] Can explain outcome vs conclusion on the experimental leg.
- [ ] Can explain `needs` + job output flow into `report`.
