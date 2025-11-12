'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Target, TrendingUp, Flame, Rocket, Heart, Sparkles, ChevronLeft, ChevronRight } from 'lucide-react'

interface Results {
  career: string
  roi: string
  fire: string
  side_hustle: string
  interests_roadmap: string
  timestamp?: string
}

const ANALYSES = [
  {
    id: 'career',
    title: 'Career Roadmap',
    subtitle: 'Your path to your dream job',
    icon: <Target className="w-8 h-8" />,
    gradient: 'from-blue-500 to-cyan-500',
    bgGradient: 'from-blue-500/10 to-cyan-500/10'
  },
  {
    id: 'roi',
    title: 'Education ROI',
    subtitle: 'Is a master\'s degree worth it?',
    icon: <TrendingUp className="w-8 h-8" />,
    gradient: 'from-emerald-500 to-green-500',
    bgGradient: 'from-emerald-500/10 to-green-500/10'
  },
  {
    id: 'fire',
    title: 'FIRE Plan',
    subtitle: 'Your path to financial independence',
    icon: <Flame className="w-8 h-8" />,
    gradient: 'from-orange-500 to-red-500',
    bgGradient: 'from-orange-500/10 to-red-500/10'
  },
  {
    id: 'side_hustle',
    title: 'Side Income',
    subtitle: 'Build passive income streams',
    icon: <Rocket className="w-8 h-8" />,
    gradient: 'from-purple-500 to-pink-500',
    bgGradient: 'from-purple-500/10 to-pink-500/10'
  },
  {
    id: 'interests_roadmap',
    title: 'Passion Paths',
    subtitle: 'Career paths based on your interests',
    icon: <Heart className="w-8 h-8" />,
    gradient: 'from-rose-500 to-fuchsia-500',
    bgGradient: 'from-rose-500/10 to-fuchsia-500/10'
  },
]

export default function ResultsDisplay({ results }: { results: Results }) {
  const [currentPage, setCurrentPage] = useState(0)

  const currentAnalysis = ANALYSES[currentPage]
  const currentContent = results[currentAnalysis.id as keyof Results]

  const nextPage = () => {
    if (currentPage < ANALYSES.length - 1) {
      setCurrentPage(currentPage + 1)
    }
  }

  const prevPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-[#0A0A0F] relative overflow-hidden"
    >
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/20 via-purple-600/10 to-fuchsia-600/20" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,0,255,0.1),transparent_50%)]" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8 md:py-12">
        {/* Progress indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {ANALYSES.map((analysis, index) => (
            <button
              key={analysis.id}
              onClick={() => setCurrentPage(index)}
              className={`transition-all duration-300 ${
                index === currentPage
                  ? 'w-12 h-3 bg-gradient-to-r ' + analysis.gradient
                  : 'w-3 h-3 bg-white/20 hover:bg-white/30'
              } rounded-full`}
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.3 }}
          >
            {/* Header for current analysis */}
            <div className="text-center mb-10">
              <motion.div
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className={`inline-flex items-center justify-center gap-4 mb-6 p-6 rounded-3xl bg-gradient-to-r ${currentAnalysis.bgGradient} border border-white/10`}
              >
                <div className={`text-transparent bg-clip-text bg-gradient-to-r ${currentAnalysis.gradient}`}>
                  {currentAnalysis.icon}
                </div>
                <div className="text-left">
                  <h1 className={`text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${currentAnalysis.gradient}`}>
                    {currentAnalysis.title}
                  </h1>
                  <p className="text-gray-400 text-lg mt-1">
                    {currentAnalysis.subtitle}
                  </p>
                </div>
              </motion.div>

              <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                <Sparkles className="w-4 h-4" />
                <span>Analysis {currentPage + 1} of {ANALYSES.length}</span>
              </div>
            </div>

            {/* Content Card */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.3, delay: 0.1 }}
              className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 md:p-10 mb-8"
            >
              <div className="prose prose-invert prose-lg max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-3xl md:text-4xl font-bold text-white mb-6 pb-3 border-b border-white/20">
                        {children}
                      </h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-2xl md:text-3xl font-bold text-white mt-10 mb-4 flex items-center gap-2">
                        <span className={`w-2 h-8 bg-gradient-to-b ${currentAnalysis.gradient} rounded-full`} />
                        {children}
                      </h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-xl md:text-2xl font-semibold text-gray-200 mt-6 mb-3">
                        {children}
                      </h3>
                    ),
                    h4: ({ children }) => (
                      <h4 className="text-lg md:text-xl font-semibold text-gray-300 mt-4 mb-2">
                        {children}
                      </h4>
                    ),
                    p: ({ children }) => (
                      <p className="text-gray-300 leading-relaxed mb-4">
                        {children}
                      </p>
                    ),
                    ul: ({ children }) => (
                      <ul className="space-y-2 mb-6 ml-4">
                        {children}
                      </ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="space-y-2 mb-6 ml-4 list-decimal">
                        {children}
                      </ol>
                    ),
                    li: ({ children }) => (
                      <li className="text-gray-300 leading-relaxed flex items-start gap-3">
                        <span className={`text-transparent bg-clip-text bg-gradient-to-r ${currentAnalysis.gradient} mt-1.5`}>•</span>
                        <span className="flex-1">{children}</span>
                      </li>
                    ),
                    table: ({ children }) => (
                      <div className="my-8 overflow-x-auto rounded-xl border border-white/20">
                        <table className="w-full border-collapse">
                          {children}
                        </table>
                      </div>
                    ),
                    thead: ({ children }) => (
                      <thead className={`bg-gradient-to-r ${currentAnalysis.bgGradient}`}>
                        {children}
                      </thead>
                    ),
                    tbody: ({ children }) => (
                      <tbody className="divide-y divide-white/10">
                        {children}
                      </tbody>
                    ),
                    tr: ({ children }) => (
                      <tr className="hover:bg-white/5 transition-colors">
                        {children}
                      </tr>
                    ),
                    th: ({ children }) => (
                      <th className="px-4 py-3 text-left text-sm font-semibold text-white border-r border-white/10 last:border-r-0">
                        {children}
                      </th>
                    ),
                    td: ({ children }) => (
                      <td className="px-4 py-3 text-gray-300 border-r border-white/10 last:border-r-0">
                        {children}
                      </td>
                    ),
                    blockquote: ({ children }) => (
                      <blockquote className={`border-l-4 border-l-transparent bg-gradient-to-r ${currentAnalysis.gradient} bg-clip-border pl-6 py-4 my-6 italic text-gray-300 bg-white/5`}>
                        {children}
                      </blockquote>
                    ),
                    code: ({ inline, children }) =>
                      inline ? (
                        <code className={`bg-gradient-to-r ${currentAnalysis.bgGradient} text-white px-2 py-1 rounded text-sm font-mono`}>
                          {children}
                        </code>
                      ) : (
                        <code className="block bg-black/30 text-green-300 p-4 rounded-lg overflow-x-auto text-sm font-mono my-4">
                          {children}
                        </code>
                      ),
                    strong: ({ children }) => (
                      <strong className="font-bold text-white">
                        {children}
                      </strong>
                    ),
                    em: ({ children }) => (
                      <em className="italic text-gray-200">
                        {children}
                      </em>
                    ),
                    a: ({ href, children }) => (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`text-transparent bg-clip-text bg-gradient-to-r ${currentAnalysis.gradient} hover:underline`}
                      >
                        {children}
                      </a>
                    ),
                    hr: () => (
                      <hr className={`my-8 border-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent`} />
                    ),
                  }}
                >
                  {currentContent}
                </ReactMarkdown>
              </div>
            </motion.div>

            {/* Navigation */}
            <div className="flex items-center justify-between gap-4">
              <button
                onClick={prevPage}
                disabled={currentPage === 0}
                className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                  currentPage === 0
                    ? 'bg-white/5 text-gray-600 cursor-not-allowed'
                    : 'bg-white/10 hover:bg-white/20 text-white border border-white/20'
                }`}
              >
                <ChevronLeft className="w-5 h-5" />
                Previous
              </button>

              <div className="text-center">
                <button
                  onClick={() => window.location.reload()}
                  className="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 text-gray-400 hover:text-white rounded-xl transition-all text-sm"
                >
                  Start New Analysis
                </button>
              </div>

              <button
                onClick={nextPage}
                disabled={currentPage === ANALYSES.length - 1}
                className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                  currentPage === ANALYSES.length - 1
                    ? 'bg-white/5 text-gray-600 cursor-not-allowed'
                    : `bg-gradient-to-r ${currentAnalysis.gradient} text-white hover:scale-105 shadow-lg`
                }`}
              >
                Next
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
