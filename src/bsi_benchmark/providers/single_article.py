"""
SingleArticleProvider: a fixed-output test fixture, not a real search
provider.

`search()` ignores its `query` argument entirely and always returns the
same one hardcoded article. This exists so pipeline/self-compare runs can
be pointed at a known, reproducible article (via provider name
"single_article", wired in pipeline/runner.py) without depending on a
live network call to a real bibliographic API -- useful for offline
smoke tests. It is registered in the same registry as the real
providers (crossref, arxiv, etc.) for that reason, but it must not be
mistaken for one: any real query passed to it is silently discarded.
"""
from .base import Provider
from .registry import registry


class SingleArticleProvider(Provider):
    name = "single_article"

    def search(self, query: str):
        return [
            {
                "title": "Oral microbiome signatures predict biological age and host health",
                "abstract": (
                    "Identifying robust, non-invasive biomarkers of biological age is key "
                    "to preventive medicine. Using oral microbiome data from two NHANES "
                    "cohorts (N=4675), researchers identified 64 age-dependent bacterial "
                    "genera and developed a machine learning model predicting chronological "
                    "age, validated in an independent cohort (N=1293). The study derived an "
                    "Oral Microbiome Aging Acceleration Score and examined associations "
                    "with mortality, frailty, kidney function, cancer and heart attack risk."
                ),
                "doi": "10.1038/s41467-026-72096-2",
                "url": "https://doi.org/10.1038/s41467-026-72096-2"
            }
        ]


registry.register(SingleArticleProvider)
