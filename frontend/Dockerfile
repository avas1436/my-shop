# Dockerfile

# ===== Base =====
FROM node:20-slim AS base

WORKDIR /frontend

ENV NODE_ENV=production

COPY package.json package-lock.json ./

RUN npm ci --no-audit --omit=dev --no-fund


# ===== Build Stage =====
FROM base AS Build

WORKDIR /frontend

COPY . .

ENV VITE_ENV=production

RUN npm run build --if-present --max-old-space-size=4096
RUN npm cache clean --force


# ===== Final Stage =====
FROM caddy:2-alpine AS release

WORKDIR usr/share/caddy

COPY --from=build /frontend/dist /usr/share/caddy
