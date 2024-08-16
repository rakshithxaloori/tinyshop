import { Customer } from "@tinyshop/tinyshop-node/interfaces/customer";

const CustomerComponent = ({ customer }: { customer: Customer }) => {
  return (
    <div>
      <span>{customer.name}</span>
    </div>
  );
};

export default CustomerComponent;
