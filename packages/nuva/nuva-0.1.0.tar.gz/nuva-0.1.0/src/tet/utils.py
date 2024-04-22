import re
import json
import pickle
import pandas as pd
import numpy as np
import asyncio
from functools import partial

def regex_convert_float(text):
    pattern = r"\{result:\s*\[([\d\.]+)\]\}"
    match = re.search(pattern, text)
    try:
        return float(match.group(1)) if match else None
    except ValueError:  # Handles cases like '123.45.67' which are not valid floats
        return None


def extract_float(s: str) -> float:
    """
    Extracts the first floating-point number from a string.

    Parameters:
        s (str): The string from which to extract the float.

    Returns:
        float: The first floating-point number found in the string.
        If no floating-point number is found, raises a ValueError.
    """
    # Regular expression pattern to match a floating-point number
    # This pattern matches optional leading signs (+ or -), digits, optional decimal part
    pattern = r"[-+]?\d*\.\d+|[-+]?\d+"
    
    # Search for the pattern in the string
    match = re.search(pattern, s)
    
    # If a match is found, convert it to float and return
    if match:
        return float(match.group(0))
    else:
        # If no match is found, you can raise an error or return a default value
        raise ValueError("No floating-point number found in the input string.")


def write_jsonl(data_list, filename):
    with open(filename, "w") as file:
        for item in data_list:
            file.write(json.dumps(item) + "\n")


def load_responses(file_path: str):
    """
    Load responses from a JSON file.

    Parameters:
        file_path (str): The path to the file from which to load the responses.

    Returns:
        list: The list of responses loaded from the file.
    """
    with open(file_path, 'r') as f:
        responses = json.load(f)
    return responses


def save_object(obj, filename):
    with open(filename, 'wb') as output_file:  # Note 'wb' for writing bytes
        pickle.dump(obj, output_file)


def load_object(filename):
    with open(filename, 'rb') as input_file:  # Note 'rb' for reading bytes
        obj = pickle.load(input_file)
    return obj


def calculate_mse(prediction_csv: str, ground_truth_csv: str, prediction_col: str, ground_truth_col: str) -> float:
    """
    Calculate the Mean Squared Error (MSE) between predictions and ground truths stored in separate CSV files.

    Parameters:
        prediction_csv (str): Path to the CSV file containing the predictions.
        ground_truth_csv (str): Path to the CSV file containing the ground truth values.
        prediction_col (str): The column name in the prediction CSV that contains the prediction values.
        ground_truth_col (str): The column name in the ground truth CSV that contains the actual values.

    Returns:
        float: The computed MSE value.
    """
    # Load the data from CSV files
    predictions = pd.read_csv(prediction_csv)[prediction_col]
    ground_truths = pd.read_csv(ground_truth_csv)[ground_truth_col]

    # Calculate MSE
    mse = np.mean((predictions - ground_truths) ** 2)
    return mse


def make_async(sync_func):
    """
    Takes a synchronous function and returns an asynchronous function
    that executes the synchronous function in a separate thread.
    
    Args:
        sync_func (callable): A synchronous function to be converted to asynchronous.
    
    Returns:
        callable: An asynchronous function.
    """
    if not sync_func:
        return None

    async def async_func(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(sync_func, *args, **kwargs))
    return async_func