# Providers / Parsers Architecture

## Decision

Providers and parsers remain separate responsibilities.

### Providers

A provider is responsible for:

- building the upstream API request
- using the centralized `HttpClient`
- handling final HTTP failure as a provider-level error
- returning the raw upstream response

Providers must not contain parsing logic.

### Parsers

A parser is responsible for:

- decoding the raw provider response
- extracting article metadata
- normalizing source-specific fields into `Article`
- preserving provenance such as DOI and URL
- applying source-specific reconstruction/normalization rules

Parsers must not perform network requests.

## Current Architecture

The following providers use the centralized network layer:

- arxiv
- crossref
- openalex
- europepmc
- semantic_scholar

The following provider/parser pairs intentionally remain separate:

- arxiv: `ArxivProvider` + `ArxivParser`
- crossref: `CrossrefProvider` + `CrossrefParser`
- openalex: `OpenAlexProvider` + `OpenAlexParser`

This is not considered duplicated business logic. The provider owns transport/fetch semantics while the parser owns response interpretation.

## Why They Should Not Be Merged

Merging provider and parser implementations would couple:

1. transport behavior
2. HTTP retry behavior
3. provider error handling
4. response decoding
5. article normalization

Keeping them separate allows:

- parser testing with offline fixtures
- provider testing independently from parsing
- reuse of parsers with recorded responses
- centralized network resilience
- easier addition of alternative transport mechanisms
- clearer provenance and failure boundaries

## Architectural Invariants

1. All real HTTP traffic must go through `bsi_benchmark.network.HttpClient`.
2. Providers must not import `requests`, `httpx`, or `urllib.request` directly.
3. Parsers must not perform HTTP requests.
4. Provider failures are translated into the benchmark's provider-level error model.
5. Parsers convert source-specific payloads into the common `Article` model.
6. Provider/parser responsibilities must not be merged merely because they share a source name.

## Refactoring Rule

A future provider/parser refactor is justified only when semantic comparison demonstrates actual duplicated behavior that can be safely extracted into a shared component.

The existence of similarly named classes such as `ArxivProvider` and `ArxivParser` is not, by itself, duplication.

## Audit Result

Current inspection found:

- no same-named provider/parser functions requiring extraction
- no direct HTTP implementation outside `network/client.py`
- no evidence that provider/parser merging would reduce meaningful duplication
- the current separation is architecturally sound

Therefore no provider/parser merge is performed in this change.
