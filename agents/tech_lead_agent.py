from crewai import Agent, Task
from crewai_tools import FileWriterTool
from core.llm.factory import LLMFactory
from core.tools.folder_tool import CreateFolderTool

file_tool = FileWriterTool()
folder_tool = CreateFolderTool()
llm = LLMFactory.create()

tech_lead_agent = Agent(
    role='Technical Team Lead',
    goal='Setup the project environment, create folders, and configuration files.',
    backstory="""
    You are the Tech Lead. You take the Architect's design and prepare the ground.
    You create the actual folders using the CreateFolderTool.
    You write the 'requirements.txt', '.gitignore', and 'README.md'.
    You ensure the environment is ready for developers.
    """,
    llm=llm,
    verbose=True,
    tools=[file_tool, folder_tool],
    allow_delegation=False
)
