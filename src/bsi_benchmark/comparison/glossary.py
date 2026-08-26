"""
BSI terminology glossary for the independent judge.

Provides semantic disambiguation only -- definitions for BSI-specific
abbreviations and constructs (BSI, ER, BIO, CORE_BEHMANESH, the EIG
family, the ECC family, REIG, D1-D7) so the judge is not left guessing
at unfamiliar acronyms when they appear in a BSI analysis. This is NOT
an evaluation rubric and must not be treated as evidence that BSI is
superior -- see comparison/judge.py for how the caveat is restated in
the prompt section that includes this text.

Design: the judge must be able to reason about BSI terminology in EITHER
analysis, and about D1-D7/EIG/ECC framework structure even when a given
analysis paraphrases rather than naming a term outright -- a per-call
keyword filter can silently omit exactly the definitions the judge would
have needed. So the full glossary file (docs/BSI_GLOSSARY_FINAL.md) is
loaded whole, once, and sent to every judge call unfiltered alongside
both the raw and bsi analyses.

Fail-open by design: if the glossary file is missing (e.g. a packaged
install without docs/) or disabled via BSI_JUDGE_GLOSSARY=0, the judge
runs without it rather than crashing the comparison.
"""

import os

_GLOSSARY_CACHE = None


def _repo_glossary_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    # comparison/ -> bsi_benchmark/ -> src/ -> repo root
    repo_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(repo_root, "docs", "BSI_GLOSSARY_FINAL.md")


def load_full_glossary() -> str:
    """Return the full, unfiltered glossary file content, cached after
    first load. Empty string if the file is missing or the glossary is
    disabled via BSI_JUDGE_GLOSSARY=0.

    Unlike a per-call relevance filter, this always returns the complete
    file -- the judge sees the whole glossary alongside both analyses on
    every call, not just entries matched by keyword presence.
    """
    global _GLOSSARY_CACHE

    if os.environ.get("BSI_JUDGE_GLOSSARY", "1") == "0":
        return ""

    if _GLOSSARY_CACHE is not None:
        return _GLOSSARY_CACHE

    path = _repo_glossary_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            _GLOSSARY_CACHE = f.read().strip()
    except OSError:
        _GLOSSARY_CACHE = ""

    return _GLOSSARY_CACHE


def load_compact_glossary(max_chars: int = 3000) -> str:
    """
    Return a compact semantic version of the full BSI glossary.

    The full glossary remains unchanged on disk. For LLM judging, retain
    section headings plus a short semantic excerpt from each section so
    the judge can understand BSI terminology without consuming the full
    prompt/token budget.
    """
    full = load_full_glossary()
    if not full:
        return ""

    lines = full.splitlines()
    sections = []
    current = []

    for line in lines:
        if line.startswith("#"):
            if current:
                sections.append(current)
            current = [line]
        elif current:
            current.append(line)

    if current:
        sections.append(current)

    compact_sections = []

    for section in sections:
        heading = section[0].strip()
        body = " ".join(
            x.strip()
            for x in section[1:]
            if x.strip() and not x.strip().startswith("```")
        )

        if not body:
            compact_sections.append(heading)
            continue

        # Keep enough text to preserve the semantic definition while
        # aggressively reducing prompt size.
        excerpt = body[:360].rstrip()
        if len(body) > 360:
            excerpt += "..."

        compact_sections.append(f"{heading}\n{excerpt}")

    compact = "\n\n".join(compact_sections)

    # Hard upper bound for the entire glossary contribution.
    if len(compact) > max_chars:
        compact = compact[:max_chars].rsplit("\n", 1)[0].rstrip()
        compact += "\n[Compact glossary truncated for token budget.]"

    return compact


def load_judge_resource() -> str:
    """Load glossary content as an independent judge knowledge resource.

    This function deliberately does NOT build or modify a comparison prompt.
    The caller must treat the returned text as judge-side context/resource only.
    """
    return load_full_glossary()
