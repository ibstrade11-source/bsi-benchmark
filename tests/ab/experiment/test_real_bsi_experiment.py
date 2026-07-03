import os

import pytest

from bsi_benchmark.ab.experiment.engine import ExperimentEngine
from bsi_benchmark.ab.runner import ABRunner
from bsi_benchmark.ab.llm.adapter import LLMAdapter
from bsi_benchmark.ab.llm.bsi_adapter import BSILLMAdapter
from bsi_benchmark.ab.llm.base import BaseLLM


class EchoLLM(BaseLLM):

    def generate(self, prompt):
        return prompt


@pytest.mark.integration
def test_real_bsi_experiment():

    if os.environ.get("BSI_API") != "1":
        pytest.skip("BSI API not enabled")

    runner = ABRunner(
        LLMAdapter(EchoLLM()),
        LLMAdapter(BSILLMAdapter()),
    )

    engine = ExperimentEngine(runner)

    result = engine.run(
        "Artificial intelligence is transforming science."
    )

    assert len(result.baseline) > 0
    assert len(result.treatment) > 0
