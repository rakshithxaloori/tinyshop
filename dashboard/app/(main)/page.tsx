import { stackServerApp } from "@/stack";
import Shops from "./list";
import { DialogCreate } from "./create";
import Logo from "@/components/logo";

async function Main() {
  const user = await stackServerApp.getUser({ or: "redirect" });
  const allTeams = await user.listTeams();

  return (
    <div className="min-h-full">
      <nav className="flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
        <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b w-full bg-background px-4 md:px-6">
          <Logo />
        </header>
      </nav>
      {/* <div className="md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Shops
          </h2>
        </div>
        <div className="mt-4 flex md:ml-4 md:mt-0">
          <DialogCreate />
        </div>
      </div> */}
      <main className="py-10">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Shops teams={allTeams} />
        </div>
      </main>
    </div>
  );
}

export default Main;
