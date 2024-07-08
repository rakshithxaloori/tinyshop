// ApiService.ts
// apiFetch.ts
const apiFetch = async (
  url: string,
  secretKey: string,
  options: RequestInit = {}
): Promise<Response> => {
  const headers = new Headers(options.headers || {});
  const encodedCredentials = btoa(`${secretKey}:`);
  headers.append("Authorization", `Basic ${encodedCredentials}`);

  const fetchOptions: RequestInit = {
    ...options,
    headers,
  };

  const response = await fetch(url, fetchOptions);

  if (!response.ok) {
    console.log(url);
    console.log(fetchOptions.body);
    console.log(await response.json());
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response;
};

class ApiService {
  private baseUrl: string;
  private secretKey: string;

  constructor(secretKey: string) {
    this.baseUrl = "http://localhost:8000"; // TODO
    this.secretKey = secretKey;
  }

  async get(
    endpoint: string,
    queryParams?: any
  ): Promise<// | Product
  // | ProductList
  // | Option
  // | OptionList
  // | Variant
  // | VariantList
  // | Price
  // | PriceList
  any> {
    if (queryParams) {
      const query = urlEncode(queryParams);
      endpoint = `${endpoint}?${query}`;
    }
    const url = `${this.baseUrl}${endpoint}`;
    const response = await apiFetch(url, this.secretKey, {
      method: "GET",
    });
    return response.json();
  }

  async post(
    endpoint: string,
    data: //   | ProductCreate
    //   | ProductUpdate
    //   | OptionCreate
    //   | OptionUpdate
    //   | VariantCreate
    //   | VariantUpdate
    //   | PriceCreate
    //   | PriceUpdate
    any
  ): Promise<//   Product | Option | Variant | Price
  any> {
    const url = `${this.baseUrl}${endpoint}`;
    const formBody = urlEncode(data);
    const response = await apiFetch(url, this.secretKey, {
      method: "POST",
      body: formBody,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.json();
  }

  async delete(
    endpoint: string
  ): Promise<//   ProductDelete | OptionDelete | VariantDelete | PriceDelete
  any> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await apiFetch(url, this.secretKey, {
      method: "DELETE",
    });
    return response.json();
  }
}

export default ApiService;

const urlEncode = (data: any) =>
  new URLSearchParams(
    Object.entries(data).reduce((acc, [key, value]) => {
      if (value !== null && value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach((val) => {
            acc.append(`${key}[]`, String(val));
          });
        } else if (typeof value === "object") {
          Object.entries(value).forEach(([subKey, subValue]) => {
            acc.append(`${key}[${subKey}]`, String(subValue));
          });
        } else {
          acc.append(key, String(value));
        }
      }
      return acc;
    }, new URLSearchParams())
  ).toString();
