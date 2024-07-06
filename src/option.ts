import Api from "./api";

export class Options {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/options";
  }

  async create(data: OptionCreate): Promise<Option> {
    const response_json: Option = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: OptionUpdate): Promise<Option> {
    const response_json: Option = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Option> {
    const response_json: Option = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(productId: string): Promise<OptionList> {
    const query_params = { product: productId };
    const response_json: OptionList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<OptionDelete> {
    const response_json: OptionDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
