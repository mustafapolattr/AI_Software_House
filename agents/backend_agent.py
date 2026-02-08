from crewai import Agent
from crewai_tools import FileWriterTool
from core.llm.factory import LLMFactory

file_tool = FileWriterTool()
llm = LLMFactory.create()

backend_agent = Agent(
    role='Senior Backend Developer',
    goal='Implement business logic and API endpoints based on the architecture.',
    backstory="""
    You are a Python expert (FastAPI/Flask/Django).
    You write clean, documented, and efficient code.
    You strictly follow the file paths defined by the Architect and Tech Lead.
    """,
    llm=llm,
    verbose=True,
    tools=[file_tool],
    allow_delegation=False
)
