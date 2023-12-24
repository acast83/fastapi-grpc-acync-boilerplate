import json
import pathlib
from typing import Dict, Any

import yaml

from core.configuration.configuration import load_configuration


def parse_yaml(file_path: pathlib.Path) -> Dict[str, Any]:
    """
    Parses a YAML file and returns its contents as a dictionary.

    Args:
    file_path (pathlib.Path): The path to the YAML file.

    Returns:
    Dict[str, Any]: The contents of the YAML file as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# def generate_class_definitions(yaml_data: Dict[str, Any]) -> str:
#     """
#     Generates Python class definitions based on the provided YAML data.
#
#     Args:
#     yaml_data (Dict[str, Any]): The data extracted from a YAML file.
#
#     Returns:
#     str: A string containing the generated Python class definitions.
#     """
#     classes = "import uuid\nimport json\nfrom enum import Enum\n\n\n"
#     lookups_class = "class Lookups:\n\n"
#
#     for service, classes_data in yaml_data.items():
#         service_lookups_class = f"class {service}:\n\n"
#         lookups_class += f"    {service} = {service}\n"
#         for class_name, values in classes_data.items():
#             service_lookups_class += f"    {class_name} = {class_name}\n"
#             classes += f"class {class_name}(Enum):\n\n"
#             for key, value in values.items():
#                 classes += f"    {key.upper()} = '{value}'\n"
#             classes += "\n    def __str__(self): \n        return self.value\n\n\n"
#
#         classes += service_lookups_class + "\n\n"
#     classes += f"{lookups_class}\n"
#
#     classes += """\nclass RevLookupsSingle:
#     def __init__(self, code, id):
#         self.code = code
#         self.id = id
#
#
# class LookupsReversed:
#     _instance = None
#     _instance_obj = None
#
#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             with open("reversed_lookups.json") as file:
#                 cls._instance = json.load(file)
#         return cls._instance
#
#     @classmethod
#     def get_instance_obj(cls):
#         if not cls._instance_obj:
#             cls._instance_obj = {}
#             with open("reversed_lookups.json") as file:
#                 data = json.load(file)
#             for k in data:
#                 cls._instance_obj[k] = RevLookupsSingle(**data[k])
#                 cls._instance_obj[uuid.UUID(k)] = RevLookupsSingle(**data[k])
#
#         return cls._instance_obj\n"""
#
#     return classes
def generate_class_definitions(yaml_data: Dict[str, Any]) -> str:
    """
    Generates Python class definitions based on the provided YAML data.

    Args:
    yaml_data (Dict[str, Any]): The data extracted from a YAML file.

    Returns:
    str: A string containing the generated Python class definitions.
    """
    classes = "import uuid\nimport json\nfrom enum import Enum\n\n\n"
    lookups_class = "class Lookups:\n\n"

    for service, classes_data in yaml_data.items():
        lookups_types = []
        service_lookups_class = f"class {service}:\n"
        lookups_class += f"    {service} = {service}\n"
        for lookup_type, values in classes_data.items():
            lookups_types.append(lookup_type)
            # service_lookups_class += f"    {class_name} = {class_name}\n"
            service_lookups_class += f"    class {lookup_type}(Enum):\n"
            # service_lookups_class += f"    class {lookup_type}:\n"

            for key, value in values.items():
                service_lookups_class += f"        {key.upper()} = '{value}'\n"
            service_lookups_class += "\n"
            # service_lookups_class += "\n        def __str__(self): \n            return self.value\n\n"

        classes += service_lookups_class
        for lookup_type in lookups_types:
            classes += f"    {lookup_type} = {lookup_type}\n"
        classes += "\n\n"
        # break
    classes += f"{lookups_class}\n\n"

    classes += """class RevLookupsSingle:
    def __init__(self, code, id):
        self.code = code
        self.id = id

    class LookupsReversed:
        _instance = None
        _instance_obj = None

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                with open("reversed_lookups.json") as file:
                    cls._instance = json.load(file)
            return cls._instance

        @classmethod
        def get_instance_obj(cls):
            if not cls._instance_obj:
                cls._instance_obj = {}
                with open("reversed_lookups.json") as file:
                    data = json.load(file)
                for k in data:
                    cls._instance_obj[k] = RevLookupsSingle(**data[k])
                    cls._instance_obj[uuid.UUID(k)] = RevLookupsSingle(**data[k])

            return cls._instance_obj\n"""

    return classes


def generate_class_iterators(yaml_data: Dict[str, Any]) -> str:
    """
    Generates Python class definitions based on the provided YAML data.

    Args:
    yaml_data (Dict[str, Any]): The data extracted from a YAML file.

    Returns:
    str: A string containing the generated Python class definitions.
    """
    # classes = "import uuid\nimport json\nfrom enum import Enum\n\n\n"
    classes = """class LookupSingle:
    def __init__(self, id, code):
        self.id = id
        self.code = code\n\n\n"""
    lookups_class = "class Lookups:\n\n"

    for service, classes_data in yaml_data.items():
        service_lookups_class = f"class {service}:\n"
        lookups_class += f"    {service} = {service}\n"
        for lookup_type, values in classes_data.items():
            service_lookups_class += f"    {lookup_type} = ["
            for key, value in values.items():
                service_lookups_class += f"\n        LookupSingle('{value}','{key}'),"
            service_lookups_class += "\n]\n"

        classes += service_lookups_class
        classes += "\n\n"
    classes += f"{lookups_class}\n\n"

    return classes


def generate_lookups() -> None:
    """
    Generates lookup classes for the application from YAML configurations.
    """
    lookups = {}
    configuration = load_configuration()
    current_folder = pathlib.Path(__file__).parent
    root_folder = current_folder.parent.parent
    for service in configuration["services"]["grpc"]:
        lookups_path = root_folder / "services" / "grpc" / service / "lookups" / f"lookups_{service}.yaml"
        service_lookups = parse_yaml(lookups_path)
        if service_lookups:
            lookups.update(service_lookups)

    lookups_code = generate_class_definitions(lookups)
    with open(current_folder / "lookups.py", "w") as lookups_file:
        lookups_file.write(lookups_code)

    lookups_iterators_code = generate_class_iterators(lookups)
    with open(current_folder / "lookups_iterator.py", "w") as lookups_file:
        lookups_file.write(lookups_iterators_code)

    reversed_lookups = generate_reverse_lookups(lookups)

    with open(current_folder / "reversed_lookups.json", "w") as lookups_file:
        json.dump(reversed_lookups, lookups_file, indent=2)


def generate_reverse_lookups(lookups: dict) -> dict:

    # check for the duplicate ids
    if not hasattr(generate_reverse_lookups, 'id_exists'):
        generate_reverse_lookups.id_exists = set()

    res = {}
    for k, v in lookups.items():
        if isinstance(v, str):
            if str(v) in generate_reverse_lookups.id_exists:
                raise Exception(f"Duplicate id {v} found in lookups for {k}")

            generate_reverse_lookups.id_exists.add(str(v))

            res[v] = {"code": k, "id": v}
        else:
            res.update(generate_reverse_lookups(lookups[k]))
    return res


if __name__ == "__main__":
    generate_lookups()
