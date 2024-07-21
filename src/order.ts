import Api from "./api";
import {
  Order,
  OrderCreate,
  OrderUpdate,
  OrderList,
  OrderDelete,
} from "../interfaces/order";

export class Orders {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/orders";
  }

  async create(data: OrderCreate): Promise<Order> {
    const response_json: Order = await this.api.post(this.endpoint, data || {});
    return response_json;
  }

  async update(id: string, data: OrderUpdate): Promise<Order> {
    const response_json: Order = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Order> {
    const response_json: Order = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(): Promise<OrderList> {
    const response_json: OrderList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<OrderDelete> {
    const response_json: OrderDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
