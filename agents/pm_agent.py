import os
import sys

# 1. PATH FIX: Add project root to system path to ensure imports work correctly
# This is necessary because this file is inside the 'agents' folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# --- CUSTOM MODULES ---
# Importing our modular infrastructure
from core.llm.factory import LLMFactory
from core.utils.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize Centralized Logger
logger = get_logger(__name__)

# --- 2. LLM INITIALIZATION ---
try:
    # Factory creates the model based on .env config (DEFAULT_LLM_PROVIDER)
    # It automatically handles API Key validation.
    llm = LLMFactory.create()
    logger.info("LLM initialized successfully for Product Manager Agent.")
except Exception as e:
    logger.critical(f"PM Agent LLM Initialization Failed: {e}")
    sys.exit(1)

# --- 3. AGENT DEFINITION ---
product_manager = Agent(
    role='Senior Technical Product Manager',
    goal='Analyze customer requirements, identify gaps, and generate detailed Technical PRDs (Product Requirements Documents).',
    backstory="""
    You are an expert Technical Product Manager with over 10 years of experience in Agile software development.
    Your specialty is bridging the gap between vague client requests and concrete technical specifications.

    You do not make assumptions. If a requirement is ambiguous, you flag it in the 'Questions' section.
    Your output is always structured, technical, and ready for a Senior Developer to implement immediately.
    You focus on defining the MVP (Minimum Viable Product) clearly.
    """,
    llm=llm,  # Injected dynamically from the Factory
    verbose=True,
    allow_delegation=False,
    memory=False  # Disabled to prevent OpenAI embedding errors if using other providers
)


# --- 4. TASK DEFINITION HELPER ---
# This function allows main.py to pass dynamic requests to this agent.
def get_pm_task(customer_request: str) -> Task:
    return Task(
        description=f"""
        Analyze the following customer request deeply:

        --- CUSTOMER REQUEST START ---
        "{customer_request}"
        --- CUSTOMER REQUEST END ---

        YOUR TASKS:
        1. **Scope Definition:** Define what is in scope and out of scope (Web/Mobile/API etc.).
        2. **MVP Features:** List the core features required for the Minimum Viable Product.
        3. **User Stories:** Write detailed User Stories with Acceptance Criteria.
        4. **Technical Stack & Risks:** Recommend libraries (Python) and identify potential technical risks.

        Make the output detailed and professional using Markdown format.
        """,
        expected_output="A professional Product Requirements Document (PRD) in Markdown format.",
        agent=product_manager
    )


# --- 5. ISOLATED TEST BLOCK ---
# This block runs ONLY if you execute this file directly (python agents/pm_agent.py)
if __name__ == "__main__":
    logger.info("Starting Product Manager Agent in TEST mode...")

    # Dummy data for testing
    dummy_request = "I need a website to track my crypto portfolio. It should use CoinGecko API."
    task = get_pm_task(dummy_request)

    # Create a temporary crew for testing
    crew = Crew(
        agents=[product_manager],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
        memory=False  # Important: Disable memory to avoid embedding issues during test
    )

    result = crew.kickoff()

    logger.info("Test Run Completed.")
    logger.info("--------------------------------------------------")
    logger.info(f"Final Output:\n{result}")