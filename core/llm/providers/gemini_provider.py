import os
from langchain_google_genai import ChatGoogleGenerativeAI
from ..interface import LLMProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)


class GeminiProvider(LLMProvider):
    def get_llm(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

        if not api_key:
            logger.critical("GOOGLE_API_KEY is missing.")
            raise ValueError("GOOGLE_API_KEY is missing.")

        logger.info(f"🔹 [Gemini Provider] Initializing LangChain wrapper for: {model_name}")

        try:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.5,
                verbose=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise e
