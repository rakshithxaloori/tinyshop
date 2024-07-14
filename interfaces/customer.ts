import { CustomerAddressCreate, CustomerAddressList } from "./customerAddress";

interface CustomerBase {
  name: string;
  email?: string | null;
  phone: string;
}

interface CustomerCreate extends CustomerBase {
  address?: CustomerAddressCreate | null;
}

interface Customer extends CustomerBase {
  id: string;
  object: string;
  addresses?: CustomerAddressList | null;
}

interface CustomerList {
  object: string;
  url: string;
  has_more: boolean;
  data: Customer[];
}

interface CustomerUpdate {
  name?: string | null;
  email?: string | null;
  phone?: string | null;
}

interface CustomerDelete {
  id: string;
  object: string;
  deleted: boolean;
}

export {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerList,
  CustomerDelete,
};
