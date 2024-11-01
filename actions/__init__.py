import yaml
import os


class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls, path='config.yml'):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._config = cls._load_config(path)
        return cls._instance

    @classmethod
    def _load_config(cls, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at: {path}")
        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
                if config is None:
                    raise ValueError("Config file is empty or invalid.")
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse config file: {e}")

    @classmethod
    def get_config(cls):
        if cls._instance is None:
            cls._instance = cls() 
        return cls._config
