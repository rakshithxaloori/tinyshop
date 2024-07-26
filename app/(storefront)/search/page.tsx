import SearchPageComponent from "@/components/pages/search-page";
import { Metadata } from "next";

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME! as string || "tinyshop";
export const metadata: Metadata = {
  title: `Search - ${shopName}`,
  description: "Search for products",
};

const SearchPage = () => {
  return (
    <SearchPageComponent indexName="test_products" />
  );
}

export default SearchPage;