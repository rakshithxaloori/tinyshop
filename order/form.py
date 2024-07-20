import re
from collections import defaultdict
from typing import Annotated
from fastapi import Form, Request
from fastapi.datastructures import FormData


from order import schema


def parse_form_data(form_data: FormData):
    data = defaultdict(dict)

    for key, value in form_data.items():
        match = re.match(r"(\w+)\[(\d+)\]\[(\w+)\]", key)
        if match:
            main_key, index, sub_key = match.groups()
            if main_key not in data:
                data[main_key] = []
            index = int(index)
            while len(data[main_key]) <= index:
                data[main_key].append({})
            data[main_key][index][sub_key] = value
        else:
            data[key] = value

    return dict(data)


async def create_order_form(request: Request) -> schema.OrderCreate:
    form_data = await request.form()
    parsed_data = parse_form_data(form_data)
    order = schema.OrderCreate.model_validate(parsed_data)
    return order


def update_order_form(
    order_type: Annotated[str, Form(alias="type")],
    status: Annotated[str | None, Form()] = None,
) -> schema.OrderUpdate:
    return schema.OrderUpdate(
        type=order_type,
        status=status,
    )
