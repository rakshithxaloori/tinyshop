import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";

import DashboardLinks from "./links";
import { UserButton } from "@stackframe/stack";

function Dashboard({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen min-h-[100svh] w-full flex-col ">
      <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
        <DashboardLinks />
        <div className="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
          <form className="ml-auto flex-1 sm:flex-initial">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search products..."
                className="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
              />
            </div>
          </form>
          <UserButton />
        </div>
      </header>
      <main className="flex-1 px-4 md:px-6">{children}</main>
    </div>
  );
}

export default Dashboard;
