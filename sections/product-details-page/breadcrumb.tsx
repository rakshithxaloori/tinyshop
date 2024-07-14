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

const BreadcrumbSection = ({ product, collections }: { product: any; collections: any[] }) => {
  const { name } = product;
  // TODO: handle multiple collections
  return (
    <Breadcrumb className="mt-lg">
      <BreadcrumbList>
        <BreadcrumbItem>
          <BreadcrumbLink href="/collections">All Products</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        {
          collections.map((collection: any) => {
            return (
              <React.Fragment key={collection.url}>
                <BreadcrumbItem>
                  <BreadcrumbLink href={collection.url}>{collection.name}</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator />
              </React.Fragment>
            )
          })
        }
        <BreadcrumbItem >
          <BreadcrumbPage className="font-semibold">{name}</BreadcrumbPage>
        </BreadcrumbItem>
      </BreadcrumbList>
    </Breadcrumb>
  )
}

export default BreadcrumbSection