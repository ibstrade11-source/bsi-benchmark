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
