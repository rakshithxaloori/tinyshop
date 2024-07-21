import re
from collections import defaultdict
from typing import Any
from fastapi import Request
from fastapi.datastructures import FormData

from subscription import schema


def parse_form_data(form_data: FormData) -> dict[str, Any]:
    """
    Parse form data into a structured dictionary.

    :param form_data: A dictionary of form data where keys are strings and values are strings
    :return: A structured dictionary representing the parsed form data
    """
    result = {}

    for key, value in form_data.items():
        # Parse boolean values
        if value.lower() in ["true", "false"]:
            value = value.lower() == "true"

        # Split the key into parts
        parts = re.findall(r"\w+|\[\d*\]", key)

        current = result
        for i, part in enumerate(parts):
            if part.startswith("[") and part.endswith("]"):
                # Handle array
                index = part[1:-1]
                if index == "":
                    # Simple array (e.g., high[])
                    if parts[i - 1] not in current:
                        current[parts[i - 1]] = []
                    current[parts[i - 1]].append(value)
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
                    current[part] = value
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

    return result


async def create_subscription_form(request: Request) -> schema.SubscriptionCreate:
    form_data = await request.form()
    parsed_data = parse_form_data(form_data)
    subscription = schema.SubscriptionCreate.model_validate(parsed_data)
    return subscription


async def update_subscription_form(request: Request) -> schema.SubscriptionUpdate:
    form_data = await request.form()
    parsed_data = parse_form_data(form_data)
    subscription = schema.SubscriptionUpdate.model_validate(parsed_data)
    return subscription
