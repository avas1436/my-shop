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
RUN pip install -i https://pypi.iranserver.com/repository/pypi/simple uv


# ===== Dependencies (builder) =====
FROM base AS builder

# این محل از محیط لوکال نیست صرفا یک فولدر داخل کانتینر ایجاد خواهد شد
# container working directory
WORKDIR /backend


# Install dependencies
# این دو فایل از محیط کنار داکرفایل کپی میشه به پوشه بک اند داخل ایمیج
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --verbose --no-dev --system-certs

# ===== Final lightweight image =====
FROM base AS final

WORKDIR /backend

# کپی کردن تمام پکیج‌های نصب شده از مرحله قبل
COPY --from=builder /backend/.venv /backend/.venv

# کپی کردن کدهای پروژه
COPY . .

# اضافه کردن محیط مجازی به PATH سیستم برای دسترسی راحت به دستورات
ENV PATH="/backend/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run service
CMD ["uv", "run", "--no-dev", "gunicorn", "main:app","--worker-class", "uvicorn.workers.UvicornWorker","--workers", "2","--bind", "0.0.0.0:8000","--timeout", "60","--keep-alive", "5","--graceful-timeout", "30","--worker-tmp-dir", "/dev/shm","--log-level", "info","--access-logfile", "-","--error-logfile", "-"]



