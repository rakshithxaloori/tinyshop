"use server";

import Image from "next/image";
import Link from "next/link";

interface CollectionDisplayListProps {
  title: string;
  collections: any[];
}

const CollectionDisplayListItem = ({ collection }: {
  collection: any
}) => {
  const { name, image_web: image } = collection;
  const handle = "/collections/" + collection.handle;
  return (
    <Link className="group grid grid-rows-[5fr,1fr] auto-rows-min relative border-primary shadow-sm rounded-lg" href={handle}>
      <div className="relative overflow-hidden rounded-lg">
        <Image
          src={image}
          alt={name}
          fill
          className="w-full scale-105 object-cover transition-all group-hover:scale-100 group-hover:opacity-75"
        />
      </div>
      <div className=" gap-2 px-4 py-4 text-base-content">
        <h3 className="text-lg font-bold tracking-tight">{name}</h3>
        <p>Shop Now</p>
      </div>
    </Link>
  )
}

const CollectionDisplayList = ({ title, collections }: CollectionDisplayListProps) => {
  return (
    <section className="w-full my-xl">
      <h2 className="text-3xl md:text-5xl font-normal antialiased text-center uppercase">{title}</h2>
      <div className="mt-lg md:mt-2xl grid lg:grid-cols-2 gap-8 overflow-x-scroll">
        {
          collections.map((collection) => (
            <CollectionDisplayListItem key={collection.name} collection={collection} />
          ))
        }
      </div>
    </section>
  )
}

export default CollectionDisplayList;