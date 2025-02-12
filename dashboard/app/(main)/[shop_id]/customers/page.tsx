import { stackServerApp } from "@/stack";
import Tinyshop from "@tinyshop/tinyshop-node";
import { redirect } from "next/navigation";
import CustomerComponent from "./customer";

const Customers = async (
  { params: { shop_id } }: { params: { shop_id: string } }
) => {
  const user = await stackServerApp.getUser();
  const teamId = shop_id;
  const dk = user?.serverMetadata.dashboardKeys[teamId];

  const tinyshop = new Tinyshop(dk, "http://localhost:8000");
  const customers = await tinyshop.customers.list();

  return (
    <div>
      <span>Customers</span>
      <div>
        {customers.data.map((customer) => (
          <CustomerComponent key={customer.id} customer={customer} />
        ))}
      </div>
    </div>
  );
};

export default Customers;
