from typing import Optional, Any, Callable, Awaitable
import traceback
import re
import json

from codeinterpreterapi_yayi import CodeInterpreterSession
from codeinterpreterapi_yayi.schema import (
    SessionStatus,
    UserRequest,
    File,
    CodeInterpreterResponse
)
from codeinterpreterapi_yayi.chains import (
    aremove_download_link,
    remove_download_link,
)

from langchain.agents import (
    BaseSingleActionAgent,
    ConversationalAgent,
    ConversationalChatAgent,
)
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import Callbacks
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.chat import MessagesPlaceholder
from langchain.tools import BaseTool, StructuredTool
from langchain.schema import BaseMessage

from tet.schema import QueryInput, AgentResponse
from tet import settings
from tet.utils import make_async

ContentType = BaseMessage.__annotations__['content']
RewardFunctionType = Callable[[ContentType, list[File]], float]
ARewardFunctionType = Callable[[ContentType, list[File]], Awaitable[float]]


class AgentSession(CodeInterpreterSession):
    def __init__(
        self, 
        llm: Optional[BaseLanguageModel] = None, 
        additional_tools: list[BaseTool] = [], 
        callbacks: Callbacks = None, 
        reward_function: RewardFunctionType = None, 
        areward_function: ARewardFunctionType = None, 
        **kwargs: Any
    ) -> None:
        super().__init__(llm=llm, additional_tools=additional_tools, callbacks=callbacks, **kwargs)
        self.verbose = kwargs.get("verbose", settings.VERBOSE)
        self.codeinterpreterapi_model = kwargs.get("codeinterpreterapi_model", 'gpt-4-turbo-preview')
        self.system_message = kwargs.get("system_message", settings.SYSTEM_MESSAGE)
        self.codeinterpreterapi = CodeInterpreterSession(model=self.codeinterpreterapi_model, 
                                                         verbose=True, 
                                                         handle_parsing_errors=("Check your output and make sure it conforms,"
                                                                                " use 'code' as the input key. "))
        self.reward_function = reward_function
        if not areward_function:
            self.areward_function = make_async(reward_function)
        else:
            self.areward_function = areward_function

    def start(self) -> SessionStatus:
        status = self.codeinterpreterapi.start()
        self.agent_executor = self._agent_executor()

        return status

    async def astart(self) -> SessionStatus:
        status = await self.codeinterpreterapi.astart()
        self.agent_executor = self._agent_executor()

        return status

    def _tools(self, additional_tools: list[BaseTool]) -> list[BaseTool]:
        return additional_tools + [
            StructuredTool(
                name="assistant_api",
                description=("This function is a GPT based assistant api. "
                "Ask it to perform supervised learning tasks. "
                "It can write code and execute code on its code interpreter and return you the results. "
                "Input should be string based prompt query."),
                func=self._run_handler,
                coroutine=self._arun_handler,
                args_schema=QueryInput,  # type: ignore
            ),
        ]
    
    def _choose_agent(self) -> BaseSingleActionAgent:
        return (
            OpenAIFunctionsAgent.from_llm_and_tools(
                llm=self.llm,
                tools=self.tools,
                system_message=self.system_message,
                extra_prompt_messages=[
                    MessagesPlaceholder(variable_name="chat_history")
                ],
            )
            if isinstance(self.llm, ChatOpenAI)
            else ConversationalChatAgent.from_llm_and_tools(
                llm=self.llm,
                tools=self.tools,
                system_message=self.system_message.content.__str__(),
            )
            if isinstance(self.llm, BaseChatModel)
            else ConversationalAgent.from_llm_and_tools(
                llm=self.llm,
                tools=self.tools,
                prefix=self.system_message.content.__str__(),
            )
        )
    
    def _run_handler(self, query: str) -> str:
        """Run code in container and send the output to the user"""
        self.show_code(query)
        output: CodeInterpreterResponse = self.codeinterpreterapi.generate_response(query, files=self.input_files)
        self.code_log.append((query, output.content))
        self.output_files += output.files

        return output.content

    async def _arun_handler(self, query: str) -> str:
        """Run code in container and send the output to the user"""
        await self.ashow_code(query)
        output: CodeInterpreterResponse = await self.codeinterpreterapi.agenerate_response(query, files=self.input_files)
        self.code_log.append((query, output.content))
        self.output_files += output.files

        return output.content
    
    def _input_handler(self, request: UserRequest) -> None:
        """Callback function to handle user input."""
        if not request.files:
            return
        if not request.content:
            request.content = (
                "I uploaded, just text me back and confirm that you got the file(s)."
            )
        assert isinstance(request.content, str), "TODO: implement image support"
        request.content += "\n**The user uploaded the following files: **\n"
        self.input_files = request.files
        for file in request.files:
            request.content += f"[Attachment: {file.name}]\n"
        request.content += "**File(s) are now available in the cwd. **\n"

    async def _ainput_handler(self, request: UserRequest) -> None:
        """Callback function to handle user input."""
        if not request.files:
            return
        if not request.content:
            request.content = (
                "I uploaded, just text me back and confirm that you got the file(s)."
            )
        assert isinstance(request.content, str), "TODO: implement image support"
        request.content += "\n**The user uploaded the following files: **\n"
        self.input_files = request.files
        for file in request.files:
            request.content += f"[Attachment: {file.name}]\n"
        request.content += "**File(s) are now available in the cwd. **\n"

    def _output_handler(self, final_response: str, evaluate: bool) -> AgentResponse:
        """Post-process the response"""
        for file in self.output_files:
            if str(file.name) in final_response:
                # rm ![Any](file.name) from the response
                final_response = re.sub(r"\n\n!\[.*\]\(.*\)", "", final_response)

        if self.output_files and re.search(r"\n\[.*\]\(.*\)", final_response):
            try:
                final_response = remove_download_link(final_response, self.llm)
            except Exception as e:
                if self.verbose:
                    print("Error while removing download links:", e)

        output_files = self.output_files
        code_log = self.code_log
        self.output_files = []
        self.code_log = []
        if evaluate:
            reward = self.reward_function(final_response, output_files)
        else:
            reward = None

        return AgentResponse(
            content=final_response, files=output_files, code_log=code_log, reward=reward
        )

    async def _aoutput_handler(self, final_response: str, evaluate: bool) -> AgentResponse:
        """Post-process the response"""
        for file in self.output_files:
            if str(file.name) in final_response:
                # rm ![Any](file.name) from the response
                final_response = re.sub(r"\n\n!\[.*\]\(.*\)", "", final_response)

        if self.output_files and re.search(r"\n\[.*\]\(.*\)", final_response):
            try:
                final_response = await aremove_download_link(final_response, self.llm)
            except Exception as e:
                if self.verbose:
                    print("Error while removing download links:", e)

        output_files = self.output_files
        code_log = self.code_log
        self.output_files = []
        self.code_log = []
        if evaluate:
            reward = await self.areward_function(final_response, output_files)
        else:
            reward = None


        return AgentResponse(
            content=final_response, files=output_files, code_log=code_log, reward=reward
        )

    def generate_response(
        self,
        user_msg: str,
        files: list[File] = [],
        evaluate: bool = False,
    ) -> AgentResponse:
        """Generate an Agent response based on the user's input."""
        user_request = UserRequest(content=user_msg, files=files)
        try:
            self._input_handler(user_request)
            assert self.agent_executor, "Session not initialized."
            response = self.agent_executor.run(input=user_request.content)
            return self._output_handler(response, evaluate=evaluate)
        except Exception as e:
            if self.verbose:
                traceback.print_exc()
            if settings.DETAILED_ERROR:
                return AgentResponse(
                    content="Error in AgentSession: "
                    f"{e.__class__.__name__}  - {e}"
                )
            else:
                return AgentResponse(
                    content="Sorry, something went wrong while generating your response."
                    "Please try again or restart the session."
                )

    async def agenerate_response(
        self,
        user_msg: str,
        files: list[File] = [],
        evaluate: bool = False,
    ) -> AgentResponse:
        """Generate an Agent response based on the user's input."""
        user_request = UserRequest(content=user_msg, files=files)
        try:
            await self._ainput_handler(user_request)
            assert self.agent_executor, "Session not initialized."
            response = await self.agent_executor.arun(input=user_request.content)
            return await self._aoutput_handler(response, evaluate=evaluate)
        except Exception as e:
            if self.verbose:
                traceback.print_exc()
            if settings.DETAILED_ERROR:
                return AgentResponse(
                    content="Error in AgentSession: "
                    f"{e.__class__.__name__}  - {e}"
                )
            else:
                return AgentResponse(
                    content="Sorry, something went wrong while generating your response."
                    "Please try again or restart the session."
                )

    def stop(self) -> SessionStatus:
        return self.codeinterpreterapi.stop()

    async def astop(self) -> SessionStatus:
        return await self.codeinterpreterapi.astop()