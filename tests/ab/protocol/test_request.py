from bsi_benchmark.ab.protocol.request import ABRequest


def test_request():

    req = ABRequest(
        provider="crossref",
        query="Artificial Intelligence",
    )

    assert req.provider == "crossref"
    assert req.query == "Artificial Intelligence"
    assert req.use_bsi is False
