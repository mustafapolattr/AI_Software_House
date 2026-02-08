import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Central configuration class.
    Manages environment variables, model names, and dynamic validation.
    """

    # 1. Get the active provider (defaults to gemini if not set)
    DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()

    # 2. Map Providers to their specific API Key Environment Variable NAMES
    # This allows us to check dynamically based on selection.
    PROVIDER_KEY_MAPPING = {
        "gemini": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY"
    }

    # 3. Model Names Configuration
    MODEL_NAMES = {
        "gemini": os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash"),
        "openai": os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
        "claude": os.getenv("CLAUDE_MODEL_NAME", "claude-3-5-sonnet-20240620"),
        "deepseek": os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
    }

    OUTPUT_PATH = os.getenv("PROJECT_OUTPUT_PATH", "./output")

    @staticmethod
    def validate():
        """
        Validates that the REQUIRED API key is present for the SELECTED provider.
        If the provider is 'gemini', it only checks 'GOOGLE_API_KEY'.
        If 'openai', it checks 'OPENAI_API_KEY', and so on.
        """
        selected_provider = Config.DEFAULT_LLM_PROVIDER
        required_key_name = Config.PROVIDER_KEY_MAPPING.get(selected_provider)

        # 1. Check if provider is supported
        if not required_key_name:
            supported = list(Config.PROVIDER_KEY_MAPPING.keys())
            raise ValueError(
                f"❌ Configuration Error: Unknown DEFAULT_LLM_PROVIDER '{selected_provider}'. Supported providers: {supported}")

        # 2. Check if the specific API Key exists in the environment
        api_key_value = os.getenv(required_key_name)

        if not api_key_value or api_key_value.strip() == "":
            raise ValueError(
                f"❌ Configuration Error: System is set to use '{selected_provider}', "
                f"but the environment variable '{required_key_name}' is missing or empty in .env file."
            )

        return True
