import { stackServerApp } from "@/stack";
import Tinyshop from "@tinyshop/tinyshop-node";
import { redirect } from "next/navigation";

import ProductTable from "./table";

const Products = async () => {
  const user = await stackServerApp.getUser();
  if (!user?.selectedTeam?.id) {
    redirect("/");
  }
  const dk = user?.serverMetadata.dashboardKeys[user.selectedTeam?.id];

  const tinyshop = new Tinyshop(dk, "http://localhost:8000");
  const products = await tinyshop.products.list();

  return (
    <div>
      <span>Products</span>
      <ProductTable products={products.data} />
    </div>
  );
};

export default Products;
