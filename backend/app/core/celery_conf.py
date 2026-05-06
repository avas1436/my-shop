# app/core/celery_conf.py
from __future__ import annotations

from datetime import timedelta

from celery import Celery
from kombu import Exchange, Queue

from app.config.settings import get_settings

settings = get_settings()


celery_app = Celery(
    "worker",
    broker=settings.redis_broker_url,
    backend=settings.redis_backend_url,
)

# کانفیگ کامل
celery_app.conf.update(
    # ==== Serialization ====
    # موجب امنیت و سازگاری بیشتر میشه
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    # ==== Reliability ====
    task_acks_late=True,  # تسک بعد از اتمام موفق حذف میشه
    task_reject_on_worker_lost=True,  # اگر وسط کار کرش کرد دوباره شروع به فعالیت میکند
    worker_prefetch_multiplier=1,  # مانع از ایجاد چندین تسک همزمان برای یک ورکر میشه
    # ==== Retry & Limits ====
    task_default_retry_delay=10,  # ثانیه
    task_max_retries=3,  # حداکثر تلاش مجدد پیش فرض
    task_time_limit=300,  # حداکثر زمان انتظار برای اتمام یک تسک
    task_soft_time_limit=280,  # به جای مجبور کردن به خاموش شدن تسک نرم خاموش میشود
    # ==== Result / Backend ====
    result_expires=timedelta(days=1),  # نتایج بعد از ۱ روز پاک شود
    result_backend_transport_options={
        "retry_policy": {"timeout": 5},
    },
    # ==== Broker Transport ====
    broker_transport_options={
        "visibility_timeout": 3600,  # برای کارهای طولانی
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.5,
        "interval_max": 5,
    },
    # ==== Task Routing ====
    task_default_queue="default",
    task_queues=(
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("critical", Exchange("critical"), routing_key="critical"),
    ),
    task_routes={
        "app.tasks.critical_task": {"queue": "critical", "routing_key": "critical"},
    },
    # ==== Worker ====
    worker_max_tasks_per_child=100,  # جلوگیری از memory leak
    worker_disable_rate_limits=False,  # محدود کردن تعداد انجام تسک
)


# روش استفاده از خاموش شدن نرم
# @celery_app.task
# def long_job():
#     try:
#         do_something()
#     except SoftTimeLimitExceeded:
#         cleanup_temp_files()


# Flower
celery_app.conf.update(
    flower_basic_auth=f"{settings.flower_user}:{settings.flower_pass}",
    flower_port=5555,
)
