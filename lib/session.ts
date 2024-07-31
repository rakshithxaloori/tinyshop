'use server'
import { SignJWT, jwtVerify } from 'jose'
import { cookies } from 'next/headers'

const secretKey = process.env.SECRET_KEY
if (!secretKey) {
  throw new Error('SECRET_KEY is not set in environment variables')
}
const signKey = new TextEncoder().encode(secretKey)

export const encrypt = async (data: Record<string, string>) => {
  const jwt = await new SignJWT(data)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d') // Set expiry to 7 days
    .sign(signKey)

  cookies().set('session', jwt, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 7 * 24 * 60 * 60, // 7 days in seconds
    path: '/'
  })
}

export const decrypt = async (): Promise<Record<string, string> | null> => {
  const jwt = cookies().get('session')?.value

  if (!jwt) {
    return null
  }

  try {
    const { payload } = await jwtVerify(jwt, signKey)
    return payload as Record<string, string>
  } catch (error) {
    console.error('Failed to decrypt session:', error)
    return null
  }
}

export const getSessionData = async (): Promise<{ customerId: string } | null> => {
  const data = await decrypt()
  if (data && 'customerId' in data) {
    return { customerId: data.customerId }
  }
  return null
}

export const setSessionData = async (customerId: string) => {
  const data: Record<string, string> = { customerId }
  await encrypt(data)
}

export const clearSessionData = () => {
  cookies().delete('session')
}

