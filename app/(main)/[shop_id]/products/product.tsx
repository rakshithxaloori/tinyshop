import { Product } from "@tinyshop/tinyshop-node/interfaces/product";

const ProductComponent = ({ product }: { product: Product }) => {
  return (
    <div>
      <span>{product.name}</span>
    </div>
  );
};

export default ProductComponent;
