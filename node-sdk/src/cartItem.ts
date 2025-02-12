import Api from "./api";
import {
  CartItem,
  CartItemCreate,
  CartItemUpdate,
  CartItemList,
  CartItemDelete,
} from "../interfaces/cartItem";

export class CartItems {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/cart_items";
  }

  async create(data: CartItemCreate): Promise<CartItem> {
    const response_json: CartItem = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: CartItemUpdate): Promise<CartItem> {
    const response_json: CartItem = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<CartItem> {
    const response_json: CartItem = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(cartId: string): Promise<CartItemList> {
    const query_params = { cart: cartId };
    const response_json: CartItemList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<CartItemDelete> {
    const response_json: CartItemDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
