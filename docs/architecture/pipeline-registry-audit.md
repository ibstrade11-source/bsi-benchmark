# Pipeline / Registry Architecture Audit

Generated from the current working tree.

## Scope

This audit examines pipeline wiring, provider/parser registries, generation registries and managers for unnecessary duplication or parallel orchestration paths.

## Pipeline Runner

- Path: `src/bsi_benchmark/pipeline/runner.py`
- Classes: PipelineRunner
- Functions: __init__, run
- Relevant orchestration markers: Provider, Parser, Runner, Manager

## Provider Registry

- Path: `src/bsi_benchmark/providers/registry.py`
- Classes: ProviderRegistry
- Functions: __init__, register, get, names
- Relevant orchestration markers: registry, Provider, get\(, register\(

## Provider Manager

- Path: `src/bsi_benchmark/providers/manager.py`
- Classes: ProviderManager
- Functions: available, create
- Relevant orchestration markers: registry, Provider, Manager, get\(

## Provider Package

- Path: `src/bsi_benchmark/providers/__init__.py`
- Classes: —
- Functions: —
- Relevant orchestration markers: Provider, Manager

## Parser Registry

- Path: `src/bsi_benchmark/parsers/registry.py`
- Classes: ParserRegistry
- Functions: __init__, register, get, available
- Relevant orchestration markers: registry, Provider, Parser, get\(, register\(

## Parser Package

- Path: `src/bsi_benchmark/parsers/__init__.py`
- Classes: —
- Functions: —
- Relevant orchestration markers: registry

## Generation Registry

- Path: `src/bsi_benchmark/generation/registry.py`
- Classes: —
- Functions: —
- Relevant orchestration markers: registry, Generator, register\(

## Generation Manager

- Path: `src/bsi_benchmark/generation/manager.py`
- Classes: GeneratorManager
- Functions: available, create
- Relevant orchestration markers: registry, Provider, Generator, Manager, get\(

## Generation Package

- Path: `src/bsi_benchmark/generation/__init__.py`
- Classes: —
- Functions: —
- Relevant orchestration markers: registry, Generator, Manager

## Cross-Reference Search

### `ProviderRegistry`
- `src/bsi_benchmark/providers/registry.py:12`: `class ProviderRegistry:`
- `src/bsi_benchmark/providers/registry.py:26`: `registry = ProviderRegistry()`

### `ParserRegistry`
- `src/bsi_benchmark/parsers/registry.py:1`: `class ParserRegistry:`
- `src/bsi_benchmark/parsers/registry.py:16`: `registry = ParserRegistry()`

### `GenerationRegistry`
- No references found.

### `ProviderManager`
- `src/bsi_benchmark/pipeline/runner.py:1`: `from bsi_benchmark.providers import ProviderManager`
- `src/bsi_benchmark/pipeline/runner.py:12`: `self.providers = ProviderManager()`
- `src/bsi_benchmark/providers/__init__.py:1`: `from .manager import ProviderManager`
- `src/bsi_benchmark/providers/__init__.py:11`: `__all__ = ["ProviderManager"]`
- `src/bsi_benchmark/providers/manager.py:8`: `class ProviderManager:`

### `GenerationManager`
- No references found.

### `PipelineRunner`
- `src/bsi_benchmark/benchmark/runner.py:1`: `from bsi_benchmark.pipeline import PipelineRunner`
- `src/bsi_benchmark/benchmark/runner.py:9`: `self.pipeline = PipelineRunner()`
- `src/bsi_benchmark/cli.py:220`: `from bsi_benchmark.pipeline import PipelineRunner`
- `src/bsi_benchmark/cli.py:244`: `dataset = PipelineRunner().run(`
- `src/bsi_benchmark/datasets/builder.py:1`: `from bsi_benchmark.pipeline import PipelineRunner`
- `src/bsi_benchmark/datasets/builder.py:10`: `self.runner = PipelineRunner()`
- `src/bsi_benchmark/parsers/mock.py:12`: `PipelineRunner.parsers, so it always raised KeyError.`
- `src/bsi_benchmark/pipeline/__init__.py:1`: `from .runner import PipelineRunner`
- `src/bsi_benchmark/pipeline/runner.py:10`: `class PipelineRunner:`

### `registry.register`
- `src/bsi_benchmark/export/html.py:44`: `registry.register("html", HtmlReport())`
- `src/bsi_benchmark/export/json_exporter.py:19`: `registry.register("json", JsonExporter())`
- `src/bsi_benchmark/export/markdown_exporter.py:26`: `registry.register("md", MarkdownExporter())`
- `src/bsi_benchmark/export/markdown_exporter.py:27`: `registry.register("markdown", MarkdownExporter())`
- `src/bsi_benchmark/frameworks/registry.py:72`: `registry.register(Framework(`
- `src/bsi_benchmark/generation/registry.py:16`: `registry.register("mock", MockGenerator)`
- `src/bsi_benchmark/generation/registry.py:17`: `registry.register("anthropic", AnthropicGenerator)`
- `src/bsi_benchmark/generation/registry.py:18`: `registry.register("openai", OpenAIGenerator)`
- `src/bsi_benchmark/generation/registry.py:19`: `registry.register("deepseek", DeepSeekGenerator)`
- `src/bsi_benchmark/generation/registry.py:20`: `registry.register("bsi_api", BSIAPIGenerator)`
- `src/bsi_benchmark/generation/registry.py:21`: `registry.register("local", LocalGenerator)`
- `src/bsi_benchmark/generation/registry.py:22`: `registry.register("gemini", GeminiGenerator)`
- `src/bsi_benchmark/generation/registry.py:23`: `registry.register("gemini-pro", lambda **kw: GeminiGenerator(model="gemini-2.5-pro", **kw))`
- `src/bsi_benchmark/generation/registry.py:24`: `registry.register("groq", GroqGenerator)`
- `src/bsi_benchmark/generation/registry.py:25`: `registry.register("openrouter", OpenRouterGenerator)`
- `src/bsi_benchmark/generation/registry.py:26`: `registry.register("openrouter-gemma", lambda **kw: OpenRouterGenerator(model="google/gemma-4-31b-it:free", **kw))`
- `src/bsi_benchmark/generation/registry.py:27`: `registry.register("openrouter-gpt", lambda **kw: OpenRouterGenerator(model="openai/gpt-oss-20b:free", **kw))`
- `src/bsi_benchmark/generation/registry.py:28`: `registry.register("gapgpt", GapGptGenerator)`
- `src/bsi_benchmark/parsers/arxiv.py:57`: `registry.register("arxiv", ArxivParser())`
- `src/bsi_benchmark/parsers/crossref.py:55`: `registry.register("crossref", CrossrefParser())`
- `src/bsi_benchmark/parsers/mock.py:22`: `registry.register("mock", MockParser())`
- `src/bsi_benchmark/parsers/openalex.py:64`: `registry.register("openalex", OpenAlexParser())`
- `src/bsi_benchmark/providers/arxiv.py:42`: `registry.register(ArxivProvider)`
- `src/bsi_benchmark/providers/crossref.py:45`: `registry.register(CrossrefProvider)`
- `src/bsi_benchmark/providers/europepmc.py:42`: `registry.register(EuropePMCProvider)`
- `src/bsi_benchmark/providers/mock.py:12`: `registry.register(MockProvider)`
- `src/bsi_benchmark/providers/openalex.py:41`: `registry.register(OpenAlexProvider)`
- `src/bsi_benchmark/providers/semantic_scholar.py:44`: `registry.register(SemanticScholarProvider)`
- `src/bsi_benchmark/providers/single_article.py:40`: `registry.register(SingleArticleProvider)`
- `src/bsi_benchmark/reporting/csv_reporter.py:19`: `registry.register(CsvReporter())`
- `src/bsi_benchmark/reporting/json_reporter.py:21`: `registry.register(JsonReporter())`

### `registry.get`
- `src/bsi_benchmark/cli.py:412`: `fw = registry.get(name)`
- `src/bsi_benchmark/evaluation/engine.py:7`: `evaluator = registry.get(name)`
- `src/bsi_benchmark/export/manager.py:7`: `exporter = registry.get(fmt)`
- `src/bsi_benchmark/generation/manager.py:14`: `cls = registry.get(name)`
- `src/bsi_benchmark/providers/manager.py:14`: `cls = registry.get(name)`
- `src/bsi_benchmark/reporting/manager.py:7`: `return registry.get(reporter).generate(result)`

## Architectural Assessment

The audit is intentionally non-invasive.

The following conditions are considered acceptable:

1. Registries own registration and lookup.
2. Managers coordinate provider/generator selection without reimplementing transport or parsing.
3. PipelineRunner coordinates execution rather than owning provider-specific HTTP or parser logic.
4. Provider/parser separation remains intact.
5. Generator implementations remain behind the generation registry.

No refactor should be performed solely because multiple components contain similar lookup or orchestration code. A change is justified only when duplicated behavior is semantically equivalent and can be extracted without changing CLI, result, provenance, or error behavior.

## Conclusion

This document records the current architecture so future refactors can be based on evidence rather than structural similarity alone.
