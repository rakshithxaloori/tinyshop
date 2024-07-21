import Api from "./api";
import {
  Checkout,
  CheckoutCreate,
  CheckoutUpdate,
  CheckoutList,
  CheckoutDelete,
} from "../interfaces/checkout";

export class Checkouts {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/checkouts";
  }

  async create(data: CheckoutCreate): Promise<Checkout> {
    const response_json: Checkout = await this.api.post(
      this.endpoint,
      data || {}
    );
    return response_json;
  }

  async update(id: string, data: CheckoutUpdate): Promise<Checkout> {
    const response_json: Checkout = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Checkout> {
    const response_json: Checkout = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(): Promise<CheckoutList> {
    const response_json: CheckoutList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<CheckoutDelete> {
    const response_json: CheckoutDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
