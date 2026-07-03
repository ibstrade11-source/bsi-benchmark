from bsi_benchmark.ab.protocol.request import ABRequest
from bsi_benchmark.ab.protocol.session import ABSession


def test_session():

    session = ABSession()

    req = ABRequest(
        provider="crossref",
        query="AI",
    )

    session.add(req, {"bsi_score": 0.7})

    assert len(session.history) == 1
    assert session.history[0].result["bsi_score"] == 0.7
