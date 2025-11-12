import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { supabase } from '@/lib/supabase'

/**
 * Save Analysis Results
 * POST /api/analyses
 */
export async function POST(request: NextRequest) {
  try {
    // Verify user session
    const cookieStore = cookies()
    const sessionCookie = cookieStore.get('fire_planner_session')

    if (!sessionCookie) {
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    const session = JSON.parse(sessionCookie.value)
    const { userId } = session

    // Get analysis data from request body
    const body = await request.json()
    const {
      profileData,
      career,
      roi,
      fire,
      side_hustle,
      interests_roadmap,
    } = body

    if (!profileData || !career || !roi || !fire || !side_hustle || !interests_roadmap) {
      return NextResponse.json(
        { error: 'Missing required analysis data' },
        { status: 400 }
      )
    }

    // Save to Supabase
    const { data, error } = await supabase
      .from('analyses')
      .insert({
        user_id: userId,
        profile_data: profileData,
        career_analysis: career,
        roi_analysis: roi,
        fire_analysis: fire,
        side_hustle_analysis: side_hustle,
        interests_roadmap: interests_roadmap,
      })
      .select()
      .single()

    if (error) {
      console.error('Error saving analysis:', error)
      return NextResponse.json(
        { error: 'Failed to save analysis' },
        { status: 500 }
      )
    }

    return NextResponse.json({
      success: true,
      analysisId: data.id,
    })
  } catch (error) {
    console.error('Save analysis error:', error)
    return NextResponse.json(
      { error: 'Server error' },
      { status: 500 }
    )
  }
}

/**
 * Get User's Analyses
 * GET /api/analyses
 */
export async function GET(request: NextRequest) {
  try {
    // Verify user session
    const cookieStore = cookies()
    const sessionCookie = cookieStore.get('fire_planner_session')

    if (!sessionCookie) {
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    const session = JSON.parse(sessionCookie.value)
    const { userId } = session

    // Get user's analyses from Supabase
    const { data, error } = await supabase
      .from('analyses')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching analyses:', error)
      return NextResponse.json(
        { error: 'Failed to fetch analyses' },
        { status: 500 }
      )
    }

    return NextResponse.json({
      analyses: data || [],
    })
  } catch (error) {
    console.error('Fetch analyses error:', error)
    return NextResponse.json(
      { error: 'Server error' },
      { status: 500 }
    )
  }
}
