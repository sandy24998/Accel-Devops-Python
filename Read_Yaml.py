#Q1. Write a Python function that safely reads a YAML config file (e.g., config.yaml) and returns the data as a dict. Handle missing file, invalid YAML, 
# and return a sensible default. Use context managers.

import yaml

def load_config(file_path):

    default_config={}

    try:
        with open(file_path, 'r') as file:
            data=yaml.safe_load(file)

            if data is None:
                return default_config
            
            return data
        
    except (FileNotFoundError, yaml.YAMLError):
        return default_config


config = load_config("config.yaml")
print(config)

broken_config = load_config("missing_or_broken_file.yaml")
print(broken_config)