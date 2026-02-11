import os
import sys

# Add the project root directory to the system path to ensure imports work correctly
# This allows us to import modules from the 'core' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from core.llm.factory import LLMFactory
from core.utils.logger import get_logger

# Initialize the centralized logger
logger = get_logger(__name__)

# --- LLM INITIALIZATION ---
try:
    # Use the Factory pattern to create the LLM instance
    # It automatically selects the provider (Claude, Gemini, etc.) based on the .env configuration
    llm = LLMFactory.create()
except Exception as e:
    # Log a critical error and exit if the LLM cannot be initialized
    logger.critical(f"PM Agent LLM Initialization Failed: {e}")
    sys.exit(1)

# --- AGENT DEFINITION ---
product_manager = Agent(
    role='Senior Technical Product Manager',
    goal='Analyze customer requests deeply and generate comprehensive Product Requirements Documents (PRD).',
    backstory="""
    You are a veteran Technical Product Manager with 15+ years of experience in Agile software development.
    Your expertise lies in translating vague client ideas into structured, actionable technical specifications.

    You focus strictly on:
    1. **Scope Definition:** Clearly defining what is in-scope and out-of-scope to prevent scope creep.
    2. **MVP Features:** Identifying the core features needed for a Minimum Viable Product.
    3. **User Stories:** Creating detailed user stories with clear Acceptance Criteria.
    4. **Data Flow:** Describing conceptually how data should move (input -> processing -> output).

    You create the "Vision" that the Software Architect will structure and the Developers will code.
    Your output must be structured, professional, and ready for a technical team to consume.
    """,
    llm=llm,
    verbose=True,  # Enable detailed logging of the agent's thought process
    allow_delegation=False,  # This agent works independently and does not delegate tasks
    memory=False  # Disabled to prevent embedding errors when using non-OpenAI models
)
