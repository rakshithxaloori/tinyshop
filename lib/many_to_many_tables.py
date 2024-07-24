from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from lib.model import SqlBase

if TYPE_CHECKING:
    from discount.model import Discount
    from customer.model import Customer
    from collection.model import Collection
    from product.model import Product
    from cart.model import Cart


class DiscountCustomerLink(SqlBase, table=True):
    """Only these Customers can use the Discount."""

    discount_id: str = Field(foreign_key="discount.id", primary_key=True)
    customer_id: str = Field(foreign_key="customer.id", primary_key=True)

    discount: "Discount" = Relationship(back_populates="customer_links")
    customer: "Customer" = Relationship(back_populates="discount_links")

    # TODO shop, shop id ?


class CartDiscountLinks(SqlBase, table=True):
    """Discounts that are added to Cart."""

    discount_id: str = Field(foreign_key="discount.id", primary_key=True)
    cart_id: str = Field(foreign_key="cart.id", primary_key=True)

    discount: "Discount" = Relationship(back_populates="cart_links")
    cart: "Cart" = Relationship(back_populates="discount_links")


class CollectionProductLink(SqlBase, table=True):
    """Collections and Products."""

    collection_id: str = Field(foreign_key="collection.id", primary_key=True)
    product_id: str = Field(foreign_key="product.id", primary_key=True)

    collection: "Collection" = Relationship(back_populates="product_links")
    product: "Product" = Relationship(back_populates="collection_links")


# TODO create one for customers, shop

# class DiscountOrderLink(SqlBase, table=True):
#     """The Discount has been applied to these Orders."""

#     discount_id: str = Field(foreign_key="discount.id", primary_key=True)
#     order_id: str = Field(foreign_key="order.id", primary_key=True)
