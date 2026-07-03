from bsi_benchmark.generation import GeneratorManager


def test_generator_manager_lists_all_backends():
    names = GeneratorManager().available()
    assert set(names) == {"mock", "anthropic", "openai", "deepseek", "bsi_api"}


def test_generator_manager_creates_mock_instance():
    gen = GeneratorManager().create("mock")
    assert gen.name == "mock"
