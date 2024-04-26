import os

import yaml

ENV_DATA_STORAGE_NAME_ENV_VAR_KEY = "BTPY_ENV_DATA_STORAGE_NAME"
ENV_DATA_STORAGE_NAME_CONFIG_KEY = "EnvDataStorageName"


def get_env_data_storage_name():
    # Try env var
    env_value = os.getenv(ENV_DATA_STORAGE_NAME_ENV_VAR_KEY)

    if env_value:
        return env_value

    # Try user config file
    config_file_path = os.path.expanduser(os.path.normpath("~/.btpy/config.yaml"))

    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as config_file:
            config_yaml = yaml.safe_load(config_file)
            config_value = config_yaml[ENV_DATA_STORAGE_NAME_CONFIG_KEY]

            if config_value:
                return config_value

    # No value found, raise error
    raise FileNotFoundError(
        f"Failed to read env data storage name from file: {config_file_path} \
        (can also be set through env var: {ENV_DATA_STORAGE_NAME_ENV_VAR_KEY})")
