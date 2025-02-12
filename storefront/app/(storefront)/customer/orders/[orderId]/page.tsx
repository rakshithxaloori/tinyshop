import Link from 'next/link';

export default function OrderDetailsPage(
  { params: { orderId } }: Readonly<{ params: { orderId: string } }>,
) {
  return (
    <div>
      <h2>Order Details for Order {orderId}</h2>
      <p>Details about the order...</p>
      <Link href="/customer/orders">Back to Orders List</Link>
    </div>
  );
}