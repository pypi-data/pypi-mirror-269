from langchain.pydantic_v1 import BaseModel
from langchain.schema import AIMessage
from codeinterpreterapi_yayi.schema import File

class QueryInput(BaseModel):
    query: str


class AgentResponse(AIMessage):
    """
    Response from the code interpreter agent.

    files: list of files to be sent to the user (File )
    code_log: list[tuple[str, str]] = []
    reward: float = None
    """

    files: list[File] = []
    code_log: list[tuple[str, str]] = []
    reward: float = None

    def show(self) -> None:
        print("AI: ", self.content)
        for file in self.files:
            print("File: ", file.name)

    def __str__(self) -> str:
        return str(self.content)

    def __repr__(self) -> str:
        return f"AgentResponse(content={self.content}, files={self.files})"