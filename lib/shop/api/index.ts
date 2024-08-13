import { ShopCreate } from "./interfaces";

const DASHBOARD_SECRET = process.env.DASHBOARD_SECRET as string;

const baseUrl = "http://127.0.0.1:8000";

const apiFetch = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  const headers = new Headers(options.headers || {});
  headers.append("X-Tinyshop-Dashboard-Secret", DASHBOARD_SECRET);

  const fetchOptions: RequestInit = {
    ...options,
    headers,
  };

  const response = await fetch(url, fetchOptions);

  if (!response.ok) {
    console.log(url);
    console.log(fetchOptions.body);
    const responseHeaders = Array.from(response.headers.entries());
    console.log(responseHeaders);
    console.log(await response.json());
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response;
};

class Api {
  private dashboard_secret: string;

  constructor() {
    this.dashboard_secret = DASHBOARD_SECRET;
  }

  async post(endpoint: string, data: any): Promise<Response> {
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const url = `${baseUrl}${endpoint}`;
    const response = await apiFetch(url, options);
    return response;
  }
}

class DashboardKeys {
  private endpoint: string;
  private api: Api;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/shops/dashboard_keys";
  }
}

class Shops {
  private endpoint: string;
  private api: Api;
  public dashboardKeys: DashboardKeys;

  constructor(api: Api) {
    this.api = api;
    this.endpoint = "/v1/shops";
    this.dashboardKeys = new DashboardKeys(this.api);
  }

  async create(shop: ShopCreate): Promise<{
    dashboard_key: string;
  }> {
    const response = await this.api.post(this.endpoint, shop);
    return response.json();
  }
}

class Tinyshop {
  private api: Api;
  public shops: Shops;

  constructor() {
    this.api = new Api();
    this.shops = new Shops(this.api);
  }
}

export const tinyshop = new Tinyshop();
