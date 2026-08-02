# 🔰 Part 1 — Build Your First Self-Hosted Runner on AWS

---

# 🎯 Mission

Create a fully working GitHub Actions Self-Hosted Runner on AWS EC2 and use it to execute a Node.js CI pipeline.

---

# 🔹 Stage 0 — Create an AWS EC2 Instance

## Requirements

Create an EC2 instance that will act as a GitHub Actions Runner.

---

## Instance Requirements

### OS

Use:

```text
Ubuntu Server 24.04 LTS
```

> **AMI note:** Use Canonical's official AMI owner `099720109477`.  
> Find the latest AMI with:
>
> ```bash
> aws ec2 describe-images \
>   --owners 099720109477 \
>   --filters "Name=name,Values=ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*" \
>             "Name=state,Values=available" \
>   --query "sort_by(Images, &CreationDate)[-1].ImageId" \
>   --output text
> ```

---

### Instance Type

Use:

```text
t3.small
```

> **Availability Zone note:** `t3.small` is not available in every AZ.  
> If you get an "Unsupported" error, pick a different AZ (e.g. `us-east-1a`).

---

### Storage

Minimum:

```text
20 GB gp3
```

---

## Security Group Requirements

Allow:

| Type | Port | Source    |
| ---- | ---- | --------- |
| SSH  | 22   | 0.0.0.0/0 |

---

## Key Pair Requirements

You need an SSH key pair to connect to the instance.

> **Important:** When you download the `.pem` file on Windows, it will have  
> Windows-style line endings (CRLF). OpenSSH on Git Bash / WSL rejects these.  
> Before using the key, strip the carriage returns:
>
> ```bash
> sed 's/\r//' ~/Downloads/my-key.pem > ~/.ssh/my-key.pem
> chmod 600 ~/.ssh/my-key.pem
> ssh-keygen -l -f ~/.ssh/my-key.pem   # should print the fingerprint — no error
> ```

---

# 🔹 Stage 1 — Connect to the Machine

## Instructions

SSH into the EC2 instance:

```bash
ssh -o StrictHostKeyChecking=no -i ~/.ssh/my-key.pem ubuntu@<PUBLIC_IP>
```

> Wait ~30–60 seconds after launch for the SSH daemon to be ready.

---

## Validation

Run:

```bash
whoami
hostname
pwd
uptime
```

---

# 🔹 Stage 2 — Prepare the Runner Machine

## Requirements

Install:

```bash
sudo apt-get update
sudo apt-get install -y git curl tar unzip
```

> Ubuntu 24.04 ships with `git`, `curl`, and `tar` pre-installed.  
> Only `unzip` needs to be added.

---

## Validation

Verify:

```bash
git --version
curl --version
```

---

# 🔹 Stage 3 — Create a GitHub Repository

## Instructions

1. Open GitHub.

2. Click the `+` icon in the top-right corner.

3. Select:

   ```text
   New repository
   ```

4. Repository name:

   ```text
   aws-self-hosted-runner
   ```

5. Set visibility to:

   ```text
   Private
   ```

6. Enable:

   ```text
   Add a README file
   ```

7. Click:

   ```text
   Create repository
   ```

---

# 🔹 Stage 4 — Configure the Self-Hosted Runner

## Instructions

Inside the repository:

```text
Settings → Actions → Runners
```

Click:

```text
New self-hosted runner
```

---

## Requirements

Choose:

```text
Linux
x64
```

GitHub will generate setup commands — **run them on the EC2 instance**.

---

## Step-by-step on the EC2

```bash
# 1. Create a directory for the runner
mkdir ~/actions-runner && cd ~/actions-runner

# 2. Download the latest runner package
RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest \
  | grep '"tag_name"' | sed 's/.*"v\([^"]*\)".*/\1/')

curl -o actions-runner-linux-x64.tar.gz -L \
  "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"

# 3. Extract
tar xzf actions-runner-linux-x64.tar.gz

# 4. Configure (use the token from the GitHub UI or API)
./config.sh \
  --url https://github.com/<YOUR_GITHUB_USERNAME>/aws-self-hosted-runner \
  --token <REGISTRATION_TOKEN> \
  --name "aws-ec2-runner" \
  --labels "self-hosted,linux,x64,aws" \
  --work "_work" \
  --unattended
```

> The registration token expires after **1 hour**. Generate a fresh one if configuration fails.

---

# 🔹 Stage 5 — Start the Runner

## Instructions

Rather than running the runner manually (which stops when you disconnect),  
**install it as a systemd service** so it starts automatically. See Stage 11 below.

For a quick manual test:

```bash
cd ~/actions-runner
./run.sh
```

---

## Validation

On GitHub navigate to:

```text
Settings → Actions → Runners
```

Verify the runner shows:

```text
Idle
```

---

# 🔹 Stage 6 — Create the First Workflow

## Requirements

Create:

```text
.github/workflows/main.yml
```

---

## Workflow Requirements

### Trigger

Run on every push to:

```text
main
```

---

## Job Requirements

Create one job named:

```yaml
runner-test
```

Run it on:

```yaml
runs-on: self-hosted
```

---

## Steps

### Step 1 — Print Machine Information

```yaml
- name: Print machine information
  run: |
    echo "Hostname: $(hostname)"
    echo "User: $(whoami)"
    echo "Uptime:"
    uptime
```

---

### Step 2 — Print Custom Message

```yaml
- name: Print custom message
  run: echo "Hello from AWS self-hosted runner!"
```

---

# 🔹 Stage 7 — Commit and Run the Workflow

## Instructions

1. Commit the workflow.

2. Push the changes to `main`.

3. Open the **Actions** tab in your repository.

4. Open the workflow execution logs.

---

## Validation

Verify the workflow:

* Runs successfully ✅
* Executes on the self-hosted runner (shows `aws-ec2-runner`) ✅
* Prints the EC2 machine information ✅

---

# 🔹 Stage 8 — Prove Runner Persistence

## Instructions

Add a workflow step that creates a file on the runner's filesystem:

```yaml
- name: Prove runner persistence
  run: touch proof.txt
```

---

## Validation

SSH back into the EC2 instance and verify:

```bash
ls ~/actions-runner/_work/aws-self-hosted-runner/aws-self-hosted-runner/
```

You should see:

```text
proof.txt
```

> **Why this path?** The runner checks out your repo inside  
> `~/actions-runner/_work/<repo-name>/<repo-name>/` by default.

---

# 🔹 Stage 9 — Install Node.js 20

## Requirements

Install Node.js 20 on the EC2 instance **before** pushing the CI workflow:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version   # v20.x.x
npm --version
```

---

## Validation

Add workflow steps that print:

```yaml
- name: Print Node.js versions
  run: |
    node --version
    npm --version
```

---

# 🔹 Stage 10 — Run the Node.js CI Pipeline

## Requirements

The repository contains:

* `package.json`
* Tests (`tests/`)
* Build script (`scripts/build.js`)

---

## Workflow Requirements

Add steps for:

### Checkout

```yaml
- name: Checkout
  uses: actions/checkout@v4
```

### Install dependencies

```yaml
- name: Install dependencies
  run: npm ci
```

### Run tests

```yaml
- name: Run tests
  run: npm test
```

### Run build

```yaml
- name: Run build
  run: npm run build
```

---

# 🔹 Stage 11 — Configure the Runner as a Linux Service

## Instructions

The GitHub runner ships with a built-in helper to install itself as a systemd service.

Run these commands on the EC2 instance:

```bash
cd ~/actions-runner

# Install the service (runs as the 'ubuntu' user)
sudo ./svc.sh install ubuntu

# Start the service immediately
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

The service is automatically **enabled** (starts on boot).

---

## Validation

1. Confirm the service is enabled:

   ```bash
   sudo systemctl is-enabled actions.runner.*
   # expected output: enabled
   ```

2. Reboot the EC2 instance:

   ```bash
   sudo reboot
   ```

3. Wait ~60 seconds, then check GitHub:

   ```text
   Settings → Actions → Runners
   ```

   The runner should show **Idle** again without any manual action.

4. Trigger a new workflow execution by pushing an empty commit:

   ```bash
   git commit --allow-empty -m "ci: verify runner persists after reboot"
   git push origin main
   ```

5. Verify the pipeline completes successfully.

---

# ✅ Lab Complete

| Stage | What you built                              | Verified |
| ----- | ------------------------------------------- | -------- |
| 0     | EC2 instance (Ubuntu 24.04, t3.small, 20GB) | ✅       |
| 1     | SSH access                                  | ✅       |
| 2     | Runner dependencies installed               | ✅       |
| 3     | Private GitHub repository                   | ✅       |
| 4     | Self-hosted runner configured               | ✅       |
| 5     | Runner online (Idle) on GitHub              | ✅       |
| 6–7   | Workflow runs on self-hosted runner         | ✅       |
| 8     | proof.txt persists on EC2 filesystem        | ✅       |
| 9     | Node.js 20 installed, printed in logs       | ✅       |
| 10    | Full CI pipeline: install → test → build    | ✅       |
| 11    | Runner auto-starts after reboot             | ✅       |
