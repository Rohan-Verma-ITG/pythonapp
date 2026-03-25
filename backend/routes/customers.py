from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Customer


router = APIRouter(prefix='/customers', tags=['customers'])


@router.get('')
def list_customers(shop_id: int, q: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Customer).filter(Customer.shop_id == shop_id)
    if q:
        query = query.filter(Customer.email.ilike(f'%{q}%'))
    return query.limit(100).all()


@router.get('/{customer_id}')
def get_customer(customer_id: int, shop_id: int, db: Session = Depends(get_db)):
    return db.query(Customer).filter(Customer.shop_id == shop_id, Customer.id == customer_id).first()
