import os
from pathlib import Path

from dotenv import load_dotenv

# Determine the path to the current file to locate the default directory for .env files
current_file_folder = os.path.dirname(os.path.realpath(__file__))


def set_env_variables(directory: Path | None = None) -> None:
    """
    Reads all .env files from a specified directory and sets the environment variables.

    Parameters:
    directory (Path): A Path object pointing to the directory containing .env files.
                      If not provided, it defaults to the '../../config/environments'
                      directory relative to the current file.

    Returns:
    None
    """
    # Set the default directory if not specified
    if directory is None:
        directory = Path(f'{current_file_folder}/../../config/environments').resolve()

    # Iterate through all the files in the specified directory
    for item in directory.iterdir():
        # Check if the item is a file and has a .env extension
        if item.is_file() and item.suffix == '.env':
            # Load the .env file and set the environment variables
            load_dotenv(dotenv_path=item, override=True)
