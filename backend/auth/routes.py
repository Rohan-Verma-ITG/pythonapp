import secrets

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Shop
from backend.services.shopify import exchange_code, install_url, verify_hmac


router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/install')
def install(shop: str = Query(...)):
    state = secrets.token_urlsafe(20)
    return RedirectResponse(install_url(shop, state))


@router.get('/callback')
async def callback(request: Request, db: Session = Depends(get_db)):
    params = dict(request.query_params)
    if not verify_hmac(params):
        raise HTTPException(status_code=400, detail='Invalid HMAC')

    payload = await exchange_code(params['shop'], params['code'])
    shop = db.query(Shop).filter_by(shop_domain=params['shop']).first()
    if not shop:
        shop = Shop(shop_domain=params['shop'], access_token=payload['access_token'])
        db.add(shop)
    else:
        shop.access_token = payload['access_token']
    db.commit()
    return {'ok': True, 'shop': params['shop']}
