
import type { Metadata } from "next";
import { Inter, } from "next/font/google";
import "./globals.css";
import Transitions, { Animate } from "@/components/transitions";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

const shopName = process.env.NEXT_PUBLIC_SHOP_NAME || "tinyshop";

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
    <html lang="en" className="" data-theme="lemonade">
      <body className={inter.className}>
        <Transitions>
          <Animate>
            {children}
          </Animate>
        </Transitions>
        <Toaster />
      </body>

    </html>
  );
}
