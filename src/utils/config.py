import yaml
import os
from pathlib import Path
from typing import Any, Dict

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load YAML configuration file with environment variable support.
    
    Environment variables can be used with ${VAR_NAME} syntax in the YAML file.
    Falls back to template if main config doesn't exist.
    """
    root = get_project_root()
    full_path = os.path.join(root, config_path)
    
    # If config.yaml doesn't exist, try template
    if not os.path.exists(full_path):
        template_path = full_path + ".template"
        if os.path.exists(template_path):
            print(f"⚠️  Config file not found at {full_path}")
            print(f"📋 Using template from {template_path}")
            full_path = template_path
        else:
            raise RuntimeError(f"Config file not found: {full_path}")
    
    try:
        with open(full_path, "r") as file:
            config = yaml.safe_load(file)
        
        # Replace environment variables
        config = _replace_env_vars(config)
        
        return config
    except Exception as e:
        raise RuntimeError(f"Error loading config file: {e}")

def _replace_env_vars(obj: Any) -> Any:
    """
    Recursively replace ${VAR_NAME} with environment variables.
    """
    if isinstance(obj, dict):
        return {k: _replace_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_replace_env_vars(item) for item in obj]
    elif isinstance(obj, str):
        # Check if string contains ${VAR_NAME} pattern
        if obj.startswith("${") and obj.endswith("}"):
            var_name = obj[2:-1]
            return os.environ.get(var_name, obj)  # Return original if not found
        return obj
    else:
        return obj

def get_project_root() -> str:
    """
    Returns the absolute path to the project root directory.
    Useful for building paths dynamically.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def ensure_dir(path: str) -> None:
    """
    Creates a directory if it doesn't already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
