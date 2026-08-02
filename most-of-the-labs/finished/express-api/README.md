# student-api

a rest api lab built with express, typescript, and mongodb. the goal was to practice building a production-style backend from scratch and deploying it to aws using a full ci/cd pipeline.

---

## what i built

a crud api for managing items, with the following structure:

- `GET /items` — list all items
- `POST /items` — create an item
- `GET /items/:id` — get one item by id
- `PUT /items/:id` — update an item
- `DELETE /items/:id` — delete an item
- `GET /health` — health check endpoint

---

## what i practiced and learned

### typescript + express
- setting up an express app in typescript with strict typing
- using `Router` and separating routes into their own files
- writing typed request/response handlers with `Request`, `Response`, `NextFunction`
- centralized error handling middleware that catches validation errors, cast errors, and generic 500s

### mongodb + mongoose
- defining schemas and models with typescript interfaces (`IItem extends Document`)
- using `timestamps: true` to auto-manage `createdAt` / `updatedAt`
- using `runValidators: true` on updates so schema rules are enforced on edits too
- connecting to mongodb with a timeout setting to fail fast if the db is unreachable

### environment config
- loading env vars with `dotenv` and centralizing them in a single `config` object
- injecting `COMMIT_SHA` at docker build time as a build arg so you can always trace which version is running

### docker
- multi-stage dockerfile: build stage compiles typescript, production stage copies only the compiled output
- running the container as `USER node` (non-root) for security
- keeping the production image lean by using `npm ci --omit=dev`

### ci/cd with github actions
- **ci pipeline** (`ci.yaml`): runs lint, tests (with a real mongodb service container), and a docker build check on every push and pull request
- **deploy pipeline** (`deploy.yaml`): triggers on push to main, builds and pushes the docker image to docker hub tagged with the commit sha and `latest`, then deploys to aws

### aws deployment
- authenticating to aws from github actions using **oidc** (no long-lived access keys stored as secrets)
- storing secrets like `MONGODB_URI`, dockerhub credentials in **aws ssm parameter store** as `SecureString` — the ec2 instances pull them at runtime, not at build time
- using **aws systems manager (ssm) send-command** to remotely run a deploy script on ec2 instances without needing ssh access
- querying the **auto scaling group** to get the current in-service instance ids dynamically, so the deploy works even after scale-in/scale-out events
- waiting for the ssm command to finish on each instance before marking the deploy as complete
- using `sed` to inject the image tag and commit sha into the deploy script at runtime (since heredocs don't expand variables from the outer shell when quoted)

### infrastructure as code
- writing a **cloudformation template** to define security groups for the alb and ec2 instances
- alb accepts traffic on port 80 from the internet; ec2 only accepts traffic on port 3000 from the alb security group (not directly from the internet)
- exporting stack outputs so other stacks can reference the security group ids

### testing
- integration tests with **vitest** and **supertest** that hit a real mongodb instance (not mocked)
- separate test setup file to connect/disconnect the db around the test suite

---

## stack

| layer | tech |
|---|---|
| runtime | node 22, typescript |
| framework | express 4 |
| database | mongodb + mongoose |
| containerization | docker (multi-stage) |
| ci/cd | github actions |
| registry | docker hub |
| cloud | aws (ec2, alb, asg, ssm, cloudformation) |
| auth | aws oidc from github actions |
| testing | vitest + supertest |
