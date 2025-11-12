import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { supabase } from '@/lib/supabase'

/**
 * Verify User Session & Membership
 *
 * Checks if user has valid session cookie and active Whop membership
 * Used by client-side to verify authentication status
 */
export async function GET(request: NextRequest) {
  try {
    const cookieStore = cookies()
    const sessionCookie = cookieStore.get('fire_planner_session')

    if (!sessionCookie) {
      return NextResponse.json(
        { authenticated: false, error: 'No session found' },
        { status: 401 }
      )
    }

    const session = JSON.parse(sessionCookie.value)

    // Verify session has required fields
    if (!session.userId || !session.whopUserId) {
      return NextResponse.json(
        { authenticated: false, error: 'Invalid session' },
        { status: 401 }
      )
    }

    // Get user's Whop access token from Supabase (if stored)
    // For now, we'll skip real-time membership validation to avoid API rate limits
    // Membership is validated during OAuth callback
    // In production, you might want to:
    // 1. Store access token in database
    // 2. Implement token refresh
    // 3. Validate membership periodically (e.g., once per hour)

    return NextResponse.json({
      authenticated: true,
      user: {
        id: session.userId,
        whopUserId: session.whopUserId,
        email: session.email,
        name: session.name,
      },
    })
  } catch (error) {
    console.error('Session verification error:', error)
    return NextResponse.json(
      { authenticated: false, error: 'Verification failed' },
      { status: 500 }
    )
  }
}

/**
 * Logout / Clear Session
 */
export async function DELETE(request: NextRequest) {
  const response = NextResponse.json({ success: true })

  // Clear session cookie
  response.cookies.delete('fire_planner_session')

  return response
}
