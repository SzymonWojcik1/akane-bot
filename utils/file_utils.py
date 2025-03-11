import json
import os

def load_config(filename='config.json'):
    """
    Load the config as a json file

    Args:
        filename: by default config.json
    Return:
        None: If the the file is not found or if there is a problem while parsing the json file
        config: return a dict with the info in the config file
    """
    try:
        # Reads the file filename and returns a dict of said file here config.json
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        # If it does not find the file it prints an error and returns nothing
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError:
        # If there is a problem with the json file then it returns nothing and prints the error
        print(f"Error: Failed to parse {filename} as JSON.")
        return None