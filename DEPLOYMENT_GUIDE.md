# 🚀 FIRE Planning System - Deployment Guide

Bu dokümanda sistemin nasıl çalıştırılacağını ve deploy edileceğini bulacaksın.

## 📋 İçindekiler

1. [Yerel Geliştirme](#yerel-geliştirme)
2. [Production Deployment](#production-deployment)
3. [Önerilen Stack](#önerilen-stack)

---

## 🏠 Yerel Geliştirme

### Hızlı Başlangıç (Tek Komut)

```bash
cd web
./start.sh
```

Bu script:
- ✅ Backend ve frontend'i otomatik kurar
- ✅ Her iki serveri başlatır
- ✅ Log dosyalarını takip eder
- ✅ Ctrl+C ile her ikisini de kapatır

### Manuel Başlatma

#### 1. Backend

```bash
cd web/backend

# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# .env oluştur (GROQ_API_KEY gerekli)
cp ../../.env .env

# Başlat
python main.py
```

Backend: `http://localhost:8000`

#### 2. Frontend

```bash
cd web/frontend

# Dependencies
npm install

# .env.local oluştur
cp .env.example .env.local

# Başlat
npm run dev
```

Frontend: `http://localhost:3000`

---

## 🌍 Production Deployment

### Option 1: Vercel (Frontend) + Railway (Backend)

**En Kolay ve Hızlı Seçenek** ⭐

#### Backend → Railway

1. [Railway](https://railway.app) hesabı oluştur
2. New Project → Deploy from GitHub
3. `web/backend` klasörünü seç
4. Environment Variables:
   ```
   GROQ_API_KEY=your_key_here
   PORT=8000
   ```
5. Deploy!

Railway otomatik URL verecek: `https://your-app.railway.app`

#### Frontend → Vercel

1. [Vercel](https://vercel.com) hesabı oluştur
2. New Project → Import Git Repository
3. Root Directory: `web/frontend`
4. Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
5. Deploy!

Vercel otomatik domain verecek: `https://your-app.vercel.app`

**Toplam Maliyet**: $0 (hobby tier limits dahilinde)

---

### Option 2: Full Stack Hosting

#### Render.com (Tek Platform)

**Backend**:
- New Web Service
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment: `GROQ_API_KEY`

**Frontend**:
- New Static Site
- Build Command: `npm install && npm run build`
- Publish Directory: `out`
- Environment: `NEXT_PUBLIC_API_URL`

---

### Option 3: VPS (DigitalOcean/Hetzner)

**En Ucuz Uzun Vadeli Seçenek**

```bash
# VPS'e bağlan
ssh root@your-vps-ip

# Update sistem
apt update && apt upgrade -y

# Python & Node
apt install python3 python3-venv nodejs npm nginx -y

# Repo clone
git clone your-repo
cd crewai_orchestration/web

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# systemd service (backend)
sudo nano /etc/systemd/system/fire-backend.service
```

**fire-backend.service**:
```ini
[Unit]
Description=FIRE Planning Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/root/crewai_orchestration/web/backend
Environment="PATH=/root/crewai_orchestration/web/backend/venv/bin"
Environment="GROQ_API_KEY=your_key"
ExecStart=/root/crewai_orchestration/web/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Frontend setup
cd ../frontend
npm install
npm run build

# Nginx config
sudo nano /etc/nginx/sites-available/fire-planner
```

**fire-planner nginx config**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable & start
sudo ln -s /etc/nginx/sites-available/fire-planner /etc/nginx/sites-enabled/
sudo systemctl enable fire-backend
sudo systemctl start fire-backend
sudo systemctl restart nginx

# SSL (optional but recommended)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

**Maliyet**: ~$5-10/month (Hetzner CPX11)

---

### Option 4: Docker (Her Yerde Çalışır)

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
```

**backend/Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**frontend/Dockerfile**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Deploy
docker-compose up -d
```

---

## 💰 Maliyet Karşılaştırması

| Platform | Maliyet | Kolay | Performans | Önerilen |
|----------|---------|-------|------------|----------|
| Vercel + Railway | $0 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Başlangıç |
| Render.com | $0-7/mo | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Orta |
| VPS (Hetzner) | $5/mo | ⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Uzun vade |
| AWS/GCP | $10+/mo | ⭐ | ⭐⭐⭐⭐⭐ | Enterprise |

---

## 🔐 Güvenlik Checklist

- [ ] `.env` dosyası `.gitignore`'da
- [ ] CORS sadece production domain'e izin veriyor
- [ ] HTTPS kullanılıyor (SSL sertifikası)
- [ ] API rate limiting eklenmiş (optional)
- [ ] Input validation aktif
- [ ] GROQ API key güvenli

---

## 📊 Monitoring

### Free Options:
- **UptimeRobot**: Uptime monitoring
- **LogRocket**: Frontend errors
- **Sentry**: Backend errors

### Logs:
```bash
# Railway: Dashboard → Logs
# Vercel: Dashboard → Deployments → Logs
# VPS: journalctl -u fire-backend -f
```

---

## 🚨 Troubleshooting

### CORS Error
Frontend .env.local'de `NEXT_PUBLIC_API_URL` doğru mu?
Backend CORS settings frontend URL'ini içeriyor mu?

### 500 Error
Backend logs kontrol et. GROQ_API_KEY geçerli mi?

### Slow Responses
Groq API ilk çağrıda yavaş olabilir (cold start).
Sonraki çağrılarda çok hızlı.

---

## 📈 Scaling

### Traffic Artınca:
1. **Backend**: Railway autoscaling veya VPS upgrade
2. **Frontend**: Vercel otomatik scale eder
3. **Database**: Eğer eklerseniz, Supabase/PlanetScale

### AI Costs:
Groq şu an ücretsiz ama production'da:
- Rate limiting ekle
- Caching düşün (aynı profile için)
- Alternative: OpenAI API (daha pahalı ama daha güvenilir)

---

## 🎉 İlk Deployment'tan Sonra

1. ✅ Test et - Tüm flow'u baştan sona dene
2. ✅ Analytics ekle - Vercel Analytics (ücretsiz)
3. ✅ SEO optimize et - Meta tags, sitemap
4. ✅ Social share - OG images ekle
5. ✅ Domain bağla - Kendi domain'ini kullan

---

**Başarılar! 🚀**

Sorular için: GitHub Issues veya Discord
