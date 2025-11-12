'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: string
  whopUserId: string
  email?: string
  name?: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: () => void
  logout: () => Promise<void>
  refreshSession: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const checkSession = async () => {
    try {
      const response = await fetch('/api/auth/whop/verify')
      const data = await response.json()

      if (data.authenticated && data.user) {
        setUser(data.user)
      } else {
        setUser(null)
      }
    } catch (error) {
      console.error('Session check failed:', error)
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    checkSession()
  }, [])

  const login = () => {
    // Redirect to Whop OAuth for existing users (no checkout)
    const clientId = process.env.NEXT_PUBLIC_WHOP_CLIENT_ID
    const redirectUri = typeof window !== 'undefined'
      ? `${window.location.origin}/api/auth/whop/callback`
      : `${process.env.NEXT_PUBLIC_APP_URL}/api/auth/whop/callback`

    const oauthUrl =
      `https://whop.com/oauth/authorize?` +
      `client_id=${clientId}` +
      `&redirect_uri=${encodeURIComponent(redirectUri)}` +
      `&response_type=code`

    window.location.href = oauthUrl
  }

  const logout = async () => {
    try {
      await fetch('/api/auth/whop/verify', { method: 'DELETE' })
      setUser(null)
      window.location.href = '/'
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  const refreshSession = async () => {
    setIsLoading(true)
    await checkSession()
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshSession,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
