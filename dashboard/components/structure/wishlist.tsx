"use client";

import { cn } from "@/lib/utils";
import { HeartIcon } from "lucide-react";
import { useState } from "react";

// TODO: Implement WishlistStructure as HOC.
// infact, all the child structures should be implemented as HOCs.
// they should be able to accept a className prop and pass it to the root element.

const WishlistStructure = ({ id, className }: { id: string; className?: string }) => {
  const [ok, setOk] = useState<boolean>(false);
  return (
    <div className={cn("absolute top-0 right-0 m-0 mt-2 mr-2 p-0", className)}>
      <label className={cn("swap swap-flip p-0 m-0",
        { "swap-active": ok }

      )}
        onClick={(e) => setOk((k) => !k)}
      >
        <HeartIcon size={24}
          fillOpacity={0.5}
          className="swap-on fill-primary stroke-primary" />
        <HeartIcon size={24}
          className="swap-off stroke-primary/80"
        />
      </label>
    </div >
  )
}

export default WishlistStructure;