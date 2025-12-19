# Multi-stage build for Svelte + Vite frontend

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile --network-timeout 100000

# Copy source code
COPY frontend/src ./src
COPY frontend/index.html ./
COPY frontend/svelte.config.js ./
COPY frontend/tsconfig.json ./
COPY frontend/tsconfig.app.json ./
COPY frontend/vite.config.ts ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Build frontend
RUN yarn build

# Stage 2: Minimal Nginx setup
FROM alpine:3.19

# Install nginx and curl for health checks
RUN apk add --no-cache nginx curl && \
    mkdir -p /run/nginx && \
    mkdir -p /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html /var/lib/nginx /var/log/nginx

# Copy custom nginx config
COPY nginx.conf /etc/nginx/http.d/default.conf

# Copy built frontend from builder stage
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Expose port
EXPOSE 80

# Run as nginx user
USER nginx

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
