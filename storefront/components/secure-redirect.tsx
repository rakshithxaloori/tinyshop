import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import {
  Drawer,
  DrawerContent,
} from "@/components/ui/drawer"
import { checkIfAuthenticated } from '@/lib/server-actions'
import PhoneAuth from './phone-auth'

interface SecureRedirectProps {
  href: string
  children: React.ReactNode
}

function SecureRedirect({ href, children }: SecureRedirectProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const router = useRouter()

  useEffect(() => {
    checkSession()
  }, [])

  const checkSession = async () => {
    const isAuth = await checkIfAuthenticated()
    setIsAuthenticated(isAuth)
    setIsLoading(false)
  }

  const handleClick = () => {
    if (isAuthenticated) {
      router.push(href)
    } else {
      setIsDrawerOpen(true)
    }
  }

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <>
      <div onClick={handleClick}>{children}</div>
      <Drawer direction='bottom' open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <DrawerContent className='max-sm:h-full md:h-fit flex flex-1 items-center bg-base-100 text-base-content'>
          <div className='max-w-lg mx-auto p-lg'>
            <PhoneAuth />
          </div>
        </DrawerContent>
      </Drawer>
    </>
  )
}

export default SecureRedirect