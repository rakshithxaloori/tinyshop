import base64
from sqlmodel import SQLModel
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

import team.model as team_models
import shop.model as shop_models

import customer.model as customer_models
import customer_address.model as customer_address_models

from product import model as product_models
from option import model as option_models
from variant import model as variant_models
from price import model as price_models

from warehouse import model as warehouse_models
from inventory import model as inventory_models

from cart import model as cart_models
from cart_item import model as cart_item_models

# from discount import model as discount_models

from database import engine

from customer.router import router as customers_router
from customer_address.router import router as customer_addresses_router

from product.router import router as products_router
from option.router import router as options_router
from variant.router import router as variant_router
from price.router import router as price_router

from warehouse.router import router as warehouse_router
from inventory.router import router as inventory_router

from cart.router import router as cart_router
from cart_item.router import router as cart_item_router


SQLModel.metadata.create_all(bind=engine)


app = FastAPI(
    title="tinyshop API",
    version="0.0.1",
    contact={
        "name": "tinyshop",
        "url": "https://support.tinyshop.me/",
        "email": "hi@tinyshop.me",
    },
    root_path="tinyshop",
)


# TODO middleware to log your requests or cache the results


@app.middleware("http")
async def get_credentials(request: Request, call_next):
    # TODO if it's not a dashboard login route
    auth = request.headers.get("Authorization")
    scheme, data = (auth or " ").split(" ", 1)
    if scheme != "Basic":
        return JSONResponse(
            content={"message": "Only Basic Authentication is allowed"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    username, _ = base64.b64decode(data).decode().split(":", 1)
    # TODO check secret key and get shop id
    secret_key = "sk_test_1234abcd"
    if username != secret_key:
        return JSONResponse(
            content={"message": "Secret key is invalid"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    livemode = username.split("_")[1]
    if livemode not in ["live", "test"]:
        return JSONResponse(
            content={"message": "Secret key is invalid"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    request.state.shop_id = "shop_HGoa9bZKaD4VjV6WPubQqJ"
    request.state.livemode = livemode == "live"
    response = await call_next(request)
    return response


app.include_router(customers_router)
app.include_router(customer_addresses_router)

app.include_router(products_router)
app.include_router(options_router)
app.include_router(variant_router)
app.include_router(price_router)

app.include_router(warehouse_router)
app.include_router(inventory_router)

app.include_router(cart_router)
app.include_router(cart_item_router)
