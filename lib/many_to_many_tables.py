from sqlmodel import Field
from lib.model import SqlBase


# TODO discount
# class DiscountCustomerLink(SqlBase, table=True):
#     """Only these Customers can use the Discount."""

#     discount_id: str = Field(foreign_key="discount.id", primary_key=True)
#     customer_id: str = Field(foreign_key="customer.id", primary_key=True)


# TODO create one for customers, shop

# class DiscountOrderLink(SqlBase, table=True):
#     """The Discount has been applied to these Orders."""

#     discount_id: str = Field(foreign_key="discount.id", primary_key=True)
#     order_id: str = Field(foreign_key="order.id", primary_key=True)
