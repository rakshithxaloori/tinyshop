
import type { Metadata } from "next";
import { Inter, } from "next/font/google";
import "./globals.css";
import Transitions, { Animate } from "@/components/transitions";
import { Toaster } from "@/components/ui/sonner";
import ClientSideProvider from "./providers";

const inter = Inter({ subsets: ["latin"] });

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME || "tinyshop";
const globalTheme = process.env.NEXT_PUBLIC_THEME || "retro";

export const metadata: Metadata = {
  title: `${shopName}`,
  description: "e-commerce site powered by tinyshop",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="" data-theme={globalTheme}>
      <body className={inter.className}>
        <Transitions>
          <Animate>
            <ClientSideProvider>
              {children}
            </ClientSideProvider>
          </Animate>
        </Transitions>
        <Toaster />
      </body>

    </html>
  );
}
