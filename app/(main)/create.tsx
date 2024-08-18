import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { createNewTeam } from "@/lib/shop";
import { redirect } from "next/navigation";

export function DialogCreate() {
  const createShop = async (formdata: FormData) => {
    "use server";
    if (!formdata.get("name")) return;
    const teamId = await createNewTeam(formdata.get("name") as string);
    if (teamId) {
      redirect(`/${teamId}`);
    }
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Create New Shop</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Shop</DialogTitle>
          <DialogDescription>
            New beginnings. Click create when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <form action={createShop}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">
                Shop Name
              </Label>
              <Input
                id="name"
                name="name"
                placeholder="Apple"
                required
                className="col-span-3"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Create</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
