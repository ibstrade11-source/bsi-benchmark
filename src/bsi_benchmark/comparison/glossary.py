"""
BSI terminology glossary for the independent judge.

Provides semantic disambiguation only -- definitions for BSI-specific
abbreviations and constructs (BSI, ER, BIO, CORE_BEHMANESH, the EIG
family, the ECC family, REIG, D1-D7) so the judge is not left guessing
at unfamiliar acronyms when they appear in a BSI analysis. This is NOT
an evaluation rubric and must not be treated as evidence that BSI is
superior -- see comparison/judge.py for how the caveat is restated in
the prompt section that includes this text.

Design: the glossary file (docs/BSI_GLOSSARY.md) is parsed once into a
{term: definition} map. On each judge call, only the entries whose term
actually appears in that specific raw/bsi analysis text are included in
the prompt -- not the full ~560-line file every time. A judge call for
an analysis that never mentions EIG, ECC, or D1-D7 pays nothing for
those definitions.

Fail-open by design: if the glossary file is missing (e.g. a packaged
install without docs/) or disabled via BSI_JUDGE_GLOSSARY=0, the judge
runs without it rather than crashing the comparison.
"""

import os
import re

_TERMS_CACHE = None
_MAX_SECTION_CHARS = 4000  # safety cap on the assembled per-call excerpt

_HEADER_RE = re.compile(r"^### (.+?)$", re.MULTILINE)
_DIM_TABLE_ROW_RE = re.compile(r"^\|\s*(D[1-7])\s*\|\s*([A-Za-z]+)\s*\|\s*([\d.]+)\s*\|$", re.MULTILINE)
_WORD_PATTERN_CACHE = {}


def _repo_glossary_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    # comparison/ -> bsi_benchmark/ -> src/ -> repo root
    repo_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    return os.path.join(repo_root, "docs", "BSI_GLOSSARY.md")


def _parse_sections(raw_text: str) -> dict:
    terms = {}
    matches = list(_HEADER_RE.finditer(raw_text))
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_text)
        body = raw_text[start:end]
        for boundary in ("\n---", "\n## "):
            idx = body.find(boundary)
            if idx != -1:
                body = body[:idx]
        body = body.strip()
        if not body:
            continue

        if "—" in header:
            term, full_name = (p.strip() for p in header.split("—", 1))
            entry = f"{term} ({full_name}): {body}"
        else:
            term = header
            entry = f"{term}: {body}"

        terms[term] = entry

        # BSI analyses commonly use short tags (e.g. "Manifest") rather
        # than the full header phrase ("Manifest Layer") -- also index
        # under the leading word so those short tags still match.
        first_word = term.split()[0]
        if first_word != term and len(first_word) > 3:
            terms.setdefault(first_word, entry)

    for dim_id, name, weight in _DIM_TABLE_ROW_RE.findall(raw_text):
        terms[dim_id] = (
            f"{dim_id} ({name}): one of BSI's seven internal dimensions "
            f"(weight {weight}) -- not independently required criteria "
            f"for this judge, see the independence rules above."
        )

    return terms


def load_glossary_terms() -> dict:
    """Return the parsed {term: definition} map, cached after first
    load. Empty dict if the file is missing or the glossary is disabled
    via BSI_JUDGE_GLOSSARY=0."""
    global _TERMS_CACHE

    if os.environ.get("BSI_JUDGE_GLOSSARY", "1") == "0":
        return {}

    if _TERMS_CACHE is not None:
        return _TERMS_CACHE

    path = _repo_glossary_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError:
        _TERMS_CACHE = {}
        return _TERMS_CACHE

    _TERMS_CACHE = _parse_sections(raw)
    return _TERMS_CACHE


def relevant_glossary_section(*texts):
    """Return only the glossary entries whose term actually appears in
    the given text(s) (the raw and bsi analysis text for this specific
    cell), brace-escaped and ready to embed in a prompt that will later
    pass through str.format(). Returns None if nothing matched or the
    glossary is unavailable/disabled."""
    terms = load_glossary_terms()
    if not terms:
        return None

    combined = "\n".join(t or "" for t in texts)
    matched = []
    for term, definition in terms.items():
        pattern = _WORD_PATTERN_CACHE.get(term)
        if pattern is None:
            pattern = re.compile(r"\b" + re.escape(term) + r"\b")
            _WORD_PATTERN_CACHE[term] = pattern
        if pattern.search(combined):
            matched.append(definition)

    if not matched:
        return None

    text = "\n\n".join(matched)
    if len(text) > _MAX_SECTION_CHARS:
        text = text[:_MAX_SECTION_CHARS] + "\n\n[glossary excerpt truncated for length]"

    # This text gets embedded into a prompt string that
    # generation/prompt.py's render() later runs through
    # str.format(title=..., abstract=...) -- literal { or } here would
    # otherwise be misparsed as a format placeholder.
    return text.replace("{", "{{").replace("}", "}}")
