"use server";
import CollectionDisplayList from "@/components/collection-display-list";
import Basic2DHeroSection from "@/template/hero/2d-basic";
import Image3DCarousel from "../3d-image-carousel";
import dynamic from "next/dynamic";
import ThreeStatementBanner from "../banner/three-statement";

const ClientProductDisplayList = dynamic(() => import("@/components/product-display-horizontal-list"), {
  ssr: false,
  loading: () => <div>Loading...</div>
});

const StorefrontLandingPage = ({
  products,
  collections,
  heroSectionConfig,
  carouselImages
}:
  {
    products: any,
    collections: any,
    heroSectionConfig: any,
    carouselImages: string[]
  }
) => {
  return (
    <div className="overflow-y-auto scrollbar-hide px-lg md:px-xl">
      <Basic2DHeroSection
        config={heroSectionConfig}
      />

      <ThreeStatementBanner
        firstStatement="OUR MISSION"
        secondStatement="Prioritizing Holistic Health"
        thirdStatement="Overwhelmed by quick fixes, diet culture and toxic beauty standards, we set
        out to revolutionize the health industry."
        statementStyles={
          [
            'text-lg',
            'font-semibold mt-md',
            'mt-sm w-full md:max-w-md md:text-center font-normal text-md'
          ]
        }
      />

      <Image3DCarousel
        title="Featured Products"
        images={carouselImages}
      />
      <ClientProductDisplayList
        title="COSMIX ESSENTIALS"
        {...{ products }}
      />
      <CollectionDisplayList
        title="COMMUNITY FAVOURITES"
        {...{ collections }}
      />
    </div>
  );
}

export default StorefrontLandingPage;