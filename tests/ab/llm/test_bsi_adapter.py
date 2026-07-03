from unittest.mock import patch

from bsi_benchmark.ab.llm.bsi_adapter import BSILLMAdapter


def test_bsi_adapter():

    with patch(
        "bsi_benchmark.ab.client.BSIApiClient.analyze_llm"
    ) as mock:

        mock.return_value = {
            "final_synthesis": "analysis"
        }

        adapter = BSILLMAdapter()

        assert adapter.generate("hello") == "analysis"
