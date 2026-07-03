from bsi_benchmark.ab.protocol.response import ABResponse


def test_response():

    res = ABResponse(
        provider="crossref",
        query="AI",
        use_bsi=True,
        result={"bsi_score": 0.8},
    )

    assert res.use_bsi
    assert res.result["bsi_score"] == 0.8
