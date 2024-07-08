import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint


from lib.model import SqlBase
from lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from shop.model import Shop
    from customer.model import Customer
    from product.model import Product


# An enum that has quick feedback
class FeedbackEnum(str, enum.Enum):
    CUSTOMER_SERVICE = "customer_service"
    LOW_QUALITY = "low_quality"
    MISSING_FEATURES = "missing_features"
    TOO_COMPLEX = "too_complex"
    TOO_EXPENSIVE = "too_expensive"
    UNUSED = "unused"
    OTHER = "other"


class Review(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("review_"))
    product_rating: int = Field()  # Out of 5
    shipping_rating: int = Field()  # Out of 5
    feedback: FeedbackEnum = Field(nullable=True)
    comment: str = Field(nullable=True)

    shop_id: str = Field(foreign_key="shop.id")
    shop: "Shop" = Relationship(back_populates="reviews")
    customer_id: str = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="reviews")
    product_id: str = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="reviews")

    __table_args__ = (
        UniqueConstraint(
            "customer_id", "product_id", name="unique_product_customer_review"
        ),
    )
