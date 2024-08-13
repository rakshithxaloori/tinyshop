import { stackServerApp } from "@/stack";
import Tinyshop from "@tinyshop/tinyshop-node";
import ProductComponent from "./product";

const Products = async () => {
  const user = await stackServerApp.getUser();
  const dk = user?.serverMetadata.dashboardKeys[user.selectedTeam?.id];
  console.log(dk);
  const tinyshop = new Tinyshop(dk, "http://localhost:8000");
  const products = await tinyshop.products.list();

  return (
    <div>
      <span>Products</span>
      <div>
        {products.data.map((product) => (
          <ProductComponent key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default Products;
