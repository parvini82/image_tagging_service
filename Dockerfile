# Multi-stage build for Node.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package.json frontend/yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source
COPY frontend/src ./src
COPY frontend/svelte.config.js frontend/tsconfig.json frontend/vite.config.ts ./

# Build frontend
RUN yarn build

# Main stage for Python backend + frontend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements
COPY project/backend/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copy backend code
COPY project/backend ./

# Copy built frontend to static files location (optional - for serving)
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/auth/me/', timeout=5)" || exit 1

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "backend.wsgi:application"]
