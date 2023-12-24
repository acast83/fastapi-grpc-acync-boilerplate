import os
import re


def replace_env_variables(item):
    # Regular expression to match pattern ${NAME}
    pattern = re.compile(r'\$\{(\w+)\}')

    if isinstance(item, dict):
        # If the item is a dictionary, recursively process each key-value pair
        for key, value in item.items():
            item[key] = replace_env_variables(value)
    elif isinstance(item, list):
        # If the item is a list, recursively process each element
        return [replace_env_variables(elem) for elem in item]
    elif isinstance(item, str):
        # If the item is a string, search for pattern and replace
        def replace_match(match):
            env_var = match.group(1)
            return os.getenv(env_var, match.group(0))  # Replace with environment variable or keep original

        return pattern.sub(replace_match, item)
    return item
