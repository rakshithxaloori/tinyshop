import Image from "next/image";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Product } from "@tinyshop/tinyshop-node/interfaces/product";

interface ProductTableProps {
  products: Product[];
}

const ProductTable: React.FC<ProductTableProps> = ({ products }) => {
  const getBadgeVariant = (
    status: boolean,
    type: "active" | "shippable" | "preorder"
  ): "default" | "secondary" | "destructive" | "outline" => {
    if (type === "active") return status ? "default" : "destructive";
    if (type === "shippable") return status ? "default" : "secondary";
    if (type === "preorder") return status ? "outline" : "secondary";
    return "default";
  };

  return (
    <Table>
      {/* <TableCaption>A list of your products.</TableCaption> */}
      <TableHeader>
        <TableRow>
          <TableHead>
            <span className="sr-only">Image</span>
          </TableHead>
          <TableHead>Name</TableHead>
          <TableHead>Active</TableHead>
          <TableHead>Shippable</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {products.map((product) => (
          <TableRow key={product.id}>
            <TableCell>
              {product.images && product.images.length > 0 ? (
                <div className="relative h-16 w-16">
                  <Image
                    src={product.images[0]}
                    alt={product.name}
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
              ) : (
                <span className="text-gray-400">No image</span>
              )}
            </TableCell>
            <TableCell className="font-semibold">
              {product.name}
              {/* <Badge variant={getBadgeVariant(product.preorder, "preorder")}>
                {product.preorder ? "Preorder" : "In Stock"}
              </Badge> */}
            </TableCell>

            <TableCell>
              <Badge variant={getBadgeVariant(product.active, "active")}>
                {product.active ? "Active" : "Inactive"}
              </Badge>
            </TableCell>
            <TableCell>
              <Badge variant={getBadgeVariant(product.shippable, "shippable")}>
                {product.shippable ? "Shippable" : "Non-shippable"}
              </Badge>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default ProductTable;
