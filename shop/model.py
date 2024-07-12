from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from team.model import Team
    from customer.model import Customer

    from product.model import Product
    from option.model import Option
    from variant.model import Variant
    from price.model import Price
    from collection.model import Collection

    from warehouse.model import Warehouse
    from inventory.model import Inventory

    from cart.model import Cart
    from cart_item.model import CartItem

    from review.model import Review
    from discount.model import Discount


class Shop(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("shop"))
    name: str = Field(nullable=True)

    team_id: str = Field(foreign_key="team.id", unique=True)
    team: "Team" = Relationship(back_populates="shop")
    customers: list["Customer"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    products: list["Product"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    options: list["Option"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    variants: list["Variant"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    prices: list["Price"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    collections: list["Collection"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    warehouses: list["Warehouse"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    inventories: list["Inventory"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    carts: list["Cart"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    cart_items: list["CartItem"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    reviews: list["Review"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    discounts: list["Discount"] = Relationship(
        back_populates="shop",
        sa_relationship_kwargs={"cascade": "delete"},
    )
