import pandas as pd
import numpy as np

from codeinterpreterapi_yayi.schema import File

from tet.utils import calculate_mse


def reward_mse_prediction(content: str, files: list[File]) -> float:
    """
    Reward function that calculates the reward based on the Mean Squared Error (MSE) between the predictions
    and ground truths stored in separate CSV files.

    Parameters:
        content (str): The content of the response.
        files (list[File]): List of files attached to the response.

    Returns:
        float: The reward value based on the MSE.
    """

    for file in files:
        if file.name == 'prediction.csv':
            file.save('data/predictions.csv')
            mse = calculate_mse('data/predictions.csv', 'examples/assets/test_data.csv', 'Sales', 'Sales')
            return 1.0 / mse
    return 0.0