"""
Small helper functions for calling the FastAPI backend.

Keeping API calls in one file makes app.py easier to read.
"""

import requests

BASE_URL = "http://127.0.0.1:8000"


def signup(email: str, password: str):
    """Call POST /signup."""
    return requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password}, timeout=15)


def login(email: str, password: str):
    """Call POST /login."""
    return requests.post(f"{BASE_URL}/login", json={"email": email, "password": password}, timeout=15)


def create_post(uid: str, email: str, caption: str, image_base64: str | None = None):
    """Call POST /posts."""
    payload = {
        "uid": uid,
        "email": email,
        "caption": caption,
        "image_base64": image_base64,
    }
    return requests.post(f"{BASE_URL}/posts", json=payload, timeout=15)


def get_posts():
    """Call GET /posts."""
    return requests.get(f"{BASE_URL}/posts", timeout=15)
