from typing import Annotated
from fastapi import Depends, Request


def get_livemode(request: Request) -> bool:
    return request.state.livemode
    # return livemode == "live"


def get_shop_id(request: Request) -> str:
    return request.state.shop_id


ShopIDDep = Annotated[str, Depends(get_shop_id)]
LivemodeDep = Annotated[bool, Depends(get_livemode)]
