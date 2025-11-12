# 🚀 Guindo Production Deployment Checklist

## ✅ Security Fixes Completed

### Backend Security Enhancements ✅

1. **API Authentication** ✅
   - Added API key verification via `X-API-Key` header
   - Optional in development, required in production
   - Protects `/api/analyze` and `/api/analyze-all` endpoints

2. **Input Validation & Sanitization** ✅
   - Pydantic validators for all user inputs
   - String length limits (2000 chars per field)
   - HTML/code injection character removal (`<>{}`)
   - Age validation (16-100)
   - Required field validation

3. **CORS Configuration** ✅
   - Environment-based allowed origins
   - Restricted HTTP methods (POST, GET, OPTIONS only)
   - Specific headers allowed
   - Production: `ALLOWED_ORIGINS=https://guindo.me`

4. **Rate Limiting** ✅
   - `/api/analyze`: 10 requests/minute per IP
   - `/api/analyze-all`: 3 requests/hour per IP (heavy operation)
   - Automatic 429 responses for rate limit exceeded

5. **Security Headers** ✅
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin
   - Strict-Transport-Security (production only)

## ⚠️ CRITICAL: Actions Required Before Deployment

### 1. Revoke Exposed API Keys (URGENT)

The following API keys in `/web/backend/.env` must be revoked **immediately**:

```bash
GROQ_API_KEY=<YOUR_GROQ_API_KEY_HERE>
SERPER_API_KEY=<YOUR_SERPER_API_KEY_HERE>
```

**Steps:**

1. **Revoke GROQ key:**
   - Visit: https://console.groq.com/keys
   - Delete key ending in `...UY6H`
   - Generate new key
   - Update `.env` locally (never commit!)

2. **Revoke SERPER key:**
   - Visit: https://serper.dev/dashboard
   - Delete key ending in `...7940`
   - Generate new key
   - Update `.env` locally

3. **Generate API Secret:**
   ```bash
   openssl rand -hex 32
   ```
   Add to `.env`:
   ```bash
   API_SECRET_KEY=<generated_secret>
   ```

### 2. Configure Environment Variables

#### Backend Production Environment Variables

Set these in your deployment platform (Railway/Render/Fly.io):

```bash
# Required
GROQ_API_KEY=<new_groq_key>
API_SECRET_KEY=<generated_secret_key>
ENVIRONMENT=production

# CORS
ALLOWED_ORIGINS=https://guindo.me

# Optional
SERPER_API_KEY=<new_serper_key>
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_service_key>
```

#### Frontend Production Environment Variables

Set these in Vercel dashboard:

```bash
# API
NEXT_PUBLIC_API_URL=https://api.guindo.me
NEXT_PUBLIC_APP_URL=https://guindo.me

# Supabase
NEXT_PUBLIC_SUPABASE_URL=<your_supabase_url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your_anon_key>

# Whop
NEXT_PUBLIC_WHOP_PLAN_ID=plan_kY8lADYVlHmhE
NEXT_PUBLIC_WHOP_CLIENT_ID=<your_client_id>
WHOP_CLIENT_SECRET=<your_client_secret>
WHOP_API_KEY=<your_whop_api_key>
```

### 3. Update Frontend API Client

The frontend needs to send the `X-API-Key` header with all API requests.

**File to update:** `/web/frontend/app/dashboard/page.tsx`

Find this section (around line 50-60):

```typescript
const response = await fetch(`${API_URL}/api/analyze-all`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(formData),
})
```

**Change to:**

```typescript
const response = await fetch(`${API_URL}/api/analyze-all`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.NEXT_PUBLIC_API_SECRET || '',  // Add this to .env.local
  },
  body: JSON.stringify(formData),
})
```

Add to `/web/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_SECRET=<same_as_backend_API_SECRET_KEY>
```

⚠️ **Security Note:** While this is client-side visible, it's protected by:
- Rate limiting (3 requests/hour per IP)
- CORS restrictions (only guindo.me allowed)
- Can be rotated if compromised

**Better Alternative (Recommended):** Use Whop authentication to generate short-lived API keys server-side.

## 📋 Pre-Deployment Testing

### Local Testing

1. **Install dependencies:**
   ```bash
   cd web/backend
   pip3 install -r requirements.txt

   cd ../frontend
   npm install
   ```

2. **Generate API secret:**
   ```bash
   openssl rand -hex 32
   ```
   Add to `/web/backend/.env`:
   ```bash
   API_SECRET_KEY=<generated_secret>
   ```

3. **Test backend:**
   ```bash
   cd web/backend
   python3 main.py
   ```
   Should see: "Application startup complete"

4. **Test API with authentication:**
   ```bash
   curl -X POST http://localhost:8000/api/analyze-all \
     -H "Content-Type: application/json" \
     -H "X-API-Key: <your_api_secret>" \
     -d '{"name": "Test", "age": 25, ...}'
   ```

5. **Test rate limiting:**
   Make 11 rapid requests to `/api/analyze` - the 11th should return 429.

6. **Test frontend:**
   ```bash
   cd web/frontend
   npm run dev
   ```
   Visit http://localhost:3000 and test questionnaire flow.

## 🌐 Deployment Steps

### Backend Deployment (api.guindo.me)

**Recommended Platform: Railway**

1. Create Railway account
2. New Project → Deploy from GitHub
3. Select `web/backend` directory
4. Add environment variables (see section 2 above)
5. Deploy
6. Add custom domain: `api.guindo.me`
   - Point A record to Railway IP
   - Wait for SSL certificate

**Alternative: Render/Fly.io** - Similar process

### Frontend Deployment (guindo.me)

**Recommended Platform: Vercel**

1. Import GitHub repository
2. Set root directory: `web/frontend`
3. Framework preset: Next.js
4. Add environment variables (see section 2 above)
5. Deploy
6. Add custom domain: `guindo.me`
   - Point A/CNAME record to Vercel
   - SSL automatic

## 🔍 Post-Deployment Verification

### Backend Health Check

```bash
curl https://api.guindo.me/health
```

Expected response:
```json
{
  "status": "healthy",
  "groq_api_configured": true
}
```

### Frontend Check

Visit: https://guindo.me

Test:
1. Landing page loads
2. Questionnaire flow works
3. Payment page displays
4. All persona cards visible

### API Endpoint Test

```bash
curl -X POST https://api.guindo.me/api/analyze-all \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your_production_key>" \
  -d '{
    "name": "Test User",
    "age": 25,
    "university": "Test University",
    "major": "Computer Science",
    ...
  }'
```

Expected: JSON response with 5 analysis types

### Rate Limiting Test

Make 4 requests within an hour - 4th should return 429:
```json
{
  "detail": "Rate limit exceeded: 3 per 1 hour"
}
```

## 📊 Monitoring Setup

### 1. Error Tracking (Recommended: Sentry)

**Backend:**
```bash
pip3 install sentry-sdk[fastapi]
```

Add to `main.py`:
```python
import sentry_sdk
sentry_sdk.init(
    dsn="your_sentry_dsn",
    environment="production",
    traces_sample_rate=0.1
)
```

**Frontend:**
```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

### 2. API Usage Monitoring

- **GROQ Dashboard:** https://console.groq.com/usage
- **SERPER Dashboard:** https://serper.dev/dashboard

Monitor for:
- Unexpected usage spikes
- Failed requests
- Rate limit hits

### 3. Uptime Monitoring

Use UptimeRobot or similar:
- Monitor `https://api.guindo.me/health`
- Alert on downtime
- Check every 5 minutes

## 🛡️ Security Best Practices

1. **Key Rotation Schedule:**
   - API keys: Every 90 days
   - API Secret: Every 180 days
   - OAuth secrets: Annually

2. **Regular Security Audits:**
   - Monthly dependency updates
   - Quarterly security reviews
   - Test rate limits monthly

3. **Logging:**
   - Enable access logs on hosting platform
   - Review logs weekly for anomalies
   - Set up alerts for 4xx/5xx errors

4. **Backup Strategy:**
   - Database backups (if using Supabase)
   - Environment variable documentation
   - Code in version control (without secrets!)

## 📝 Remaining Tasks (Optional Improvements)

### High Priority

- [ ] **Whop Authentication Integration** - Replace API secret with OAuth flow
- [ ] **Server-side Logging** - Replace print statements with proper logger
- [ ] **Error Boundaries** - Add React error boundaries to frontend

### Medium Priority

- [ ] **Response Caching** - Cache AI responses for common profiles
- [ ] **Analytics** - Add PostHog/Mixpanel for user behavior
- [ ] **Email Notifications** - Send analysis results via email

### Low Priority

- [ ] **Database Integration** - Store user profiles in Supabase
- [ ] **PDF Export** - Generate downloadable PDF reports
- [ ] **Multi-language Support** - Add Turkish translation

## 🆘 Troubleshooting

### "Invalid API key" error

- Verify `X-API-Key` header is being sent
- Check API_SECRET_KEY matches in both frontend and backend
- In development, ensure API_SECRET_KEY is not set (optional mode)

### "Rate limit exceeded" error

- Expected behavior after 3 requests/hour
- Wait 1 hour or deploy with higher limits
- Consider user authentication to increase limits

### CORS errors

- Verify ALLOWED_ORIGINS includes frontend domain
- Check protocol (http vs https)
- Ensure no trailing slashes in origins

### Frontend can't reach backend

- Verify NEXT_PUBLIC_API_URL is correct
- Check backend is running and healthy
- Test with curl first to isolate issue

## 📞 Support

For deployment issues:
- Backend logs: Check Railway/Render dashboard
- Frontend logs: Check Vercel deployment logs
- Browser console: Check for JavaScript errors

---

**Last Updated:** 2025-10-27
**Version:** 1.0
**Status:** Ready for production deployment after completing critical actions above
