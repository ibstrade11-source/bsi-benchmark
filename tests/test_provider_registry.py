from bsi_benchmark.providers import ProviderManager


def test_provider_registry():

    pm = ProviderManager()

    names = pm.available()

    assert "crossref" in names
    assert "arxiv" in names
    assert "openalex" in names
