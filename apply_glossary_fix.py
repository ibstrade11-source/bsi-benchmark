import re
from pathlib import Path

JUDGE_PATH = Path("src/bsi_benchmark/comparison/judge.py")
GLOSSARY_STALE_PATH = Path("docs/BSI_GLOSSARY.md")

src = JUDGE_PATH.read_text(encoding="utf-8")

START_MARKER = "    def _compare_with_llm(self, article, raw_text, bsi_text):\n"
END_MARKER = "\n        result = self.generator.generate(article, prompt)\n"

start = src.index(START_MARKER)
end = src.index(END_MARKER, start) + len(END_MARKER)

old_block = src[start:end]

new_block = '''    def _compare_with_llm(self, article, raw_text, bsi_text):
        # Braces here are single, not doubled: this prompt goes through
        # generator.generate() -> prompt.render(), which substitutes only
        # the literal {title}/{abstract}/{doi} placeholders via regex and
        # leaves every other brace untouched (it does NOT use str.format,
        # despite an earlier version of this comment claiming otherwise --
        # that was stale and caused the JSON schema below to be sent to
        # the judge LLM with literal doubled braces).
        #
        # The `\\n`/`\\n\\n` sequences below are real newline escapes
        # (single backslash), not literal two-character "\\n" text -- an
        # earlier version of this file had them double-escaped, which sent
        # the judge a wall of text with literal backslash-n markers
        # instead of actual line breaks.
        glossary_text = _load_glossary()
        glossary_block = ""
        if glossary_text:
            glossary_block = (
                "GLOSSARY (semantic disambiguation only, not evidence of "
                "quality):\\n"
                "If the BSI analysis below uses BSI-specific terms or "
                "abbreviations you don't recognize, consult this glossary "
                "to understand what they mean. It exists only to reduce "
                "semantic ambiguity -- a term's presence, absence, or "
                "correct use must never by itself raise or lower a score, "
                "and the glossary is not evidence that BSI is correct, "
                "rigorous, or superior.\\n\\n"
                f"{glossary_text}\\n"
                "--- END GLOSSARY ---\\n\\n"
            )

        prompt = (
            "You are an independent scientific evaluator. "
            "Your task is to compare RAW and BSI analyses fairly and "
            "scientifically.\\n\\n"

            "IMPORTANT INDEPENDENCE RULES:\\n"
            "1. Do not assume that RAW is superior merely because it is "
            "simpler or does not use a specialized analytical framework.\\n"
            "2. Do not assume that BSI is superior merely because it uses "
            "a specialized framework.\\n"
            "3. You may consider BSI-specific analytical capabilities "
            "when they are relevant to the scientific task and the article. "
            "Do NOT automatically exclude, ignore, or penalize capabilities "
            "simply because they originate from BSI.\\n"
            "4. You are NOT required to use BSI's internal vocabulary "
            "(such as D1-D7 or EIG), but you are permitted to recognize "
            "and evaluate the underlying analytical capabilities they "
            "represent when those capabilities are observable in the BSI "
            "analysis. Translate them into scientifically meaningful "
            "evaluation criteria rather than treating the vocabulary "
            "itself as evidence of quality.\\n\\n"

            f"{glossary_block}"

            "ARTICLE-ADAPTIVE CRITERIA:\\n"
            "5. Read the article title and both analyses carefully.\\n"
            "6. Develop 4-8 evaluation criteria appropriate to THIS specific "
            "article, its scientific domain, and the task of comparing the "
            "two analyses.\\n"
            "7. Criteria must be substantive and analytically meaningful. "
            "Do not create criteria merely to favor RAW or BSI.\\n"
            "8. Assign an importance weight to EACH criterion yourself. "
            "Weights must reflect the criterion's relative importance for "
            "THIS article, not simply the number of criteria.\\n"
            "9. Use weights from 5 to 35. The weights MUST sum exactly to 100.\\n"
            "10. Do NOT use equal weights by default. At least two criteria "
            "MUST have different weights unless genuinely equal importance "
            "is scientifically justified. If equal weighting is justified, "
            "explain why explicitly.\\n"
            "11. For EVERY criterion, briefly explain why its assigned "
            "weight is appropriate for this particular article.\\n\\n"

            "SCORING:\\n"
            "12. Score RAW and BSI independently on every criterion from "
            "0-10.\\n"
            "13. Base scores on the actual analytical content provided, "
            "not on the name of the framework.\\n"
            "14. Do not award a bonus or penalty merely because an analysis "
            "uses or does not use BSI.\\n\\n"

            "BSI CAPABILITY ASSESSMENT:\\n"
            "15. Separately assess BSI's capability relevance: whether "
            "the capabilities represented by BSI are relevant to this "
            "article and analytical task.\\n"
            "16. Separately assess capability realization: whether those "
            "relevant capabilities were actually realized effectively in "
            "the BSI analysis supplied here.\\n"
            "17. Separately assess incremental value: whether BSI provides "
            "analytical value beyond RAW. This may be high, medium, low, "
            "none, or negative.\\n"
            "18. These BSI assessments must NEVER constitute an automatic "
            "bonus to the BSI score.\\n\\n"

            "FINAL DECISION:\\n"
            "19. Give an overall winner (raw/bsi/tie) for analytical quality.\\n"
            "20. Give a concise overall reason supported by the actual "
            "comparison.\\n\\n"

            "Return ONLY valid JSON, exactly this shape:\\n"
            '{"criteria":[{"name":"","importance":20,"raw_score":0,'
            '"bsi_score":0,"reason":""}],'
            '"bsi_capability_assessment":{'
            '"relevance":"high|medium|low",'
            '"realization":"high|medium|low",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reason":""},'
            '"winner":"raw|bsi|tie",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reasoning":""}\\n\\n'

            f"ARTICLE TITLE\\n{article.title}\\n\\n"
            f"RAW ANALYSIS\\n{raw_text}\\n\\n"
            f"BSI ANALYSIS\\n{bsi_text}\\n"
        )

        result = self.generator.generate(article, prompt)
'''

assert old_block in src, "anchor block not found -- refusing to write, file may have diverged"
src = src.replace(old_block, new_block, 1)

IMPORT_MARKER = "import json\n"
assert src.count(IMPORT_MARKER) == 1, "expected exactly one 'import json' line"

loader = '''import json

from bsi_benchmark import config

_GLOSSARY_CACHE = None


def _load_glossary():
    """
    Load the canonical BSI glossary (docs/BSI_GLOSSARY_FINAL.md) so the LLM
    judge actually has access to the semantic-disambiguation reference the
    README describes it using. Previously this file was never read by any
    code -- the judge prompt had no glossary content in it at all.

    Returns "" (and prints a one-time warning) if the file is missing,
    rather than crashing the judge over a documentation file.
    """
    global _GLOSSARY_CACHE
    if _GLOSSARY_CACHE is not None:
        return _GLOSSARY_CACHE
    path = config.ROOT / "docs" / "BSI_GLOSSARY_FINAL.md"
    try:
        _GLOSSARY_CACHE = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"JUDGE_GLOSSARY_WARNING: could not load {path}: {e!r}")
        _GLOSSARY_CACHE = ""
    return _GLOSSARY_CACHE
'''

src = src.replace(IMPORT_MARKER, loader, 1)

JUDGE_PATH.write_text(src, encoding="utf-8")
print("judge.py patched OK, new size:", len(src))

if GLOSSARY_STALE_PATH.exists():
    GLOSSARY_STALE_PATH.unlink()
    print("removed stale duplicate:", GLOSSARY_STALE_PATH)
