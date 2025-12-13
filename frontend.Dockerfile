FROM node:18-alpine

WORKDIR /app/frontend

COPY frontend/package.json frontend/yarn.lock* ./

RUN yarn install --frozen-lockfile

COPY frontend/ ./

EXPOSE 5173

CMD ["yarn", "dev", "--host", "0.0.0.0"]
