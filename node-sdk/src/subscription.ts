import Api from "./api";
import {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
  SubscriptionList,
  SubscriptionDelete,
} from "../interfaces/subscription";

export class Subscriptions {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/subscriptions";
  }

  async create(data: SubscriptionCreate): Promise<Subscription> {
    const response_json: Subscription = await this.api.post(
      this.endpoint,
      data || {}
    );
    return response_json;
  }

  async update(id: string, data: SubscriptionUpdate): Promise<Subscription> {
    const response_json: Subscription = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Subscription> {
    const response_json: Subscription = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(): Promise<SubscriptionList> {
    const response_json: SubscriptionList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<SubscriptionDelete> {
    const response_json: SubscriptionDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
