from sqlmodel import Session, select

from cart.model import Cart
from cart.cart_item.model import CartItem
from cart.cart_item import schema
from cart.cart_item.utils import pydantify_cart_items
from lib.session import update_refresh


def create_cart_item(
    x_shop_id: str,
    livemode: bool,
    cart_id: str,
    cart_item: schema.CartItemCreate,
    db: Session,
) -> schema.CartItem | None:
    with db.begin():
        try:
            cart_res = db.exec(
                select(Cart)
                .where(Cart.shop_id == x_shop_id)
                .where(Cart.livemode == livemode)
                .where(Cart.id == cart_id)
            )

            cart = cart_res.one()
            ci_data = cart_item.model_dump()
            new_ci = CartItem(
                cart_id=cart.id,
                **ci_data,
            )
            db.add(new_ci)
            db.commit()
            db.refresh(new_ci)
            py_cart_items = pydantify_cart_items([new_ci])
            return py_cart_items.pop()
        except Exception as e:
            print("EXCEPTION create_cart_item:", e)
            return None


def update_cart_item(
    x_shop_id: str,
    livemode: bool,
    cart_id: str,
    cart_item_id: str,
    cart_item: schema.CartItemUpdate,
    db: Session,
) -> schema.CartItem | None:
    with db.begin():
        try:
            update_data = cart_item.model_dump(exclude_none=True)
            results = db.exec(
                select(Cart)
                .where(Cart.livemode == livemode)
                .where(CartItem.cart_id == cart_id)
                .where(CartItem.id == cart_item_id)
            )
            updated_ci = results.one()
            update_refresh(db, update_data, updated_ci)
            py_cis = pydantify_cart_items([updated_ci])
            return py_cis.pop()
        except Exception as e:
            print("EXCEPTION update_cart_item:", e)
            return None


def retrieve_cart_item(
    x_shop_id: str,
    livemode: bool,
    cart_id: str,
    cart_item_id: str,
    db: Session,
) -> schema.CartItem | None:
    with db.begin():
        try:
            results = db.exec(
                select(CartItem)
                .where(CartItem.livemode == livemode)
                .where(CartItem.cart_id == cart_id)
                .where(CartItem.id == cart_item_id)
            )
            ci = results.one()
            py_cis = pydantify_cart_items([ci])
            return py_cis.pop()
        except Exception as e:
            print("EXCEPTION retrieve_cart_item:", e)
            return None


def list_cart_items(
    x_shop_id: str,
    livemode: bool,
    cart_id: str,
    db: Session,
    skip: str = None,
    limit: int = 50,
) -> schema.CartItemList:
    with db.begin():
        # TODO skip and limit
        results = db.exec(
            select(CartItem)
            .where(CartItem.livemode == livemode)
            .where(CartItem.cart_id == cart_id)
            .offset(skip)
            .limit(limit)
        )
        all_rows = list(results.all())
        cart_items = pydantify_cart_items(all_rows)
        return schema.CartItemList(
            url="/v1/carts/{cart_id}/cart_items".format(cart_id=cart_id),
            has_more=False,
            data=cart_items,
        )


def delete_cart_item(
    x_shop_id: str,
    livemode: bool,
    cart_id: str,
    cart_item_id: str,
    db: Session,
) -> schema.CartItemDelete | None:
    with db.begin():
        try:
            results = db.exec(
                select(CartItem)
                .where(CartItem.livemode == livemode)
                .where(CartItem.cart_id == cart_id)
                .where(CartItem.id == cart_item_id)
            )
            ci = results.one()
            db.delete(ci)
            db.commit()
            return ci.id
        except Exception as e:
            print("EXCEPTION delete_cart_item:", e)
            return None
