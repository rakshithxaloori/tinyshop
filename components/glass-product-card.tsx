import Image from "next/image";

const GlassProductCard = ({ product }: {
  product: TProduct;

}) => {
  const displayImage = product.images ? product.images[0] : '/images/placeholder.jpg';
  const displayImageAlt = product.images ? product.name : 'Placeholder image';
  return (
    <div className="glass h-[20rem] w-full">
      <div className="glass-content">
        <div className="glass-content-inner">
          {
            (product.images) && (
              <div className="glass-content-front">
                <Image src={product.images[0]} alt={product.name} width={100} height={100} />
              </div>
            )
          }

          <div className="glass-content-back">
            <h1 className="text-2xl font-bold">{product.name}</h1>
            <p>{product.handle}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GlassProductCard;