import Api from "./api";
import {
  Invoice,
  InvoiceCreate,
  InvoiceUpdate,
  InvoiceList,
  InvoiceDelete,
} from "../interfaces/invoice";

export class Invoices {
  public endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/invoices";
  }

  async create(data: InvoiceCreate): Promise<Invoice> {
    const response_json: Invoice = await this.api.post(
      this.endpoint,
      data || {}
    );
    return response_json;
  }

  async update(id: string, data: InvoiceUpdate): Promise<Invoice> {
    const response_json: Invoice = await this.api.post(
      `${this.endpoint}/${id}`,
      data
    );
    return response_json;
  }

  async retrieve(id: string): Promise<Invoice> {
    const response_json: Invoice = await this.api.get(`${this.endpoint}/${id}`);
    return response_json;
  }

  async list(): Promise<InvoiceList> {
    const response_json: InvoiceList = await this.api.get(this.endpoint);
    return response_json;
  }

  async delete(id: string): Promise<InvoiceDelete> {
    const response_json: InvoiceDelete = await this.api.delete(
      `${this.endpoint}/${id}`
    );
    return response_json;
  }
}
