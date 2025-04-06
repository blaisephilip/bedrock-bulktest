import json
from pathlib import Path

def read_config(config_path):
    """
    Read the Bedrock test configuration file and return its contents as a dictionary.
    
    Args:
        config_path (str): Path to the configuration JSON file
    
    Returns:
        dict: Configuration settings
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_path}")
