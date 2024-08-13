import { Satisfy } from "next/font/google";

export const satisfy = Satisfy({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-satisfy",
  weight: ["400"],
});

export default function Logo() {
  return (
    <div className="flex flex-row items-center">
      <span className={`text-2xl ml-2 ${satisfy.className}`}>tinyshop</span>
    </div>
  );
}
