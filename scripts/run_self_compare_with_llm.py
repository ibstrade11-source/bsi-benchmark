#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bsi_benchmark.generation import GeneratorManager  # noqa: E402

SELF_COMPARE_PROMPT_PATH = Path(__file__).resolve().parent.parent / "examples" / "self_compare_prompt.md"

JSON_OUTPUT_INSTRUCTIONS = """
## دستور نهایی مهم برای همین اجرا

خروجی خودت را **فقط و فقط** به‌صورت یک شیء JSON معتبر بده -- بدون ```json،
بدون هیچ متن قبل یا بعدش، دقیقاً با همان کلیدهایی که در «فرمت خروجی لازم»
بالا توصیف شده (article, analyst_model, criteria_rationale, criteria,
overall_winner, overall_reasoning, raw_analysis_text, bsi_analysis_text).
عنوان مقاله و متن دو تحلیل (raw و bsi) که باید مقایسه کنی، همین‌جا زیر
آورده شده -- این‌ها را عیناً در raw_analysis_text و bsi_analysis_text هم
برگردان.

عنوان مقاله: {title}

--- متن تحلیل raw ---
{raw_text}

--- متن تحلیل bsi ---
{bsi_text}
"""


def build_prompt(title: str, raw_text: str, bsi_text: str) -> str:
    instructions = SELF_COMPARE_PROMPT_PATH.read_text(encoding="utf-8")
    tail = JSON_OUTPUT_INSTRUCTIONS.format(title=title, raw_text=raw_text, bsi_text=bsi_text)
    return instructions + "\n\n" + tail


def strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--raw-file", required=True, type=Path)
    parser.add_argument("--bsi-file", required=True, type=Path)
    parser.add_argument("--generator", default="gemini",
                         help="Which registered generator to use as judge (default: gemini)")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    raw_text = args.raw_file.read_text(encoding="utf-8")
    bsi_text = args.bsi_file.read_text(encoding="utf-8")

    prompt = build_prompt(args.title, raw_text, bsi_text)

    generator = GeneratorManager().create(args.generator)

    print(f"Calling {args.generator} as judge (this hits a real API)...")

    if args.generator == "gemini":
        import os
        from bsi_benchmark.network import HttpClient
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        client = HttpClient()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{generator.model}:generateContent"
        response = client.post(
            url,
            json_body={"contents": [{"parts": [{"text": prompt}]}]},
            headers={"x-goog-api-key": api_key, "content-type": "application/json"},
        )
        if not response.ok:
            print(f"Gemini HTTP {response.status_code}: {response.body}", file=sys.stderr)
            sys.exit(1)
        payload = json.loads(response.body)
        candidates = payload.get("candidates") or []
        raw_reply = "".join(
            part.get("text", "")
            for candidate in candidates
            for part in candidate.get("content", {}).get("parts", [])
        )
    elif args.generator == "groq":
        import os
        from bsi_benchmark.network import HttpClient
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("GROQ_API_KEY not set.", file=sys.stderr)
            sys.exit(1)
        client = HttpClient()
        response = client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json_body={
                "model": generator.model,
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        if not response.ok:
            print(f"Groq HTTP {response.status_code}: {response.body}", file=sys.stderr)
            sys.exit(1)
        payload = json.loads(response.body)
        raw_reply = payload["choices"][0]["message"]["content"]
    else:
        print(f"This script only wires up 'gemini' and 'groq' as judges "
              f"today; '{args.generator}' would need its own branch here.",
              file=sys.stderr)
        sys.exit(1)

    cleaned = strip_code_fences(raw_reply)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        print(f"Judge did not return valid JSON: {exc}\n\n--- raw reply ---\n{raw_reply}",
              file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Criteria chosen by {args.generator}: "
          f"{[c.get('criterion') for c in parsed.get('criteria', [])]}")
    print(f"Next: bsi-benchmark self-compare --input {args.output} "
          f"--output results/self_compare/<name>")


if __name__ == "__main__":
    main()
