import os
from langchain_anthropic import ChatAnthropic
from ..interface import LLMProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ClaudeProvider(LLMProvider):
    def get_llm(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        model_name = os.getenv("CLAUDE_MODEL_NAME", "claude-3-5-sonnet-20241022")

        if not api_key:
            logger.critical("ANTHROPIC_API_KEY is missing.")
            raise ValueError("ANTHROPIC_API_KEY is missing.")

        logger.info(f"🟠 [Claude Provider] Initializing: {model_name}")

        try:
            return ChatAnthropic(
                model=model_name,
                api_key=api_key,
                temperature=0.5,
                verbose=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize Claude: {e}")
            raise e
