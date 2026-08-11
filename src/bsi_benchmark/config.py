"""
Global project configuration.
"""

from pathlib import Path

PROJECT_NAME = "BSI Benchmark"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[2]

DATASETS_DIR = ROOT / "datasets"
RAW_DATASETS_DIR = DATASETS_DIR / "raw"
PROCESSED_DATASETS_DIR = DATASETS_DIR / "processed"

OUTPUTS_DIR = ROOT / "outputs"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"

import os

# Central HTTP timeout. Override for slow/long-running environments with:
# BSI_HTTP_TIMEOUT=<seconds>
DEFAULT_TIMEOUT = int(os.environ.get("BSI_HTTP_TIMEOUT", "300"))

DEFAULT_USER_AGENT = (
    "BSI-Benchmark/0.1.0 "
    "(https://github.com/ibstrade11-source/bsi-benchmark)"
)
