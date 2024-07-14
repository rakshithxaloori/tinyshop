import Api from "./api";
import {
  CustomerAddress,
  CustomerAddressCreate,
  CustomerAddressUpdate,
  CustomerAddressList,
  CustomerAddressDelete,
} from "../interfaces/customerAddress";

export class CustomerAddresses {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/customer_addresses";
  }

  async create(data: CustomerAddressCreate): Promise<CustomerAddress> {
    const response_json: CustomerAddress = await this.api.post(
      this.endpoint,
      data
    );
    return response_json;
  }

  async update(
    id: string,
    data: CustomerAddressUpdate
  ): Promise<CustomerAddress> {
    const response_json: CustomerAddress = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<CustomerAddress> {
    const response_json: CustomerAddress = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(customerId: string): Promise<CustomerAddressList> {
    const query_params = { customer: customerId };
    const response_json: CustomerAddressList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<CustomerAddressDelete> {
    const response_json: CustomerAddressDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
