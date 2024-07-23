import re
from typing import Any
from fastapi.datastructures import FormData


def parse_value(value: str) -> Any:
    # Parse boolean values
    if value.lower() in ["true", "false"]:
        return value.lower() == "true"

    return value


# Flatten nested structures
def flatten(data):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if isinstance(value, dict) and len(value) == 1 and key in value:
                data[key] = flatten(value[key])
            else:
                data[key] = flatten(value)
    elif isinstance(data, list):
        return [flatten(item) for item in data]
    return data


def parse_form_data(form_data: FormData) -> dict[str, Any]:
    """
    Parse form data into a structured dictionary.

    :param form_data: A dictionary of form data where keys are strings and values are strings
    :return: A structured dictionary representing the parsed form data
    """
    result = {}

    for key, value in form_data.multi_items():
        # Parse the value
        parsed_value = parse_value(value)

        # Split the key into parts
        parts = re.findall(r"\w+|\[\d*\]", key)

        current = result
        for i, part in enumerate(parts):
            if part.startswith("[") and part.endswith("]"):
                # Handle array
                index = part[1:-1]
                if index == "":
                    # Simple array (e.g., images[])
                    if parts[i - 1] not in current:
                        current[parts[i - 1]] = []
                    current[parts[i - 1]].append(parsed_value)
                    break
                else:
                    # Array with index (e.g., high[0])
                    index = int(index)
                    if parts[i - 1] not in current:
                        current[parts[i - 1]] = []
                    while len(current[parts[i - 1]]) <= index:
                        current[parts[i - 1]].append({})
                    current = current[parts[i - 1]][index]
            else:
                # Handle dictionary
                if i == len(parts) - 1:
                    current[part] = parsed_value
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

    # Flatten simple arrays
    result = flatten(result)

    return result
