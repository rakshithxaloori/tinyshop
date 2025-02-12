"use server";
import CollectionDisplayList from "@/components/collection-display-list";
import Basic2DHeroSection from "@/template/hero/2d-basic";
import Image3DCarousel from "../3d-image-carousel";
import dynamic from "next/dynamic";
import ThreeStatementBanner from "../banner/three-statement";
import { ProductLayout } from "../product/card-structure";

const ClientProductDisplayList = dynamic(() => import("@/components/product-display-horizontal-list"), {
  ssr: false,
  loading: () => <div>Loading...</div>
});

const StorefrontLandingPage = ({
  products,
  collections,
  heroSectionConfig,
  carouselImages,
  productCardLayout
}:
  {
    products: any,
    collections: any,
    heroSectionConfig: any,
    carouselImages: string[];
    productCardLayout: ProductLayout
  }
) => {
  return (
    <div className="overflow-y-auto scrollbar-hide px-lg md:px-xl">
      <Basic2DHeroSection
        config={heroSectionConfig}
      />

      <ThreeStatementBanner
        firstStatement="Why YC?"
        secondStatement="We give startups a disproportionate advantage."
        thirdStatement="We help foundersmake something people want and the results speak for themselves."
        statementStyles={
          [
            'text-lg',
            'font-semibold mt-md',
            'mt-sm w-full md:max-w-md md:text-center font-normal text-md'
          ]
        }
      />

      {/* <Image3DCarousel
        title="Featured Products"
        images={carouselImages}
      /> */}
      <ClientProductDisplayList
        title="YC ESSENTIALS"
        {...{ products }}
        layout={productCardLayout}
      />
      <CollectionDisplayList
        title="COMMUNITY FAVOURITES"
        {...{ collections }}
      />
    </div>
  );
}

export default StorefrontLandingPage;