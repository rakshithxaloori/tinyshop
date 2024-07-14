import CollectionDisplayList from "@/components/collection-display-list";
import ProductDisplayList from "@/components/product-display-list";
import Basic2DHeroSection from "@/template/hero/2d-basic";

const StorefrontLandingPage = ({
  products,
  collections,
  heroSectionConfig
}:
  {
    products: any,
    collections: any,
    heroSectionConfig: any
  }
) => {
  return (
    <div className="">
      <Basic2DHeroSection
        config={heroSectionConfig}
      />

      <ProductDisplayList
        name="All Products"
        {...{ products }}
      />
      <CollectionDisplayList
        {...{ collections }}
      />
    </div>
  );
}

export default StorefrontLandingPage;