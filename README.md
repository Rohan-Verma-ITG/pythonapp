# Shopify Helpdesk Embedded App (FastAPI + Remix)

Production-oriented multi-tenant Shopify public app architecture for shared inbox, ticketing, AI assistant, automation, and Shopify sync.

## Architecture

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL + Celery/Redis + WebSockets
- **Frontend**: Remix + React + Shopify Polaris + App Bridge-ready embedded shell
- **Integrations**: Shopify OAuth + GraphQL Admin API + mandatory webhooks

## Backend structure

```
/backend
  /ai
  /auth
  /core
  /db
  /models
  /routes
  /schemas
  /services
  /webhooks
  main.py
```

## Frontend structure

```
/frontend
  /app
    /components
    /hooks
    /routes
    /services
```

## Required DB schema

Implemented models: `shops`, `users`, `customers`, `orders`, `conversations`, `messages`, `tickets`, `automation_rules` with shop-scoped indexes/constraints for multi-tenancy.

## Mandatory OAuth + webhooks

- OAuth endpoints:
  - `GET /auth/install`
  - `GET /auth/callback`
- Webhooks endpoint:
  - `POST /webhooks/shopify`
  - Handles: `customers/create`, `customers/update`, `orders/create`, `orders/updated`, `app/uninstalled`

## API surface

- Customers: `GET /customers`, `GET /customers/{id}`
- Conversations: `GET /conversations`, `POST /conversations`, `GET /messages/{conversation_id}`
- Messages: `POST /messages`
- Tickets: CRUD under `/tickets`
- AI: `POST /ai/suggest-reply`, `POST /ai/auto-reply`
- Realtime: `WS /ws/chat/{shop_id}`

## Run locally

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

- Backend: Render/AWS (container)
- Frontend: Vercel/Remix host
- Set webhook subscriptions during install and after token rotation.

