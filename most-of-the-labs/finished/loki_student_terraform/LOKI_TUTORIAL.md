# Loki Step-by-Step Tutorial

## 1. Install Loki

SSH into the Loki server.

```bash
ssh -i /path/to/key ubuntu@<LOKI_SERVER_IP>
```

Download Loki.

```bash
sudo apt update
sudo apt install unzip -y
curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
chmod +x loki-linux-amd64
```

Download the Loki config.

```bash
wget https://raw.githubusercontent.com/grafana/loki/v2.9.0/cmd/loki/loki-local-config.yaml
```

Start Loki.

```bash
./loki-linux-amd64 -config.file=loki-local-config.yaml
```

Test Loki.

```bash
curl http://<LOKI_SERVER_IP>:3100/metrics
```

## 2. Install Grafana

Run this on the Loki server.

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https wget gnupg
```

Add the Grafana key.

```bash
sudo mkdir -p /etc/apt/keyrings
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
```

Add the Grafana repository.

```bash
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

Install Grafana.

```bash
sudo apt-get update
sudo apt-get install -y grafana
```

Start Grafana.

```bash
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

Check Grafana.

```bash
sudo systemctl status grafana-server
```

Test Grafana.

```bash
curl http://<LOKI_SERVER_IP>:3000
```

## 3. Install Promtail On Each Node

SSH into `node-1`.

```bash
ssh -i /path/to/key ubuntu@<NODE_1_IP>
```

Download Promtail.

```bash
sudo apt update
sudo apt install unzip -y
curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
chmod +x promtail-linux-amd64
```

Download the Promtail config.

```bash
wget https://raw.githubusercontent.com/grafana/loki/v2.9.0/clients/cmd/promtail/promtail-local-config.yaml
```

Edit the config.

```bash
nano promtail-local-config.yaml
```

Set the Loki URL.

```yaml
clients:
  - url: http://<LOKI_PRIVATE_IP>:3100/loki/api/v1/push
```

Use the Loki server private IP when Promtail runs on EC2 nodes in the same VPC.

Start Promtail.

```bash
sudo ./promtail-linux-amd64 -config.file=promtail-local-config.yaml
```

Repeat the same steps on `node-2`.

## Fix Loki Config Version Error

If Loki fails because of unknown config fields, remove the config file.

```bash
rm loki-local-config.yaml
```

Download the Loki 2.9.0 config.

```bash
wget https://raw.githubusercontent.com/grafana/loki/v2.9.0/cmd/loki/loki-local-config.yaml
```

Start Loki again.

```bash
./loki-linux-amd64 -config.file=loki-local-config.yaml
```

If `wget` or `unzip` is missing, install them.

```bash
sudo apt update
sudo apt install wget unzip -y
```

## 4. Connect Grafana To Loki

Open Grafana.

```text
http://<GRAFANA_SERVER_IP>:3000
```

Go to:

```text
Connections -> Data sources -> Add data source -> Loki
```

Set the Loki URL.

```text
http://localhost:3100
```

Click:

```text
Save & test
```

## 5. Query System Logs

Open:

```text
Explore
```

Select the Loki data source.

Run:

```logql
{job="varlogs"}
```

Search for text.

```logql
{job="varlogs"} |= "docker"
```

Query one file.

```logql
{filename="/var/log/syslog"}
```

Query multiple files.

```logql
{filename=~"/var/log/syslog|/var/log/kern.log"}
```

## 6. Add Application Logs

Stop Promtail on each node.

```text
CTRL+C
```

Edit the Promtail config.

```bash
nano promtail-local-config.yaml
```

Use this config.

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://<LOKI_PRIVATE_IP>:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log

  - job_name: api
    static_configs:
      - targets:
          - localhost
        labels:
          job: api_logs
          __path__: /home/ubuntu/app/*.log
```

Start Promtail again.

```bash
sudo ./promtail-linux-amd64 -config.file=promtail-local-config.yaml
```

## 7. Query Application Logs

Run:

```logql
{job="api_logs"}
```

Filter by text.

```logql
{job="api_logs"} |= "error"
```

Query the app log file.

```logql
{filename="/home/ubuntu/app/app.log"}
```
