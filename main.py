import sys
import os

# --- CRASH FIX ---
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "NA"

from dotenv import load_dotenv
from crewai import Crew, Process, Task

# Import Agents
from agents.pm_agent import product_manager
from agents.architect_agent import architect_agent
from agents.tech_lead_agent import tech_lead_agent
from agents.backend_agent import backend_agent

# Import Config & Utils
from core.utils.logger import get_logger
from core.config import Config
from core.llm.factory import LLMFactory

load_dotenv()
logger = get_logger(__name__)


def run_software_house():
    # 1. Hazırlık
    Config.validate()
    target_path = Config.OUTPUT_PATH

    # 2. Müşteri İsteği (Daha Karmaşık Bir İstek)
    customer_request = """
    I want a 'ToDo API' project using Python Flask.
    Features:
    1. Add a task.
    2. List all tasks.
    3. Save tasks to a JSON file (database).

    Structure Requirement:
    - Separate folders for 'app', 'data', and 'tests'.
    - Use 'run.py' to start the app.
    """

    # --- GÖREVLER (TASKS) ---

    # Görev 1: PM Analizi
    task_pm = Task(
        description=f"Analyze this request: {customer_request}. Create a detailed PRD.",
        expected_output="A comprehensive PRD document.",
        agent=product_manager
    )

    # Görev 2: Mimarın Planı (Klasör Yapısı)
    task_architect = Task(
        description=f"""
        Based on the PRD, define a clean folder structure for a Flask project.
        Target Project Path: {target_path}

        List exactly which folders and files need to be created.
        Example:
        - {target_path}/app/
        - {target_path}/run.py
        """,
        expected_output="A list of file paths and folder structures.",
        agent=architect_agent,
        context=[task_pm]
    )

    # Görev 3: Tech Lead (Klasörleri Oluştur ve Config Yaz)
    task_tech_lead = Task(
        description=f"""
        1. Use 'Create Folder Tool' to create ALL folders defined by the Architect at {target_path}.
        2. Create 'requirements.txt' (include flask).
        3. Create 'README.md'.
        """,
        expected_output="Folders created and config files written.",
        agent=tech_lead_agent,
        context=[task_architect]
    )

    # Görev 4: Backend Dev (Kodlama)
    task_backend = Task(
        description=f"""
        Write the actual Python code for the Flask application.
        1. Create 'app/__init__.py' (Flask app factory).
        2. Create 'app/routes.py' (The endpoints).
        3. Create 'run.py' in the root folder.

        Use the paths prepared by the Tech Lead.
        """,
        expected_output="Working Python code files.",
        agent=backend_agent,
        context=[task_pm, task_tech_lead]
    )

    # --- EKİBİ KUR ---
    crew = Crew(
        agents=[product_manager, architect_agent, tech_lead_agent, backend_agent],
        tasks=[task_pm, task_architect, task_tech_lead, task_backend],
        process=Process.sequential,
        verbose=True,
        memory=False
    )

    logger.info("🚀 Enterprise AI Team is starting...")
    result = crew.kickoff()
    logger.info("✅ Project Completed!")


if __name__ == "__main__":
    run_software_house()
