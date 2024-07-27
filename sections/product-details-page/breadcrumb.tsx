import {
  Breadcrumb,
  BreadcrumbEllipsis,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import React from "react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const BreadcrumbSection = ({ product, collections }: { product: any; collections: any[] }) => {
  const { name } = product;
  const isMultipleCollections = collections.length > 1
  const isImplicitCollection = collections.length === 0

  return (
    <Breadcrumb className="mt-lg">
      <BreadcrumbList>
        <BreadcrumbItem>
          <BreadcrumbLink href="/collections">All Products</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        {
          isMultipleCollections ? (
            <React.Fragment>
              <BreadcrumbItem>
                <DropdownMenu>
                  <DropdownMenuTrigger className="flex items-center gap-1">
                    <BreadcrumbEllipsis className="h-4 w-4" />
                    <span className="sr-only">Toggle menu</span>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="start">
                    {
                      collections.map((collection: any) => {
                        return (
                          <DropdownMenuItem key={collection.url}>
                            <BreadcrumbLink href={collection.url}>{collection.name}</BreadcrumbLink>
                          </DropdownMenuItem>
                        )
                      })
                    }
                  </DropdownMenuContent>
                </DropdownMenu>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
            </React.Fragment>
          ) : (
            !isImplicitCollection && <React.Fragment>
              <BreadcrumbItem>
                <BreadcrumbLink href={collections[0].url}>{collections[0].name}</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
            </React.Fragment>
          )
        }
        <BreadcrumbItem >
          <BreadcrumbPage className="font-semibold">{name}</BreadcrumbPage>
        </BreadcrumbItem>
      </BreadcrumbList>
    </Breadcrumb>
  )
}

export default BreadcrumbSection