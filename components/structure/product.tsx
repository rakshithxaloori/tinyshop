import { cn } from "@/lib/utils";
import { css } from "@emotion/css";
import Image from "next/image";
import { z } from 'zod';

export const ProductLayoutSchema = z.object({
  outerContainer: z.string().describe("Emotion css string for the outer container of the product card. This will be placed alongside className = \"card-wrapper cursor-pointer border-primary/60 hover:border-primary md:hover:m-1 transition-all duration-100 ease-linear bg-base-100 border-2 rounded-xl\"."),
  innerContainer: z.string().describe("Emotion css string for the inner container of the product card. This will be placed alongside className = \"group card card-compact\"."),
  imageContainer: z.string().describe("Emotion css string for the image container of the product card. This will be placed alongside className = \"relative aspect-square rounded-t-xl\"."),
  image: z.string().describe("Emotion css string for the image of the product card. This will be placed alongside className = \"w-full h-full group-hover:opacity-75 group-focus:opacity-100 transition-opacity duration-200 ease-in-out\"."),
  wishlistContainer: z.string().describe("Emotion css string for the wishlist container of the product card."),
  badge: z.string().describe("Emotion css string for the badge of the product card. This will be placed alongside className = \"badge badge-primary ml-2 mb-2 absolute top-0 left-0 mt-2 ml-2\"."),
  cardBodyContainer: z.string().describe("Emotion css string for the card body container of the product card. Card body contains the title, price, add to cart button, quantity and icon button. This will be placed alongside className = \"flex m-0 mt-md mx-md\"."),
  titleContainer: z.string().describe("Emotion css string for the title container of the product card. This will be placed alongside className = \"w-full\"."),
  title: z.string().describe("Emotion css string for the title of the product card. This will be placed alongside className = \"group card-title text-base group-hover:opacity-75 transition-opacity duration-200 ease-in-out h-[3rem] line-clamp-2\"."),
  priceContainer: z.string().describe("Emotion css string for the outer container of the price of the product card. This will be placed alongside className = \"group flex justify-between p-2 m-0 mt-xs md:mt-sm  group-hover:opacity-75\"."),
  price: z.string().describe("Emotion css string for the price of the product card."),
  addToCartContainer: z.string().describe("Emotion css string for the Add to cart container of the product card. This will be placed alongside className = \"card-action w-full px-2 visible md:hidden my-sm\"."),
  addToCartButton: z.string().describe("Emotion css string for the Add to cart button of the product card."),
  quantityContainer: z.string().describe("Emotion css string for the quantity container of the product card."),
  quantity: z.string().describe("Emotion css string for the quantity of the product card."),
  iconButtonContainer: z.string().describe("Emotion css string for the icon button container of the product card. This will be placed alongside className = \"card-action flex-1 hidden md:block\"."),
  iconButton: z.string().describe("Emotion css string for the icon button of the product card."),
}).describe("Layout styles for a product card using inline style strings to be used as an input to css`` from @emotion/css. These styles are used in conjunction with the daisyUI and tailwind classes. Generate background using CSS variables of the daisy UI theme colors.");

export type ProductLayout = z.infer<typeof ProductLayoutSchema>;

export const nullProductLayout = {
  outerContainer: "",
  innerContainer: "",
  imageContainer: "",
  image: "",
  wishlistContainer: "",
  badge: "",
  cardBodyContainer: "",
  titleContainer: "",
  title: "",
  priceContainer: "",
  price: "",
  addToCartContainer: "",
  addToCartButton: "",
  quantityContainer: "",
  quantity: "",
  iconButtonContainer: "",
  iconButton: ""
}

type ProductCardData = {
  id: string;
  productImage: string;
  name: string;
  badgeTitle: string | null;
  quantity: number;
  price: number | string;
  currency: string;
}

interface ProductCardStructureProps {
  layout: ProductLayout;
  data: null | ProductCardData;
  actions: {
    handleCardClick: React.MouseEventHandler<HTMLDivElement>;
    handleAddToCart: React.MouseEventHandler<HTMLButtonElement>;
    [key: string]: Function
  };
  wishlist?: React.ComponentType<{ id: string; className?: string }>;
  priceCard?: React.ComponentType<{ className?: string; price: string | number; currency: string; }>;
  addToCartButton?: React.ComponentType<{ className?: string; onClick: React.MouseEventHandler<HTMLButtonElement> }>;
  quantityDisplay?: React.ComponentType<{ className?: string; quantity: number }>;
  iconButton?: React.ComponentType<{ className?: string; onClick: React.MouseEventHandler<HTMLButtonElement> }>;
}

const ProductCardStructure = (props: ProductCardStructureProps) => {
  const {
    layout,
    data,
    actions,
    wishlist: WishlistStructure,
    priceCard: PriceStructure,
    addToCartButton: AddToCartButtonStructure,
    quantityDisplay: QuantityStructure,
    iconButton: IconButtonStructure
  } = props;
  const hasData = data !== null;

  if (!hasData) {
    // TODO
    return null
  }

  return (
    <div
      className={cn(
        "card-wrapper cursor-pointer border-primary/60 hover:border-primary bg-primary md:hover:m-1 transition-all duration-100 ease-linear bg-base-100 border-2 rounded-xl",
        css`${layout.outerContainer}`
      )}
      onClick={actions.handleCardClick}
    // data-theme="coffee"
    >
      <div className={cn("group card card-compact",
        css`${layout.innerContainer}`
      )}>
        <figure className={cn("relative aspect-square rounded-t-xl", css`${layout.imageContainer}`)}>
          <Image src={
            data.productImage
          } alt={data.name}
            className={cn("w-full h-full group-hover:opacity-75 group-focus:opacity-100 transition-opacity duration-200 ease-in-out", css`${layout.image}`)}
            fill
          />
        </figure>
        {
          WishlistStructure && <WishlistStructure className={css`${layout.wishlistContainer}`} id={data.id} />
        }
        {
          data.badgeTitle && <div
            className={cn("badge badge-primary ml-2 mb-2 absolute top-0 left-0 mt-2 ml-2",
              css`${layout.badge}`

            )}
          >{data.badgeTitle}</div>
        }

        <div className={cn("flex flex-col m-0 mt-md mx-md", css`${layout.cardBodyContainer}`)}>
          {/* Title structure */}
          <div className={cn("w-full", css`${layout.titleContainer}`)}>
            <h2 className={cn("group card-title text-base-content group-hover:opacity-75 transition-opacity duration-200 ease-in-out h-[3rem] line-clamp-2",
              css`${layout.title}`
            )}>
              {data.name}
            </h2>
          </div>

          {/* Icon button Structure */}
          {
            IconButtonStructure && (
              <div className={cn("card-action flex-1 hidden md:block", css`${layout.iconButtonContainer}`)}>
                <IconButtonStructure onClick={actions.handleAddToCart}
                  className={css`${layout.iconButton}`}
                />
              </div>
            )
          }

          {/* Price Structure*/}
          <section className="flex flex-row w-full">
            {
              PriceStructure && (
                <div
                  className={cn("group flex justify-between p-2 m-0 mt-xs md:mt-sm  group-hover:opacity-75",
                    css`${layout.priceContainer}`
                  )}>
                  <PriceStructure
                    price={data.price}
                    currency={data.currency}
                    className={css`${layout.price}`}
                  />
                </div>
              )
            }
            <div className="grow" />
            {/* Quantity Structure */}
            {
              QuantityStructure && (
                <div className={cn(css`${layout.quantityContainer}`)}>
                  <QuantityStructure quantity={data.quantity} className={css`${layout.quantity}`} />
                </div>
              )
            }

          </section>
          {/* Add to cart button Structure */}
          {
            AddToCartButtonStructure && (
              <div className={cn("card-action w-full visible my-sm",
                css`${layout.addToCartContainer}`
              )}>
                <AddToCartButtonStructure onClick={actions.handleAddToCart}
                  className={css`${layout.addToCartButton}`}
                />
              </div>
            )
          }
        </div>
      </div>
    </div >
  )

}


export default ProductCardStructure;