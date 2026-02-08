from typing import Dict, Type, Optional
from .interface import LLMProvider
from .providers import GeminiProvider, OpenAIProvider, ClaudeProvider, DeepSeekProvider
from ..config import Config


class LLMFactory:
    _providers: Dict[str, Type[LLMProvider]] = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "deepseek": DeepSeekProvider
    }

    @classmethod
    def create(cls, provider_name: Optional[str] = None):
        """
        Creates an LLM instance.
        If provider_name is None, it uses the DEFAULT_LLM_PROVIDER from config.
        """
        if not provider_name:
            provider_name = Config.DEFAULT_LLM_PROVIDER

        provider_cls = cls._providers.get(provider_name.lower())

        if not provider_cls:
            available = list(cls._providers.keys())
            raise ValueError(f"Unknown LLM Provider: '{provider_name}'. Available: {available}")

        return provider_cls().get_llm()
