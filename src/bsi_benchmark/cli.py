
"""
Command-line interface for BSI Benchmark.
"""

import argparse

from .version import __version__
from .benchmark import BenchmarkRunner
from bsi_benchmark.errors import ProviderError


def main() -> int:

    parser = argparse.ArgumentParser(prog="bsi-benchmark")

    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Run benchmark")

    run.add_argument(
        "--provider",
        required=True,
    )

    run.add_argument(
        "--query",
        required=True,
    )

    args = parser.parse_args()

    print(f"BSI Benchmark {__version__}")

    if args.command == "run":

        runner = BenchmarkRunner()

        try:
            result = runner.run(
                args.provider,
                args.query,
            )
        except ProviderError as e:
            print(f"ERROR: {e}")
            return 1

        print(f"Provider : {result.dataset.provider}")
        print(f"Query    : {result.dataset.query}")
        print(f"Articles : {len(result.dataset.articles)}")

        return 0

    parser.print_help()

    return 0
