from celery import Celery

from backend.core.config import settings


celery_app = Celery('shopify_helpdesk', broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def process_delayed_order_alert(shop_id: int, order_id: str):
    return {'shop_id': shop_id, 'order_id': order_id, 'status': 'queued'}
