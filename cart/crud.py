from sqlmodel import Session, select

from cart.model import Cart
from cart import schema
from cart_item.model import CartItem
from cart.utils import pydantify_carts
from lib.session import update_instance
from discount.model import Discount
from lib.many_to_many_tables import CartDiscountLinks


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

        new_ci = None
        cart_item = cart.cart_item
        if cart_item:
            ci_data = cart_item.model_dump(exclude={"price"})
            new_ci = CartItem(
                shop_id=shop_id,
                livemode=livemode,
                cart_id=new_cart.id,
                price_id=cart_item.price,
                **ci_data,
            )
            db.add(new_ci)

        db.commit()
        db.refresh(new_cart)
        if new_ci:
            db.refresh(new_ci)

        py_carts = pydantify_carts([new_cart])
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
        data = cart.model_dump(exclude_none=True, exclude={"discounts"})
        statement = (
            select(Cart)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == cart_id)
        )
        results = db.exec(statement)
        cart_ins = results.one()
        update_instance(db, data, cart_ins)
        discounts = cart.discounts
        if discounts:
            # TODO validate cart - whether discount applies to the cart
            if discounts.add:
                dis_res = db.exec(
                    select(Discount.id)
                    .where(Discount.shop_id == shop_id)
                    .where(Discount.livemode == livemode)
                    .where(Discount.id.in_(discounts.add))
                )
                dis_ids = list(dis_res.all())
                for dis_id in dis_ids:
                    new_cd_link = CartDiscountLinks(
                        livemode=livemode,
                        cart_id=cart_ins.id,
                        discount_id=dis_id,
                    )
                    cart_ins.discount_links.append(new_cd_link)
                    db.add(new_cd_link)
            if discounts.remove:
                cd_links_res = db.exec(
                    select(CartDiscountLinks)
                    .where(CartDiscountLinks.livemode == livemode)
                    .where(CartDiscountLinks.cart_id == cart_ins.id)
                    .where(CartDiscountLinks.discount_id.in_(discounts.remove))
                )
                cd_links = cd_links_res.all()
                for cd_link in cd_links:
                    db.delete(cd_link)
            db.add(cart_ins)
        db.commit()
        db.refresh(cart_ins)
        py_carts = pydantify_carts([cart_ins])
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
            select(Cart)
            .where(Cart.shop_id == shop_id)
            .where(Cart.livemode == livemode)
            .where(Cart.id == cart_id)
        )
        all_rows = list(results.all())
        print(all_rows)
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
    results = db.exec(
        select(Cart)
        .where(Cart.shop_id == shop_id)
        .where(Cart.livemode == livemode)
        .offset(skip)
        .limit(limit)
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
