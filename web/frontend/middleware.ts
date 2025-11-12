import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Protected routes that require authentication
  const protectedRoutes = ['/dashboard', '/questionnaire']

  // Check if the current route is protected
  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route))

  if (isProtectedRoute) {
    // Check for session cookie
    const sessionCookie = request.cookies.get('fire_planner_session')

    if (!sessionCookie) {
      // No session - redirect to payment page
      return NextResponse.redirect(new URL('/payment', request.url))
    }

    try {
      // Verify session has valid data
      const session = JSON.parse(sessionCookie.value)

      if (!session.userId || !session.whopUserId) {
        // Invalid session - redirect to payment page
        return NextResponse.redirect(new URL('/payment', request.url))
      }

      // Verify active Whop membership
      // Note: We validate membership in the verify endpoint instead of here
      // to avoid making API calls on every request (performance)
      // The verify endpoint handles membership validation with caching

    } catch (error) {
      // Invalid session format - redirect to payment page
      return NextResponse.redirect(new URL('/payment', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
