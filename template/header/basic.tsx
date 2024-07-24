"use client";
import Cart from "@/components/cart";
import SearchBar from "@/components/search-bar";
import { cn } from "@/lib/utils";
import Link from "next/link";
import React, { Suspense } from "react";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
import { PizzaIcon } from "lucide-react";
import Wishlist from "@/components/wishlist";
import useWindowSize from "@/components/hooks/window-size";

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-base-100/50 hover:text-base-content focus:bg-base-100/50 focus:text-base-content",
            className
          )}
          {...props}
        >
          <div className="text-sm font-medium leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-base-content">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  )
})
ListItem.displayName = "ListItem"

const NavItems = ({ navItems }: { navItems: any[] }) => {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuTrigger>Shop</NavigationMenuTrigger>
          <NavigationMenuContent className="bg-primary">
            <ul className="grid gap-3 p-4 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]">
              <li className="row-span-3">
                <NavigationMenuLink asChild>
                  <a
                    className="flex h-full w-full select-none flex-col justify-end rounded-md bg-primary/80 p-6 no-underline outline-none hover:bg-base-100/50 hover:text-base-content"
                    href="/"
                  >
                    <PizzaIcon size={40} />
                    <div className="mb-2 mt-4 text-lg font-medium">
                      Tinyshop
                    </div>
                    <p className="text-sm leading-tight text-primary-content">
                      Tinyshop is a modern e-commerce solution built using Tailwind CSS and Next.js.
                    </p>
                  </a>
                </NavigationMenuLink>
              </li>
              <ListItem href="/collections" title="All products">
                Explore our collections
              </ListItem>
              {
                navItems.map((item) => (
                  <ListItem key={item.url} href={item.url} title={item.name}>
                    {item.description}
                  </ListItem>
                ))
              }
            </ul>
          </NavigationMenuContent>
        </NavigationMenuItem>

      </NavigationMenuList>
    </NavigationMenu>
  )
}

export const BasicMobileHeader = ({
  className,
  navItems,
  cartId
}: {
  navItems: any[],
  cartId: string | null;
  className?: string;
}) => {
  return (
    <header className="border-b py-4 sticky top-0 z-50 bg-base-100 shadow-md">
      <div className="flex max-w-7xl flex-col items-start gap-2 px-4">
        <section className="flex flex-1 w-full items-center gap-2">
          <Link id="basic-header-name" href="/">
            <span className="inline-block -mt-0.5 whitespace-nowrap text-2xl font-bold">Your Store</span>
          </Link>
          <div className="mr-auto grow" />
          <section id="basic-header-wishlist" className="flex space-x-4">
            <Wishlist />
          </section>
          <section id="basic-header-cart" className="flex space-x-4">
            <Cart {...{ cartId }} />
          </section>
        </section>
        <section id="basic-header-search" className="flex space-x-4 w-full mt-sm">
          <Suspense fallback={<div>Loading...</div>}>
            <SearchBar />
          </Suspense>
        </section>

      </div>
    </header>
  );
}

export const BasicDesktopHeader = ({
  className,
  navItems,
  cartId
}: {
  navItems: any[],
  cartId: string | null;
  className?: string;
}) => {
  const sticky = true;
  return (
    <header className={cn("border-b py-4",
      sticky ? "sticky top-0 z-50 bg-base-100 shadow-md" : "",
    )}>
      <div className={cn("sm:items-centerm mx-auto flex max-w-7xl flex-col items-start gap-2 px-4 sm:flex-row sm:flex-wrap sm:items-center sm:px-6 md:flex-nowrap lg:px-8",
        className)}>
        <Link id="basic-header-name" href="/">
          <span className="inline-block -mt-0.5 whitespace-nowrap text-2xl font-bold">Your Store</span>
        </Link>
        <div id="basic-header-nav" className="sm:mr-auto ml-sm">
          <NavItems navItems={navItems} />
        </div>
        <section id="basic-header-right" className="flex space-x-4 min-w-lg ml-auto items-center">
          <section id="basic-header-search" className="flex space-x-4 ml-auto">
            <Suspense fallback={<div>Loading...</div>}>
              <SearchBar />
            </Suspense>
          </section>
          <section id="basic-header-wishlist" className="flex space-x-4">
            <Wishlist />
          </section>
          <section id="basic-header-cart" className="flex space-x-4">
            <Cart {...{ cartId }} />
          </section>
        </section>

      </div>
    </header>
  );
}


const BasicHeader = ({
  className,
  navItems,
  cartId
}: {
  navItems: any[],
  cartId: string | null;
  className?: string;
}) => {
  const { isMobile } = useWindowSize();
  return isMobile ? (
    <BasicMobileHeader {...{ className, navItems, cartId }} />
  ) : (
    <BasicDesktopHeader {...{ className, navItems, cartId }} />
  );
}

export default BasicHeader;