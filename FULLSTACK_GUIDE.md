# Full-Stack Image Tagging Service - Complete Guide

**Status:** ✅ Production Ready  
**Components:** Frontend (Svelte) + Backend (Django) + Database (PostgreSQL)  
**All Containerized with Docker Compose**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Port 80)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Svelte Frontend (Built with Vite)              │   │
│  │  - Responsive UI with Tailwind CSS              │   │
│  │  - Image upload and tagging                     │   │
│  │  - Results display                              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓ (reverse proxy)
┌─────────────────────────────────────────────────────────┐
│              Django REST API (Port 8000)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Image Processing                               │   │
│  │  - OpenRouter AI Vision Models                  │   │
│  │  - LangGraph for reasoning                      │   │
│  │  - Tag generation and validation                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│           PostgreSQL Database (Port 5432)               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  - User accounts                                │   │
│  │  - Image metadata                               │   │
│  │  - Tagging results                              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (for Mac/Windows)
- Docker Engine + Docker Compose (for Linux)
- Git

### 1. Clone & Configure

```bash
# Clone repository
git clone https://github.com/parvini82/image_tagging_service.git
cd image_tagging_service

# Create .env file
cp .env.example .env

# Edit .env with your settings (important!)
```

**Critical .env values to set:**

```env
DEBUG=False
SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
OPENROUTER_API_KEY=<your-actual-key>
POSTGRES_PASSWORD=<strong-password>
```

### 2. Start All Services

```bash
# Build and start
docker compose up -d

# Check status
docker compose ps

# Should show 3 running containers:
# - image_tagging_frontend (nginx)
# - image_tagging_backend (django)
# - image_tagging_db (postgres)
```

### 3. Initialize Database

```bash
# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser (optional)
docker compose exec backend python manage.py createsuperuser
```

### 4. Access Application

```
Frontend:  http://localhost
Backend:   http://localhost:8000
Admin:     http://localhost/admin
API:       http://localhost/api/v1
```

---

## 📦 Services

### Frontend (Nginx + Svelte)

- **Port:** 80
- **Built with:** Vite + Svelte + TailwindCSS
- **Features:**
  - Image upload interface
  - Real-time tagging
  - Results display
  - Responsive design

### Backend (Django REST API)

- **Port:** 8000
- **Features:**
  - RESTful API endpoints
  - Authentication & authorization
  - Image processing with OpenRouter
  - LangGraph integration for reasoning
  - PostgreSQL persistence

### Database (PostgreSQL)

- **Port:** 5432 (internal only)
- **Version:** 16-alpine
- **Data:** Persistent volume

---

## 🔧 Common Tasks

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
```

### Backend Management

```bash
# Django shell
docker compose exec backend python manage.py shell

# Collect static files
docker compose exec backend python manage.py collectstatic --noinput

# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser
```

### Database Access

```bash
# PostgreSQL CLI
docker compose exec postgres psql -U postgres -d image_tagging_db

# Backup database
docker compose exec postgres pg_dump -U postgres image_tagging_db > backup.sql

# Restore database
cat backup.sql | docker compose exec -T postgres psql -U postgres image_tagging_db
```

### Frontend Development

```bash
# Development server (local only, for debugging)
cd frontend
npm install
npm run dev

# Build for production (done in Docker automatically)
npm run build
```

### Service Management

```bash
# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v

# Restart specific service
docker compose restart backend

# Restart all services
docker compose restart

# Rebuild images
docker compose build --no-cache

# Update and restart
docker compose pull
docker compose up -d
```

---

## 🌐 API Endpoints

### Authentication

```bash
# Check auth status
curl http://localhost/api/v1/auth/me/

# Login
curl -X POST http://localhost/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Logout
curl -X POST http://localhost/api/v1/auth/logout/
```

### Image Tagging

```bash
# Tag image from URL
curl -X POST http://localhost/api/v1/fashion-tagger/tag-from-url/ \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "mode": "fast"
  }'

# Tag image from file upload
curl -X POST http://localhost/api/v1/fashion-tagger/tag-image/ \
  -F "image=@/path/to/image.jpg" \
  -F "mode=fast"

# Get tagging results
curl http://localhost/api/v1/fashion-tagger/results/
```

---

## 🔐 Security

### Development

```env
DEBUG=True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Production

```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Best Practices

1. **Always use strong SECRET_KEY**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Never commit .env to Git**
   - It's already in .gitignore

3. **Rotate API keys regularly**
   - OpenRouter API key
   - Django SECRET_KEY

4. **Use HTTPS in production**
   - Set SECURE_SSL_REDIRECT=True
   - Configure SSL certificate

---

## 📊 Monitoring

### Health Checks

```bash
# Frontend health
curl http://localhost/health

# Backend health
curl http://localhost:8000/admin/login/

# Database health
docker compose exec postgres pg_isready -U postgres
```

### Container Status

```bash
# View running containers
docker compose ps

# View resource usage
docker stats

# View container details
docker inspect <container-id>
```

---

## 🚢 Deployment

### Docker Hub

```bash
# Build for production
bash scripts/docker-build-push.sh v1.0.0

# Or manually
export DOCKER_USERNAME=your-username
docker build -t ${DOCKER_USERNAME}/image_tagging_service:latest .
docker push ${DOCKER_USERNAME}/image_tagging_service:latest
```

### Server Deployment

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Clone repository
git clone https://github.com/parvini82/image_tagging_service.git
cd image_tagging_service

# 3. Configure environment
cp .env.example .env
# Edit .env with production values

# 4. Start services
docker compose pull
docker compose up -d

# 5. Run migrations
docker compose exec backend python manage.py migrate
```

### SSL/TLS Setup

```bash
# Using Let's Encrypt with Certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx.conf to use SSL
# Add to docker-compose.yml volumes:
# - /etc/letsencrypt:/etc/letsencrypt:ro
```

---

## 🐛 Troubleshooting

### Frontend not loading

```bash
# Check logs
docker compose logs frontend

# Verify nginx is running
docker compose exec frontend nginx -t

# Rebuild frontend
docker compose build --no-cache frontend
docker compose up -d frontend
```

### Backend API errors

```bash
# Check backend logs
docker compose logs backend

# Check migrations
docker compose exec backend python manage.py migrate --check

# Run migrations
docker compose exec backend python manage.py migrate
```

### Database connection error

```bash
# Check PostgreSQL health
docker compose exec postgres pg_isready -U postgres

# Check database exists
docker compose exec postgres psql -U postgres -l | grep image_tagging_db

# Verify DATABASE_URL format
echo $DATABASE_URL
```

### Port conflicts

```bash
# Check which process is using port
lsof -i :80      # Frontend
lsof -i :8000    # Backend
lsof -i :5432    # Database

# Kill process if needed
kill -9 <PID>
```

---

## 📚 Documentation

- **Deployment:** [DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)
- **Checklist:** [PRODUCTION_DEPLOYMENT_CHECKLIST.md](./PRODUCTION_DEPLOYMENT_CHECKLIST.md)
- **Migration:** [MIGRATION_SUMMARY.md](./MIGRATION_SUMMARY.md)
- **Docker Hub:** [DOCKER_HUB_README.md](./DOCKER_HUB_README.md)

---

## 📞 Support

- **GitHub Issues:** [Report Bug](https://github.com/parvini82/image_tagging_service/issues)
- **Nginx Docs:** https://nginx.org/en/docs/
- **Svelte Docs:** https://svelte.dev/docs
- **Django Docs:** https://docs.djangoproject.com/
- **Docker Docs:** https://docs.docker.com/

---

## ✨ Key Features

✅ **Full-Stack Application**
- Frontend: Responsive Svelte UI
- Backend: Django REST API
- Database: PostgreSQL

✅ **Containerized**
- Docker Compose orchestration
- Production-ready images
- Easy deployment

✅ **AI-Powered**
- OpenRouter vision models
- LangGraph reasoning
- Multiple tagging modes

✅ **Production Ready**
- Security hardened
- Health checks
- Logging and monitoring
- Persistent storage

---

**Last Updated:** December 19, 2025  
**Version:** 1.0.0  
**Status:** 🚀 Ready for Production
