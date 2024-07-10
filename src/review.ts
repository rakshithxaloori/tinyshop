import Api from "./api";
import {
  Review,
  ReviewCreate,
  ReviewUpdate,
  ReviewList,
  ReviewDelete,
} from "../interfaces/review";

export class Reviews {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/reviews";
  }

  async create(data: ReviewCreate): Promise<Review> {
    const response_json: Review = await this.api.post(this.endpoint, data);
    return response_json;
  }

  async update(id: string, data: ReviewUpdate): Promise<Review> {
    const response_json: Review = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Review> {
    const response_json: Review = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(productId?: string, customerId?: string): Promise<ReviewList> {
    const query_params = {
      product: productId,
      customer: customerId,
    };
    const response_json: ReviewList = await this.api.get(
      this.endpoint,
      query_params
    );
    return response_json;
  }

  async delete(id: string): Promise<ReviewDelete> {
    const response_json: ReviewDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
