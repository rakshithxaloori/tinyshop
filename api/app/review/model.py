import enum
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint


from app.lib.model import SqlBase
from app.lib.primary_key import get_primary_key


if TYPE_CHECKING:
    from app.shop.model import Shop
    from app.customer.model import Customer
    from app.product.model import Product


# An enum that has quick feedback
class FeedbackEnum(str, enum.Enum):
    # Negative feedback
    LOW_QUALITY = "low_quality"
    TOO_EXPENSIVE = "too_expensive"
    OTHER = "other"

    # Positive feedback
    HIGH_QUALITY = "high_quality"
    EASY_TO_USE = "easy_to_use"
    GOOD_VALUE = "good_value"

    # Neutral feedback
    SATISFACTORY = "satisfactory"
    AVERAGE = "average"


class Review(SqlBase, table=True):
    id: str = Field(primary_key=True, default_factory=get_primary_key("review"))
    product_rating: int = Field()  # Out of 5
    shipping_rating: int = Field()  # Out of 5
    feedback: FeedbackEnum = Field(nullable=True)
    review: str = Field(nullable=True)
    image: str = Field(nullable=True)

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
