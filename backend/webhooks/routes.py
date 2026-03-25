from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Customer, Order, Shop
from backend.services.shopify import verify_webhook_hmac


router = APIRouter(prefix='/webhooks', tags=['webhooks'])


@router.post('/shopify')
async def handle_shopify_webhook(
    request: Request,
    x_shopify_topic: str = Header(...),
    x_shopify_shop_domain: str = Header(...),
    x_shopify_hmac_sha256: str = Header(...),
    db: Session = Depends(get_db),
):
    raw = await request.body()
    if not verify_webhook_hmac(raw, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail='Invalid webhook signature')

    payload = await request.json()
    shop = db.query(Shop).filter(Shop.shop_domain == x_shopify_shop_domain).first()
    if not shop:
        return {'ignored': True}

    if x_shopify_topic in ('customers/create', 'customers/update'):
        customer = db.query(Customer).filter_by(shop_id=shop.id, shopify_customer_id=str(payload['id'])).first()
        if not customer:
            customer = Customer(shop_id=shop.id, shopify_customer_id=str(payload['id']))
            db.add(customer)
        customer.email = payload.get('email')
        customer.name = f"{payload.get('first_name', '')} {payload.get('last_name', '')}".strip() or None
        customer.metadata = payload

    elif x_shopify_topic in ('orders/create', 'orders/updated'):
        customer_id = None
        if payload.get('customer'):
            customer = db.query(Customer).filter_by(shop_id=shop.id, shopify_customer_id=str(payload['customer']['id'])).first()
            customer_id = customer.id if customer else None
        order = db.query(Order).filter_by(shop_id=shop.id, shopify_order_id=str(payload['id'])).first()
        if not order:
            order = Order(shop_id=shop.id, shopify_order_id=str(payload['id']), customer_id=customer_id)
            db.add(order)
        order.status = payload.get('financial_status')
        order.total_price = payload.get('total_price')
        order.metadata = payload

    elif x_shopify_topic == 'app/uninstalled':
        db.delete(shop)

    db.commit()
    return {'ok': True}
