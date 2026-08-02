"""
Minimal plugin architecture for analysis frameworks.

Today this tool only drives BSI end-to-end -- but calling it "the BSI
benchmark" internally (a hardcoded assumption baked into every module)
is exactly the credibility problem raised in project review: a tool
that can only ever evaluate its own creator's framework cannot claim
neutrality, no matter how fair its internals are.

This module does not rewrite `compare`/`self-compare` to be
framework-generic today -- that is a larger, riskier change tracked in
ROADMAP.md. What it does now: establish the seam. A Framework is
registered once, by name, with a loader function that returns its
prompt text given a path. BSI is registered as exactly one entry in
this registry, using the exact same prompt_loader.load_bsi_prompt it
already used -- nothing about BSI's own behavior changes. A second
framework can be added later by writing one more register() call, not
by editing BSI's code.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass
class Framework:
    name: str
    description: str
    # Given a path to a prompt/template file, return the prompt text
    # ready to use (may auto-repair/template it, as BSI's loader does).
    load_prompt: Callable[[str], str]
    version: Optional[str] = None


class FrameworkRegistry:
    def __init__(self):
        self._frameworks: Dict[str, Framework] = {}

    def register(self, framework: Framework) -> None:
        if framework.name in self._frameworks:
            raise ValueError(
                f"framework '{framework.name}' is already registered -- "
                "each name must be unique. If you're replacing a "
                "framework's implementation, unregister it first."
            )
        self._frameworks[framework.name] = framework

    def unregister(self, name: str) -> None:
        self._frameworks.pop(name, None)

    def get(self, name: str) -> Framework:
        try:
            return self._frameworks[name]
        except KeyError:
            available = ", ".join(sorted(self._frameworks)) or "(none registered)"
            raise KeyError(
                f"no framework registered as '{name}'. Available: {available}"
            )

    def list_names(self) -> list:
        return sorted(self._frameworks.keys())


registry = FrameworkRegistry()


def _register_bsi() -> None:
    from ..prompt_loader import load_bsi_prompt
    from ..version import __version__ as tool_version

    registry.register(Framework(
        name="bsi",
        description=(
            "Behmanesh Structural Index -- multi-layer epistemic "
            "evaluation framework (Manifest/Latent/Meta layers, BIO "
            "v1.0 seven-dimension rubric, EIG/REIG audit)."
        ),
        load_prompt=lambda path: load_bsi_prompt(path, label="bsi-prompt-file"),
        version=tool_version,
    ))


_register_bsi()
