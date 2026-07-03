"""
Loader for BSI prompt template files used by `bsi-benchmark compare`
(--bsi-prompt-file / --raw-prompt-file).

PROBLEM this fixes permanently:
`compare` formats each prompt with `.format(title=..., abstract=...)`, so
the file passed in must contain literal `{title}` / `{abstract}`
placeholders. A raw copy of MASTER_PROMPT_BSI_v3.4.2.md pulled straight
from the main behmanesh-index-prompt repository does NOT contain these
placeholders (it's a general-purpose system prompt, not a template for
this tool). Previously this required remembering a manual edit before
every real run, and forgetting it either crashed with a KeyError deep in
`.format()` or silently produced a prompt with no article content in it.

FIX: load_bsi_prompt() inspects the file and appends a clearly-delimited
placeholder block automatically if it's missing, so the *raw, unedited*
master prompt file works directly. The original master prompt content is
never rewritten in place on disk -- only the in-memory string used for
this run is modified. Nothing here fabricates or alters BSI's actual
analytical content; it only appends the mechanical {title}/{abstract}
slot the CLI needs to inject the article.
"""
from __future__ import annotations

PLACEHOLDER_BLOCK = (
    "\n\n---\n"
    "[bsi-benchmark: article injected below by the compare command]\n"
    "Title: {title}\n"
    "Abstract: {abstract}\n"
)


def load_bsi_prompt(path: str, *, label: str = "prompt-file") -> str:
    """
    Read a prompt template file and guarantee it contains {title}/{abstract}.

    - Both placeholders present -> returned unchanged.
    - Neither present -> PLACEHOLDER_BLOCK is appended (in memory only)
      and a notice is printed so the auto-templating is never silent.
    - Only one present -> raises ValueError rather than guessing, since
      that shape usually means a hand-edit went wrong.
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()

    has_title = "{title}" in content
    has_abstract = "{abstract}" in content

    if has_title and has_abstract:
        print(f"[{label}] '{path}': {{title}}/{{abstract}} placeholders found, using as-is.")
        return content

    if has_title or has_abstract:
        missing = "{abstract}" if has_title else "{title}"
        raise ValueError(
            f"[{label}] '{path}' has only one of {{title}}/{{abstract}} "
            f"(missing {missing}). This looks like a partial hand-edit -- "
            "fix it manually rather than have this tool guess."
        )

    print(
        f"[{label}] '{path}': no {{title}}/{{abstract}} placeholders found "
        "(looks like a raw BSI master prompt copy) -- auto-appending the "
        "article placeholder block for this run. The file on disk is not "
        "modified."
    )
    return content + PLACEHOLDER_BLOCK
