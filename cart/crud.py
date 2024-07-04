from sqlmodel import Session, select

from cart.model import Cart
from cart import schema
from cart_item.model import CartItem
from cart.utils import pydantify_carts
from lib.session import update_instance


def create_cart(
    shop_id: str,
    livemode: bool,
    cart: schema.CartCreate,
    db: Session,
) -> schema.Cart | None:
    try:
        cart_data = cart.model_dump(exclude={"cart_item"})
        new_cart = Cart(
            shop_id=shop_id,
            livemode=livemode,
            **cart_data,
        )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)

        new_ci = None
        cart_item = cart.cart_item
        if cart_item:
            ci_data = cart_item.model_dump(exclude={"price"})
            new_ci = CartItem(
                livemode=livemode,
                cart_id=new_cart.id,
                price_id=cart_item.price,
                **ci_data,
            )
            db.add(new_ci)
            db.commit()
            db.refresh(new_ci)
        py_carts = pydantify_carts([(new_cart, new_ci)])
        return py_carts.pop()
    except Exception as e:
        print("EXCEPTION create_cart:", e)
        return None


def update_cart(
    shop_id: str,
    livemode: bool,
    cart_id: str,
    cart: schema.CartUpdate,
    db: Session,
) -> schema.Cart | None:
    try:
        update_data = cart.model_dump(exclude_none=True)
        statement = (
            select(Cart)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == cart_id)
        )
        results = db.exec(statement)
        updated_cart = results.one()
        update_instance(db, update_data, updated_cart)
        py_carts = pydantify_carts([(updated_cart, None)])
        return py_carts.pop()

    except Exception as e:
        print("EXCEPTION update_cart:", e)
        return None


def retrieve_cart(
    shop_id: str,
    livemode: bool,
    cart_id: str,
    db: Session,
) -> schema.Cart | None:
    try:
        results = db.exec(
            select(Cart, CartItem)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == cart_id)
            .where(Cart.id == CartItem.cart_id)
        )
        all_rows = list(results.all())
        py_carts = pydantify_carts(all_rows)
        return py_carts.pop()
    except Exception as e:
        print("EXCEPTION retrieve_cart:", e)
        return None


def list_carts(
    shop_id: str,
    livemode: bool,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.CartList:
    subquery = select(Cart.id).offset(skip).limit(limit).subquery()

    results = db.exec(
        select(Cart, CartItem)
        .where(Cart.shop_id == shop_id)
        .where(Cart.livemode == livemode)
        .where(Cart.id.in_(subquery))
        .where(Cart.id == CartItem.cart_id)
    )
    all_rows = list(results.all())
    carts = pydantify_carts(all_rows)
    return schema.CartList(
        has_more=False,  # TODO
        data=carts,
    )


def delete_cart(
    shop_id: str,
    livemode: bool,
    cart_id: str,
    db: Session,
) -> str | None:
    try:
        results = db.exec(
            select(Cart)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == cart_id)
        )
        cart = results.one()
        db.delete(cart)
        db.commit()
        return cart.id
    except Exception as e:
        print("EXCEPTION delete_cart:", e)
        return None
