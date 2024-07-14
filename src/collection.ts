import Api from "./api";
import {
  Collection,
  CollectionCreate,
  CollectionUpdate,
  CollectionList,
  CollectionDelete,
} from "../interfaces/collection";
import { OptionalParams } from "../utils/list";

export class Collections {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/collections";
  }

  async create(data: CollectionCreate): Promise<Collection> {
    const response_json: Collection = await this.api.post(
      this.endpoint,
      data || {}
    );
    return response_json;
  }

  async update(id: string, data: CollectionUpdate): Promise<Collection> {
    const response_json: Collection = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async search(
    query: string,
    options?: OptionalParams
  ): Promise<CollectionList> {
    const response_json: CollectionList = await this.api.get(
      `${this.endpoint}/search`,
      {
        query,
        ...options,
      }
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Collection> {
    const response_json: Collection = await this.api.get(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }

  async list(): Promise<CollectionList> {
    const response_json: CollectionList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<CollectionDelete> {
    const response_json: CollectionDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
