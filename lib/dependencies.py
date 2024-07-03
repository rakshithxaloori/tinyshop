from typing import Annotated
from fastapi import Header, Depends


def is_livemode(x_livemode: Annotated[str, Header(include_in_schema=False)]) -> bool:
    return x_livemode == "live"


ShopIDDep = Annotated[str, Header(include_in_schema=False)]
LivemodeDep = Annotated[bool, Depends(is_livemode)]
