from typing import Annotated
from fastapi import Header, Depends


def is_livemode(livemode: str) -> bool:
    return livemode == "live"


ShopIDDep = Annotated[str, Header()]
LivemodeDep = Annotated[str, Header()]
