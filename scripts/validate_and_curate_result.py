#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CURATED = RESULTS / "self_compare"

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True)

def valid_result(path):
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid JSON: {e}"]

    def walk(x):
        if isinstance(x, dict):
            if x.get("failed") is True:
                errors.append("failed=true")

            if x.get("error"):
                errors.append("error field present")

            if "judge_result" in x:
                j = x["judge_result"]
                if not isinstance(j, dict) or not j:
                    errors.append("missing judge_result")
                else:
                    if j.get("criteria_source") != "llm":
                        errors.append("judge is not LLM")
                    if not j.get("winner"):
                        errors.append("missing winner")
                    if not j.get("criteria"):
                        errors.append("missing criteria")
                    if not j.get("total_scores"):
                        errors.append("missing total_scores")
                    if not j.get("bsi_capability_assessment"):
                        errors.append("missing BSI capability assessment")

            for v in x.values():
                walk(v)

        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(data)
    return sorted(set(errors))

def main():
    CURATED.mkdir(parents=True, exist_ok=True)

    candidates = sorted(
        p for p in RESULTS.glob("*.json")
        if p.is_file()
    )

    curated = 0
    rejected = 0

    for src_json in candidates:
        src_md = src_json.with_suffix(".md")

        if not src_md.exists():
            continue

        errors = valid_result(src_json)

        if errors:
            rejected += 1
            print(f"INVALID: {src_json.name}")
            for e in errors:
                print(f"  - {e}")
            continue

        dst_json = CURATED / src_json.name
        dst_md = CURATED / src_md.name

        shutil.copy2(src_json, dst_json)
        shutil.copy2(src_md, dst_md)

        curated += 1
        print(f"CURATED: {src_json.name}")

    print()
    print(f"Valid curated results: {curated}")
    print(f"Rejected/invalid:       {rejected}")

    run(["git", "add", "results/self_compare",
         "scripts/validate_and_curate_result.py",
         "scripts/run_benchmark.sh"])

    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()

    if not staged:
        print("Nothing new to commit.")
        return 0

    print()
    print("===== STAGED FOR AUTOMATIC COMMIT =====")
    print(staged)

    run(["git", "diff", "--cached", "--check"])

    run([
        "git", "commit",
        "-m",
        "Automate validation and curation of benchmark results"
    ])

    print()
    print("===== COMMIT COMPLETE =====")
    run(["git", "status", "-sb"])

if __name__ == "__main__":
    main()
