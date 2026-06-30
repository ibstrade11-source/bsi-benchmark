"""
Command-line interface for BSI Benchmark.
"""

from .version import __version__


def main() -> int:
    print(f"BSI Benchmark {__version__}")
    print("Foundation initialized.")
    return 0
