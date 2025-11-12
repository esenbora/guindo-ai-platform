'use client'

import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Check, Sparkles, TrendingUp, Target, Zap, Shield, Brain, ChevronRight, Code, Briefcase, Stethoscope, Palette } from 'lucide-react'

export default function Home() {
  const router = useRouter()

  return (
    <main className="min-h-screen bg-[#0A0A0F]">
      <LandingPage onGetStarted={() => router.push('/payment')} />
    </main>
  )
}

function LandingPage({ onGetStarted }: { onGetStarted: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative min-h-screen overflow-hidden"
    >
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/20 via-purple-600/10 to-fuchsia-600/20" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,0,255,0.1),transparent_50%)]" />

      {/* Grid Pattern - Removed, file doesn't exist */}

      <div className="relative z-10 container mx-auto px-4 py-20">
        {/* Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="flex justify-between items-center mb-20"
        >
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-white font-bold text-xl">Guindo</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            <span className="text-emerald-400 text-sm font-medium">AI-Powered</span>
          </div>
        </motion.div>

        {/* Hero Section */}
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-16"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-violet-500/10 border border-violet-500/20 rounded-full mb-6">
              <Zap className="w-4 h-4 text-violet-400" />
              <span className="text-violet-300 text-sm font-medium">Make Your Life-Changing Decision</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Stop Being <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-400 via-fuchsia-400 to-pink-400">Indecisive</span>
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400">
                Plan Your Future
              </span>
            </h1>

            <p className="text-xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
              AI-powered personalized career roadmap, education ROI analysis,
              FIRE retirement planning, and side income strategies — all in one place.
            </p>

            <button
              onClick={onGetStarted}
              className="group relative inline-flex items-center gap-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white px-8 py-4 rounded-2xl font-semibold text-lg hover:scale-105 transition-all shadow-[0_0_50px_rgba(139,92,246,0.3)] hover:shadow-[0_0_80px_rgba(139,92,246,0.5)]"
            >
              <span>Get Your Plan Now</span>
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>

            <p className="mt-4 text-sm text-gray-500">
              One-time payment • $9.99 • Lifetime access to your analysis
            </p>
          </motion.div>

          {/* Persona Cards */}
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="mb-12"
          >
            <h2 className="text-2xl font-bold text-white text-center mb-8">
              Tailored for Your Industry
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <PersonaCard
                icon={<Code className="w-6 h-6" />}
                title="Tech & Engineering"
                description="Career roadmap, bootcamp vs degree ROI, tech stack decisions"
                gradient="from-blue-500 to-cyan-500"
              />
              <PersonaCard
                icon={<Briefcase className="w-6 h-6" />}
                title="Business & Finance"
                description="MBA analysis, consulting paths, corporate vs startup strategies"
                gradient="from-violet-500 to-purple-500"
              />
              <PersonaCard
                icon={<Stethoscope className="w-6 h-6" />}
                title="Healthcare"
                description="Specialty selection, residency planning, private vs hospital career"
                gradient="from-emerald-500 to-green-500"
              />
              <PersonaCard
                icon={<Palette className="w-6 h-6" />}
                title="Creative & Arts"
                description="Freelance vs agency, portfolio building, monetization strategies"
                gradient="from-fuchsia-500 to-pink-500"
              />
            </div>
          </motion.div>

          {/* Universal Features */}
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20"
          >
            <FeatureCard
              icon={<Brain className="w-6 h-6" />}
              title="Smart Career Roadmap"
              description="Step-by-step path to your dream job with AI-powered guidance"
              gradient="from-blue-500 to-cyan-500"
            />
            <FeatureCard
              icon={<TrendingUp className="w-6 h-6" />}
              title="Education ROI Analysis"
              description="Master's, MBA, certifications - analyze all scenarios with real numbers"
              gradient="from-violet-500 to-purple-500"
            />
            <FeatureCard
              icon={<Target className="w-6 h-6" />}
              title="FIRE Planning"
              description="Early retirement strategy tailored to your goals and situation"
              gradient="from-fuchsia-500 to-pink-500"
            />
          </motion.div>

          {/* Social Proof */}
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-4xl font-bold text-white mb-2">1000+</div>
                <div className="text-gray-400">Plans Generated</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-white mb-2">95%</div>
                <div className="text-gray-400">Satisfaction Rate</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-white mb-2">4.2 Years</div>
                <div className="text-gray-400">Avg. Time Saved</div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}

function PaymentPage({ onSkip }: { onSkip: () => void }) {
  const { login } = useAuth()

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative min-h-screen flex items-center justify-center p-4"
    >
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-600/20 via-purple-600/10 to-fuchsia-600/20" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,0,255,0.1),transparent_50%)]" />

      <div className="relative z-10 max-w-4xl w-full">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden"
        >
          <div className="grid grid-cols-1 md:grid-cols-2">
            {/* Left Side - Plan Details */}
            <div className="p-10 border-r border-white/10">
              <div className="flex items-center gap-2 mb-8">
                <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <span className="text-white font-bold text-xl">FIRE Planner</span>
              </div>

              <h2 className="text-3xl font-bold text-white mb-4">
                Complete Career & Life Plan
              </h2>
              <p className="text-gray-400 mb-8">
                Get your personalized roadmap to success
              </p>

              <div className="space-y-4 mb-8">
                <BenefitItem text="AI-Powered Career Roadmap" />
                <BenefitItem text="Passion-Based Path Discovery" />
                <BenefitItem text="Master's Degree ROI Analysis (5+ Scenarios)" />
                <BenefitItem text="FIRE Retirement Planning" />
                <BenefitItem text="Side Income Strategies" />
                <BenefitItem text="2025 Market Data & Trends" />
                <BenefitItem text="Lifetime Access to Your Report" />
              </div>

              <div className="pt-8 border-t border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400">One-time payment</span>
                  <span className="text-3xl font-bold text-white">$9.99</span>
                </div>
                <div className="flex items-center gap-2 text-emerald-400 text-sm">
                  <Shield className="w-4 h-4" />
                  <span>Secure payment powered by Whop</span>
                </div>
              </div>
            </div>

            {/* Right Side - Payment Action */}
            <div className="p-10 bg-white/5 flex flex-col justify-center">
              <div className="mb-8 text-center">
                <h3 className="text-2xl font-semibold text-white mb-3">Get Your Plan</h3>
                <p className="text-gray-400 text-sm">
                  Secure checkout • All payment methods accepted
                </p>
              </div>

              <button
                onClick={login}
                disabled
                className="w-full px-8 py-4 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white rounded-2xl font-semibold text-lg opacity-50 cursor-not-allowed flex items-center justify-center gap-3"
              >
                <span>Continue with Whop</span>
                <ChevronRight className="w-5 h-5" />
              </button>

              <div className="mt-4 p-3 bg-orange-500/10 border border-orange-500/20 rounded-xl">
                <p className="text-orange-300 text-xs text-center">
                  ⚠️ Whop integration disabled - API keys not configured yet
                </p>
              </div>

              <div className="mt-6">
                <button
                  onClick={onSkip}
                  className="w-full px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-xl font-medium transition-colors"
                >
                  Demo Mode: Skip Payment (Testing Only)
                </button>
              </div>

              <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                <p className="text-blue-300 text-sm text-center">
                  💡 After payment, you'll immediately access the questionnaire. Your personalized plan will be generated in real-time using the latest 2025 market data.
                </p>
              </div>

              <div className="mt-4 text-center">
                <p className="text-gray-500 text-xs">
                  By continuing, you agree to our Terms of Service and Privacy Policy
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}

function PersonaCard({ icon, title, description, gradient }: {
  icon: React.ReactNode,
  title: string,
  description: string,
  gradient: string
}) {
  return (
    <div className="group p-6 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl hover:bg-white/10 transition-all hover:scale-105">
      <div className={`w-12 h-12 bg-gradient-to-br ${gradient} rounded-xl flex items-center justify-center mb-4 text-white group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="font-semibold text-white text-base mb-2">{title}</h3>
      <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
    </div>
  )
}

function FeatureCard({ icon, title, description, gradient }: {
  icon: React.ReactNode,
  title: string,
  description: string,
  gradient: string
}) {
  return (
    <div className="group p-6 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl hover:bg-white/10 transition-all hover:scale-105">
      <div className={`w-14 h-14 bg-gradient-to-br ${gradient} rounded-2xl flex items-center justify-center mb-4 text-white group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="font-semibold text-white text-lg mb-2">{title}</h3>
      <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
    </div>
  )
}

function BenefitItem({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-3">
      <div className="w-5 h-5 bg-emerald-500/20 border border-emerald-500/30 rounded-full flex items-center justify-center flex-shrink-0">
        <Check className="w-3 h-3 text-emerald-400" />
      </div>
      <span className="text-gray-300 text-sm">{text}</span>
    </div>
  )
}
