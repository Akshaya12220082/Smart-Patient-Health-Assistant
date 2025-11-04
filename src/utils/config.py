import yaml
import os

def load_config(config_path="config/config.yaml"):
    """
    Load YAML configuration file.
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        raise RuntimeError(f"Error loading config file: {e}")

def get_project_root():
    """
    Returns the absolute path to the project root directory.
    Useful for building paths dynamically.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def ensure_dir(path):
    """
    Creates a directory if it doesn't already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
