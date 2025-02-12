import { Skeleton } from "@/components/ui/skeleton";

export default function Loading({
  ...props
}: React.HTMLAttributes<HTMLDivElement> & {
  children?: React.ReactNode;
}) {
  return (
    <div
      className="flex flex-col space-y-4 p-4 min-h-[80vh] bg-base-200 rounded-md"
      {...props}
    >
      <Skeleton className="w-full h-full flex grow" />
    </div>
  )
}