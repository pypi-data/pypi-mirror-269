from typing import Callable
import asyncio
import pytest
import time
import traceback

from codeinterpreterapi_yayi import File

from tet import AgentSession, settings
from tet.utils import extract_float, load_object
from tet.schema import AgentResponse
from tet.reward import reward_mse_prediction
from tet.data_collection import generate_and_save_responses, agenerate_and_save_responses

AssertFunctionType = Callable[[AgentResponse], bool]

user_prompt_1 = "Use the advertising dataset given in ISLR and analyse the relationship between \
                'TV advertising' and 'Sales', where 'Sales' is the prediction target. \
                Use the first 70% of the data as your train dataset and the rest 30% as your test dataset. \
                Metrics: MSE \
                Return the MSE of test dataset in your final response."
user_prompt_2 = "Use the advertising dataset given in ISLR and analyse the relationship between \
                'TV advertising' and 'Sales', where 'Sales' is the prediction target. \
                Use the first 70% of the data as your train dataset and the rest 30% as your test dataset. \
                Metrics: MSE \
                Return the model in .joblib format."
user_prompt_3 = "Train a model between \
                'TV advertising' and 'Sales' using the train dataset, where 'Sales' is the prediction target. \
                Then make inference on the test dataset. \
                Compute the Mean Squared Error (MSE) between the predictions and ground truths on the test dataset. \
                Return the prediction of 'Sales' of test dataset in a csv file named 'prediction.csv'. Set the column name of your prediction as 'Sales'."

assert_function_1 = lambda response: 2.0 <= extract_float(response.content) <= 7.0
assert_function_2 = lambda response: ".joblib" in response.files[0].name
assert_function_3 = lambda response: 1/7.0 <= response.reward <= 1/2.0

# Helper function to build parameters with defaults
def param(user_prompt, assert_function, asynch=False, reward_func=None, files=[File.from_path("examples/assets/advertising.csv")], system_message=settings.SYSTEM_MESSAGE_TEST):
    return (
        user_prompt,
        assert_function,
        asynch,
        reward_func,
        files,
        system_message,
    )

@pytest.mark.parametrize(
    "user_prompt, assert_function, asynch, reward_func, files, system_message",
    [
        param(user_prompt_1, assert_function_1),
        # param(user_prompt_1, assert_function_1, asynch=True),
        # param(user_prompt_2, assert_function_2),
        # param(user_prompt_2, assert_function_2, asynch=True),
        # param(user_prompt_3, assert_function_3, reward_func=reward_mse_prediction, files=[File.from_path("examples/assets/train_data.csv"), File.from_path("examples/assets/test_data.csv")]),
        # param(user_prompt_3, assert_function_3, asynch=True, reward_func=reward_mse_prediction, files=[File.from_path("examples/assets/train_data.csv"), File.from_path("examples/assets/test_data.csv")]),
    ]
)
def test_generate_response(
    user_prompt: str,
    assert_function: AssertFunctionType,
    asynch: bool,
    reward_func : Callable[[str, list[File]], float],
    files: list[File],
    system_message: str,
    ) -> None:

    session = AgentSession(system_message=system_message, reward_function=reward_func)
    evaluate = True if reward_func else False
    if asynch:
        assert asyncio.run(
        run_async(session, user_prompt, assert_function, files, evaluate)
        ), "Failed to run async generate_response remotely"
    else:
        assert run_sync(session, user_prompt, assert_function, files, evaluate), "Failed to run sync generate_response remotely"

def run_sync(session: AgentSession, user_prompt: str, assert_function: AssertFunctionType, files: list[File], evaluate: bool) -> bool:
    try:
        assert (session.start() == "started")
        response = session.generate_response(user_prompt, files, evaluate=evaluate)
        #print('content=', response.content, '\nfiles=', response.files, '\ncode_log=', response.code_log, '\nreward=', response.reward)
        assert assert_function(response)
    finally:
        assert session.stop() == "stopped"
    
    return True

async def run_async(session: AgentSession, user_prompt: str, assert_function: AssertFunctionType, files: list[File], evaluate: bool) -> bool:
    try:
        assert (await session.astart()) == "started"
        response = await session.agenerate_response(user_prompt, files, evaluate=evaluate)
        assert assert_function(response)
    finally:
        assert await session.astop() == "stopped"
    
    return True


@pytest.mark.parametrize(
    "user_prompt, assert_function, asynch, reward_func, files, system_message, num_samples, save_path",
    [
        param(user_prompt_1, assert_function_1) + (2, "data/responses.pickle"),
        param(user_prompt_1, assert_function_1, asynch=True) + (2, "data/aresponses.pickle"),
        param(user_prompt_2, assert_function_2) + (2, "data/responses.pickle"),
        param(user_prompt_2, assert_function_2, asynch=True) + (2, "data/responses.pickle"),
        param(user_prompt_3, assert_function_3, reward_func=reward_mse_prediction, files=[File.from_path("examples/assets/train_data.csv"), File.from_path("examples/assets/test_data.csv")]) + (2, "data/responses.pickle"),
        param(user_prompt_3, assert_function_3, asynch=True, reward_func=reward_mse_prediction, files=[File.from_path("examples/assets/train_data.csv"), File.from_path("examples/assets/test_data.csv")]) + (2, "data/responses.pickle"),
    ]
)
def test_generate_and_save_responses(
    user_prompt: str,
    assert_function: AssertFunctionType,
    asynch: bool,
    reward_func : Callable[[str, list[File]], float],
    files: list[File],
    system_message: str,
    num_samples: int,
    save_path: str,
    ) -> None:

    evaluate = True if reward_func else False
    if asynch:
        assert asyncio.run(
        run_async_responses(user_prompt, assert_function, files, num_samples, save_path, evaluate, reward_func, system_message)
        ), "Failed to run async generate_and_save_responses remotely"
    else:
        assert run_sync_responses(user_prompt, assert_function, files, num_samples, save_path, evaluate, reward_func, system_message), "Failed to run sync generate_and_save_responses remotely"

def run_sync_responses(user_prompt: str, assert_function: AssertFunctionType,
                       files: list[File], num_samples: int, save_path: str, evaluate: bool,
                       reward_func: Callable[[str, list[File]], float], system_message: str) -> bool:
    try:
        start_time = time.perf_counter()
        responses = generate_and_save_responses(user_prompt, files, num_samples, save_path, evaluate, reward_func, system_message)
        end_time = time.perf_counter()
        print(f"Sync function took {end_time - start_time} seconds")
        #print('response','content=', responses[-1].content, '\nfiles=', responses[-1].files, '\ncode_log=', responses[-1].code_log, '\nreward=', responses[-1].reward)
        assert len(responses) == num_samples
        assert assert_function(responses[-1])

        # Test the saved responses
        responses = load_object(save_path)
        #print('saved_response','content=', responses[-1].content, '\nfiles=', responses[-1].files, '\ncode_log=', responses[-1].code_log, '\nreward=', responses[-1].reward)
        assert len(responses) == num_samples
        assert assert_function(responses[0])
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()  # Print the traceback to see the stack of errors
        return False
    else:
        print("All tests passed successfully.")
        return True

async def run_async_responses(user_prompt: str, assert_function: AssertFunctionType,
                       files: list[File], num_samples: int, save_path: str, evaluate: bool,
                       reward_func: Callable[[str, list[File]], float], system_message: str) -> bool:
    try:
        start_time = time.perf_counter()
        responses = await agenerate_and_save_responses(user_prompt, files, num_samples, save_path, evaluate, reward_func, system_message)
        end_time = time.perf_counter()
        print(f"Async function took {end_time - start_time} seconds")
        #print('response','content=', responses[-1].content, '\nfiles=', responses[-1].files, '\ncode_log=', responses[-1].code_log, '\nreward=', responses[-1].reward)
        assert len(responses) == num_samples
        assert assert_function(responses[-1])

        # Test the saved responses
        responses = load_object(save_path)
        #print('saved_response','content=', responses[-1].content, '\nfiles=', responses[-1].files, '\ncode_log=', responses[-1].code_log, '\nreward=', responses[-1].reward)
        assert len(responses) == num_samples
        assert assert_function(responses[0])
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
    except Exception as e:
        print("An error occurred:", str(e))
        traceback.print_exc()  # Print the traceback to see the stack of errors
        return False
    else:
        print("All tests passed successfully.")
        return True


if __name__ == "__main__":
    test_generate_response()
    test_generate_and_save_responses()