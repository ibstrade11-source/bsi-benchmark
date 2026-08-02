
"""
Command-line interface for BSI Benchmark.
"""

import argparse
import os

from .version import __version__
from .benchmark import BenchmarkRunner
from .export import ExportManager
from bsi_benchmark.errors import ProviderError


def main() -> int:

    parser = argparse.ArgumentParser(prog="bsi-benchmark")

    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser(
        "run",
        help="Fetch articles for a query and run a Dataset-level evaluator "
             "(currently only 'basic', which counts articles).",
    )

    run.add_argument("--provider", required=True)
    run.add_argument("--query", required=True)
    run.add_argument("--format", default=None)
    run.add_argument("--output", default=None)

    evaluate = sub.add_parser(
        "evaluate",
        help="Score a BSI-generated analysis against its source article "
             "using the 'bsi' evaluator. Input is a JSON file matching the "
             "AnalyzedDataset schema (see datasets/analyzed_dataset.py) -- "
             "for a single pre-generated analysis. For an automated "
             "multi-model benchmark run, use 'compare' instead.",
    )
    evaluate.add_argument(
        "--input",
        required=True,
        help="Path to an AnalyzedDataset JSON file.",
    )

    compare = sub.add_parser(
        "compare",
        help="Automated benchmark: fetch articles, call one or more LLM "
             "generators under one or more prompt modes (e.g. raw vs bsi), "
             "score every combination with the BSI evaluator, and produce "
             "a comparison report. Requires the relevant API key env var "
             "(ANTHROPIC_API_KEY / OPENAI_API_KEY) for real generators, or "
             "use --generators mock for an offline dry run.",
    )
    compare.add_argument("--provider", required=True, help="e.g. crossref, arxiv, mock")
    compare.add_argument("--query", required=True)
    compare.add_argument(
        "--generators", required=True,
        help="Comma-separated generator names registered in generation.registry "
             "(e.g. 'anthropic,openai' or 'mock' for an offline dry run).",
    )
    compare.add_argument(
        "--raw-prompt-file",
        help="Path to a plain baseline prompt template ({title}/{abstract} "
             "placeholders). If omitted, a generic default is used.",
    )
    compare.add_argument(
        "--bsi-prompt-file",
        required=True,
        help="Path to the BSI master prompt template ({title}/{abstract} "
             "placeholders), e.g. a copy of MASTER_PROMPT_BSI_v3.4.2.md "
             "from the main BSI repository. Not fabricated by this tool -- "
             "supply the real prompt you want benchmarked.",
    )
    compare.add_argument(
        "--bsi-source-url",
        default="https://github.com/ibstrade11-source/behmanesh-index-prompt/blob/main/MASTER_PROMPT_BSI_v3.4.2.md",
        help="Link to the canonical BSI prompt file, printed in the report "
             "so readers can go read the exact unedited prompt themselves. "
             "Override if you benchmarked against a different branch/file, "
             "e.g. .../blob/conceptual-refactor-volume1/MASTER_PROMPT_BSI_v3.4.2.md. "
             "Pass '' to omit the link entirely.",
    )
    compare.add_argument(
        "--temperature", type=float, default=None,
        help="Record the generation temperature used, if you know it "
             "(this tool does not set it -- it just records it in "
             "run_metadata so 'GPT-5.5' alone is never the whole "
             "provenance record).",
    )
    compare.add_argument(
        "--max-tokens", type=int, default=None,
        help="Record the max_tokens setting used, if you know it.",
    )
    compare.add_argument(
        "--prompt-version", default=None,
        help="Record a version label for the prompt used (e.g. "
             "'v3.4.2'), if you want it distinguishable in stored "
             "records from other prompt versions later.",
    )
    compare.add_argument("--output", required=True, help="Output file path prefix (writes .md and .json).")

    self_compare = sub.add_parser(
        "self-compare",
        help="Record an analyst's own comparison of their raw-vs-bsi "
             "analysis of one article. The analyst chooses their own "
             "criteria (this tool imposes no rubric) and supplies a "
             "raw_score/bsi_score per criterion; the winner per criterion "
             "is derived from those two scores, not separately asserted. "
             "Input is a JSON file -- see examples/self_compare_example.json "
             "for the expected shape and examples/self_compare_prompt.md "
             "for the instructions to give the analyst.",
    )
    self_compare.add_argument(
        "--input", required=True,
        help="Path to a self-comparison JSON file filled in by the analyst.",
    )
    self_compare.add_argument(
        "--output", required=True,
        help="Output file path prefix (writes .md and .json). The .json "
             "output is the canonical stored record (results/ is the "
             "conventional place to keep these); the .md is for reading.",
    )

    stats = sub.add_parser(
        "stats",
        help="Aggregate multiple self-compare JSON records (from "
             "'self-compare' output) into descriptive statistics: mean "
             "raw/bsi scores, bootstrap 95%% CI on the difference, "
             "Cohen's d_z, and a Wilcoxon signed-rank test. Pure Python, "
             "no scipy dependency (so it runs on Termux). Purely "
             "descriptive of the self-reported data -- see the caveats "
             "section of its own output for what it does NOT establish.",
    )
    stats.add_argument(
        "--input", required=True, nargs="+",
        help="One or more self-compare .json record files (the output "
             "of 'self-compare --output ...'), e.g. results/self_compare/*.json",
    )
    stats.add_argument("--output", required=True, help="Output file path prefix (writes .md).")

    frameworks = sub.add_parser(
        "frameworks",
        help="List analysis frameworks registered with this tool. Today "
             "only 'bsi' is registered end-to-end; this command exists "
             "so the tool's framework list is inspectable rather than "
             "hardcoded and invisible -- see ROADMAP.md for the plan to "
             "add more.",
    )

    args = parser.parse_args()

    print(f"BSI Benchmark {__version__}")

    if args.command == "run":

        runner = BenchmarkRunner()

        try:
            result = runner.run(
                args.provider,
                args.query,
            )
        except ProviderError as e:
            print(f"ERROR: {e}")
            return 1

        print(f"Provider : {result.dataset.provider}")
        print(f"Query    : {result.dataset.query}")
        print(f"Articles : {len(result.dataset.articles)}")

        # export integration (Ma's local addition, kept)
        if args.format and args.output:
            ExportManager().export(
                result,
                args.format,
                args.output,
            )
            print(f"Report written to {args.output}")

        return 0

    if args.command == "evaluate":
        from bsi_benchmark.datasets import AnalyzedDatasetIO
        from bsi_benchmark.evaluation import EvaluationEngine

        dataset = AnalyzedDatasetIO().load(args.input)
        engine = EvaluationEngine()

        print(f"Dataset  : {dataset.name}")
        print(f"Items    : {dataset.size}")
        print()

        for i, item in enumerate(dataset.items, start=1):
            result = engine.evaluate("bsi", item)
            title = item.article.title or "(untitled)"
            print(f"[{i}] {title}")
            for dim in ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "BSI"):
                print(f"    {dim:16s} {result.scores[dim]:.3f}")
            print(f"    {'grounding_ratio':16s} {result.scores['grounding_ratio']:.3f}")
            print(f"    {'tag_coverage':16s} {result.scores['tag_coverage']:.3f}")
            print()

        return 0

    if args.command == "compare":
        from bsi_benchmark.pipeline import PipelineRunner
        from bsi_benchmark.comparison import ComparisonSpec, CrossModelRunner, render_markdown
        from bsi_benchmark.comparison.json_export import save as save_json
        from bsi_benchmark.prompt_loader import load_bsi_prompt
        from bsi_benchmark.run_metadata import RunMetadata
        from dataclasses import asdict as _asdict

        DEFAULT_RAW_PROMPT = (
            "Analyze the following academic article. Give a concise, "
            "factual analysis of its main claims and contribution.\n\n"
            "Title: {title}\nAbstract: {abstract}"
        )

        raw_prompt = DEFAULT_RAW_PROMPT
        if args.raw_prompt_file:
            raw_prompt = load_bsi_prompt(args.raw_prompt_file, label="raw-prompt-file")

        # Permanent fix: a raw copy of MASTER_PROMPT_BSI_v3.4.2.md (or any
        # other BSI master prompt) has no {title}/{abstract} placeholders.
        # load_bsi_prompt() auto-appends them if missing, so the file can
        # be used exactly as downloaded -- no manual edit required.
        bsi_prompt = load_bsi_prompt(args.bsi_prompt_file, label="bsi-prompt-file")

        try:
            dataset = PipelineRunner().run(args.provider, args.query)
        except ProviderError as e:
            print(f"ERROR fetching dataset: {e}")
            return 1

        spec = ComparisonSpec(
            generators=[g.strip() for g in args.generators.split(",") if g.strip()],
            prompt_modes={"raw": raw_prompt, "bsi": bsi_prompt},
        )

        print(f"Provider   : {dataset.provider}")
        print(f"Query      : {dataset.query}")
        print(f"Articles   : {len(dataset.articles)}")
        print(f"Generators : {', '.join(spec.generators)}")
        print(f"Modes      : {', '.join(spec.prompt_modes.keys())}")
        print("Running... (this calls a real API for each non-mock generator; may take a while)")
        print()

        report = CrossModelRunner().run(
            dataset, spec,
            source_url=args.bsi_source_url or None,
            run_metadata=_asdict(RunMetadata.capture(
                repo_dir=os.path.dirname(os.path.abspath(__file__)),
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                prompt_version=args.prompt_version,
            )),
        )

        md_path = f"{args.output}.md"
        json_path = f"{args.output}.json"

        out_dir = os.path.dirname(md_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(render_markdown(report))
        save_json(report, json_path)

        print(f"Wrote {md_path}")
        print(f"Wrote {json_path}")

        return 0

    if args.command == "self-compare":
        from bsi_benchmark.self_compare import SelfComparisonIO, render_markdown as render_self_compare_md
        from bsi_benchmark.run_metadata import RunMetadata
        from dataclasses import asdict as _asdict

        io = SelfComparisonIO()
        try:
            record = io.load(args.input)
        except (ValueError, FileNotFoundError, KeyError) as e:
            print(f"ERROR reading self-compare input: {e}")
            return 1

        if record.run_metadata is None:
            record.run_metadata = _asdict(
                RunMetadata.capture(repo_dir=os.path.dirname(os.path.abspath(__file__)))
            )

        print(f"Article        : {record.article_title}")
        print(f"Analyst        : {record.analyst_model}")
        print(f"Criteria       : {len(record.criteria)}")
        print(f"raw wins / bsi wins / ties : {record.raw_wins()} / {record.bsi_wins()} / {record.ties()}")
        print(f"Overall winner : {record.overall_winner}")
        if not record.has_source_texts():
            print(
                "WARNING: raw_analysis_text/bsi_analysis_text missing -- "
                "this record's scores are self-reported only, not checkable "
                "against the actual analysis text."
            )
        print()

        md_path = f"{args.output}.md"
        json_path = f"{args.output}.json"

        out_dir = os.path.dirname(md_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(render_self_compare_md(record))
        io.save(record, json_path)

        print(f"Wrote {md_path}")
        print(f"Wrote {json_path}")

        return 0

    if args.command == "stats":
        from bsi_benchmark.self_compare import SelfComparisonIO
        from bsi_benchmark.stats import aggregate, render_markdown as render_stats_md

        io = SelfComparisonIO()
        records = []
        for path in args.input:
            try:
                records.append(io.load(path))
            except (ValueError, FileNotFoundError, KeyError) as e:
                print(f"ERROR reading '{path}': {e}")
                return 1

        if not records:
            print("ERROR: no input records loaded.")
            return 1

        result = aggregate(records)

        print(f"Records : {result.n_records}")
        print(f"Pairs   : {result.n}")
        print(f"Mean diff (bsi - raw) : {result.mean_diff:.3f}")
        if result.ci95_low is not None:
            print(f"95% CI  : [{result.ci95_low:.3f}, {result.ci95_high:.3f}]")
        if result.wilcoxon_p_approx is not None:
            print(f"Wilcoxon p (approx) : {result.wilcoxon_p_approx:.4f}")
        print()

        md_path = f"{args.output}.md"
        out_dir = os.path.dirname(md_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(render_stats_md(result))

        print(f"Wrote {md_path}")

        return 0

    if args.command == "frameworks":
        from bsi_benchmark.frameworks import registry

        names = registry.list_names()
        if not names:
            print("No frameworks registered.")
            return 0

        print(f"{len(names)} framework(s) registered:\n")
        for name in names:
            fw = registry.get(name)
            print(f"- {fw.name} (version: {fw.version or 'unknown'})")
            print(f"  {fw.description}")
            print()

        return 0

    parser.print_help()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
