import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const AddToCartButtonStructure = ({ className, onClick }: { className?: string, onClick: React.MouseEventHandler<HTMLButtonElement> }) => {
  return (
    <Button
      className={cn("btn w-full btn-primary rounded-full", className)}
      onClick={onClick}
    >
      Add
    </Button>
  )
}

export default AddToCartButtonStructure;