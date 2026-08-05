from bsi_benchmark.common import Registry

from .mock import MockGenerator
from .anthropic import AnthropicGenerator
from .openai import OpenAIGenerator
from .deepseek import DeepSeekGenerator
from .bsi_api import BSIAPIGenerator
from .local import LocalGenerator
from .gemini import GeminiGenerator
from .groq import GroqGenerator
from .openrouter import OpenRouterGenerator

registry: Registry = Registry()

registry.register("mock", MockGenerator)
registry.register("anthropic", AnthropicGenerator)
registry.register("openai", OpenAIGenerator)
registry.register("deepseek", DeepSeekGenerator)
registry.register("bsi_api", BSIAPIGenerator)
registry.register("local", LocalGenerator)
registry.register("gemini", GeminiGenerator)
registry.register("gemini-pro", lambda **kw: GeminiGenerator(model="gemini-2.5-pro", **kw))
registry.register("groq", GroqGenerator)
registry.register("openrouter", OpenRouterGenerator)
registry.register("openrouter-gemma", lambda **kw: OpenRouterGenerator(model="google/gemma-4-31b-it:free", **kw))
registry.register("openrouter-gpt", lambda **kw: OpenRouterGenerator(model="openai/gpt-oss-20b:free", **kw))
