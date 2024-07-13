import { tinyshop } from "./tinyshop"

// Cart DS

type TItemChain = {
  priceId: string;
  variantId: string;
  productId: string;
}

type TCartItem = {
  id: string;
  quantity: number;
} & TItemChain;

export class Cart {
  id: string;
  items: TCartItem[];

  constructor(id: string = "", items: TCartItem[] = []) {
    this.id = id;
    this.items = items;
  }

  async initCart(id: string = "", items: TCartItem[] = []) {
    if (id) {
      this.id = id;
      this.items = items;
    } else {
      const cart = await tinyshop.carts.create();
      this.id = cart.id;
      this.items = [];
    }
  }

  findItemByItemId(itemId: string) {
    return this.items.find(i => i.id === itemId);
  }

  findItemByPriceId(priceId: string) {
    return this.items.find(i => i.priceId === priceId);
  }

  findItemByVariantId(variantId: string) {
    return this.items.find(i => i.variantId === variantId);
  }

  findItemByProductId(productId: string) {
    return this.items.find(i => i.productId === productId);
  }

  // Always add a new item or increase the quantity of an existing item
  async addItem(chain: TItemChain, quantity: number) {
    // Check if the item already exists
    const existingItem = this.findItemByPriceId(chain.priceId);
    if (existingItem) {
      existingItem.quantity += quantity;
      // update the backend cartItems with the new quantity
      const _ = await tinyshop.cartItems.update(existingItem.id, { quantity: existingItem.quantity });
    } else {
      const newItem = await tinyshop.cartItems.create({
        cart: this.id,
        price: chain.priceId,
        quantity
      });
      this.items.push({
        id: newItem.id,
        quantity,
        ...chain
      });
    }
  }

  async removeItem(chain: TItemChain, quantity: number) {
    // Check if the item already exists
    const existingItem = this.findItemByPriceId(chain.priceId);
    if (!existingItem) {
      return;
    }

    if (existingItem) {
      existingItem.quantity -= quantity;
    }
    // If the quantity is 0, remove the item from the cart
    if (existingItem.quantity === 0) {
      const _ = await tinyshop.cartItems.delete(existingItem.id);
      this.items = this.items.filter(i => i.priceId !== chain.priceId);
    } else {
      // update the backend cartItems with the new quantity
      const _ = await tinyshop.cartItems.update(existingItem.id, { quantity: existingItem.quantity });
    }
  }

  async clearCartItem(cartItemId: string) {
    // Check if the item already exists
    const existingItem = this.findItemByItemId(cartItemId);
    if (!existingItem) {
      return;
    }

    const _ = await tinyshop.cartItems.delete(existingItem.id);
    this.items = this.items.filter(i => i.id !== cartItemId);
  }

  clearCart() {
    // Delete all items from the cart
    const _i = this.items.forEach(async item => {
      const _ = await tinyshop.cartItems.delete(item.id);
    });
    this.items = [];
  }
}

// export type of the Cart class
export type TCart = Cart;