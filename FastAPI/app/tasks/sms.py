# app/tasks/sms.py
from app.core.celery_conf import celery_app
from app.core.sms_service import send_sms


@celery_app.task(bind=True, max_retries=3)
def send_sms_task(self, receptor: str, code: str):
    try:
        return send_sms(receptor=receptor, code=code)
    except Exception as exc:
        # اگر ارسال شکست خورد، تا 3 بار با فاصله 10 ثانیه تکرار می‌شود
        raise self.retry(exc=exc, countdown=10) from exc
