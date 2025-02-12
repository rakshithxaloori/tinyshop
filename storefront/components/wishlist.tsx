import { HeartIcon } from "lucide-react"
import Link from "next/link"

const Wishlist: React.FC = () => {
  return (
    <Link href="/wishlist">
      <HeartIcon size={24} />
    </Link>
  )
}

export default Wishlist