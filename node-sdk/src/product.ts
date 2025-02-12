import Api from "./api";
import {
  Product,
  ProductCreate,
  ProductUpdate,
  ProductList,
  ProductDelete,
} from "../interfaces/product";
import { OptionalParams } from "../utils/list";

export class Products {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/products";
  }

  async create(data: ProductCreate): Promise<Product> {
    const response_json: Product = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: ProductUpdate): Promise<Product> {
    const response_json: Product = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async search(query: string, options?: OptionalParams): Promise<ProductList> {
    const response_json: ProductList = await this.api.get(
      `${this.endpoint}/search`,
      {
        query,
        ...options,
      }
    );
    return response_json;
  }

  async retrieve(id: string, options?: OptionalParams): Promise<Product> {
    const response_json: Product = await this.api.get(`${this.endpoint}/${id}`, options);
    return response_json;
  }

  async list(options?: OptionalParams): Promise<ProductList> {
    const response_json: ProductList = await this.api.get(
      this.endpoint,
      options
    );
    return response_json;
  }

  async delete(id: string): Promise<ProductDelete> {
    const response_json: ProductDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
