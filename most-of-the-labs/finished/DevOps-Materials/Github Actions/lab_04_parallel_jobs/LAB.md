# Lab 4: Parallel Jobs, needs, and Expressions

## Goal

Extend a single-job workflow into a multi-job pipeline. You will run `lint` and `test` jobs **in parallel**, then add a `summary` job that waits for both using `needs` and prints information using GitHub Actions **expressions**. This teaches how real CI pipelines are structured: independent checks run simultaneously, and a final job collects the results.

## Background

- **Parallel jobs** — two jobs with no dependency between them start at the same time. GitHub runs them concurrently on separate runners.
- **`needs`** — declares that a job must wait for other jobs to finish before it starts. `needs: [lint, test]` means the summary job only runs after both complete.
- **Expressions** — `${{ }}` lets you embed dynamic values into steps. `${{ github.actor }}` is the user who triggered the run. `${{ needs.lint.result }}` is the outcome of the lint job (`success`, `failure`, `skipped`).

## What you have

A small Node.js project:

- `src/greet.js` — a greeting function
- `test/greet.test.js` — Jest tests
- `package.json` — two scripts: `npm test` (Jest) and `npm run lint` (ESLint)
- `.eslintrc.json` — ESLint configuration

Run locally to verify the baseline works:

```bash
npm install
npm run lint
npm test
```

Both commands should exit with no errors.

## Acceptance criteria

The workflow you write must:

- [ ] Trigger on `push` to the `main` branch
- [ ] Trigger on `pull_request` (any branch)
- [ ] Have a `lint` job that runs `npm run lint` on `ubuntu-latest`
- [ ] Have a `test` job that runs `npm test` on `ubuntu-latest`
- [ ] `lint` and `test` jobs run in parallel (neither depends on the other)
- [ ] Have a `summary` job with `needs: [lint, test]`
- [ ] `summary` job prints `${{ github.actor }}` in a step
- [ ] `summary` job prints `${{ needs.lint.result }}` and `${{ needs.test.result }}` in a step
- [ ] All three jobs complete successfully

## Hints

- Two jobs with no `needs` between them run in parallel automatically — just define them as separate keys under `jobs:`.
- `needs` takes a list: `needs: [lint, test]`. The job won't start until every listed job finishes.
- Access job results from a dependent job with `${{ needs.<job-id>.result }}`. The value will be `success`, `failure`, or `skipped`.

## Where the workflow goes

Create your workflow at `.github/workflows/ci.yml`.
