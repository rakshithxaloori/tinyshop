import Api from "./api";
import {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerList,
  CustomerDelete,
} from "../interfaces/customer";

export class Customers {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/customers";
  }

  async create(data?: CustomerCreate): Promise<Customer> {
    const response_json: Customer = await this.api.post(
      this.endpoint,
      data || {}
    );
    return response_json;
  }

  async update(id: string, data: CustomerUpdate): Promise<Customer> {
    const response_json: Customer = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Customer> {
    const response_json: Customer = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(): Promise<CustomerList> {
    const response_json: CustomerList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<CustomerDelete> {
    const response_json: CustomerDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
