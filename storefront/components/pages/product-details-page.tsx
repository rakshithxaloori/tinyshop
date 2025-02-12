import ProductVariantSection from "@/sections/product-details-page/variant";
import TabsSection from "@/sections/product-details-page/tabs";
import FAQSection from "@/sections/product-details-page/faq";
import ReviewsSection from "@/sections/product-details-page/reviews";
import RelatedSection from "@/sections/product-details-page/related";
import BreadcrumbSection from "@/sections/product-details-page/breadcrumb";
import { TPriceUI, TProductFAQSection, TProductTabs } from "@/types/product";


const ProductDetailsPage = ({
  product,
  collections,
  reviews,
  faqs,
  tabs,
}: {
  product: any;
  collections: any[];
  reviews: any[];
  faqs: TProductFAQSection | null;
  tabs: TProductTabs[] | null;
}
) => {
  return (
    <div className="flex flex-col flex-1 h-full scroll-mt-[100vh] px-lg md:px-xl">
      <BreadcrumbSection product={product} collections={collections} />
      <ProductVariantSection product={product}
        reviews={reviews}
        fallbackOptions={
          {
            fallbackImage: 'https://via.placeholder.com/400x400'
          }
        }
      />
      <TabsSection data={tabs} />
      <FAQSection data={faqs} />
      <ReviewsSection reviews={reviews}
        config={{
          title: "What our customers say",
        }}
      />
      {/* <RelatedSection product={product} /> */}
    </div>

  );
}

export default ProductDetailsPage;