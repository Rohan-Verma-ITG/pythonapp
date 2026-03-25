from fastapi import FastAPI

from backend.ai.routes import router as ai_router
from backend.auth.routes import router as auth_router
from backend.db.session import Base, engine
from backend.routes.conversations import router as conversations_router
from backend.routes.customers import router as customers_router
from backend.routes.messages import router as messages_router
from backend.routes.tickets import router as tickets_router
from backend.routes.ws import router as ws_router
from backend.webhooks.routes import router as webhooks_router

app = FastAPI(title='Shopify Helpdesk App')


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(customers_router)
app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(tickets_router)
app.include_router(ai_router)
app.include_router(ws_router)


@app.get('/health')
def health():
    return {'ok': True}
