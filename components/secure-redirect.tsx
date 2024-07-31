import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger
} from "@/components/ui/drawer"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { getSessionData, setSessionData } from '@/lib/session'
import { checkIfAuthenticated } from '@/lib/server-actions'

interface SecureRedirectProps {
  href: string
  children: React.ReactNode
}

function SecureRedirect({ href, children }: SecureRedirectProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [phoneNumber, setPhoneNumber] = useState('')
  const [otp, setOtp] = useState('')
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

  const handlePhoneSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the phone number to your backend
    // and trigger the OTP sending process
    // For this example, we'll just pretend we've sent the OTP
  }

  const handleOtpSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically verify the OTP with your backend
    // For this example, we'll just pretend it's always correct
    await setSessionData('example-customer-id')
    setIsAuthenticated(true)
    setIsDrawerOpen(false)
    router.push(href)
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
            <DrawerHeader >
              <DrawerTitle>Authentication Required</DrawerTitle>
              <DrawerDescription>
                Please enter your phone number to receive an OTP.
              </DrawerDescription>
            </DrawerHeader>
            {!phoneNumber ? (
              <form onSubmit={handlePhoneSubmit} className="p-4 space-y-4">
                <Input
                  type="tel"
                  placeholder="Phone Number"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                />
                <Button type="submit">Send OTP</Button>
              </form>
            ) : (
              <form onSubmit={handleOtpSubmit} className="p-4 space-y-4">
                <Input
                  type="text"
                  placeholder="Enter OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                />
                <Button type="submit">Verify OTP</Button>
              </form>
            )}
          </div>
        </DrawerContent>
      </Drawer>
    </>
  )
}

export default SecureRedirect