import yaml


def load_yaml_config(file_path: str):
    """Loads a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The content of the YAML file as a Python object.
    """
    with open(file_path, "r", encoding="utf-8") as file:  # Specified encoding
        config = yaml.safe_load(file)
    return config
