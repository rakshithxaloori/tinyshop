import TinyshopLogo from "@/components/logo";
import { css } from "@emotion/css";
import { LockIcon } from "lucide-react";
import Image from "next/image";

export const metadata = {
  title: "AI Editor",
  tags: ["ai", "editor"],
}

const PlaygroundLayout = ({ children }: {
  children: React.ReactNode;
}) => {
  return (
    <div className="min-h-screen min-h-[100svh] flex flex-col">
      <div className="sticky top-0 z-20">
        <header className="flex w-full flex-col gap-3 p-3 md:h-16 md:flex-row md:items-center lg:px-4 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
          <div className="flex w-full items-center gap-8">
            <div className="flex items-center gap-2">
              <a className="rounded focus:outline-0 focus:ring-0 focus-visible:bg-zinc-200" data-testid="header-logo" href="/">
                <span className="sr-only">Home</span>
                <TinyshopLogo />
              </a>
            </div>
            <div className="ml-auto flex items-center gap-2 sm:gap-4" data-testid="header-right">
              <a className="inline-flex shrink-0 items-center justify-center whitespace-nowrap font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-sh-primary text-sh-primary-foreground shadow hover:bg-sh-primary/90 h-8 px-3 text-xs gap-[6px] rounded-full" data-id="header-new-button" href="/">
                <span className="hidden sm:inline">New Generation</span><span className="sm:hidden">New</span>
              </a>
              <button className="shrink-0 items-center justify-center whitespace-nowrap transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background font-medium hover:bg-accent hover:text-accent-foreground h-8 px-3 text-xs hidden gap-[6px] rounded-full shadow-none sm:flex" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="radix-:rgd:" data-state="closed">
                Feedback
              </button>
              <button className="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 text-gray-500 hover:bg-gray-100 hover:text-gray-900 h-8 w-8 shrink-0 rounded-full border" id="menu-trigger-button" type="button" aria-haspopup="menu" aria-expanded="false" data-state="closed">
                <Image alt="Avatar"
                  src="https://vercel.com/api/www/avatar/6Ysz26mlstSJz7qUXt2n8opm?s=64"
                  height="32" width="32" className="relative flex shrink-0 rounded-full"
                />
                <span className="sr-only">Toggle Menu</span>
              </button>
            </div>
          </div>
        </header >
      </div >

      <main className="flex-1">
        {children}
      </main>

    </div >

  );
}

export default PlaygroundLayout;