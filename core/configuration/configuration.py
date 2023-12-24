import os
import pathlib

import yaml

current_file_folder = os.path.dirname(os.path.realpath(__file__))


def load_configuration() -> dict:
    """
    returns configuration stored in services.yaml
    """
    configuration_path = pathlib.Path(current_file_folder + "/../../config/services.yaml").resolve()
    with open(configuration_path, "r") as f:
        config = yaml.safe_load(f)

    return config
