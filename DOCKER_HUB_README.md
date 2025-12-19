# Image Tagging Service - Docker Hub Edition

**Production-Ready Docker Image for AI-Powered Fashion Item Image Tagging**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0-darkgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 🎨 What is Image Tagging Service?

A powerful AI-driven image tagging service that automatically analyzes images and generates descriptive tags using:

- **LangGraph** - Multi-agent orchestration for complex reasoning
- **OpenRouter API** - Access to state-of-the-art vision models (Gemini, Qwen, etc.)
- **PostgreSQL** - Robust, production-grade database
- **Django REST API** - RESTful backend with authentication
- **Svelte Frontend** - Modern, responsive UI

### Key Features

✅ **Three Tagging Modes:**
- **Fast** - Quick tagging with `gemini-2.5-flash-lite`
- **Reasoning** - Enhanced analysis with `nemotron-nano-12b-v2-vl`
- **Advanced Reasoning** - Deep analysis with `qwen2.5-vl-32b-instruct` + SerpAPI

✅ **Production Ready:**
- PostgreSQL database (no SQLite)
- Environment-based configuration
- Health checks and logging
- Non-root user execution
- Gunicorn + 4 workers

✅ **Scalable:**
- Docker containerized
- Docker Compose orchestration
- Connection pooling
- Worker-based request handling

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh | sudo sh
sudo apt-get install docker-compose-plugin -y
```

### 2. Get Configuration

```bash
# Clone and configure
git clone https://github.com/parvini82/image_tagging_service.git
cd image_tagging_service

cp .env.example .env
# Edit .env with your values
```

### 3. Start Services

```bash
# Pull latest image
docker compose pull

# Start all services
docker compose up -d

# Run migrations
docker compose exec backend python manage.py migrate
```

### 4. Access Application

- **Backend API:** `http://localhost:8000`
- **Health Check:** `curl http://localhost:8000/api/v1/auth/me/`
- **Database:** `postgresql://postgres:postgres@localhost:5432/image_tagging_db`

---

## 💳 Environment Configuration

### Required Variables

```env
# Django
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:PASSWORD@postgres:5432/image_tagging_db
POSTGRES_PASSWORD=your_secure_password

# API
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# OpenRouter AI
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_SITE_URL=https://yourdomain.com
OPENROUTER_SITE_TITLE=Image Tagging Service
```

### Optional Variables

```env
# Advanced reasoning mode only
SERPAPI_API_KEY=your-serpapi-key

# Timeouts and performance
REQUEST_TIMEOUT=120
CONN_MAX_AGE=600
```

---

## 📋 API Endpoints

### Authentication

```bash
# Check auth status
curl http://localhost:8000/api/v1/auth/me/

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### Image Tagging

```bash
# Tag image by URL
curl -X POST http://localhost:8000/api/v1/fashion-tagger/tag-from-url/ \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg", "mode": "fast"}'

# Tag image by file upload
curl -X POST http://localhost:8000/api/v1/fashion-tagger/tag-image/ \
  -F "image=@/path/to/image.jpg" \
  -F "mode=fast"
```

---

## 📋 Docker Compose Services

### Backend Service

- **Image:** `${DOCKER_USERNAME}/image_tagging_service:latest`
- **Port:** `8000`
- **Depends on:** PostgreSQL
- **Health check:** HTTP endpoint `/api/v1/auth/me/`
- **Workers:** 4 (adjustable)

### PostgreSQL Service

- **Image:** `postgres:16-alpine`
- **Port:** `5432`
- **Volume:** `postgres_data` (persistent)
- **Health check:** `pg_isready`

---

## 🚠 Deployment Scenarios

### Local Development

```bash
docker compose up -d
# Frontend: http://localhost:5173 (dev server included)
# Backend: http://localhost:8000
```

### Production on VPS

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production values

# 2. Pull pre-built image from Docker Hub
docker compose pull

# 3. Start services
docker compose up -d

# 4. Initialize database
docker compose exec backend python manage.py migrate
```

### With SSL/TLS (Nginx reverse proxy)

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
```

---

## 📊 Common Tasks

### View Logs

```bash
docker compose logs -f backend          # Backend logs
docker compose logs -f postgres         # Database logs
```

### Database Backup

```bash
docker compose exec postgres pg_dump -U postgres image_tagging_db > backup.sql
```

### Database Restore

```bash
cat backup.sql | docker compose exec -T postgres psql -U postgres image_tagging_db
```

### Create Admin User

```bash
docker compose exec backend python manage.py createsuperuser
```

### Run Django Management Commands

```bash
docker compose exec backend python manage.py <command>
```

---

## 🔐 Security Best Practices

1. **Always use strong SECRET_KEY**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Enable SSL redirect in production**
   ```env
   SECURE_SSL_REDIRECT=True
   SECURE_HSTS_SECONDS=31536000
   ```

3. **Use environment variables for secrets**
   - Never commit `.env` to Git
   - Use `.gitignore` for `.env`

4. **Keep container images updated**
   ```bash
   docker compose pull
   docker compose up -d
   ```

5. **Monitor logs for errors**
   ```bash
   docker compose logs backend | grep ERROR
   ```

---

## 🚧 Troubleshooting

### Backend not starting

```bash
# Check logs
docker compose logs backend --tail=50

# Verify DATABASE_URL format
echo $DATABASE_URL

# Check PostgreSQL connection
docker compose exec postgres pg_isready -U postgres
```

### Health check failing

```bash
# Test health endpoint
curl -v http://localhost:8000/api/v1/auth/me/

# Check migrations
docker compose exec backend python manage.py migrate --check
```

### Static files not loading

```bash
docker compose exec backend python manage.py collectstatic --noinput --clear
```

---

## 📄 Technology Stack

| Component | Version |
|-----------|----------|
| Python | 3.11 |
| Django | 5.0+ |
| PostgreSQL | 16 |
| Node.js | 18 |
| Svelte | Latest |
| Docker | 20+ |
| Docker Compose | 2.0+ |

---

## 🔗 Links

- **GitHub:** [parvini82/image_tagging_service](https://github.com/parvini82/image_tagging_service)
- **Deployment Guide:** [DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)
- **OpenRouter API:** [https://openrouter.ai](https://openrouter.ai)
- **Django Docs:** [https://docs.djangoproject.com](https://docs.djangoproject.com)
- **Docker Docs:** [https://docs.docker.com](https://docs.docker.com)

---

## 📟 License

MIT License - See LICENSE file for details

---

## 🍐 Support

For issues and questions:
- **GitHub Issues:** [Report Bug](https://github.com/parvini82/image_tagging_service/issues)
- **Deployment Help:** See `DOCKER_DEPLOYMENT_GUIDE.md`
- **API Docs:** Available at `http://localhost:8000/api/v1/`

---

**Last Updated:** December 2025  
**PostgreSQL Only** | **Production Ready** | **Docker Hub Ready**
