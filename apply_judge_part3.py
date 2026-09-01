from pathlib import Path

JUDGE_PATH = Path("src/bsi_benchmark/comparison/judge.py")
src = JUDGE_PATH.read_text(encoding="utf-8")

if "generate_with_system(article, system_prompt, user_prompt)" in src:
    print("judge.py: already patched -- skipped")
else:
    START_MARKER = "    def _compare_with_llm(self, article, raw_text, bsi_text):\n"
    END_MARKER = "\n        result = self.generator.generate(article, prompt)\n"

    if START_MARKER not in src or END_MARKER not in src:
        raise SystemExit(
            "judge.py: expected method markers not found -- send the "
            "current file content back for a manual patch."
        )

    start = src.index(START_MARKER)
    end = src.index(END_MARKER, start) + len(END_MARKER)
    old_block = src[start:end]

    new_block = '''    def _compare_with_llm(self, article, raw_text, bsi_text):
        # Architecture: the glossary and judging rules are background
        # context for HOW to judge, not part of WHAT is being judged.
        # They are sent as a separate system-level message
        # (generate_with_system's system_prompt) so they never mix into
        # the same turn as the RAW/BSI analyses themselves, which are
        # sent as the user-level message (user_prompt). Generators that
        # don't support a real system role (anything that hasn't
        # overridden AnalysisGenerator.generate_with_system) fall back to
        # a concatenated single prompt automatically -- see
        # generation/base.py.
        #
        # Full glossary is mandatory for LLM judging.
        # Never silently downgrade to a compact or glossary-free judge.
        glossary_text = load_full_glossary()

        if not glossary_text:
            raise RuntimeError(
                "BSI Judge requires the full glossary, but "
                "docs/BSI_GLOSSARY_FINAL.md could not be loaded "
                "or BSI_JUDGE_GLOSSARY is disabled"
            )

        glossary_block = (
            "FULL BSI GLOSSARY (semantic disambiguation only; NOT "
            "evidence, NOT a scoring rubric, and NOT a required "
            "criterion list):\\n"
            "Use the glossary only to disambiguate BSI terminology. "
            "Determine independently which concepts are relevant. "
            "Do not treat glossary terms as evidence, criteria, or "
            "proof that BSI is correct, effective, or superior.\\n\\n"
            f"{glossary_text}\\n"
            "--- END FULL BSI GLOSSARY ---\\n\\n"
        )

        system_prompt = (
            "You are an independent scientific evaluator comparing RAW and BSI fairly. "
            "Your task is to compare RAW and BSI analyses fairly and "
            "scientifically.\\n\\n"
            "INDEPENDENCE RULES:\\n"
            "Evaluate RAW and BSI impartially. Judge actual capabilities, "
            "not framework labels; no automatic reward or penalty.\\n\\n"
            f"{glossary_block}"
            "ARTICLE-ADAPTIVE CRITERIA:\\n"
            "Create 4-8 substantive article-specific criteria. Weight each "
            "5-35; weights must sum to 100. Avoid equal weights unless "
            "scientifically justified; briefly justify every weight.\\n\\n"
            "SCORING:\\n"
            "Score RAW and BSI independently from 0-10 using actual "
            "content; no automatic BSI bonus or penalty.\\n\\n"
            "BSI CAPABILITY ASSESSMENT:\\n"
            "Separately rate BSI relevance, realization, and incremental "
            "value beyond RAW. Base relevance/realization on this article "
            "and the supplied BSI analysis. These ratings never create an "
            "automatic BSI score bonus.\\n\\n"
            "FINAL DECISION:\\n"
            "Choose raw, bsi, or tie and give a concise evidence-grounded "
            "reason.\\n\\n"
            "Return ONLY valid JSON with this shape:\\n"
            '{"criteria":[{"name":"","importance":20,"raw_score":0,'
            '"bsi_score":0,"reason":""}],'
            '"bsi_capability_assessment":{"relevance":"high|medium|low",'
            '"realization":"high|medium|low",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reason":""},"winner":"raw|bsi|tie",'
            '"incremental_value":"high|medium|low|none|negative",'
            '"reasoning":""}\\n\\n'
            "The article title and the two analyses to compare follow in "
            "the next message."
        )

        user_prompt = (
            f"ARTICLE TITLE\\n{article.title}\\n\\n"
            f"RAW ANALYSIS\\n{raw_text}\\n\\n"
            f"BSI ANALYSIS\\n{bsi_text}\\n"
        )

        result = self.generator.generate_with_system(article, system_prompt, user_prompt)
'''
    assert old_block in src, "prompt-construction block not found -- refusing to write"
    src = src.replace(old_block, new_block, 1)
    JUDGE_PATH.write_text(src, encoding="utf-8")
    print("judge.py part 3 patched OK, new size:", len(src))
