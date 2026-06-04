# Dockerfile

# ===== Base =====
FROM node:20-slim AS base

WORKDIR /frontend

RUN corepack enable

# COPY package.json package-lock.json ./
COPY package.json pnpm-lock.yaml ./

# RUN npm ci --no-audit --no-fund
RUN pnpm install --frozen-lockfile

# ===== Build Stage =====
FROM base AS build

WORKDIR /frontend

COPY --from=base /frontend/node_modules ./node_modules
COPY . .


RUN npm run build


# ===== Final Stage =====
FROM caddy:2-alpine AS release

WORKDIR /usr/share/caddy

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /frontend/dist /usr/share/caddy


EXPOSE 80
