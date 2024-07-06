import Api from "./api";

export class Prices {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/prices";
  }

  async create(data: PriceCreate): Promise<Price> {
    const response_json: Price = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: PriceUpdate): Promise<Price> {
    const response_json: Price = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Price> {
    const response_json: Price = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(variantId: string): Promise<PriceList> {
    const query_params = { variant: variantId };
    const response_json: PriceList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<PriceDelete> {
    const response_json: PriceDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
