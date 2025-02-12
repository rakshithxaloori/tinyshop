import { stackServerApp } from "@/stack";
import Tinyshop from "@tinyshop/tinyshop-node";
import { redirect } from "next/navigation";

import ProductTable from "./table";

const Products = async (
  { params: { shop_id } }: { params: { shop_id: string } }
) => {
  const user = await stackServerApp.getUser();
  const teamId = shop_id;
  const dk = user?.serverMetadata.dashboardKeys[teamId];

  const tinyshop = new Tinyshop(dk, process.env.TINYSHOP_API_HOST);
  const products = await tinyshop.products.list();

  return (
    <div className="px-8 py-4">
      <ProductTable products={products.data} />
    </div>
  );
};

export default Products;
