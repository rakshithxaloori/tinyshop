import Link from 'next/link';

const orders = [
  { id: 1, title: 'Order 1' },
  { id: 2, title: 'Order 2' },
];

export default function OrdersPage() {
  return (
    <div>
      <h2>Orders List</h2>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            <Link href={`/customer/orders/${order.id}`}>{order.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}