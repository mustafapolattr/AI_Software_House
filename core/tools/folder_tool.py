import os
from crewai_tools import BaseTool
from pydantic import Field


class CreateFolderTool(BaseTool):
    name: str = "Create Folder Tool"
    description: str = "Creates a new directory/folder at the specified path. Use this BEFORE creating files inside a folder."

    def _run(self, folder_path: str) -> str:
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Successfully created directory: {folder_path}"
        except Exception as e:
            return f"Failed to create directory: {e}"
