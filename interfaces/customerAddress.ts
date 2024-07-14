import { ObjectType } from "../utils/enum";

interface CustomerAddressBase {
  name: string;
  line1: string;
  line2?: string | null;
  city: string;
  state: string;
  country: string;
  postal_code: string;
}

interface CustomerAddressCreate extends CustomerAddressBase {
  customer: string;
}

interface CustomerAddress extends CustomerAddressBase {
  id: string;
  object: typeof ObjectType.CUSTOMER_ADDRESS;
}

interface CustomerAddressList {
  object: string;
  url: string; // TODO
  has_more: boolean;
  data: CustomerAddress[];
}

interface CustomerAddressUpdate {
  name?: string | null;
  line1?: string | null;
  line2?: string | null;
  city?: string | null;
  state?: string | null;
  country?: string | null;
  postal_code?: string | null;
}

interface CustomerAddressDelete {
  id: string;
  object: typeof ObjectType.CUSTOMER_ADDRESS;
  deleted: boolean;
}

export type {
  CustomerAddress,
  CustomerAddressCreate,
  CustomerAddressUpdate,
  CustomerAddressList,
  CustomerAddressDelete,
};
