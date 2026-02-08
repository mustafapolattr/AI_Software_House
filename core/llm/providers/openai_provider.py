import os
from crewai import LLM
from ..interface import LLMProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIProvider(LLMProvider):
    def get_llm(self):
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

        if not api_key:
            logger.critical("OPENAI_API_KEY is missing.")
            raise ValueError("OPENAI_API_KEY is missing.")

        logger.info(f"🟢 [OpenAI Provider] Initializing: {model_name}")

        return LLM(
            model=model_name,
            api_key=api_key,
            temperature=0.5
        )
