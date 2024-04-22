from tet.finetuning import prepare_training_data, fine_tune_model, wait_for_fine_tuning_to_complete
from tet.data_collection import generate_and_save_responses, agenerate_and_save_responses
from tet.utils import write_jsonl
from tet.schema import AgentResponse
from tet import settings

import json

def select_top_responses(responses : list[AgentResponse], k: int) -> tuple[list[AgentResponse], float]:
    rewards = [response.reward for response in responses]
    top_indices = sorted(range(len(rewards)), key=lambda i: rewards[i], reverse=True)[:k]
    average_reward = sum([responses[i].reward for i in top_indices]) / k
    return [responses[i] for i in top_indices], average_reward

async def iterative_fine_tuning(user_prompt, initial_model, files, iterations, save_path, reward_func, system_message, num_samples=10, top_k=3):
    current_model = initial_model
    metrics = []
    all_training_data = []

    for i in range(iterations):
        responses = await agenerate_and_save_responses(user_prompt,
            files, num_samples, save_path, evaluate=True, reward_func=reward_func, system_message=system_message)
        top_responses, average_reward = select_top_responses(responses, top_k)
        metrics.append(average_reward)

        training_data = prepare_training_data(top_responses)
        training_file = f"training_data_iteration_{i}.jsonl"
        write_jsonl(training_data, training_file)

        # Save training details for future use
        iteration_data = {
            "iteration": i,
            "model": current_model,
            "average_reward": average_reward,
            "training_file": training_file
        }
        all_training_data.append(iteration_data)

        # Fine-tuning and model update
        fine_tune_job_id = fine_tune_model(training_file, current_model)
        new_model = wait_for_fine_tuning_to_complete(fine_tune_job_id)
        current_model = new_model

    # Save all training information
    with open("training_details.json", "w") as f:
        json.dump(all_training_data, f)

    return current_model, metrics