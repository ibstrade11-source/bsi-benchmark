#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "============================================================"
echo " BSI BENCHMARK — VALIDATE / CURATE / COMMIT"
echo "============================================================"

echo
echo "===== PYTEST ====="
PYTHONPATH=src pytest -q

echo
echo "===== COMPILE CHECK ====="
PYTHONPATH=src python -m compileall -q src tests

echo
echo "===== RESULT VALIDATION + CURATION + COMMIT ====="
python scripts/validate_and_curate_result.py

echo
echo "============================================================"
echo " COMPLETE"
echo "============================================================"

git status -sb
git log -1 --oneline --decorate
