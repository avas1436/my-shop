# Dockerfile

# ===== Base =====
FROM node:20-slim AS base

WORKDIR /frontend

ENV NODE_ENV=production
ENV VITE_ENV=production

COPY package.json package-lock.json ./

RUN npm ci --no-audit --no-fund


# ===== Build Stage =====
FROM base AS build

WORKDIR /frontend

COPY . .


RUN npm run build


# ===== Final Stage =====
FROM caddy:2-alpine AS release

WORKDIR /usr/share/caddy

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /frontend/dist /usr/share/caddy


EXPOSE 80
