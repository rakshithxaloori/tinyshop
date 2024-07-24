import { getHeaderNavItems } from "@/lib/storefront";
import { cn } from "@/lib/utils";
import BasicFooter from "@/template/footer/basic";
import dynamic from "next/dynamic";

const ClientBasicHeader = dynamic(() => import("@/template/header/basic"), {
  ssr: false,
  loading: () => <div>Loading...</div>
});


const StorefrontLayout = async ({ cartId, children }: { cartId: string | null, children: React.ReactNode }) => {
  const navItems = await getHeaderNavItems();
  return (
    <div className={cn("flex flex-col h-full min-h-screen w-full bg-base-100 text-base-content scrollbar-hide",)}
    >
      <ClientBasicHeader {...{ cartId, navItems }} />
      <div className="flex flex-1 justify-center mx-lg md:mx-xl">
        {children}
      </div>
      <BasicFooter />
    </div>
  )
}

export default StorefrontLayout;