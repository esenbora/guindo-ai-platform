'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, ChevronRight, Loader2, User, Briefcase, Code, GraduationCap, Target, DollarSign, Flame, Rocket, Brain, Clock } from 'lucide-react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Question {
  id: string
  label: string
  type: 'text' | 'number' | 'select'
  options?: string[]
  placeholder?: string
  description?: string
}

interface Section {
  id: string
  title: string
  emoji: React.ReactNode
  description: string
  questions: Question[]
}

const SECTIONS: Section[] = [
  {
    id: 'basic',
    title: 'Let\'s Get Acquainted',
    emoji: <User className="w-6 h-6" />,
    description: 'We want to get to know you! Just a few basic questions.',
    questions: [
      { id: 'name', label: 'What\'s your name?', type: 'text', placeholder: 'John' },
      { id: 'age', label: 'How old are you?', type: 'number', placeholder: '24' },
      { id: 'university', label: 'Which university do/did you attend?', type: 'text', placeholder: 'MIT, Stanford...' },
      { id: 'major', label: 'What is/was your major?', type: 'text', placeholder: 'Statistics' },
      { id: 'grad_year', label: 'When did/will you graduate?', type: 'text', placeholder: '2024' },
      { id: 'location', label: 'Where do you currently live?', type: 'text', placeholder: 'Istanbul, Turkey' },
      { id: 'relocation_ok', label: 'Open to relocating abroad?', type: 'select', options: ['yes', 'no', 'maybe'] },
    ],
  },
  {
    id: 'current',
    title: 'Current Situation',
    emoji: <Briefcase className="w-6 h-6" />,
    description: 'Let\'s talk about your job situation and satisfaction.',
    questions: [
      { id: 'current_job', label: 'What do you do currently?', type: 'text', placeholder: 'Data Analyst / Student' },
      { id: 'current_salary', label: 'Your net salary? (USD, approximate)', type: 'text', placeholder: '30000' },
      { id: 'job_satisfaction', label: 'How satisfied are you with your job?', type: 'select', options: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] },
      { id: 'years_current_job', label: 'How many years at this job?', type: 'text', placeholder: '2' },
      { id: 'industry', label: 'Which industry are you in?', type: 'text', placeholder: 'tech, finance, education...' },
      { id: 'company_size', label: 'Company size?', type: 'select', options: ['startup', 'medium', 'large'] },
    ],
  },
  {
    id: 'skills',
    title: 'Skills',
    emoji: <Code className="w-6 h-6" />,
    description: 'Let\'s learn about your technical skills and experience.',
    questions: [
      { id: 'programming_langs', label: 'Programming languages?', type: 'text', placeholder: 'Python, R, SQL...' },
      { id: 'prog_level', label: 'Programming level?', type: 'select', options: ['beginner', 'intermediate', 'advanced'] },
      { id: 'ml_exp', label: 'ML/AI experience (years)?', type: 'text', placeholder: '1' },
      { id: 'frameworks', label: 'Framework knowledge?', type: 'text', placeholder: 'TensorFlow, PyTorch...' },
      { id: 'cloud_exp', label: 'Cloud experience?', type: 'text', placeholder: 'AWS, Azure, GCP...' },
      { id: 'data_tools', label: 'Data tools?', type: 'text', placeholder: 'Tableau, PowerBI...' },
      { id: 'github_projects', label: 'How many GitHub projects?', type: 'text', placeholder: '5' },
      { id: 'certifications', label: 'Your certifications?', type: 'text', placeholder: 'AWS, Coursera...' },
    ],
  },
  {
    id: 'education',
    title: 'Education Plans',
    emoji: <GraduationCap className="w-6 h-6" />,
    description: 'Considering a Master\'s? Undecided?',
    questions: [
      { id: 'considering_masters', label: 'Considering a Master\'s?', type: 'select', options: ['yes', 'no', 'undecided'] },
      { id: 'masters_field', label: 'In which field?', type: 'text', placeholder: 'Data Science, CS...' },
      { id: 'masters_location', label: 'Where will you do it?', type: 'select', options: ['Turkey', 'Abroad', 'Online', 'undecided'] },
      { id: 'can_afford_masters', label: 'Can you afford it financially?', type: 'select', options: ['yes', 'no', 'partially'] },
      { id: 'masters_timeline', label: 'When will you start?', type: 'select', options: ['this year', 'next year', '2+ years', 'don\'t know'] },
    ],
  },
  {
    id: 'career',
    title: 'Career Goals',
    emoji: <Target className="w-6 h-6" />,
    description: 'What do you really want? What are your goals?',
    questions: [
      { id: 'dream_job', label: 'Ideal position? (5 years from now)', type: 'text', placeholder: 'Senior Data Scientist' },
      { id: 'alternative_jobs', label: 'Alternative positions?', type: 'text', placeholder: 'ML Engineer, Data Engineer...' },
      { id: 'target_salary', label: 'Target salary (USD, 5 years)?', type: 'text', placeholder: '100000' },
      { id: 'salary_vs_passion', label: 'Salary or passion?', type: 'select', options: ['salary', 'passion', 'both'] },
      { id: 'work_life_balance', label: 'How important is work-life balance?', type: 'select', options: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] },
      { id: 'career_speed', label: 'How fast do you want to advance?', type: 'select', options: ['slow', 'medium', 'fast'] },
    ],
  },
  {
    id: 'financial',
    title: 'Financial Situation',
    emoji: <DollarSign className="w-6 h-6" />,
    description: 'Let\'s be open - let\'s talk about money.',
    questions: [
      { id: 'monthly_expenses', label: 'Your monthly expenses? (USD)', type: 'text', placeholder: '1000' },
      { id: 'savings', label: 'Your current savings? (USD)', type: 'text', placeholder: '5000' },
      { id: 'debt', label: 'Do you have debt? How much?', type: 'text', placeholder: '0' },
      { id: 'family_support', label: 'Financial support from family?', type: 'select', options: ['yes', 'no', 'sometimes'] },
      { id: 'dependents', label: 'Anyone you need to support?', type: 'select', options: ['yes', 'no'] },
      { id: 'risk_tolerance', label: 'Your risk tolerance?', type: 'select', options: ['low', 'medium', 'high'] },
    ],
  },
  {
    id: 'fire',
    title: 'FIRE Vision',
    emoji: <Flame className="w-6 h-6" />,
    description: 'Do you have an early retirement goal? What kind of life do you dream of?',
    questions: [
      { id: 'retire_age', label: 'At what age do you want to retire?', type: 'number', placeholder: '40' },
      { id: 'why_fire', label: 'Why do you want to retire early?', type: 'text', placeholder: 'freedom, travel...' },
      { id: 'target_portfolio', label: 'Target savings? (USD)', type: 'text', placeholder: '600000' },
      { id: 'retirement_lifestyle', label: 'How do you want to live in retirement?', type: 'select', options: ['modest', 'moderate', 'luxury'] },
      { id: 'retirement_location', label: 'Where do you want to retire?', type: 'text', placeholder: 'Turkey, Portugal...' },
      { id: 'passive_income_goal', label: 'Monthly target passive income? (USD)', type: 'text', placeholder: '2000' },
    ],
  },
  {
    id: 'side_hustle',
    title: 'Side Income & Entrepreneurship',
    emoji: <Rocket className="w-6 h-6" />,
    description: 'Side job, freelance, startup... Are you interested?',
    questions: [
      { id: 'side_hustle_interest', label: 'Want to do a side job?', type: 'select', options: ['yes', 'no', 'maybe'] },
      { id: 'interests', label: 'Your areas of interest?', type: 'text', placeholder: 'SaaS, Course, Freelance...' },
      { id: 'weekly_hours', label: 'How many hours per week can you dedicate?', type: 'text', placeholder: '10' },
      { id: 'entrepreneurial', label: 'Do you have an entrepreneurial spirit? (1-10)', type: 'select', options: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] },
      { id: 'startup_idea', label: 'Do you have a startup idea in mind?', type: 'text', placeholder: 'Write if yes, \'none\' if no' },
      { id: 'freelance_exp', label: 'Do you have freelance experience?', type: 'select', options: ['yes', 'no'] },
    ],
  },
  {
    id: 'personality',
    title: 'Personality & Style',
    emoji: <Brain className="w-6 h-6" />,
    description: 'Let\'s get to know you better. What kind of person are you?',
    questions: [
      { id: 'learning_style', label: 'How do you learn?', type: 'select', options: ['reading', 'doing', 'watching'] },
      { id: 'team_vs_solo', label: 'Team or solo work?', type: 'select', options: ['team', 'solo', 'both'] },
      { id: 'introvert_extrovert', label: 'Introvert or extrovert?', type: 'select', options: ['introvert', 'extrovert', 'ambivert'] },
      { id: 'decision_making', label: 'Do you have difficulty making decisions?', type: 'select', options: ['yes', 'no', 'sometimes'] },
      { id: 'biggest_fear', label: 'Your biggest career-related fear?', type: 'text', placeholder: 'Making the wrong choice...' },
    ],
  },
  {
    id: 'time',
    title: 'Time & Urgency',
    emoji: <Clock className="w-6 h-6" />,
    description: 'How much time do you have? How urgently do you want change?',
    questions: [
      { id: 'time_urgency', label: 'How urgently do you want change?', type: 'select', options: ['immediately', '6 months', '1 year', 'not urgent'] },
      { id: 'daily_learning_hours', label: 'How many hours per day can you dedicate to learning?', type: 'text', placeholder: '2' },
    ],
  },
]

export default function QuestionnaireFlow({ onComplete }: {
  onComplete: (results: any) => void
}) {
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)

  const currentSection = SECTIONS[currentSectionIndex]
  const progress = ((currentSectionIndex + 1) / SECTIONS.length) * 100

  const handleAnswer = (questionId: string, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }))
  }

  const canGoNext = () => {
    return currentSection.questions.every(q => answers[q.id] && answers[q.id].trim())
  }

  const handleNext = async () => {
    if (currentSectionIndex < SECTIONS.length - 1) {
      setCurrentSectionIndex(prev => prev + 1)
    } else {
      // Last section - submit
      await handleSubmit()
    }
  }

  const handleBack = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(prev => prev - 1)
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/api/analyze-all`, answers)
      onComplete(response.data)
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex items-center justify-center p-4"
    >
      <div className="w-full max-w-3xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-400 mb-2">
            <span>Step {currentSectionIndex + 1} / {SECTIONS.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              className="h-full bg-gradient-to-r from-fire-orange to-fire-red"
            />
          </div>
        </div>

        {/* Section Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSection.id}
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -20, opacity: 0 }}
            className="bg-white/5 backdrop-blur-lg rounded-3xl border border-white/10 p-8"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-fire-orange to-fire-red rounded-xl flex items-center justify-center text-white">
                {currentSection.emoji}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{currentSection.title}</h2>
                <p className="text-gray-400">{currentSection.description}</p>
              </div>
            </div>

            <div className="space-y-6">
              {currentSection.questions.map((question, idx) => (
                <motion.div
                  key={question.id}
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: idx * 0.05 }}
                >
                  <label className="block text-white font-medium mb-2">
                    {question.label}
                  </label>
                  {question.description && (
                    <p className="text-sm text-gray-400 mb-2">{question.description}</p>
                  )}
                  {question.type === 'select' ? (
                    <select
                      value={answers[question.id] || ''}
                      onChange={(e) => handleAnswer(question.id, e.target.value)}
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-fire-orange"
                    >
                      <option value="">Select...</option>
                      {question.options?.map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={question.type}
                      value={answers[question.id] || ''}
                      onChange={(e) => handleAnswer(question.id, e.target.value)}
                      placeholder={question.placeholder}
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-fire-orange"
                    />
                  )}
                </motion.div>
              ))}
            </div>

            {/* Navigation */}
            <div className="flex justify-between mt-8 pt-6 border-t border-white/10">
              <button
                onClick={handleBack}
                disabled={currentSectionIndex === 0}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-white/5 text-white hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
                Back
              </button>

              <button
                onClick={handleNext}
                disabled={!canGoNext() || loading}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-fire-orange to-fire-red text-white hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed transition-transform"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing...
                  </>
                ) : currentSectionIndex === SECTIONS.length - 1 ? (
                  <>
                    See Analysis
                    <Rocket className="w-5 h-5" />
                  </>
                ) : (
                  <>
                    Next
                    <ChevronRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
