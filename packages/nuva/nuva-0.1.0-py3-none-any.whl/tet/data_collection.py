from typing import Callable
import asyncio

from codeinterpreterapi_yayi import File

from tet.utils import save_object
from tet import AgentSession
from tet.schema import AgentResponse
from tet import settings


def generate_and_save_responses(user_prompt: str, files: list[File], num_samples: int, save_path: str,
    evaluate: bool, reward_func: Callable[[str, list[File]], float], system_message: str
    ) -> list[AgentResponse]:
    """
    Sequencially generate responses and save them to a file.

    Args:
        user_prompt (str): User prompt to generate the response.
        files (list): List of files used in generating the response.
        num_samples (int): Number of samples to generate.
        save_path (str): Path where the responses will be saved.
        evaluate (bool): Flag to determine if evaluation is needed.
        reward_func (Callable): Reward function used for evaluation.
        system_message (str): System message to initialize the session.

    Returns:
        list: List of generated responses.
    """

    responses = []
    for _ in range(num_samples):
        try:
            with AgentSession(system_message=system_message, reward_function=reward_func) as session:
                response = session.generate_response(user_prompt, files=files, evaluate=evaluate)
                responses.append(response)
        except Exception as e:
            print(f"Failed to generate response: {e}")
            if settings.DETAILED_ERROR:
                responses.append(AgentResponse(
                    content="Error in AgentSession: "
                    f"{e.__class__.__name__}  - {e}"
                ))
            else:
                responses.append(AgentResponse(
                    content="Sorry, something went wrong while generating your response."
                    "Please try again or restart the session."
                ))

    # Save responses to a file
    save_object(responses, save_path)
    return responses


async def agenerate_and_save_responses(user_prompt: str, files: list[File], num_samples: int, save_path: str,
    evaluate: bool, reward_func: Callable[[str, list[File]], float], system_message: str
    ) -> list[AgentResponse]:
    """
    Asynchronously generate responses and save them to a file.

    Args:
        user_prompt (str): User prompt to generate the response.
        files (list): List of files used in generating the response.
        num_samples (int): Number of samples to generate.
        save_path (str): Path where the responses will be saved.
        evaluate (bool): Flag to determine if evaluation is needed.
        reward_func (Callable): Reward function used for evaluation.
        system_message (str): System message to initialize the session.

    Returns:
        list: List of generated responses.
    """
    responses = []
    tasks = []

    for _ in range(num_samples):
        task = create_and_run_session(user_prompt, files, evaluate, reward_func, system_message)
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            print(f"Failed to generate response: {result}")
            if settings.DETAILED_ERROR:
                responses.append(AgentResponse(
                    content="Error in AgentSession: "
                    f"{e.__class__.__name__}  - {result}"
                ))
            else:
                responses.append(AgentResponse(
                    content="Sorry, something went wrong while generating your response."
                    "Please try again or restart the session."
                ))
        else:
            responses.append(result)

    # Save responses to a file
    save_object(responses, save_path)
    return responses

async def create_and_run_session(user_prompt, files, evaluate, reward_func, system_message):
    async with AgentSession(system_message=system_message, reward_function=reward_func) as session:
        return await session.agenerate_response(user_prompt, files=files, evaluate=evaluate)
