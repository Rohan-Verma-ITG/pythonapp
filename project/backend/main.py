"""
FastAPI app entry point.

Run with:
uvicorn backend.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth import router as auth_router
from backend.routes.posts import router as posts_router

app = FastAPI(title="Instagram Feed Clone API")

# Allow Streamlit frontend to call this backend from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Beginner-friendly (open). Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Simple health route."""
    return {"message": "Backend is running"}


# Include route modules.
app.include_router(auth_router)
app.include_router(posts_router)
