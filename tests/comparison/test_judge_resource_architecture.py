from types import SimpleNamespace

from bsi_benchmark.comparison.judge import LLMJudge
from bsi_benchmark.generation.groq import GroqGenerator
from bsi_benchmark.generation.mock import MockGenerator
from bsi_benchmark.generation.openrouter import OpenRouterGenerator
from bsi_benchmark.models.analysis import Analysis


ARTICLE = SimpleNamespace(
    title="Judge Resource Architecture Test",
    abstract="Deterministic test article.",
    doi=None,
)

RAW = Analysis(
    text="RAW analysis only.",
    source_model="mock",
    generated_at=None,
)

BSI = Analysis(
    text="BSI analysis only.",
    source_model="mock",
    generated_at=None,
)

RESOURCE = "UNIQUE_JUDGE_RESOURCE_SENTINEL_9X7Q"
SYSTEM = "JUDGE_INSTRUCTIONS_ONLY_ABC"
USER = "RAW_AND_BSI_COMPARISON_ONLY_XYZ"


def test_mock_judge_resource_is_not_prompt_interpolated():
    generator = MockGenerator()

    result = generator.generate_with_judge_resource(
        ARTICLE,
        SYSTEM,
        USER,
        RESOURCE,
    )

    assert result is not None
    assert result.text
    # MockGenerator produces a deterministic judge response; it does not
    # echo the transport prompts. The important contract here is that the
    # independent resource does not become part of the generated result.
    assert RESOURCE not in result.text


def test_llm_judge_passes_resource_separately_to_generator():
    class CapturingGenerator(MockGenerator):
        def __init__(self):
            self.captured = None

        def generate_with_judge_resource(
            self,
            article,
            system_prompt,
            user_prompt,
            judge_resource=None,
        ):
            self.captured = {
                "system": system_prompt,
                "user": user_prompt,
                "resource": judge_resource,
            }
            return super().generate_with_judge_resource(
                article,
                system_prompt,
                user_prompt,
                judge_resource,
            )

    generator = CapturingGenerator()

    result = LLMJudge(generator).compare(
        ARTICLE,
        RAW,
        BSI,
    )

    assert result["criteria_source"] == "llm"
    assert generator.captured is not None

    captured = generator.captured
    assert captured["resource"]
    assert captured["resource"] != captured["system"]
    assert captured["resource"] not in captured["system"]
    assert captured["resource"] not in captured["user"]

    assert "RAW ANALYSIS" in captured["user"]
    assert "BSI ANALYSIS" in captured["user"]


def _capture_provider_messages(Generator):
    generator = Generator()
    captured = {}

    def fake_call_messages(api_key, messages):
        captured["messages"] = messages
        return Analysis(
            text='{"criteria":[]}',
            source_model="test",
            generated_at=None,
        )

    generator._call_messages = fake_call_messages

    return generator, captured


def test_openrouter_judge_resource_uses_separate_system_message():
    generator, captured = _capture_provider_messages(OpenRouterGenerator)

    import os
    os.environ["OPENROUTER_API_KEY"] = "TEST_KEY"

    generator.generate_with_judge_resource(
        ARTICLE,
        SYSTEM,
        USER,
        RESOURCE,
    )

    messages = captured["messages"]

    assert len(messages) == 3
    assert [m["role"] for m in messages] == [
        "system",
        "system",
        "user",
    ]

    assert RESOURCE in messages[0]["content"]
    assert SYSTEM in messages[1]["content"]
    assert USER in messages[2]["content"]

    assert RESOURCE not in messages[1]["content"]
    assert RESOURCE not in messages[2]["content"]


def test_groq_judge_resource_uses_separate_system_message():
    generator, captured = _capture_provider_messages(GroqGenerator)

    import os
    os.environ["GROQ_API_KEY"] = "TEST_KEY"

    generator.generate_with_judge_resource(
        ARTICLE,
        SYSTEM,
        USER,
        RESOURCE,
    )

    messages = captured["messages"]

    assert len(messages) == 3
    assert [m["role"] for m in messages] == [
        "system",
        "system",
        "user",
    ]

    assert RESOURCE in messages[0]["content"]
    assert SYSTEM in messages[1]["content"]
    assert USER in messages[2]["content"]

    assert RESOURCE not in messages[1]["content"]
    assert RESOURCE not in messages[2]["content"]


def test_provider_identity_is_not_injected_into_judge_messages():
    for Generator, provider_name in (
        (OpenRouterGenerator, "OPENROUTER"),
        (GroqGenerator, "GROQ"),
    ):
        generator, captured = _capture_provider_messages(Generator)

        import os
        os.environ[
            "OPENROUTER_API_KEY" if provider_name == "OPENROUTER"
            else "GROQ_API_KEY"
        ] = "TEST_KEY"

        generator.generate_with_judge_resource(
            ARTICLE,
            SYSTEM,
            USER,
            RESOURCE,
        )

        for message in captured["messages"]:
            content = message["content"]
            assert "OPENROUTER_MODEL" not in content
            assert "GROQ_MODEL" not in content
            assert "source_model" not in content
            assert "generator_name" not in content
            assert "model_name" not in content
