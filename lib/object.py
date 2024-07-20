from enum import Enum


class ObjectType(str, Enum):
    # Customer
    CUSTOMER = "customer"
    CUSTOMER_ADDRESS = "customer_address"
    # Store
    PRODUCT = "product"
    OPTION = "option"
    VARIANT = "variant"
    PRICE = "price"
    COLLECTION = "collection"
    CART = "cart"
    CART_ITEM = "cart_item"
    REVIEW = "review"
    DISCOUNT = "discount"
    # Fulfillment
    WAREHOUSE = "warehouse"
    INVENTORY = "inventory"
    # Billing
    CHECKOUT = "checkout"
    INVOICE = "invoice"
    SUBSCRIPTION = "subscription"
    # Order
    ORDER = "order"
