from datetime import datetime, timedelta
from sqlmodel import Session, select


from checkout.model import Checkout, CheckoutLineItem, CheckoutStatusEnum
from customer.model import Customer
from customer_address.model import CustomerAddress
from checkout.utils import pydantify_checkouts
from checkout import schema
from cart.model import Cart


def create_checkout(
    shop_id: str,
    livemode: bool,
    checkout: schema.CheckoutCreate,
    db: Session,
) -> schema.Checkout | None:
    try:
        checkout_data = checkout.model_dump(
            exclude={"cart", "customer", "customer_address", "url"}
        )
        cart_res = db.exec(
            select(Cart)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == checkout.cart)
        )
        cart = cart_res.one()
        customer_res = db.exec(
            select(Customer.id)
            .where(Customer.shop_id == shop_id)
            .where(Customer.livemode == livemode)
            .where(Customer.id == checkout.customer)
        )
        customer_id = customer_res.one()
        ca_res = db.exec(
            select(CustomerAddress.id)
            .where(CustomerAddress.livemode == livemode)
            .where(CustomerAddress.customer_id == checkout.customer)
            .where(CustomerAddress.id == checkout.customer_address)
        )
        ca_id = ca_res.one()
        amount_subtotal = 0
        amount_discount = 0
        amount_shipping = 0
        amount_tax = 0
        for ci in cart.items:
            amount_subtotal += ci.price.unit_amount

        # TODO discount, shipping, tax

        amount_total = amount_subtotal - amount_discount + amount_shipping + amount_tax
        new_checkout = Checkout(
            shop_id=shop_id,
            livemode=livemode,
            cart_id=cart.id,
            customer_id=customer_id,
            customer_address_id=ca_id,
            amount_subtotal=amount_subtotal,
            amount_discount=amount_discount,
            amount_shipping=amount_shipping,
            amount_tax=amount_tax,
            amount_total=amount_total,
            # Expires in 1 hour
            expires_at=int((datetime.now() + timedelta(days=1)).timestamp()),
            **checkout_data,
        )
        new_checkout.url = checkout.url.replace("{CHECKOUT_ID}", new_checkout.id)
        db.add(new_checkout)
        # Create Checkout Lines
        for ci in cart.items:
            new_cli = CheckoutLineItem(
                livemode=livemode,
                quantity=ci.quantity,
                checkout_id=new_checkout.id,
                price_id=ci.price_id,
            )
            db.add(new_cli)
        db.commit()
        db.refresh(new_checkout)
        py_checkouts = pydantify_checkouts([new_checkout])
        return py_checkouts.pop()
    except Exception as e:
        print("EXCEPTION create_checkout:", e)
        return None


def update_checkout(
    shop_id: str,
    livemode: bool,
    checkout_id: str,
    checkout: schema.CheckoutUpdate,
    db: Session,
) -> schema.Checkout | None:
    try:
        checkout_res = db.exec(
            select(Checkout)
            .where(Checkout.shop_id == shop_id)
            .where(Checkout.livemode == livemode)
            .where(Checkout.id == checkout_id)
        )
        checkout_ins = checkout_res.one()
        ca_res = db.exec(
            select(CustomerAddress.id)
            .where(CustomerAddress.livemode == livemode)
            .where(CustomerAddress.customer_id == checkout_ins.customer_id)
            .where(CustomerAddress.id == checkout.customer_address)
        )
        ca_id = ca_res.one()
        checkout_ins.customer_address_id = ca_id
        db.add(checkout_ins)
        db.commit()
        db.refresh(checkout_ins)
        py_checkouts = pydantify_checkouts([checkout_ins])
        return py_checkouts.pop()

    except Exception as e:
        print("EXCEPTION update_checkout:", e)
        return None


def retrieve_checkout(
    shop_id: str,
    livemode: bool,
    checkout_id: str,
    db: Session,
) -> schema.Checkout | None:
    try:
        results = db.exec(
            select(Checkout)
            .where(Checkout.shop_id == shop_id)
            .where(Checkout.livemode == livemode)
            .where(Checkout.id == checkout_id)
        )
        ch_ins = results.one()
        py_chs = pydantify_checkouts([ch_ins])
        return py_chs.pop()

    except Exception as e:
        print("EXCEPTION retrieve_checkout:", e)
        return None


def list_checkouts(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.CheckoutList:
    results = db.exec(
        select(Checkout)
        .where(Checkout.shop_id == shop_id)
        .where(Checkout.livemode == livemode)
        .offset(skip)
        .limit(limit)
    )
    ch_rows = list(results.all())
    checkouts = pydantify_checkouts(ch_rows)
    return schema.CheckoutList(
        url="/v1/checkouts",
        data=checkouts,
        has_more=False,  # TODO
    )


def delete_checkout(
    shop_id: str,
    livemode: bool,
    checkout_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Checkout)
            .where(Checkout.shop_id == shop_id)
            .where(Checkout.livemode == livemode)
            .where(Checkout.id == checkout_id)
        )
        ch_ins = results.one()
        db.delete(ch_ins)
        db.commit()
        return ch_ins.id
    except Exception as e:
        print("EXCEPTION delete_checkout:", e)
        return None
