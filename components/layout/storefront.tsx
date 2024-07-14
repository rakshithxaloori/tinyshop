import { getHeaderNavItems } from "@/lib/storefront";
import { cn } from "@/lib/utils";
import BasicFooter from "@/template/footer/basic";
import BasicHeader from "@/template/header/basic";

const StorefrontLayout = async ({ children }: { children: React.ReactNode }) => {
  const navItems = await getHeaderNavItems();
  return (
    <div className={cn("flex flex-col h-full min-h-screen w-full bg-base-200 text-base-content",)}
      data-theme="black"
    >
      <BasicHeader {...{ navItems }} />
      <div className="flex flex-1 justify-center mx-sm md:mx-xl">
        {children}
      </div>
      <BasicFooter />
    </div>
  )
}

export default StorefrontLayout;