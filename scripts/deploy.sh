#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d --build
sleep 3
curl --fail http://localhost:5000/health
