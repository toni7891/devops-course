#!/bin/bash
set -euo pipefail

apt-get update -y
apt-get install -y curl wget unzip gnupg apt-transport-https software-properties-common
