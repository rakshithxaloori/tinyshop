import { CustomerAddressList } from "./customerAddress";

type CUSTOMER_OBJECT = "customer";

interface CustomerBase {
  name?: string | null;
}

interface CustomerCreate extends CustomerBase {
  email?: string | null;
  phone: string;
  send_otp?: boolean | null;
}

interface Customer extends CustomerBase {
  id: string;
  object: CUSTOMER_OBJECT;
  is_verified: boolean;
  email?: string | null;
  phone?: string | null;
}

interface CustomerList {
  object: "list";
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
  object: CUSTOMER_OBJECT;
  deleted: boolean;
}

interface CustomerVerify {
  otp?: string | null;
  send_otp?: boolean | null;
}

export type {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerList,
  CustomerDelete,
  CustomerVerify,
};
