# Docker Deployment Guide - PostgreSQL Edition

**Status:** Production-ready for Docker Hub deployment  
**Database:** PostgreSQL 16-alpine (exclusive)  
**No SQLite**, No Hamravesh-specific configs  

---

## 🎯 Quick Start (30 seconds)

### For Local Development

```bash
cp .env.example .env
# Edit .env: Set OPENROUTER_API_KEY, SECRET_KEY, etc.

docker compose up -d
# Backend: http://localhost:8000
# PostgreSQL: localhost:5432
```

### For Production (Docker Hub)

```bash
# 1. Pull image
docker compose pull

# 2. Configure environment
cp .env.example .env
# Edit .env with your production values

# 3. Start services
docker compose up -d

# 4. Run migrations (first time only)
docker compose exec backend python manage.py migrate
```

---

## 📦 Building & Pushing to Docker Hub

### Prerequisites

- Docker installed
- Docker Hub account

### Build Steps

```bash
# 1. Set your Docker Hub username
export DOCKER_USERNAME=your-dockerhub-username

# 2. Build image
docker build -t ${DOCKER_USERNAME}/image_tagging_service:latest .

# 3. Tag versions (optional)
docker tag ${DOCKER_USERNAME}/image_tagging_service:latest ${DOCKER_USERNAME}/image_tagging_service:v1.0.0

# 4. Login
docker login

# 5. Push to Docker Hub
docker push ${DOCKER_USERNAME}/image_tagging_service:latest
docker push ${DOCKER_USERNAME}/image_tagging_service:v1.0.0

# 6. Verify at https://hub.docker.com/r/${DOCKER_USERNAME}/image_tagging_service
```

---

## 🖥️ Server Deployment

### Step 1: Server Prerequisites

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose plugin
sudo apt-get update
sudo apt-get install docker-compose-plugin -y

# Verify
docker --version
docker compose version
```

### Step 2: Clone & Configure

```bash
# Clone repository
git clone https://github.com/parvini82/image_tagging_service.git
cd image_tagging_service

# Create .env from template
cp .env.example .env

# Edit .env (critical values)
cat > .env << 'EOF'
# Django settings
DEBUG=False
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL
DATABASE_URL=postgresql://postgres:YOUR_SECURE_PASSWORD@postgres:5432/image_tagging_db
POSTGRES_DB=image_tagging_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD

# API Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
API_BASE_URL=https://yourdomain.com

# OpenRouter AI
OPENROUTER_API_KEY=your-actual-openrouter-key
OPENROUTER_SITE_URL=https://yourdomain.com
OPENROUTER_SITE_TITLE=Image Tagging Service

# Security (update for HTTPS)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Docker settings
DOCKER_USERNAME=your-dockerhub-username
IMAGE_TAG=latest
EOF
```

### Step 3: Start Services

```bash
# Pull latest image
docker compose pull

# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend
```

### Step 4: Initialize Database

```bash
# Run migrations (first time only)
docker compose exec backend python manage.py migrate

# Create superuser (optional)
docker compose exec backend python manage.py createsuperuser

# Check health
curl http://localhost:8000/api/v1/auth/me/
```

---

## 📋 Configuration Reference

### Required Environment Variables

| Variable | Example | Purpose |
|----------|---------|----------|
| `SECRET_KEY` | Auto-generated | Django security key |
| `DEBUG` | `False` | Production safety |
| `ALLOWED_HOSTS` | `yourdomain.com` | Allowed domains |
| `DATABASE_URL` | `postgresql://...` | PostgreSQL connection |
| `OPENROUTER_API_KEY` | `sk-...` | AI vision model API |

### Optional Environment Variables

| Variable | Default | Purpose |
|----------|---------|----------|
| `SERPAPI_API_KEY` | Empty | Advanced reasoning mode |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `SECURE_SSL_REDIRECT` | `False` | HTTPS enforcement |
| `SECURE_HSTS_SECONDS` | `0` | HSTS header |

### Database Configuration

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB_NAME

Examples:
- Local: postgresql://postgres:postgres@postgres:5432/image_tagging_db
- Remote: postgresql://user:pass@db.example.com:5432/prod_db
```

---

## 🚀 Production Checklist

- [ ] `SECRET_KEY` - Generated strong random value
- [ ] `DEBUG=False` - Never enable in production
- [ ] `POSTGRES_PASSWORD` - Strong unique password
- [ ] `ALLOWED_HOSTS` - Set to actual domain(s)
- [ ] `CORS_ALLOWED_ORIGINS` - Correct frontend URLs
- [ ] `OPENROUTER_API_KEY` - Valid API key configured
- [ ] `SECURE_SSL_REDIRECT=True` - When using HTTPS
- [ ] `SESSION_COOKIE_SECURE=True` - When using HTTPS
- [ ] `CSRF_COOKIE_SECURE=True` - When using HTTPS
- [ ] Database backups configured
- [ ] SSL/TLS certificate installed
- [ ] Firewall rules configured (ports 80, 443)
- [ ] Health checks verified
- [ ] Logs monitored

---

## 🔧 Common Commands

### Monitoring

```bash
# View logs
docker compose logs -f backend
docker compose logs -f postgres

# Check container status
docker compose ps

# Inspect resource usage
docker stats
```

### Database Management

```bash
# Access PostgreSQL CLI
docker compose exec postgres psql -U postgres -d image_tagging_db

# Backup database
docker compose exec postgres pg_dump -U postgres image_tagging_db > backup.sql

# Restore database
cat backup.sql | docker compose exec -T postgres psql -U postgres image_tagging_db

# Show DB size
docker compose exec postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('image_tagging_db'));"
```

### Application Management

```bash
# Django shell
docker compose exec backend python manage.py shell

# Run migrations
docker compose exec backend python manage.py migrate

# Collect static files
docker compose exec backend python manage.py collectstatic --noinput

# Create superuser
docker compose exec backend python manage.py createsuperuser
```

### Maintenance

```bash
# Restart backend
docker compose restart backend

# Restart database
docker compose restart postgres

# Stop all services
docker compose down

# Remove all volumes (WARNING: deletes data)
docker compose down -v

# Update image
docker compose pull
docker compose up -d

# View Docker logs
docker compose logs backend --tail=100
```

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check logs
docker compose logs backend

# Common issues:
# - DATABASE_URL incorrect
# - OPENROUTER_API_KEY missing
# - Migration failed (run: docker compose exec backend python manage.py migrate)
```

### Database connection error

```bash
# Check PostgreSQL is running
docker compose ps postgres

# Check PostgreSQL health
docker compose exec postgres pg_isready -U postgres

# Verify DATABASE_URL format
echo $DATABASE_URL
```

### Health check failing

```bash
# Test health endpoint
curl -v http://localhost:8000/api/v1/auth/me/

# Check backend logs
docker compose logs backend --tail=50
```

### Static files not loading

```bash
# Collect static files
docker compose exec backend python manage.py collectstatic --noinput --clear

# Verify volume
docker volume inspect image_tagging_service_backend_static
```

---

## 📊 Performance Tuning

### Database Connection Pool

```env
# In .env
CONN_MAX_AGE=600  # Connection timeout (seconds)
```

### Gunicorn Workers

```bash
# Formula: (2 × CPU_CORES) + 1
# Edit docker-compose.yml workers setting:
--workers 4  # For 2-core machine
--workers 8  # For 4-core machine
```

### Request Timeout

```env
# For long-running image processing
REQUEST_TIMEOUT=120
```

---

## 🔐 Security Best Practices

1. **Always use HTTPS** in production
2. **Rotate SECRET_KEY** regularly
3. **Use strong PostgreSQL password** (20+ characters)
4. **Keep API keys in .env** (never commit to Git)
5. **Enable SSL redirect** (`SECURE_SSL_REDIRECT=True`)
6. **Set HSTS headers** (`SECURE_HSTS_SECONDS=31536000`)
7. **Restrict CORS origins** to actual frontend URLs
8. **Use environment variables** for all secrets
9. **Keep Docker images updated**
10. **Monitor logs** for suspicious activity

---

## 📚 Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres/)
- [OpenRouter API](https://openrouter.ai/docs)

---

**Last Updated:** December 2025  
**PostgreSQL Version:** 16-alpine  
**Django Version:** 5.0+
