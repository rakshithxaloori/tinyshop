import Tinyshop from "@tinyshop/tinyshop-node";
import { stackServerApp } from "@/stack";
import { redirect } from "next/navigation";
import AiEditorPage from "@/components/page/ai-editor";


const AIEditorDisplayPage = async (
  { params: { shop_id } }: { params: { shop_id: string } }
) => {
  const user = await stackServerApp.getUser();
  const teamId = shop_id;
  const dk = user?.serverMetadata.dashboardKeys[teamId];
  const tinyshop = new Tinyshop(dk, process.env.TINYSHOP_API_HOST);
  const { data: products } = await tinyshop.products.list({ expand: ["default_variant"] });
  const displayProducts = products.slice(0, 4);

  return (
    <AiEditorPage data={displayProducts} />
  );
}

export default AIEditorDisplayPage;