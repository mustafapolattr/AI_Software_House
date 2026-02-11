import sys
import os

# --- CRITICAL FIX: BYPASS OPENAI REQUIREMENT ---
# CrewAI checks for an OPENAI_API_KEY by default upon initialization.
# We inject a dummy key here to prevent a crash, as we use Gemini/Claude via our custom provider.
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "NA"

from dotenv import load_dotenv
from crewai import Crew, Process, Task

# --- IMPORT AGENTS ---
from agents.pm_agent import product_manager
from agents.architect_agent import architect_agent
from agents.tech_lead_agent import tech_lead_agent
from agents.backend_agent import backend_agent
from agents.qa_agent import qa_agent

# --- IMPORT CORE UTILITIES ---
from core.utils.logger import get_logger
from core.config import Config

# Load environment variables
load_dotenv()

# Initialize centralized logger
logger = get_logger(__name__)


def run_software_house():
    """
    Main orchestration function for the AI Software House.
    It defines the workflow, creates tasks, and manages the agent crew.
    """

    # 1. Validate Configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.critical(f"Configuration Error: {e}")
        sys.exit(1)

    # 2. Define Project Path
    # The agents will create files STRICTLY inside this directory.
    PROJECT_NAME = "todo_flask_app"

    # Ensure consistent path formatting (forward slashes are safer for AI context)
    project_root = os.path.join(Config.OUTPUT_PATH, PROJECT_NAME).replace("\\", "/")

    logger.info(f"🚀 AI Software House Initialized")
    logger.info(f"📂 Target Project Path: {project_root}")

    # 3. Define Customer Request
    customer_request = """
    I want a robust 'ToDo API' project using Python Flask.

    Functional Requirements:
    1. Add a task (POST /tasks) with title and description.
    2. List all tasks (GET /tasks).
    3. Save tasks persistently to a JSON file (data/tasks.json).

    Non-Functional Requirements:
    - Clean architecture.
    - Robust error handling.
    """

    # --- DEFINE TASKS ---

    # Task 1: Product Manager (Analysis)
    task_pm = Task(
        description=f"Analyze the following customer request deeply: '{customer_request}'. Create a detailed Product Requirements Document (PRD).",
        expected_output="A comprehensive PRD defining scope, features, and user stories.",
        agent=product_manager
    )

    # Task 2: Software Architect (Structure Design)
    task_architect = Task(
        description=f"""
        Based on the PRD, define a scalable folder structure for a Flask project.

        CRITICAL CONSTRAINT: All file paths MUST start with the root: {project_root}

        Required Structure:
        - {project_root}/app/ (Source code)
        - {project_root}/data/ (Storage)
        - {project_root}/tests/ (Unit tests)
        - {project_root}/run.py (Entry point)
        """,
        expected_output="A list of absolute file paths and architectural decisions.",
        agent=architect_agent,
        context=[task_pm]  # Architect reads PM's report
    )

    # Task 3: Tech Lead (Environment Setup)
    task_tech_lead = Task(
        description=f"""
        Prepare the project environment based on the Architect's design.

        Actions:
        1. Use 'Create Folder Tool' to create the main folder: {project_root}
        2. Create necessary subfolders (app, data, tests) inside it.
        3. Create 'requirements.txt' inside {project_root} (include flask, pytest, requests).
        4. Create a professional 'README.md' inside {project_root}.
        """,
        expected_output="Project folders created and configuration files (requirements.txt, README) written.",
        agent=tech_lead_agent,
        context=[task_architect]  # Tech Lead follows Architect's plan
    )

    # Task 4: Backend Developer (Implementation)
    task_backend = Task(
        description=f"""
        Write the production-ready Python code for the Flask application.

        Files to create:
        1. {project_root}/app/__init__.py (App factory pattern).
        2. {project_root}/app/routes.py (API Endpoints implementation).
        3. {project_root}/run.py (Entry point script).

        IMPORTANT: Save files strictly to the paths defined above.
        """,
        expected_output="Functional Python code files saved to the directory.",
        agent=backend_agent,
        context=[task_pm, task_tech_lead]  # Dev reads PRD and uses Tech Lead's setup
    )

    # Task 5: QA Engineer (Testing)
    task_qa = Task(
        description=f"""
        Write comprehensive functional tests for the application.
        Target File: {project_root}/tests/test_app.py

        Requirements:
        1. Use 'pytest' framework.
        2. Write tests for creating a task and listing tasks.
        3. Ensure imports are correct relative to the project root.

        Review the Backend Developer's code to ensure tests match the implemented endpoints.
        """,
        expected_output="A complete test suite saved as test_app.py.",
        agent=qa_agent,
        context=[task_backend]  # QA checks Backend Dev's work
    )

    # --- ASSEMBLE THE CREW ---
    project_team = Crew(
        agents=[product_manager, architect_agent, tech_lead_agent, backend_agent, qa_agent],
        tasks=[task_pm, task_architect, task_tech_lead, task_backend, task_qa],
        process=Process.sequential,  # Execute tasks one by one
        verbose=True,  # Log detailed output to console
        memory=False  # Disable memory to prevent embedding provider issues
    )

    # --- KICKOFF ---
    logger.info("🚀 Starting the Enterprise Software Development Lifecycle...")
    result = project_team.kickoff()

    logger.info("✅ Project Execution Completed Successfully!")
    logger.info(f"📂 Output generated at: {project_root}")
    print("\n\n######################## FINAL REPORT ########################\n")
    print(result)


if __name__ == "__main__":
    run_software_house()
