from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from engine.provider_loader import providers

print("BSI Benchmark Engine v2")
print("-----------------------")

for p in providers():
    print(f"Provider: {p.name}")
