import ProductVariantSection from "@/sections/product-details-page/variant";
import TabsSection from "@/sections/product-details-page/tabs";
import FAQSection from "@/sections/product-details-page/faq";
import ReviewsSection from "@/sections/product-details-page/reviews";
import RelatedSection from "@/sections/product-details-page/related";

const ProductDetailsPage = ({
  product
}: {
  product: any;
}
) => {
  return (
    <div className="flex flex-col flex-1 h-full">
      <ProductVariantSection product={product}
        fallbackOptions={
          {
            fallbackImage: 'https://via.placeholder.com/400x400'
          }
        }
      />
      <TabsSection product={product} config={{}} />
      <FAQSection product={product} />
      <ReviewsSection product={product} />
      <RelatedSection product={product} />
    </div>

  );
}

export default ProductDetailsPage;