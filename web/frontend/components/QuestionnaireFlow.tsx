'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, ChevronRight, Loader2, User, Briefcase, Code, GraduationCap, Target, DollarSign, Flame, Rocket, Brain, Clock, Sparkles, Heart } from 'lucide-react'
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
  conditionalQuestions?: {
    working?: Question[]
    interested?: Question[]
  }
}

const SECTIONS: Section[] = [
  {
    id: 'basic',
    title: 'About You',
    emoji: <User className="w-6 h-6" />,
    description: 'Let\'s get to know you! Just a few basic questions.',
    questions: [
      { id: 'name', label: 'What\'s your name?', type: 'text', placeholder: 'John' },
      { id: 'age', label: 'How old are you?', type: 'number', placeholder: '24' },
      { id: 'university', label: 'Which university did/do you attend?', type: 'text', placeholder: 'MIT, Stanford...' },
      { id: 'major', label: 'What is/was your major?', type: 'text', placeholder: 'Computer Science, Business Admin, Medicine, Law, Design, Engineering...' },
      { id: 'grad_year', label: 'When did/will you graduate?', type: 'text', placeholder: '2024, June 2025...' },
      { id: 'location', label: 'Where are you currently living?', type: 'text', placeholder: 'Istanbul, Turkey' },
      { id: 'relocation_ok', label: 'Would you be open to relocating abroad?', type: 'select', options: ['yes', 'no', 'maybe'] },
    ],
  },
  {
    id: 'current',
    title: 'Current Situation',
    emoji: <Briefcase className="w-6 h-6" />,
    description: 'Tell us about your current work situation.',
    questions: [
      { id: 'current_job', label: 'What are you currently doing?', type: 'text', placeholder: 'Data Analyst / Student / Unemployed / Doctor / Designer...' },
      {
        id: 'primary_industry',
        label: 'Which industry best describes your career focus?',
        type: 'select',
        options: ['Technology & Engineering', 'Business & Finance', 'Healthcare & Medicine', 'Creative & Design', 'Education', 'Legal', 'Other'],
        description: 'This helps us personalize your career roadmap'
      },
    ],
    conditionalQuestions: {
      working: [
        { id: 'current_salary', label: 'What\'s your current salary? (USD/year)', type: 'text', placeholder: '30000' },
        { id: 'job_satisfaction', label: 'How satisfied are you with your current job?', type: 'select', options: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] },
        { id: 'years_current_job', label: 'How long have you been in this job?', type: 'text', placeholder: '2 years' },
        { id: 'industry', label: 'What specific industry/sector are you in?', type: 'text', placeholder: 'Software, Investment Banking, Surgery, UX Design, Consulting...' },
        { id: 'company_size', label: 'Company size?', type: 'select', options: ['startup', 'medium', 'large'] },
      ]
    }
  },
  {
    id: 'skills',
    title: 'Skills & Experience',
    emoji: <Code className="w-6 h-6" />,
    description: 'Optional: Share your professional skills to get more tailored recommendations.',
    questions: [
      {
        id: 'share_skills',
        label: 'Would you like to share your professional skills?',
        type: 'select',
        options: ['yes', 'no', 'skip this section'],
        description: 'This is optional but helps us give better career advice'
      },
    ],
    conditionalQuestions: {
      interested: [
        {
          id: 'key_skills',
          label: 'What are your key professional skills?',
          type: 'text',
          placeholder: 'Python, Excel, Surgery, Design Tools, Public Speaking, Financial Analysis...',
          description: 'List your most relevant skills for your career goals'
        },
        {
          id: 'skill_level',
          label: 'Overall, how would you rate your skill level?',
          type: 'select',
          options: ['beginner', 'intermediate', 'advanced', 'expert']
        },
        {
          id: 'tools_platforms',
          label: 'Any specific tools or platforms you use?',
          type: 'text',
          placeholder: 'Figma, SAP, AWS, Salesforce, Adobe Suite, AutoCAD...',
          description: 'Industry-specific tools you\'re proficient with'
        },
        {
          id: 'certifications',
          label: 'Any certifications, licenses, or completed courses?',
          type: 'text',
          placeholder: 'CPA, AWS Certified, Medical License, PMP, Design Bootcamp...'
        },
        {
          id: 'portfolio_work',
          label: 'Do you have a portfolio, published work, or notable projects?',
          type: 'text',
          placeholder: 'GitHub projects, Design portfolio, Published papers, Case studies...'
        },
      ]
    }
  },
  {
    id: 'education',
    title: 'Education & Master\'s Decision',
    emoji: <GraduationCap className="w-6 h-6" />,
    description: 'Unsure about doing a master\'s? We\'ll help you decide.',
    questions: [
      {
        id: 'considering_masters',
        label: 'Are you considering a master\'s degree?',
        type: 'select',
        options: ['definitely doing it', 'yes but undecided', 'maybe', 'no', 'never thought about it'],
        description: 'Be honest - if you\'re undecided, we\'ll help!'
      },
    ],
    conditionalQuestions: {
      interested: [
        {
          id: 'masters_fields_interested',
          label: 'What fields are you interested in? (comma-separated)',
          type: 'text',
          placeholder: 'MBA, Data Science, Medicine, Law, Design, Engineering, Public Health...',
          description: 'List all fields you\'re considering'
        },
        {
          id: 'masters_location_preference',
          label: 'Where would you like to do your master\'s?',
          type: 'select',
          options: ['Turkey', 'Europe', 'USA', 'Canada', 'UK', 'Online/Remote', 'Doesn\'t matter', 'Undecided']
        },
        {
          id: 'masters_program_language',
          label: 'Preferred program language?',
          type: 'select',
          options: ['English', 'Turkish', 'Doesn\'t matter']
        },
        {
          id: 'masters_type',
          label: 'What type of master\'s are you considering?',
          type: 'select',
          options: ['Thesis (research)', 'Non-thesis (coursework)', 'Professional', 'Undecided', 'Doesn\'t matter']
        },
        {
          id: 'can_afford_masters',
          label: 'Can you afford a master\'s program?',
          type: 'select',
          options: ['yes, fully', 'partially, need scholarship', 'no, need full scholarship', 'undecided/need to know costs']
        },
        {
          id: 'masters_timeline',
          label: 'When are you planning to start?',
          type: 'select',
          options: ['this year', 'next year', '2+ years', 'flexible', 'undecided']
        },
        {
          id: 'masters_work_while_study',
          label: 'Do you plan to work while studying?',
          type: 'select',
          options: ['yes, full-time', 'yes, part-time', 'no, full-time student', 'undecided']
        },
        {
          id: 'masters_priority',
          label: 'What\'s your top priority for a master\'s?',
          type: 'select',
          options: ['career boost', 'salary increase', 'knowledge/skills', 'research', 'networking', 'prestige', 'visa/immigration']
        },
        {
          id: 'masters_specific_programs',
          label: 'Any specific programs you\'re considering?',
          type: 'text',
          placeholder: 'Stanford MS CS, ETH Zurich DS, MIT EECS...',
          description: 'List any programs you\'ve already researched'
        },
        {
          id: 'masters_concerns',
          label: 'What are your main concerns about doing a master\'s?',
          type: 'text',
          placeholder: 'Cost, time, career gap, ROI, opportunity cost...',
          description: 'Be specific - we\'ll address each concern'
        },
      ]
    }
  },
  {
    id: 'goals',
    title: 'Career Goals',
    emoji: <Target className="w-6 h-6" />,
    description: 'Where do you see yourself in the future?',
    questions: [
      { id: 'dream_job', label: 'What\'s your dream job or role?', type: 'text', placeholder: 'Senior Consultant, Surgeon, Creative Director, Data Scientist, Partner at Law Firm...' },
      { id: 'dream_salary', label: 'What\'s your target salary? (USD/year)', type: 'text', placeholder: '150000' },
      { id: 'target_years', label: 'In how many years do you want to achieve this?', type: 'text', placeholder: '3-5 years' },
      { id: 'career_path_preference', label: 'Which career path interests you most?', type: 'select', options: ['big tech', 'consulting', 'healthcare', 'creative agency', 'startup', 'freelance', 'entrepreneur', 'academia', 'legal firm', 'don\'t know yet'] },
      { id: 'willing_to_study', label: 'Are you willing to invest time/money in education?', type: 'select', options: ['yes, definitely', 'maybe', 'probably not'] },
    ],
  },
  {
    id: 'finances',
    title: 'Financial Situation',
    emoji: <DollarSign className="w-6 h-6" />,
    description: 'Help us understand your financial situation and goals.',
    questions: [
      { id: 'monthly_expenses', label: 'What are your monthly expenses? (USD)', type: 'text', placeholder: '1500' },
      { id: 'savings', label: 'How much do you currently have in savings? (USD)', type: 'text', placeholder: '10000, or 0 if none' },
      { id: 'monthly_savings_goal', label: 'How much would you like to save each month?', type: 'text', placeholder: '500' },
      { id: 'debts', label: 'Do you have any student loans or debts?', type: 'text', placeholder: '0, 5000, none...' },
      { id: 'family_support', label: 'Do you receive financial support from family?', type: 'select', options: ['yes', 'partial', 'no'] },
      { id: 'risk_tolerance', label: 'How comfortable are you with investment risks?', type: 'select', options: ['conservative (low risk)', 'moderate', 'aggressive (high risk)'] },
    ],
  },
  {
    id: 'fire',
    title: 'FIRE Goals',
    emoji: <Flame className="w-6 h-6" />,
    description: 'Let\'s talk about your retirement and financial independence goals.',
    questions: [
      { id: 'retire_age', label: 'At what age would you like to retire?', type: 'text', placeholder: '45, 50, 65...' },
      { id: 'fire_lifestyle', label: 'What kind of retirement lifestyle do you envision?', type: 'select', options: ['lean FIRE (minimal expenses)', 'regular FIRE (comfortable)', 'fat FIRE (luxurious)'] },
      { id: 'retirement_location', label: 'Where would you like to retire?', type: 'text', placeholder: 'Bali, Portugal, same city...' },
      { id: 'passive_income_interest', label: 'How interested are you in building passive income?', type: 'select', options: ['very interested', 'somewhat interested', 'not really interested'] },
    ],
  },
  {
    id: 'side',
    title: 'Side Income Ideas',
    emoji: <Rocket className="w-6 h-6" />,
    description: 'Let\'s explore ways you could increase your income.',
    questions: [
      { id: 'time_for_side', label: 'How many hours per week could you dedicate to side projects?', type: 'text', placeholder: '5-10 hours' },
      { id: 'side_interests', label: 'What topics or activities are you passionate about?', type: 'text', placeholder: 'teaching, writing, coding, design...' },
      { id: 'freelance_exp', label: 'Have you done any freelance work before?', type: 'select', options: ['yes, currently doing it', 'tried it before', 'never tried it', 'want to start'] },
      { id: 'preferred_side_income', label: 'What type of side income interests you most?', type: 'select', options: ['freelancing', 'content creation', 'building products/SaaS', 'teaching/courses', 'consulting', 'investments', 'open to anything'] },
      { id: 'monthly_side_income_goal', label: 'What\'s your monthly side income goal? (USD)', type: 'text', placeholder: '500, 1000, 2000...' },
    ],
  },
  {
    id: 'constraints',
    title: 'Constraints & Preferences',
    emoji: <Clock className="w-6 h-6" />,
    description: 'Help us understand your situation and what works best for you.',
    questions: [
      { id: 'time_commit', label: 'How many hours per week can you dedicate to career development?', type: 'text', placeholder: '10-15 hours' },
      { id: 'learning_style', label: 'How do you learn best?', type: 'select', options: ['hands-on projects', 'structured courses', 'reading/self-study', 'bootcamps', 'mentorship'] },
      { id: 'work_life_balance', label: 'How important is work-life balance to you?', type: 'select', options: ['very important', 'somewhat important', 'not a priority right now'] },
      { id: 'biggest_obstacle', label: 'What\'s your biggest challenge or obstacle right now?', type: 'text', placeholder: 'lack of time, money, skills, direction...' },
      { id: 'need_most', label: 'What would help you most right now?', type: 'select', options: ['clear roadmap', 'skill development plan', 'financial strategy', 'help making decisions', 'all of the above'] },
    ],
  },
  {
    id: 'interests',
    title: 'Interests & Passions',
    emoji: <Heart className="w-6 h-6" />,
    description: 'What truly excites you? Let\'s explore career paths aligned with your passions!',
    questions: [
      {
        id: 'passion_topics',
        label: 'What topics or fields genuinely excite you?',
        type: 'text',
        placeholder: 'AI/ML, blockchain, game dev, UI/UX design, climate tech, fintech, biotech...',
        description: 'Think beyond your current skills - what would you love to work on?'
      },
      {
        id: 'flow_activities',
        label: 'What kind of work makes you lose track of time?',
        type: 'text',
        placeholder: 'building apps, analyzing data, teaching, designing, solving puzzles...',
        description: 'When do you enter a "flow state"?'
      },
      {
        id: 'dream_projects',
        label: 'If you had 6 months and no restrictions, what would you build or work on?',
        type: 'text',
        placeholder: 'an AI app, a game, a startup, write a book, contribute to open source...',
        description: 'Dream big - what passion project comes to mind?'
      },
      {
        id: 'role_models',
        label: 'Any people, companies, or projects that inspire you?',
        type: 'text',
        placeholder: 'OpenAI, indie hackers, Figma, specific YouTube creators, researchers...',
        description: 'Who or what do you look up to professionally?'
      },
    ],
  },
]

export default function QuestionnaireFlow({ onComplete }: { onComplete: (results: any) => void }) {
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)

  const currentSection = SECTIONS[currentSectionIndex]
  const progress = ((currentSectionIndex + 1) / SECTIONS.length) * 100

  // Calculate current questions based on conditional logic
  const getCurrentQuestions = () => {
    let questions = [...currentSection.questions]

    // Check if user is working (for job details)
    if (currentSection.id === 'current' && currentSection.conditionalQuestions) {
      const currentJob = answers['current_job']?.toLowerCase() || ''
      const isWorking = currentJob &&
        !currentJob.includes('student') &&
        !currentJob.includes('unemployed') &&
        !currentJob.includes('none') &&
        !currentJob.includes('no')

      if (isWorking && currentSection.conditionalQuestions.working) {
        questions = [...questions, ...currentSection.conditionalQuestions.working]
      }
    }

    // Check if user is interested in master's (for master details)
    if (currentSection.id === 'education' && currentSection.conditionalQuestions) {
      const masterInterest = answers['considering_masters']?.toLowerCase() || ''
      const isInterested = masterInterest &&
        masterInterest !== 'no' &&
        masterInterest !== 'never thought about it'

      if (isInterested && currentSection.conditionalQuestions.interested) {
        questions = [...questions, ...currentSection.conditionalQuestions.interested]
      }
    }

    return questions
  }

  const currentQuestions = getCurrentQuestions()

  const handleNext = () => {
    if (currentSectionIndex < SECTIONS.length - 1) {
      setCurrentSectionIndex(currentSectionIndex + 1)
    } else {
      handleSubmit()
    }
  }

  const handleBack = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(currentSectionIndex - 1)
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      // Add defaults for skipped questions
      const finalAnswers = { ...answers }

      // If not working, set default values
      const currentJob = answers['current_job']?.toLowerCase() || ''
      const isWorking = currentJob &&
        !currentJob.includes('student') &&
        !currentJob.includes('unemployed') &&
        !currentJob.includes('none')

      if (!isWorking) {
        finalAnswers['current_salary'] = '0'
        finalAnswers['job_satisfaction'] = '0'
        finalAnswers['years_current_job'] = '0'
        finalAnswers['industry'] = 'none'
        finalAnswers['company_size'] = 'none'
      }

      // If not interested in master's, set defaults
      const masterInterest = answers['considering_masters']?.toLowerCase() || ''
      const isInterested = masterInterest &&
        masterInterest !== 'no' &&
        masterInterest !== 'never thought about it'

      if (!isInterested) {
        finalAnswers['masters_fields_interested'] = ''
        finalAnswers['masters_location_preference'] = ''
        finalAnswers['masters_program_language'] = ''
        finalAnswers['masters_type'] = ''
        finalAnswers['can_afford_masters'] = ''
        finalAnswers['masters_timeline'] = ''
        finalAnswers['masters_work_while_study'] = ''
        finalAnswers['masters_priority'] = ''
        finalAnswers['masters_specific_programs'] = ''
        finalAnswers['masters_concerns'] = ''
      }

      // Generate AI analyses
      const response = await axios.post(
        `${API_URL}/api/analyze-all`,
        finalAnswers,
        {
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': process.env.NEXT_PUBLIC_API_SECRET || '',
          },
        }
      )
      const analysisResults = response.data

      // Save analyses to database
      try {
        await fetch('/api/analyses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            profileData: finalAnswers,
            career: analysisResults.career,
            roi: analysisResults.roi,
            fire: analysisResults.fire,
            side_hustle: analysisResults.side_hustle,
            interests_roadmap: analysisResults.interests_roadmap,
          }),
        })
      } catch (saveError) {
        console.error('Error saving to database:', saveError)
        // Don't block user from seeing results if save fails
      }

      onComplete(analysisResults)
    } catch (error) {
      console.error('Error submitting:', error)
      alert('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const isCurrentSectionComplete = currentQuestions.every(q => answers[q.id])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen relative overflow-hidden"
    >
      {/* Premium Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/20 via-purple-600/10 to-fuchsia-600/20" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,0,255,0.1),transparent_50%)]" />

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header with Progress */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-white font-bold">Guindo</span>
            </div>
            <div className="text-sm text-gray-400">
              Step {currentSectionIndex + 1} of {SECTIONS.length}
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Question Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSectionIndex}
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -20, opacity: 0 }}
            className="max-w-4xl mx-auto"
          >
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 md:p-12">
              {/* Section Header */}
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-2xl flex items-center justify-center text-white">
                  {currentSection.emoji}
                </div>
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-white">{currentSection.title}</h2>
                  <p className="text-gray-400">{currentSection.description}</p>
                </div>
              </div>

              {/* Questions */}
              <div className="space-y-6 mb-8">
                {currentQuestions.map((question, index) => (
                  <div key={question.id} className="space-y-2">
                    <label className="block text-white font-medium">
                      {index + 1}. {question.label}
                    </label>
                    {question.description && (
                      <p className="text-sm text-gray-400">{question.description}</p>
                    )}
                    {question.type === 'select' ? (
                      <select
                        value={answers[question.id] || ''}
                        onChange={(e) => setAnswers({ ...answers, [question.id]: e.target.value })}
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                      >
                        <option value="" className="bg-gray-900">Select an option</option>
                        {question.options?.map((option) => (
                          <option key={option} value={option} className="bg-gray-900">{option}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={question.type}
                        value={answers[question.id] || ''}
                        onChange={(e) => setAnswers({ ...answers, [question.id]: e.target.value })}
                        placeholder={question.placeholder}
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                      />
                    )}
                  </div>
                ))}
              </div>

              {/* Navigation Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={handleBack}
                  disabled={currentSectionIndex === 0}
                  className="flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-medium transition-colors"
                >
                  <ChevronLeft className="w-5 h-5" />
                  Back
                </button>
                <button
                  onClick={handleNext}
                  disabled={!isCurrentSectionComplete || loading}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Generating your plan...
                    </>
                  ) : currentSectionIndex === SECTIONS.length - 1 ? (
                    <>
                      <Brain className="w-5 h-5" />
                      Generate My Plan
                    </>
                  ) : (
                    <>
                      Next
                      <ChevronRight className="w-5 h-5" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
