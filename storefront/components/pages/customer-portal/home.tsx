import { cn } from "@/lib/utils";
import Image from "next/image";
import Link from "next/link";

const navigation = {
  categories: [
    {
      featured: [
        {
          name: 'Orders',
          href: '#',
          imageSrc: 'https://images.unsplash.com/44/fN6hZMWqRHuFET5YoApH_StBalmainCoffee.jpg',
          imageAlt:
            'Wooden shelf with gray and olive drab green baseball caps, next to wooden clothes hanger with sweaters.',
        },
        {
          name: 'Addresses',
          href: '/customer/addresses',
          imageSrc: 'https://images.unsplash.com/photo-1569348942716-961cdf07eaaf?q=80&w=2787&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
          imageAlt: 'Drawstring top with elastic loop closure and textured interior padding.',
        },
        {
          name: 'Subscriptions',
          href: '#',
          imageSrc: 'https://tailwindui.com/img/ecommerce-images/category-page-02-image-card-06.jpg',
          imageAlt:
            'Three shirts in gray, white, and blue arranged on table with same line drawing of hands and shapes overlapping on front of shirt.',
        },
        {
          name: 'Reviews',
          href: '#',
          imageSrc: 'https://images.unsplash.com/photo-1633613286991-611fe299c4be?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
          imageAlt:
            'Walnut desk organizer with white modular trays, next to porcelain mug on saucer.',
        },
      ],
    }
  ],
}

const category = navigation.categories[0]

const CustomerPortalHomePage = ({ customerId }: { customerId: string }) => {
  return (
    <div className="grid grid-cols-4 gap-2 my-lg">
      <div className="grid my-md col-span-4">
        Welcome to the Customer Portal
      </div>
      {category.featured.map((item, itemIdx) => (
        <Link key={item.name} href={item.href}>
          <div

            className={cn(
              'group aspect-square relative rounded-md bg-gray-100 col-span-1 cursor-pointer overflow-hidden',
            )}
          >
            <Image
              alt={item.imageAlt}
              src={item.imageSrc}
              className="object-cover object-center group-hover:opacity-75 transition duration-300 ease-in-out"
              fill
            />
            <div className="flex flex-col justify-end relative">
              <div className="bg-white bg-opacity-60 p-4 text-sm relative">
                <span aria-hidden="true" className="absolute inset-0" />
                {item.name}
              </div>
            </div>
          </div>
        </Link>
      ))}

    </div>
  );
}

export default CustomerPortalHomePage;
