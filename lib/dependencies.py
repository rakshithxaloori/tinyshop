from typing import Annotated
from fastapi import Depends, Request
from pydantic import BaseModel


from lib.form.parser import parse_form_data


def get_livemode(request: Request) -> bool:
    return request.state.livemode


def get_shop_id(request: Request) -> str:
    return request.state.shop_id


async def get_form(request: Request, schema: BaseModel) -> BaseModel:
    form_data = await request.form()
    parsed_data = parse_form_data(form_data)
    schema_ins = schema.model_validate(parsed_data)
    return schema_ins


ShopIDDep = Annotated[str, Depends(get_shop_id)]
LivemodeDep = Annotated[bool, Depends(get_livemode)]


def FormDep(schema: BaseModel):
    async def dependency(request: Request):
        return await get_form(request, schema)

    return Depends(dependency)
