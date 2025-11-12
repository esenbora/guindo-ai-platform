'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { Sparkles, Calendar, TrendingUp, LogOut, Loader2, FileText } from 'lucide-react'
import ResultsDisplay from '@/components/ResultsDisplay'

interface Analysis {
  id: string
  created_at: string
  profile_data: any
  career_analysis: string
  roi_analysis: string
  fire_analysis: string
  side_hustle_analysis: string
  interests_roadmap: string
}

export default function Dashboard() {
  const { user, isAuthenticated, isLoading, logout } = useAuth()
  const router = useRouter()
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [selectedAnalysis, setSelectedAnalysis] = useState<Analysis | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/')
    }
  }, [isAuthenticated, isLoading, router])

  useEffect(() => {
    if (isAuthenticated) {
      fetchAnalyses()
    }
  }, [isAuthenticated])

  const fetchAnalyses = async () => {
    try {
      const response = await fetch('/api/analyses')
      const data = await response.json()

      if (data.analyses) {
        setAnalyses(data.analyses)
      }
    } catch (error) {
      console.error('Error fetching analyses:', error)
    } finally {
      setLoading(false)
    }
  }

  if (isLoading || loading) {
    return (
      <main className="min-h-screen bg-[#0A0A0F] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 text-violet-400 animate-spin" />
          <p className="text-gray-400">Loading your dashboard...</p>
        </div>
      </main>
    )
  }

  if (selectedAnalysis) {
    return (
      <main className="min-h-screen bg-[#0A0A0F]">
        <div className="container mx-auto px-4 py-8">
          <button
            onClick={() => setSelectedAnalysis(null)}
            className="mb-6 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-xl transition-colors"
          >
            ← Back to Dashboard
          </button>

          <ResultsDisplay
            results={{
              career: selectedAnalysis.career_analysis,
              roi: selectedAnalysis.roi_analysis,
              fire: selectedAnalysis.fire_analysis,
              side_hustle: selectedAnalysis.side_hustle_analysis,
              interests_roadmap: selectedAnalysis.interests_roadmap,
            }}
          />
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#0A0A0F]">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/10 via-purple-600/5 to-fuchsia-600/10" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,0,255,0.05),transparent_50%)]" />

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex justify-between items-center mb-12"
        >
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Your Dashboard</h1>
              <p className="text-gray-400 text-sm">Welcome back, {user?.name || user?.email}</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/questionnaire')}
              className="px-4 py-2 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white rounded-xl font-medium transition-all shadow-lg shadow-violet-500/25"
            >
              ✨ New Analysis
            </button>
            <button
              onClick={logout}
              className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-xl transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
        >
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-blue-500/20 rounded-xl flex items-center justify-center">
                <FileText className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <div className="text-3xl font-bold text-white">{analyses.length}</div>
                <div className="text-gray-400 text-sm">Total Analyses</div>
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-emerald-500/20 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <div className="text-3xl font-bold text-white">5</div>
                <div className="text-gray-400 text-sm">Reports per Analysis</div>
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-violet-500/20 rounded-xl flex items-center justify-center">
                <Calendar className="w-5 h-5 text-violet-400" />
              </div>
              <div>
                <div className="text-3xl font-bold text-white">
                  {analyses.length > 0 ? new Date(analyses[0].created_at).toLocaleDateString() : '-'}
                </div>
                <div className="text-gray-400 text-sm">Latest Analysis</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Analyses List */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold text-white mb-6">Your Analyses</h2>

          {analyses.length === 0 ? (
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-12 text-center">
              <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No analyses yet</h3>
              <p className="text-gray-400 mb-6">Create your first AI-powered career analysis</p>
              <button
                onClick={() => router.push('/')}
                className="px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white rounded-xl font-medium hover:scale-105 transition-all"
              >
                Get Started
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {analyses.map((analysis, index) => (
                <motion.div
                  key={analysis.id}
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all cursor-pointer group"
                  onClick={() => setSelectedAnalysis(analysis)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          Career Analysis #{analyses.length - index}
                        </h3>
                        <span className="px-3 py-1 bg-emerald-500/20 border border-emerald-500/30 rounded-full text-emerald-400 text-xs font-medium">
                          Complete
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          {new Date(analysis.created_at).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          })}
                        </div>
                        <div>
                          {analysis.profile_data.name} • {analysis.profile_data.age} years old
                        </div>
                      </div>
                    </div>
                    <div className="text-violet-400 group-hover:translate-x-2 transition-transform">
                      →
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </main>
  )
}
