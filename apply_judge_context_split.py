from pathlib import Path

# ===========================================================================
# PART 1: generation/base.py -- default generate_with_system() fallback
# ===========================================================================
BASE_PATH = Path("src/bsi_benchmark/generation/base.py")
base_src = BASE_PATH.read_text(encoding="utf-8")
BASE_ANCHOR = "        raise NotImplementedError\n"
assert base_src.count(BASE_ANCHOR) == 1, "base.py anchor not unique/found -- aborting"
base_addition = '''        raise NotImplementedError

    def generate_with_system(self, article, system_prompt: str, user_prompt: str):
        """
        Like generate(), but with the prompt split into a system-level
        context (background/reference material, e.g. task rules and the
        BSI glossary) and a user-level task (the actual content being
        acted on, e.g. the RAW/BSI analyses to compare).

        Keeping this split matters for the judge specifically: the
        glossary is background context for interpreting BSI terminology,
        not part of the comparison task itself, and mixing it into the
        same turn as the RAW/BSI analyses blurs that distinction for the
        model. Subclasses whose backend supports a real system-role
        message (OpenRouterGenerator, GroqGenerator) override this to
        send system_prompt and user_prompt as separate messages.

        Default implementation (for generators that don't override this):
        falls back to a single combined prompt via generate(), so every
        generator keeps working without needing this method implemented.
        """
        combined = f"{system_prompt}\\n\\n{user_prompt}"
        return self.generate(article, combined)
'''
if BASE_ANCHOR in base_src and "generate_with_system" not in base_src:
    base_src = base_src.replace(BASE_ANCHOR, base_addition, 1)
    BASE_PATH.write_text(base_src, encoding="utf-8")
    print("base.py patched, new size:", len(base_src))
else:
    print("base.py: generate_with_system already present or anchor missing -- skipped")

# ===========================================================================
# PART 2: openrouter.py / groq.py -- real system+user role support
# ===========================================================================
def patch_openai_compatible_generator(path: Path, env_var: str):
    src = path.read_text(encoding="utf-8")
    if "generate_with_system" in src:
        print(f"{path}: already patched -- skipped")
        return

    OLD_GENERATE_HEAD = '    def generate(self, article, prompt_template: str) -> Analysis:\n'
    assert src.count(OLD_GENERATE_HEAD) == 1, f"{path}: generate() signature not found/unique"

    PREAMBLE_END_MARKER = "        response = self.client.post(\n"
    start = src.index(OLD_GENERATE_HEAD)
    preamble_end = src.index(PREAMBLE_END_MARKER, start)
    preamble = src[start:preamble_end]

    END_MARKER = "\n        return Analysis(text=text, source_model=self.model)\n"
    end = src.index(END_MARKER, preamble_end) + len(END_MARKER)
    call_and_parse_body = src[preamble_end:end]

    new_call_method = (
        "    def _call_messages(self, api_key: str, messages: list) -> Analysis:\n"
        + call_and_parse_body.replace(
            '"messages": [{"role": "user", "content": prompt}],',
            '"messages": messages,',
        )
    )

    new_generate = (
        OLD_GENERATE_HEAD
        + preamble[len(OLD_GENERATE_HEAD):]
        + "        return self._call_messages(\n"
        + "            api_key, [{\"role\": \"user\", \"content\": prompt}]\n"
        + "        )\n"
        + "\n"
        + "    def generate_with_system(self, article, system_prompt: str, user_prompt: str) -> Analysis:\n"
        + f"        api_key = os.environ.get({env_var!r})\n"
        + "        if not api_key:\n"
        + "            raise ProviderUnavailable(\n"
        + f"                \"{env_var} is not set.\"\n"
        + "            )\n"
        + "        return self._call_messages(\n"
        + "            api_key,\n"
        + "            [\n"
        + "                {\"role\": \"system\", \"content\": system_prompt},\n"
        + "                {\"role\": \"user\", \"content\": user_prompt},\n"
        + "            ],\n"
        + "        )\n"
        + "\n"
        + new_call_method
    )

    old_full_method = src[start:end]
    src = src.replace(old_full_method, new_generate, 1)
    path.write_text(src, encoding="utf-8")
    print(f"{path} patched, new size:", len(src))

patch_openai_compatible_generator(Path("src/bsi_benchmark/generation/openrouter.py"), "OPENROUTER_API_KEY")
patch_openai_compatible_generator(Path("src/bsi_benchmark/generation/groq.py"), "GROQ_API_KEY")

# ===========================================================================
# PART 3: comparison/judge.py -- split the judge prompt into
#          system_prompt (rules + glossary) / user_prompt (RAW/BSI only),
#          call generate_with_system(), and fix the glossary source to use
#          the canonical load_full_glossary() instead of a hardcoded path
#          to an experimental candidate file.
# ===========================================================================
JUDGE_PATH = Path("src/bsi_benchmark/comparison/judge.py")
src = JUDGE_PATH.read_text(encoding="utf-8")

if "generate_with_system(article, system_prompt, user_prompt)" in src:
    print("judge.py: already patched -- skipped")
else:
    OLD_IMPORTS_CANDIDATES = [
        (
            "from pathlib import Path\n"
            "import json\n"
            "\n"
            "from bsi_benchmark import config\n"
            "from bsi_benchmark.comparison.glossary import load_full_glossary\n"
        ),
        (
            "import json\n"
            "\n"
            "from bsi_benchmark import config\n"
            "from bsi_benchmark.comparison.glossary import load_full_glossary\n"
        ),
    ]
    NEW_IMPORTS = (
        "import json\n"
        "\n"
        "from bsi_benchmark.comparison.glossary import load_full_glossary\n"
    )
    replaced_imports = False
    for old in OLD_IMPORTS_CANDIDATES:
        if src.count(old) == 1:
            src = src.replace(old, NEW_IMPORTS, 1)
            replaced_imports = True
            break
    if not replaced_imports:
        raise SystemExit(
            "judge.py: could not find a matching import block -- aborting "
            "without writing anything so nothing gets silently corrupted. "
            "Send this error back for a manual patch."
        )

    START_MARKER = "    def _compare_with_llm(self, article, raw_text, bsi_text):\n"
    END_MARKER = "\n        result = self.generator.generate(article, prompt)\n"

    if START_MARKER not in src or END_MARKER not in src:
        raise SystemExit(
            "judge.py: expected method markers not found -- judge.py has "
            "likely drifted further since this patch was written. Aborting "
            "without writing anything. Send the current file content back "
            "for a manual patch."
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
    print("judge.py patched OK, new size:", len(src))
