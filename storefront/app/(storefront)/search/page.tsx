import SearchPageComponent from "@/components/pages/search-page";
import { getProductLayoutDetails } from "@/lib/storefront";
import { Metadata } from "next";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";
export const metadata: Metadata = {
  title: `Search - ${shopName}`,
  description: "Search for products",
};

const SearchPage = async () => {

  const mongoLayout = await getProductLayoutDetails(shopName);
  const cardLayout = mongoLayout?.layout || null;
  if (!cardLayout) {
    throw new Error('No layout found for the brand');
  }


  return (
    <SearchPageComponent indexName="test_products" layout={cardLayout} />
  );
}

export default SearchPage;