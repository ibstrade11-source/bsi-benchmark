
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
    compare.add_argument("--output", required=True, help="Output file path prefix (writes .md and .json).")

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

        DEFAULT_RAW_PROMPT = (
            "Analyze the following academic article. Give a concise, "
            "factual analysis of its main claims and contribution.\n\n"
            "Title: {title}\nAbstract: {abstract}"
        )

        raw_prompt = DEFAULT_RAW_PROMPT
        if args.raw_prompt_file:
            with open(args.raw_prompt_file, encoding="utf-8") as f:
                raw_prompt = f.read()

        with open(args.bsi_prompt_file, encoding="utf-8") as f:
            bsi_prompt = f.read()

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

        report = CrossModelRunner().run(dataset, spec)

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

    parser.print_help()

    return 0
