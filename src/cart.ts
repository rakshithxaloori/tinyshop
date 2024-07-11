import Api from "./api";
import {
  Cart,
  CartCreate,
  CartUpdate,
  CartList,
  CartDelete,
} from "../interfaces/cart";

export class Carts {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/carts";
  }

  async create(data?: CartCreate): Promise<Cart> {
    const response_json: Cart = await this.api.post(this.endpoint, data || {});
    return response_json;
  }

  async update(id: string, data: CartUpdate): Promise<Cart> {
    const response_json: Cart = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Cart> {
    const response_json: Cart = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(): Promise<CartList> {
    const response_json: CartList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<CartDelete> {
    const response_json: CartDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
