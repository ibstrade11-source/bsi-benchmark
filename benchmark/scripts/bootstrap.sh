#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p \
"$ROOT/datasets" \
"$ROOT/prompts" \
"$ROOT/outputs/baseline" \
"$ROOT/outputs/bsi" \
"$ROOT/reports" \
"$ROOT/logs" \
"$ROOT/temp"

echo "[OK] benchmark initialized"
