"use client";
import { cn } from "@/lib/utils";
import { CustomerAddress, CustomerAddressList } from "@tinyshop/tinyshop-node/interfaces/customerAddress";

interface AddressListItemProps {
  address: CustomerAddress;
  onEdit: () => void;
  onDelete: () => void;
  className?: string;
}

const AddressListItem = ({ address, onEdit, onDelete, className }: AddressListItemProps) => {
  // while constructing the address string, we need to make sure that we don't include null values
  const addressLine2 = address.line2 ? `${address.line2}, ` : "";
  const combinedAddress = `${address.line1}, ${addressLine2}${address.city}, ${address.state}, ${address.country}, ${address.postal_code}`;

  // const combinedAddress = `${address.line1}, ${address.line2}, ${address.city}, ${address.state}, ${address.country}, ${address.postal_code}`;


  return (
    <div className={cn("col-span-1 border-2 border-primary rounded-sm md:rounded-lg p-sm md:p-md", className)}>
      <h1 className="text-lg font-bold mb-sm md:mb-sm">{address.name}</h1>

      <p className="text-base-content text-sm break-words overflow-hidden">{combinedAddress}</p>
      <div className="flex gap-2 mt-sm">
        <button onClick={onEdit} className="btn btn-sm btn-primary">Edit</button>
        <button onClick={onDelete} className="btn btn-sm btn-primary">Delete</button>
      </div>
    </div>
  )
}
const AddressList = ({ addressList }: { addressList: CustomerAddressList }) => {
  const { data } = addressList;
  return (
    <div className="grid grid-cols-3 gap-2 my-md md:my-lg">
      {data.map((address) => (
        <AddressListItem
          key={address.id}
          address={address}
          onEdit={() => { }}
          onDelete={() => { }}
        />
      ))

      }
    </div>
  )

}

const CustomerAddressPage = ({
  customerAddressList
}:
  {
    customerAddressList: CustomerAddressList
  }
) => {

  return (
    <div className="my-md md:my-lg">
      <h1 className="text-3xl text-bold">My Addresses</h1>
      <AddressList addressList={customerAddressList} />
    </div>
  )

}

export default CustomerAddressPage;