import os
from langchain_openai import ChatOpenAI
from ..interface import LLMProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)

class DeepSeekProvider(LLMProvider):
    def get_llm(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        model_name = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is missing in .env file.")

        logger.info(f"Initializing DeepSeek Strategy with model: {model_name}")
        return ChatOpenAI(
            model=model_name,
            openai_api_base="https://api.deepseek.com",
            openai_api_key=api_key,
            temperature=0.5
        )
