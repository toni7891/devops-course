# Lab: Artifacts & Outputs — Pass Data Between Jobs

## Goal

Build a two-job GitHub Actions workflow for the **Harmonic Haven** React app.
You'll learn two ways jobs communicate: **artifacts** (files) and **outputs** (strings).

- The `build` job compiles the app, sets a job output, and uploads the build as an artifact.
- The `inspect` job reads the output value, downloads the artifact, and prints both.

---

## Getting Started

```bash
npm install
npm run build      # compiles to dist/
```

---

## Core concepts

### Job outputs — passing a string between jobs

A step writes to `$GITHUB_OUTPUT`:
```bash
echo "my-key=my-value" >> $GITHUB_OUTPUT
```
The job exposes it:
```yaml
jobs:
  my-job:
    outputs:
      my-key: ${{ steps.step-id.outputs.my-key }}
```
A downstream job reads it:
```yaml
${{ needs.my-job.outputs.my-key }}
```

### Artifacts — passing files between jobs

Upload in one job:
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: my-artifact
    path: dist/
```
Download in another:
```yaml
- uses: actions/download-artifact@v4
  with:
    name: my-artifact
    path: dist/
```

---

## Workflow shape

```
build  →  set output (artifact name)
       →  upload dist/ as artifact
              ↓
           inspect  →  read output value  →  download artifact  →  print files
```

---

## Acceptance criteria

The workflow you write must:

- [ ] Have a `build` job that runs `npm run build`, sets a job output called `artifact-name` with the value `build-output`, and uploads `dist/` as an artifact using that name
- [ ] Have an `inspect` job that depends on `build`, reads the `artifact-name` output and prints it, downloads the artifact, and lists its contents with `ls -R`
- [ ] Trigger on `push` to any branch

---

## Hints

- To set an output: give the step an `id:`, then `run: echo "artifact-name=build-output" >> $GITHUB_OUTPUT`
- Reference a job output in another job: `${{ needs.build.outputs.artifact-name }}`
- You can use the output value as the artifact `name:` in both upload and download steps — that's the point

---

## Where the workflow goes

Create your workflow at `.github/workflows/ci.yml`.
