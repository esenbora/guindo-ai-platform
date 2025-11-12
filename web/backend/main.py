"""
FIRE Planning System - FastAPI Backend
Modern, async API for personalized FIRE planning
"""

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict
import os
import re
import time
from dotenv import load_dotenv
from groq import Groq
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from logger import logger, log_request, log_ai_request, log_error

load_dotenv()

# Security: API Secret Key for authentication
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
if not API_SECRET_KEY and os.getenv("ENVIRONMENT") == "production":
    raise ValueError("API_SECRET_KEY must be set in production environment")

app = FastAPI(
    title="FIRE Planning API",
    description="AI-powered personalized FIRE planning and career guidance",
    version="1.0.0"
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration from environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],  # Restrict to only needed methods
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

# Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# ============ SECURITY ============

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key for protected endpoints.
    In development, API key is optional.
    In production, API key is required.
    """
    # Skip auth in development if no API_SECRET_KEY is set
    if not API_SECRET_KEY:
        return "dev-mode"

    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing X-API-Key header"
        )

    if x_api_key != API_SECRET_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return x_api_key

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests and add security headers"""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Log request
    log_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms
    )

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # HTTPS only in production
    if os.getenv("ENVIRONMENT") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response

# ============ MODELS ============

class UserProfile(BaseModel):
    # Basic Info
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=16, le=100)
    university: str = Field(..., min_length=1, max_length=200)
    major: str = Field(..., min_length=1, max_length=200)
    grad_year: str = Field(..., min_length=4, max_length=20)
    location: str = Field(..., min_length=1, max_length=100)
    relocation_ok: str

    # Current Status
    current_job: str
    primary_industry: Optional[str] = ""  # Industry detection
    current_salary: Optional[str] = "0"
    job_satisfaction: Optional[str] = "0"
    years_current_job: Optional[str] = "0"
    industry: Optional[str] = "none"
    company_size: Optional[str] = "none"

    # Skills (Now optional and multi-industry)
    share_skills: Optional[str] = "no"
    key_skills: Optional[str] = ""
    skill_level: Optional[str] = ""
    tools_platforms: Optional[str] = ""
    certifications: Optional[str] = ""
    portfolio_work: Optional[str] = ""

    # Legacy fields (keep for backwards compatibility)
    programming_langs: Optional[str] = ""
    prog_level: Optional[str] = ""
    ml_exp: Optional[str] = ""
    frameworks: Optional[str] = ""
    cloud_exp: Optional[str] = ""
    data_tools: Optional[str] = ""
    github_projects: Optional[str] = ""

    # Education - Basic
    considering_masters: str

    # Education - Detailed (conditional)
    masters_fields_interested: Optional[str] = ""
    masters_location_preference: Optional[str] = ""
    masters_program_language: Optional[str] = ""
    masters_type: Optional[str] = ""
    can_afford_masters: Optional[str] = ""
    masters_timeline: Optional[str] = ""
    masters_work_while_study: Optional[str] = ""
    masters_priority: Optional[str] = ""
    masters_specific_programs: Optional[str] = ""
    masters_concerns: Optional[str] = ""

    # Career Goals
    dream_job: str
    dream_salary: str
    target_years: str
    career_path_preference: str
    willing_to_study: str

    # Financial
    monthly_expenses: str
    savings: str
    monthly_savings_goal: str
    debts: str
    family_support: str
    risk_tolerance: str

    # FIRE Vision
    retire_age: str
    fire_lifestyle: str
    retirement_location: str
    passive_income_interest: str

    # Side Hustle
    time_for_side: str
    side_interests: str
    freelance_exp: str
    preferred_side_income: str
    monthly_side_income_goal: str

    # Constraints & Preferences
    time_commit: str
    learning_style: str
    work_life_balance: str
    biggest_obstacle: str
    need_most: str

    # Interests & Passions
    passion_topics: str
    flow_activities: str
    dream_projects: str
    role_models: str

    # Input validation and sanitization
    @validator('*', pre=True)
    def sanitize_strings(cls, v):
        """Strip whitespace and limit string length to prevent injection attacks"""
        if isinstance(v, str):
            # Strip whitespace
            v = v.strip()
            # Limit max length to 2000 characters per field
            if len(v) > 2000:
                v = v[:2000]
            # Remove potentially dangerous characters
            # Allow alphanumeric, spaces, common punctuation, and international characters
            v = re.sub(r'[<>{}]', '', v)  # Remove HTML/code injection characters
        return v

    @validator('name', 'university', 'major', 'location')
    def validate_text_fields(cls, v):
        """Additional validation for critical text fields"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Field cannot be empty")
        return v

    @validator('age')
    def validate_age(cls, v):
        """Validate age is within reasonable range"""
        if v < 16 or v > 100:
            raise ValueError("Age must be between 16 and 100")
        return v

class AnalysisRequest(BaseModel):
    profile: UserProfile
    analysis_type: str  # "career" | "roi" | "fire" | "side_hustle"

class AnalysisResponse(BaseModel):
    analysis: str
    analysis_type: str
    timestamp: str

# ============ AI HELPERS ============

def call_ai(prompt: str, system: str, analysis_type: str = "general") -> str:
    """Call Groq API with logging"""
    model = "llama-3.3-70b-versatile"

    try:
        logger.info(f"AI Request - Type: {analysis_type}, Model: {model}")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )

        # Log token usage if available
        if hasattr(response, 'usage') and response.usage:
            tokens = response.usage.total_tokens
            logger.info(f"AI Response - Type: {analysis_type}, Tokens: {tokens}")

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("AI response content is None")
        return content

    except Exception as e:
        log_error(e, context=f"AI Request ({analysis_type})")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

# ============ ANALYSIS FUNCTIONS ============

def analyze_career(profile: UserProfile) -> str:
    """Generate career path analysis with 2025 market insights"""

    # Determine industry from user profile
    industry = profile.primary_industry or "Technology & Engineering"

    # Industry-specific system prompts
    industry_prompts = {
        "Technology & Engineering": "You are an experienced tech career coach. As of 2025, you provide CLEAR and ACTIONABLE roadmaps with current market data, trending technologies, and realistic salary benchmarks. You stay updated on the latest tools, frameworks, and industry trends.",
        "Business & Finance": "You are an experienced business and finance career consultant. As of 2025, you provide CLEAR and ACTIONABLE roadmaps for MBA, consulting, finance, and corporate careers with current market data, realistic salary benchmarks, and industry trends.",
        "Healthcare & Medicine": "You are an experienced healthcare career consultant. As of 2025, you provide CLEAR and ACTIONABLE roadmaps for medical professionals with current market data, specialty insights, residency paths, and realistic salary benchmarks.",
        "Creative & Design": "You are an experienced creative industry career consultant. As of 2025, you provide CLEAR and ACTIONABLE roadmaps for designers, artists, and creative professionals with current market data, portfolio strategies, and realistic income benchmarks.",
        "Education": "You are an experienced education career consultant. As of 2025, you provide CLEAR and ACTIONABLE roadmaps for educators and academic professionals with current market data and realistic salary benchmarks.",
        "Legal": "You are an experienced legal career consultant. As of 2025, you provide CLEAR and ACTIONABLE roadmaps for legal professionals with current market data, firm paths, and realistic salary benchmarks.",
        "Other": "You are an experienced multi-industry career coach. As of 2025, you provide CLEAR and ACTIONABLE roadmaps with current market data and realistic salary benchmarks for various industries."
    }

    system = industry_prompts.get(industry, industry_prompts["Other"])

    prompt = f"""DETAILED PERSONAL CAREER ANALYSIS:

👤 PERSON:
- {profile.name}, {profile.age} years old, {profile.university} {profile.major} ({profile.grad_year})
- Location: {profile.location}, Open to relocation: {profile.relocation_ok}
- Biggest obstacle: {profile.biggest_obstacle}, What they need most: {profile.need_most}

💼 CURRENT SITUATION:
- Position: {profile.current_job} (${profile.current_salary}/year)
- Satisfaction: {profile.job_satisfaction}/10, Experience: {profile.years_current_job}
- Industry: {profile.industry}, Company size: {profile.company_size}

🛠️ SKILLS:
{"- Key Skills: " + profile.key_skills if profile.key_skills else "- Professional skills not specified"}
{"- Skill Level: " + profile.skill_level if profile.skill_level else ""}
{"- Tools/Platforms: " + profile.tools_platforms if profile.tools_platforms else ""}
{"- Certifications/Licenses: " + profile.certifications if profile.certifications else ""}
{"- Portfolio/Work: " + profile.portfolio_work if profile.portfolio_work else ""}

🎓 EDUCATION:
- Master's consideration: {profile.considering_masters}
- Fields interested: {profile.masters_fields_interested}
- Location preference: {profile.masters_location_preference}
- Can afford: {profile.can_afford_masters}

🎯 GOALS:
- Dream role: {profile.dream_job}
- Target salary: ${profile.dream_salary}/year (in {profile.target_years} years)
- Career path preference: {profile.career_path_preference}
- Work-life balance importance: {profile.work_life_balance}
- Learning commitment: {profile.time_commit} hours/week
- Learning style: {profile.learning_style}

CREATE DETAILED CAREER PLAN (Markdown format):

**IMPORTANT 2025 CONTEXT**:
- Use 2025 salary data from Levels.fyi, Glassdoor, LinkedIn Salary
- Recommend current tools: Cursor IDE, Claude/GPT-4, v0.dev, Replit Agent, etc.
- Focus on trending tech: LLMs/AI agents, Next.js 15, Python 3.12, Rust, Go
- Mention 2025 market trends: 🔥 Hot, ⚡ Rising, 📈 Growing, 📊 Steady

## 1️⃣ Current Situation Analysis (2025 Perspective)
- **Strengths** (3 points - mention if skills are 🔥 hot in 2025)
- **Gaps/Risks** (3 points - what's outdated or missing in 2025 market)
- **Master's Decision**: Should they do it? (clear reasoning with 2025 ROI data)

## 2️⃣ Step-by-Step Roadmap
- **First 3 Months**: Concrete actions (use 2025 tools/platforms)
- **6-12 Months**: Skills/Certifications (trending in 2025)
- **1-2 Years**: Position changes
- **3-5 Years**: Reaching target role

## 3️⃣ Priority Skills (2025 Edition)
- **Immediate** (1-3 months): 🔥 Hot skills to learn NOW
  - Specific versions: e.g., "Next.js 15 with Server Components", "FastAPI + Pydantic V2"
- **Mid-term** (3-12 months): ⚡ Rising technologies
- **Long-term** (1-2 years): 📈 Future-proof skills

## 4️⃣ Projects & Certifications
- **3 project recommendations** (using 2025 tech stack)
  - Example: "Build an AI agent with LangChain + GPT-4 API"
- **2-3 certifications** (2025 relevant)
  - Prioritize: AWS/Azure AI certifications, etc.

## 5️⃣ Salary & Timeline Projection (2025 Benchmark Data)
| Year | Position | Salary (2025 $) | Market Trend | Notes |
|------|----------|-----------------|--------------|-------|
| 0 | {profile.current_job} | ${profile.current_salary} | - | Now |
| ... | ... | ... | 🔥/⚡/📈 | ... |

**Use 2025 salary ranges from Levels.fyi for {profile.dream_job}**

## 6️⃣ Risks & Plan B
- Failure probability (considering 2025 job market)
- Things to watch out for (AI automation, market saturation)
- Alternative plan

## 7️⃣ 2025 Tools & Resources to Use NOW
- **AI Coding**: Cursor, GitHub Copilot, v0.dev
- **Learning**: YouTube creators, specific Discord communities
- **Job Search**: Levels.fyi, Wellfound (AngelList), specific Slack/Discord

CLEAR, ACTIONABLE, CURRENT. Max 60 lines.
Every recommendation should feel like it's from 2025, not 2020."""

    return call_ai(prompt, system, analysis_type="career")

def analyze_roi(profile: UserProfile) -> str:
    """Generate ULTRA DETAILED education ROI analysis with 2025 program recommendations"""

    # Industry-specific education analysis
    industry = profile.primary_industry or "Technology & Engineering"

    industry_ed_prompts = {
        "Technology & Engineering": "You are a world-class tech education consultant and financial analyst. As of 2025, you analyze Master's degrees, bootcamps, certifications, and self-learning for tech professionals with current tuition costs, 2025-2026 admission data, and ROI statistics.",
        "Business & Finance": "You are a world-class business education consultant and financial analyst. As of 2025, you analyze MBA programs, executive education, CFA, CPA, and other business credentials with current costs, admission data, and ROI statistics.",
        "Healthcare & Medicine": "You are a world-class medical education consultant and financial analyst. As of 2025, you analyze medical specialties, residency paths, fellowships, and additional certifications with current costs and ROI statistics.",
        "Creative & Design": "You are a world-class creative education consultant and financial analyst. As of 2025, you analyze MFA programs, design bootcamps, specialized courses, and portfolio schools with current costs and ROI statistics.",
        "Education": "You are a world-class education sector consultant and financial analyst. As of 2025, you analyze Master's in Education, EdD, PhD programs, and teaching certifications with current costs and ROI statistics.",
        "Legal": "You are a world-class legal education consultant and financial analyst. As of 2025, you analyze law school (JD), LLM programs, legal specializations, and bar exam preparation with current costs and ROI statistics.",
        "Other": "You are a world-class education consultant and financial analyst. As of 2025, you analyze various advanced degrees and professional certifications across industries with current costs and ROI statistics."
    }

    system = industry_ed_prompts.get(industry, industry_ed_prompts["Other"])

    years_left = int(profile.retire_age) - int(profile.age)
    current_age = int(profile.age)

    prompt = f"""ULTRA DETAILED EDUCATION & MASTER'S ANALYSIS + PROGRAM RECOMMENDATIONS

👤 PERSON:
- {profile.name}, {current_age} years old, {profile.university} {profile.major}
- Master's consideration: {profile.considering_masters}
- Fields interested: {profile.masters_fields_interested}
- Location preference: {profile.masters_location_preference}
- Program language: {profile.masters_program_language}
- Type: {profile.masters_type}
- Budget: {profile.can_afford_masters}
- Timeline: {profile.masters_timeline}
- Work while studying: {profile.masters_work_while_study}
- Priority: {profile.masters_priority}
- Programs in mind: {profile.masters_specific_programs}
- Concerns: {profile.masters_concerns}

💰 FINANCIAL:
- Current salary: ${profile.current_salary}, Savings: ${profile.savings}
- Target: {profile.dream_job} - ${profile.dream_salary}/year
- FIRE goal: Retire at {profile.retire_age}, {years_left} years left
- Risk tolerance: {profile.risk_tolerance}

**IMPORTANT 2025 CONTEXT**:
- Use 2025-2026 tuition costs (check recent updates!)
- Reference 2024-2025 admission cycles and acceptance rates
- Use post-COVID salary data (2023-2025 graduates)
- Mention program changes, new specializations
- For each university: Check if they added AI/ML tracks in 2024-2025
- Include trend indicators: 🔥 Program getting more competitive, ⚡ New program, 📈 Rising in rankings

## 1️⃣ MASTER'S DECISION ANALYSIS

### Is a Master's Necessary for You?
- For {profile.dream_job}, is a master's **REQUIRED** or just a **BONUS**?
- Can you reach this position WITHOUT a master's?
- What's the real value of a master's in this field?

## 2️⃣ DETAILED SCENARIO COMPARISON (6 Scenarios)

For each scenario provide:
- Total cost (tuition + living + opportunity cost)
- Starting salary (post-master's)
- Total earnings over {years_left} years
- NPV (5% discount rate)
- ROI (%)
- How many years to reach {profile.dream_job}
- Impact on FIRE goal ({years_left} years)

### Scenario 1: NO Master's - Straight to Work
- Advantages / Disadvantages
- Financial calculations

### Scenario 2: Public University Master (Low/Free Cost)
- Which universities (top 3-5 in user's country/region)
- Advantages / Disadvantages
- Financial calculations

### Scenario 3: Private University Master ($5-15K)
- Which specific programs (concrete recommendations)
- Advantages / Disadvantages
- Financial calculations

### Scenario 4: European Master ($15-30K)
- Which countries/programs (budget-friendly)
- Germany (tuition-free), Netherlands, Sweden, etc.
- Advantages / Disadvantages
- Financial calculations

### Scenario 5: US/UK Top Programs ($60K+)
- Which programs (especially evaluate {profile.masters_specific_programs} if mentioned)
- Scholarship opportunities
- Advantages / Disadvantages
- Financial calculations

### Scenario 6: Online/Part-time Master
- Which programs (Georgia Tech OMSCS, UT Austin, etc.)
- Advantages / Disadvantages
- Financial calculations

## 3️⃣ CONCRETE PROGRAM RECOMMENDATIONS

Based on your profile, the BEST 5-7 PROGRAMS for you:

For each program provide:
- **Program Name & University**
- **Location & City**
- **Duration** (1 year / 2 years / part-time)
- **Total Cost** (realistic estimate)
- **Your Admission Chance** (low/medium/high + reasoning)
- **Strengths** (career impact, network, location)
- **Weaknesses**
- **ROI Score** (/10)
- **Fit Score for You** (/10)
- **Application Deadline** (approximate)

Example format:
### Program 1: MIT Computer Science MS
- **Location**: Cambridge, MA, USA
- **Duration**: 2 years (thesis-based)
- **Cost**: ~$80K
- **Admission Chance**: Medium (strong tech background needed)
- **Strengths**: Prestige, network, research opportunities
- **Weaknesses**: High cost, competitive admission
- **ROI**: 9/10
- **Fit**: 7/10

## 4️⃣ DETAILED FINANCIAL TABLE

| Scenario | Cost | Starting Salary | 5Y Total | 10Y Total | NPV | ROI | FIRE Impact |
|---------|------|------------------|----------|-----------|-----|-----|-------------|
| 1. Work | $0   | $?K             | $?K      | $?K       | $?K | -   | ? years     |
| 2. Public | $?K | $?K            | $?K      | $?K       | $?K | ?%  | ? years     |
| 3. Private | $?K | $?K           | $?K      | $?K       | $?K | ?%  | ? years     |
| 4. Europe | $?K  | $?K            | $?K      | $?K       | $?K | ?%  | ? years     |
| 5. US/UK | $?K  | $?K             | $?K      | $?K       | $?K | ?%  | ? years     |
| 6. Online | $?K | $?K             | $?K      | $?K       | $?K | ?%  | ? years     |

## 5️⃣ ADDRESSING YOUR CONCERNS

Concerns: {profile.masters_concerns}

Address EACH concern individually with solutions and recommendations.

## 6️⃣ CLEAR RECOMMENDATION & DECISION TREE

### IF {profile.masters_priority} is your priority:
→ Which scenario/program should you choose?
→ Why this one?
→ How to apply?
→ How to finance it?

### ALTERNATIVE PLAN:
If your best option doesn't work out, what's Plan B?

### TIMELINE:
- Now - 3 months: ?
- 3-6 months: ?
- 6-12 months: ?
- Application deadlines

### FINAL VERDICT:
1 paragraph, CLEAR decision: Do/Don't do a master's + which program + why?

Max 100 lines. DETAILED, CONCRETE, ACTIONABLE.
Use real program names, universities, cities.
Make calculations REALISTIC."""

    return call_ai(prompt, system, analysis_type="roi")

def analyze_fire(profile: UserProfile) -> str:
    """Generate FIRE retirement plan with 2025 investment strategies"""
    system = "You are a FIRE (Financial Independence, Retire Early) movement expert. As of 2025, you create REALISTIC and ACTIONABLE retirement plans using current inflation rates, 2025 investment platforms, updated 4% rule discussions, and modern portfolio strategies. You understand post-2024 market conditions and tax-advantaged accounts."

    current_age = int(profile.age)
    retire_age = int(profile.retire_age)
    years = retire_age - current_age

    prompt = f"""PERSONALIZED FIRE RETIREMENT PLAN (Markdown format):

👤 PERSON:
{profile.name}: Age {current_age} → {retire_age} ({years} years to FIRE)
Lifestyle: {profile.fire_lifestyle}
Location: {profile.retirement_location}
Passive income interest: {profile.passive_income_interest}

💰 FINANCIAL SITUATION:
- Current salary: ${profile.current_salary}/year
- Dream salary: ${profile.dream_salary}/year
- Monthly expenses: ${profile.monthly_expenses}
- Savings: ${profile.savings}
- Monthly savings goal: ${profile.monthly_savings_goal}
- Debts: ${profile.debts}
- Family support: {profile.family_support}
- Risk tolerance: {profile.risk_tolerance}

**IMPORTANT 2025 CONTEXT**:
- Use 2025 inflation rate (current estimates)
- Recommend 2025 investment platforms: Vanguard, Fidelity, IBKR, Schwab
- Reference updated 4% rule discussions (some say 3.5% post-2024)
- ETF recommendations: VT, VTI, VXUS (check 2025 expense ratios)
- Tax optimization: Roth IRA limits 2025, backdoor Roth strategies
- Include crypto allocation debate (if risk tolerance allows)
- Market trend: 📈 Consider recent bull/bear market impact

## 1️⃣ Reality Check
- Is retiring at {retire_age} realistic in {years} years?
- What are the main risks and challenges?
- Required portfolio size (4% rule calculation)

## 2️⃣ Monthly Savings Plan
- With current salary (${profile.current_salary}): How much can you save?
- With target salary (${profile.dream_salary}): How much can you save?
- Required savings rate: ?%
- Can you reach it? How?

## 3️⃣ Investment Strategy
Risk tolerance: {profile.risk_tolerance}
- Stocks/ETFs: ?%
- Bonds: ?%
- Real Estate: ?%
- Alternative investments: ?%
- Recommended platforms/brokers
- Specific fund recommendations

## 4️⃣ Annual Milestones
| Year | Age | Portfolio Value | How to Reach |
|------|-----|-----------------|--------------|
| 0 | {current_age} | ${profile.savings} | Current |
| ... | ... | ... | ... |
| {years} | {retire_age} | $? | FIRE! |

## 5️⃣ Income Growth Strategy
- Main job salary projection
- Side income target (from side hustle plan)
- Is side income necessary for FIRE?
- How to accelerate income growth

## 6️⃣ Expense Optimization
- Current: ${profile.monthly_expenses}/month
- Optimized target: ?
- Major cutting opportunities
- Lifestyle changes needed
- Impact on FIRE timeline

## 7️⃣ Emergency Plans
- **Bear Market**: What if market drops 50%?
- **Job Loss**: Backup plan?
- **Health Issues**: Insurance coverage?
- **Inflation**: How to protect?

## 8️⃣ First 30 Days Action Plan
5 concrete steps to start NOW:
1. ?
2. ?
3. ?
4. ?
5. ?

## 9️⃣ Success Probability
- With current approach: ?%
- With all recommendations: ?%
- Key factors affecting success
- Biggest obstacles to watch out for

## 🔟 FIRE Number Breakdown
- Annual expenses in retirement: $?
- Required portfolio (4% rule): $?
- With {profile.fire_lifestyle} lifestyle: $?
- Monthly passive income needed: $?

Max 60 lines. REALISTIC, DETAILED, ACTIONABLE."""

    return call_ai(prompt, system, analysis_type="fire")

def analyze_side_hustle(profile: UserProfile) -> str:
    """Generate side income strategies with 2025 platforms and trends"""

    # Industry-specific side hustle opportunities
    industry = profile.primary_industry or "Technology & Engineering"

    industry_hustle_prompts = {
        "Technology & Engineering": "You are an entrepreneurship and tech side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for tech professionals using current platforms (Gumroad, Lemon Squeezy, Stripe), trending niches (AI tools, no-code, SaaS), and realistic 2025 freelance rates.",
        "Business & Finance": "You are an entrepreneurship and business side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for business professionals including consulting, coaching, courses, and financial advisory with realistic 2025 rates.",
        "Healthcare & Medicine": "You are an entrepreneurship and healthcare side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for medical professionals including telemedicine, medical writing, consulting, and education with realistic 2025 rates.",
        "Creative & Design": "You are an entrepreneurship and creative side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for creatives including freelance work, digital products, stock assets, and courses with realistic 2025 rates.",
        "Education": "You are an entrepreneurship and education side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for educators including tutoring, course creation, educational content, and consulting with realistic 2025 rates.",
        "Legal": "You are an entrepreneurship and legal side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas for legal professionals including consulting, legal writing, courses, and advisory services with realistic 2025 rates.",
        "Other": "You are an entrepreneurship and side income consultant. As of 2025, you provide CONCRETE, ACTIONABLE side business ideas using current platforms and realistic 2025 rates for various industries."
    }

    system = industry_hustle_prompts.get(industry, industry_hustle_prompts["Other"])

    prompt = f"""PERSONALIZED SIDE INCOME STRATEGIES (Markdown format):

👤 PERSON:
{profile.name}, {profile.age} years old
Industry: {industry}
{"Key Skills: " + profile.key_skills if profile.key_skills else ""}
{"Tools/Platforms: " + profile.tools_platforms if profile.tools_platforms else ""}
{"Portfolio/Work: " + profile.portfolio_work if profile.portfolio_work else ""}

⏰ TIME & PREFERENCES:
- Available time for side hustle: {profile.time_for_side}
- Interests: {profile.side_interests}
- Freelance experience: {profile.freelance_exp}
- Preferred side income type: {profile.preferred_side_income}
- Monthly goal: ${profile.monthly_side_income_goal}
- Learning commitment: {profile.time_commit} hours/week
- Work-life balance importance: {profile.work_life_balance}

💰 GOALS:
- FIRE target age: {profile.retire_age}
- Monthly side income goal: ${profile.monthly_side_income_goal}
- Risk tolerance: {profile.risk_tolerance}

**IMPORTANT 2025 CONTEXT**:
- Recommend 2025 platforms: Gumroad, Lemon Squeezy, Whop, Stripe
- Trending niches: 🔥 AI tools/wrappers, AI content, no-code solutions, automation
- Freelance rates: Use 2025 Upwork/Contra/Toptal averages
- Creator tools: Beehiiv, ConvertKit, Substack (2025 features)
- Payment: Stripe Climate, crypto payments becoming mainstream
- Market indicators: 🔥 Very hot / ⚡ Growing / 📈 Emerging

## 5 SIDE INCOME STRATEGIES (Easy → Hard)

For EACH strategy provide:

### Strategy 1: Freelance/Consulting
- **What you'll do**: Specific services (be concrete)
- **Income Timeline**: Month 1 $?, Month 6 $?, Year 1 $?
- **Time Investment**: Initial setup hours, weekly maintenance hours
- **Startup Cost**: $?
- **Fit Score**: ?/10 (how well this matches your skills/interests)
- **First 30 Days Plan**:
  - Week 1: ?
  - Week 2: ?
  - Week 3: ?
  - Week 4: ?
- **Success Probability**: ?%
- **Platforms to Use**: (Upwork, Fiverr, etc.)
- **How to Get First Client**: Concrete steps

### Strategy 2: Product/SaaS Development
- **What you'll do**: Specific product idea
- **Income Timeline**: Month 1 $?, Month 6 $?, Year 1 $?
- **Time Investment**: Initial setup hours, weekly maintenance hours
- **Startup Cost**: $?
- **Fit Score**: ?/10
- **First 30 Days Plan**: Week-by-week
- **Success Probability**: ?%
- **Tech Stack**: Recommended technologies
- **Monetization**: How will you charge?

### Strategy 3: Content Creation/Education
- **What you'll do**: (YouTube, courses, blog, newsletter)
- **Income Timeline**: Month 1 $?, Month 6 $?, Year 1 $?
- **Time Investment**: Initial setup hours, weekly maintenance hours
- **Startup Cost**: $?
- **Fit Score**: ?/10
- **First 30 Days Plan**: Week-by-week
- **Success Probability**: ?%
- **Platform**: Where to publish?
- **Content Ideas**: First 10 topics

### Strategy 4: Passive Income Products
- **What you'll do**: (Digital products, templates, tools)
- **Income Timeline**: Month 1 $?, Month 6 $?, Year 1 $?
- **Time Investment**: Initial setup hours, weekly maintenance hours
- **Startup Cost**: $?
- **Fit Score**: ?/10
- **First 30 Days Plan**: Week-by-week
- **Success Probability**: ?%
- **Distribution**: How to sell?

### Strategy 5: Advanced/Scalable Business
- **What you'll do**: Specific business model
- **Income Timeline**: Month 1 $?, Month 6 $?, Year 1 $?
- **Time Investment**: Initial setup hours, weekly maintenance hours
- **Startup Cost**: $?
- **Fit Score**: ?/10
- **First 30 Days Plan**: Week-by-week
- **Success Probability**: ?%
- **Scaling Plan**: How to grow?

## CLEAR RECOMMENDATION

### Which strategy should you START with?
- **Pick**: Strategy #?
- **Why**: Reasoning based on skills, time, goals
- **First 7 Days Action Plan**:
  - Day 1: ?
  - Day 2-3: ?
  - Day 4-5: ?
  - Day 6-7: ?

### 6-Month Income Target
- Conservative: $?/month
- Realistic: $?/month
- Optimistic: $?/month

### Impact on FIRE Goal
- Without side income: Retire at {profile.retire_age}
- With ${profile.monthly_side_income_goal}/month side income: Retire ? years earlier

### Backup Plan
If your primary strategy doesn't work after 3 months, what's Plan B?

Max 80 lines. CONCRETE, SPECIFIC, ACTIONABLE.
Real platforms, real numbers, real timelines."""

    return call_ai(prompt, system, analysis_type="side_hustle")

def analyze_interests_roadmap(profile: UserProfile) -> str:
    """Generate passion-based career roadmap and alternative paths"""
    system = "You are a career pivot specialist and passion-career alignment expert across all industries. You help people discover career paths that align with their true interests - whether in tech, business, healthcare, creative fields, or any other sector. As of 2025, you provide current industry insights and realistic transition strategies for any profession."

    prompt = f"""PASSION-ALIGNED CAREER ROADMAP (Markdown format):

👤 PERSON:
{profile.name}, {profile.age} years old
Current: {profile.current_job} (${profile.current_salary}/year)
Industry: {profile.primary_industry or "Not specified"}
{"Key Skills: " + profile.key_skills if profile.key_skills else ""}
Dream role: {profile.dream_job}

💝 PASSIONS & INTERESTS:
- **Topics that excite them**: {profile.passion_topics}
- **Flow state activities**: {profile.flow_activities}
- **Dream projects**: {profile.dream_projects}
- **Role models/inspiration**: {profile.role_models}

🎯 CURRENT GOALS:
- Target role: {profile.dream_job} (${profile.dream_salary}/year in {profile.target_years} years)
- Career preference: {profile.career_path_preference}
- FIRE goal: Retire at {profile.retire_age}

## 1️⃣ PASSION-CAREER ALIGNMENT ANALYSIS

### How aligned is your current path with your passions?
- Current role ({profile.current_job}) vs interests alignment: ?/10
- Dream role ({profile.dream_job}) vs passions alignment: ?/10
- Are you on the right track or should you pivot?

### Hidden Opportunities
Based on passions ({profile.passion_topics}), identify 3-5 career paths they might not have considered:
- Emerging roles in 2025 that match their interests
- Intersection of their skills + passions
- Non-obvious opportunities

## 2️⃣ ALTERNATIVE CAREER PATHS (Based on Passions)

For EACH path provide (3-5 paths total):

### Path 1: [Role Name] 🔥
**Example**: If interested in "AI + teaching" → AI/ML Educator, DevRel Engineer
**Example**: If interested in "game dev" → Game AI Engineer, Technical Game Designer

- **What it is**: Clear description
- **Why it matches your passions**: Connect to {profile.passion_topics}, {profile.flow_activities}
- **2025 Market Demand**: 🔥 Hot / ⚡ Rising / 📈 Growing / 📊 Steady / ⬇️ Declining
- **Salary Range (2025)**: Entry: $?, Mid: $?, Senior: $?
- **Required Skills**: What you already have vs what you need
- **Time to Transition**: ? months realistically
- **Companies Hiring**: Specific companies (2025 data)
- **How to Start**: First 3 concrete steps
- **Resources**: Specific courses, communities, people to follow
- **Success Probability**: ?% (considering current background)
- **Alignment Score**: ?/10 (passion fit)

### Path 2-5: [Repeat format]

## 3️⃣ PIVOT vs STAY COMPARISON

### Option A: Stay on Current Path ({profile.dream_job})
- Pros (3 points)
- Cons (3 points)
- 5-year projection
- Passion fulfillment: ?/10

### Option B: Pivot to Passion-Aligned Path ([Best Alternative])
- Pros (3 points)
- Cons (3 points)
- 5-year projection
- Passion fulfillment: ?/10

### Financial Comparison
| Path | Year 1 | Year 3 | Year 5 | FIRE Impact |
|------|--------|--------|--------|-------------|
| Current ({profile.dream_job}) | $? | $? | $? | Retire at {profile.retire_age} |
| Passion ([Alternative]) | $? | $? | $? | Retire at ? |

## 4️⃣ HYBRID APPROACH (Best of Both Worlds)

Can you blend passion with current path?
- **Strategy 1**: Side project approach (keep {profile.current_job}, build passion project)
- **Strategy 2**: Internal pivot (same company, different role)
- **Strategy 3**: Gradual transition (part-time both for ? months)
- **Recommended**: Which hybrid strategy is best?

## 5️⃣ CONCRETE TRANSITION PLAN

### If you decide to pivot to [Best Passion-Aligned Path]:

**Months 1-3: Foundation**
- Week-by-week action plan
- Skills to acquire
- Projects to build
- Network to build

**Months 4-6: Building Credibility**
- Concrete deliverables
- Portfolio pieces
- First paid work / contributions

**Months 7-12: Transition**
- When to quit current job (if needed)
- How to get first role in new field
- Financial safety net needed: $?

### First 7 Days Starting TODAY:
- Day 1: ?
- Day 2-3: ?
- Day 4-5: ?
- Day 6-7: ?

## 6️⃣ INSPIRATION & VALIDATION

### Real People Who Made Similar Pivots:
- Example 1: [Person/story similar to user's situation]
- Example 2: [Another success story]
- Where to find community: Specific Discord/Slack/communities (2025)

### Your Dream Projects ({profile.dream_projects})
How can these become reality?
- Feasibility analysis
- Monetization potential
- Steps to start

### Role Models ({profile.role_models})
What can you learn from them?
- Their journey insights
- Applicable lessons
- How to connect/learn from them

## 7️⃣ FINAL RECOMMENDATION

### Should you pivot or stay?
**Clear verdict**: Stay on current path / Pivot to [X] / Hybrid approach
**Reasoning**: 2-3 sentences

### If PIVOT recommended:
- Which path: [Specific role]
- Why this one: [Reasoning based on passion + pragmatism]
- Timeline: Start transition in ? months
- Success keys: 3 critical factors

### If STAY recommended:
- How to inject passion into current path
- Side projects to pursue
- Long-term satisfaction strategy

Max 90 lines. CONCRETE, INSPIRING, REALISTIC.
Use 2025 job market data, real company names, specific resources.
Show them a path where work = passion."""

    return call_ai(prompt, system, analysis_type="interests_roadmap")

# ============ API ENDPOINTS ============

@app.get("/")
async def root():
    return {
        "message": "FIRE Planning API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze (POST)"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "groq_api_configured": bool(os.getenv('GROQ_API_KEY'))
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def analyze(
    request: Request,
    analysis_request: AnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate AI analysis based on user profile

    Requires X-API-Key header for authentication.
    Rate limit: 10 requests per minute per IP address.

    analysis_type: "career" | "roi" | "fire" | "side_hustle"
    """
    from datetime import datetime

    analysis_funcs = {
        "career": analyze_career,
        "roi": analyze_roi,
        "fire": analyze_fire,
        "side_hustle": analyze_side_hustle
    }

    if analysis_request.analysis_type not in analysis_funcs:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis_type. Must be one of: {list(analysis_funcs.keys())}"
        )

    try:
        analysis = analysis_funcs[analysis_request.analysis_type](analysis_request.profile)

        return AnalysisResponse(
            analysis=analysis,
            analysis_type=analysis_request.analysis_type,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-all")
@limiter.limit("3/hour")  # 3 requests per hour per IP (heavy operation)
async def analyze_all(
    request: Request,
    profile: UserProfile,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate all 5 analyses at once

    Requires X-API-Key header for authentication.
    Rate limit: 3 requests per hour per IP address (this is a heavy operation).

    Returns: {career, roi, fire, side_hustle, interests_roadmap}
    """
    from datetime import datetime

    try:
        results = {
            "career": analyze_career(profile),
            "roi": analyze_roi(profile),
            "fire": analyze_fire(profile),
            "side_hustle": analyze_side_hustle(profile),
            "interests_roadmap": analyze_interests_roadmap(profile),
            "timestamp": datetime.now().isoformat()
        }
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
