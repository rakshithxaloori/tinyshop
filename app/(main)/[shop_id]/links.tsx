"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Logo from "@/components/logo";

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
    name: "Analytics",
    href: "/analytics",
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
              ? "text-foreground"
              : "text-muted-foreground",
            "transition-colors hover:text-foreground"
          )}
        >
          {navLink.name}
        </Link>
      ))}
    </nav>
  );
};

export default DashboardLinks;
