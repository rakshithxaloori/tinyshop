import base64
from sqlmodel import SQLModel
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from lib.error import TinyshopException

import shop.model as shop_models

import customer.model as customer_models
import customer_address.model as customer_address_models

from product import model as product_models
from option import model as option_models
from variant import model as variant_models
from price import model as price_models
from collection import model as collection_models

from warehouse import model as warehouse_models
from inventory import model as inventory_models

from cart import model as cart_models
from cart_item import model as cart_item_models

from review import model as review_models

from discount import model as discount_models

from checkout import model as checkout_models
from subscription import model as subscription_models
from invoice import model as invoice_models
from order import model as order_models


from lib import many_to_many_tables as m2m_models


from database import engine

from customer.router import router as customers_router
from customer_address.router import router as customer_addresses_router

from product.router import router as products_router
from option.router import router as options_router
from variant.router import router as variants_router
from price.router import router as prices_router
from collection.router import router as collections_router

from warehouse.router import router as warehouses_router
from inventory.router import router as inventory_router

from cart.router import router as carts_router
from cart_item.router import router as cart_items_router

from review.router import router as reviews_router

from discount.router import router as discounts_router

from checkout.router import router as checkouts_router
from subscription.router import router as subscriptions_router
from invoice.router import router as invoices_router
from order.router import router as orders_router

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


@app.exception_handler(TinyshopException)
async def tinyshop_exception_handler(request: Request, exc: TinyshopException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.type,
            "code": exc.code,
            "message": exc.message,
            "param": exc.param,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # TODO handle form incorrect name and type errors
    print(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Hmmmmmm", "Error": "Name field is missing"},
    )


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
    request.state.shop_id = "shop_Qs88gs4YWcffZ7ChQeiSYQ"
    request.state.livemode = livemode == "live"
    response = await call_next(request)
    return response


app.include_router(customers_router)
app.include_router(customer_addresses_router)

app.include_router(products_router)
app.include_router(options_router)
app.include_router(variants_router)
app.include_router(prices_router)
app.include_router(collections_router)

app.include_router(warehouses_router)
app.include_router(inventory_router)

app.include_router(carts_router)
app.include_router(cart_items_router)

app.include_router(reviews_router)
app.include_router(discounts_router)

app.include_router(checkouts_router)
app.include_router(subscriptions_router)
app.include_router(invoices_router)
app.include_router(orders_router)
