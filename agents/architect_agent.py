from crewai import Agent
from core.llm.factory import LLMFactory

try:
    llm = LLMFactory.create()
except:
    pass

architect_agent = Agent(
    role='Software Architect',
    goal='Design scalable folder structures and define technology stack.',
    backstory="""
    You are a Software Architect with 15 years of experience.
    You do NOT write application code. You define the BLUEPRINT.
    You decide which folders are needed (e.g., /src, /tests, /config) and 
    which files go where based on best practices (Clean Architecture).
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)