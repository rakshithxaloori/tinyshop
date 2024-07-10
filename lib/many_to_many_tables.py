from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from lib.model import SqlBase

if TYPE_CHECKING:
    from discount.model import Discount
    from customer.model import Customer


class DiscountCustomerLink(SqlBase, table=True):
    """Only these Customers can use the Discount."""

    discount_id: str = Field(foreign_key="discount.id", primary_key=True)
    customer_id: str = Field(foreign_key="customer.id", primary_key=True)

    discount: "Discount" = Relationship(back_populates="customer_links")
    customer: "Customer" = Relationship(back_populates="discount_links")


# TODO create one for customers, shop

# class DiscountOrderLink(SqlBase, table=True):
#     """The Discount has been applied to these Orders."""

#     discount_id: str = Field(foreign_key="discount.id", primary_key=True)
#     order_id: str = Field(foreign_key="order.id", primary_key=True)
