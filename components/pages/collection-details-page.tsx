import Image from "next/image"
import ProductDisplayList from "../product-display-list"

const CollectionDetailsPage = ({
  collection
}: {
  collection: any
}) => {

  const { name, image_web: image } = collection

  const { products: products_raw } = collection
  const { data: all_products } = products_raw;

  return (
    <div className="my-lg">
      {/* Collection display banner */}
      <div className="my-sm min-h-[15rem] relative w-full">
        <Image
          src={image}
          alt={name}
          fill
          className="w-full object-cover border-primary shadow-lg rounded-lg opacity-60"
        />

        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-3xl font-bold tracking-tight bg-base-300 px-[1.25rem] py-[0.5rem] rounded-xl bg-opacity-60 text-base-content">{name}</h1>
        </div>

      </div>

      {/* Product Grid */}
      <ProductDisplayList
        name="All Products"
        products={all_products}
      />
    </div >
  )

}

export default CollectionDetailsPage