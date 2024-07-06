import Api from "./api";

export class Variants {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/variants";
  }

  async create(data: VariantCreate): Promise<Variant> {
    const response_json: Variant = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: VariantUpdate): Promise<Variant> {
    const response_json: Variant = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Variant> {
    const response_json: Variant = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(
    query_params: VariantListQueryParams
  ): Promise<VariantList> {
    const query = new URLSearchParams(query_params as Record<string, string>);
    const response_json: VariantList = await this.api.get(`${this.endpoint}?${query}`);
    return response_json;
  }

  async delete(id: string): Promise<VariantDelete> {
    const response_json: VariantDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
