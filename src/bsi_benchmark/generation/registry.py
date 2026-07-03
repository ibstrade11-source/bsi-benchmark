from bsi_benchmark.common.registry import Registry
from .base import AnalysisGenerator
from .mock import MockGenerator
from .anthropic import AnthropicGenerator
from .openai import OpenAIGenerator

registry = Registry()

registry.register("mock", MockGenerator)
registry.register("anthropic", AnthropicGenerator)
registry.register("openai", OpenAIGenerator)

print("✅ Registry ready")
