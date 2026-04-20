# Dockerfile

# ===== Base =====
FROM python:3.12-slim AS base

# نمایش لاگ های پایتون
ENV PYTHONUNBUFFERED=1
# عدم ایجاد کش پایتون برای ایمیج کوچک تر
ENV PYTHONDONTWRITEBYTECODE=1
# عدم ایجاد محیط مجازی توسط یو وی
ENV UV_SYSTEM_PYTHON=1

# install uv
RUN pip install -i https://mirror-pypi.runflare.com/ uv


# ===== Dependencies (builder) =====
FROM base AS builder

# این محل از محیط لوکال نیست صرفا یک فولدر داخل کانتینر ایجاد خواهد شد
# container working directory
WORKDIR /backend


# Install dependencies
# این دو فایل از محیط کنار داکرفایل کپی میشه به پوشه بک اند داخل ایمیج
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --verbose --no-dev

# ===== Final lightweight image =====
FROM base AS final

WORKDIR /backend

# Copy virtualenv (from builder)
COPY --from=builder /backend/.venv /backend/.venv
# Copy actual application source (from repo)
COPY . .


# Run service
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
