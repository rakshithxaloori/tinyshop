"use server";
import CollectionDisplayList from "@/components/collection-display-list";

const ClientProductDisplayList = dynamic(() => import("@/components/product-display-list"), {
  ssr: false,
  loading: () => <div>Loading...</div>
});
import Basic2DHeroSection from "@/template/hero/2d-basic";
import Image3DCarousel from "../3d-image-carousel";
import dynamic from "next/dynamic";

const carouselImages = [
  // Add your image URLs here
  "https://images.unsplash.com/photo-1523437237164-d442d57cc3c9",
  "https://images.unsplash.com/photo-1421930866250-aa0594cea05c",
  "https://images.unsplash.com/photo-1536152470836-b943b246224c",
  "https://images.unsplash.com/photo-1518717202715-9fa9d099f58a",
  "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab",
  "https://images.unsplash.com/photo-1584148721201-b6432e0d5106"
];


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
    <div className="overflow-y-auto scrollbar-hide" data-theme="black">
      <Basic2DHeroSection
        config={heroSectionConfig}
      />

      {/* <Image3DCarousel
        title="Featured Products"
        images={carouselImages}
      /> */}

      <ClientProductDisplayList
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