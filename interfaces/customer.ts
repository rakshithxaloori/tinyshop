import { CustomerAddressList } from "./customerAddress";

interface CustomerBase {
  name?: string | null;
}

interface CustomerCreate extends CustomerBase {
  email?: string | null;
  phone: string;
  send_otp?: boolean;
}

interface Customer extends CustomerBase {
  id: string;
  object: "customer";
  is_verified: boolean;
  email?: string | null;
  phone?: string | null;
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
}

interface CustomerDelete {
  id: string;
  object: "customer";
  deleted: boolean;
}

interface CustomerVerify {
  otp?: string | null;
  send_otp?: boolean;
}

export type {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerList,
  CustomerDelete,
  CustomerVerify,
};
