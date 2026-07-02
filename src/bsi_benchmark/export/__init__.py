from importlib import import_module
from pathlib import Path

from .registry import registry
from .manager import ExportManager


def _load_plugins():
    base_path = Path(__file__).parent

    for file in base_path.glob("*_exporter.py"):
        import_module(f"bsi_benchmark.export.{file.stem}")

    # special case for html
    try:
        import_module("bsi_benchmark.export.html")
    except ImportError:
        pass


_load_plugins()

__all__ = ["ExportManager", "registry"]
