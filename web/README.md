# 🎯 FIRE Planning System - Web Application

Modern, AI-powered career and retirement planning system with beautiful UI.

## 🚀 Features

- **Modern Multi-Step Form**: Beautiful, smooth questionnaire with 10 sections
- **AI-Powered Analysis**: Real Groq AI (Llama 3.3 70B) for personalized insights
- **4 Comprehensive Reports**:
  - 🎯 Career Roadmap
  - 💰 Education ROI Analysis
  - 🔥 FIRE Retirement Plan
  - 🚀 Side Hustle Strategies
- **Responsive Design**: Works on all devices
- **Real-time Progress**: See your progress as you complete sections
- **Beautiful Results**: Markdown-powered, tabbed results display

## 📁 Project Structure

```
web/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   └── requirements.txt
└── frontend/            # Next.js frontend
    ├── app/
    │   ├── page.tsx     # Landing page
    │   ├── layout.tsx
    │   └── globals.css
    ├── components/
    │   ├── QuestionnaireFlow.tsx
    │   └── ResultsDisplay.tsx
    ├── package.json
    └── tailwind.config.ts
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python API framework
- **Groq AI** - Llama 3.3 70B for AI analysis
- **Pydantic** - Data validation
- **CORS** - Cross-origin requests

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Smooth animations
- **React Markdown** - Display AI responses
- **Axios** - API requests
- **Lucide React** - Icons

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- GROQ API Key

### Backend Setup

```bash
cd web/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../../.env .env  # Use the existing .env with GROQ_API_KEY
```

### Frontend Setup

```bash
cd web/frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local
# Edit .env.local if backend runs on different port
```

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd web/backend
source venv/bin/activate
python main.py
```

Backend will run on: `http://localhost:8000`

### Start Frontend (Terminal 2)

```bash
cd web/frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## 📱 Usage Flow

1. **Landing Page**
   - User sees beautiful hero section
   - Click "Hadi Başlayalım" to start

2. **Questionnaire (10 Sections)**
   - Basic Info (name, age, university...)
   - Current Status (job, salary, satisfaction...)
   - Skills (programming, ML, cloud...)
   - Education Plans (master decision...)
   - Career Goals (dream job, salary...)
   - Financial (savings, debt, risk...)
   - FIRE Vision (retirement age, lifestyle...)
   - Side Hustle (interests, hours...)
   - Personality (learning style, fears...)
   - Time (urgency, daily hours...)

3. **AI Analysis**
   - Backend receives profile
   - Calls Groq AI 4 times (parallel)
   - Generates personalized reports

4. **Results Display**
   - Beautiful tabbed interface
   - Markdown rendering
   - Download/Share options

## 🔑 API Endpoints

### `GET /`
Health check and API info

### `GET /health`
Check if GROQ API is configured

### `POST /api/analyze`
Request body:
```json
{
  "profile": { ...UserProfile },
  "analysis_type": "career" | "roi" | "fire" | "side_hustle"
}
```

Returns single analysis

### `POST /api/analyze-all`
Request body: `UserProfile`

Returns all 4 analyses at once

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (trust, professionalism)
- **FIRE**: Orange/Red gradient (energy, fire theme)
- **Purple**: Accent (creativity, ambition)

### Typography
- **Font**: Inter (clean, modern)
- **Sizes**: Responsive, mobile-first

### Components
- **Cards**: Glassmorphism (backdrop-blur)
- **Buttons**: Gradient backgrounds with hover effects
- **Forms**: Clean, minimal with focus states
- **Progress**: Linear gradient bar

## 🔒 Security

- API keys stored in `.env` (not committed)
- CORS configured for frontend origin only
- Input validation with Pydantic
- No file storage (all in-memory)

## 📊 AI Prompts

Each analysis has a detailed, structured prompt:

1. **Career Analysis**
   - Current situation analysis
   - Step-by-step roadmap
   - Priority skills
   - Projects & certifications
   - Salary projection
   - Risks & Plan B

2. **ROI Analysis**
   - 3 scenarios (no master / TR master / abroad master)
   - Financial analysis (NPV, ROI)
   - Career impact
   - FIRE contribution
   - Risk analysis
   - Net recommendation

3. **FIRE Plan**
   - Reality check
   - Monthly savings plan
   - Investment strategy
   - Yearly milestones
   - Income growth
   - Expense optimization
   - Emergency plans
   - Success probability

4. **Side Hustle**
   - 5 strategies (easy → hard)
   - Financial projections
   - Time & effort
   - Fit score
   - 30-day action plan
   - Success probability

## 🚢 Deployment

### Backend (Railway/Render/Fly.io)
```bash
# Dockerfile for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy 'out' directory
```

## 📈 Future Improvements

- [ ] Email reports
- [ ] PDF generation
- [ ] User accounts (save profiles)
- [ ] Progress tracking over time
- [ ] Community features (share plans anonymously)
- [ ] Multiple AI model options
- [ ] Multilingual support

## 🐛 Troubleshooting

### Backend won't start
- Check GROQ_API_KEY in .env
- Verify Python 3.11+
- Check port 8000 availability

### Frontend connection error
- Verify backend is running
- Check NEXT_PUBLIC_API_URL in .env.local
- Check CORS settings

### AI responses slow
- Normal for first request (cold start)
- Groq is generally fast (<5s)

## 💡 Development Tips

1. **Hot Reload**: Both backend (uvicorn) and frontend (Next.js) support hot reload
2. **Console Logs**: Check browser console for frontend errors, terminal for backend
3. **API Testing**: Use `/docs` endpoint for Swagger UI (`http://localhost:8000/docs`)

## 📝 License

MIT

## 🙏 Credits

- **AI**: Groq (Llama 3.3 70B)
- **UI**: Tailwind CSS, Framer Motion
- **Icons**: Lucide React

---

**Made with ❤️ for people who are undecided about their future**
