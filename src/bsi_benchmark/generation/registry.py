from bsi_benchmark.common import Registry

from .mock import MockGenerator
from .anthropic import AnthropicGenerator
from .openai import OpenAIGenerator
from .deepseek import DeepSeekGenerator
from .bsi_api import BSIAPIGenerator

registry: Registry = Registry()

registry.register("mock", MockGenerator)
registry.register("anthropic", AnthropicGenerator)
registry.register("openai", OpenAIGenerator)
registry.register("deepseek", DeepSeekGenerator)
registry.register("bsi_api", BSIAPIGenerator)
