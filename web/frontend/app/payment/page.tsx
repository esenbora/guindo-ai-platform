'use client'

import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Check, Sparkles, Shield, ChevronRight } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

export default function PaymentPage() {
  const router = useRouter()
  const { login } = useAuth()

  const handleCheckout = () => {
    // Redirect to Whop OAuth + Checkout flow
    const clientId = process.env.NEXT_PUBLIC_WHOP_CLIENT_ID
    const redirectUri = `${process.env.NEXT_PUBLIC_APP_URL || window.location.origin}/api/auth/whop/callback`
    const planId = process.env.NEXT_PUBLIC_WHOP_PLAN_ID || 'plan_vOJtGvp39ut5y'

    // OAuth flow with checkout parameter
    const checkoutUrl =
      `https://whop.com/oauth/authorize?` +
      `client_id=${clientId}` +
      `&redirect_uri=${encodeURIComponent(redirectUri)}` +
      `&response_type=code` +
      `&checkout=${planId}`

    window.location.href = checkoutUrl
  }

  return (
    <main className="min-h-screen bg-[#0A0A0F]">
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
                  <span className="text-white font-bold text-xl">Guindo</span>
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
                  <BenefitItem text="Education Investment Analysis (5+ Scenarios)" />
                  <BenefitItem text="FIRE Retirement Planning" />
                  <BenefitItem text="Side Income Strategies" />
                  <BenefitItem text="Industry-Specific Insights & Trends" />
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
                  onClick={handleCheckout}
                  className="w-full px-8 py-4 bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white rounded-2xl font-semibold text-lg transition-all flex items-center justify-center gap-3 shadow-lg shadow-violet-500/25"
                >
                  <span>Continue with Whop</span>
                  <ChevronRight className="w-5 h-5" />
                </button>

                <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                  <p className="text-emerald-300 text-xs text-center">
                    ✅ Secure checkout powered by Whop
                  </p>
                </div>

                <div className="mt-6">
                  <button
                    onClick={() => router.push('/questionnaire')}
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
    </main>
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
