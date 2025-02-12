import Api from "./api";
import { Variant, VariantCreate, VariantUpdate, VariantList, VariantDelete } from "../interfaces/variant";

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

  async list(productId: string): Promise<VariantList> {
    const query_params = { product: productId };
    const response_json: VariantList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<VariantDelete> {
    const response_json: VariantDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
