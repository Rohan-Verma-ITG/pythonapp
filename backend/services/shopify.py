import hashlib
import hmac
from urllib.parse import urlencode

import httpx

from backend.core.config import settings


def install_url(shop: str, state: str) -> str:
    params = {
        'client_id': settings.shopify_api_key,
        'scope': settings.shopify_scopes,
        'redirect_uri': f"{settings.shopify_app_url}/auth/callback",
        'state': state,
    }
    return f"https://{shop}/admin/oauth/authorize?{urlencode(params)}"


async def exchange_code(shop: str, code: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"https://{shop}/admin/oauth/access_token",
            json={
                'client_id': settings.shopify_api_key,
                'client_secret': settings.shopify_api_secret,
                'code': code,
            },
        )
        resp.raise_for_status()
        return resp.json()


def verify_hmac(params: dict) -> bool:
    qs = '&'.join(f'{k}={v}' for k, v in sorted(params.items()) if k != 'hmac')
    expected = hmac.new(settings.shopify_api_secret.encode(), qs.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, params.get('hmac', ''))


def verify_webhook_hmac(raw_body: bytes, hmac_header: str) -> bool:
    digest = hmac.new(settings.shopify_api_secret.encode(), raw_body, hashlib.sha256).digest()
    calculated = __import__('base64').b64encode(digest).decode()
    return hmac.compare_digest(calculated, hmac_header)


async def graphql(shop_domain: str, access_token: str, query: str, variables: dict | None = None):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"https://{shop_domain}/admin/api/2025-10/graphql.json",
            headers={'X-Shopify-Access-Token': access_token},
            json={'query': query, 'variables': variables or {}},
        )
        resp.raise_for_status()
        payload = resp.json()
        if payload.get('errors'):
            raise ValueError(payload['errors'])
        return payload['data']
