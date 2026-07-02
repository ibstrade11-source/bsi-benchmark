from bsi_benchmark.common import Registry

from .mock import MockGenerator
from .anthropic import AnthropicGenerator
from .openai import OpenAIGenerator

registry: Registry = Registry()

registry.register("mock", MockGenerator)
registry.register("anthropic", AnthropicGenerator)
registry.register("openai", OpenAIGenerator)
