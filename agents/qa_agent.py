from crewai import Agent
from crewai_tools import FileWriterTool
from core.llm.factory import LLMFactory

file_tool = FileWriterTool()
llm = LLMFactory.create()

qa_agent = Agent(
    role='Senior QA Engineer',
    goal='Write comprehensive automated tests using pytest.',
    backstory="""
    You are a meticulous QA Engineer. You break things to make them stronger.
    You analyze the Backend Developer's code and write 'test_app.py' to verify functionality.
    You specifically look for deprecated methods (like before_first_request) and fix them in your tests logic.
    """,
    llm=llm,
    verbose=True,
    tools=[file_tool],
    allow_delegation=False
)
