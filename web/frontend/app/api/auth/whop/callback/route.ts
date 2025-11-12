import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'
import { getWhopUser } from '@/lib/whop'

/**
 * Whop OAuth Callback Handler
 *
 * This endpoint is called by Whop after successful payment
 * Flow: User pays → Whop redirects here with code → We verify & create user
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const code = searchParams.get('code')
    const error = searchParams.get('error')

    // Check for errors from Whop
    if (error) {
      console.error('Whop auth error:', error)
      return NextResponse.redirect(
        new URL(`/?error=auth_failed&message=${error}`, request.url)
      )
    }

    if (!code) {
      return NextResponse.redirect(
        new URL('/?error=no_code', request.url)
      )
    }

    // Exchange code for access token
    const tokenResponse = await fetch('https://api.whop.com/v1/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        client_id: process.env.NEXT_PUBLIC_WHOP_CLIENT_ID,
        client_secret: process.env.WHOP_CLIENT_SECRET,
        grant_type: 'authorization_code',
        redirect_uri: `${process.env.NEXT_PUBLIC_APP_URL}/api/auth/whop/callback`,
      }),
    })

    if (!tokenResponse.ok) {
      const errorData = await tokenResponse.json()
      console.error('Whop token exchange failed:', errorData)
      return NextResponse.redirect(
        new URL('/?error=token_failed', request.url)
      )
    }

    const tokenData = await tokenResponse.json()
    const { access_token } = tokenData

    // Get detailed user info from Whop
    const userInfo = await getWhopUser(access_token)

    if (!userInfo) {
      console.error('Failed to fetch user info from Whop')
      return NextResponse.redirect(
        new URL('/?error=user_fetch_failed', request.url)
      )
    }

    // Verify user has active membership for our plan
    try {
      const planId = process.env.NEXT_PUBLIC_WHOP_PLAN_ID
      const membershipResponse = await fetch(
        `https://api.whop.com/v1/me/memberships`,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        }
      )

      if (!membershipResponse.ok) {
        console.error('Failed to fetch memberships')
        return NextResponse.redirect(
          new URL('/?error=membership_check_failed', request.url)
        )
      }

      const memberships = await membershipResponse.json()
      const activeMembership = memberships.data?.find(
        (m: any) => m.plan_id === planId && m.status === 'active'
      )

      if (!activeMembership) {
        console.error('No active membership found for plan:', planId)
        return NextResponse.redirect(
          new URL('/?error=no_active_membership', request.url)
        )
      }
    } catch (membershipError) {
      console.error('Membership validation error:', membershipError)
      // Continue anyway - user might have just purchased
    }

    // Check or create user in Supabase
    const { data: existingUser } = await supabase
      .from('users')
      .select('*')
      .eq('whop_user_id', userInfo.id)
      .single()

    let userId: string

    if (existingUser) {
      // User exists, update their info
      userId = existingUser.id
      await supabase
        .from('users')
        .update({
          email: userInfo.email,
          name: userInfo.name || userInfo.username,
          updated_at: new Date().toISOString(),
        })
        .eq('id', userId)
    } else {
      // Create new user
      const { data: newUser, error: createError } = await supabase
        .from('users')
        .insert({
          whop_user_id: userInfo.id,
          email: userInfo.email,
          name: userInfo.name || userInfo.username,
        })
        .select()
        .single()

      if (createError || !newUser) {
        console.error('Error creating user:', createError)
        return NextResponse.redirect(
          new URL('/?error=user_creation_failed', request.url)
        )
      }

      userId = newUser.id
    }

    // Create a session cookie
    const response = NextResponse.redirect(
      new URL('/questionnaire', request.url)
    )

    // Set secure HTTP-only cookie with user session
    response.cookies.set({
      name: 'fire_planner_session',
      value: JSON.stringify({
        userId,
        whopUserId: userInfo.id,
        email: userInfo.email,
        name: userInfo.name || userInfo.username,
      }),
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: '/',
    })

    return response
  } catch (error) {
    console.error('Callback error:', error)
    return NextResponse.redirect(
      new URL('/?error=unexpected', request.url)
    )
  }
}
