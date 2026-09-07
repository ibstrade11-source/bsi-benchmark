import json

from bsi_benchmark.pipeline import PipelineRunner


def _openalex_response(items):
    return json.dumps({"results": items})


def _item(title, doi):
    # OpenAlex parser requires a reconstructable abstract.
    return {
        "title": title,
        "doi": doi,
        "id": f"https://openalex.org/{doi.replace('/', '_')}",
        "abstract_inverted_index": {
            "This": [0],
            "is": [1],
            "a": [2],
            "deterministic": [3],
            "abstract": [4],
        },
    }


def test_title_query_rejects_wrong_openalex_result(monkeypatch):
    query = "A Long History: From Universal Language to Artificial Intelligence"

    wrong = _item(
        "Artificial Intelligence (AI): Multidisciplinary perspectives on "
        "emerging challenges, opportunities, and agenda for research, "
        "practice and policy",
        "https://doi.org/10.1016/j.ijinfomgt.2019.08.002",
    )

    class FakeResponse:
        ok = True
        status_code = 200
        body = _openalex_response([wrong])

    monkeypatch.setattr(
        "bsi_benchmark.network.HttpClient.get",
        lambda self, url, *args, **kwargs: FakeResponse(),
    )

    result = PipelineRunner().run("openalex", query)

    assert result.articles == []
    assert result.retrieval_status == "invalid"
    assert result.retrieval_validation["reason"] == "title_query_mismatch"
    assert result.rejected_articles
    assert result.rejected_articles[0]["status"] == "invalid_retrieval"


def test_title_query_can_select_matching_later_candidate(monkeypatch):
    query = "A Long History: From Universal Language to Artificial Intelligence"

    wrong = _item(
        "Artificial Intelligence: Multidisciplinary perspectives and agenda",
        "https://doi.org/10.0000/wrong",
    )
    correct = _item(
        "A Long History: From Universal Language to Artificial Intelligence",
        "https://doi.org/10.0000/correct",
    )

    class FakeResponse:
        ok = True
        status_code = 200
        body = _openalex_response([wrong, correct])

    monkeypatch.setattr(
        "bsi_benchmark.network.HttpClient.get",
        lambda self, url, *args, **kwargs: FakeResponse(),
    )

    result = PipelineRunner().run("openalex", query, limit=1)

    assert len(result.articles) == 1
    assert result.articles[0].title == query
    assert result.retrieval_status == "accepted"
    assert result.retrieval_validation["selected_rank"] == 2


def test_topic_query_is_not_rejected_as_title_query(monkeypatch):
    query = "quantum physics"

    item = _item(
        "Quantum physics and modern research",
        "https://doi.org/10.0000/topic",
    )

    class FakeResponse:
        ok = True
        status_code = 200
        body = _openalex_response([item])

    monkeypatch.setattr(
        "bsi_benchmark.network.HttpClient.get",
        lambda self, url, *args, **kwargs: FakeResponse(),
    )

    result = PipelineRunner().run("openalex", query)

    assert len(result.articles) == 1
    assert result.retrieval_status == "accepted"
    assert result.retrieval_validation["query_type"] == "topic"
