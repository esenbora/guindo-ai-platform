'use client'

import { useRouter } from 'next/navigation'
import QuestionnaireFlow from '@/components/QuestionnaireFlow'

export default function QuestionnairePage() {
  const router = useRouter()

  return (
    <main className="min-h-screen bg-[#0A0A0F]">
      <QuestionnaireFlow
        onComplete={(results) => {
          // Store results in sessionStorage and redirect to first analysis
          sessionStorage.setItem('analysisResults', JSON.stringify(results))
          router.push('/results/career')
        }}
      />
    </main>
  )
}
