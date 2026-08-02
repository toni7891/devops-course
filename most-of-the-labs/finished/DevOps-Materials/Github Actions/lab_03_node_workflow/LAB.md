# Lab 3: Node.js CI with GitHub Actions

## Goal

Add a GitHub Actions workflow to this Node.js project that automatically installs dependencies and runs the test suite every time code is pushed or a pull request is opened. You will learn how to connect a real npm project to a CI pipeline.

## What you have

A small Node.js project:

- `src/greet.js` — a greeting function
- `test/greet.test.js` — Jest tests for that function

Run locally to verify it works:

```bash
npm install
npm test
```

## Acceptance criteria

The workflow you write must:

- [ ] Trigger on `push` to the `main` branch
- [ ] Trigger on `pull_request` (any branch)
- [ ] Run on `ubuntu-latest`
- [ ] Check out the repository code
- [ ] Set up Node.js version 20
- [ ] Install dependencies with `npm install`
- [ ] Run the test suite with `npm test`
- [ ] All steps complete successfully

## Hints

- You will need `actions/checkout@v4` to pull the code into the runner environment.
- `actions/setup-node@v4` handles Node.js setup — look for its `node-version` input.
- Use `run:` to execute shell commands, `uses:` to run prebuilt actions.

## Where the workflow goes

Create your workflow file at `.github/workflows/ci.yml`.
