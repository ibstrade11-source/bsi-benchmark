from bsi_benchmark.parsers.europepmc import EuropePMCParser
from bsi_benchmark.parsers.semantic_scholar import SemanticScholarParser


def test_europepmc_parser_keeps_fulltext_url_out_of_full_text():
    raw = {
        "resultList": {
            "result": [{
                "title": "Test Article",
                "abstractText": "Test abstract.",
                "doi": "10.1234/test",
                "source": "MED",
                "id": "123",
                "fullTextUrlList": {
                    "fullTextUrl": [{"url": "https://example.org/fulltext.pdf"}]
                },
            }]
        }
    }
    article = EuropePMCParser().parse(raw)[0]
    assert article.title == "Test Article"
    assert article.abstract == "Test abstract."
    assert article.full_text is None
    assert article.url == "https://europepmc.org/article/MED/123"
    assert article.input_quality["has_full_text"] is False


def test_semantic_scholar_parser_preserves_metadata_without_fake_fulltext():
    raw = {
        "data": [{
            "title": "Test Paper",
            "abstract": "Test abstract.",
            "externalIds": {"DOI": "10.1234/test"},
            "url": "https://www.semanticscholar.org/paper/test",
        }]
    }
    article = SemanticScholarParser().parse(raw)[0]
    assert article.title == "Test Paper"
    assert article.abstract == "Test abstract."
    assert article.doi == "10.1234/test"
    assert article.full_text is None
    assert article.input_quality["has_full_text"] is False
