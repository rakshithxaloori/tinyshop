import { stackServerApp } from "@/stack";
import Tinyshop from "@tinyshop/tinyshop-node";
import { redirect } from "next/navigation";
import CustomerComponent from "./customer";

const Customers = async () => {
  const user = await stackServerApp.getUser();
  if (!user?.selectedTeam?.id) {
    redirect("/");
  }
  const dk = user?.serverMetadata.dashboardKeys[user.selectedTeam?.id];

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
