import Tinyshop from "@tinyshop/tinyshop-node";
import { stackServerApp } from "@/stack";
import { redirect } from "next/navigation";
import AiEditorPage from "@/components/page/ai-editor";

const AIEditorDisplayPage = async () => {
  const user = await stackServerApp.getUser();
  if (!user?.selectedTeam?.id) {
    redirect("/");
  }
  const dk = user?.serverMetadata.dashboardKeys[user.selectedTeam?.id];
  const tinyshop = new Tinyshop(dk);
  const { data: products } = await tinyshop.products.list({ expand: ["default_variant"] });
  const displayProducts = products.slice(0, 4);


  return (
    <AiEditorPage data={displayProducts} />
  );
}

export default AIEditorDisplayPage;