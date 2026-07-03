from bsi_benchmark.ab.llm.registry import LLMRegistry


def test_registry():

    registry = LLMRegistry()

    backend = object()

    registry.register("dummy", backend)

    assert registry.get("dummy") is backend
    assert registry.names() == ["dummy"]
