"use client";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { DirectionAwareHover } from "./aceternity-ui/direction-aware-hover";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import useCartStore from "@/store/cart";
import { toast } from "sonner";
import Link from "next/link";

const ProductToastCard = ({ product }: { product: TProduct }) => {
  const imageUrl = product.images ? product.images[0] : '/images/placeholder.jpg';
  return (
    <div className="flex flex-1 flex-row w-full gap-x-2">
      <div className="w-1/6 relative">
        <Image src={imageUrl} alt={product.name} fill />
      </div>
      <div className="flex flex-col">
        <p className="clamp-1">
          {product.name}
        </p>
        <p>
          added to cart
        </p>
      </div>
    </div>
  );
}

const ProductCard = ({ product }: { product: TProduct }) => {
  const imageUrl = product.images ? product.images[0] : '/images/placeholder.jpg';
  const addToCart = useCartStore((state) => state.addToCart);
  const removeFromCart = useCartStore((state) => state.removeFromCart);
  const productHref = `/products/${product.handle}`;

  const handleAddToCart = (e: any) => {
    e.preventDefault();
    console.log("add to cart");
    addToCart("domain", "variant_id");
    toast.message(
      <ProductToastCard product={product} />,
    )
  }

  const handleRemoveFromCart = (e: any) => {
    e.preventDefault();
    console.log("remove from cart");
    removeFromCart("domain", "variant_id", false);
    toast("Removed from cart");
  }

  return (
    <div className={
      cn(
        "text-xs md:text-sm pb-1 glass flex flex-col items-center justify-between bg-white border-2 border-gray-200 rounded"
      )
    }>
      <Link href={productHref}>
        <div className="self-start flex flex-row flex-1 z-20  relative top-0 left-0 ml-1 mt-1 gap-x-1">
          <Badge className="bg-white text-black pointer-events-none">New</Badge>
          <Badge className="bg-white text-black pointer-events-none">Sale</Badge>
        </div>

        <div className={cn("aspect-square w-full relative",
          "h-[15rem]",
          "-mt-[1.5rem]"
        )}>
          <DirectionAwareHover imageUrl={imageUrl} className="aspect-square rounded-0"
            childrenClassName="hidden"
          >
            <div />
          </DirectionAwareHover>
        </div>
        <div className="flex flex-col p-1 w-full gap-1">
          <span className={cn("font-medium", "leading-4 h-8", "line-clamp-2")}>{product.name}</span>
          <div className="grow" />

        </div>
      </Link>
      <div className="flex flex-row gap-x-2">
        <Button
          onClick={handleAddToCart}
        >
          Add
        </Button>
        <Button variant="outline"
          onClick={handleRemoveFromCart}
        >
          Remove
        </Button>
      </div>


    </div>
  );
}

export default ProductCard;