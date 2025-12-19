# Simple production build - serve with Node.js
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/yarn.lock* ./

# Install dependencies (including serve for production)
RUN yarn install --frozen-lockfile --network-timeout 100000 && \
    yarn global add serve

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

# Expose port
EXPOSE 80

# Serve built files with serve package
CMD ["serve", "-s", "dist", "-l", "80"]
