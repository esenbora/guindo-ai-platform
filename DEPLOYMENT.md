# 🚀 guindo.me Deployment Guide

This guide covers deploying the Guindo AI Career Planning application to production.

## Architecture Overview

```
guindo.me (Vercel Frontend) → api.guindo.me (Railway Backend) → Groq AI API
```

## Prerequisites

### Required Accounts
- [Vercel Account](https://vercel.com) (for frontend)
- [Railway Account](https://railway.app) (for backend)
- [Domain Name] (guindo.me already purchased)

### Required Tools
```bash
# Install Node.js and npm (if not already installed)
# Install Python 3.11 (already done)

# Install deployment tools
npm install -g vercel
npm install -g @railway/cli
```

## Environment Variables

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://api.guindo.me
NEXT_PUBLIC_WHOP_CLIENT_ID=your_whop_client_id
```

### Backend (Railway)
```env
GROQ_API_KEY=your_production_groq_key
SERPER_API_KEY=your_production_serper_key
API_SECRET_KEY=your_secure_random_secret
ENVIRONMENT=production
ALLOWED_ORIGINS=https://guindo.me,https://www.guindo.me
```

## Quick Deployment

### Option 1: Automated Script
```bash
./deploy.sh
```

### Option 2: Manual Deployment

#### Frontend (Vercel)
```bash
cd web/frontend
npm install
npm run build
vercel --prod
```

#### Backend (Railway)
```bash
cd web/backend
python3.11 -m pip install -r requirements.txt
railway login
railway init
railway up
```

## DNS Configuration

### Step 1: Point Domain to Vercel
1. Go to your domain registrar (where you bought guindo.me)
2. Update nameservers to Vercel's nameservers:
   - `ns1.vercel-dns.com`
   - `ns2.vercel-dns.com`
   - `ns3.vercel-dns.com`

### Step 2: Configure API Subdomain
Create a CNAME record:
```
api.guindo.me → your-railway-app.railway.app
```

## Configuration Files

### Frontend Configuration
- `web/frontend/vercel.json` - Vercel deployment settings
- `web/frontend/next.config.js` - Next.js configuration

### Backend Configuration
- `web/backend/railway.toml` - Railway deployment settings
- `web/backend/Dockerfile` - Container configuration
- `web/backend/requirements.txt` - Python dependencies

## Security Considerations

### API Security
- Rate limiting implemented (10 requests/minute)
- API key authentication required
- CORS configured for production domains
- Input validation and sanitization

### Environment Security
- All secrets stored in environment variables
- No hardcoded API keys in source code
- Production secrets separate from development

## Monitoring & Maintenance

### Health Checks
- Frontend: Vercel Analytics
- Backend: `/health` endpoint monitored by Railway
- API: Groq API usage monitoring

### Logging
- Application logs available in Railway dashboard
- Error tracking ready for Sentry integration
- Performance monitoring via Vercel Analytics

## Troubleshooting

### Common Issues

#### Frontend Deployment Issues
```bash
# Clear Next.js cache
rm -rf .next
npm run build

# Check environment variables
vercel env ls
```

#### Backend Deployment Issues
```bash
# Check Railway logs
railway logs

# Restart service
railway restart
```

#### DNS Propagation Issues
```bash
# Check DNS propagation
dig guindo.me
dig api.guindo.me
```

### Performance Issues
- Check Vercel Analytics for frontend performance
- Monitor Railway resource usage
- Review API response times
- Check Groq API rate limits

## Scaling Considerations

### Frontend Scaling
- Vercel automatically scales globally
- Edge caching configured
- CDN included

### Backend Scaling
- Railway auto-scales based on load
- Consider database for persistent storage
- Implement caching for API responses

## Cost Analysis

### Monthly Costs (Estimate)
- Vercel Pro: $20/month
- Railway: $5-20/month (depending on usage)
- Domain: $12/year
- Groq API: $20-50/month (depending on usage)
- **Total**: ~$45-90/month

## Backup & Recovery

### Data Backup
- User data stored in Supabase (if implemented)
- Regular database backups
- Configuration version controlled

### Disaster Recovery
- Multi-region deployment possible
- Automated rollback capabilities
- Monitoring and alerting setup

## Support & Maintenance

### Regular Tasks
- Monitor API usage and costs
- Update dependencies regularly
- Review security advisories
- Backup configuration

### Emergency Contacts
- Vercel Support: https://vercel.com/support
- Railway Support: https://railway.app/support
- Domain Registrar Support

## Next Steps

1. **Initial Deployment**: Follow the steps above
2. **Testing**: Thoroughly test all functionality
3. **Monitoring**: Set up alerts and monitoring
4. **Optimization**: Optimize based on usage patterns
5. **Scaling**: Scale as user base grows

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)