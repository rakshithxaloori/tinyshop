from typing import Annotated
from fastapi import Header, Depends


def is_livemode(x_livemode: Annotated[str, Header()]) -> bool:
    return x_livemode == "live"


ShopIDDep = Annotated[str, Header()]
LivemodeDep = Annotated[bool, Depends(is_livemode)]
