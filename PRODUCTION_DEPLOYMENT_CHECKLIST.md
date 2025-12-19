# Production Deployment Checklist - PostgreSQL Edition

**Commit Date:** December 19, 2025  
**Status:** ✅ Production Ready  
**Database:** PostgreSQL 16 (exclusive)  
**Deployment Method:** Docker Hub + Docker Compose  

---

## 📋 Pre-Deployment Tasks

### Code Changes

- [x] **settings.py** - PostgreSQL-only configuration
  - Removed SQLite support
  - Environment-based configuration
  - Added logging configuration
  - Security settings for production

- [x] **.env.example** - PostgreSQL-only template
  - PostgreSQL connection string format
  - All required environment variables
  - Removed SQLite options
  - Clear documentation

- [x] **docker-compose.yml** - Production setup
  - PostgreSQL service (required)
  - Backend service with environment variables
  - Health checks for both services
  - Persistent volumes for data
  - Network isolation

- [x] **Dockerfile** - Production image
  - Multi-stage build (Node + Python)
  - Non-root user execution
  - Health checks
  - Gunicorn 4 workers
  - Security hardening

- [x] **requirements.txt** - Dependencies
  - Added `dj-database-url>=2.0.0`
  - PostgreSQL adapter included
  - All AI/ML dependencies

### Documentation

- [x] **DOCKER_DEPLOYMENT_GUIDE.md** - Complete deployment guide
  - Quick start (30 seconds)
  - Build & push to Docker Hub
  - Server deployment steps
  - Configuration reference
  - Troubleshooting guide
  - Security best practices
  - Common commands

- [x] **DOCKER_HUB_README.md** - Docker Hub presentation
  - What is the service
  - Quick start
  - Environment configuration
  - API endpoints
  - Docker Compose services
  - Deployment scenarios

- [x] **scripts/docker-build-push.sh** - Build automation
  - Automated Docker build
  - Push to Docker Hub
  - Version tagging
  - Verification steps

---

## 🔄 Changes Summary

### Database Migration

**Before:** SQLite + PostgreSQL optional  
**After:** PostgreSQL exclusive (production requirement)

### Configuration

**Before:** Hardcoded settings  
**After:** 100% environment-based configuration

### Deployment Platform

**Before:** Hamravesh-specific
**After:** Generic Docker Hub + Docker Compose (platform-agnostic)

---

## 🚀 Deployment Steps

### Step 1: Build Docker Image

```bash
# Option A: Using helper script (recommended)
bash scripts/docker-build-push.sh v1.0.0

# Option B: Manual build
export DOCKER_USERNAME=your-username
docker build -t ${DOCKER_USERNAME}/image_tagging_service:latest .
docker login
docker push ${DOCKER_USERNAME}/image_tagging_service:latest
```

### Step 2: Deploy on Server

```bash
# Clone repository
git clone https://github.com/parvini82/image_tagging_service.git
cd image_tagging_service

# Configure environment
cp .env.example .env
# Edit .env with production values

# Start services
docker compose pull
docker compose up -d

# Initialize database
docker compose exec backend python manage.py migrate
```

### Step 3: Verify Deployment

```bash
# Check services
docker compose ps

# Check health
curl http://localhost:8000/api/v1/auth/me/

# View logs
docker compose logs -f backend
```

---

## ✅ Production Verification Checklist

### Backend Service

- [ ] Container is running
  ```bash
  docker compose ps | grep backend
  ```

- [ ] Health check passing
  ```bash
  curl -v http://localhost:8000/api/v1/auth/me/
  ```

- [ ] No errors in logs
  ```bash
  docker compose logs backend | grep ERROR
  ```

- [ ] API endpoints responding
  ```bash
  curl http://localhost:8000/api/v1/
  ```

### PostgreSQL Service

- [ ] Container is running
  ```bash
  docker compose ps | grep postgres
  ```

- [ ] Health check passing
  ```bash
  docker compose exec postgres pg_isready -U postgres
  ```

- [ ] Database created
  ```bash
  docker compose exec postgres psql -U postgres -l | grep image_tagging_db
  ```

- [ ] Tables created
  ```bash
  docker compose exec postgres psql -U postgres -d image_tagging_db -c "\dt"
  ```

### Environment Configuration

- [ ] `.env` file present
  ```bash
  ls -la .env
  ```

- [ ] All required variables set
  ```bash
  grep -E '^(DEBUG|SECRET_KEY|OPENROUTER_API_KEY|POSTGRES_PASSWORD)=' .env
  ```

- [ ] SECRET_KEY is strong (not default)
  ```bash
  grep SECRET_KEY .env | grep -v 'change-in-production'
  ```

- [ ] DEBUG is False
  ```bash
  grep 'DEBUG=False' .env
  ```

### Data Persistence

- [ ] PostgreSQL volume exists
  ```bash
  docker volume ls | grep postgres_data
  ```

- [ ] Static files volume exists
  ```bash
  docker volume ls | grep backend_static
  ```

- [ ] Logs volume exists
  ```bash
  docker volume ls | grep backend_logs
  ```

### Security

- [ ] `.env` file in `.gitignore`
  ```bash
  grep '.env' .gitignore
  ```

- [ ] No Hamravesh files in repo
  ```bash
  git ls-files | grep -i hamravesh
  ```

- [ ] SSL/TLS configured (if using HTTPS)
  ```bash
  grep 'SECURE_SSL_REDIRECT=True' .env
  ```

---

## 🔐 Security Hardening

### Immediate Actions

- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] Set strong POSTGRES_PASSWORD (20+ characters)
- [ ] Restrict ALLOWED_HOSTS to actual domain
- [ ] Set CORS_ALLOWED_ORIGINS to frontend domain only

### HTTPS Setup

- [ ] Install SSL certificate (Let's Encrypt)
  ```bash
  sudo apt-get install certbot python3-certbot-nginx -y
  sudo certbot certonly --standalone -d yourdomain.com
  ```

- [ ] Enable SSL redirect
  ```env
  SECURE_SSL_REDIRECT=True
  SESSION_COOKIE_SECURE=True
  CSRF_COOKIE_SECURE=True
  ```

- [ ] Enable HSTS
  ```env
  SECURE_HSTS_SECONDS=31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS=True
  SECURE_HSTS_PRELOAD=True
  ```

### API Key Security

- [ ] OpenRouter API key stored in `.env`
- [ ] `.env` never committed to Git
- [ ] API key rotated regularly
- [ ] API key permissions restricted on OpenRouter

### Database Security

- [ ] Strong PostgreSQL password
- [ ] Database user has minimal required permissions
- [ ] Backups scheduled and tested
- [ ] Backups encrypted and stored securely

---

## 📊 Monitoring & Maintenance

### Daily Checks

```bash
# Check container health
docker compose ps

# View recent logs
docker compose logs --tail=50 backend

# Monitor resource usage
docker stats
```

### Weekly Tasks

```bash
# Check for updates
docker compose pull

# Backup database
docker compose exec postgres pg_dump -U postgres image_tagging_db > backup-$(date +%Y%m%d).sql

# Clean up old logs
docker exec image_tagging_backend sh -c 'find /app/logs -type f -mtime +30 -delete'
```

### Monthly Tasks

- [ ] Review security logs
- [ ] Test database restore
- [ ] Update Docker base images
- [ ] Review API usage and rate limiting
- [ ] Check disk space usage
- [ ] Review error logs for patterns

---

## 📝 Important Configuration Reference

### DATABASE_URL Format

```
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME

Local Example:
postgresql://postgres:password@postgres:5432/image_tagging_db

Remote Example:
postgresql://user:pass@db.example.com:5432/prod_db
```

### Environment Variables

**Required:**
- `DEBUG=False`
- `SECRET_KEY` (generated)
- `DATABASE_URL` (PostgreSQL)
- `ALLOWED_HOSTS` (your domain)
- `OPENROUTER_API_KEY`

**Optional:**
- `SERPAPI_API_KEY` (for advanced mode)
- `LOG_LEVEL` (default: INFO)
- `REQUEST_TIMEOUT` (default: 120)

---

## 🆘 Rollback Plan

If issues occur after deployment:

```bash
# 1. Stop services
docker compose down

# 2. Restore backup (if needed)
cat backup.sql | docker compose exec -T postgres psql -U postgres image_tagging_db

# 3. Restart services
docker compose up -d

# 4. Check status
docker compose ps
```

---

## 📞 Support Resources

- **Deployment Guide:** [DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)
- **Docker Hub README:** [DOCKER_HUB_README.md](./DOCKER_HUB_README.md)
- **GitHub Issues:** [Report Bug](https://github.com/parvini82/image_tagging_service/issues)
- **Docker Docs:** [https://docs.docker.com](https://docs.docker.com)
- **Django Docs:** [https://docs.djangoproject.com](https://docs.djangoproject.com)

---

## ✨ Summary

✅ **Status:** Production Ready  
✅ **Database:** PostgreSQL Only  
✅ **Platform:** Docker Hub + Docker Compose  
✅ **Configuration:** 100% Environment-based  
✅ **Security:** Hardened & Best Practices  
✅ **Documentation:** Comprehensive  

**Ready for deployment on any Linux server with Docker!**

---

**Last Updated:** December 19, 2025  
**Version:** 1.0.0  
**Maintainer:** Mohammad Hosein Parvini
