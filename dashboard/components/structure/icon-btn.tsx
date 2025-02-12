import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ShoppingCartIcon } from "lucide-react";

const IconButtonStructure = ({ className, onClick }: { className?: string, onClick: React.MouseEventHandler<HTMLButtonElement> }) => {
  return (
    <Button className={cn("btn btn-sm btn-primary", className)}
      onClick={onClick}
    >
      <ShoppingCartIcon size={24} />
    </Button>
  )
}

export default IconButtonStructure;