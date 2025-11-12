import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Script from 'next/script'
import { AuthProvider } from '@/contexts/AuthContext'
import ErrorBoundary from '@/components/ErrorBoundary'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Guindo - AI-Powered Career & Life Planning',
  description: 'AI-powered personalized career roadmap, education ROI analysis, FIRE retirement planning, and side income strategies',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://js.whop.com/static/checkout/loader.js"
          strategy="afterInteractive"
        />
      </head>
      <body className={inter.className}>
        <ErrorBoundary>
          <AuthProvider>{children}</AuthProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
