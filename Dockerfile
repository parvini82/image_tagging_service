# Multi-stage build for Node.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile --network-timeout 100000

# Copy frontend source files
COPY frontend/src ./src
COPY frontend/index.html ./
COPY frontend/svelte.config.js ./
COPY frontend/tsconfig.json ./
COPY frontend/tsconfig.app.json ./
COPY frontend/vite.config.ts ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Build frontend with optimizations
RUN yarn build

# ============================================
# Main stage for Python backend + frontend
# ============================================
FROM python:3.11-slim

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements
COPY requirements.txt .

# Install Python dependencies with production optimizations
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install gunicorn psycopg2-binary

# Copy backend code
COPY project/backend ./

# Copy built frontend to static files location
COPY --from=frontend-builder /app/frontend/dist ./static/frontend_dist

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs /app/media && \
    chmod -R 755 /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/auth/me/ || exit 1

# Expose port
EXPOSE 8000

# Run gunicorn with production settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "backend.wsgi:application"]
