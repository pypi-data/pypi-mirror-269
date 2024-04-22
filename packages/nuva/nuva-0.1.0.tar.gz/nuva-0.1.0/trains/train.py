from tet import AgentSession
from tet.finetuning import iterative_fine_tuning

async def main():
    session = AgentSession()  # Assume this session is correctly set up
    initial_model = "text-davinci-002"
    file_path = "path_to_your_dataset.csv"
    iterations = 5

    final_model, metrics = await iterative_fine_tuning(session, initial_model, file_path, iterations)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())