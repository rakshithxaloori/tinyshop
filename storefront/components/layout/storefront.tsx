import { getHeaderNavItems } from "@/lib/storefront";
import { cn } from "@/lib/utils";
import BasicFooter from "@/template/footer/basic";
import BasicHeader from "@/template/header/basic";

const StorefrontLayout = async ({
  children,
  theme
}: {
  children: React.ReactNode,
  theme?: string
}) => {
  const navItems = await getHeaderNavItems();

  return (
    <div className={cn("flex flex-col h-full min-h-screen w-full bg-base-100 text-base-content scrollbar-hide",
    )}
      // inject theme into the data-theme attribute only if it exists
      {...(theme ? { 'data-theme': theme } : {})}
    >
      <BasicHeader {...{ navItems }} />
      <div className={cn("flex flex-col flex-1 w-full md:max-w-7xl md:self-center",
      )}>
        {children}
      </div>
      <BasicFooter />
    </div>
  )
}

export default StorefrontLayout;