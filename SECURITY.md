# 🔒 Security Configuration Guide

This document provides step-by-step instructions to secure your Guindo application for production deployment.

## ⚠️ CRITICAL: Immediate Actions Required

### 1. Revoke Exposed API Keys (URGENT)

The following API keys in `/web/backend/.env` are currently exposed and must be revoked immediately:

```bash
# Example format (DO NOT USE REAL KEYS):
GROQ_API_KEY=<YOUR_GROQ_API_KEY_HERE>
SERPER_API_KEY=<YOUR_SERPER_API_KEY_HERE>
```

**Action Steps:**

1. **Revoke GROQ API Key:**
   - Go to https://console.groq.com/keys
   - Delete the key ending in `...UY6H`
   - Generate a new API key
   - Update your local `.env` file (never commit this!)

2. **Revoke SERPER API Key:**
   - Go to https://serper.dev/dashboard
   - Delete the key ending in `...7940`
   - Generate a new API key
   - Update your local `.env` file

3. **Secure the .env file:**
   ```bash
   # The .env file is already in .gitignore, but verify:
   cat .gitignore | grep ".env"

   # If you ever committed .env to git, clean the history:
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch web/backend/.env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

### 2. Environment Variables Setup

#### Backend (.env)

```bash
cd web/backend
cp .env.example .env
```

Then edit `.env` and fill in:

```bash
# Required
GROQ_API_KEY=<new_groq_key>
API_SECRET_KEY=<generate_with_openssl_rand_-hex_32>

# Optional
SERPER_API_KEY=<new_serper_key>
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_key>

# Production
ALLOWED_ORIGINS=https://guindo.me
```

#### Frontend (.env.local)

```bash
cd web/frontend
```

Edit `.env.local` and replace placeholders:

```bash
# Production settings for guindo.me
NEXT_PUBLIC_API_URL=https://api.guindo.me
NEXT_PUBLIC_APP_URL=https://guindo.me

# Supabase (get from https://app.supabase.com/project/_/settings/api)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...your_actual_key

# Whop (get from https://dash.whop.com/)
NEXT_PUBLIC_WHOP_PLAN_ID=plan_kY8lADYVlHmhE
NEXT_PUBLIC_WHOP_CLIENT_ID=your_client_id
WHOP_CLIENT_SECRET=your_client_secret
WHOP_API_KEY=your_whop_api_key
```

## 🛡️ Security Checklist

### Before Production Deployment

- [ ] **API Keys Revoked** - Old GROQ and SERPER keys deleted
- [ ] **New Keys Generated** - Fresh API keys in `.env`
- [ ] **API Secret Set** - `API_SECRET_KEY` generated and configured
- [ ] **CORS Configured** - `ALLOWED_ORIGINS` set to production domain
- [ ] **Environment Files Secured** - `.env` files never committed to git
- [ ] **HTTPS Enabled** - SSL certificate configured for guindo.me
- [ ] **API Authentication** - Backend endpoints require API key
- [ ] **Rate Limiting** - API endpoints protected from abuse
- [ ] **Input Validation** - Pydantic validators implemented
- [ ] **Error Handling** - Error boundaries and proper logging
- [ ] **Monitoring Enabled** - Error tracking configured

### Recommended Security Measures

#### 1. API Authentication

Add API key verification to backend endpoints:

```python
# In main.py
from fastapi import Header, HTTPException

API_SECRET = os.getenv("API_SECRET_KEY")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Protect endpoints:
@app.post("/api/analyze", dependencies=[Depends(verify_api_key)])
async def analyze_endpoint(profile: UserProfile):
    # ...
```

#### 2. Rate Limiting

Install slowapi:

```bash
pip install slowapi
```

Add to main.py:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/analyze-all")
@limiter.limit("3/hour")  # 3 requests per hour per IP
async def analyze_all(profile: UserProfile, request: Request):
    # ...
```

#### 3. Input Validation

Add Pydantic validators:

```python
from pydantic import validator, Field

class UserProfile(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=16, le=100)

    @validator('name')
    def sanitize_name(cls, v):
        # Remove potentially dangerous characters
        return ''.join(c for c in v if c.isalnum() or c.isspace())

    @validator('*', pre=True)
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()[:1000]  # Max 1000 chars
        return v
```

#### 4. CORS Configuration

Update CORS to use environment variable:

```python
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)
```

#### 5. HTTPS Headers

Add security headers:

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["guindo.me", "api.guindo.me"])

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## 🚀 Production Deployment

### Backend Deployment (api.guindo.me)

**Recommended: Railway/Render/Fly.io**

1. Create new project
2. Connect GitHub repository (if using git - ensure .env is NOT committed)
3. Set environment variables in platform dashboard
4. Deploy from `web/backend` directory
5. Custom domain: `api.guindo.me`

**Environment Variables to Set:**
- `GROQ_API_KEY`
- `SERPER_API_KEY`
- `API_SECRET_KEY`
- `ALLOWED_ORIGINS=https://guindo.me`
- `SUPABASE_URL`
- `SUPABASE_KEY`

### Frontend Deployment (guindo.me)

**Recommended: Vercel**

1. Create new project
2. Import from GitHub
3. Set root directory to `web/frontend`
4. Add environment variables in Vercel dashboard
5. Custom domain: `guindo.me`

**Environment Variables to Set:**
- `NEXT_PUBLIC_API_URL=https://api.guindo.me`
- `NEXT_PUBLIC_APP_URL=https://guindo.me`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_WHOP_PLAN_ID`
- `NEXT_PUBLIC_WHOP_CLIENT_ID`
- `WHOP_CLIENT_SECRET`
- `WHOP_API_KEY`

## 📊 Monitoring

### Error Tracking

Install Sentry:

```bash
# Backend
pip install sentry-sdk[fastapi]

# Frontend
npm install @sentry/nextjs
```

Configure in code:

```python
# Backend main.py
import sentry_sdk
sentry_sdk.init(dsn="your_sentry_dsn", environment="production")
```

```typescript
// Frontend next.config.js
const { withSentryConfig } = require("@sentry/nextjs");
```

### API Usage Monitoring

Track GROQ API usage:
- https://console.groq.com/usage

Monitor for:
- Unexpected spikes in usage
- Failed requests
- Rate limit hits

## 🔐 Key Rotation Schedule

- **API Keys**: Rotate every 90 days
- **API Secret**: Rotate every 180 days
- **OAuth Secrets**: Rotate annually

## 📝 Incident Response

If API keys are compromised:

1. **Immediately revoke** compromised keys
2. **Generate new keys** and update production
3. **Review logs** for unauthorized usage
4. **Monitor billing** for unexpected charges
5. **Update incident log** with details and prevention steps

## 🆘 Support

For security issues or questions:
- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Never share API keys in issues or public forums

---

**Last Updated:** 2025-10-27
**Version:** 1.0
