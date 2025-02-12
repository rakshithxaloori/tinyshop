import PlaygroundPage from "@/components/page/playground";
import { getProductList } from "@/lib/fetcher";

const PlaygroundDisplayPage = async () => {
  const all_products_raw = await getProductList();
  const { data: products } = all_products_raw;

  // show 6 products at max
  const productsToShow = products.slice(0, 4);
  return (
    <PlaygroundPage data={productsToShow} />
  );
}

export default PlaygroundDisplayPage;