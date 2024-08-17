"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Logo from "@/components/logo";
import { Badge } from "@/components/ui/badge";

function classNames(...classes: (string | undefined | null)[]) {
  return classes.filter(Boolean).join(" ");
}

const navLinks = [
  {
    name: "Dashboard",
    href: "",
  },
  {
    name: "Orders",
    href: "/orders",
  },
  {
    name: "Products",
    href: "/products",
  },
  {
    name: "Customers",
    href: "/customers",
  },
  {
    name: "AI Editor",
    href: "/ai-editor",
  },
];

const DashboardLinks = () => {
  const pathname = usePathname();
  const teamId = pathname.split("/")[1];

  return (
    <nav className="flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
      <Link
        href=""
        className="flex items-center gap-2 text-lg font-semibold md:text-base"
      >
        <Logo />
      </Link>
      {navLinks.map((navLink) => (
        <Link
          key={navLink.href}
          href={`/${teamId}${navLink.href}`}
          className={classNames(
            pathname === `/${teamId}${navLink.href}`
              ? "text-foreground bg-muted"
              : "text-muted-foreground hover:bg-muted hover:text-foreground",
            "transition-colors duration-100 ease-in-out hover:text-foreground w-auto px-4 py-2  rounded-lg text-nowrap"
          )}
        >
          {navLink.name}
          {
            (navLink.name === "AI Editor") &&
            <Badge className="ml-2">
              Beta
            </Badge>}
        </Link>
      ))}
    </nav>
  );
};

export default DashboardLinks;
