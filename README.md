# 🚀 Guindo - AI-Powered Career & Life Planning Platform

**Domain**: [guindo.me](https://guindo.me)

Guindo is an AI-powered SaaS platform that provides personalized career roadmaps, education ROI analysis, FIRE retirement planning, and side income strategies. Using GPT-4 and multi-agent AI orchestration, Guindo helps users make data-driven life decisions.

---

## ✨ Features

### 🎯 **5 AI-Powered Analysis Modules**

1. **Career Roadmap** - Step-by-step path to your dream job
2. **Education ROI** - Master's degree vs alternatives (5+ scenarios)
3. **FIRE Planning** - Early retirement strategy & timeline
4. **Side Income** - Passive income opportunities
5. **Passion Paths** - Turn hobbies into careers

### 🤖 **AI Technology**
- **GPT-4 Turbo** powered analysis
- **Multi-agent system** (5 agents working in parallel)
- **2025 market data** integration
- **CrewAI** orchestration

### 💎 **User Experience**
- Dark mode UI with smooth animations
- URL-based navigation for each analysis
- Professional markdown reports with tables
- Mobile-responsive design
- One-time payment: $9.99

---

## 🏗️ Project Structure

```
crewai_orchestration/
├── web/
│   ├── frontend/          # Next.js 14 (TypeScript)
│   │   ├── app/
│   │   │   ├── page.tsx                    # Landing page
│   │   │   ├── payment/page.tsx            # Payment page
│   │   │   ├── questionnaire/page.tsx      # Form
│   │   │   └── results/[type]/page.tsx     # Dynamic results
│   │   ├── components/
│   │   └── .env.local
│   │
│   └── backend/           # FastAPI (Python)
│       ├── main.py
│       ├── crew.py        # AI agents
│       └── .env
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API Key
- Serper API Key (optional)

### 1️⃣ **Backend Setup**

```bash
cd web/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
EOL

# Run backend
python main.py
# Backend runs on: http://localhost:8000
```

### 2️⃣ **Frontend Setup**

```bash
cd web/frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your keys
# For local dev, the defaults work fine

# Run frontend
npm run dev
# Frontend runs on: http://localhost:3000
```

---

## 🌐 Deployment (guindo.me)

### Frontend (Vercel/Netlify)

```bash
# Update .env.local for production:
NEXT_PUBLIC_API_URL=https://api.guindo.me
NEXT_PUBLIC_APP_URL=https://guindo.me

# Build
npm run build

# Deploy to Vercel
vercel --prod
```

### Backend (Railway/Fly.io/AWS)

```bash
# Set environment variables:
OPENAI_API_KEY=your_key
SERPER_API_KEY=your_key

# Deploy (example for Railway)
railway up
```

### DNS Configuration

Point your domain to deployment:
- **guindo.me** → Frontend (Vercel/Netlify)
- **api.guindo.me** → Backend (Railway/Fly.io)

---

## 🔐 Environment Variables

### Frontend (.env.local)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000          # or https://api.guindo.me

# Whop (Payment)
NEXT_PUBLIC_WHOP_PLAN_ID=plan_xxx
NEXT_PUBLIC_WHOP_CLIENT_ID=your_client_id
WHOP_CLIENT_SECRET=your_secret
WHOP_API_KEY=your_api_key
NEXT_PUBLIC_APP_URL=http://localhost:3000          # or https://guindo.me

# Supabase (Database)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### Backend (.env)

```bash
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...
```

---

## 📊 Tech Stack

### **Frontend**
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Markdown**: ReactMarkdown + remark-gfm
- **Auth**: Whop OAuth
- **Database**: Supabase

### **Backend**
- **Framework**: FastAPI
- **AI**: OpenAI GPT-4 Turbo
- **Orchestration**: CrewAI + LangChain
- **Language**: Python 3.11

---

## 🎨 Design System

- **Base Color**: `#0A0A0F` (dark background)
- **Gradients**: Violet → Purple → Fuchsia
- **Font**: Inter
- **Icons**: Lucide React
- **Layout**: Glassmorphism cards with backdrop blur

---

## 🛣️ URL Routes

```
/                           → Landing page
/payment                    → Payment & auth
/questionnaire              → 30+ question form
/results/career             → Career roadmap
/results/roi                → Education ROI
/results/fire               → FIRE planning
/results/side_hustle        → Side income
/results/interests_roadmap  → Passion paths
```

---

## 🤝 Contributing

This is a private project. Contact the team for access.

---

## 📄 License

Proprietary - All rights reserved

---

## 🔗 Links

- **Production**: [guindo.me](https://guindo.me)
- **API**: [api.guindo.me](https://api.guindo.me)
- **Support**: contact@guindo.me

---

**Built with ❤️ using AI**
