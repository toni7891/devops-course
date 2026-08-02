# Loki Student Terraform

This is the starter Terraform project for the Loki tutorial.

It creates only the base AWS infrastructure:

- one Ubuntu EC2 instance for Loki and Grafana
- two Ubuntu EC2 app nodes
- a security group for SSH, Grafana, Loki, app traffic, and internal instance traffic
- a generated `ssh_commands.txt` file with public and private IPs

It does not install Loki, Grafana, or Promtail. Students should follow [`../LOKI_TUTORIAL.md`](../LOKI_TUTORIAL.md) after Terraform finishes.

## Before You Apply

Create the SSH key expected by this project in your user home directory.

macOS or Linux:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/loki-student-key
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.ssh"
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\loki-student-key"
```

Windows Git Bash or WSL:

```bash
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/loki-student-key
```

If you want to use a different AWS key pair name or key path, set `key_name`, `ssh_private_key_path`, or `ssh_public_key_path` in `terraform.tfvars`. On Windows, use forward slashes in Terraform paths, for example `C:/Users/your-name/.ssh/loki-student-key`.

## Deploy

```bash
terraform init
terraform apply
```

After apply, use `ssh_commands.txt` or the `instance_ips` output to find:

- `LOKI_SERVER_IP`: the public IP of `loki-student-server`
- `LOKI_PRIVATE_IP`: the private IP of `loki-student-server`
- `NODE_1_IP` and `NODE_2_IP`: the public IPs of the app nodes

Then continue with the Loki setup in [`../LOKI_TUTORIAL.md`](../LOKI_TUTORIAL.md).

## What Is Preinstalled

The Loki/Grafana server has basic command-line packages only.

Each app node runs the demo Node.js app from `../app`, so application logs are available under:

```text
/home/ubuntu/app/*.log
```
