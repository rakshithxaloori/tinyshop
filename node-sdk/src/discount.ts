import Api from "./api";
import {
  Discount,
  DiscountCreate,
  DiscountUpdate,
  DiscountList,
  DiscountDelete,
} from "../interfaces/discount";

export class Discounts {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/discounts";
  }

  async create(data: DiscountCreate): Promise<Discount> {
    const response_json: Discount = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: DiscountUpdate): Promise<Discount> {
    const response_json: Discount = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Discount> {
    const response_json: Discount = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(): Promise<DiscountList> {
    const response_json: DiscountList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<DiscountDelete> {
    const response_json: DiscountDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
